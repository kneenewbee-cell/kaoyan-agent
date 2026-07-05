from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from materials.embeddings.text_builder import build_chunk_embedding_text
from materials.indexing.vector_indexer import build_material_vector_index, delete_material_vector_index
from materials.schemas import Chunk, MaterialManifest, MaterialSearchResult
from materials.search import _hybrid_results, search_user_materials, search_user_materials_vector
from materials.search_planning import build_retrieval_plan


class FakeChromaStore:
    collection_name = "test_collection"

    def __init__(self) -> None:
        self.records = []
        self.deleted = []

    def collection(self):
        return self

    def upsert_records(self, records):
        self.records.extend(records)
        return len(records)

    def delete_material(self, user_id, material_id):
        self.deleted.append((user_id, material_id))

    def query(self, query_embedding, *, top_k, filters):
        return {
            "documents": [["罗尔定理要求闭区间连续，开区间可导。"]],
            "metadatas": [[
                {
                    "user_id": filters["user_id"],
                    "material_id": "mat_1",
                    "chunk_id": "chunk_1",
                    "chunk_index": 7,
                    "section_title": "罗尔定理",
                    "heading_path_text": "高数 > 中值定理 > 罗尔定理",
                    "subject": "math",
                    "material_type": "lecture",
                    "original_filename": "rolle.md",
                    "source_markdown_path": "parsed/content.md",
                }
            ]],
            "distances": [[0.12]],
        }


