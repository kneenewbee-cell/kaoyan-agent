from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.user_state import UserSystemQuestionStateStore
from qa.tutors.system_question.api import router as system_question_tutor_router
from tests.test_system_library import SystemQuestionLibraryTest


class SystemQuestionTutorApiTest(unittest.TestCase):
    def test_api_streams_lightweight_system_question_tutor_from_qa_router(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = SystemQuestionLibraryTest()._make_raw_root(base / "raw")
            users_root = base / "users"
            UserSystemQuestionStateStore(users_root).update_question_state(
                "tester",
                "kaoyan_math1_2099_q001",
                {"personal_note": "注意定义法"},
            )
            app = FastAPI()
            app.include_router(system_question_tutor_router)
            client = TestClient(app)

            captured: dict[str, object] = {}

            def fake_stream_system_question_tutor(**kwargs):
                captured.update(kwargs)
                yield "第一段"
                yield "第二段"

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
                patch("qa.tutors.system_question.api.stream_system_question_tutor", fake_stream_system_question_tutor),
            ):
                response = client.post(
                    "/api/qa/system-questions/kaoyan_math1_2099_q001/tutor/stream",
                    params={"user_id": "tester"},
                    data={
                        "message": "这题能用罗尔定理吗？",
                        "history": '[{"role":"assistant","content":"先看定义。"}]',
                    },
                )

            self.assertEqual(response.status_code, 200)
            self.assertIn("第一段", response.text)
            self.assertIn("第二段", response.text)
            self.assertEqual(captured["user_message"], "这题能用罗尔定理吗？")
            self.assertEqual(captured["history"], [{"role": "assistant", "content": "先看定义。"}])
            self.assertEqual(captured["personal_state"]["personal_note"], "注意定义法")
            self.assertTrue(captured["image_paths"])


if __name__ == "__main__":
    unittest.main()
