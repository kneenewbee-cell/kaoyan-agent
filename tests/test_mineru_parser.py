from __future__ import annotations

import subprocess
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from materials.parsers.mineru_parser import MinerUParser, _build_command


class MinerUParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.base_dir = Path(self.temp_dir.name)
        self.source_pdf = self.base_dir / "sample.pdf"
        self.source_pdf.write_bytes(b"%PDF-1.4 fake")
        self.output_dir = self.base_dir / "parsed"

    def test_disabled_returns_clear_error(self) -> None:
        with patch.dict("os.environ", {"MINERU_ENABLED": "0"}, clear=False):
            result = MinerUParser().parse(self.source_pdf, self.output_dir)
        self.assertEqual(result.status.value, "failed")
        self.assertIn("MinerU is disabled", result.error or "")

    def test_default_command_preserves_paths_with_spaces(self) -> None:
        input_path = self.base_dir / "a file with spaces.pdf"
        output_path = self.base_dir / "out dir"
        with patch.dict("os.environ", {}, clear=True):
            args, _ = _build_command(mineru_bin="mineru", input_path=input_path, output_dir=output_path)
        self.assertEqual(args, ["mineru", "-p", str(input_path), "-o", str(output_path), "-b", "pipeline"])

    def test_cli_output_copies_content_and_layout_to_parsed_root(self) -> None:
        def fake_run(args, **kwargs):
            raw_dir = Path(args[args.index("-o") + 1])
            raw_dir.mkdir(parents=True, exist_ok=True)
            (raw_dir / "full.md").write_text("# Chapter\n\nbody ![](images/a.png)\n", encoding="utf-8")
            (raw_dir / "layout.json").write_text('{"pdf_info":[]}', encoding="utf-8")
            (raw_dir / "abc_content_list.json").write_text("[]", encoding="utf-8")
            (raw_dir / "images").mkdir()
            (raw_dir / "images" / "a.png").write_bytes(b"fake")
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

        with patch.dict(
            "os.environ",
            {
                "MINERU_ENABLED": "1",
                "MINERU_BACKEND": "cli",
                "MINERU_BIN": "mineru",
                "MINERU_COMMAND_TEMPLATE": "{bin} -p {input} -o {output} -b pipeline",
            },
            clear=False,
        ), patch("materials.parsers.mineru_parser.subprocess.run", side_effect=fake_run):
            result = MinerUParser().parse(self.source_pdf, self.output_dir)

        self.assertEqual(result.status.value, "ready")
        self.assertEqual(result.markdown_path, self.output_dir / "content.md")
        self.assertEqual(result.layout_path, self.output_dir / "layout.json")
        self.assertTrue((self.output_dir / "content.md").exists())
        self.assertTrue((self.output_dir / "layout.json").exists())
        self.assertTrue((self.output_dir / "mineru_raw" / "full.md").exists())
        self.assertTrue((self.output_dir / "mineru_raw" / "layout.json").exists())
        self.assertTrue((self.output_dir / "mineru_raw" / "mineru_stdout.txt").exists())
        self.assertTrue((self.output_dir / "mineru_raw" / "mineru_command.json").exists())
        self.assertEqual(result.metadata["source_format"], "pdf")
        self.assertEqual(result.metadata["parser_backend"], "mineru_cli")
        self.assertEqual(result.metadata["source_dir"], str(self.output_dir / "mineru_raw"))
        self.assertEqual(result.metadata["image_ref_count"], 1)
        self.assertEqual(result.warnings, [])

    def test_cli_nested_output_uses_markdown_parent_as_source_dir(self) -> None:
        def fake_run(args, **kwargs):
            raw_dir = Path(args[args.index("-o") + 1])
            nested = raw_dir / "sample.pdf-id"
            nested.mkdir(parents=True, exist_ok=True)
            (nested / "full.md").write_text("# Nested\n", encoding="utf-8")
            (nested / "layout.json").write_text('{"pdf_info":[]}', encoding="utf-8")
            (nested / "images").mkdir()
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")

        with patch.dict(
            "os.environ",
            {
                "MINERU_ENABLED": "1",
                "MINERU_BACKEND": "cli",
                "MINERU_COMMAND_TEMPLATE": "{bin} -p {input} -o {output} -b pipeline",
            },
            clear=False,
        ), patch("materials.parsers.mineru_parser.subprocess.run", side_effect=fake_run):
            result = MinerUParser().parse(self.source_pdf, self.output_dir)

        self.assertEqual(result.status.value, "ready")
        self.assertEqual(result.metadata["source_dir"], str(self.output_dir / "mineru_raw" / "sample.pdf-id"))
        self.assertEqual((self.output_dir / "content.md").read_text(encoding="utf-8"), "# Nested\n")

    def test_cli_missing_markdown_fails(self) -> None:
        def fake_run(args, **kwargs):
            Path(args[args.index("-o") + 1]).mkdir(parents=True, exist_ok=True)
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")

        with patch.dict(
            "os.environ",
            {
                "MINERU_ENABLED": "1",
                "MINERU_BACKEND": "cli",
                "MINERU_COMMAND_TEMPLATE": "{bin} -p {input} -o {output} -b pipeline",
            },
            clear=False,
        ), patch("materials.parsers.mineru_parser.subprocess.run", side_effect=fake_run):
            result = MinerUParser().parse(self.source_pdf, self.output_dir)

        self.assertEqual(result.status.value, "failed")
        self.assertIn("did not produce full.md", result.error or "")

    def test_cloud_output_downloads_zip_and_materializes_content(self) -> None:
        calls: list[tuple[str, str]] = []

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as archive:
            archive.writestr("cloud/full.md", "# Cloud\n\nbody ![](images/a.jpg)\n")
            archive.writestr("cloud/abc_content_list.json", "[]")
            archive.writestr("cloud/images/a.jpg", b"fake")
        zip_bytes = zip_buffer.getvalue()

        def fake_json_request(method, url, **kwargs):
            calls.append((method, url))
            if method == "POST":
                headers = kwargs["headers"]
                self.assertEqual(headers["Authorization"], "Bearer test-token")
                return {"code": 0, "data": {"batch_id": "batch-1", "file_urls": ["https://upload.example/pdf"]}}
            if method == "GET":
                return {
                    "code": 0,
                    "data": {
                        "extract_result": [
                            {
                                "state": "done",
                                "extract_progress": {"total": 1, "done": 1},
                                "full_zip_url": "https://download.example/result.zip",
                            }
                        ]
                    },
                }
            raise AssertionError(method)

        def fake_put_file(upload_url, input_path, **kwargs):
            self.assertEqual(upload_url, "https://upload.example/pdf")
            self.assertEqual(input_path, self.source_pdf)
            return 200

        def fake_download(url, **kwargs):
            self.assertEqual(url, "https://download.example/result.zip")
            return zip_bytes

        with patch.dict(
            "os.environ",
            {
                "MINERU_ENABLED": "1",
                "MINERU_BACKEND": "cloud",
                "MINERU_API_TOKEN": "test-token",
                "MINERU_API_BASE_URL": "https://mineru.example",
                "MINERU_CLOUD_POLL_INTERVAL_SECONDS": "0.01",
            },
            clear=False,
        ), patch("materials.parsers.mineru_parser._json_http_request", side_effect=fake_json_request), patch(
            "materials.parsers.mineru_parser._put_file", side_effect=fake_put_file
        ), patch("materials.parsers.mineru_parser._download_bytes", side_effect=fake_download):
            result = MinerUParser().parse(self.source_pdf, self.output_dir)

        self.assertEqual(result.status.value, "ready")
        self.assertEqual(result.markdown_path, self.output_dir / "content.md")
        self.assertEqual((self.output_dir / "content.md").read_text(encoding="utf-8"), "# Cloud\n\nbody ![](images/a.jpg)\n")
        self.assertEqual(result.metadata["parser_backend"], "mineru_cloud")
        self.assertEqual(result.metadata["mineru_batch_id"], "batch-1")
        request_record = (self.output_dir / "mineru_raw" / "mineru_cloud_request.json").read_text(encoding="utf-8")
        self.assertIn("<redacted>", request_record)
        self.assertNotIn("test-token", request_record)
        self.assertIn(("POST", "https://mineru.example/api/v4/file-urls/batch"), calls)
        self.assertIn(("GET", "https://mineru.example/api/v4/extract-results/batch/batch-1"), calls)


if __name__ == "__main__":
    unittest.main()
