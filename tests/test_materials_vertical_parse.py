from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from materials.service import MaterialIngestionService
from materials.storage import MaterialStorage


class MaterialsVerticalParseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.storage_patcher = patch("materials.storage.DEFAULT_USER_MATERIALS_DIR", self.base_dir)
        self.storage_patcher.start()
        self.addCleanup(self.storage_patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)
        self.service = MaterialIngestionService(storage=MaterialStorage(self.base_dir))

    def test_markdown_generates_content_and_parse_report(self) -> None:
        source = self.base_dir / "rolle.md"
        source.write_text(
            "罗尔定理\n========\n\n若函数在闭区间连续，在开区间可导，且端点函数值相等。\n",
            encoding="utf-8",
        )
        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="unknown",
            material_type="unknown",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )
        self.assertEqual(result.parse_status.value, "ready")

        material_dir = self.base_dir / "tester" / result.material_id
        content_path = material_dir / "parsed" / "content.md"
        report_path = material_dir / "parsed" / "parse_report.json"
        manifest_path = material_dir / "manifest.json"

        self.assertTrue(content_path.exists())
        self.assertTrue(report_path.exists())
        self.assertTrue(manifest_path.exists())
        self.assertIn("# 罗尔定理", content_path.read_text(encoding="utf-8"))

        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertIn(report["quality_status"], {"high", "medium", "low", "failed"})
        self.assertIn("overall_confidence", report)

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["paths"]["parse_report"], "parsed/parse_report.json")
        self.assertIn("quality_status", manifest)

    def test_text_converts_to_markdown_root_heading(self) -> None:
        source = self.base_dir / "高数笔记.txt"
        source.write_text(
            "罗尔定理\n\n若函数在闭区间连续，在开区间可导。\n\n证明思路\n\n利用费马定理。\n",
            encoding="utf-8",
        )
        result = self.service.ingest_file(source, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.parse_status.value, "ready")

        material_dir = self.base_dir / "tester" / result.material_id
        content = (material_dir / "parsed" / "content.md").read_text(encoding="utf-8")
        self.assertIn("# 高数笔记", content)
        self.assertIn("罗尔定理", content)
        self.assertNotIn("## 罗尔定理", content)
        self.assertTrue((material_dir / "parsed" / "parse_report.json").exists())
        self.assertGreaterEqual(result.chunk_count, 1)


if __name__ == "__main__":
    unittest.main()
