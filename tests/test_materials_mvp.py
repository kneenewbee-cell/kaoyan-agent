from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.api import router as materials_router
from materials.search import search_user_materials
from materials.service import MaterialIngestionService
from materials.storage import MaterialStorage


class MaterialsMvpTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.storage_patcher = patch("materials.storage.DEFAULT_USER_MATERIALS_DIR", self.base_dir)
        self.storage_patcher.start()
        self.addCleanup(self.storage_patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

        self.app = FastAPI()
        self.app.include_router(materials_router)
        self.client = TestClient(self.app)

        self.service = MaterialIngestionService(storage=MaterialStorage(self.base_dir))
        self.demo_md = Path("data/demo/test.md")
        self.demo_txt = Path("data/demo/test.txt")

    def test_md_ingest_success(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester")
        self.assertEqual(result.user_id, "tester")
        self.assertEqual(result.parse_status.value, "ready")
        material_dir = self.base_dir / "tester" / result.material_id
        self.assertTrue((material_dir / "manifest.json").exists())
        self.assertTrue((material_dir / "parsed" / "content.md").exists())
        self.assertTrue((material_dir / "chunks" / "chunks.jsonl").exists())
        self.assertTrue((material_dir / "index" / "search_index.json").exists())

    def test_txt_ingest_success(self) -> None:
        result = self.service.ingest_file(self.demo_txt, user_id="tester")
        self.assertEqual(result.parse_status.value, "ready")
        self.assertGreaterEqual(result.chunk_count, 1)

    def test_default_user_is_tester(self) -> None:
        result = self.service.ingest_file(self.demo_md)
        self.assertEqual(result.user_id, "tester")
        self.assertTrue((self.base_dir / "tester" / result.material_id).exists())

    def test_search_finds_expected_content(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester")
        self.assertEqual(result.parse_status.value, "ready")
        matches = search_user_materials("tester", "罗尔定理", storage=MaterialStorage(self.base_dir))
        self.assertTrue(matches)
        self.assertTrue(any("罗尔定理" in match.text for match in matches))

    def test_delete_removes_current_user_material(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester")
        material_dir = self.base_dir / "tester" / result.material_id
        payload = self.service.delete_material("tester", result.material_id)
        self.assertTrue(payload["deleted"])
        self.assertFalse(material_dir.exists())

    def test_user_isolation(self) -> None:
        tester_result = self.service.ingest_file(self.demo_md, user_id="tester")
        other_result = self.service.ingest_file(self.demo_txt, user_id="test_user_a")
        tester_items = self.service.list_materials("tester")
        other_items = self.service.list_materials("test_user_a")

        self.assertEqual([item["material_id"] for item in tester_items], [tester_result.material_id])
        self.assertEqual([item["material_id"] for item in other_items], [other_result.material_id])

        tester_search = search_user_materials("tester", "主要矛盾", storage=MaterialStorage(self.base_dir))
        self.assertEqual(tester_search, [])

        with self.assertRaises(FileNotFoundError):
            self.service.delete_material("tester", other_result.material_id)

    def test_unsupported_file_returns_clear_error(self) -> None:
        bad_file = self.base_dir / "unsupported.csv"
        bad_file.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
        result = self.service.ingest_file(bad_file, user_id="tester")
        self.assertEqual(result.parse_status.value, "failed")
        self.assertIn("Unsupported file type", result.error or "")

    def test_api_upload_list_search_delete(self) -> None:
        with self.demo_md.open("rb") as file:
            upload_response = self.client.post(
                "/api/materials/upload",
                files={"file": ("test.md", file, "text/markdown")},
                data={"subject": "unknown", "material_type": "unknown"},
            )
        self.assertEqual(upload_response.status_code, 200)
        upload_payload = upload_response.json()
        self.assertEqual(upload_payload["user_id"], "tester")
        material_id = upload_payload["material_id"]

        list_response = self.client.get("/api/materials/list")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.json()["items"][0]["material_id"], material_id)

        search_response = self.client.get("/api/materials/search", params={"query": "罗尔定理"})
        self.assertEqual(search_response.status_code, 200)
        self.assertGreaterEqual(search_response.json()["total_results"], 1)

        delete_response = self.client.delete(f"/api/materials/{material_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertTrue(delete_response.json()["deleted"])

        list_after_delete = self.client.get("/api/materials/list")
        self.assertEqual(list_after_delete.status_code, 200)
        self.assertEqual(list_after_delete.json()["items"], [])


if __name__ == "__main__":
    unittest.main()
