from __future__ import annotations

import json
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from materials.llm_reranker import (
    apply_llm_decisions,
    build_candidate_payload,
    build_material_search_rerank_client_from_env,
    generate_material_search_rerank_with_qwen,
)
from materials.schemas import MaterialSearchResult


def search_result(chunk_id: str, *, score: float = 0.1, text: str | None = None) -> MaterialSearchResult:
    return MaterialSearchResult(
        rank=1,
        material_id="mat_1",
        user_id="tester",
        chunk_id=chunk_id,
        score=score,
        text=text if text is not None else f"{chunk_id} text",
        section_title=f"{chunk_id} title",
        heading_path=["资料", f"{chunk_id} title"],
        metadata={"matched_by": ["keyword"], "rerank_score": score},
    )


class MaterialsLlmRerankerTest(unittest.TestCase):
    def test_candidate_payload_truncates_text_and_preserves_scores(self) -> None:
        result = search_result("chunk_a", score=0.42, text="x" * 2000)

        payload = build_candidate_payload("方差公式", [result], max_text_chars=500)

        candidate = payload["candidates"][0]
        self.assertLessEqual(len(candidate["text"]), 530)
        self.assertEqual(candidate["chunk_id"], "chunk_a")
        self.assertEqual(candidate["score"], 0.42)
        self.assertEqual(candidate["matched_by"], ["keyword"])

    def test_apply_llm_decisions_outputs_primary_then_related_and_hides_noise(self) -> None:
        results = [
            search_result("noise", score=0.9),
            search_result("related", score=0.5),
            search_result("good", score=0.4),
        ]
        decisions = {
            "results": [
                {
                    "chunk_id": "good",
                    "decision": "primary",
                    "rank": 1,
                    "confidence": 0.9,
                    "reason": "直接回答",
                },
                {
                    "chunk_id": "related",
                    "decision": "related",
                    "rank": 2,
                    "confidence": 0.7,
                    "reason": "相关扩展",
                },
                {
                    "chunk_id": "noise",
                    "decision": "hide",
                    "rank": 3,
                    "confidence": 0.8,
                    "reason": "不能回答",
                },
            ]
        }

        ranked = apply_llm_decisions(results, decisions, top_k=5)

        self.assertEqual([item.chunk_id for item in ranked], ["good", "related"])
        self.assertEqual(ranked[0].rank, 1)
        self.assertEqual(ranked[1].rank, 2)
        self.assertEqual(ranked[0].metadata["llm_rerank"]["decision"], "primary")
        self.assertEqual(ranked[1].metadata["llm_rerank"]["decision"], "related")

    def test_build_client_returns_none_when_api_key_missing(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            client = build_material_search_rerank_client_from_env(env_path="E:/python_project/not-found.env")

        self.assertIsNone(client)

    def test_generate_rerank_with_qwen_requests_json_without_thinking(self) -> None:
        class FakeCompletions:
            def __init__(self) -> None:
                self.calls = []

            def create(self, **kwargs):
                self.calls.append(kwargs)
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(
                                content=json.dumps(
                                    {
                                        "results": [
                                            {
                                                "chunk_id": "chunk_a",
                                                "decision": "primary",
                                                "rank": 1,
                                                "confidence": 0.9,
                                                "reason": "直接回答",
                                            }
                                        ]
                                    },
                                    ensure_ascii=False,
                                )
                            )
                        )
                    ],
                    usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5, total_tokens=15),
                )

        fake_completions = FakeCompletions()
        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=fake_completions))

        with patch("openai.OpenAI", return_value=fake_client):
            result = generate_material_search_rerank_with_qwen(
                {"query": "方差公式", "candidates": []},
                model="qwen-test",
                api_key="test-key",
            )

        self.assertEqual(result["results"][0]["chunk_id"], "chunk_a")
        call = fake_completions.calls[0]
        self.assertEqual(call["response_format"], {"type": "json_object"})
        self.assertEqual(call["temperature"], 0)
        self.assertEqual(call["extra_body"], {"enable_thinking": False})


if __name__ == "__main__":
    unittest.main()
