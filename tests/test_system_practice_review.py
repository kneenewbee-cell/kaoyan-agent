from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.system_library import SystemQuestionLibrary
from materials.system_ai_planner import (
    generate_ai_review_plan_draft,
    _fallback_review_plan_draft,
    _call_planning_model,
    _context_candidate_lookup,
    _normalize_ai_plan_payload,
    _plan_item_load_minutes,
    _planning_prompt,
)
from materials.system_review_plan_load import (
    calculate_candidate_load,
    calculate_question_load_units,
    estimate_minutes_from_load,
    split_candidate_into_plan_segments,
)
from materials.system_practice_review import PRACTICE_ATTEMPT_FILENAME, PRACTICE_ATTEMPT_ITEM_FILENAME, SystemPracticeReviewStore
from materials.system_practice_review_api import router as system_practice_review_router
from materials.system_review_plan_evaluator import (
    build_synthetic_ai_planning_context,
    build_persona_catalog,
    evaluate_deterministic_planner_for_personas,
    evaluate_full_ai_plan_flow_for_personas,
    evaluate_mode_candidate_budget_for_personas,
    evaluate_ai_planner_sample_for_personas,
    evaluate_mode_readiness_for_personas,
    evaluate_mode_policy_for_personas,
    _evaluate_plan_items_against_context,
)
from materials.system_review_plan_policy import build_ai_candidate_limits, build_ai_review_plan_policy
from materials.user_state import UserSystemQuestionStateStore


