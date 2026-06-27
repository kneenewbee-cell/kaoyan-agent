from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from materials.schemas import MaterialSearchResult
from materials.search_logger import write_material_search_log


class MaterialsSearchLoggerTest(unittest.TestCase):
    def test_write_material_search_log_summarizes_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(
            os.environ,
            {
                "MATERIALS_SEARCH_LOG_DIR": temp_dir,
                "MATERIALS_SEARCH_LOG_ENABLED": "1",
            },
        ):
            result = MaterialSearchResult(
                rank=1,
                material_id="mat_1",
                user_id="tester",
                chunk_id="chunk_1",
                score=0.8754321,
                text="Rolle theorem requires continuity on the closed interval.\n" * 8,
                section_title="Rolle theorem",
                heading_path=["math", "mean value theorem", "Rolle theorem"],
                source_markdown_path="parsed/content.md",
                metadata={
                    "original_filename": "rolle.md",
                    "subject": "math",
                    "material_type": "note",
                    "search_mode": "hybrid",
                    "matched_by": ["keyword", "vector"],
                    "distance": 0.1245678,
                },
            )

            path = write_material_search_log(
                user_id="tester",
                query="Rolle theorem",
                mode="hybrid",
                top_k=5,
                filters={"subject": "math"},
                results=[result],
                elapsed_ms=12.34,
            )

            self.assertIsNotNone(path)
            payload = json.loads(Path(path).read_text(encoding="utf-8").strip())
            self.assertEqual(payload["event"], "material_search")
            self.assertEqual(payload["query"], "Rolle theorem")
            self.assertEqual(payload["mode"], "hybrid")
            self.assertEqual(payload["filters"], {"subject": "math"})
            self.assertEqual(payload["result_count"], 1)
            self.assertEqual(payload["results"][0]["material_id"], "mat_1")
            self.assertEqual(payload["results"][0]["chunk_id"], "chunk_1")
            self.assertEqual(payload["results"][0]["matched_by"], ["keyword", "vector"])
            self.assertIn("text_preview", payload["results"][0])

    def test_search_log_can_be_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(
            os.environ,
            {
                "MATERIALS_SEARCH_LOG_DIR": temp_dir,
                "MATERIALS_SEARCH_LOG_ENABLED": "0",
            },
        ):
            path = write_material_search_log(
                user_id="tester",
                query="Rolle theorem",
                mode="keyword",
                top_k=5,
                filters=None,
                results=[],
            )

            self.assertIsNone(path)
            self.assertEqual(list(Path(temp_dir).glob("*.jsonl")), [])


if __name__ == "__main__":
    unittest.main()
