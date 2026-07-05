from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.system_library import SystemQuestionLibrary
from materials.system_practice_review import SystemPracticeReviewStore
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
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q003"]["status"], "needs_grading")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q004"]["status"], "incorrect")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q005"]["status"], "unanswered")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q006"]["status"], "needs_review")
            self.assertEqual(
                submitted["summary"],
                {
                    "total": 5,
                    "correct": 1,
                    "incorrect": 1,
                    "unanswered": 1,
                    "needs_review": 1,
                    "needs_grading": 1,
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
                            "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "42"},
                        }
                    },
                )
                submit_response = client.post(
                    f"/api/materials/system/practice-attempts/{attempt_id}/submit",
                    params={"user_id": "tester"},
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
            self.assertEqual(update_response.json()["practice_attempt"]["answers"]["kaoyan_math1_2099_q006"]["value"], "42")
            self.assertEqual(submit_response.status_code, 200)
            self.assertEqual(submit_response.json()["practice_attempt"]["status"], "submitted")
            self.assertEqual(submit_response.json()["practice_attempt"]["summary"]["correct"], 2)
            self.assertEqual(locked_response.status_code, 400)
            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(list_response.json()["practice_attempts"][0]["attempt_id"], attempt_id)

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
