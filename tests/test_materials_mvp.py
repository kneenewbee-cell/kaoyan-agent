from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.api import router as materials_router
from materials.indexing.material_indexer import build_search_index
from materials.indexing.vector_indexer import VectorIndexResult
from materials.schemas import Chunk, MaterialManifest, MaterialType, ParseStatus
from materials.search import search_user_materials
from materials.service import MaterialIngestionService
from materials.storage import MaterialStorage
from materials.tools import _score_kind


def qwen_bundle_for_metadata(subject: str, material_type: str, confidence: float = 0.92) -> dict:
    return {
        "metadata_profile": {
            "subject": subject,
            "material_type": material_type,
            "confidence": confidence,
            "evidence": [f"detected as {subject}/{material_type}"],
        },
        "cleaning_strategy": {
            "version": "1.2",
            "document_profile": {
                "subject": subject,
                "document_type": "knowledge_notes",
                "language": "zh",
                "confidence": confidence,
            },
            "main_section_rule": {
                "enabled": False,
                "target_level": 2,
                "marker_type": "none",
                "aliases": [],
                "number_styles": [],
                "requires_line_start": True,
                "requires_colon": False,
                "min_repeats": 2,
                "examples": [],
            },
            "subsection_rules": [],
            "heading_families": [],
            "relation_hints": [],
            "metadata_rules": {
                "recognize_bracket_fields": True,
                "fields": ["考频", "难度", "题型", "来源", "备注"],
            },
            "cleanup_rules": {
                "normalize_blank_lines": True,
                "strip_trailing_spaces": True,
                "remove_control_chars": True,
                "preserve_tables": True,
                "preserve_code_blocks": True,
                "preserve_formulas": True,
                "preserve_images": True,
            },
            "fallback_policy": {
                "if_main_sections_less_than": 2,
                "action": "keep_original_structure",
                "chunk_by": "length",
                "reason": "test strategy",
            },
            "safety_rules": {
                "do_not_rewrite_content": True,
                "do_not_summarize": True,
                "do_not_translate": True,
                "do_not_delete_unknown_lines": True,
            },
        },
        "document_zones": {
            "front_matter_zones": [],
            "body_start_line": None,
            "confidence": 0.0,
        },
    }


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

    def test_material_type_contract_uses_three_active_types(self) -> None:
        self.assertEqual(
            [item.value for item in MaterialType],
            ["textbook", "lecture", "exercise", "unknown"],
        )
        self.assertNotIn("note", MaterialType._value2member_map_)
        self.assertNotIn("exam", MaterialType._value2member_map_)
        self.assertNotIn("wrong_book", MaterialType._value2member_map_)
        self.assertNotIn("school_info", MaterialType._value2member_map_)
        self.assertNotIn("other", MaterialType._value2member_map_)

    def test_legacy_material_type_values_are_mapped_on_manifest_read(self) -> None:
        base_payload = {
            "material_id": "mat_legacy",
            "user_id": "tester",
            "original_filename": "legacy.md",
            "file_ext": ".md",
            "mime_type": "text/markdown",
            "sha256": "abc",
            "subject": "math",
            "parser_name": "markdown",
            "parse_status": "ready",
        }
        cases = {
            "note": "lecture",
            "exam": "exercise",
            "wrong_book": "exercise",
            "school_info": "lecture",
            "other": "lecture",
        }
        for legacy_value, expected in cases.items():
            with self.subTest(legacy_value=legacy_value):
                payload = {**base_payload, "material_type": legacy_value}
                manifest = MaterialManifest.from_dict(payload)
                self.assertEqual(manifest.material_type.value, expected)

    def test_service_normalizes_legacy_material_type_inputs(self) -> None:
        cases = {
            "textbook": "textbook",
            "lecture": "lecture",
            "exercise": "exercise",
            "note": "lecture",
            "exam": "exercise",
            "wrong_book": "exercise",
            "school_info": "lecture",
            "other": "lecture",
            "unknown": "unknown",
            "auto": "unknown",
            "": "unknown",
        }
        for raw_value, expected in cases.items():
            with self.subTest(raw_value=raw_value):
                normalized = MaterialIngestionService._normalize_material_type(raw_value, "sample.md")
                self.assertEqual(normalized.value, expected)

    def test_api_rejects_legacy_material_type_filters(self) -> None:
        response = self.client.get(
            "/api/materials/search",
            params={
                "user_id": "tester",
                "query": "极限",
                "material_type": "exam",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_ingest_records_exam_paper_structure_profile_for_exam_like_exercise(self) -> None:
        source = self.base_dir / "2023考研数学二真题.md"
        source.write_text(
            "# 2023年全国硕士研究生招生考试数学（二）试题\n\n"
            "## 一、选择题\n\n"
            "(1) 设函数 f(x) 连续，求极限。\n\n"
            "## 二、填空题\n\n"
            "(11) 已知矩阵 A，求行列式。\n",
            encoding="utf-8",
        )

        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="exercise",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertIsNone(result.error)
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.material_type.value, "exercise")
        self.assertEqual(
            manifest.metadata.get("structure_profile", {}).get("exercise_kind"),
            "exam_paper",
        )

    def test_exercise_ingest_writes_structure_report_and_problem_chunk_metadata(self) -> None:
        source = self.base_dir / "exercise_examples.md"
        source.write_text(
            "# 例题资料\n\n"
            "## 一、选择题\n\n"
            "### (1) 设函数 f(x) 连续，求极限\n\n"
            "A. 0\nB. 1\n\n"
            "**解析：** 先化简再代入。\n\n"
            "### (2) 已知矩阵 A，求行列式\n\n"
            "**答案：** 2\n",
            encoding="utf-8",
        )

        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="exercise",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertIsNone(result.error)
        material_dir = MaterialStorage(self.base_dir).material_dir("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))
        manifest = json.loads((material_dir / "manifest.json").read_text(encoding="utf-8"))
        chunks = [
            json.loads(line)
            for line in (material_dir / "chunks" / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        self.assertEqual(report["metrics"]["exercise_structure"]["problem_count"], 2)
        self.assertEqual(report["metrics"]["exercise_structure"]["status"], "high")
        self.assertEqual(manifest["metadata"]["exercise_structure"]["problem_count"], 2)
        self.assertTrue(any(chunk["metadata"].get("problem_id") == "problem_001" for chunk in chunks))

    def test_exercise_ingest_repairs_absorbed_missing_problem_with_deepseek_client(self) -> None:
        class FakeStructureRepairClient:
            model = "deepseek-v4-flash"

            def judge_problem_boundary(self, payload: dict) -> dict:
                self.payload = payload
                return {
                    "decision": "split_previous_problem",
                    "target_problem_index": 2,
                    "start_line": 7,
                    "end_line": 8,
                    "confidence": 0.91,
                    "title": "(2) 已知线性方程组有解，求参数。",
                    "reason_codes": ["contaminated_marker_inside_previous_problem"],
                }

        source = self.base_dir / "exercise_repair.md"
        source.write_text(
            "# 真题\n\n"
            "## 填空题(本题共3小题)\n\n"
            "(1) 第一问\n"
            "正文一。\n"
            "污染(2) 已知线性方程组有解，求参数。\n"
            "参数条件继续。\n\n"
            "(3) 第三问\n"
            "正文三。\n",
            encoding="utf-8",
        )

        fake_client = FakeStructureRepairClient()
        with patch("materials.service.build_deepseek_structure_repair_client_from_env", return_value=fake_client):
            result = self.service.ingest_file(
                source,
                user_id="tester",
                subject="math",
                material_type="exercise",
                use_llm_cleanup=False,
                enable_vector_index=False,
            )

        self.assertIsNone(result.error)
        material_dir = MaterialStorage(self.base_dir).material_dir("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))
        manifest = json.loads((material_dir / "manifest.json").read_text(encoding="utf-8"))
        chunks = [
            json.loads(line)
            for line in (material_dir / "chunks" / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        self.assertEqual(manifest["metadata"]["exercise_structure"]["problem_count"], 3)
        self.assertEqual(manifest["metadata"]["exercise_structure_repair"]["applied_count"], 1)
        self.assertEqual(report["metrics"]["exercise_structure_repair"]["applied_count"], 1)
        self.assertTrue((material_dir / "parsed" / "exercise_structure_repair.json").exists())
        self.assertIn("problem_002", {chunk["metadata"].get("problem_id") for chunk in chunks})
        self.assertEqual(fake_client.payload["target_missing_index"], 2)

    def test_exercise_search_result_keeps_problem_metadata(self) -> None:
        source = self.base_dir / "exercise_search.md"
        source.write_text(
            "# 题集\n\n"
            "## 一、选择题\n\n"
            "### (1) 二项分布期望公式\n\n"
            "题干：求 E(X)。\n\n"
            "**答案：** np\n\n"
            "### (2) 泊松分布方差公式\n\n"
            "题干：求 D(X)。\n\n"
            "**答案：** lambda\n",
            encoding="utf-8",
        )
        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="exercise",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertIsNone(result.error)
        search_result = search_user_materials(
            "tester",
            "泊松分布方差公式",
            top_k=3,
            filters={"material_id": result.material_id},
        )

        self.assertGreaterEqual(len(search_result), 1)
        self.assertEqual(search_result[0].metadata.get("problem_id"), "problem_002")
        self.assertEqual(search_result[0].metadata.get("problem_index"), 2)

    def test_md_ingest_success(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.user_id, "tester")
        self.assertEqual(result.parse_status.value, "ready")
        material_dir = self.base_dir / "tester" / "other" / result.material_id
        self.assertTrue((material_dir / "manifest.json").exists())
        self.assertTrue((material_dir / "parsed" / "content.md").exists())
        self.assertTrue((material_dir / "chunks" / "chunks.jsonl").exists())
        self.assertTrue((material_dir / "index" / "search_index.json").exists())

    def test_ingest_stores_material_under_subject_directory(self) -> None:
        result = self.service.ingest_file(
            self.demo_md,
            user_id="tester",
            subject="math",
            material_type="lecture",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        subject_dir = self.base_dir / "tester" / "math" / result.material_id
        legacy_dir = self.base_dir / "tester" / result.material_id
        self.assertTrue(subject_dir.exists())
        self.assertFalse(legacy_dir.exists())
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.subject.value, "math")
        self.assertEqual(manifest.material_type.value, "lecture")

    def test_unknown_subject_uses_other_directory(self) -> None:
        ambiguous = self.base_dir / "ambiguous_upload.md"
        ambiguous.write_text("# 上传资料\n\n普通内容。", encoding="utf-8")

        result = self.service.ingest_file(
            ambiguous,
            user_id="tester",
            subject="unknown",
            material_type="unknown",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        material_dir = self.base_dir / "tester" / "other" / result.material_id
        self.assertTrue(material_dir.exists())
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.subject.value, "other")

    def test_auto_metadata_uses_qwen_profile_and_moves_to_subject_directory(self) -> None:
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_bundle_with_qwen",
            return_value=qwen_bundle_for_metadata("math", "exercise", confidence=0.93),
        ):
            result = self.service.ingest_file(
                self.demo_md,
                user_id="tester",
                subject="auto",
                material_type="auto",
                use_llm_cleanup=True,
                enable_vector_index=False,
            )

        self.assertEqual(result.error, None)
        material_dir = self.base_dir / "tester" / "math" / result.material_id
        self.assertTrue(material_dir.exists())
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.subject.value, "math")
        self.assertEqual(manifest.material_type.value, "exercise")
        self.assertEqual(manifest.metadata["metadata_profile"]["source"], "qwen")

    def test_metadata_conflict_blocks_upload_until_user_confirms(self) -> None:
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_bundle_with_qwen",
            return_value=qwen_bundle_for_metadata("math", "lecture", confidence=0.94),
        ):
            result = self.service.ingest_file(
                self.demo_md,
                user_id="tester",
                subject="politics",
                material_type="lecture",
                use_llm_cleanup=True,
                enable_vector_index=False,
            )

        self.assertEqual(result.error, "metadata_conflict")
        self.assertEqual(result.metadata["metadata_conflict"]["field"], "subject")
        self.assertEqual(result.metadata["metadata_conflict"]["selected"], "politics")
        self.assertEqual(result.metadata["metadata_conflict"]["detected"], "math")
        self.assertEqual(MaterialIngestionService(storage=MaterialStorage(self.base_dir)).list_materials("tester"), [])

    def test_metadata_conflict_retry_reuses_strategy_bundle_without_qwen(self) -> None:
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_bundle_with_qwen",
            return_value=qwen_bundle_for_metadata("math", "lecture", confidence=0.94),
        ):
            conflict = self.service.ingest_file(
                self.demo_md,
                user_id="tester",
                subject="politics",
                material_type="lecture",
                use_llm_cleanup=True,
                enable_vector_index=False,
            )

        self.assertEqual(conflict.error, "metadata_conflict")
        retry_overrides = conflict.metadata["metadata_retry_overrides"]

        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_bundle_with_qwen",
            side_effect=AssertionError("qwen should not be called on metadata retry"),
        ):
            result = self.service.ingest_file(
                self.demo_md,
                user_id="tester",
                subject="math",
                material_type="lecture",
                metadata={
                    "allow_metadata_mismatch": True,
                    "cleaning_strategy_override": retry_overrides["cleaning_strategy"],
                    "document_zones_override": retry_overrides["document_zones"],
                    "metadata_profile_override": retry_overrides["metadata_profile"],
                },
                use_llm_cleanup=True,
                enable_vector_index=False,
            )

        self.assertIsNone(result.error)
        self.assertEqual(result.parse_status.value, "ready")
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.subject.value, "math")
        self.assertEqual(manifest.material_type.value, "lecture")
        self.assertEqual(manifest.metadata["raw_markdown_cleaning"]["strategy_source"], "qwen")

    def test_metadata_conflict_can_continue_with_user_selection(self) -> None:
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_bundle_with_qwen",
            return_value=qwen_bundle_for_metadata("math", "lecture", confidence=0.94),
        ):
            result = self.service.ingest_file(
                self.demo_md,
                user_id="tester",
                subject="politics",
                material_type="lecture",
                metadata={"allow_metadata_mismatch": True},
                use_llm_cleanup=True,
                enable_vector_index=False,
            )

        self.assertEqual(result.error, None)
        material_dir = self.base_dir / "tester" / "politics" / result.material_id
        self.assertTrue(material_dir.exists())
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.subject.value, "politics")
        self.assertEqual(manifest.metadata["metadata_conflict"]["accepted_by_user"], True)

    def test_txt_ingest_success(self) -> None:
        result = self.service.ingest_file(self.demo_txt, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.parse_status.value, "ready")
        self.assertGreaterEqual(result.chunk_count, 1)

    def test_formula_cleanup_is_recorded_in_ingest_outputs(self) -> None:
        source = self.base_dir / "formula_obsidian.md"
        source.write_text(
            "# 公式测试\n\n"
            "步骤 $\\textcircled { 2 }$ 和 $\\operatorname* { l i m } _ { x  \\infty } \\mathbf { x }$。\n",
            encoding="utf-8",
        )

        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="lecture",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertEqual(result.parse_status.value, "ready")
        material_dir = self.base_dir / "tester" / "math" / result.material_id
        content = (material_dir / "parsed" / "content.md").read_text(encoding="utf-8")
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))

        self.assertIn("$②$", content)
        self.assertIn("\\lim _ { x \\to \\infty }", content)
        self.assertIn("\\mathbf{x}", content)
        self.assertIsNotNone(manifest)
        self.assertGreater(manifest.metadata["formula_cleaning"]["stats"]["changed_count"], 0)
        self.assertGreater(report["metrics"]["formula_cleaning"]["stats"]["changed_count"], 0)

    def test_formula_cleanup_can_be_disabled(self) -> None:
        source = self.base_dir / "formula_raw.md"
        source.write_text("# 公式原文\n\n保留 $\\textcircled { 2 }$。\n", encoding="utf-8")

        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="lecture",
            use_llm_cleanup=False,
            use_formula_cleanup=False,
            enable_vector_index=False,
        )

        self.assertEqual(result.parse_status.value, "ready")
        material_dir = self.base_dir / "tester" / "math" / result.material_id
        content = (material_dir / "parsed" / "content.md").read_text(encoding="utf-8")
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))

        self.assertIn("\\textcircled { 2 }", content)
        self.assertIsNotNone(manifest)
        self.assertFalse(manifest.metadata["formula_cleaning"]["enabled"])
        self.assertFalse(report["metrics"]["formula_cleaning"]["enabled"])

    def test_llm_formula_cleanup_report_is_recorded_when_requested_without_client(self) -> None:
        source = self.base_dir / "formula_llm_residual.md"
        source.write_text(
            "# Formula LLM\n\n"
            "Residual $x + \\kern - delimiterspace + y$ issue.\n",
            encoding="utf-8",
        )

        with patch("materials.service.build_qwen_formula_repair_client_from_env", return_value=None):
            result = self.service.ingest_file(
                source,
                user_id="tester",
                subject="math",
                material_type="lecture",
                metadata={"use_llm_formula_cleanup": True},
                use_llm_cleanup=False,
                enable_vector_index=False,
            )

        self.assertEqual(result.parse_status.value, "ready")
        material_dir = self.base_dir / "tester" / "math" / result.material_id
        content = (material_dir / "parsed" / "content.md").read_text(encoding="utf-8")
        manifest = MaterialStorage(self.base_dir).load_manifest("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))
        llm_report_path = material_dir / "parsed" / "llm_cleaning_report.json"

        self.assertIn("\\kern - delimiterspace", content)
        self.assertTrue(llm_report_path.exists())
        self.assertIsNotNone(manifest)
        self.assertTrue(manifest.metadata["llm_cleaning"]["requested"])
        self.assertEqual(manifest.metadata["llm_cleaning"]["report"]["formula_repair"]["candidate_count"], 1)
        self.assertEqual(report["metrics"]["llm_cleaning"]["report"]["formula_repair"]["candidate_count"], 1)

    def test_default_user_is_tester(self) -> None:
        result = self.service.ingest_file(self.demo_md, use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.user_id, "tester")
        self.assertTrue((self.base_dir / "tester" / "other" / result.material_id).exists())

    def test_search_finds_expected_content(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.parse_status.value, "ready")
        matches = search_user_materials("tester", "罗尔定理", storage=MaterialStorage(self.base_dir))
        self.assertTrue(matches)
        self.assertTrue(any("罗尔定理" in match.text for match in matches))

    def test_search_expands_adjacent_length_split_chunks(self) -> None:
        storage = MaterialStorage(self.base_dir)
        material_id = "mat_split"
        storage.create_material_dir("tester", material_id)
        chunks = [
            Chunk(
                chunk_id="part_1",
                material_id=material_id,
                user_id="tester",
                chunk_index=0,
                text=(
                    "### \u51fd\u6570\u6982\u5ff5\n\n"
                    "\u51fd\u6570\u6982\u5ff5\u662f\u63cf\u8ff0\u53d8\u91cf\u4e4b\u95f4\u5bf9\u5e94\u5173\u7cfb\u7684\u57fa\u672c\u6982\u5ff5\u3002\n\n"
                    "3. \u503c\u57df"
                ),
                section_title="\u51fd\u6570\u6982\u5ff5",
                heading_path=["\u51fd\u6570\u6982\u5ff5"],
                metadata={"split_reason": "length", "part_index": 1},
            ),
            Chunk(
                chunk_id="part_2",
                material_id=material_id,
                user_id="tester",
                chunk_index=1,
                text=(
                    "3. \u503c\u57df\n\n"
                    "\u503c\u57df\u662f\u51fd\u6570\u503c\u7684\u96c6\u5408\uff0c\u5e94\u4e0e\u5b9a\u4e49\u57df\u548c\u5bf9\u5e94\u5173\u7cfb\u4e00\u8d77\u7406\u89e3\u3002"
                ),
                section_title="\u51fd\u6570\u6982\u5ff5",
                heading_path=["\u51fd\u6570\u6982\u5ff5"],
                metadata={"split_reason": "length", "part_index": 2},
            ),
        ]
        manifest = MaterialManifest(
            material_id=material_id,
            user_id="tester",
            original_filename="split.md",
            file_ext=".md",
            mime_type="text/markdown",
            sha256="abc",
            parse_status=ParseStatus.READY,
            paths={
                "markdown": "parsed/content.md",
                "chunks": "chunks/chunks.jsonl",
                "search_index": "index/search_index.json",
            },
        )
        storage.save_chunks_jsonl("tester", material_id, chunks)
        storage.save_search_index("tester", material_id, build_search_index(chunks))
        storage.save_manifest("tester", material_id, manifest)

        matches = search_user_materials(
            "tester",
            "\u51fd\u6570\u6982\u5ff5",
            top_k=1,
            storage=storage,
            mode="keyword",
        )

        self.assertTrue(matches)
        self.assertIn("\u503c\u57df\u662f\u51fd\u6570\u503c\u7684\u96c6\u5408", matches[0].text)
        self.assertTrue(matches[0].metadata.get("context_expanded"))

    def test_delete_removes_current_user_material(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        material_dir = self.base_dir / "tester" / "other" / result.material_id
        payload = self.service.delete_material("tester", result.material_id)
        self.assertTrue(payload["deleted"])
        self.assertFalse(material_dir.exists())

    def test_delete_clears_vector_index_before_removing_material_files(self) -> None:
        result = self.service.ingest_file(self.demo_md, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        events: list[str] = []
        original_storage_delete = self.service.storage.delete_material

        def record_storage_delete(user_id: str, material_id: str) -> None:
            events.append("storage")
            original_storage_delete(user_id, material_id)

        def record_vector_delete(user_id: str, material_id: str, *, enabled: bool = True) -> VectorIndexResult:
            events.append("vector")
            return VectorIndexResult(status="ready", enabled=enabled)

        with patch.object(self.service.storage, "delete_material", side_effect=record_storage_delete), patch(
            "materials.service.delete_material_vector_index",
            side_effect=record_vector_delete,
        ):
            payload = self.service.delete_material("tester", result.material_id)

        self.assertTrue(payload["deleted"])
        self.assertEqual(events, ["vector", "storage"])

    def test_legacy_flat_material_directory_is_still_listed_and_deleted(self) -> None:
        storage = MaterialStorage(self.base_dir)
        material_id = "mat_legacy"
        legacy_dir = self.base_dir / "tester" / material_id
        legacy_dir.mkdir(parents=True)
        manifest = MaterialManifest(
            material_id=material_id,
            user_id="tester",
            original_filename="legacy.md",
            file_ext=".md",
            mime_type="text/markdown",
            sha256="abc",
            parse_status=ParseStatus.READY,
        )
        (legacy_dir / "manifest.json").write_text(json.dumps(manifest.to_dict(), ensure_ascii=False), encoding="utf-8")

        items = MaterialIngestionService(storage=storage).list_materials("tester")
        self.assertEqual([item["material_id"] for item in items], [material_id])

        MaterialIngestionService(storage=storage).delete_material("tester", material_id)
        self.assertFalse(legacy_dir.exists())

    def test_user_isolation(self) -> None:
        tester_result = self.service.ingest_file(self.demo_md, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        other_result = self.service.ingest_file(self.demo_txt, user_id="test_user_a", use_llm_cleanup=False, enable_vector_index=False)
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
        result = self.service.ingest_file(bad_file, user_id="tester", use_llm_cleanup=False, enable_vector_index=False)
        self.assertEqual(result.parse_status.value, "failed")
        self.assertIn("Unsupported file type", result.error or "")

    def test_api_search_accepts_llm_mode(self) -> None:
        with patch("materials.api.search_user_materials_tool", return_value=[]) as search_tool:
            response = self.client.get(
                "/api/materials/search",
                params={"query": "方差公式", "subject": "math", "mode": "llm"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mode"], "llm")
        self.assertEqual(search_tool.call_args.kwargs["mode"], "llm")

    def test_api_search_can_omit_subject_for_all_my_materials(self) -> None:
        with patch("materials.api.search_user_materials_tool", return_value=[]) as search_tool:
            response = self.client.get(
                "/api/materials/search",
                params={"query": "方差公式", "mode": "hybrid"},
            )

        self.assertEqual(response.status_code, 200)
        filters = search_tool.call_args.kwargs["filters"]
        self.assertTrue(filters is None or "subject" not in filters)

    def test_llm_search_mode_has_distinct_score_kind(self) -> None:
        self.assertEqual(_score_kind("llm"), "llm_rerank")

    def test_api_upload_list_search_delete(self) -> None:
        with self.demo_md.open("rb") as file:
            upload_response = self.client.post(
                "/api/materials/upload",
                files={"file": ("test.md", file, "text/markdown")},
                data={"subject": "math", "material_type": "lecture", "use_llm_cleanup": "false", "enable_vector_index": "false"},
            )
        self.assertEqual(upload_response.status_code, 200)
        upload_payload = upload_response.json()
        self.assertEqual(upload_payload["user_id"], "tester")
        material_id = upload_payload["material_id"]

        list_response = self.client.get("/api/materials/list", params={"subject": "math"})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.json()["items"][0]["material_id"], material_id)

        search_response = self.client.get("/api/materials/search", params={"query": "罗尔定理", "subject": "math"})
        self.assertEqual(search_response.status_code, 200)
        self.assertGreaterEqual(search_response.json()["total_results"], 1)

        delete_response = self.client.delete(f"/api/materials/{material_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertTrue(delete_response.json()["deleted"])

        list_after_delete = self.client.get("/api/materials/list", params={"subject": "math"})
        self.assertEqual(list_after_delete.status_code, 200)
        self.assertEqual(list_after_delete.json()["items"], [])


if __name__ == "__main__":
    unittest.main()
