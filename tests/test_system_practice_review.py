from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.system_library import SystemQuestionLibrary
from materials.system_practice_review import PRACTICE_ATTEMPT_ITEM_FILENAME, SystemPracticeReviewStore
from materials.system_practice_review_api import router as system_practice_review_router
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