class SystemPracticeReviewTest(unittest.TestCase):
    def test_practice_attempt_create_save_submit_and_lock_answers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )

            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            updated = store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": " a "},
                    "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"},
                    "kaoyan_math1_2099_q004": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            listed = store.list_practice_attempts("tester", practice_set_id=practice_set["set_id"])

            self.assertEqual(attempt["status"], "draft")
            self.assertEqual(attempt["practice_set_id"], practice_set["set_id"])
            self.assertEqual(updated["answers"]["kaoyan_math1_2099_q002"]["value"], "a")
            self.assertEqual(submitted["status"], "submitted")
            self.assertIsNotNone(submitted["submitted_at"])
            self.assertGreaterEqual(submitted["duration_seconds"], 0)
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q002"]["status"], "correct")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q003"]["status"], "pending_review")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q004"]["status"], "incorrect")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q005"]["status"], "unanswered")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q006"]["status"], "incorrect")
            self.assertEqual(
                submitted["summary"],
                {
                    "total": 5,
                    "correct": 1,
                    "incorrect": 2,
                    "partial": 0,
                    "pending_review": 1,
                    "unanswered": 1,
                },
            )
            self.assertEqual(listed[0]["attempt_id"], attempt["attempt_id"])
            self.assertTrue((users_root / "tester" / "system_library" / "practice_attempts.jsonl").exists())
            with self.assertRaises(ValueError):
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"}},
                )

    def test_practice_attempt_submit_writes_item_and_stats_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )

            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            items = store.list_practice_attempt_items("tester", attempt_id=attempt["attempt_id"])
            question_stats = store.list_user_question_stats("tester")
            topic_stats = store.list_user_topic_stats("tester")

            self.assertEqual(submitted["status"], "submitted")
            self.assertEqual(len(items), 5)
            item_by_question = {item["question_id"]: item for item in items}
            self.assertEqual(item_by_question["kaoyan_math1_2099_q002"]["final_status"], "correct")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["final_status"], "incorrect")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["standard_answer"], "42")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["judge_method"], "local")
            self.assertTrue((users_root / "tester" / "system_library" / "practice_attempt_items.jsonl").exists())
            self.assertTrue((users_root / "tester" / "system_library" / "user_question_stats.jsonl").exists())
            self.assertTrue((users_root / "tester" / "system_library" / "user_topic_stats.jsonl").exists())
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["attempt_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["correct_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["incorrect_count"], 1)
            self.assertTrue(any(stat["topic"] == "limits" for stat in topic_stats.values()))

    def test_pending_review_backfills_legacy_submitted_attempt_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"}},
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])

            records = store._read_records("tester", PRACTICE_ATTEMPT_FILENAME, "attempt_id")
            records[0]["results"]["kaoyan_math1_2099_q003"].pop("final_status", None)
            records[0]["results"]["kaoyan_math1_2099_q003"]["status"] = "needs_grading"
            store._write_records("tester", PRACTICE_ATTEMPT_FILENAME, records)
            item_path = users_root / "tester" / "system_library" / PRACTICE_ATTEMPT_ITEM_FILENAME
            item_path.unlink()

            pending = store.list_pending_review_items("tester", subject="math")
            insights = store.build_learning_insights("tester", subject="math")

            self.assertEqual(pending["total"], 1)
            self.assertEqual(pending["items"][0]["question_id"], "kaoyan_math1_2099_q003")
            self.assertEqual(pending["items"][0]["final_status"], "pending_review")
            self.assertEqual(insights["summary"]["pending_review_count"], 1)
            self.assertEqual(insights["summary"]["pending_review_question_count"], 1)
            self.assertTrue(item_path.exists())

    def test_practice_attempt_submit_marks_answered_questions_learning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            state_store = UserSystemQuestionStateStore(base_dir=users_root)
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            state_store.update_question_state(
                "tester",
                "kaoyan_math1_2099_q002",
                {"mastery_status": "mastered", "is_favorite": True},
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"},
                    "kaoyan_math1_2099_q004": {"answer_type": "choice", "value": "B"},
                },
            )

            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            states = state_store.list_question_states(
                "tester",
                [
                    "kaoyan_math1_2099_q002",
                    "kaoyan_math1_2099_q003",
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q005",
                ],
            )

            self.assertEqual(states["kaoyan_math1_2099_q002"]["mastery_status"], "mastered")
            self.assertTrue(states["kaoyan_math1_2099_q002"]["is_favorite"])
            self.assertEqual(states["kaoyan_math1_2099_q003"]["mastery_status"], "learning")
            self.assertEqual(states["kaoyan_math1_2099_q004"]["mastery_status"], "learning")
            self.assertEqual(states["kaoyan_math1_2099_q005"]["mastery_status"], "not_started")
            self.assertEqual(
                states["kaoyan_math1_2099_q003"]["last_practiced_at"],
                submitted["submitted_at"],
            )

    def test_practice_attempt_insights_explain_recorded_learning_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])

            insights = store.build_practice_attempt_insights("tester", submitted["attempt_id"])

            self.assertEqual(insights["attempt_id"], submitted["attempt_id"])
            self.assertEqual(insights["record_status"], "recorded")
            self.assertEqual(insights["summary"]["total"], 5)
            self.assertTrue(insights["headline"])
            self.assertTrue(insights["topic_impacts"])
            self.assertTrue(insights["question_impacts"])
            self.assertTrue(insights["next_actions"])
            self.assertTrue(any(action.get("status") == "incorrect" for action in insights["next_actions"]))
            self.assertTrue(any(action.get("topic") == "limits" for action in insights["next_actions"]))
            self.assertIn("practice_attempt_items", insights["recorded_fields"])
            self.assertIn("question_stats_updated", insights["recorded_fields"])
            self.assertIn("topic_stats_updated", insights["recorded_fields"])

    def test_practice_attempt_list_and_learning_insights_do_not_reload_question_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "42"},
                },
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])

            calls: list[str] = []
            original_get_question = store.library.get_question

            def counting_get_question(question_id: str) -> dict:
                calls.append(question_id)
                return original_get_question(question_id)

            store.library.get_question = counting_get_question  # type: ignore[method-assign]

            listed = store.list_practice_attempts("tester")
            insights = store.build_learning_insights("tester")

            self.assertEqual(listed[0]["attempt_id"], submitted["attempt_id"])
            self.assertEqual(insights["summary"]["submitted_attempt_count"], 1)
            self.assertEqual(calls, [])

    def test_question_learning_snapshot_returns_history_and_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])

            snapshot = store.build_question_learning_snapshot("tester", "kaoyan_math1_2099_q002")

            self.assertEqual(snapshot["question_id"], "kaoyan_math1_2099_q002")
            self.assertEqual(snapshot["attempt_count"], 1)
            self.assertEqual(snapshot["correct_count"], 1)
            self.assertEqual(len(snapshot["recent_attempts"]), 1)
            self.assertEqual(snapshot["latest_status"], "correct")

    def test_practice_attempt_submit_is_idempotent_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )

            first = store.submit_practice_attempt("tester", attempt["attempt_id"])
            second = store.submit_practice_attempt("tester", attempt["attempt_id"])
            items = store.list_practice_attempt_items("tester", attempt_id=attempt["attempt_id"])
            question_stats = store.list_user_question_stats("tester")

            self.assertEqual(first["attempt_id"], second["attempt_id"])
            self.assertEqual(first["submitted_at"], second["submitted_at"])
            self.assertEqual(len(items), 5)
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["attempt_count"], 1)

    def test_practice_attempt_records_layered_grading_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                    "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "证明过程"},
                },
            )

            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            choice_result = submitted["results"]["kaoyan_math1_2099_q002"]
            blank_result = submitted["results"]["kaoyan_math1_2099_q006"]
            solution_result = submitted["results"]["kaoyan_math1_2099_q003"]

            self.assertEqual(choice_result["local_status"], "correct")
            self.assertEqual(choice_result["final_status"], "correct")
            self.assertEqual(choice_result["judge_method"], "local")
            self.assertEqual(choice_result["ai_status"], "not_used")
            self.assertEqual(blank_result["local_status"], "incorrect")
            self.assertEqual(blank_result["final_status"], "incorrect")
            self.assertEqual(blank_result["judge_method"], "local")
            self.assertEqual(blank_result["status"], "incorrect")
            self.assertEqual(solution_result["local_status"], "pending_review")
            self.assertEqual(solution_result["final_status"], "pending_review")
            self.assertEqual(solution_result["judge_method"], "manual")
            self.assertEqual(submitted["summary"]["pending_review"], 1)

    def test_ai_grade_override_can_correct_blank_result_and_updates_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])

            corrected = store.apply_practice_item_grade(
                "tester",
                submitted["attempt_id"],
                "kaoyan_math1_2099_q006",
                judge_method="ai",
                final_status="correct",
                judge_confidence=0.91,
                judge_reason="AI 判定用户答案与参考答案等价。",
                ai_feedback="写法不同，但数学含义一致。",
            )
            result = corrected["results"]["kaoyan_math1_2099_q006"]

            self.assertEqual(result["local_status"], "incorrect")
            self.assertEqual(result["ai_status"], "correct")
            self.assertEqual(result["final_status"], "correct")
            self.assertEqual(result["status"], "correct")
            self.assertEqual(result["judge_method"], "ai")
            self.assertEqual(result["judge_confidence"], 0.91)
            self.assertEqual(corrected["summary"]["correct"], 1)
            self.assertEqual(corrected["summary"]["incorrect"], 0)
            items = store.list_practice_attempt_items("tester", attempt_id=submitted["attempt_id"])
            item_by_question = {item["question_id"]: item for item in items}
            question_stats = store.list_user_question_stats("tester")
            topic_stats = store.list_user_topic_stats("tester")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["final_status"], "correct")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["judge_method"], "ai")
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["correct_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["incorrect_count"], 0)
            self.assertTrue(any(stat["correct_count"] >= 1 for stat in topic_stats.values()))

    def test_manual_grade_records_conflict_with_local_or_ai_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            manually_corrected = store.apply_practice_item_grade(
                "tester",
                submitted["attempt_id"],
                "kaoyan_math1_2099_q006",
                judge_method="manual",
                final_status="correct",
                judge_confidence=1,
                judge_reason="用户人工确认正确。",
                manual_override=True,
            )
            result = manually_corrected["results"]["kaoyan_math1_2099_q006"]

            self.assertEqual(result["local_status"], "incorrect")
            self.assertEqual(result["final_status"], "correct")
            self.assertEqual(result["judge_method"], "manual")
            self.assertEqual(result["manual_direction"], "confirm_correct")
            self.assertTrue(result["manual_conflict"])
            self.assertEqual(result["manual_conflict_sources"], ["local"])
            self.assertEqual(result["manual_evidence"], {"local_status": "incorrect", "ai_status": "not_used"})

            items = store.list_practice_attempt_items("tester", attempt_id=submitted["attempt_id"])
            item_by_question = {item["question_id"]: item for item in items}
            item = item_by_question["kaoyan_math1_2099_q006"]
            self.assertEqual(item["manual_direction"], "confirm_correct")
            self.assertTrue(item["manual_conflict"])
            self.assertEqual(item["manual_conflict_sources"], ["local"])

            question_stats = store.list_user_question_stats("tester")
            question_stat = question_stats["kaoyan_math1_2099_q006"]
            self.assertEqual(question_stat["manual_override_count"], 1)
            self.assertEqual(question_stat["manual_conflict_count"], 1)
            topic_stats = store.list_user_topic_stats("tester")
            self.assertTrue(any(int(stat.get("manual_conflict_count") or 0) == 1 for stat in topic_stats.values()))

    def test_manual_grade_records_conflict_with_existing_ai_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            ai_incorrect = store.apply_practice_item_grade(
                "tester",
                submitted["attempt_id"],
                "kaoyan_math1_2099_q006",
                judge_method="ai",
                final_status="incorrect",
                judge_confidence=0.82,
                judge_reason="AI 判定不等价。",
                ai_feedback="参考答案是 42，用户答案是 43。",
            )
            manual_correct = store.apply_practice_item_grade(
                "tester",
                ai_incorrect["attempt_id"],
                "kaoyan_math1_2099_q006",
                judge_method="manual",
                final_status="correct",
                judge_confidence=1,
                judge_reason="用户人工确认正确。",
                manual_override=True,
            )
            result = manual_correct["results"]["kaoyan_math1_2099_q006"]

            self.assertEqual(result["local_status"], "incorrect")
            self.assertEqual(result["ai_status"], "incorrect")
            self.assertEqual(result["final_status"], "correct")
            self.assertEqual(result["manual_conflict_sources"], ["local", "ai"])
            self.assertEqual(result["manual_evidence"], {"local_status": "incorrect", "ai_status": "incorrect"})

    def test_ai_grade_request_uses_grader_result_without_frontend_final_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            seen_context: dict = {}

            def fake_grader(context: dict) -> dict:
                seen_context.update(context)
                return {
                    "final_status": "correct",
                    "judge_confidence": 0.92,
                    "judge_reason": "AI 判定填空答案等价。",
                    "ai_feedback": "表达方式不同，但数学含义一致。",
                }

            graded = store.request_practice_item_ai_grade(
                "tester",
                submitted["attempt_id"],
                "kaoyan_math1_2099_q006",
                grader=fake_grader,
            )
            result = graded["results"]["kaoyan_math1_2099_q006"]

            self.assertEqual(seen_context["answer_type"], "blank")
            self.assertEqual(seen_context["user_answer"], "43")
            self.assertEqual(seen_context["standard_answer"], "42")
            self.assertEqual(result["local_status"], "incorrect")
            self.assertEqual(result["ai_status"], "correct")
            self.assertEqual(result["final_status"], "correct")
            self.assertEqual(result["judge_method"], "ai")
            self.assertEqual(result["judge_confidence"], 0.92)
            self.assertEqual(graded["summary"]["correct"], 1)
            self.assertEqual(graded["summary"]["incorrect"], 0)

    def test_get_practice_attempt_backfills_legacy_blank_local_grade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = {
                "set_id": "set_legacy_blank",
                "title": "legacy blank",
                "question_ids": ["kaoyan_math1_2099_q006"],
                "questions": [],
                "status": "active",
                "created_at": "2026-07-05T00:00:00+00:00",
                "updated_at": "2026-07-05T00:00:00+00:00",
            }
            legacy_attempt = {
                "attempt_id": "attempt_legacy_blank",
                "practice_set_id": "set_legacy_blank",
                "status": "submitted",
                "started_at": "2026-07-05T00:00:00+00:00",
                "submitted_at": "2026-07-05T00:01:00+00:00",
                "answers": {
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
                "results": {
                    "kaoyan_math1_2099_q006": {
                        "question_id": "kaoyan_math1_2099_q006",
                        "answer_type": "blank",
                        "status": "pending_review",
                        "final_status": "pending_review",
                        "standard_answer": "42",
                        "user_answer": "43",
                    },
                },
                "summary": {
                    "total": 1,
                    "correct": 0,
                    "incorrect": 0,
                    "partial": 0,
                    "pending_review": 1,
                    "unanswered": 0,
                },
            }
            store._write_records("tester", "practice_sets.jsonl", [practice_set])
            store._write_records("tester", "practice_attempts.jsonl", [legacy_attempt])

            backfilled = store.get_practice_attempt("tester", "attempt_legacy_blank")
            result = backfilled["results"]["kaoyan_math1_2099_q006"]

            self.assertEqual(result["local_status"], "incorrect")
            self.assertEqual(result["final_status"], "incorrect")
            self.assertEqual(result["status"], "incorrect")
            self.assertEqual(result["judge_method"], "local")
            self.assertEqual(backfilled["summary"]["incorrect"], 1)
            self.assertEqual(backfilled["summary"]["pending_review"], 0)

    def test_practice_attempt_rejects_answers_outside_practice_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=2,
                same_type_only=True,
                exclude_mastered=False,
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])

            with self.assertRaises(ValueError):
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q001": {"answer_type": "choice", "value": "A"}},
                )

    def test_practice_set_selects_by_topic_overlap_but_displays_in_paper_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_practice_order_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            preview = store.preview_practice_candidates(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=4,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=4,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )

            self.assertEqual(preview["items"][0]["question_id"], "kaoyan_math1_2099_q004")
            self.assertEqual(
                practice_set["question_ids"],
                [
                    "kaoyan_math1_2099_q002",
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q003",
                    "kaoyan_math1_2099_q010",
                ],
            )

    def test_practice_ranking_evaluates_weight_presets_with_diverse_samples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_practice_ranking_eval_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            evaluation = store.evaluate_practice_ranking_presets(
                "tester",
                [
                    {
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q002": 3,
                            "kaoyan_math1_2099_q003": 2,
                            "kaoyan_math1_2099_q004": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q010",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q011": 3,
                            "kaoyan_math1_2099_q012": 2,
                            "kaoyan_math1_2099_q013": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q020",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q022": 3,
                            "kaoyan_math1_2099_q021": 2,
                            "kaoyan_math1_2099_q024": 2,
                            "kaoyan_math1_2099_q023": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q030",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q032": 3,
                            "kaoyan_math1_2099_q031": 2,
                            "kaoyan_math1_2099_q034": 2,
                            "kaoyan_math1_2099_q033": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q040",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q042": 3,
                            "kaoyan_math1_2099_q041": 2,
                            "kaoyan_math1_2099_q044": 2,
                            "kaoyan_math1_2099_q043": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q050",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q052": 3,
                            "kaoyan_math1_2099_q051": 2,
                            "kaoyan_math1_2099_q054": 2,
                            "kaoyan_math1_2099_q053": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q060",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q062": 3,
                            "kaoyan_math1_2099_q061": 2,
                            "kaoyan_math1_2099_q064": 2,
                            "kaoyan_math1_2099_q063": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q070",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q072": 3,
                            "kaoyan_math1_2099_q071": 2,
                            "kaoyan_math1_2099_q074": 2,
                            "kaoyan_math1_2099_q073": 1,
                        },
                    },
                    {
                        "source_question_id": "kaoyan_math1_2099_q080",
                        "count": 4,
                        "relevance": {
                            "kaoyan_math1_2098_q082": 3,
                            "kaoyan_math1_2099_q081": 2,
                            "kaoyan_math1_2099_q084": 2,
                            "kaoyan_math1_2099_q083": 1,
                        },
                    },
                ],
            )

            self.assertEqual(evaluation["best_preset"], "topic_first_v2")
            self.assertEqual(evaluation["case_count"], 9)
            self.assertEqual(evaluation["coverage"]["source_question_count"], 9)
            self.assertEqual(evaluation["coverage"]["labelled_candidate_count"], 34)
            self.assertGreaterEqual(len(evaluation["coverage"]["source_topics"]), 20)
            self.assertGreater(
                evaluation["presets"]["topic_first_v2"]["mean_ndcg_at_k"],
                evaluation["presets"]["legacy_linear"]["mean_ndcg_at_k"],
            )
            self.assertGreater(
                evaluation["presets"]["topic_first_v2"]["mean_ndcg_at_k"],
                evaluation["presets"]["type_heavy"]["mean_ndcg_at_k"],
            )
            first_case = evaluation["cases"][0]["presets"]["topic_first_v2"]
            self.assertEqual(first_case["items"][0]["question_id"], "kaoyan_math1_2098_q002")
            self.assertEqual(first_case["items"][0]["score_breakdown"]["shared_topic_count"], 2)
            self.assertEqual(first_case["items"][0]["score_breakdown"]["extra_topic_count"], 0)
            preview = store.preview_practice_candidates(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=2,
                same_type_only=False,
                exclude_mastered=False,
            )
            self.assertEqual(preview["items"][0]["question_id"], "kaoyan_math1_2098_q002")
            self.assertIn("score_breakdown", preview["items"][0])

    def test_practice_attempt_incremental_answer_saves_preserve_existing_answers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])

            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )
            updated = store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "42"}},
            )

            self.assertEqual(updated["answers"]["kaoyan_math1_2099_q002"]["value"], "A")
            self.assertEqual(updated["answers"]["kaoyan_math1_2099_q006"]["value"], "42")

    def test_practice_attempt_api_creates_updates_submits_and_lists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
                patch(
                    "materials.system_practice_review.grade_practice_item_with_ai",
                    return_value={
                        "final_status": "correct",
                        "judge_confidence": 0.88,
                        "judge_reason": "AI 判定两个答案等价。",
                        "ai_feedback": "表达不同但结果一致。",
                    },
                ),
            ):
                practice_response = client.post(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 5,
                        "same_type_only": False,
                        "exclude_mastered": False,
                        "source_scope": "same_year",
                    },
                )
                practice_set = practice_response.json()["practice_set"]
                create_response = client.post(
                    f"/api/materials/system/practice-sets/{practice_set['set_id']}/attempts",
                    params={"user_id": "tester"},
                    json={},
                )
                attempt_id = create_response.json()["practice_attempt"]["attempt_id"]
                update_response = client.patch(
                    f"/api/materials/system/practice-attempts/{attempt_id}/answers",
                    params={"user_id": "tester"},
                    json={
                        "answers": {
                            "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                            "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                        }
                    },
                )
                submit_response = client.post(
                    f"/api/materials/system/practice-attempts/{attempt_id}/submit",
                    params={"user_id": "tester"},
                )
                grade_response = client.post(
                    f"/api/materials/system/practice-attempts/{attempt_id}/items/kaoyan_math1_2099_q006/grade",
                    params={"user_id": "tester"},
                    json={
                        "judge_method": "ai",
                        "final_status": "correct",
                        "judge_confidence": 0.88,
                        "judge_reason": "AI 判定两个答案等价。",
                        "ai_feedback": "表达不同但结果一致。",
                    },
                )
                ai_request_response = client.post(
                    f"/api/materials/system/practice-attempts/{attempt_id}/items/kaoyan_math1_2099_q006/grade",
                    params={"user_id": "tester"},
                    json={"judge_method": "ai"},
                )
                locked_response = client.patch(
                    f"/api/materials/system/practice-attempts/{attempt_id}/answers",
                    params={"user_id": "tester"},
                    json={"answers": {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"}}},
                )
                list_response = client.get(
                    "/api/materials/system/practice-attempts",
                    params={"user_id": "tester", "practice_set_id": practice_set["set_id"]},
                )

            self.assertEqual(create_response.status_code, 200)
            self.assertEqual(create_response.json()["practice_attempt"]["status"], "draft")
            self.assertEqual(update_response.status_code, 200)
            self.assertEqual(update_response.json()["practice_attempt"]["answers"]["kaoyan_math1_2099_q006"]["value"], "43")
            self.assertEqual(submit_response.status_code, 200)
            self.assertEqual(submit_response.json()["practice_attempt"]["status"], "submitted")
            self.assertEqual(submit_response.json()["practice_attempt"]["summary"]["correct"], 1)
            self.assertEqual(grade_response.status_code, 200)
            graded_result = grade_response.json()["practice_attempt"]["results"]["kaoyan_math1_2099_q006"]
            self.assertEqual(graded_result["final_status"], "correct")
            self.assertEqual(graded_result["judge_method"], "ai")
            self.assertEqual(grade_response.json()["practice_attempt"]["summary"]["correct"], 2)
            self.assertEqual(ai_request_response.status_code, 200)
            ai_result = ai_request_response.json()["practice_attempt"]["results"]["kaoyan_math1_2099_q006"]
            self.assertEqual(ai_result["final_status"], "correct")
            self.assertEqual(ai_result["judge_method"], "ai")
            self.assertEqual(locked_response.status_code, 400)
            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(list_response.json()["practice_attempts"][0]["attempt_id"], attempt_id)

    def test_practice_attempt_api_returns_attempt_items_and_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                practice_set = store.create_practice_set(
                    "tester",
                    source_question_id="kaoyan_math1_2099_q001",
                    count=5,
                    same_type_only=False,
                    exclude_mastered=False,
                    source_scope="same_year",
                )
                attempt = store.create_practice_attempt("tester", practice_set["set_id"])
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
                )
                store.submit_practice_attempt("tester", attempt["attempt_id"])

                response = client.get(
                    f"/api/materials/system/practice-attempts/{attempt['attempt_id']}",
                    params={"user_id": "tester"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["practice_attempt"]["attempt_id"], attempt["attempt_id"])
            self.assertEqual(len(payload["items"]), 5)
            self.assertEqual(payload["summary"]["total"], 5)
            self.assertIn("question_stats", payload)
            self.assertIn("topic_stats", payload)
            self.assertEqual(payload["insights"]["record_status"], "recorded")
            self.assertIn("next_actions", payload["insights"])
            self.assertIn("topic_impacts", payload["insights"])
            self.assertEqual(payload["question_stats"]["kaoyan_math1_2099_q002"]["correct_count"], 1)

    def test_question_learning_snapshot_api_returns_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                practice_set = store.create_practice_set(
                    "tester",
                    source_question_id="kaoyan_math1_2099_q001",
                    count=5,
                    same_type_only=False,
                    exclude_mastered=False,
                    source_scope="same_year",
                )
                attempt = store.create_practice_attempt("tester", practice_set["set_id"])
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
                )
                store.submit_practice_attempt("tester", attempt["attempt_id"])

                response = client.get(
                    "/api/materials/system/questions/kaoyan_math1_2099_q002/learning-snapshot",
                    params={"user_id": "tester"},
                )

            self.assertEqual(response.status_code, 200)
            snapshot = response.json()["snapshot"]
            self.assertEqual(snapshot["question_id"], "kaoyan_math1_2099_q002")
            self.assertEqual(snapshot["attempt_count"], 1)
            self.assertEqual(len(snapshot["recent_attempts"]), 1)

    def test_similar_practice_excludes_source_and_sorts_shared_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=3,
                same_type_only=False,
                exclude_mastered=False,
            )

            self.assertNotIn("kaoyan_math1_2099_q001", practice_set["question_ids"])
            self.assertEqual(
                practice_set["question_ids"],
                [
                    "kaoyan_math1_2099_q002",
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q003",
                ],
            )
            self.assertEqual(practice_set["matching_topics"], ["continuity", "limits"])

    def test_similar_practice_can_require_same_type_and_exclude_mastered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            UserSystemQuestionStateStore(base_dir=users_root).update_question_state(
                "tester",
                "kaoyan_math1_2099_q002",
                {"mastery_status": "mastered"},
            )
            store = self._store(raw_root, users_root)

            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=3,
                same_type_only=True,
                exclude_mastered=True,
            )

            self.assertNotIn("kaoyan_math1_2099_q002", practice_set["question_ids"])
            self.assertNotIn("kaoyan_math1_2099_q003", practice_set["question_ids"])
            self.assertEqual(
                practice_set["question_ids"],
                [
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q005",
                ],
            )

    def test_similar_practice_can_filter_by_selected_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                topic_filters=["derivatives"],
            )

            self.assertEqual(practice_set["question_ids"], ["kaoyan_math1_2099_q005"])
            self.assertEqual(practice_set["criteria"]["topic_filters"], ["derivatives"])

    def test_similar_practice_can_limit_scope_to_same_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )

            self.assertEqual(
                practice_set["question_ids"],
                [
                    "kaoyan_math1_2099_q002",
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q005",
                    "kaoyan_math1_2099_q003",
                ],
            )
            self.assertEqual(practice_set["criteria"]["source_scope"], "same_year")

    def test_practice_set_api_accepts_topic_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 5,
                        "topic_filters": ["derivatives"],
                        "source_scope": "same_library",
                    },
                )

            self.assertEqual(response.status_code, 200)
            practice_set = response.json()["practice_set"]
            self.assertEqual(practice_set["question_ids"], ["kaoyan_math1_2099_q005"])
            self.assertEqual(practice_set["criteria"]["topic_filters"], ["derivatives"])
            self.assertEqual(practice_set["criteria"]["source_scope"], "same_library")

    def test_practice_candidate_api_uses_same_scope_and_topic_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/practice-candidates",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 5,
                        "topic_filters": ["derivatives"],
                        "source_scope": "same_library",
                    },
                )

            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["total"], 1)
            self.assertEqual(body["items"][0]["question_id"], "kaoyan_math1_2099_q005")

    def test_practice_candidate_api_infers_exam_type_from_source_question(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            math2_year_dir = raw_root / "math" / "exam_papers" / "math2" / "2099"
            math2_questions_dir = math2_year_dir / "questions"
            math2_questions_dir.mkdir(parents=True)
            rows = [
                self._row("kaoyan_math2_2099_q001", 1, "single_choice", ["limits", "continuity"]),
                self._row("kaoyan_math2_2099_q002", 2, "single_choice", ["limits", "continuity"]),
                self._row("kaoyan_math2_2099_q003", 3, "solution", ["limits"]),
            ]
            for row in rows:
                row["exam_id"] = "kaoyan_math2_2099"
                row["exam_type"] = "math2"
            (math2_year_dir / "questions.jsonl").write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                encoding="utf-8",
            )
            for row in rows:
                number = int(row["question_number"])
                (math2_questions_dir / f"q{number:03d}.md").write_text(
                    "\n".join(
                        [
                            "---",
                            f"question_id: {row['question_id']}",
                            "---",
                            "",
                            "## Question",
                            "",
                            f"Math2 question {number}",
                            "",
                            "## Answer",
                            "",
                            "A",
                        ]
                    ),
                    encoding="utf-8",
                )
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/practice-candidates",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math2_2099_q001",
                        "count": 5,
                        "same_type_only": False,
                        "exclude_mastered": False,
                        "source_scope": "exam_type",
                        "exam_type": "math1",
                    },
                )

            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["source_question"]["exam_type"], "math2")
            self.assertEqual([item["question_id"] for item in body["items"]], ["kaoyan_math2_2099_q002", "kaoyan_math2_2099_q003"])

    def test_practice_set_api_persists_lists_gets_and_deletes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                create_response = client.post(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 2,
                        "same_type_only": True,
                        "exclude_mastered": False,
                    },
                )
                list_response = client.get(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                )
                persisted_after_create = (
                    users_root / "tester" / "system_library" / "practice_sets.jsonl"
                ).exists()
                practice_set_id = create_response.json()["practice_set"]["set_id"]
                detail_response = client.get(
                    f"/api/materials/system/practice-sets/{practice_set_id}",
                    params={"user_id": "tester"},
                )
                delete_response = client.delete(
                    f"/api/materials/system/practice-sets/{practice_set_id}",
                    params={"user_id": "tester"},
                )
                empty_response = client.get(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                )

            self.assertEqual(create_response.status_code, 200)
            created = create_response.json()["practice_set"]
            self.assertEqual(created["source_question_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(created["question_ids"], ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"])
            self.assertEqual(created["status"], "active")
            self.assertTrue(persisted_after_create)

            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(list_response.json()["total"], 1)
            self.assertEqual(list_response.json()["items"][0]["set_id"], practice_set_id)

            self.assertEqual(detail_response.status_code, 200)
            self.assertEqual(detail_response.json()["practice_set"]["set_id"], practice_set_id)

            self.assertEqual(delete_response.status_code, 200)
            self.assertTrue(delete_response.json()["deleted"])
            self.assertEqual(empty_response.json()["items"], [])

    def test_review_task_api_creates_lists_patches_and_deletes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                create_response = client.post(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                    json={
                        "target_type": "question",
                        "target_id": "kaoyan_math1_2099_q001",
                        "title": "Review source question",
                        "due_at": "2099-01-01T00:00:00+00:00",
                        "priority": 3,
                        "note": "redo without hints",
                    },
                )
                list_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                )
                review_task_id = create_response.json()["review_task"]["task_id"]
                patch_response = client.patch(
                    f"/api/materials/system/review-tasks/{review_task_id}",
                    params={"user_id": "tester"},
                    json={"status": "completed", "note": "done"},
                )
                delete_response = client.delete(
                    f"/api/materials/system/review-tasks/{review_task_id}",
                    params={"user_id": "tester"},
                )
                empty_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                )

            self.assertEqual(create_response.status_code, 200)
            created = create_response.json()["review_task"]
            self.assertEqual(created["target_type"], "question")
            self.assertEqual(created["target_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(created["status"], "pending")
            self.assertIsNone(created["completed_at"])

            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(list_response.json()["items"][0]["task_id"], review_task_id)

            self.assertEqual(patch_response.status_code, 200)
            patched = patch_response.json()["review_task"]
            self.assertEqual(patched["status"], "completed")
            self.assertEqual(patched["note"], "done")
            self.assertIsNotNone(patched["completed_at"])

            self.assertEqual(delete_response.status_code, 200)
            self.assertTrue(delete_response.json()["deleted"])
            self.assertEqual(empty_response.json()["items"], [])

    def test_review_task_inherits_source_metadata_and_deduplicates_same_due_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            first = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q001",
                due_at="2099-01-01",
                priority=3,
            )
            second = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q001",
                due_at="2099-01-01",
                priority=5,
                note="same day should not duplicate",
            )
            tasks = store.list_review_tasks("tester")

            self.assertEqual(first["task_id"], second["task_id"])
            self.assertEqual(len(tasks), 1)
            self.assertEqual(first["subject"], "math")
            self.assertEqual(first["exam_type"], "math1")
            self.assertEqual(first["library_name"], "数一历年真题")
            self.assertEqual(first["source_title"], "2099 数一 Q1")
            self.assertTrue(second["duplicate"])

    def test_review_tasks_filter_and_summary_for_planning_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            math_task = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q001",
                due_at="2099-01-01",
            )
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=2,
                same_type_only=True,
                exclude_mastered=False,
                title="同类训练：极限",
            )
            practice_task = store.create_review_task(
                "tester",
                target_type="practice_set",
                target_id=practice_set["set_id"],
                due_at="2099-01-02",
            )
            store.update_review_task("tester", math_task["task_id"], {"status": "completed"})

            math_items = store.list_review_tasks("tester", subject="math")
            practice_items = store.list_review_tasks("tester", target_type="practice_set")
            keyword_items = store.list_review_tasks("tester", keyword="极限")
            completed_items = store.list_review_tasks("tester", status="completed")
            future_items = store.list_review_tasks("tester", date_group="future")
            summary = store.review_task_summary("tester")

            self.assertEqual([item["task_id"] for item in math_items], [practice_task["task_id"], math_task["task_id"]])
            self.assertEqual([item["task_id"] for item in practice_items], [practice_task["task_id"]])
            self.assertEqual([item["task_id"] for item in keyword_items], [practice_task["task_id"]])
            self.assertEqual([item["task_id"] for item in completed_items], [math_task["task_id"]])
            self.assertEqual([item["task_id"] for item in future_items], [practice_task["task_id"]])
            self.assertEqual(practice_task["library_name"], "数一历年真题")
            self.assertEqual(summary["by_subject"]["math"]["total"], 2)
            self.assertEqual(summary["by_target_type"]["question"], 1)
            self.assertEqual(summary["by_target_type"]["practice_set"], 1)

    def test_review_task_actions_cancel_restore_postpone_and_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            task = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q001",
                due_at="2099-01-01",
            )
            cancelled = store.update_review_task("tester", task["task_id"], {"status": "cancelled"})
            restored = store.update_review_task(
                "tester",
                task["task_id"],
                {"status": "pending", "due_at": "2099-01-02"},
            )
            completed = store.update_review_task("tester", task["task_id"], {"status": "completed"})

            self.assertEqual(cancelled["status"], "cancelled")
            self.assertIsNotNone(cancelled["cancelled_at"])
            self.assertEqual(restored["status"], "pending")
            self.assertEqual(restored["due_at"], "2099-01-02")
            self.assertIsNone(restored["cancelled_at"])
            self.assertEqual(completed["status"], "completed")
            self.assertIsNotNone(completed["completed_at"])

    def test_review_task_feedback_events_feed_ai_planning_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            task = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q001",
                due_at="2099-01-01",
                created_from="ai_plan",
                plan_id="plan_20990101",
                plan_mode="weakness",
                plan_source="llm",
                plan_batch_title="AI weekly plan",
                plan_reason="Limits stayed weak after recent practice.",
            )

            started = store.update_review_task(
                "tester",
                task["task_id"],
                {"feedback_action": "started"},
            )
            postponed = store.update_review_task(
                "tester",
                task["task_id"],
                {"status": "pending", "due_at": "2099-01-03", "feedback_action": "postponed"},
            )
            completed = store.update_review_task(
                "tester",
                task["task_id"],
                {"status": "completed", "feedback_action": "completed"},
            )

            self.assertIsNotNone(started["started_at"])
            self.assertEqual([event["event"] for event in postponed["feedback_events"]], ["started", "postponed"])
            self.assertEqual(completed["last_review_action"], "completed")
            self.assertEqual([event["event"] for event in completed["feedback_events"]], ["started", "postponed", "completed"])
            self.assertEqual(completed["feedback_events"][-1]["plan_id"], "plan_20990101")

            context = store.build_ai_planning_context("tester", subject="math", mode="balanced")
            feedback = context["plan_feedback"]

            self.assertEqual(feedback["total_events"], 3)
            self.assertEqual(feedback["by_action"]["started"], 1)
            self.assertEqual(feedback["by_action"]["postponed"], 1)
            self.assertEqual(feedback["by_action"]["completed"], 1)
            self.assertEqual(feedback["recent_events"][-1]["event"], "completed")

    def test_review_tasks_include_learning_reason_from_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])
            task = store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q006",
                due_at="2099-01-01",
            )

            listed = store.list_review_tasks("tester")

            self.assertEqual(listed[0]["task_id"], task["task_id"])
            self.assertTrue(listed[0]["learning_reasons"])
            self.assertEqual(listed[0]["learning_reasons"][0]["type"], "wrong_history")

    def test_learning_insights_prioritize_weak_topics_and_actions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            first_attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                first_attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "证明过程"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            store.submit_practice_attempt("tester", first_attempt["attempt_id"])
            second_attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                second_attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q004": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            store.submit_practice_attempt("tester", second_attempt["attempt_id"])
            store.create_review_task(
                "tester",
                target_type="question",
                target_id="kaoyan_math1_2099_q006",
                due_at="2000-01-01",
                priority=4,
            )
            store.create_review_task(
                "tester",
                target_type="practice_set",
                target_id=practice_set["set_id"],
                due_at="2099-01-01",
                priority=2,
            )

            insights = store.build_learning_insights("tester", subject="math")

            self.assertEqual(insights["summary"]["practice_attempt_count"], 2)
            self.assertEqual(insights["summary"]["question_attempt_count"], 10)
            self.assertGreaterEqual(insights["summary"]["incorrect_count"], 2)
            self.assertGreaterEqual(insights["summary"]["pending_review_count"], 1)
            self.assertEqual(insights["review_summary"]["overdue_count"], 1)
            self.assertEqual(insights["review_summary"]["future_count"], 1)
            self.assertTrue(insights["weak_topics"])
            self.assertEqual(insights["weak_topics"][0]["topic"], "limits")
            self.assertGreater(insights["weak_topics"][0]["priority_score"], 0)
            self.assertIn("smoothed_error_rate", insights["weak_topics"][0])
            self.assertIn("confidence", insights["weak_topics"][0])
            self.assertTrue(insights["weak_topics"][0]["priority_reasons"])
            self.assertTrue(
                any(
                    reason["type"] in {"risk_confidence", "recent_risk", "pending_review"}
                    for reason in insights["weak_topics"][0]["priority_reasons"]
                )
            )
            action_types = {action["type"] for action in insights["next_actions"]}
            self.assertIn("review_wrong", action_types)
            self.assertIn("confirm_grading", action_types)
            self.assertIn("topic_review", action_types)

    def test_learning_insights_surface_unsubmitted_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=3,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            draft = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                draft["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )

            insights = store.build_learning_insights("tester", subject="math")

            self.assertEqual(insights["summary"]["draft_attempt_count"], 1)
            self.assertEqual(insights["summary"]["submitted_attempt_count"], 0)
            self.assertEqual(insights["summary"]["latest_draft_attempt_id"], draft["attempt_id"])
            self.assertTrue(any(action["type"] == "continue_draft" for action in insights["next_actions"]))

    def test_learning_insights_weights_prioritize_reliable_weak_topic_over_single_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            store._write_records(
                "tester",
                "user_topic_stats.jsonl",
                [
                    {
                        "stat_id": "math__single_pending",
                        "user_id": "tester",
                        "subject": "math",
                        "topic": "single_pending",
                        "attempt_count": 1,
                        "correct_count": 0,
                        "incorrect_count": 0,
                        "partial_count": 0,
                        "pending_review_count": 1,
                        "latest_practiced_at": "2099-01-01T00:00:00+00:00",
                        "representative_wrong_question_ids": [],
                    },
                    {
                        "stat_id": "math__reliable_weak",
                        "user_id": "tester",
                        "subject": "math",
                        "topic": "reliable_weak",
                        "attempt_count": 8,
                        "correct_count": 3,
                        "incorrect_count": 4,
                        "partial_count": 0,
                        "pending_review_count": 1,
                        "latest_practiced_at": "2099-01-01T00:00:00+00:00",
                        "representative_wrong_question_ids": ["kaoyan_math1_2099_q002"],
                    },
                ],
            )

            insights = store.build_learning_insights("tester", subject="math")

            self.assertEqual(insights["weak_topics"][0]["topic"], "reliable_weak")
            self.assertEqual(
                insights["score_weights"],
                {
                    "risk_confidence": 0.5928,
                    "recent_risk": 0.0829,
                    "wrong_streak": 0.0794,
                    "pending_review": 0.0616,
                    "repeated_skip": 0.0679,
                    "unstarted_not_mastered": 0.0466,
                    "manual_signal": 0.0582,
                    "question_importance": 0.0106,
                    "single_correct_relief": 0.9616,
                    "stable_correct_relief": 0.7030,
                    "skip_only_cap": 0.4984,
                    "unstarted_only_cap": 0.4588,
                },
            )

    def test_wrong_question_pool_v2_prioritizes_risk_without_overranking_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            store._write_records(
                "tester",
                "user_question_stats.jsonl",
                [
                    self._question_stat(
                        "kaoyan_math1_2099_q001",
                        ["limits"],
                        attempt_count=8,
                        correct_count=1,
                        incorrect_count=5,
                        latest_status="correct",
                        correct_streak=1,
                        wrong_streak=0,
                    ),
                    self._question_stat(
                        "kaoyan_math1_2099_q002",
                        ["limits", "continuity"],
                        attempt_count=7,
                        incorrect_count=4,
                        partial_count=1,
                        wrong_streak=3,
                    ),
                    self._question_stat(
                        "kaoyan_math1_2099_q003",
                        ["limits", "continuity"],
                        attempt_count=6,
                        unanswered_count=5,
                        latest_status="unanswered",
                        wrong_streak=0,
                    ),
                    self._question_stat(
                        "kaoyan_math1_2099_q004",
                        ["limits"],
                        attempt_count=1,
                        incorrect_count=1,
                    ),
                    self._question_stat(
                        "kaoyan_math1_2099_q006",
                        ["limits"],
                        attempt_count=2,
                        correct_count=2,
                        latest_status="correct",
                        correct_streak=2,
                        wrong_streak=0,
                    ),
                ],
            )

            pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1")
            by_id = {item["question_id"]: item for item in pool["items"]}
            ranked_ids = [item["question_id"] for item in pool["items"]]

            self.assertLess(ranked_ids.index("kaoyan_math1_2099_q002"), ranked_ids.index("kaoyan_math1_2099_q003"))
            self.assertLess(ranked_ids.index("kaoyan_math1_2099_q001"), ranked_ids.index("kaoyan_math1_2099_q004"))
            self.assertIn("kaoyan_math1_2099_q003", ranked_ids)
            self.assertNotIn("kaoyan_math1_2099_q006", ranked_ids)
            self.assertGreater(by_id["kaoyan_math1_2099_q003"]["priority_features"]["repeated_skip"], 0)
            self.assertLessEqual(by_id["kaoyan_math1_2099_q003"]["priority_score"], 0.4984)
            self.assertTrue(by_id["kaoyan_math1_2099_q003"]["priority_reasons"])
            self.assertTrue(
                any(reason["type"] == "repeated_skip" for reason in by_id["kaoyan_math1_2099_q003"]["priority_reasons"])
            )

    def test_learning_priority_v2_relief_drops_more_after_consecutive_correct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            one_correct = self._question_stat(
                "kaoyan_math1_2099_q001",
                ["limits"],
                attempt_count=8,
                correct_count=1,
                incorrect_count=5,
                latest_status="correct",
                correct_streak=1,
                wrong_streak=0,
            )
            stable_correct = self._question_stat(
                "kaoyan_math1_2099_q002",
                ["limits"],
                attempt_count=9,
                correct_count=2,
                incorrect_count=5,
                latest_status="correct",
                correct_streak=2,
                wrong_streak=0,
            )
            active_wrong = self._question_stat(
                "kaoyan_math1_2099_q004",
                ["limits"],
                attempt_count=7,
                correct_count=1,
                incorrect_count=5,
                wrong_streak=2,
            )

            one_score = store._wrong_question_pool_item("tester", self._row("kaoyan_math1_2099_q001", 1, "single_choice", ["limits"]), one_correct, {})["priority_score"]
            stable_score = store._wrong_question_pool_item("tester", self._row("kaoyan_math1_2099_q002", 2, "single_choice", ["limits"]), stable_correct, {})["priority_score"]
            active_score = store._wrong_question_pool_item("tester", self._row("kaoyan_math1_2099_q004", 4, "single_choice", ["limits"]), active_wrong, {})["priority_score"]

            self.assertLess(stable_score, one_score)
            self.assertLess(one_score, active_score)
            self.assertGreater(one_score, active_score * 0.6)

    def test_wrong_question_pool_filters_defaults_top_five_and_creates_practice_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            store._write_records(
                "tester",
                "user_question_stats.jsonl",
                [
                    self._question_stat("kaoyan_math1_2099_q001", ["limits"], attempt_count=2, incorrect_count=1),
                    self._question_stat("kaoyan_math1_2099_q002", ["limits", "continuity"], attempt_count=4, incorrect_count=3),
                    self._question_stat("kaoyan_math1_2099_q003", ["limits", "continuity"], attempt_count=1, pending_review_count=1),
                    self._question_stat("kaoyan_math1_2099_q004", ["limits"], attempt_count=3, partial_count=1),
                    self._question_stat("kaoyan_math1_2099_q005", ["derivatives"], attempt_count=2, correct_count=2),
                    self._question_stat("kaoyan_math1_2099_q006", ["limits"], attempt_count=2, incorrect_count=1),
                ],
            )

            pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1")
            limits_pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1", topic="continuity")
            choice_pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1", question_type="single_choice")
            wrong_pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1", risk_type="wrong")
            pending_pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1", risk_type="pending")
            practice_set = store.create_practice_set_from_wrong_pool(
                "tester",
                question_ids=pool["default_selected_question_ids"][:3],
                title="错题复习",
                subject="math",
                exam_type="math1",
                filters={"topic": "limits"},
            )

            self.assertEqual(pool["total"], 5)
            self.assertEqual(len(pool["default_selected_question_ids"]), 5)
            self.assertIn("continuity", pool["topic_options"])
            self.assertEqual(pool["filters"]["risk_type"], "")
            self.assertTrue(pool["risk_type_options"])
            self.assertIn("wrong", {item["value"] for item in pool["risk_type_options"]})
            self.assertIn("pending", {item["value"] for item in pool["risk_type_options"]})
            self.assertTrue(all(item["wrong_count"] > 0 for item in wrong_pool["items"]))
            self.assertTrue(all(item["pending_review_count"] > 0 for item in pending_pool["items"]))
            self.assertTrue(pool["items"][0]["priority_reasons"])
            self.assertEqual(
                [item["question_id"] for item in limits_pool["items"]],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q003", "kaoyan_math1_2099_q001"],
            )
            self.assertTrue(all(item["question_type"] == "single_choice" for item in choice_pool["items"]))
            self.assertEqual(practice_set["source_type"], "wrong_pool")
            self.assertEqual(practice_set["criteria"]["source"], "wrong_pool")
            self.assertEqual(practice_set["criteria"]["feedback_hook"], "wrong_pool_review_v1")
            self.assertEqual(practice_set["criteria"]["filters"], {"topic": "limits"})

    def test_create_practice_set_from_question_ids_for_single_question_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/practice-sets/from-question-ids",
                    params={"user_id": "tester"},
                    json={
                        "question_ids": ["kaoyan_math1_2099_q001"],
                        "title": "2099 数一 Q1 单题复习",
                        "subject": "math",
                        "exam_type": "math1",
                        "source_type": "review_question",
                        "filters": {"review_task_id": "rt_001"},
                    },
                )

            self.assertEqual(response.status_code, 200)
            practice_set = response.json()["practice_set"]
            self.assertEqual(practice_set["question_ids"], ["kaoyan_math1_2099_q001"])
            self.assertEqual(practice_set["question_count"], 1)
            self.assertEqual(practice_set["source_type"], "review_question")
            self.assertEqual(practice_set["source_question_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(practice_set["title"], "2099 数一 Q1 单题复习")
            self.assertEqual(practice_set["criteria"]["source"], "review_question")
            self.assertEqual(practice_set["criteria"]["selected_question_ids"], ["kaoyan_math1_2099_q001"])
            self.assertEqual(practice_set["criteria"]["filters"], {"review_task_id": "rt_001"})

    def test_pending_review_items_are_question_level_and_exclude_choice_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            store.apply_practice_item_grade(
                "tester",
                submitted["attempt_id"],
                "kaoyan_math1_2099_q002",
                judge_method="manual",
                final_status="pending_review",
                manual_override=True,
            )
            records = store._read_records("tester", PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
            for record in records:
                source_meta = record.setdefault("source_meta", {})
                source_meta["subject"] = "高数"
            solution_record = next(record for record in records if record.get("question_id") == "kaoyan_math1_2099_q003")
            duplicate_solution_record = {
                **solution_record,
                "attempt_item_id": "pai_duplicate_pending_solution",
                "attempt_id": "pa_older_duplicate",
                "submitted_at": "2000-01-01T00:00:00+00:00",
            }
            records.append(duplicate_solution_record)
            store._write_records("tester", PRACTICE_ATTEMPT_ITEM_FILENAME, records)

            pending = store.list_pending_review_items("tester", subject="math", exam_type="math1")
            limits_pending = store.list_pending_review_items("tester", subject="math", exam_type="math1", topic="limits")

            self.assertEqual(pending["total"], 1)
            self.assertEqual(pending["items"][0]["question_id"], "kaoyan_math1_2099_q003")
            self.assertEqual(pending["items"][0]["attempt_id"], submitted["attempt_id"])
            self.assertEqual(pending["items"][0]["answer_type"], "solution")
            self.assertEqual(pending["items"][0]["final_status"], "pending_review")
            self.assertNotIn("kaoyan_math1_2099_q002", {item["question_id"] for item in pending["items"]})
            self.assertIn("continuity", pending["topic_options"])
            self.assertEqual(limits_pending["items"][0]["question_id"], "kaoyan_math1_2099_q003")

    def test_pending_review_items_api_returns_question_level_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"}},
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])

            app = FastAPI()
            app.include_router(system_practice_review_router)
            with patch(
                "materials.system_practice_review_api.SystemPracticeReviewStore",
                lambda: self._store(raw_root, users_root),
            ):
                client = TestClient(app)
                response = client.get(
                    "/api/materials/system/pending-review-items",
                    params={"user_id": "tester", "subject": "math", "exam_type": "math1"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()["pending_review"]
            self.assertEqual(payload["total"], 1)
            self.assertEqual(payload["items"][0]["question_id"], "kaoyan_math1_2099_q003")

    def test_wrong_question_pool_rebuilds_stats_from_attempt_items_when_stats_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])
            stats_path = users_root / "tester" / "system_library" / "user_question_stats.jsonl"
            stats_path.unlink()

            pool = store.list_wrong_question_pool("tester", subject="math", exam_type="math1")

            self.assertGreaterEqual(pool["total"], 2)
            self.assertIn("kaoyan_math1_2099_q002", pool["default_selected_question_ids"])

    def test_wrong_question_pool_api_lists_and_creates_practice_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                store._write_records(
                    "tester",
                    "user_question_stats.jsonl",
                    [
                        self._question_stat("kaoyan_math1_2099_q002", ["limits"], attempt_count=3, incorrect_count=2),
                        self._question_stat("kaoyan_math1_2099_q006", ["limits"], attempt_count=2, incorrect_count=1),
                    ],
                )
                pool_response = client.get(
                    "/api/materials/system/wrong-question-pool",
                    params={"user_id": "tester", "subject": "math", "exam_type": "math1"},
                )
                selected_ids = pool_response.json()["pool"]["default_selected_question_ids"]
                create_response = client.post(
                    "/api/materials/system/practice-sets/from-wrong-pool",
                    params={"user_id": "tester"},
                    json={
                        "question_ids": selected_ids,
                        "title": "错题复习",
                        "subject": "math",
                        "exam_type": "math1",
                        "filters": {"topic": "limits"},
                    },
                )

            self.assertEqual(pool_response.status_code, 200)
            self.assertEqual(pool_response.json()["pool"]["total"], 2)
            self.assertEqual(create_response.status_code, 200)
            self.assertEqual(create_response.json()["practice_set"]["source_type"], "wrong_pool")

    def test_review_task_api_filters_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                create_response = client.post(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                    json={
                        "target_type": "question",
                        "target_id": "kaoyan_math1_2099_q001",
                        "due_at": "2099-01-01",
                    },
                )
                filtered_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester", "subject": "math", "target_type": "question"},
                )
                summary_response = client.get(
                    "/api/materials/system/review-tasks/summary",
                    params={"user_id": "tester"},
                )

            self.assertEqual(create_response.status_code, 200)
            self.assertEqual(filtered_response.status_code, 200)
            self.assertEqual(filtered_response.json()["total"], 1)
            self.assertEqual(filtered_response.json()["items"][0]["subject"], "math")
            self.assertEqual(summary_response.status_code, 200)
            self.assertEqual(summary_response.json()["summary"]["by_subject"]["math"]["total"], 1)

    def test_learning_insights_api_returns_dashboard_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                practice_set = store.create_practice_set(
                    "tester",
                    source_question_id="kaoyan_math1_2099_q001",
                    count=5,
                    same_type_only=False,
                    exclude_mastered=False,
                    source_scope="same_year",
                )
                attempt = store.create_practice_attempt("tester", practice_set["set_id"])
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"}},
                )
                store.submit_practice_attempt("tester", attempt["attempt_id"])

                response = client.get(
                    "/api/materials/system/learning-insights",
                    params={"user_id": "tester", "subject": "math"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["user_id"], "tester")
            self.assertEqual(payload["insights"]["subject"], "math")
            self.assertTrue(payload["insights"]["weak_topics"])
            self.assertTrue(payload["insights"]["next_actions"])

    def test_ai_planning_context_returns_wider_candidate_pool_than_ui(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                practice_set = store.create_practice_set(
                    "tester",
                    source_question_id="kaoyan_math1_2099_q001",
                    count=5,
                    same_type_only=False,
                    exclude_mastered=False,
                    source_scope="same_year",
                )
                attempt = store.create_practice_attempt("tester", practice_set["set_id"])
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {
                        "kaoyan_math1_2099_q003": {"answer_type": "solution", "value": "proof"},
                        "kaoyan_math1_2099_q004": {"answer_type": "choice", "value": "B"},
                        "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                    },
                )
                store.submit_practice_attempt("tester", attempt["attempt_id"])
                store.create_review_task(
                    "tester",
                    target_type="practice_set",
                    target_id=practice_set["set_id"],
                    due_at="2099-01-03",
                    priority=4,
                    note="AI should see scheduled practice",
                )

                response = client.get(
                    "/api/materials/system/ai-planning-context",
                    params={
                        "user_id": "tester",
                        "subject": "math",
                        "days": 7,
                        "daily_minutes": 60,
                        "goal": "补弱",
                    },
                )

            self.assertEqual(response.status_code, 200)
            context = response.json()["context"]
            self.assertEqual(context["constraints"]["days"], 7)
            self.assertEqual(context["constraints"]["daily_minutes"], 60)
            self.assertGreater(context["limits"]["ai_weak_topic_limit"], context["limits"]["ui_weak_topic_limit"])
            self.assertGreater(context["limits"]["ai_wrong_question_limit"], context["limits"]["ui_action_limit"])
            self.assertTrue(context["ai_candidates"]["weak_topics"])
            self.assertTrue(context["ai_candidates"]["wrong_questions"])
            self.assertTrue(context["ai_candidates"]["pending_review_items"])
            self.assertTrue(context["ai_candidates"]["review_tasks"])

    def test_ai_planning_context_enriches_candidates_with_load_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            context = store.build_ai_planning_context(
                "tester",
                subject="math",
                mode="startup",
                days=7,
                daily_minutes=60,
            )

            candidate = context["ai_candidates"]["unstarted_questions"][0]

            self.assertIn("load_units", candidate)
            self.assertIn("estimated_minutes", candidate)
            self.assertIn("question_type_mix", candidate)
            self.assertIn("state_mix", candidate)
            self.assertIn("difficulty_mix", candidate)
            self.assertIn("splittable", candidate)
            self.assertNotIn("explanation", candidate)

    def test_ai_planning_context_wrong_mode_excludes_unstarted_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.get(
                    "/api/materials/system/ai-planning-context",
                    params={
                        "user_id": "tester",
                        "subject": "math",
                        "days": 7,
                        "daily_minutes": 60,
                        "mode": "wrong",
                        "include_types": "unstarted_questions",
                    },
                )

            self.assertEqual(response.status_code, 200)
            context = response.json()["context"]
            self.assertEqual(context["constraints"]["mode"], "wrong")
            self.assertIn("unstarted_questions", context["policy"]["disabled_types"])
            self.assertEqual(context["ai_candidates"].get("unstarted_questions", []), [])

    def test_ai_planning_context_maps_frontend_due_tasks_to_review_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                practice_set = store.create_practice_set(
                    "tester",
                    source_question_id="kaoyan_math1_2099_q001",
                    count=5,
                    same_type_only=False,
                    exclude_mastered=False,
                    source_scope="same_year",
                )
                attempt = store.create_practice_attempt("tester", practice_set["set_id"])
                store.create_review_task(
                    "tester",
                    target_type="practice_set",
                    target_id=practice_set["set_id"],
                    due_at="2099-01-03",
                    priority=4,
                    note="AI should see due practice",
                )

                response = client.get(
                    "/api/materials/system/ai-planning-context",
                    params={
                        "user_id": "tester",
                        "subject": "math",
                        "mode": "weak",
                        "include_types": "due_tasks,draft_attempts",
                    },
                )

            self.assertEqual(response.status_code, 200)
            context = response.json()["context"]
            self.assertIn("review_tasks", context["policy"]["requested_types"])
            self.assertIn("review_tasks", context["policy"]["enabled_types"])
            self.assertIn("draft_attempts", context["policy"]["enabled_types"])
            self.assertTrue(context["ai_candidates"]["review_tasks"])
            self.assertEqual(context["ai_candidates"]["draft_attempts"][0]["attempt_id"], attempt["attempt_id"])

    def test_ai_planning_context_frontend_include_aliases_are_all_recognized(self) -> None:
        policy = build_ai_review_plan_policy(
            "balanced",
            ["due_tasks", "pending_review", "unstarted", "draft", "favorite"],
        )

        self.assertEqual(
            policy["requested_types"],
            [
                "review_tasks",
                "pending_review_items",
                "unstarted_questions",
                "draft_attempts",
                "favorite_unmastered",
            ],
        )
        self.assertIn("review_tasks", policy["enabled_types"])
        self.assertIn("pending_review_items", policy["enabled_types"])
        self.assertIn("unstarted_questions", policy["enabled_types"])
        self.assertIn("draft_attempts", policy["enabled_types"])
        self.assertIn("favorite_unmastered", policy["enabled_types"])

    def test_ai_candidate_limits_scale_with_planning_days(self) -> None:
        policy = build_ai_review_plan_policy(
            "balanced",
            ["wrong_questions", "review_tasks", "draft_attempts"],
        )

        short_limits = build_ai_candidate_limits(policy, days=3, daily_minutes=60)
        week_limits = build_ai_candidate_limits(policy, days=7, daily_minutes=60)

        self.assertLess(short_limits["ai_total_candidate_budget"], week_limits["ai_total_candidate_budget"])
        self.assertLess(
            short_limits["candidate_type_limits"]["wrong_questions"],
            week_limits["candidate_type_limits"]["wrong_questions"],
        )
        self.assertLess(
            short_limits["candidate_type_limits"]["draft_attempts"],
            week_limits["candidate_type_limits"]["draft_attempts"],
        )

    def test_ai_candidate_limits_allow_more_short_items_for_60_minutes(self) -> None:
        limits = build_ai_candidate_limits(build_ai_review_plan_policy("startup"), days=7, daily_minutes=60)

        self.assertEqual(limits["candidate_budget_basis"]["tasks_per_day"], 8)
        self.assertEqual(limits["candidate_budget_basis"]["plan_slots"], 56)

    def test_ai_candidate_limits_redistribute_when_include_types_change(self) -> None:
        broad_policy = build_ai_review_plan_policy(
            "weak",
            ["weak_topics", "wrong_questions", "review_tasks", "draft_attempts"],
        )
        narrow_policy = build_ai_review_plan_policy(
            "weak",
            ["review_tasks", "draft_attempts"],
        )

        broad_limits = build_ai_candidate_limits(broad_policy, days=7, daily_minutes=60)
        narrow_limits = build_ai_candidate_limits(narrow_policy, days=7, daily_minutes=60)

        self.assertEqual(narrow_limits["candidate_type_limits"]["weak_topics"], 0)
        self.assertEqual(narrow_limits["candidate_type_limits"]["wrong_questions"], 0)
        self.assertGreater(
            narrow_limits["candidate_type_limits"]["review_tasks"],
            broad_limits["candidate_type_limits"]["review_tasks"],
        )
        self.assertGreater(
            narrow_limits["candidate_type_limits"]["draft_attempts"],
            broad_limits["candidate_type_limits"]["draft_attempts"],
        )

    def test_synthetic_ai_planning_context_candidates_include_load_fields(self) -> None:
        persona = next(item for item in build_persona_catalog() if item["category"] == "heavy_wrong")

        context = build_synthetic_ai_planning_context(
            persona,
            mode="wrong",
            days=7,
            daily_minutes=60,
        )

        candidate = context["ai_candidates"]["wrong_questions"][0]
        self.assertIn("load_units", candidate)
        self.assertIn("estimated_minutes", candidate)
        self.assertIn("question_type_mix", candidate)

    def test_ai_policy_reports_requested_types_ignored_by_mode(self) -> None:
        policy = build_ai_review_plan_policy(
            "wrong",
            ["wrong_questions", "pending_review_items", "unstarted_questions", "review_tasks"],
        )

        self.assertIn("unstarted_questions", policy["requested_types"])
        self.assertNotIn("unstarted_questions", policy["enabled_types"])
        self.assertIn("unstarted_questions", policy["ignored_requested_types"])

    def test_ai_planning_context_reports_readiness_and_candidate_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            context = store.build_ai_planning_context(
                "tester",
                subject="math",
                days=7,
                daily_minutes=60,
                mode="wrong",
            )

        self.assertEqual(context["constraints"]["mode"], "wrong")
        self.assertEqual(context["candidate_summary"]["filtered_total"], 0)
        self.assertEqual(context["readiness"]["status"], "blocked")
        self.assertEqual(context["readiness"]["core_available"], 0)
        self.assertFalse(context["readiness"]["should_call_llm"])

    def test_ai_review_plan_draft_skips_model_when_mode_has_no_usable_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
                patch(
                    "materials.system_practice_review_api.generate_ai_review_plan_draft",
                    side_effect=AssertionError("blocked readiness should not call the model"),
                ),
            ):
                response = client.post(
                    "/api/materials/system/ai-review-plan/draft",
                    params={"user_id": "tester"},
                    json={
                        "subject": "math",
                        "days": 3,
                        "daily_minutes": 60,
                        "mode": "wrong",
                    },
                )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["context"]["readiness"]["status"], "blocked")
        self.assertEqual(payload["draft"]["source"], "blocked")
        self.assertTrue(payload["draft"]["skipped_llm"])
        self.assertEqual(len(payload["draft"]["days"]), 3)
        self.assertTrue(all(not day["items"] for day in payload["draft"]["days"]))

    def test_ai_planning_context_startup_mode_allows_unstarted_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.get(
                    "/api/materials/system/ai-planning-context",
                    params={
                        "user_id": "tester",
                        "subject": "math",
                        "days": 7,
                        "daily_minutes": 60,
                        "mode": "startup",
                    },
                )

            self.assertEqual(response.status_code, 200)
            context = response.json()["context"]
            self.assertEqual(context["constraints"]["mode"], "startup")
            self.assertIn("unstarted_questions", context["policy"]["enabled_types"])
            self.assertTrue(context["ai_candidates"].get("startup_candidates"))
            self.assertEqual(context["ai_candidates"]["startup_candidates"][0]["candidate_type"], "startup_question")

    def test_ai_planning_context_cold_start_uses_startup_candidates_not_weak_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)

            context = store.build_ai_planning_context(
                "tester",
                subject="math",
                days=3,
                daily_minutes=45,
                mode="startup",
            )

            self.assertEqual(context["constraints"]["mode"], "startup")
            self.assertEqual(context["ai_candidates"]["weak_topics"], [])
            self.assertTrue(context["ai_candidates"]["startup_candidates"])
            self.assertEqual(context["ai_candidates"]["startup_candidates"][0]["candidate_type"], "startup_question")

    def test_ai_planning_context_sends_lightweight_draft_question_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            answered_question_id = practice_set["question_ids"][0]
            unanswered_question_id = practice_set["question_ids"][1]
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {answered_question_id: {"answer_type": "choice", "value": "A"}},
            )

            context = store.build_ai_planning_context("tester", subject="math", mode="balanced")
            draft = context["ai_candidates"]["draft_attempts"][0]
            questions = {item["question_id"]: item for item in draft["questions"]}

            self.assertEqual(draft["attempt_id"], attempt["attempt_id"])
            self.assertEqual(draft["practice_set_id"], practice_set["set_id"])
            self.assertEqual(draft["question_count"], len(practice_set["question_ids"]))
            self.assertEqual(draft["answered_count"], 1)
            self.assertEqual(draft["unanswered_count"], len(practice_set["question_ids"]) - 1)
            self.assertTrue(questions[answered_question_id]["answered"])
            self.assertFalse(questions[unanswered_question_id]["answered"])
            self.assertEqual(questions[answered_question_id]["question_type"], "single_choice")
            self.assertEqual(questions[answered_question_id]["topics"], ["limits", "continuity"])
            self.assertNotIn("question_markdown", questions[answered_question_id])
            self.assertNotIn("answer_markdown", questions[answered_question_id])

    def test_ai_review_plan_weak_mode_honors_requested_draft_attempts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])

            context = store.build_ai_planning_context(
                "tester",
                subject="math",
                mode="weak",
                include_types=[
                    "weak_topics",
                    "wrong_questions",
                    "pending_review_items",
                    "draft_attempts",
                ],
            )
            draft = _fallback_review_plan_draft(
                context=context,
                model="deepseek-v4-flash",
                warning="",
            )
            planned_items = [
                item
                for day in draft["days"]
                for item in day.get("items", [])
            ]

            self.assertIn("draft_attempts", context["policy"]["enabled_types"])
            self.assertEqual(context["ai_candidates"]["draft_attempts"][0]["attempt_id"], attempt["attempt_id"])
            self.assertTrue(
                any(
                    item["type"] == "continue_draft"
                    and attempt["attempt_id"] in item.get("source_ids", [])
                    for item in planned_items
                )
            )

    def test_ai_plan_normalization_balances_weak_topics_and_drafts_by_daily_load(self) -> None:
        context = {
            "constraints": {"days": 4, "daily_minutes": 60, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["weak_topics", "draft_attempts"],
                "requested_types": ["weak_topics", "draft_attempts"],
            },
            "ai_candidates": {
                "weak_topics": [
                    {"topic": f"topic_{index}", "title": f"Topic {index}"}
                    for index in range(1, 5)
                ],
                "draft_attempts": [
                    {
                        "attempt_id": f"attempt_{index}",
                        "title": f"Draft {index}",
                        "question_count": 5,
                        "unanswered_count": 5,
                    }
                    for index in range(1, 5)
                ],
            },
        }
        payload = {
            "plan_id": "uneven_plan",
            "days": [
                {
                    "date": "2099-01-01",
                    "items": [
                        {
                            "type": "topic_review",
                            "title": "Topic 1",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_1"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 2",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_2"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 3",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_3"],
                        },
                    ],
                },
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "topic_review",
                            "title": "Topic 4",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_4"],
                        }
                    ],
                },
                {
                    "date": "2099-01-03",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Draft 1",
                            "estimated_minutes": 30,
                            "source_ids": ["attempt_1"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Draft 2",
                            "estimated_minutes": 30,
                            "source_ids": ["attempt_2"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Draft 3",
                            "estimated_minutes": 30,
                            "source_ids": ["attempt_3"],
                        },
                    ],
                },
                {
                    "date": "2099-01-04",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Draft 4",
                            "estimated_minutes": 30,
                            "source_ids": ["attempt_4"],
                        }
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )
        loads = [
            sum(int(item["estimated_minutes"]) for item in day["items"])
            for day in normalized["days"]
        ]

        self.assertLessEqual(max(loads) - min(loads), 10)
        self.assertEqual(sum(loads), 200)

    def test_ai_plan_normalization_counts_draft_questions_in_daily_load(self) -> None:
        context = {
            "constraints": {"days": 2, "daily_minutes": 60, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["weak_topics", "draft_attempts"],
                "requested_types": ["weak_topics", "draft_attempts"],
            },
            "ai_candidates": {
                "weak_topics": [
                    {"topic": "topic_1", "title": "Topic 1"},
                    {"topic": "topic_2", "title": "Topic 2"},
                ],
                "draft_attempts": [
                    {
                        "attempt_id": "draft_big",
                        "title": "Big Draft",
                        "question_count": 10,
                        "unanswered_count": 10,
                    },
                    {
                        "attempt_id": "draft_small",
                        "title": "Small Draft",
                        "question_count": 1,
                        "unanswered_count": 1,
                    },
                ],
            },
        }
        payload = {
            "plan_id": "draft_question_load_plan",
            "days": [
                {
                    "date": "2099-01-01",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Big Draft",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_big"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Small Draft",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_small"],
                        },
                    ],
                },
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "topic_review",
                            "title": "Topic 1",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_1"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 2",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_2"],
                        },
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )
        day_with_big_draft = next(
            day
            for day in normalized["days"]
            if any("draft_big" in item.get("source_ids", []) for item in day["items"])
        )

        self.assertEqual(len(day_with_big_draft["items"]), 1)
        self.assertEqual(day_with_big_draft["items"][0]["source_ids"], ["draft_big"])

    def test_ai_plan_normalization_counts_multi_question_items_in_daily_load(self) -> None:
        question_ids = [f"q{index}" for index in range(1, 15)]
        context = {
            "constraints": {"days": 4, "daily_minutes": 60, "mode": "balanced"},
            "policy": {
                "mode": "balanced",
                "enabled_types": ["wrong_questions"],
                "requested_types": ["wrong_questions"],
            },
            "ai_candidates": {
                "wrong_questions": [
                    {"question_id": question_id, "title": f"Question {question_id}"}
                    for question_id in question_ids
                ],
            },
        }
        payload = {
            "plan_id": "multi_question_load_plan",
            "days": [
                {
                    "date": "2099-01-01",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Question q1",
                            "estimated_minutes": 20,
                            "source_ids": ["q1"],
                        },
                        {
                            "type": "wrong_question",
                            "title": "Question q2",
                            "estimated_minutes": 20,
                            "source_ids": ["q2"],
                        },
                    ],
                },
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Question q3",
                            "estimated_minutes": 20,
                            "source_ids": ["q3"],
                        },
                        {
                            "type": "wrong_question",
                            "title": "Question q4",
                            "estimated_minutes": 20,
                            "source_ids": ["q4"],
                        },
                    ],
                },
                {
                    "date": "2099-01-03",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Question group 1",
                            "estimated_minutes": 20,
                            "source_ids": ["q5", "q6", "q7", "q8", "q9"],
                        },
                    ],
                },
                {
                    "date": "2099-01-04",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Question group 2",
                            "estimated_minutes": 20,
                            "source_ids": ["q10", "q11", "q12", "q13", "q14"],
                        },
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )
        question_loads = sorted(
            sum(len(item.get("source_ids") or []) for item in day["items"])
            for day in normalized["days"]
        )

        self.assertEqual(question_loads, [2, 2, 5, 5])

    def test_ai_plan_normalization_sums_multiple_candidate_source_minutes(self) -> None:
        context = {
            "constraints": {"days": 1, "daily_minutes": 60, "mode": "startup"},
            "policy": {
                "mode": "startup",
                "enabled_types": ["unstarted_questions"],
                "requested_types": ["unstarted_questions"],
            },
            "ai_candidates": {
                "unstarted_questions": [
                    {
                        "question_id": "q1",
                        "title": "Question 1",
                        "estimated_minutes": 12,
                        "load_units": 1.67,
                        "question_count": 1,
                    },
                    {
                        "question_id": "q2",
                        "title": "Question 2",
                        "estimated_minutes": 5,
                        "load_units": 0.69,
                        "question_count": 1,
                    },
                    {
                        "question_id": "q3",
                        "title": "Question 3",
                        "estimated_minutes": 5,
                        "load_units": 0.69,
                        "question_count": 1,
                    },
                ],
            },
        }

        normalized = _normalize_ai_plan_payload(
            {
                "plan_id": "multi_source_minutes",
                "days": [
                    {
                        "date": "2099-01-01",
                        "items": [
                            {
                                "type": "unstarted_question",
                                "title": "Three startup questions",
                                "estimated_minutes": 5,
                                "source_ids": ["q1", "q2", "q3"],
                            }
                        ],
                    }
                ],
            },
            context=context,
            model="deepseek-v4-flash",
        )

        item = normalized["days"][0]["items"][0]
        self.assertEqual(item["estimated_minutes"], 22)
        self.assertEqual(item["question_count"], 3)
        self.assertAlmostEqual(float(item["load_units"]), 3.05, places=2)

    def test_ai_plan_normalization_tops_up_underfilled_days_to_daily_minutes(self) -> None:
        candidates = [
            {
                "question_id": f"q{index}",
                "title": f"Question {index}",
                "estimated_minutes": 12 if index % 2 else 5,
                "load_units": 1.67 if index % 2 else 0.69,
                "question_count": 1,
            }
            for index in range(1, 15)
        ]
        context = {
            "constraints": {"days": 2, "daily_minutes": 60, "mode": "startup"},
            "policy": {
                "mode": "startup",
                "enabled_types": ["unstarted_questions"],
                "requested_types": ["unstarted_questions"],
                "type_priority": ["unstarted_questions"],
            },
            "ai_candidates": {"unstarted_questions": candidates},
        }

        normalized = _normalize_ai_plan_payload(
            {
                "plan_id": "underfilled_startup_plan",
                "days": [
                    {
                        "date": "2099-01-01",
                        "items": [
                            {
                                "type": "unstarted_question",
                                "title": "Question 1",
                                "estimated_minutes": 12,
                                "source_ids": ["q1"],
                            }
                        ],
                    },
                    {
                        "date": "2099-01-02",
                        "items": [
                            {
                                "type": "unstarted_question",
                                "title": "Question 2",
                                "estimated_minutes": 5,
                                "source_ids": ["q2"],
                            }
                        ],
                    },
                ],
            },
            context=context,
            model="deepseek-v4-flash",
        )
        daily_minutes = [
            sum(int(item["estimated_minutes"]) for item in day["items"])
            for day in normalized["days"]
        ]
        source_ids = [
            source_id
            for day in normalized["days"]
            for item in day["items"]
            for source_id in item.get("source_ids", [])
        ]

        self.assertGreaterEqual(min(daily_minutes), 51)
        self.assertLessEqual(max(daily_minutes), 60)
        self.assertGreater(len(source_ids), 4)
        self.assertEqual(len(source_ids), len(set(source_ids)))

    def test_ai_plan_fallback_tops_up_underfilled_startup_days(self) -> None:
        candidates = [
            {
                "question_id": f"q{index}",
                "title": f"Question {index}",
                "estimated_minutes": 12 if index % 2 else 5,
                "load_units": 1.67 if index % 2 else 0.69,
                "question_count": 1,
            }
            for index in range(1, 15)
        ]
        context = {
            "constraints": {"days": 2, "daily_minutes": 60, "mode": "startup"},
            "policy": {
                "mode": "startup",
                "enabled_types": ["unstarted_questions"],
                "requested_types": ["unstarted_questions"],
                "type_priority": ["unstarted_questions"],
            },
            "ai_candidates": {
                "unstarted_questions": candidates,
                "startup_candidates": [],
            },
        }

        draft = _fallback_review_plan_draft(
            context=context,
            model="deepseek-v4-flash",
            warning="fallback test",
        )
        daily_minutes = [
            sum(int(item["estimated_minutes"]) for item in day["items"])
            for day in draft["days"]
        ]

        self.assertEqual(draft["source"], "fallback")
        self.assertGreaterEqual(min(daily_minutes), 51)
        self.assertLessEqual(max(daily_minutes), 60)

    def test_ai_plan_fallback_merges_startup_top_up_with_initial_item(self) -> None:
        candidates = [
            {
                "question_id": f"q{index}",
                "title": f"Question {index}",
                "estimated_minutes": 12 if index % 2 else 5,
                "load_units": 1.67 if index % 2 else 0.69,
                "question_count": 1,
            }
            for index in range(1, 7)
        ]
        context = {
            "constraints": {"days": 1, "daily_minutes": 60, "mode": "startup"},
            "policy": {
                "mode": "startup",
                "enabled_types": ["unstarted_questions"],
                "requested_types": ["unstarted_questions"],
                "type_priority": ["unstarted_questions"],
            },
            "ai_candidates": {
                "unstarted_questions": candidates,
                "startup_candidates": [],
            },
        }

        draft = _fallback_review_plan_draft(
            context=context,
            model="deepseek-v4-flash",
            warning="fallback test",
        )
        items = draft["days"][0]["items"]

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["type"], "startup_question")
        self.assertEqual(items[0]["title"], "新题启动 6 道题")
        self.assertEqual(items[0]["estimated_minutes"], 51)
        self.assertEqual(items[0]["question_count"], 6)
        self.assertEqual(items[0]["source_ids"], [f"q{index}" for index in range(1, 7)])

    def test_ai_plan_fallback_uses_time_without_daily_item_or_source_limit(self) -> None:
        candidates = [
            {
                "question_id": f"q{index}",
                "title": f"Question {index}",
                "estimated_minutes": 3,
                "load_units": 0.42,
                "question_count": 1,
            }
            for index in range(1, 51)
        ]
        context = {
            "constraints": {"days": 1, "daily_minutes": 120, "mode": "startup"},
            "policy": {
                "mode": "startup",
                "enabled_types": ["unstarted_questions"],
                "requested_types": ["unstarted_questions"],
                "type_priority": ["unstarted_questions"],
            },
            "ai_candidates": {
                "unstarted_questions": candidates,
                "startup_candidates": [],
            },
        }

        draft = _fallback_review_plan_draft(
            context=context,
            model="deepseek-v4-flash",
            warning="fallback test",
        )
        items = draft["days"][0]["items"]
        source_ids = [
            source_id
            for item in items
            for source_id in item.get("source_ids", [])
        ]

        self.assertEqual(sum(int(item["estimated_minutes"]) for item in items), 120)
        self.assertEqual(len(source_ids), 40)
        self.assertGreater(max(len(item.get("source_ids", [])) for item in items), 3)

    def test_ai_plan_normalization_keeps_pending_review_on_first_cleanup_day(self) -> None:
        context = {
            "constraints": {"days": 3, "daily_minutes": 60, "mode": "balanced"},
            "policy": {
                "mode": "balanced",
                "enabled_types": ["pending_review_items", "weak_topics"],
                "requested_types": ["pending_review_items", "weak_topics"],
            },
            "ai_candidates": {
                "pending_review_items": [
                    {"question_id": "pending_q1", "title": "Pending 1"},
                    {"question_id": "pending_q2", "title": "Pending 2"},
                    {"question_id": "pending_q3", "title": "Pending 3"},
                ],
                "weak_topics": [
                    {"topic": "topic_1", "title": "Topic 1"},
                    {"topic": "topic_2", "title": "Topic 2"},
                    {"topic": "topic_3", "title": "Topic 3"},
                ],
            },
        }
        payload = {
            "plan_id": "pending_spread_plan",
            "days": [
                {
                    "date": "2099-01-01",
                    "items": [
                        {
                            "type": "pending_review",
                            "title": "Pending 1",
                            "estimated_minutes": 10,
                            "source_ids": ["pending_q1"],
                        },
                    ],
                },
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "pending_review",
                            "title": "Pending 2",
                            "estimated_minutes": 10,
                            "source_ids": ["pending_q2"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 1",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_1"],
                        },
                    ],
                },
                {
                    "date": "2099-01-03",
                    "items": [
                        {
                            "type": "pending_review",
                            "title": "Pending 3",
                            "estimated_minutes": 10,
                            "source_ids": ["pending_q3"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 2",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_2"],
                        },
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )

        pending_by_day = [
            [
                item["source_ids"][0]
                for item in day["items"]
                if item["type"] == "pending_review"
            ]
            for day in normalized["days"]
        ]
        self.assertEqual(pending_by_day[0], ["pending_q1", "pending_q2", "pending_q3"])
        self.assertEqual(pending_by_day[1], [])
        self.assertEqual(pending_by_day[2], [])

    def test_ai_plan_normalization_balances_many_drafts_and_wrong_questions_by_real_question_load(self) -> None:
        context = {
            "constraints": {"days": 5, "daily_minutes": 60, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["draft_attempts", "wrong_questions"],
                "requested_types": ["draft_attempts", "wrong_questions"],
            },
            "ai_candidates": {
                "draft_attempts": [
                    {
                        "attempt_id": f"draft_{index}",
                        "title": f"Draft {index}",
                        "question_count": 5,
                        "unanswered_count": 5,
                    }
                    for index in range(1, 7)
                ],
                "wrong_questions": [
                    {"question_id": f"wrong_{index}", "title": f"Wrong {index}"}
                    for index in range(1, 5)
                ],
            },
        }
        payload = {
            "plan_id": "clumped_drafts_and_wrong_questions",
            "days": [
                {
                    "date": "2099-01-01",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Wrong 1",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_1"],
                        },
                        {
                            "type": "wrong_question",
                            "title": "Wrong 2",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_2"],
                        },
                    ],
                },
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Wrong 3",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_3"],
                        },
                        {
                            "type": "wrong_question",
                            "title": "Wrong 4",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_4"],
                        },
                    ],
                },
                {
                    "date": "2099-01-03",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Draft 1",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_1"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Draft 2",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_2"],
                        },
                    ],
                },
                {
                    "date": "2099-01-04",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Draft 3",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_3"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Draft 4",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_4"],
                        },
                    ],
                },
                {
                    "date": "2099-01-05",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Draft 5",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_5"],
                        },
                        {
                            "type": "continue_draft",
                            "title": "Draft 6",
                            "estimated_minutes": 20,
                            "source_ids": ["draft_6"],
                        },
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )
        candidate_lookup = _context_candidate_lookup(context)
        daily_loads = [
            sum(_plan_item_load_minutes(item, candidate_lookup=candidate_lookup) for item in day["items"])
            for day in normalized["days"]
        ]
        daily_draft_counts = [
            sum(1 for item in day["items"] if item["type"] == "continue_draft")
            for day in normalized["days"]
        ]

        self.assertEqual(sorted(daily_loads), [40, 40, 40, 40, 60])
        self.assertLessEqual(max(daily_draft_counts), 2)

    def test_ai_plan_normalization_balances_multiple_day_counts_and_mixed_question_quantities(self) -> None:
        scenarios = [
            {
                "days": 3,
                "draft_sizes": [8, 8],
                "wrong_count": 4,
                "expected_max_gap": 8,
            },
            {
                "days": 4,
                "draft_sizes": [10, 5, 5],
                "wrong_count": 6,
                "expected_max_gap": 20,
            },
            {
                "days": 7,
                "draft_sizes": [5, 5, 5, 5, 3],
                "wrong_count": 8,
                "expected_max_gap": 20,
            },
        ]

        for scenario in scenarios:
            with self.subTest(days=scenario["days"], draft_sizes=scenario["draft_sizes"]):
                draft_sizes = scenario["draft_sizes"]
                wrong_count = int(scenario["wrong_count"])
                context = {
                    "constraints": {"days": scenario["days"], "daily_minutes": 60, "mode": "balanced"},
                    "policy": {
                        "mode": "balanced",
                        "enabled_types": ["draft_attempts", "wrong_questions"],
                        "requested_types": ["draft_attempts", "wrong_questions"],
                    },
                    "ai_candidates": {
                        "draft_attempts": [
                            {
                                "attempt_id": f"case_{scenario['days']}_draft_{index}",
                                "title": f"Draft {index}",
                                "question_count": size,
                                "unanswered_count": size,
                            }
                            for index, size in enumerate(draft_sizes, start=1)
                        ],
                        "wrong_questions": [
                            {
                                "question_id": f"case_{scenario['days']}_wrong_{index}",
                                "title": f"Wrong {index}",
                            }
                            for index in range(1, wrong_count + 1)
                        ],
                    },
                }
                payload_days = [{"date": f"2099-02-{index + 1:02d}", "items": []} for index in range(scenario["days"])]
                for index, _ in enumerate(draft_sizes, start=1):
                    payload_days[-1]["items"].append(
                        {
                            "type": "continue_draft",
                            "title": f"Draft {index}",
                            "estimated_minutes": 20,
                            "source_ids": [f"case_{scenario['days']}_draft_{index}"],
                        }
                    )
                for index in range(1, wrong_count + 1):
                    payload_days[0]["items"].append(
                        {
                            "type": "wrong_question",
                            "title": f"Wrong {index}",
                            "estimated_minutes": 10,
                            "source_ids": [f"case_{scenario['days']}_wrong_{index}"],
                        }
                    )

                normalized = _normalize_ai_plan_payload(
                    {"plan_id": "mixed_question_quantities", "days": payload_days},
                    context=context,
                    model="deepseek-v4-flash",
                )
                candidate_lookup = _context_candidate_lookup(context)
                daily_loads = [
                    sum(_plan_item_load_minutes(item, candidate_lookup=candidate_lookup) for item in day["items"])
                    for day in normalized["days"]
                ]

                self.assertLessEqual(max(daily_loads) - min(daily_loads), scenario["expected_max_gap"])

    def test_ai_plan_normalization_does_not_duplicate_sources_from_fallback_days(self) -> None:
        context = {
            "constraints": {"days": 3, "daily_minutes": 60, "mode": "balanced"},
            "policy": {
                "mode": "balanced",
                "enabled_types": ["wrong_questions"],
                "requested_types": ["wrong_questions"],
            },
            "ai_candidates": {
                "wrong_questions": [
                    {"question_id": f"wrong_{index}", "title": f"Wrong {index}"}
                    for index in range(1, 5)
                ],
            },
        }
        payload_days = [
            {
                "date": "2099-04-01",
                "items": [
                    {
                        "type": "wrong_question",
                        "title": f"Wrong {index}",
                        "estimated_minutes": 10,
                        "source_ids": [f"wrong_{index}"],
                    }
                    for index in range(1, 5)
                ],
            },
            {"date": "2099-04-02", "items": []},
            {"date": "2099-04-03", "items": []},
        ]

        normalized = _normalize_ai_plan_payload(
            {"plan_id": "dedupe_fallback_sources", "days": payload_days},
            context=context,
            model="deepseek-v4-flash",
        )
        seen_sources = [
            source_id
            for day in normalized["days"]
            for item in day["items"]
            for source_id in item.get("source_ids", [])
        ]

        self.assertCountEqual(seen_sources, [f"wrong_{index}" for index in range(1, 5)])
        self.assertEqual(len(seen_sources), len(set(seen_sources)))

    def test_ai_plan_normalization_keeps_many_pending_reviews_on_one_cleanup_day(self) -> None:
        pending_count = 8
        context = {
            "constraints": {"days": 5, "daily_minutes": 60, "mode": "balanced"},
            "policy": {
                "mode": "balanced",
                "enabled_types": ["pending_review_items", "weak_topics"],
                "requested_types": ["pending_review_items", "weak_topics"],
            },
            "ai_candidates": {
                "pending_review_items": [
                    {"question_id": f"pending_q{index}", "title": f"Pending {index}"}
                    for index in range(1, pending_count + 1)
                ],
                "weak_topics": [
                    {"topic": f"topic_{index}", "title": f"Topic {index}"}
                    for index in range(1, 6)
                ],
            },
        }
        payload_days = [{"date": f"2099-03-{index:02d}", "items": []} for index in range(1, 6)]
        for index in range(1, pending_count + 1):
            payload_days[(index - 1) % 5]["items"].append(
                {
                    "type": "pending_review",
                    "title": f"Pending {index}",
                    "estimated_minutes": 10,
                    "source_ids": [f"pending_q{index}"],
                }
            )
        for index in range(1, 6):
            payload_days[index - 1]["items"].append(
                {
                    "type": "topic_review",
                    "title": f"Topic {index}",
                    "estimated_minutes": 20,
                    "source_ids": [f"topic_{index}"],
                }
            )

        normalized = _normalize_ai_plan_payload(
            {"plan_id": "pending_reviews_should_not_be_spread", "days": payload_days},
            context=context,
            model="deepseek-v4-flash",
        )
        pending_counts_by_day = [
            sum(1 for item in day["items"] if item["type"] == "pending_review")
            for day in normalized["days"]
        ]

        self.assertEqual(pending_counts_by_day[0], pending_count)
        self.assertEqual(pending_counts_by_day[1:], [0, 0, 0, 0])

    def test_ai_plan_normalization_filters_out_unrequested_candidate_types(self) -> None:
        context = {
            "constraints": {"days": 3, "daily_minutes": 60, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["weak_topics"],
                "requested_types": ["weak_topics"],
            },
            "ai_candidates": {
                "weak_topics": [
                    {"topic": f"topic_{index}", "title": f"Topic {index}"}
                    for index in range(1, 4)
                ],
                "wrong_questions": [
                    {"question_id": f"wrong_{index}", "title": f"Wrong {index}"}
                    for index in range(1, 4)
                ],
            },
        }
        payload = {
            "plan_id": "unrequested_wrong_questions",
            "days": [
                {
                    "date": "2099-04-01",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Wrong 1",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_1"],
                        },
                        {
                            "type": "topic_review",
                            "title": "Topic 1",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_1"],
                        },
                    ],
                },
                {
                    "date": "2099-04-02",
                    "items": [
                        {
                            "type": "wrong_question",
                            "title": "Wrong 2",
                            "estimated_minutes": 10,
                            "source_ids": ["wrong_2"],
                        }
                    ],
                },
                {
                    "date": "2099-04-03",
                    "items": [
                        {
                            "type": "topic_review",
                            "title": "Topic 2",
                            "estimated_minutes": 20,
                            "source_ids": ["topic_2"],
                        }
                    ],
                },
            ],
        }

        normalized = _normalize_ai_plan_payload(
            payload,
            context=context,
            model="deepseek-v4-flash",
        )
        item_types = [item["type"] for day in normalized["days"] for item in day["items"]]

        self.assertNotIn("wrong_question", item_types)
        self.assertIn("topic_review", item_types)

    def test_ai_plan_normalization_keeps_draft_attempts_as_separate_tasks(self) -> None:
        context = {
            "constraints": {"days": 1, "daily_minutes": 60, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["draft_attempts"],
                "requested_types": ["draft_attempts"],
                "type_priority": ["draft_attempts"],
            },
            "ai_candidates": {
                "draft_attempts": [
                    {
                        "attempt_id": f"pa_{index}",
                        "source_id": f"pa_{index}",
                        "title": f"Draft {index}",
                        "estimated_minutes": 10,
                        "load_units": 1.4,
                        "question_count": 1,
                        "unanswered_count": 1,
                    }
                    for index in range(1, 5)
                ],
            },
        }

        normalized = _normalize_ai_plan_payload(
            {"days": [{"date": "2099-01-02", "items": []}]},
            context=context,
            model="deepseek-v4-flash",
        )
        draft_items = [
            item
            for day in normalized["days"]
            for item in day.get("items", [])
            if item.get("type") == "continue_draft"
        ]

        self.assertGreaterEqual(len(draft_items), 2)
        self.assertTrue(all(len(item.get("source_ids") or []) == 1 for item in draft_items))

    def test_ai_plan_commit_accepts_continue_draft_attempt_as_resumable_practice_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])

            committed = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="plan_draft_resume",
                plan_mode="balanced",
                plan_model="deepseek-v4-flash",
                plan_source="llm",
                subject="math",
                items=[
                    {
                        "type": "continue_draft",
                        "title": "Continue unfinished practice",
                        "due_at": "2099-01-02",
                        "estimated_minutes": 20,
                        "source_ids": [attempt["attempt_id"]],
                    }
                ],
            )

            self.assertEqual(committed["created_count"], 1)
            self.assertEqual(committed["rejected_count"], 0)
            review_task = committed["results"][0]["review_task"]
            self.assertEqual(review_task["target_type"], "practice_set")
            self.assertEqual(review_task["target_id"], practice_set["set_id"])
            self.assertEqual(review_task["source_meta"]["resume_attempt_id"], attempt["attempt_id"])
            self.assertEqual(review_task["source_meta"]["task_kind"], "continue_draft")

    def test_ai_plan_persona_catalog_has_at_least_sixty_fixed_personas(self) -> None:
        personas = build_persona_catalog()

        self.assertGreaterEqual(len(personas), 60)
        self.assertTrue(any(persona["category"] == "cold_start" for persona in personas))
        self.assertTrue(any(persona["category"] == "heavy_wrong" for persona in personas))

    def test_ai_plan_persona_catalog_has_at_least_200_diverse_personas(self) -> None:
        personas = build_persona_catalog()
        categories = {str(persona["category"]) for persona in personas}
        required_categories = {
            "cold_start",
            "strong",
            "heavy_wrong",
            "low_volume_concentrated",
            "review_pressure",
            "skip_unanswered",
            "scope_bias",
            "edge_cases",
            "all_done_no_new",
            "no_wrong_history",
            "pending_review_heavy",
            "favorite_unmastered_heavy",
            "overdue_neglect",
            "high_volume_unstable",
            "low_volume_accurate",
            "math2_scope",
            "math3_scope",
            "cross_subject_mixed",
            "wrong_resolved_history",
            "wrong_still_frequent_after_review",
            "ai_corrected_pending",
            "manual_override_heavy",
            "favorite_never_practiced",
            "short_daily_budget",
            "long_daily_budget",
            "exam_sprint_week",
            "repeat_postpone",
            "recent_improving",
            "recent_declining",
            "choice_only_bias",
            "solution_avoidance",
            "all_done_wrong_backlog",
            "chapter_cold_start",
            "scattered_wrong",
            "unstarted_foundation",
            "unstarted_advanced",
            "reviewed_but_unmastered",
            "oversized_practice_sheet",
            "proof_heavy_backlog",
            "mixed_type_load_gap",
        }
        signatures = {
            (
                persona.get("category"),
                persona.get("practice_volume"),
                persona.get("wrong_level"),
                persona.get("pending_review_level"),
                persona.get("overdue_level"),
                persona.get("draft_level"),
                persona.get("unstarted_level"),
                persona.get("topic_concentration"),
                persona.get("manual_state_level"),
                persona.get("completion_state"),
                persona.get("scope_profile"),
                persona.get("learning_trait"),
            )
            for persona in personas
        }

        self.assertGreaterEqual(len(personas), 200)
        self.assertGreaterEqual(len(categories), 35)
        self.assertTrue(required_categories.issubset(categories))
        self.assertGreaterEqual(len(signatures), 170)

    def test_ai_plan_persona_catalog_expected_modes_cover_specialized_categories(self) -> None:
        personas = build_persona_catalog()
        by_category = {str(persona["category"]): persona for persona in personas}

        self.assertIn("startup", by_category["favorite_never_practiced"]["expected_modes"])
        self.assertIn("startup", by_category["chapter_cold_start"]["expected_modes"])
        self.assertIn("sprint", by_category["exam_sprint_week"]["expected_modes"])
        self.assertIn("wrong", by_category["all_done_wrong_backlog"]["expected_modes"])
        self.assertIn("weak", by_category["recent_declining"]["expected_modes"])
        self.assertIn("balanced", by_category["cross_subject_mixed"]["expected_modes"])
        self.assertIn("wrong", by_category["wrong_still_frequent_after_review"]["expected_modes"])

    def test_ai_plan_policy_evaluator_runs_all_five_modes(self) -> None:
        personas = build_persona_catalog()[:3]

        report = evaluate_mode_policy_for_personas(personas)

        self.assertEqual(set(report["modes"]), {"balanced", "weak", "wrong", "startup", "sprint"})
        self.assertEqual(report["persona_count"], 3)
        self.assertEqual(report["case_count"], 15)
        self.assertIn("hard_violation_count", report["summary"])

    def test_ai_plan_policy_exposes_mode_priority_order(self) -> None:
        wrong_policy = build_ai_review_plan_policy("wrong")
        startup_policy = build_ai_review_plan_policy("startup")

        self.assertIn("type_priority", wrong_policy)
        self.assertEqual(
            wrong_policy["type_priority"][:3],
            ["wrong_questions", "pending_review_items", "review_tasks"],
        )
        self.assertNotIn("unstarted_questions", wrong_policy["type_priority"])
        self.assertIn("type_priority", startup_policy)
        self.assertEqual(
            startup_policy["type_priority"][:2],
            ["unstarted_questions", "startup_candidates"],
        )
        self.assertNotIn("wrong_questions", startup_policy["type_priority"])

    def test_ai_plan_deterministic_planner_evaluates_all_personas_and_modes(self) -> None:
        personas = build_persona_catalog()

        report = evaluate_deterministic_planner_for_personas(personas)

        self.assertEqual(report["persona_count"], len(personas))
        self.assertEqual(report["case_count"], len(personas) * 5)
        self.assertGreaterEqual(report["summary"]["mode_fit_score"], 0.8)
        self.assertEqual(report["summary"]["invalid_task_count"], 0)

    def test_ai_plan_candidate_budget_evaluator_covers_personas_and_modes(self) -> None:
        personas = build_persona_catalog()

        report = evaluate_mode_candidate_budget_for_personas(personas)

        self.assertEqual(report["persona_count"], len(personas))
        self.assertEqual(report["case_count"], len(personas) * 5)
        self.assertEqual(report["summary"]["hard_policy_violation_count"], 0)
        self.assertLess(report["summary"]["top_budget_violation_rate"], 0.10)
        self.assertGreaterEqual(report["summary"]["average_top_primary_ratio"], 0.80)
        self.assertEqual(set(report["by_mode"]), {"balanced", "weak", "wrong", "startup", "sprint"})

    def test_ai_plan_candidate_budget_respects_wrong_and_startup_boundaries(self) -> None:
        by_category = {
            str(persona["category"]): persona
            for persona in reversed(build_persona_catalog())
        }
        personas = [
            by_category["heavy_wrong"],
            by_category["all_done_wrong_backlog"],
            by_category["favorite_never_practiced"],
            by_category["chapter_cold_start"],
        ]

        report = evaluate_mode_candidate_budget_for_personas(personas, modes=["wrong", "startup"])
        cases = {(case["category"], case["mode"]): case for case in report["cases"]}

        for case in report["cases"]:
            self.assertEqual(case["disabled_present_count"], 0)

        for category in ("heavy_wrong", "all_done_wrong_backlog"):
            wrong_case = cases[(category, "wrong")]
            self.assertGreater(wrong_case["top_primary_ratio"], 0.70)
            self.assertEqual(wrong_case["input_counts"]["unstarted_questions"], 0)
            self.assertEqual(wrong_case["input_counts"]["startup_candidates"], 0)

        for category in ("favorite_never_practiced", "chapter_cold_start"):
            startup_case = cases[(category, "startup")]
            self.assertGreater(startup_case["top_primary_ratio"], 0.70)
            self.assertEqual(startup_case["input_counts"]["wrong_questions"], 0)
            self.assertEqual(startup_case["input_counts"]["pending_review_items"], 0)

    def test_ai_plan_readiness_evaluator_covers_personas_and_modes(self) -> None:
        personas = build_persona_catalog()

        report = evaluate_mode_readiness_for_personas(personas, days=7, daily_minutes=60)

        self.assertEqual(report["persona_count"], len(personas))
        self.assertEqual(report["case_count"], len(personas) * 5)
        self.assertGreater(report["summary"]["blocked_count"], 0)
        self.assertGreater(report["summary"]["weak_count"], 0)
        self.assertGreater(report["summary"]["ready_count"], 0)
        self.assertLess(report["summary"]["false_ready_rate"], 0.15)
        self.assertLess(report["summary"]["false_block_rate"], 0.15)

    def test_ai_plan_readiness_matches_representative_personas(self) -> None:
        personas = build_persona_catalog()
        cold_start = next(persona for persona in personas if persona["category"] == "cold_start")
        heavy_wrong = next(persona for persona in personas if persona["category"] == "heavy_wrong")
        strong = next(persona for persona in personas if persona["category"] == "strong")
        all_done = next(persona for persona in personas if persona["category"] == "all_done_no_new")

        report = evaluate_mode_readiness_for_personas(
            [cold_start, heavy_wrong, strong, all_done],
            days=7,
            daily_minutes=60,
        )
        cases = {
            (case["category"], case["mode"]): case["readiness"]["status"]
            for case in report["cases"]
        }

        self.assertEqual(cases[("cold_start", "wrong")], "blocked")
        self.assertIn(cases[("cold_start", "startup")], {"ready", "weak"})
        self.assertEqual(cases[("heavy_wrong", "wrong")], "ready")
        self.assertIn(cases[("strong", "startup")], {"weak", "blocked"})
        self.assertEqual(cases[("all_done_no_new", "startup")], "blocked")

    def test_ai_plan_readiness_penalizes_low_volume_sprint_confidence(self) -> None:
        persona = next(
            persona
            for persona in build_persona_catalog()
            if persona["category"] == "low_volume_concentrated"
        )

        report = evaluate_mode_readiness_for_personas([persona], modes=["sprint"], days=7, daily_minutes=60)
        status = report["cases"][0]["readiness"]["status"]

        self.assertEqual(status, "weak")

    def test_ai_plan_full_flow_evaluator_checks_load_duplicates_and_mode_fit(self) -> None:
        personas = build_persona_catalog()

        report = evaluate_full_ai_plan_flow_for_personas(personas, days=3, daily_minutes=60)

        self.assertEqual(report["persona_count"], len(personas))
        self.assertEqual(report["case_count"], len(personas) * 5)
        self.assertGreater(report["summary"]["should_call_llm_count"], 0)
        self.assertGreater(report["summary"]["blocked_case_count"], 0)
        self.assertEqual(report["summary"]["invalid_source_count"], 0)
        self.assertEqual(report["summary"]["duplicate_source_count"], 0)
        self.assertEqual(report["summary"]["daily_overload_count"], 0)
        self.assertGreaterEqual(report["summary"]["average_mode_fit_score"], 0.85)
        self.assertEqual(set(report["by_mode"]), {"balanced", "weak", "wrong", "startup", "sprint"})

    def test_ai_plan_full_flow_evaluator_blocks_mismatched_empty_modes_before_llm(self) -> None:
        by_category = {
            str(persona["category"]): persona
            for persona in build_persona_catalog()
        }
        personas = [
            by_category["cold_start"],
            by_category["all_done_no_new"],
        ]

        report = evaluate_full_ai_plan_flow_for_personas(
            personas,
            modes=["wrong", "startup"],
            days=7,
            daily_minutes=60,
        )
        cases = {(case["category"], case["mode"]): case for case in report["cases"]}

        cold_start_wrong = cases[("cold_start", "wrong")]
        self.assertFalse(cold_start_wrong["should_call_llm"])
        self.assertEqual(cold_start_wrong["task_count"], 0)
        self.assertEqual(cold_start_wrong["readiness_status"], "blocked")

        all_done_startup = cases[("all_done_no_new", "startup")]
        self.assertFalse(all_done_startup["should_call_llm"])
        self.assertEqual(all_done_startup["task_count"], 0)
        self.assertEqual(all_done_startup["readiness_status"], "blocked")

    def test_ai_plan_evaluator_rewards_balanced_priority_then_broad_followup(self) -> None:
        context = {
            "policy": build_ai_review_plan_policy("balanced"),
            "ai_candidates": {
                "review_tasks": [{"task_id": "task-1"}],
                "wrong_questions": [{"question_id": "wrong-1"}],
                "weak_topics": [{"topic": "limits"}],
                "pending_review_items": [{"question_id": "pending-1"}],
                "draft_attempts": [{"attempt_id": "draft-1"}],
                "favorite_unmastered": [{"question_id": "favorite-1"}],
                "unstarted_questions": [{"question_id": "unstarted-1"}],
                "startup_candidates": [{"question_id": "startup-1"}],
            },
        }
        draft = {
            "days": [
                {
                    "items": [
                        {"type": "review_tasks", "source_ids": ["task-1"]},
                        {"type": "wrong_questions", "source_ids": ["wrong-1"]},
                        {"type": "weak_topics", "source_ids": ["limits"]},
                    ]
                },
                {
                    "items": [
                        {"type": "pending_review_items", "source_ids": ["pending-1"]},
                        {"type": "draft_attempts", "source_ids": ["draft-1"]},
                        {"type": "favorite_unmastered", "source_ids": ["favorite-1"]},
                    ]
                },
                {
                    "items": [
                        {"type": "unstarted_questions", "source_ids": ["unstarted-1"]},
                        {"type": "startup_candidates", "source_ids": ["startup-1"]},
                    ]
                },
            ]
        }

        result = _evaluate_plan_items_against_context(draft, context)

        self.assertGreaterEqual(result["mode_fit_score"], 0.8)

    def test_ai_review_plan_fallback_uses_startup_candidates_for_startup_mode(self) -> None:
        draft = _fallback_review_plan_draft(
            context={
                "constraints": {"days": 1, "daily_minutes": 45, "mode": "startup"},
                "policy": {
                    "mode": "startup",
                    "enabled_types": ["startup_candidates", "unstarted_questions"],
                    "disabled_types": ["weak_topics", "wrong_questions"],
                },
                "ai_candidates": {
                    "startup_candidates": [
                        {
                            "candidate_type": "startup_question",
                            "question_id": "kaoyan_math1_2025_q001",
                            "title": "2025 math1 Q1",
                            "reason": "startup",
                        }
                    ],
                    "weak_topics": [],
                    "wrong_questions": [],
                },
            },
            model="deepseek-v4-flash",
            warning="",
        )

        first_item = draft["days"][0]["items"][0]
        self.assertEqual(first_item["type"], "startup_question")
        self.assertEqual(first_item["source_ids"], ["kaoyan_math1_2025_q001"])

    def test_ai_review_plan_normalize_keeps_requested_draft_even_if_llm_omits_it(self) -> None:
        context = {
            "constraints": {"days": 1, "daily_minutes": 45, "mode": "weak"},
            "policy": {
                "mode": "weak",
                "enabled_types": ["weak_topics", "draft_attempts"],
                "requested_types": ["weak_topics", "draft_attempts"],
            },
            "ai_candidates": {
                "weak_topics": [{"topic": "limits", "title": "limits"}],
                "draft_attempts": [
                    {
                        "attempt_id": "draft-1",
                        "practice_set_id": "ps-1",
                        "title": "2025 数一 Q1 同类训练",
                        "unanswered_count": 3,
                    }
                ],
            },
        }
        normalized = _normalize_ai_plan_payload(
            {
                "plan_id": "plan-1",
                "days": [
                    {
                        "date": "2099-01-01",
                        "items": [
                            {
                                "type": "topic_review",
                                "title": "limits",
                                "reason": "weak topic",
                                "estimated_minutes": 20,
                                "source_ids": ["limits"],
                            }
                        ],
                    }
                ],
            },
            context=context,
            model="deepseek-v4-flash",
        )
        planned_items = normalized["days"][0]["items"]

        self.assertTrue(
            any(
                item["type"] == "continue_draft"
                and item.get("source_ids") == ["draft-1"]
                for item in planned_items
            )
        )

    def test_ai_review_plan_fallback_keeps_generic_candidate_source_ids(self) -> None:
        context = {
            "constraints": {"days": 1, "daily_minutes": 45, "mode": "balanced"},
            "policy": {
                "mode": "balanced",
                "enabled_types": ["review_tasks", "pending_review_items", "weak_topics", "wrong_questions"],
            },
            "ai_candidates": {
                "review_tasks": [{"source_id": "task:1", "title": "到期任务"}],
                "pending_review_items": [{"source_id": "pending:1", "title": "待核对题"}],
                "weak_topics": [{"source_id": "topic:limits", "title": "极限"}],
                "wrong_questions": [{"source_id": "wrong:1", "title": "错题"}],
            },
        }

        draft = _fallback_review_plan_draft(context=context, model="deepseek-v4-flash", warning="")
        items = draft["days"][0]["items"]

        self.assertIn("task:1", items[0]["source_ids"])
        self.assertIn("pending:1", items[1]["source_ids"])
        self.assertEqual(items[2]["source_ids"], ["topic:limits"])
        self.assertEqual(items[3]["source_ids"], ["wrong:1"])

    def test_ai_review_plan_drops_items_without_real_candidate_sources(self) -> None:
        persona = build_persona_catalog()[0]
        context = build_synthetic_ai_planning_context(persona, mode="wrong", days=1, daily_minutes=45)

        draft = _normalize_ai_plan_payload(
            {
                "plan_id": "bad-source-test",
                "days": [
                    {
                        "date": "2099-01-01",
                        "items": [
                            {
                                "type": "wrong_questions",
                                "title": "复习错题",
                                "reason": "AI 编造了一个没有 source_ids 的错题任务。",
                                "estimated_minutes": 20,
                                "source_ids": [],
                            }
                        ],
                    }
                ],
            },
            context=context,
            model="deepseek-v4-flash",
        )

        self.assertNotEqual(draft["days"][0]["items"][0]["type"], "wrong_questions")

    def test_ai_planner_sample_evaluator_limits_cases_and_scores_mock_planner(self) -> None:
        def fake_planner(*, context: dict[str, object], model: str) -> dict[str, object]:
            candidates = context["ai_candidates"]  # type: ignore[assignment]
            candidate = None
            for values in candidates.values():  # type: ignore[union-attr]
                if values:
                    candidate = values[0]
                    break
            if candidate is None:
                return {
                    "plan_id": "sample-test",
                    "model": model,
                    "source": "llm",
                    "days": [{"date": "2099-01-01", "items": []}],
                    "warnings": [],
                }
            return {
                "plan_id": "sample-test",
                "model": model,
                "source": "llm",
                "days": [
                    {
                        "date": "2099-01-01",
                        "items": [
                            {
                                "type": candidate["candidate_type"],  # type: ignore[index]
                                "title": candidate["title"],  # type: ignore[index]
                                "reason": "mock",
                                "estimated_minutes": 15,
                                "source_ids": [candidate["source_id"]],  # type: ignore[index]
                            }
                        ],
                    }
                ],
                "warnings": [],
            }

        report = evaluate_ai_planner_sample_for_personas(
            build_persona_catalog(),
            modes=["startup"],
            max_cases=5,
            planner=fake_planner,
        )

        self.assertEqual(report["case_count"], 5)
        self.assertGreater(report["summary"]["llm_success_count"], 0)
        self.assertEqual(
            report["summary"]["llm_success_count"] + report["summary"]["llm_skipped_count"],
            5,
        )
        self.assertEqual(report["summary"]["candidate_validity_rate"], 1.0)

    def test_ai_planner_sample_evaluator_skips_blocked_cases_before_llm(self) -> None:
        cold_start = next(
            persona
            for persona in build_persona_catalog()
            if persona["category"] == "cold_start"
        )

        def planner_should_not_run(*, context: dict[str, object], model: str) -> dict[str, object]:
            raise AssertionError("blocked planning case should not call the model")

        report = evaluate_ai_planner_sample_for_personas(
            [cold_start],
            modes=["wrong"],
            max_cases=1,
            planner=planner_should_not_run,
        )

        self.assertEqual(report["case_count"], 1)
        self.assertEqual(report["summary"]["llm_skipped_count"], 1)
        self.assertEqual(report["cases"][0]["source"], "skipped")
        self.assertEqual(report["cases"][0]["readiness_status"], "blocked")

    def test_ai_review_plan_draft_uses_deepseek_flash_and_does_not_write_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
                patch("materials.system_practice_review_api.generate_ai_review_plan_draft") as fake_planner,
            ):
                store = self._store(raw_root, users_root)
                before_total = store.review_task_summary("tester")["total"]
                fake_planner.return_value = {
                    "plan_id": "draft-test",
                    "model": "deepseek-v4-flash",
                    "days": [
                        {
                            "date": "2099-01-02",
                            "items": [
                                {
                                    "type": "wrong_pool",
                                    "title": "复习 limits 错题 3 道",
                                    "reason": "limits 最近错题较多",
                                    "estimated_minutes": 25,
                                }
                            ],
                        }
                    ],
                    "warnings": [],
                }

                response = client.post(
                    "/api/materials/system/ai-review-plan/draft",
                    params={"user_id": "tester"},
                    json={"subject": "math", "days": 3, "daily_minutes": 45, "goal": "错题回收"},
                )
                after_total = store.review_task_summary("tester")["total"]

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["draft"]["model"], "deepseek-v4-flash")
            self.assertEqual(before_total, after_total)
            _, planner_kwargs = fake_planner.call_args
            self.assertEqual(planner_kwargs["model"], "deepseek-v4-flash")
            self.assertEqual(planner_kwargs["context"]["constraints"]["goal"], "错题回收")

    def test_ai_review_plan_commit_selected_items_creates_idempotent_review_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            selected_item = {
                "type": "wrong_pool",
                "title": "复习 limits 错题",
                "reason": "limits 最近错题较多",
                "estimated_minutes": 25,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q001"],
            }
            unselected_item = {
                "type": "freeform_review",
                "title": "复习 derivatives",
                "reason": "derivatives 还没开始",
                "estimated_minutes": 20,
                "date": "2099-01-03",
                "source_ids": ["derivatives"],
            }

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                first_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-test",
                        "subject": "math",
                        "mode": "wrong",
                        "items": [selected_item],
                        "draft": {
                            "plan_id": "draft-test",
                            "model": "deepseek-v4-flash",
                            "source": "llm",
                        },
                    },
                )
                second_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-test",
                        "subject": "math",
                        "mode": "wrong",
                        "items": [selected_item, unselected_item],
                        "selected_item_keys": ["0"],
                        "draft": {
                            "plan_id": "draft-test",
                            "model": "deepseek-v4-flash",
                            "source": "llm",
                        },
                    },
                )
                list_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                )

            self.assertEqual(first_response.status_code, 200)
            first_payload = first_response.json()
            self.assertTrue(first_payload["ok"])
            self.assertEqual(first_payload["result"]["created_count"], 1)
            self.assertEqual(first_payload["result"]["skipped_count"], 0)
            self.assertEqual(first_payload["result"]["results"][0]["status"], "created")

            self.assertEqual(second_response.status_code, 200)
            second_payload = second_response.json()
            self.assertEqual(second_payload["result"]["created_count"], 0)
            self.assertEqual(second_payload["result"]["skipped_count"], 1)
            self.assertEqual(second_payload["result"]["results"][0]["status"], "duplicate")

            tasks = list_response.json()["items"]
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "question")
            self.assertEqual(tasks[0]["target_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(tasks[0]["due_at"], "2099-01-02")
            self.assertIn("AI规划", tasks[0]["note"])
            self.assertEqual(tasks[0]["created_from"], "ai_plan")
            self.assertEqual(tasks[0]["plan_id"], "draft-test")
            self.assertEqual(tasks[0]["plan_mode"], "wrong")
            self.assertEqual(tasks[0]["plan_model"], "deepseek-v4-flash")
            self.assertEqual(tasks[0]["plan_source"], "llm")
            self.assertEqual(tasks[0]["plan_reason"], selected_item["reason"])
            self.assertEqual(tasks[0]["estimated_minutes"], 25)

    def test_ai_review_plan_commit_groups_multiple_question_sources_into_practice_set_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            group_item = {
                "type": "wrong_pool",
                "title": "Review limits wrong questions",
                "reason": "Several limits questions should be practiced together.",
                "estimated_minutes": 30,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q004", "kaoyan_math1_2099_q002"],
            }

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                validate_response = client.post(
                    "/api/materials/system/ai-review-plan/validate",
                    params={"user_id": "tester"},
                    json={"subject": "math", "items": [group_item]},
                )
                commit_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-group",
                        "subject": "math",
                        "mode": "wrong",
                        "items": [group_item],
                        "draft": {"model": "deepseek-v4-flash", "source": "llm"},
                    },
                )
                second_commit_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-group",
                        "subject": "math",
                        "mode": "wrong",
                        "items": [group_item],
                        "draft": {"model": "deepseek-v4-flash", "source": "llm"},
                    },
                )
                store = self._store(raw_root, users_root)
                practice_sets = store.list_practice_sets("tester")
                tasks = store.list_review_tasks("tester")

            self.assertEqual(validate_response.status_code, 200)
            validation = validate_response.json()["validation"]
            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "practice_set")
            self.assertEqual(
                validation["valid_items"][0]["derived_practice_question_ids"],
                ["kaoyan_math1_2099_q004", "kaoyan_math1_2099_q002"],
            )

            self.assertEqual(commit_response.status_code, 200)
            result = commit_response.json()["result"]
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["rejected_count"], 0)
            self.assertEqual(result["results"][0]["target_type"], "practice_set")
            self.assertEqual(second_commit_response.status_code, 200)
            second_result = second_commit_response.json()["result"]
            self.assertEqual(second_result["created_count"], 0)
            self.assertEqual(second_result["skipped_count"], 1)
            self.assertEqual(second_result["results"][0]["status"], "duplicate")

            self.assertEqual(len(practice_sets), 1)
            self.assertEqual(practice_sets[0]["source_type"], "ai_plan_wrong_pool")
            self.assertEqual(
                practice_sets[0]["question_ids"],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            )
            self.assertEqual(practice_sets[0]["criteria"]["filters"]["source_plan_id"], "draft-group")
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "practice_set")
            self.assertEqual(tasks[0]["target_id"], practice_sets[0]["set_id"])
            self.assertEqual(tasks[0]["source_meta"]["question_count"], 2)
            self.assertEqual(tasks[0]["source_meta"]["matching_topics"], ["continuity", "limits"])

    def test_ai_review_plan_commit_merges_same_day_practice_sources_into_one_practice_set_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            first_practice_item = {
                "type": "wrong_pool",
                "title": "Continuity practice",
                "reason": "Practice continuity as a compact set.",
                "estimated_minutes": 25,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            }
            second_practice_item = {
                "type": "wrong_pool",
                "title": "Limits practice",
                "reason": "Practice limits as a compact set.",
                "estimated_minutes": 20,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q005", "kaoyan_math1_2099_q006"],
            }

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                commit_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-same-day-practice",
                        "subject": "math",
                        "mode": "weak",
                        "items": [first_practice_item, second_practice_item],
                        "draft": {"model": "deepseek-v4-flash", "source": "llm"},
                    },
                )
                store = self._store(raw_root, users_root)
                practice_sets = store.list_practice_sets("tester")
                tasks = store.list_review_tasks("tester")

            self.assertEqual(commit_response.status_code, 200)
            result = commit_response.json()["result"]
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["failed_count"], 0)
            self.assertEqual(result["results"][0]["target_type"], "practice_set")
            self.assertEqual(result["results"][0]["merged_count"], 2)
            self.assertEqual(result["results"][0]["merged_item_indexes"], [0, 1])
            self.assertEqual(len(practice_sets), 1)
            self.assertEqual(
                practice_sets[0]["question_ids"],
                [
                    "kaoyan_math1_2099_q002",
                    "kaoyan_math1_2099_q004",
                    "kaoyan_math1_2099_q005",
                    "kaoyan_math1_2099_q006",
                ],
            )
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "practice_set")
            self.assertEqual(tasks[0]["target_id"], practice_sets[0]["set_id"])
            self.assertEqual(tasks[0]["source_meta"]["question_count"], 4)
            self.assertEqual(
                tasks[0]["source_meta"]["merged_question_ids"],
                practice_sets[0]["question_ids"],
            )

    def test_ai_review_plan_commit_keeps_existing_practice_set_out_of_single_question_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                store = self._store(raw_root, users_root)
                existing_set = store.create_practice_set_from_question_ids(
                    "tester",
                    question_ids=["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
                    title="Existing AI practice",
                    source_type="ai_plan_wrong_pool",
                    filters={"source_plan_id": "older-plan"},
                )
                practice_set_item = {
                    "type": "wrong_pool",
                    "title": "Continue existing practice",
                    "reason": "Existing same-day practice set should stay as its own review task.",
                    "estimated_minutes": 25,
                    "date": "2099-01-02",
                    "source_ids": [existing_set["set_id"]],
                }
                single_question_item = {
                    "type": "wrong_question",
                    "title": "Add one more wrong question",
                    "reason": "Same subject and day should be merged into the daily practice set.",
                    "estimated_minutes": 15,
                    "date": "2099-01-02",
                    "source_ids": ["kaoyan_math1_2099_q005"],
                }
                commit_response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-existing-plus-single",
                        "subject": "math",
                        "mode": "weak",
                        "items": [practice_set_item, single_question_item],
                        "draft": {"model": "deepseek-v4-flash", "source": "llm"},
                    },
                )
                practice_sets = store.list_practice_sets("tester")
                tasks = store.list_review_tasks("tester")

            self.assertEqual(commit_response.status_code, 200)
            result = commit_response.json()["result"]
            self.assertEqual(result["created_count"], 2)
            self.assertEqual(result["failed_count"], 0)
            self.assertEqual(result["results"][0]["target_type"], "practice_set")
            self.assertEqual(result["results"][0]["target_id"], existing_set["set_id"])
            self.assertEqual(result["results"][0].get("merged_count", 0), 0)
            self.assertEqual(result["results"][1]["target_type"], "question")
            self.assertEqual(result["results"][1]["target_id"], "kaoyan_math1_2099_q005")
            self.assertEqual(len(practice_sets), 1)
            self.assertEqual(practice_sets[0]["set_id"], existing_set["set_id"])
            self.assertEqual(len(tasks), 2)
            self.assertEqual(
                [(task["target_type"], task["target_id"]) for task in tasks],
                [
                    ("question", "kaoyan_math1_2099_q005"),
                    ("practice_set", existing_set["set_id"]),
                ],
            )

    def test_ai_review_plan_commit_keeps_topic_placeholder_and_merges_same_day_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            topic_item = {
                "type": "topic_review",
                "title": "Extrema review",
                "reason": "System knowledge point library is not ready, keep this as a topic placeholder.",
                "estimated_minutes": 25,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            }
            question_items = [
                {
                    "type": "wrong_question",
                    "title": "Wrong question 2",
                    "reason": "Same-day question should be part of a practice set.",
                    "estimated_minutes": 15,
                    "date": "2099-01-02",
                    "source_ids": ["kaoyan_math1_2099_q002"],
                },
                {
                    "type": "pending_review_item",
                    "title": "Pending question 4",
                    "reason": "Same-day question should be part of a practice set.",
                    "estimated_minutes": 15,
                    "date": "2099-01-02",
                    "source_ids": ["kaoyan_math1_2099_q004"],
                },
                {
                    "type": "unstarted_question",
                    "title": "Startup question 5",
                    "reason": "Same-day question should be part of a practice set.",
                    "estimated_minutes": 15,
                    "date": "2099-01-02",
                    "source_ids": ["kaoyan_math1_2099_q005"],
                },
            ]

            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="draft-topic-plus-questions",
                items=[topic_item, *question_items],
                subject="math",
                plan_mode="weak",
                plan_model="deepseek-v4-flash",
                plan_source="llm",
            )
            practice_sets = store.list_practice_sets("tester")
            tasks = sorted(store.list_review_tasks("tester"), key=lambda item: item["target_type"])

            self.assertEqual(result["created_count"], 2)
            self.assertEqual(result["failed_count"], 0)
            self.assertEqual(len(practice_sets), 1)
            self.assertEqual(
                practice_sets[0]["question_ids"],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004", "kaoyan_math1_2099_q005"],
            )
            self.assertEqual([task["target_type"] for task in tasks], ["knowledge_point", "practice_set"])
            knowledge_task = tasks[0]
            practice_task = tasks[1]
            self.assertEqual(
                knowledge_task["source_meta"]["task_kind"],
                "ai_plan_knowledge_point_placeholder",
            )
            self.assertEqual(
                knowledge_task["source_meta"]["representative_question_ids"],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            )
            self.assertEqual(practice_task["target_id"], practice_sets[0]["set_id"])
            self.assertEqual(practice_task["source_meta"]["question_count"], 3)
            self.assertEqual(practice_task["source_meta"]["merged_item_indexes"], [1, 2, 3])

    def test_ai_review_plan_topic_review_remains_knowledge_placeholder_with_representative_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            item = {
                "type": "topic_review",
                "title": "Extrema review",
                "reason": "Use representative questions only as context.",
                "estimated_minutes": 25,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            }

            validation = store.validate_ai_review_plan_items(
                "tester",
                items=[item],
                subject="math",
            )
            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="draft-topic-placeholder",
                items=[item],
                subject="math",
                plan_mode="weak",
            )
            practice_sets = store.list_practice_sets("tester")
            tasks = store.list_review_tasks("tester")

            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "knowledge_point")
            self.assertEqual(validation["valid_items"][0]["derived_practice_question_ids"], [])
            self.assertEqual(
                validation["valid_items"][0]["source_meta_extra"]["task_kind"],
                "ai_plan_knowledge_point_placeholder",
            )
            self.assertEqual(
                validation["valid_items"][0]["source_meta_extra"]["representative_question_ids"],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            )
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["results"][0]["target_type"], "knowledge_point")
            self.assertEqual(practice_sets, [])
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "knowledge_point")
            self.assertTrue(str(tasks[0]["target_id"]).startswith("kp_ai_"))
            self.assertEqual(
                tasks[0]["source_meta"]["representative_question_ids"],
                ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"],
            )

    def test_ai_review_plan_topic_review_without_source_becomes_knowledge_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            item = {
                "type": "topic_review",
                "title": "Derivative application",
                "reason": "System knowledge library is not connected yet.",
                "estimated_minutes": 20,
                "date": "2099-01-02",
                "source_ids": [],
            }

            validation = store.validate_ai_review_plan_items(
                "tester",
                items=[item],
                subject="math",
            )
            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="draft-topic-only",
                items=[item],
                subject="math",
                plan_mode="weak",
            )
            tasks = store.list_review_tasks("tester")

            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "knowledge_point")
            self.assertEqual(
                validation["valid_items"][0]["source_meta_extra"]["task_kind"],
                "ai_plan_knowledge_point_placeholder",
            )
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["failed_count"], 0)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "knowledge_point")
            self.assertEqual(tasks[0]["source_meta"]["topic_title"], "Derivative application")

    def test_ai_review_plan_topic_like_title_with_representative_questions_stays_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            item = {
                "type": "review",
                "title": "continuity",
                "reason": "Treat this as a knowledge point placeholder, not a generated practice set.",
                "estimated_minutes": 20,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q001", "kaoyan_math1_2099_q002"],
            }

            validation = store.validate_ai_review_plan_items(
                "tester",
                items=[item],
                subject="math",
            )
            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="draft-topic-like-title",
                items=[item],
                subject="math",
                plan_mode="weak",
            )
            tasks = store.list_review_tasks("tester")

            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "knowledge_point")
            self.assertEqual(validation["valid_items"][0]["derived_practice_question_ids"], [])
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["failed_count"], 0)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "knowledge_point")
            self.assertEqual(
                tasks[0]["source_meta"]["representative_question_ids"],
                ["kaoyan_math1_2099_q001", "kaoyan_math1_2099_q002"],
            )

    def test_ai_review_plan_question_load_uses_three_type_difficulty_minutes(self) -> None:
        cases = [
            ({"question_type": "single_choice", "difficulty": "easy"}, "unstarted", 3),
            ({"question_type": "single_choice", "difficulty": "unknown"}, "unstarted", 4),
            ({"question_type": "single_choice", "difficulty": "hard"}, "unstarted", 5),
            ({"question_type": "fill_blank", "difficulty": "easy"}, "unstarted", 4),
            ({"question_type": "fill_blank", "difficulty": "unknown"}, "unstarted", 5),
            ({"question_type": "fill_blank", "difficulty": "hard"}, "unstarted", 6),
            ({"question_type": "solution", "difficulty": "easy"}, "unstarted", 10),
            ({"question_type": "solution", "difficulty": "unknown"}, "unstarted", 12),
            ({"question_type": "solution", "difficulty": "hard"}, "unstarted", 15),
            ({"question_type": "proof", "difficulty": "hard"}, "unstarted", 15),
        ]

        for question, state, expected_minutes in cases:
            with self.subTest(question=question, state=state):
                load_units = calculate_question_load_units(question, state)
                self.assertEqual(estimate_minutes_from_load(load_units), expected_minutes)

    def test_ai_review_plan_question_load_adds_user_state_after_base_minutes(self) -> None:
        self.assertEqual(
            estimate_minutes_from_load(
                calculate_question_load_units(
                    {"question_type": "single_choice", "difficulty": "hard"},
                    "repeat_wrong",
                )
            ),
            8,
        )
        self.assertEqual(
            estimate_minutes_from_load(
                calculate_question_load_units(
                    {"question_type": "solution", "difficulty": "hard"},
                    "wrong",
                )
            ),
            20,
        )
        self.assertEqual(estimate_minutes_from_load(8.1), 58)

    def test_ai_review_plan_single_question_candidates_do_not_add_sheet_overhead(self) -> None:
        load = calculate_candidate_load(
            {
                "candidate_type": "unstarted_questions",
                "questions": [
                    {"question_id": "q1", "question_type": "single_choice", "difficulty": "unknown"}
                ],
            },
            "unstarted_questions",
        )

        self.assertEqual(load["question_count"], 1)
        self.assertEqual(load["task_kind"], "single_question")
        self.assertEqual(load["estimated_minutes"], 4)

    def test_ai_review_plan_candidate_minutes_use_precise_load_before_display_rounding(self) -> None:
        load = calculate_candidate_load(
            {
                "candidate_type": "wrong_questions",
                "questions": [
                    {"question_id": "q1", "question_type": "fill_blank", "difficulty": "unknown"}
                ],
            },
            "wrong_questions",
        )

        self.assertEqual(load["load_units"], 0.9)
        self.assertEqual(load["estimated_minutes"], 7)

    def test_ai_review_plan_candidate_load_sums_question_details(self) -> None:
        candidate = {
            "candidate_type": "draft_attempts",
            "question_ids": ["q1", "q2", "q3"],
            "questions": [
                {"question_id": "q1", "question_type": "single_choice", "difficulty": "medium"},
                {"question_id": "q2", "question_type": "fill_blank", "difficulty": "unknown"},
                {"question_id": "q3", "question_type": "solution", "difficulty": "hard"},
            ],
            "state": "draft_unanswered",
        }

        load = calculate_candidate_load(candidate)

        self.assertEqual(load["question_count"], 3)
        self.assertEqual(load["question_type_mix"], {"single_choice": 1, "fill_blank": 1, "solution": 1})
        self.assertEqual(load["estimated_minutes"], 27)
        self.assertEqual(load["estimated_minutes"], estimate_minutes_from_load(load["load_units"]))

    def test_ai_review_plan_splits_oversized_practice_sheet_without_mutating_parent(self) -> None:
        candidate = {
            "candidate_type": "draft_attempts",
            "attempt_id": "pa_big",
            "practice_set_id": "ps_big",
            "title": "Large sheet",
            "question_ids": [f"q{i}" for i in range(1, 21)],
            "questions": [
                {"question_id": f"q{i}", "question_type": "solution", "difficulty": "hard"}
                for i in range(1, 21)
            ],
            "state": "draft_unanswered",
        }
        original_ids = list(candidate["question_ids"])

        segments, pending = split_candidate_into_plan_segments(candidate, daily_minutes=60, days=3)

        self.assertGreater(len(segments), 1)
        self.assertTrue(pending)
        self.assertEqual(candidate["question_ids"], original_ids)
        self.assertEqual(segments[0]["parent_practice_set_id"], "ps_big")
        self.assertEqual(segments[0]["part_index"], 1)
        self.assertEqual(segments[0]["part_count"], len(segments) + len(pending))
        self.assertLessEqual(segments[0]["estimated_minutes"], 69)

    def test_ai_review_plan_keeps_small_practice_sheet_whole(self) -> None:
        candidate = {
            "candidate_type": "unstarted_questions",
            "source_id": "sheet_small",
            "question_ids": ["q1", "q2"],
            "questions": [
                {"question_id": "q1", "question_type": "single_choice", "difficulty": "medium"},
                {"question_id": "q2", "question_type": "fill_blank", "difficulty": "unknown"},
            ],
            "state": "unstarted",
        }

        segments, pending = split_candidate_into_plan_segments(candidate, daily_minutes=60, days=7)

        self.assertEqual(len(segments), 1)
        self.assertEqual(pending, [])
        self.assertNotIn("part_index", segments[0])

    def test_ai_review_plan_commit_creates_practice_segment_from_planned_question_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            item = {
                "type": "unstarted_question",
                "title": "Large sheet - Part 1/3",
                "reason": "练习单过大，先完成第一段。",
                "date": "2099-01-02",
                "estimated_minutes": 58,
                "load_units": 8.1,
                "source_ids": ["ps_big__seg_1"],
                "planned_question_ids": ["kaoyan_math1_2099_q001", "kaoyan_math1_2099_q002"],
                "parent_practice_set_id": "ps_big",
                "parent_source_id": "ps_big",
                "plan_segment_id": "ps_big__seg_1",
                "part_index": 1,
                "part_count": 3,
            }

            validation = store.validate_ai_review_plan_items(
                "tester",
                items=[item],
                subject="math",
                daily_minutes=60,
            )
            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="plan_segment",
                plan_mode="balanced",
                plan_model="deepseek-v4-flash",
                plan_source="llm",
                subject="math",
                items=[item],
                daily_minutes=60,
            )

            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "practice_set")
            self.assertEqual(
                validation["valid_items"][0]["derived_practice_question_ids"],
                ["kaoyan_math1_2099_q001", "kaoyan_math1_2099_q002"],
            )
            self.assertEqual(result["created_count"], 1)
            review_task = result["results"][0]["review_task"]
            self.assertEqual(review_task["target_type"], "practice_set")
            self.assertEqual(review_task["source_meta"]["task_kind"], "ai_plan_practice_segment")
            self.assertEqual(review_task["source_meta"]["parent_practice_set_id"], "ps_big")
            self.assertEqual(review_task["source_meta"]["plan_segment_id"], "ps_big__seg_1")
            self.assertEqual(review_task["source_meta"]["part_index"], 1)
            self.assertEqual(review_task["source_meta"]["part_count"], 3)

    def test_ai_review_plan_commit_recovers_exact_practice_set_id_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=3,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            item = {
                "type": "draft_attempt",
                "title": practice_set["set_id"],
                "reason": "未提交练习，需继续完成",
                "estimated_minutes": 30,
                "date": "2099-01-02",
                "source_ids": [],
            }

            validation = store.validate_ai_review_plan_items(
                "tester",
                items=[item],
                subject="math",
            )
            result = store.create_review_tasks_from_ai_plan(
                "tester",
                plan_id="draft-practice-set-title",
                items=[item],
                subject="math",
                plan_mode="balanced",
            )

            self.assertEqual(validation["valid_count"], 1)
            self.assertEqual(validation["valid_items"][0]["target_type"], "practice_set")
            self.assertEqual(validation["valid_items"][0]["target_id"], practice_set["set_id"])
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["results"][0]["target_type"], "practice_set")
            self.assertEqual(result["results"][0]["target_id"], practice_set["set_id"])

    def test_ai_review_plan_validate_rejects_generic_items_without_real_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/ai-review-plan/validate",
                    params={"user_id": "tester"},
                    json={
                        "daily_minutes": 60,
                        "items": [
                            {
                                "type": "freeform_review",
                                "title": "泛化复习 limits",
                                "reason": "AI 建议但没有真实题目来源",
                                "estimated_minutes": 20,
                                "date": "2099-01-02",
                                "source_ids": ["limits"],
                            }
                        ],
                    },
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["validation"]["valid_count"], 0)
            self.assertEqual(payload["validation"]["rejected_count"], 1)
            self.assertIn("真实题目或练习单", payload["validation"]["rejected"][0]["reason"])

    def test_ai_review_plan_commit_skips_invalid_items_and_reports_daily_load_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            valid_one = {
                "type": "wrong_pool",
                "title": "复习 Q1",
                "estimated_minutes": 40,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q001"],
            }
            valid_two = {
                "type": "wrong_pool",
                "title": "复习 Q2",
                "estimated_minutes": 35,
                "date": "2099-01-02",
                "source_ids": ["kaoyan_math1_2099_q002"],
            }
            invalid = {
                "type": "freeform_review",
                "title": "泛化复习 limits",
                "estimated_minutes": 20,
                "date": "2099-01-03",
                "source_ids": ["limits"],
            }

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.post(
                    "/api/materials/system/ai-review-plan/commit",
                    params={"user_id": "tester"},
                    json={
                        "plan_id": "draft-test",
                        "subject": "math",
                        "daily_minutes": 60,
                        "items": [valid_one, valid_two, invalid],
                    },
                )
                list_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertTrue(payload["ok"])
            result = payload["result"]
            self.assertEqual(result["created_count"], 1)
            self.assertEqual(result["rejected_count"], 1)
            self.assertEqual(result["failed_count"], 0)
            self.assertTrue(result["warnings"])
            self.assertEqual(result["daily_load"][0]["date"], "2099-01-02")
            self.assertEqual(result["daily_load"][0]["minutes"], 75)
            tasks = list_response.json()["items"]
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["target_type"], "practice_set")
            self.assertEqual(tasks[0]["source_meta"]["question_count"], 2)
            self.assertEqual(result["results"][0]["merged_count"], 2)
            self.assertEqual(result["results"][0]["merged_item_indexes"], [0, 1])

    def test_ai_plan_payload_uses_invoked_model_not_model_claimed_by_llm(self) -> None:
        payload = _normalize_ai_plan_payload(
            {
                "plan_id": "draft-test",
                "model": "study_plan_v1",
                "days": [
                    {
                        "date": "2099-01-02",
                        "items": [
                            {
                                "type": "wrong_pool",
                                "title": "Review wrong questions",
                                "reason": "High priority",
                                "estimated_minutes": 20,
                            }
                        ],
                    }
                ],
            },
            context={"constraints": {"days": 1, "daily_minutes": 45}},
            model="deepseek-v4-flash",
        )

        self.assertEqual(payload["model"], "deepseek-v4-flash")
        self.assertEqual(payload["source"], "llm")

    def test_ai_plan_payload_repairs_question_mark_titles_from_source_ids(self) -> None:
        payload = _normalize_ai_plan_payload(
            {
                "plan_id": "draft-test",
                "days": [
                    {
                        "date": "2099-01-02",
                        "items": [
                            {
                                "type": "review_task",
                                "title": "2025 ?? Q1 ??",
                                "reason": "到期任务",
                                "estimated_minutes": 20,
                                "source_ids": ["task1"],
                            }
                        ],
                    }
                ],
            },
            context={
                "constraints": {"days": 1, "daily_minutes": 45},
                "ai_candidates": {"review_tasks": [{"task_id": "task1", "title": "2025 数一 Q1 复习"}]},
            },
            model="deepseek-v4-flash",
        )

        self.assertEqual(payload["days"][0]["items"][0]["title"], "2025 数一 Q1 复习")

    def test_ai_review_plan_prompt_uses_precomputed_load_and_segments(self) -> None:
        prompt = _planning_prompt(
            {
                "constraints": {"days": 2, "daily_minutes": 60, "mode": "balanced"},
                "policy": {"type_priority": ["draft_attempts"]},
                "ai_candidates": {
                    "draft_attempts": [
                        {
                            "source_id": "pa_big__seg_1",
                            "load_units": 8.1,
                            "estimated_minutes": 58,
                            "parent_practice_set_id": "ps_big",
                            "part_index": 1,
                            "part_count": 3,
                        }
                    ]
                },
            }
        )

        self.assertIn("load_units", prompt)
        self.assertIn("estimated_minutes", prompt)
        self.assertIn("每天负载尽量接近", prompt)
        self.assertIn("不区分周末/工作日", prompt)
        self.assertIn("题型会影响任务量", prompt)
        self.assertIn("不要自行拆分练习单", prompt)
        self.assertNotIn("璇峰", prompt)

    def test_ai_plan_normalization_recomputes_minutes_and_preserves_segment_metadata(self) -> None:
        context = {
            "constraints": {"days": 1, "daily_minutes": 60},
            "policy": {"enabled_types": ["draft_attempts"]},
            "ai_candidates": {
                "draft_attempts": [
                    {
                            "source_id": "pa_big__seg_1",
                        "candidate_type": "draft_attempts",
                        "title": "Large sheet - Part 1/3",
                        "load_units": 8.1,
                        "estimated_minutes": 58,
                        "parent_practice_set_id": "ps_big",
                        "part_index": 1,
                        "part_count": 3,
                    }
                ]
            },
        }

        payload = _normalize_ai_plan_payload(
            {
                "days": [
                    {
                        "date": "2099-01-02",
                        "items": [
                            {
                                "type": "continue_draft",
                                "title": "Bad estimate",
                                "estimated_minutes": 5,
                                "source_ids": ["pa_big__seg_1"],
                            }
                        ],
                    }
                ]
            },
            context=context,
            model="deepseek-v4-flash",
        )

        item = payload["days"][0]["items"][0]
        self.assertEqual(item["estimated_minutes"], 58)
        self.assertEqual(item["load_units"], 8.1)
        self.assertEqual(item["parent_practice_set_id"], "ps_big")
        self.assertEqual(item["part_index"], 1)
        self.assertEqual(item["part_count"], 3)

    def test_ai_review_plan_draft_falls_back_quickly_when_model_times_out(self) -> None:
        def slow_model_call(**_: object) -> dict:
            time.sleep(0.2)
            return {"days": []}

        with (
            patch("materials.system_ai_planner._planning_timeout_seconds", return_value=0.01),
            patch("materials.system_ai_planner._call_planning_model", side_effect=slow_model_call),
        ):
            started = time.perf_counter()
            draft = generate_ai_review_plan_draft(
                context={"constraints": {"days": 1, "daily_minutes": 30}, "ai_candidates": {}},
                model="deepseek-v4-flash",
            )
            elapsed = time.perf_counter() - started

        self.assertLess(elapsed, 0.15)
        self.assertEqual(draft["model"], "deepseek-v4-flash")
        self.assertEqual(draft["source"], "fallback")
        self.assertFalse(draft["writes_review_tasks"])

    def test_ai_review_plan_model_call_disables_thinking_and_requests_json(self) -> None:
        calls: list[dict] = []

        class FakeCompletions:
            def create(self, **kwargs: object) -> object:
                calls.append(dict(kwargs))
                message = SimpleNamespace(
                    content='{"plan_id":"draft-test","days":[{"date":"2099-01-02","items":[]}],"warnings":[]}'
                )
                return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=None)

        class FakeOpenAI:
            def __init__(self, **_: object) -> None:
                self.chat = SimpleNamespace(completions=FakeCompletions())

        with (
            patch.dict(
                os.environ,
                {
                    "AI_REVIEW_PLAN_API_KEY": "test-key",
                    "AI_REVIEW_PLAN_BASE_URL": "https://example.invalid/v1",
                    "AI_REVIEW_PLAN_MAX_TOKENS": "800",
                },
                clear=False,
            ),
            patch("openai.OpenAI", FakeOpenAI),
            patch("materials.system_ai_planner.load_dotenv", return_value=True),
            patch("qa.usage_tracking.notify_usage"),
        ):
            payload = _call_planning_model(
                context={"constraints": {"days": 1, "daily_minutes": 45}, "ai_candidates": {}},
                model="deepseek-v4-flash",
            )

        self.assertEqual(payload["plan_id"], "draft-test")
        call = calls[0]
        self.assertEqual(call["model"], "deepseek-v4-flash")
        self.assertEqual(call["temperature"], 0)
        self.assertEqual(call["max_tokens"], 800)
        self.assertEqual(call["response_format"], {"type": "json_object"})
        self.assertEqual(call["extra_body"], {"thinking": {"type": "disabled"}})

    def test_ai_review_plan_prompt_is_readable_chinese(self) -> None:
        prompt = _planning_prompt({"constraints": {"days": 1, "daily_minutes": 45}})

        self.assertIn("复习规划草案", prompt)
        self.assertIn("输出 JSON", prompt)
        self.assertNotIn("璇峰", prompt)

    def test_ai_review_plan_prompt_limits_output_size_to_avoid_truncated_json(self) -> None:
        from materials.system_ai_planner import DEFAULT_AI_REVIEW_PLAN_MAX_TOKENS

        prompt = _planning_prompt(
            {
                "constraints": {"days": 7, "daily_minutes": 60, "mode": "wrong"},
                "policy": {
                    "mode": "wrong",
                    "enabled_types": ["wrong_questions", "pending_review_items", "review_tasks"],
                    "type_priority": ["wrong_questions", "pending_review_items", "review_tasks"],
                },
            }
        )

        self.assertGreaterEqual(DEFAULT_AI_REVIEW_PLAN_MAX_TOKENS, 3000)
        self.assertIn("每天 item 数不是固定 3 个", prompt)
        self.assertIn("至少达到每日时长目标", prompt)
        self.assertIn("不要按题数或 item 数设上限", prompt)
        self.assertNotIn("每天最多", prompt)
        self.assertNotIn("source_ids 最多", prompt)
        self.assertIn("优先类型顺序", prompt)
        self.assertIn("不要平均铺开所有类型", prompt)

    def test_practice_set_to_review_plan_workflow_keeps_target_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                practice_response = client.post(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 2,
                        "same_type_only": True,
                        "exclude_mastered": False,
                        "topic_filters": ["limits"],
                        "source_scope": "same_library",
                        "title": "Limits practice set",
                    },
                )
                practice_set = practice_response.json()["practice_set"]
                review_response = client.post(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester"},
                    json={
                        "target_type": "practice_set",
                        "target_id": practice_set["set_id"],
                        "due_at": "2099-01-03",
                        "priority": 4,
                        "note": "finish as one paper",
                    },
                )
                task_id = review_response.json()["review_task"]["task_id"]
                type_filter_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester", "target_type": "practice_set", "subject": "math"},
                )
                postpone_response = client.patch(
                    f"/api/materials/system/review-tasks/{task_id}",
                    params={"user_id": "tester"},
                    json={"status": "pending", "due_at": "2099-01-04"},
                )
                cancel_response = client.patch(
                    f"/api/materials/system/review-tasks/{task_id}",
                    params={"user_id": "tester"},
                    json={"status": "cancelled"},
                )
                cancelled_filter_response = client.get(
                    "/api/materials/system/review-tasks",
                    params={"user_id": "tester", "date_group": "cancelled"},
                )
                restore_response = client.patch(
                    f"/api/materials/system/review-tasks/{task_id}",
                    params={"user_id": "tester"},
                    json={"status": "pending"},
                )
                complete_response = client.patch(
                    f"/api/materials/system/review-tasks/{task_id}",
                    params={"user_id": "tester"},
                    json={"status": "completed"},
                )

            self.assertEqual(practice_response.status_code, 200)
            self.assertEqual(practice_set["question_ids"], ["kaoyan_math1_2099_q002", "kaoyan_math1_2099_q004"])
            self.assertEqual(review_response.status_code, 200)
            review_task = review_response.json()["review_task"]
            self.assertEqual(review_task["target_type"], "practice_set")
            self.assertEqual(review_task["target_id"], practice_set["set_id"])
            self.assertEqual(review_task["subject"], "math")
            self.assertEqual(review_task["source_meta"]["question_count"], 2)
            self.assertEqual(review_task["source_meta"]["matching_topics"], ["limits"])
            self.assertEqual(type_filter_response.json()["total"], 1)
            self.assertEqual(postpone_response.json()["review_task"]["due_at"], "2099-01-04")
            self.assertEqual(cancel_response.json()["review_task"]["status"], "cancelled")
            self.assertEqual(cancelled_filter_response.json()["total"], 1)
            self.assertEqual(restore_response.json()["review_task"]["status"], "pending")
            self.assertEqual(complete_response.json()["review_task"]["status"], "completed")

    def _store(self, raw_root: Path, users_root: Path) -> SystemPracticeReviewStore:
        return SystemPracticeReviewStore(
            users_dir=users_root,
            library=SystemQuestionLibrary(raw_root=raw_root),
            state_store=UserSystemQuestionStateStore(base_dir=users_root),
        )

    def _make_raw_root(self, root: Path, include_blank: bool = False) -> Path:
        year_dir = root / "math" / "exam_papers" / "math1" / "2099"
        questions_dir = year_dir / "questions"
        questions_dir.mkdir(parents=True)

        rows = [
            self._row("kaoyan_math1_2099_q001", 1, "single_choice", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q002", 2, "single_choice", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q003", 3, "solution", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q004", 4, "single_choice", ["limits"]),
            self._row("kaoyan_math1_2099_q005", 5, "single_choice", ["derivatives"]),
        ]
        if include_blank:
            rows.append(self._row("kaoyan_math1_2099_q006", 6, "fill_blank", ["limits"], answer="42"))
        (year_dir / "questions.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )
        for row in rows:
            number = int(row["question_number"])
            (questions_dir / f"q{number:03d}.md").write_text(
                "\n".join(
                    [
                        "---",
                        f"question_id: {row['question_id']}",
                        "---",
                        "",
                        "## Question",
                        "",
                        f"Question {number}",
                        "",
                        "## Answer",
                        "",
                        "A",
                        "",
                        "## Explanation",
                        "",
                        f"Explanation {number}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        return root

    def _make_practice_order_raw_root(self, root: Path) -> Path:
        year_dir = root / "math" / "exam_papers" / "math1" / "2099"
        questions_dir = year_dir / "questions"
        questions_dir.mkdir(parents=True)

        rows = [
            self._row("kaoyan_math1_2099_q001", 1, "single_choice", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q002", 2, "single_choice", ["limits"]),
            self._row("kaoyan_math1_2099_q003", 3, "fill_blank", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q004", 4, "single_choice", ["limits", "continuity"]),
            self._row("kaoyan_math1_2099_q010", 10, "solution", ["limits", "continuity"]),
        ]
        (year_dir / "questions.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )
        for row in rows:
            number = int(row["question_number"])
            (questions_dir / f"q{number:03d}.md").write_text(
                "\n".join(
                    [
                        "---",
                        f"question_id: {row['question_id']}",
                        "---",
                        "",
                        "## Question",
                        "",
                        f"Question {number}",
                        "",
                        "## Answer",
                        "",
                        "A",
                    ]
                ),
                encoding="utf-8",
            )
        return root

    def _make_practice_ranking_eval_raw_root(self, root: Path) -> Path:
        rows_by_year = {
            2099: [
                self._row_for_year("kaoyan_math1_2099_q001", 1, "single_choice", ["limits", "continuity"], 2099),
                self._row_for_year("kaoyan_math1_2099_q003", 3, "single_choice", ["limits", "continuity", "derivatives", "series"], 2099),
                self._row_for_year("kaoyan_math1_2099_q004", 4, "single_choice", ["limits"], 2099),
                self._row_for_year("kaoyan_math1_2099_q005", 5, "solution", ["limits", "method"], 2099),
                self._row_for_year("kaoyan_math1_2099_q010", 10, "solution", ["matrix", "eigenvalue", "linear algebra"], 2099),
                self._row_for_year("kaoyan_math1_2099_q012", 12, "solution", ["matrix", "eigenvalue", "linear algebra", "rank"], 2099),
                self._row_for_year("kaoyan_math1_2099_q013", 13, "solution", ["matrix"], 2099),
                self._row_for_year("kaoyan_math1_2099_q014", 14, "single_choice", ["matrix", "eigenvalue"], 2099),
                self._row_for_year("kaoyan_math1_2099_q020", 20, "fill_blank", ["series", "convergence", "comparison"], 2099),
                self._row_for_year("kaoyan_math1_2099_q021", 21, "fill_blank", ["series", "convergence", "comparison", "power series"], 2099),
                self._row_for_year("kaoyan_math1_2099_q023", 23, "fill_blank", ["series"], 2099),
                self._row_for_year("kaoyan_math1_2099_q024", 24, "single_choice", ["series", "convergence"], 2099),
                self._row_for_year("kaoyan_math1_2099_q030", 30, "solution", ["probability", "distribution", "expectation"], 2099),
                self._row_for_year("kaoyan_math1_2099_q031", 31, "solution", ["probability", "distribution", "expectation", "variance"], 2099),
                self._row_for_year("kaoyan_math1_2099_q033", 33, "solution", ["probability"], 2099),
                self._row_for_year("kaoyan_math1_2099_q034", 34, "single_choice", ["probability", "distribution"], 2099),
                self._row_for_year("kaoyan_math1_2099_q040", 40, "single_choice", ["derivative", "monotonicity"], 2099),
                self._row_for_year("kaoyan_math1_2099_q041", 41, "single_choice", ["derivative", "monotonicity", "extremum"], 2099),
                self._row_for_year("kaoyan_math1_2099_q043", 43, "single_choice", ["derivative"], 2099),
                self._row_for_year("kaoyan_math1_2099_q044", 44, "solution", ["derivative", "monotonicity"], 2099),
                self._row_for_year("kaoyan_math1_2099_q050", 50, "solution", ["linear equation", "rank"], 2099),
                self._row_for_year("kaoyan_math1_2099_q051", 51, "solution", ["linear equation", "rank", "determinant"], 2099),
                self._row_for_year("kaoyan_math1_2099_q053", 53, "solution", ["rank"], 2099),
                self._row_for_year("kaoyan_math1_2099_q054", 54, "single_choice", ["linear equation", "rank"], 2099),
                self._row_for_year("kaoyan_math1_2099_q060", 60, "fill_blank", ["double integral", "region transformation"], 2099),
                self._row_for_year("kaoyan_math1_2099_q061", 61, "fill_blank", ["double integral", "region transformation", "polar coordinates"], 2099),
                self._row_for_year("kaoyan_math1_2099_q063", 63, "fill_blank", ["double integral"], 2099),
                self._row_for_year("kaoyan_math1_2099_q064", 64, "solution", ["double integral", "region transformation"], 2099),
                self._row_for_year("kaoyan_math1_2099_q070", 70, "single_choice", ["differential equation", "general solution"], 2099),
                self._row_for_year("kaoyan_math1_2099_q071", 71, "single_choice", ["differential equation", "general solution", "initial value"], 2099),
                self._row_for_year("kaoyan_math1_2099_q073", 73, "single_choice", ["differential equation"], 2099),
                self._row_for_year("kaoyan_math1_2099_q074", 74, "solution", ["differential equation", "general solution"], 2099),
                self._row_for_year("kaoyan_math1_2099_q080", 80, "solution", ["vector", "orthogonality", "geometry"], 2099),
                self._row_for_year("kaoyan_math1_2099_q081", 81, "solution", ["vector", "orthogonality", "geometry", "projection"], 2099),
                self._row_for_year("kaoyan_math1_2099_q083", 83, "solution", ["vector"], 2099),
                self._row_for_year("kaoyan_math1_2099_q084", 84, "single_choice", ["vector", "orthogonality"], 2099),
            ],
            2098: [
                self._row_for_year("kaoyan_math1_2098_q002", 2, "fill_blank", ["limits", "continuity"], 2098),
                self._row_for_year("kaoyan_math1_2098_q011", 11, "single_choice", ["matrix", "eigenvalue", "linear algebra"], 2098),
                self._row_for_year("kaoyan_math1_2098_q022", 22, "solution", ["series", "convergence", "comparison"], 2098),
                self._row_for_year("kaoyan_math1_2098_q032", 32, "single_choice", ["probability", "distribution", "expectation"], 2098),
                self._row_for_year("kaoyan_math1_2098_q042", 42, "fill_blank", ["derivative", "monotonicity"], 2098),
                self._row_for_year("kaoyan_math1_2098_q052", 52, "single_choice", ["linear equation", "rank"], 2098),
                self._row_for_year("kaoyan_math1_2098_q062", 62, "solution", ["double integral", "region transformation"], 2098),
                self._row_for_year("kaoyan_math1_2098_q072", 72, "solution", ["differential equation", "general solution"], 2098),
                self._row_for_year("kaoyan_math1_2098_q082", 82, "single_choice", ["vector", "orthogonality", "geometry"], 2098),
            ],
        }
        for year, rows in rows_by_year.items():
            year_dir = root / "math" / "exam_papers" / "math1" / str(year)
            questions_dir = year_dir / "questions"
            questions_dir.mkdir(parents=True)
            (year_dir / "questions.jsonl").write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                encoding="utf-8",
            )
            for row in rows:
                number = int(row["question_number"])
                (questions_dir / f"q{number:03d}.md").write_text(
                    "\n".join(
                        [
                            "---",
                            f"question_id: {row['question_id']}",
                            "---",
                            "",
                            "## Question",
                            "",
                            f"Question {year}-{number}",
                            "",
                            "## Answer",
                            "",
                            "A",
                        ]
                ),
                encoding="utf-8",
            )
        return root

    def _question_stat(
        self,
        question_id: str,
        topics: list[str],
        *,
        attempt_count: int,
        correct_count: int = 0,
        incorrect_count: int = 0,
        partial_count: int = 0,
        pending_review_count: int = 0,
        unanswered_count: int = 0,
        latest_status: str | None = None,
        correct_streak: int = 0,
        wrong_streak: int | None = None,
    ) -> dict:
        resolved_latest_status = latest_status
        if not resolved_latest_status:
            if incorrect_count or partial_count:
                resolved_latest_status = "incorrect"
            elif pending_review_count:
                resolved_latest_status = "pending_review"
            elif unanswered_count:
                resolved_latest_status = "unanswered"
            elif correct_count:
                resolved_latest_status = "correct"
            else:
                resolved_latest_status = "pending_review"
        resolved_wrong_streak = incorrect_count + partial_count if wrong_streak is None else wrong_streak
        return {
            "stat_id": question_id,
            "user_id": "tester",
            "question_id": question_id,
            "attempt_count": attempt_count,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "partial_count": partial_count,
            "pending_review_count": pending_review_count,
            "unanswered_count": unanswered_count,
            "latest_attempt_id": "attempt_test",
            "latest_status": resolved_latest_status,
            "latest_answer": "",
            "latest_practiced_at": "2099-01-01T00:00:00+00:00",
            "wrong_streak": resolved_wrong_streak,
            "correct_streak": correct_streak,
            "last_wrong_at": "2099-01-01T00:00:00+00:00" if incorrect_count or partial_count else "",
            "topics": topics,
        }

    def _row(
        self,
        question_id: str,
        number: int,
        question_type: str,
        topics: list[str],
        answer: str = "A",
    ) -> dict:
        return {
            "question_id": question_id,
            "exam_id": "kaoyan_math1_2099",
            "exam_type": "math1",
            "year": 2099,
            "question_number": number,
            "question_type": question_type,
            "module": "math",
            "topics": topics,
            "difficulty": "unknown",
            "card_path": f"questions/q{number:03d}.md",
            "assets": [],
            "answer": answer,
            "explanation": f"Explanation {number}",
            "summary": f"Question {number}",
        }

    def _row_for_year(
        self,
        question_id: str,
        number: int,
        question_type: str,
        topics: list[str],
        year: int,
    ) -> dict:
        row = self._row(question_id, number, question_type, topics)
        row["exam_id"] = f"kaoyan_math1_{year}"
        row["year"] = year
        row["summary"] = f"Question {year}-{number}"
        return row


if __name__ == "__main__":
    unittest.main()
