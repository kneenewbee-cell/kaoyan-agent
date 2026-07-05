from __future__ import annotations

import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from materials.postprocess.deepseek_structure_client import (
    DEFAULT_DEEPSEEK_STRUCTURE_MODEL,
    build_deepseek_structure_repair_client_from_env,
    generate_problem_boundary_judgement_with_deepseek,
)


class _FakeCompletions:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(dict(kwargs))
        payload = {
            "decision": "split_previous_problem",
            "target_problem_index": 20,
            "start_line": 75,
            "end_line": 78,
            "confidence": 0.88,
            "title": "(20) 设平面有界区域D",
            "reason_codes": ["previous_problem_absorption"],
        }
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload, ensure_ascii=False)))],
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=8, total_tokens=18),
        )


class _FakeOpenAIClient:
    def __init__(self) -> None:
        self.completions = _FakeCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


class DeepSeekStructureClientTest(unittest.TestCase):
    def test_build_client_returns_none_when_api_key_is_missing(self) -> None:
        with patch.dict(
            os.environ,
            {
                "MATERIALS_STRUCTURE_REPAIR_API_KEY": "",
                "DEEPSEEK_API_KEY": "",
            },
            clear=False,
        ):
            client = build_deepseek_structure_repair_client_from_env(env_path="E:/python_project/not-found.env")

        self.assertIsNone(client)

    def test_boundary_judgement_uses_v4_flash_without_thinking_mode(self) -> None:
        fake_client = _FakeOpenAIClient()
        payload = {
            "candidate_type": "previous_problem_absorption",
            "target_missing_index": 20,
            "candidate_lines": [{"line_no": 75, "text": "设平面有界区域D..."}],
        }

        with patch("openai.OpenAI", return_value=fake_client):
            result = generate_problem_boundary_judgement_with_deepseek(
                payload,
                api_key="test-key",
                base_url="https://deepseek.example/v1",
                timeout_seconds=1,
            )

        call = fake_client.completions.calls[0]
        self.assertEqual(call["model"], DEFAULT_DEEPSEEK_STRUCTURE_MODEL)
        self.assertEqual(call["temperature"], 0)
        self.assertEqual(call["response_format"], {"type": "json_object"})
        self.assertEqual(call["extra_body"], {"thinking": {"type": "disabled"}})
        self.assertNotIn("reasoning_effort", call)
        self.assertEqual(result["target_problem_index"], 20)


if __name__ == "__main__":
    unittest.main()
