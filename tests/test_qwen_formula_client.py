from __future__ import annotations

import os
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from materials.postprocess.qwen_formula_client import (
    build_qwen_formula_repair_client_from_env,
    generate_formula_variants_with_qwen,
)


class APITimeoutError(Exception):
    pass


class _FakeCompletions:
    def __init__(self) -> None:
        self.attempts = 0

    def create(self, **_: object) -> SimpleNamespace:
        self.attempts += 1
        if self.attempts == 1:
            raise APITimeoutError("temporary timeout")
        payload = {
            "formula_id": "formula_0001",
            "variants": [
                {
                    "formula": r"\mu + 1",
                    "confidence": 0.95,
                    "reason": "replace unsupported textmu",
                }
            ],
        }
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))],
            usage=SimpleNamespace(prompt_tokens=3, completion_tokens=4, total_tokens=7),
        )


class _FakeOpenAIClient:
    def __init__(self) -> None:
        self.completions = _FakeCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


class QwenFormulaClientTest(unittest.TestCase):
    def test_build_client_returns_none_when_api_key_is_missing(self) -> None:
        with patch.dict(os.environ, {"QWEN_API_KEY": "", "DASHSCOPE_API_KEY": ""}, clear=False):
            client = build_qwen_formula_repair_client_from_env(env_path="E:/python_project/not-found.env")

        self.assertIsNone(client)

    def test_formula_variants_retries_timeout_once_and_returns_json(self) -> None:
        fake_client = _FakeOpenAIClient()
        payload = {
            "formula_id": "formula_0001",
            "formula": r"\textmu + 1",
            "container": "inline_math",
            "line_start": 1,
            "line_end": 1,
        }

        with patch("openai.OpenAI", return_value=fake_client), patch("time.sleep", return_value=None):
            result = generate_formula_variants_with_qwen(
                payload,
                model="qwen-test",
                api_key="test-key",
                base_url="https://example.test/v1",
                timeout_seconds=1,
            )

        self.assertEqual(fake_client.completions.attempts, 2)
        self.assertEqual(result["variants"][0]["formula"], r"\mu + 1")


if __name__ == "__main__":
    unittest.main()
