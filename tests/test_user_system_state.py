from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from materials.user_state import UserSystemQuestionStateStore


class UserSystemQuestionStateStoreTest(unittest.TestCase):
    def test_default_state_does_not_create_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            users_root = Path(tmp) / "users"
            store = UserSystemQuestionStateStore(base_dir=users_root)

            state = store.get_question_state("tester", "kaoyan_math1_2099_q001")

            self.assertEqual(state["user_id"], "tester")
            self.assertEqual(state["question_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(state["mastery_status"], "not_started")
            self.assertFalse(state["is_favorite"])
            self.assertFalse(state["in_wrong_book"])
            self.assertEqual(state["personal_note"], "")
            self.assertFalse((users_root / "tester" / "system_library" / "question_states.jsonl").exists())

    def test_update_persists_state_under_user_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            users_root = Path(tmp) / "users"
            store = UserSystemQuestionStateStore(base_dir=users_root)

            state = store.update_question_state(
                "tester",
                "kaoyan_math1_2099_q001",
                {
                    "mastery_status": "learning",
                    "is_favorite": True,
                    "in_wrong_book": True,
                    "personal_note": "watch the endpoint",
                },
            )

            state_path = users_root / "tester" / "system_library" / "question_states.jsonl"
            self.assertTrue(state_path.exists())
            self.assertEqual(state["mastery_status"], "learning")
            self.assertTrue(state["is_favorite"])
            self.assertTrue(state["in_wrong_book"])
            self.assertEqual(state["personal_note"], "watch the endpoint")
            self.assertIn("updated_at", state)

            roundtrip = UserSystemQuestionStateStore(base_dir=users_root).get_question_state(
                "tester",
                "kaoyan_math1_2099_q001",
            )
            self.assertEqual(roundtrip["mastery_status"], "learning")
            self.assertTrue(roundtrip["is_favorite"])
            self.assertTrue(roundtrip["in_wrong_book"])
            self.assertEqual(roundtrip["personal_note"], "watch the endpoint")

    def test_update_back_to_default_removes_state_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            users_root = Path(tmp) / "users"
            store = UserSystemQuestionStateStore(base_dir=users_root)
            state_path = users_root / "tester" / "system_library" / "question_states.jsonl"

            store.update_question_state(
                "tester",
                "kaoyan_math1_2099_q001",
                {"is_favorite": True},
            )
            self.assertTrue(state_path.exists())

            state = store.update_question_state(
                "tester",
                "kaoyan_math1_2099_q001",
                {
                    "mastery_status": "not_started",
                    "is_favorite": False,
                    "in_wrong_book": False,
                    "personal_note": "",
                    "last_practiced_at": None,
                    "review_due_at": None,
                },
            )

            self.assertEqual(state["mastery_status"], "not_started")
            self.assertFalse(state["is_favorite"])
            self.assertFalse(state["in_wrong_book"])
            self.assertEqual(state["personal_note"], "")
            self.assertIsNone(state["updated_at"])
            self.assertFalse(state_path.exists())

    def test_rejects_invalid_mastery_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = UserSystemQuestionStateStore(base_dir=Path(tmp) / "users")

            with self.assertRaises(ValueError):
                store.update_question_state(
                    "tester",
                    "kaoyan_math1_2099_q001",
                    {"mastery_status": "done"},
                )


if __name__ == "__main__":
    unittest.main()
