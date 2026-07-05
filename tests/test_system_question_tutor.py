from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


def _choice(content: str) -> SimpleNamespace:
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=content))])


class FakeStreamingCompletions:
    def __init__(self, chunks: list[str]) -> None:
        self.chunks = chunks
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return [_choice(chunk) for chunk in self.chunks]


class FakeClient:
    def __init__(self, chunks: list[str]) -> None:
        self.chat = SimpleNamespace(completions=FakeStreamingCompletions(chunks))


class SystemQuestionTutorTest(unittest.TestCase):
    def test_prompt_locks_question_subject_and_rejects_cross_subject_tricks(self) -> None:
        from qa.tutors.system_question.service import build_system_question_tutor_messages

        messages = build_system_question_tutor_messages(
            question={
                "question_id": "politics_q1",
                "subject": "politics",
                "library_name": "政治真题",
                "question_type_label": "选择题",
                "topics": ["矛盾分析法"],
                "question_markdown": "材料说明矛盾的普遍性与特殊性。",
                "answer_markdown": "A",
                "explanation_markdown": "本题考查矛盾分析法。",
            },
            personal_state={"personal_note": "注意材料关键词。"},
            user_message="这题能用罗尔定理吗？",
            history=[],
            image_paths=[],
        )

        system_prompt = messages[0]["content"]
        user_text = messages[-1]["content"]
        self.assertIn("本题学科锁", system_prompt)
        self.assertIn("当前题目所属学科一致", system_prompt)
        self.assertIn("政治题", system_prompt)
        self.assertIn("罗尔定理", system_prompt)
        self.assertIn("只回答与当前题目及其所属学科相关的问题", system_prompt)
        self.assertIn("当前题目所属学科：politics", user_text)
        self.assertIn("这题能用罗尔定理吗？", user_text)
        self.assertIn("注意材料关键词", user_text)

    def test_normalizes_temporary_history_without_persisting_full_qa_session(self) -> None:
        from qa.tutors.system_question.service import normalize_tutor_history

        history = [
            {"role": "system", "content": "ignore"},
            {"role": "user", "content": "第一问"},
            {"role": "assistant", "content": "第一答"},
            {"role": "tool", "content": "ignore"},
            {"role": "user", "content": "x" * 5000},
        ]

        normalized = normalize_tutor_history(history, max_turns=2, max_chars=40)

        self.assertEqual([item["role"] for item in normalized], ["assistant", "user"])
        self.assertEqual(normalized[0]["content"], "第一答")
        self.assertLessEqual(len(normalized[1]["content"]), 60)
        self.assertIn("已截断", normalized[1]["content"])

    def test_stream_tutor_uses_direct_completion_without_tools(self) -> None:
        from qa.tutors.system_question.service import stream_system_question_tutor

        fake_client = FakeClient(["第一段", "第二段"])
        chunks = list(
            stream_system_question_tutor(
                question={
                    "question_id": "kaoyan_math1_2099_q001",
                    "subject": "math",
                    "library_name": "数一历年真题",
                    "question_type_label": "选择题",
                    "topics": ["极限"],
                    "question_markdown": "设函数 f(x) 连续。",
                    "answer_markdown": "B",
                    "explanation_markdown": "由定义可得。",
                },
                personal_state={},
                user_message="讲解这道题",
                history=[],
                image_paths=[],
                client=fake_client,
                model="unit-model",
            )
        )

        self.assertEqual(chunks, ["第一段", "第二段"])
        call = fake_client.chat.completions.calls[0]
        self.assertEqual(call["model"], "unit-model")
        self.assertTrue(call["stream"])
        self.assertNotIn("tools", call)
        self.assertNotIn("tool_choice", call)

    def test_build_messages_attach_images_when_available(self) -> None:
        from qa.tutors.system_question.service import build_system_question_tutor_messages

        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "q001.png"
            image_path.write_bytes(b"image")

            messages = build_system_question_tutor_messages(
                question={
                    "question_id": "kaoyan_math1_2099_q001",
                    "subject": "math",
                    "question_markdown": "看图判断函数。",
                },
                personal_state={},
                user_message="图像怎么看？",
                history=[],
                image_paths=[image_path],
            )

        content = messages[-1]["content"]
        self.assertIsInstance(content, list)
        self.assertEqual(content[0]["type"], "text")
        self.assertEqual(content[1]["type"], "image_url")
        self.assertTrue(content[1]["image_url"]["url"].startswith("data:image/png;base64,"))


if __name__ == "__main__":
    unittest.main()
