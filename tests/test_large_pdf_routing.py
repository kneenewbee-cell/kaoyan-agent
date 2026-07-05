from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from materials.large_pdf_chapters import (
    combine_chapter_markdown,
    extract_outline_chapter_segments,
    restore_large_pdf_chapter_headings,
    split_pdf_by_segments,
)
from materials.large_pdf_samples import build_sample_windows, create_large_pdf_samples
from materials.schemas import ParseResult, ParseStatus
from materials.service import MaterialIngestionService
from materials.storage import MaterialStorage


class _FakePdfParser:
    parser_name = "mineru"

    def parse(self, input_path: Path, output_dir: Path, context=None) -> ParseResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = output_dir / "content.md"
        raw_table = (
            "<table><tr><th>Topic</th><th>Math</th></tr>"
            "<tr><td>Rolle</td><td>required</td></tr></table>"
        )
        body = f"# Parsed {input_path.stem}\n\n罗尔定理\n"
        layout_path = None
        if input_path.name.startswith("chapter_"):
            body = f"# Parsed {input_path.stem}\n\n{raw_table}\n\n罗尔定理\n"
            layout_path = output_dir / "layout.json"
            layout_path.write_text(
                json.dumps(
                    {
                        "pdf_info": [
                            {
                                "preproc_blocks": [
                                    {
                                        "type": "table",
                                        "bbox": [0, 0, 100, 100],
                                        "blocks": [
                                            {
                                                "lines": [
                                                    {
                                                        "spans": [
                                                            {"type": "table", "html": raw_table}
                                                        ]
                                                    }
                                                ]
                                            }
                                        ],
                                    }
                                ]
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        markdown_path.write_text(body, encoding="utf-8")
        return ParseResult(
            status=ParseStatus.READY,
            markdown_path=markdown_path,
            layout_path=layout_path,
            metadata={"source_format": "pdf", "source_dir": str(output_dir)},
        )


class LargePdfRoutingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base_dir = Path(self.temp_dir.name)
        self.service = MaterialIngestionService(storage=MaterialStorage(self.base_dir / "materials"))

    def _write_blank_pdf(self, name: str, page_count: int) -> Path:
        from pypdf import PdfWriter

        path = self.base_dir / name
        writer = PdfWriter()
        for _ in range(page_count):
            writer.add_blank_page(width=595, height=842)
        with path.open("wb") as file:
            writer.write(file)
        return path

    def _write_outline_pdf(self, name: str, page_count: int) -> Path:
        from pypdf import PdfWriter

        path = self.base_dir / name
        writer = PdfWriter()
        for _ in range(page_count):
            writer.add_blank_page(width=595, height=842)
        writer.add_outline_item("封面", 0)
        first = writer.add_outline_item("第一章 函数", 2)
        writer.add_outline_item("第一节 函数概念", 3, parent=first)
        writer.add_outline_item("第二章 极限", 7)
        writer.add_outline_item("附录 真题", 10)
        with path.open("wb") as file:
            writer.write(file)
        return path

    def test_build_sample_windows_uses_front_middle_tail_for_large_pdf(self) -> None:
        windows = build_sample_windows(total_pages=296)

        self.assertEqual(
            [(window.name, window.start_pdf_index, window.end_pdf_index) for window in windows],
            [
                ("front", 0, 30),
                ("middle", 138, 158),
                ("tail", 276, 296),
            ],
        )

    def test_create_large_pdf_samples_writes_pdfs_and_page_mapping(self) -> None:
        source = self._write_blank_pdf("sample-source.pdf", page_count=12)
        sample_dir = self.base_dir / "samples"

        sample_pages_path = create_large_pdf_samples(
            source,
            sample_dir,
            front_pages=3,
            middle_pages=4,
            tail_pages=2,
        )

        self.assertEqual(sample_pages_path, sample_dir / "sample_pages.json")
        sample_pages = json.loads(sample_pages_path.read_text(encoding="utf-8"))
        self.assertEqual(sample_pages["total_pages"], 12)
        self.assertEqual(
            [(window["sample_name"], window["start_pdf_index"], window["end_pdf_index"]) for window in sample_pages["windows"]],
            [
                ("front", 0, 3),
                ("middle", 4, 8),
                ("tail", 10, 12),
            ],
        )
        self.assertTrue((sample_dir / "front.pdf").exists())
        self.assertTrue((sample_dir / "middle.pdf").exists())
        self.assertTrue((sample_dir / "tail.pdf").exists())

        physical_pages = [page["physical_page"] for page in sample_pages["pages"]]
        self.assertEqual(physical_pages, [1, 2, 3, 5, 6, 7, 8, 11, 12])

        from pypdf import PdfReader

        self.assertEqual(len(PdfReader(str(sample_dir / "front.pdf")).pages), 3)
        self.assertEqual(len(PdfReader(str(sample_dir / "middle.pdf")).pages), 4)
        self.assertEqual(len(PdfReader(str(sample_dir / "tail.pdf")).pages), 2)

    def test_extract_outline_chapter_segments_uses_top_level_chapters_only(self) -> None:
        source = self._write_outline_pdf("outline-source.pdf", page_count=12)

        segments = extract_outline_chapter_segments(source)

        self.assertEqual(
            [(segment.title, segment.start_pdf_index, segment.end_pdf_index) for segment in segments],
            [
                ("第一章 函数", 2, 7),
                ("第二章 极限", 7, 10),
                ("附录 真题", 10, 12),
            ],
        )

    def test_split_pdf_by_segments_writes_chapter_pdfs_and_plan(self) -> None:
        source = self._write_outline_pdf("split-source.pdf", page_count=12)
        segments = extract_outline_chapter_segments(source)
        chapter_dir = self.base_dir / "chapters"

        plan_path = split_pdf_by_segments(source, chapter_dir, segments)

        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertEqual(plan["source"], "pdf_outline")
        self.assertEqual(len(plan["chapters"]), 3)
        self.assertEqual(plan["chapters"][0]["start_physical_page"], 3)
        self.assertEqual(plan["chapters"][0]["end_physical_page"], 7)
        from pypdf import PdfReader

        self.assertEqual(len(PdfReader(str(chapter_dir / "chapter_001.pdf")).pages), 5)
        self.assertEqual(len(PdfReader(str(chapter_dir / "chapter_002.pdf")).pages), 3)
        self.assertEqual(len(PdfReader(str(chapter_dir / "chapter_003.pdf")).pages), 2)

    def test_combine_chapter_markdown_removes_leading_duplicate_chapter_heading(self) -> None:
        chapter_md = self.base_dir / "chapter.md"
        chapter_md.write_text("# 第一章 函数极限连续\n\n正文内容\n", encoding="utf-8")
        combined = self.base_dir / "parsed" / "content.md"

        combine_chapter_markdown(
            book_title="测试书",
            chapters=[
                {
                    "chapter_index": 1,
                    "title": "第一章 函数 极限 连续",
                    "start_physical_page": 1,
                    "end_physical_page": 10,
                    "markdown_path": chapter_md,
                    "source_dir": chapter_md.parent,
                }
            ],
            combined_markdown_path=combined,
        )

        text = combined.read_text(encoding="utf-8")
        self.assertEqual(text.count("第一章 函数 极限 连续"), 1)
        self.assertNotIn("第一章 函数极限连续", text)
        self.assertIn("正文内容", text)

    def test_restore_large_pdf_chapter_headings_promotes_marker_following_text(self) -> None:
        markdown = "\n".join(
            [
                "# 书名",
                "",
                "<!-- large_pdf_chapter index=10 physical_pages=284-296 -->",
                "附录 2024年考研数学——高等数学试题",
                "",
                "正文",
            ]
        )

        restored = restore_large_pdf_chapter_headings(markdown)

        self.assertIn("## 附录 2024年考研数学——高等数学试题", restored)

    def test_small_pdf_below_threshold_uses_existing_parser_path(self) -> None:
        source = self._write_blank_pdf("small.pdf", page_count=1)
        fake_parser = _FakePdfParser()

        with patch("materials.service.get_parser", return_value=fake_parser) as get_parser:
            result = self.service.ingest_file(
                source,
                user_id="tester",
                use_llm_cleanup=False,
                enable_vector_index=False,
                metadata={"pdf_mode": "auto", "large_pdf_threshold_mb": 1},
            )

        self.assertEqual(result.parse_status, ParseStatus.READY)
        get_parser.assert_called_once_with(".pdf")
        self.assertEqual(result.metadata.get("pdf_route_decision", {}).get("selected_route"), "current")
        self.assertTrue(Path(result.markdown_path or "").exists())

    def test_large_pdf_above_threshold_runs_split_pipeline_without_parsing_original_pdf(self) -> None:
        source = self._write_outline_pdf("large.pdf", page_count=12)
        parser = _FakePdfParser()

        with patch.object(parser, "parse", wraps=parser.parse) as parse_mock, patch("materials.service.get_parser", return_value=parser):
            result = self.service.ingest_file(
                source,
                user_id="tester",
                use_llm_cleanup=False,
                enable_vector_index=False,
                metadata={"pdf_mode": "auto", "large_pdf_page_threshold": 3},
            )

        self.assertEqual(result.parse_status, ParseStatus.READY)
        self.assertIsNone(result.error)
        parsed_inputs = [call.kwargs["input_path"].name for call in parse_mock.call_args_list]
        self.assertNotIn("large.pdf", parsed_inputs)
        self.assertIn("full.pdf", parsed_inputs)
        self.assertIn("chapter_001.pdf", parsed_inputs)

        material_dir = self.service.storage.material_dir("tester", result.material_id)
        plan_path = material_dir / "parsed" / "large_pdf_route_plan.json"
        sample_pages_path = material_dir / "parsed" / "large_pdf_samples" / "sample_pages.json"
        chapter_plan_path = material_dir / "parsed" / "large_pdf_chapters" / "chapter_plan.json"
        manifest_path = material_dir / "manifest.json"
        self.assertTrue(plan_path.exists())
        self.assertTrue(sample_pages_path.exists())
        self.assertTrue(chapter_plan_path.exists())
        self.assertTrue(manifest_path.exists())

        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertEqual(plan["route"], "large_pdf_split")
        self.assertEqual(plan["status"], "samples_and_chapters_ready")
        self.assertTrue(plan["small_pdf_path_unchanged"])

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["parse_status"], "ready")
        self.assertEqual(manifest["paths"]["large_pdf_route_plan"], "parsed/large_pdf_route_plan.json")
        self.assertEqual(manifest["paths"]["large_pdf_sample_pages"], "parsed/large_pdf_samples/sample_pages.json")
        self.assertEqual(manifest["paths"]["large_pdf_chapter_plan"], "parsed/large_pdf_chapters/chapter_plan.json")
        self.assertEqual(manifest["metadata"]["pdf_route_decision"]["selected_route"], "large_pdf_split")
        self.assertEqual(manifest["metadata"]["large_pdf_chapter_plan"]["chapter_count"], 3)
        markdown_text = Path(result.markdown_path or "").read_text(encoding="utf-8")
        self.assertIn("第一章 函数", markdown_text)
        self.assertNotIn("<table", markdown_text)
        self.assertIn("<!-- table: table_001 page=3 source=layout.json -->", markdown_text)
        self.assertIn("| Topic | Math |", markdown_text)
        self.assertEqual(manifest["metadata"]["large_pdf_table_sidecar"]["table_count"], 3)
        self.assertEqual(manifest["metadata"]["layout_sidecar"]["table_count"], 3)
        self.assertEqual(manifest["paths"]["layout_summary"], "parsed/layout_summary.json")
        self.assertEqual(manifest["paths"]["tables"], "parsed/tables")
        table_dir = material_dir / "parsed" / "tables"
        self.assertTrue((table_dir / "table_001.md").exists())
        chunks = [
            json.loads(line)
            for line in (material_dir / "chunks" / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertTrue(any(chunk.get("metadata", {}).get("source_type") == "table" for chunk in chunks))
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["metrics"]["layout_sidecar"]["table_count"], 3)

    def test_pdf_page_count_above_threshold_is_intercepted_even_when_size_is_small(self) -> None:
        source = self._write_blank_pdf("many-pages.pdf", page_count=3)
        parser = _FakePdfParser()

        with patch("materials.service.get_parser", return_value=parser):
            result = self.service.ingest_file(
                source,
                user_id="tester",
                use_llm_cleanup=False,
                enable_vector_index=False,
                metadata={
                    "pdf_mode": "auto",
                    "large_pdf_threshold_mb": 999,
                    "large_pdf_page_threshold": 3,
                },
            )

        self.assertEqual(result.parse_status, ParseStatus.READY)
        decision = result.metadata.get("pdf_route_decision", {})
        self.assertEqual(decision.get("selected_route"), "large_pdf_split")
        self.assertEqual(decision.get("reason"), "page_threshold")
        self.assertEqual(decision.get("page_count"), 3)
        self.assertEqual(decision.get("page_threshold"), 3)
        self.assertEqual(result.metadata.get("large_pdf_chapter_plan", {}).get("source"), "fixed_page_chunks")

    def test_pdf_mode_normal_forces_current_parser_even_above_threshold(self) -> None:
        source = self._write_blank_pdf("forced-normal.pdf", page_count=1)
        fake_parser = _FakePdfParser()

        with patch("materials.service.get_parser", return_value=fake_parser):
            result = self.service.ingest_file(
                source,
                user_id="tester",
                use_llm_cleanup=False,
                enable_vector_index=False,
                metadata={"pdf_mode": "normal", "large_pdf_threshold_mb": 0.0001},
            )

        self.assertEqual(result.parse_status, ParseStatus.READY)
        self.assertEqual(result.metadata.get("pdf_route_decision", {}).get("selected_route"), "current")
        self.assertEqual(result.metadata.get("pdf_route_decision", {}).get("reason"), "forced_normal")


if __name__ == "__main__":
    unittest.main()