class MaterialsVectorIndexTest(unittest.TestCase):
    def test_adaptive_plan_for_small_scope_caps_llm_candidates(self) -> None:
        plan = build_retrieval_plan(chunk_count=60, query="方差公式", scope="material")

        self.assertEqual(plan.recall_limit, 12)
        self.assertEqual(plan.llm_candidate_limit, 6)
        self.assertEqual(plan.keyword_top_k, 6)
        self.assertEqual(plan.vector_top_k, 6)

    def test_adaptive_plan_for_large_subject_caps_absolute_budget(self) -> None:
        plan = build_retrieval_plan(
            chunk_count=2500,
            query="指数分布 均匀分布 正态分布",
            scope="subject",
        )

        self.assertEqual(plan.recall_limit, 80)
        self.assertEqual(plan.llm_candidate_limit, 32)
        self.assertTrue(plan.is_multi_intent)

    def test_embedding_text_includes_heading_context(self) -> None:
        chunk = Chunk(
            chunk_id="chunk_1",
            material_id="mat_1",
            user_id="tester",
            chunk_index=0,
            text="闭区间连续，开区间可导。",
            section_title="罗尔定理",
            heading_path=["高数", "中值定理", "罗尔定理"],
            metadata={"subject": "math", "material_type": "lecture", "title": "高数笔记"},
        )

        text = build_chunk_embedding_text(chunk)

        self.assertIn("标题路径：高数 > 中值定理 > 罗尔定理", text)
        self.assertIn("学科：math", text)
        self.assertIn("正文：", text)
        self.assertIn("闭区间连续", text)

    def test_vector_index_writes_chunk_records_to_store(self) -> None:
        chunk = Chunk(
            chunk_id="chunk_1",
            material_id="mat_1",
            user_id="tester",
            chunk_index=0,
            text="罗尔定理内容",
            heading_path=["高数", "罗尔定理"],
            metadata={"subject": "math", "material_type": "lecture", "original_filename": "rolle.md"},
        )
        manifest = MaterialManifest(
            material_id="mat_1",
            user_id="tester",
            original_filename="rolle.md",
            file_ext=".md",
            mime_type="text/markdown",
            sha256="abc",
        )
        store = FakeChromaStore()

        result = build_material_vector_index(
            [chunk],
            manifest,
            enabled=True,
            store=store,
            embedder=lambda texts: [[0.1, 0.2, 0.3] for _ in texts],
        )

        self.assertEqual(result.status, "ready")
        self.assertEqual(result.chunk_count, 1)
        self.assertEqual(store.records[0].record_id, "tester:mat_1:chunk_1")
        self.assertEqual(store.records[0].metadata["heading_path_text"], "高数 > 罗尔定理")

    def test_vector_index_preserves_table_metadata(self) -> None:
        chunk = Chunk(
            chunk_id="chunk_1",
            material_id="mat_1",
            user_id="tester",
            chunk_index=0,
            text="表格：课标要求\n考点: 函数定义域",
            metadata={
                "source_type": "table",
                "table_id": "table_001",
                "table_row_index": 2,
                "page": 18,
                "kind_guess": "data_table",
            },
        )
        manifest = MaterialManifest(
            material_id="mat_1",
            user_id="tester",
            original_filename="rolle.md",
            file_ext=".md",
            mime_type="text/markdown",
            sha256="abc",
        )
        store = FakeChromaStore()

        build_material_vector_index(
            [chunk],
            manifest,
            enabled=True,
            store=store,
            embedder=lambda texts: [[0.1, 0.2, 0.3] for _ in texts],
        )

        metadata = store.records[0].metadata
        self.assertEqual(metadata["source_type"], "table")
        self.assertEqual(metadata["table_id"], "table_001")
        self.assertEqual(metadata["table_row_index"], 2)

    def test_vector_search_uses_chroma_results(self) -> None:
        with patch.dict(os.environ, {"MATERIALS_EMBEDDING_API_KEY": "test-key"}), patch(
            "materials.search.embed_texts",
            return_value=[[0.1, 0.2, 0.3]],
        ), patch("materials.search._allowed_material_ids", return_value={"mat_1"}):
            results = search_user_materials_vector("tester", "罗尔定理", store=FakeChromaStore())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk_id, "chunk_1")
        self.assertEqual(results[0].heading_path, ["高数", "中值定理", "罗尔定理"])
        self.assertEqual(results[0].metadata["search_mode"], "vector")
        self.assertEqual(results[0].metadata["chunk_index"], 7)

    def test_hybrid_falls_back_to_keyword_when_vector_unavailable(self) -> None:
        keyword_result = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="chunk_1",
            score=1.0,
            text="罗尔定理",
        )
        with patch("materials.search.search_user_materials_keyword", return_value=[keyword_result]) as keyword, patch(
            "materials.search.search_user_materials_vector",
            return_value=[],
        ) as vector:
            results = search_user_materials("tester", "罗尔定理", mode="hybrid")

        self.assertEqual(results, [keyword_result])
        keyword.assert_called_once()
        vector.assert_called_once()

    def test_llm_mode_uses_adaptive_high_recall_then_applies_decisions(self) -> None:
        keyword_good = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="variance",
            score=5.0,
            text="variance formula and definition",
            section_title="variance",
        )
        keyword_noise = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="covariance",
            score=4.5,
            text="covariance definition",
            section_title="covariance",
        )
        vector_related = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="normal_variance",
            score=0.78,
            text="normal distribution variance",
            section_title="normal distribution",
            metadata={"search_mode": "vector"},
        )

        class FakeRerankClient:
            def __init__(self) -> None:
                self.payloads = []

            def rerank(self, payload):
                self.payloads.append(payload)
                return {
                    "results": [
                        {
                            "chunk_id": "variance",
                            "decision": "primary",
                            "rank": 1,
                            "confidence": 0.94,
                            "reason": "direct match",
                        },
                        {
                            "chunk_id": "normal_variance",
                            "decision": "related",
                            "rank": 2,
                            "confidence": 0.78,
                            "reason": "related formula",
                        },
                        {
                            "chunk_id": "covariance",
                            "decision": "hide",
                            "rank": 3,
                            "confidence": 0.8,
                            "reason": "different concept",
                        },
                    ]
                }

        fake_client = FakeRerankClient()
        with patch("materials.search.search_user_materials_keyword", return_value=[keyword_good, keyword_noise]) as keyword, patch(
            "materials.search.search_user_materials_vector",
            return_value=[vector_related],
        ) as vector, patch("materials.search._search_scope_chunk_count", return_value=500, create=True), patch(
            "materials.search._expand_result_split_context",
            side_effect=lambda results, **_kwargs: results,
        ):
            results = search_user_materials(
                "tester",
                "variance formula",
                top_k=5,
                mode="llm",
                rerank_client=fake_client,
            )

        self.assertEqual([result.chunk_id for result in results], ["variance", "normal_variance"])
        self.assertEqual(results[0].metadata["search_mode"], "llm")
        self.assertEqual(results[0].metadata["llm_rerank"]["decision"], "primary")
        self.assertEqual(results[1].metadata["llm_rerank"]["decision"], "related")
        self.assertGreater(keyword.call_args.kwargs["top_k"], 5)
        self.assertGreater(vector.call_args.kwargs["top_k"], 5)
        self.assertLessEqual(len(fake_client.payloads[0]["candidates"]), 15)

    def test_llm_mode_can_return_empty_when_all_candidates_are_hidden(self) -> None:
        keyword_noise = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="noise",
            score=5.0,
            text="unrelated chunk",
            section_title="unrelated",
        )

        class HideAllRerankClient:
            def rerank(self, payload):
                return {
                    "results": [
                        {
                            "chunk_id": item["chunk_id"],
                            "decision": "hide",
                            "rank": index,
                            "confidence": 0.8,
                            "reason": "not relevant",
                        }
                        for index, item in enumerate(payload["candidates"], start=1)
                    ]
                }

        with patch("materials.search.search_user_materials_keyword", return_value=[keyword_noise]), patch(
            "materials.search.search_user_materials_vector",
            return_value=[],
        ), patch("materials.search._search_scope_chunk_count", return_value=80, create=True), patch(
            "materials.search._expand_result_split_context",
            side_effect=lambda results, **_kwargs: results,
        ):
            results = search_user_materials(
                "tester",
                "law meaning",
                top_k=5,
                mode="llm",
                rerank_client=HideAllRerankClient(),
            )

        self.assertEqual(results, [])

    def test_hybrid_does_not_add_rank_score_for_same_source_duplicate_text(self) -> None:
        duplicate_a = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="dup_a",
            score=10.0,
            text="same irrelevant text",
        )
        duplicate_b = MaterialSearchResult(
            rank=2,
            material_id="mat_2",
            user_id="tester",
            chunk_id="dup_b",
            score=9.0,
            text="same irrelevant text",
        )

        results = _hybrid_results([duplicate_a, duplicate_b], [], top_k=1)

        self.assertEqual(results[0].chunk_id, "dup_a")
        self.assertLess(results[0].score, 0.02)

    def test_hybrid_allows_high_confidence_vector_result_to_beat_keyword_noise(self) -> None:
        keyword_noise = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="keyword_noise",
            score=12.0,
            text="generic keyword match",
        )
        vector_exact = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="vector_exact",
            score=0.82,
            text="exact semantic match",
            metadata={"search_mode": "vector"},
        )

        results = _hybrid_results([keyword_noise], [vector_exact], top_k=2)

        self.assertEqual(results[0].chunk_id, "vector_exact")
        self.assertEqual(results[0].metadata["matched_by"], ["vector"])

    def test_hybrid_rerank_prefers_heading_hit_over_overview_table_for_specific_query(self) -> None:
        overview_table = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="overview_table",
            score=0.7,
            text="表格：考试内容与考试要求。微分方程、欧拉方程、齐次方程均为考试内容。",
            section_title="第四章 常微分方程",
            heading_path=["第四章 常微分方程"],
            metadata={"source_type": "table", "kind_guess": "overview_table"},
        )
        heading_hit = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="euler",
            score=0.65,
            text="形如 x^n y^(n)+... 的方程称为欧拉方程，通常作变量代换。",
            section_title="4. 欧拉方程(仅数学一要求)",
            heading_path=["第四章 常微分方程", "高阶线性微分方程", "4. 欧拉方程(仅数学一要求)"],
        )

        results = _hybrid_results(
            [overview_table, heading_hit],
            [overview_table, heading_hit],
            top_k=2,
            query="欧拉型微分方程一般怎么处理",
        )

        self.assertEqual(results[0].chunk_id, "euler")
        if len(results) > 1:
            self.assertGreater(results[0].metadata["rerank_score"], results[1].metadata["rerank_score"])

    def test_hybrid_rerank_allows_overview_table_for_overview_query(self) -> None:
        overview_table = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="overview_table",
            score=0.7,
            text="表格：考试内容与考试要求。微分方程及其阶、解、通解、初始条件。",
            section_title="考试内容与考试要求",
            heading_path=["第四章 常微分方程"],
            metadata={"source_type": "table", "kind_guess": "overview_table"},
        )
        concept = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="concept",
            score=0.65,
            text="微分方程的通解和特解是基础概念。",
            section_title="微分方程的通解",
            heading_path=["第四章 常微分方程", "微分方程的通解"],
        )

        results = _hybrid_results(
            [overview_table, concept],
            [overview_table, concept],
            top_k=2,
            query="常微分方程考试要求",
        )

        self.assertEqual(results[0].chunk_id, "overview_table")

    def test_hybrid_filters_vector_only_result_missing_exact_phrase(self) -> None:
        exact = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="rolle",
            score=0.7,
            text="\u7f57\u5c14\u5b9a\u7406\u8981\u6c42\u95ed\u533a\u95f4\u8fde\u7eed\u3001\u5f00\u533a\u95f4\u53ef\u5bfc\u3002",
            section_title="\u7f57\u5c14\u5b9a\u7406",
        )
        vector_noise = MaterialSearchResult(
            rank=2,
            material_id="mat_2",
            user_id="tester",
            chunk_id="clt",
            score=0.82,
            text="\u4e2d\u5fc3\u6781\u9650\u5b9a\u7406\u548c\u5927\u6570\u5b9a\u5f8b\u7684\u76f8\u5173\u5185\u5bb9\u3002",
            section_title="\u4e2d\u5fc3\u6781\u9650\u5b9a\u7406",
            metadata={"search_mode": "vector"},
        )

        results = _hybrid_results(
            [exact],
            [exact, vector_noise],
            top_k=5,
            query="\u7f57\u5c14\u5b9a\u7406\u600e\u4e48\u7406\u89e3",
        )

        self.assertEqual([result.chunk_id for result in results], ["rolle"])

    def test_hybrid_filters_broad_topic_when_context_terms_are_missing(self) -> None:
        specific = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="sinicization",
            score=0.75,
            text=(
                "\u9a6c\u514b\u601d\u4e3b\u4e49\u4e2d\u56fd\u5316\u65f6\u4ee3\u5316\u8981\u628a"
                "\u9a6c\u514b\u601d\u4e3b\u4e49\u57fa\u672c\u539f\u7406\u540c\u4e2d\u56fd\u5177\u4f53\u5b9e\u9645\u76f8\u7ed3\u5408\u3002"
            ),
            section_title="\u9a6c\u514b\u601d\u4e3b\u4e49\u4e2d\u56fd\u5316\u65f6\u4ee3\u5316\u7684\u5185\u6db5",
        )
        broad = MaterialSearchResult(
            rank=1,
            material_id="mat_2",
            user_id="tester",
            chunk_id="generic_marxism",
            score=0.8,
            text="\u9a6c\u514b\u601d\u4e3b\u4e49\u5177\u6709\u79d1\u5b66\u6027\u3001\u4eba\u6c11\u6027\u3001\u5b9e\u8df5\u6027\u548c\u53d1\u5c55\u6027\u3002",
            section_title="\u9a6c\u514b\u601d\u4e3b\u4e49\u7684\u57fa\u672c\u7279\u5f81",
        )

        results = _hybrid_results(
            [broad, specific],
            [broad, specific],
            top_k=5,
            query="\u9a6c\u514b\u601d\u4e3b\u4e49\u4e3a\u4ec0\u4e48\u8981\u548c\u4e2d\u56fd\u5b9e\u9645\u7ed3\u5408",
        )

        self.assertEqual([result.chunk_id for result in results], ["sinicization"])

    def test_hybrid_keyword_fallback_suppresses_single_weak_term_match(self) -> None:
        weak_keyword = MaterialSearchResult(
            rank=1,
            material_id="mat_math",
            user_id="tester",
            chunk_id="confidence_interval",
            score=4.3,
            text="\u7f6e\u4fe1\u533a\u95f4\u4e2d\u542b\u6709\u4e00\u4e2a\u672a\u77e5\u53c2\u6570\u7684\u542b\u4e49\u3002",
            section_title="\u7f6e\u4fe1\u533a\u95f4",
        )

        with patch("materials.search.search_user_materials_keyword", return_value=[weak_keyword]), patch(
            "materials.search.search_user_materials_vector",
            return_value=[],
        ):
            results = search_user_materials(
                "tester",
                "\u6cd5\u5f8b\u7684\u542b\u4e49",
                top_k=5,
                mode="hybrid",
            )

        self.assertEqual(results, [])

    def test_hybrid_exact_heading_phrase_beats_related_heading(self) -> None:
        related = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="legal_thinking",
            score=0.74,
            text="\u6cd5\u6cbb\u601d\u7ef4\u4ee5\u6cd5\u5f8b\u539f\u5219\u548c\u6cd5\u5f8b\u89c4\u5219\u4e3a\u4f9d\u636e\u3002",
            section_title="\u6cd5\u6cbb\u601d\u7ef4\u7684\u542b\u4e49",
            heading_path=["26\u8003\u7814\u653f\u6cbb", "\u6cd5\u6cbb\u601d\u7ef4\u7684\u542b\u4e49"],
        )
        exact = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="law_meaning",
            score=0.70,
            text="\u6cd5\u5f8b\u7684\u542b\u4e49\uff1a\u6cd5\u5f8b\u662f\u7531\u56fd\u5bb6\u521b\u5236\u548c\u5b9e\u65bd\u7684\u884c\u4e3a\u89c4\u8303\u3002",
            section_title="\u8003\u70b952\uff1a\u6cd5\u5f8b\u7684\u542b\u4e49",
            heading_path=["26\u8003\u7814\u653f\u6cbb", "\u7b2c 8 \u8bfe", "\u8003\u70b952\uff1a\u6cd5\u5f8b\u7684\u542b\u4e49"],
        )

        results = _hybrid_results(
            [related, exact],
            [related, exact],
            top_k=2,
            query="\u6cd5\u5f8b\u7684\u542b\u4e49",
        )

        self.assertEqual(results[0].chunk_id, "law_meaning")

    def test_search_limits_duplicate_rows_from_same_table(self) -> None:
        table_result_a = MaterialSearchResult(
            rank=1,
            material_id="mat_1",
            user_id="tester",
            chunk_id="row_1",
            score=2.0,
            text="表格：课标要求\n考点: 函数定义域",
            metadata={"source_type": "table", "table_id": "table_001"},
        )
        table_result_b = MaterialSearchResult(
            rank=2,
            material_id="mat_1",
            user_id="tester",
            chunk_id="row_2",
            score=1.8,
            text="表格：课标要求\n考点: 函数值域",
            metadata={"source_type": "table", "table_id": "table_001"},
        )
        normal_result = MaterialSearchResult(
            rank=3,
            material_id="mat_1",
            user_id="tester",
            chunk_id="normal_1",
            score=1.2,
            text="函数概念正文",
        )
        with patch(
            "materials.search.search_user_materials_keyword",
            return_value=[table_result_a, table_result_b, normal_result],
        ), patch("materials.search.search_user_materials_vector", return_value=[]):
            results = search_user_materials("tester", "函数概念", top_k=5, mode="hybrid")

        self.assertEqual([result.chunk_id for result in results], ["row_1", "normal_1"])

    def test_vector_delete_runs_even_when_indexing_disabled(self) -> None:
        store = FakeChromaStore()

        with patch.dict(os.environ, {"MATERIALS_VECTOR_INDEX_ENABLED": "0"}):
            result = delete_material_vector_index("tester", "mat_1", store=store)

        self.assertEqual(result.status, "ready")
        self.assertEqual(store.deleted, [("tester", "mat_1")])


if __name__ == "__main__":
    unittest.main()
