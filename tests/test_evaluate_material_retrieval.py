from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scripts.evaluate_material_retrieval import CONFIGS, QueryCase, evaluate_case, summarize_result


class EvaluateMaterialRetrievalReportTest(unittest.TestCase):
    def test_summarize_result_includes_llm_rerank_metadata(self) -> None:
        result = SimpleNamespace(
            rank=1,
            score=0.5,
            material_id="mat_1",
            chunk_id="chunk_1",
            section_title="方差公式",
            heading_path=["概率统计", "方差"],
            text="方差公式 DX = EX^2 - (EX)^2",
            metadata={
                "search_mode": "llm",
                "matched_by": ["keyword", "vector"],
                "llm_rerank": {
                    "decision": "primary",
                    "rank": 1,
                    "confidence": 0.98,
                    "reason": "直接命中方差公式",
                },
                "retrieval_plan": {
                    "chunk_count": 181,
                    "recall_limit": 14,
                    "llm_candidate_limit": 6,
                },
            },
        )

        summary = summarize_result(result)

        self.assertEqual(summary["llm_rerank"]["decision"], "primary")
        self.assertEqual(summary["llm_rerank"]["reason"], "直接命中方差公式")
        self.assertEqual(summary["retrieval_plan"]["llm_candidate_limit"], 6)

    def test_evaluate_case_preserves_llm_rerank_order(self) -> None:
        llm_primary = SimpleNamespace(
            rank=1,
            score=0.1,
            material_id="mat_1",
            chunk_id="primary",
            section_title="LLM primary",
            heading_path=[],
            text="target concept",
            metadata={"search_mode": "llm", "llm_rerank": {"decision": "primary", "rank": 1}},
        )
        llm_related = SimpleNamespace(
            rank=2,
            score=100.0,
            material_id="mat_1",
            chunk_id="related",
            section_title="High hybrid score",
            heading_path=[],
            text="target concept",
            metadata={"search_mode": "llm", "llm_rerank": {"decision": "related", "rank": 2}},
        )
        case = QueryCase("x01", "target", "math", True, ("target",), 1)

        with patch(
            "scripts.evaluate_material_retrieval.search_user_materials",
            return_value=[llm_primary, llm_related],
        ):
            payload = evaluate_case(case, CONFIGS[-1], mode="llm", top_k=2)

        self.assertEqual(payload["top_results"][0]["chunk_id"], "primary")
        self.assertEqual(payload["top_results"][1]["chunk_id"], "related")


if __name__ == "__main__":
    unittest.main()
