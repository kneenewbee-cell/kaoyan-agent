from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from materials.embeddings.text_builder import build_chunk_embedding_text
from materials.indexing.vector_indexer import build_material_vector_index, delete_material_vector_index
from materials.schemas import Chunk, MaterialManifest, MaterialSearchResult
from materials.search import _hybrid_results, search_user_materials, search_user_materials_vector


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
                    "material_type": "note",
                    "original_filename": "rolle.md",
                    "source_markdown_path": "parsed/content.md",
                }
            ]],
            "distances": [[0.12]],
        }


class MaterialsVectorIndexTest(unittest.TestCase):
    def test_embedding_text_includes_heading_context(self) -> None:
        chunk = Chunk(
            chunk_id="chunk_1",
            material_id="mat_1",
            user_id="tester",
            chunk_index=0,
            text="闭区间连续，开区间可导。",
            section_title="罗尔定理",
            heading_path=["高数", "中值定理", "罗尔定理"],
            metadata={"subject": "math", "material_type": "note", "title": "高数笔记"},
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
            metadata={"subject": "math", "material_type": "note", "original_filename": "rolle.md"},
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
