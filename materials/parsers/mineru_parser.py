"""MinerU parser backend for PDF/image materials.

The parser keeps MinerU's raw output under ``parsed/mineru_raw`` and exposes
stable project entry points at ``parsed/content.md`` and ``parsed/layout.json``.
Downstream cleaning/chunking code should only depend on those stable paths.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


DEFAULT_TIMEOUT_SECONDS = 900
DEFAULT_COMMAND_TEMPLATE = "{bin} -p {input} -o {output} -b pipeline"
IMAGE_RE = re.compile(r'!\[[^\]]*]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _safe_read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gbk", "cp936"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _find_first(root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(path for path in root.rglob(pattern) if path.is_file())
        if matches:
            return matches[0]
    return None


def _find_full_markdown(raw_dir: Path) -> Path | None:
    full_md = _find_first(raw_dir, ["full.md"])
    if full_md:
        return full_md
    return _find_first(raw_dir, ["*.md"])


def _find_layout_json(markdown_path: Path, raw_dir: Path) -> Path | None:
    nearby = markdown_path.parent / "layout.json"
    if nearby.exists() and nearby.is_file():
        return nearby
    return _find_first(raw_dir, ["layout.json"])


def _find_content_list_json(markdown_path: Path, raw_dir: Path) -> Path | None:
    patterns = ["*_content_list.json", "content_list.json", "*_content_list_v2.json"]
    for base in (markdown_path.parent, raw_dir):
        result = _find_first(base, patterns)
        if result:
            return result
    return None


def _build_command(*, mineru_bin: str, input_path: Path, output_dir: Path) -> tuple[list[str], str]:
    template = os.environ.get("MINERU_COMMAND_TEMPLATE")
    if not template:
        args = [mineru_bin, "-p", str(input_path), "-o", str(output_dir), "-b", "pipeline"]
        return args, " ".join(subprocess.list2cmdline([arg]) for arg in args)

    command_text = template.format(
        bin=mineru_bin,
        input=str(input_path),
        output=str(output_dir),
    )
    args = shlex.split(command_text, posix=os.name != "nt")
    args = [arg[1:-1] if len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in {"'", '"'} else arg for arg in args]
    return args, command_text


class MinerUParser(BaseMaterialParser):
    """Parse PDFs/images with a locally installed MinerU CLI."""

    parser_name = "mineru"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        if not input_path.exists():
            return ParseResult(status=ParseStatus.FAILED, error=f"Input file does not exist: {input_path}")

        if not _env_flag("MINERU_ENABLED"):
            return ParseResult(
                status=ParseStatus.FAILED,
                error=(
                    "MinerU is disabled. Set MINERU_ENABLED=1 and configure MINERU_BIN "
                    "or MINERU_COMMAND_TEMPLATE to enable PDF parsing."
                ),
            )

        backend = os.environ.get("MINERU_BACKEND", "cli").strip().lower()
        if backend != "cli":
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"Unsupported MinerU backend '{backend}'. Only MINERU_BACKEND=cli is implemented.",
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "mineru_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        mineru_bin = os.environ.get("MINERU_BIN", "mineru")
        timeout_seconds = int(os.environ.get("MINERU_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))
        args, command_text = _build_command(mineru_bin=mineru_bin, input_path=input_path, output_dir=raw_dir)

        command_record = {
            "backend": "cli",
            "command": command_text,
            "args": args,
            "input_path": str(input_path),
            "output_dir": str(raw_dir),
            "timeout_seconds": timeout_seconds,
            "started_at": time.time(),
        }
        (raw_dir / "mineru_command.json").write_text(
            json.dumps(command_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        try:
            completed = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except FileNotFoundError:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU binary '{mineru_bin}' not found. Configure MINERU_BIN or MINERU_COMMAND_TEMPLATE.",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )
        except subprocess.TimeoutExpired as exc:
            (raw_dir / "mineru_stdout.txt").write_text(exc.stdout or "", encoding="utf-8", errors="replace")
            (raw_dir / "mineru_stderr.txt").write_text(exc.stderr or "", encoding="utf-8", errors="replace")
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU parsing timed out after {timeout_seconds}s.",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )
        except Exception as exc:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU invocation failed: {exc}",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )

        (raw_dir / "mineru_stdout.txt").write_text(completed.stdout or "", encoding="utf-8", errors="replace")
        (raw_dir / "mineru_stderr.txt").write_text(completed.stderr or "", encoding="utf-8", errors="replace")

        if completed.returncode != 0:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU parsing failed with exit code {completed.returncode}.",
                metadata={
                    "parser_backend": "mineru_cli",
                    "mineru_raw_dir": str(raw_dir),
                    "mineru_exit_code": completed.returncode,
                },
            )

        markdown_source = _find_full_markdown(raw_dir)
        if markdown_source is None:
            return ParseResult(
                status=ParseStatus.FAILED,
                error="MinerU did not produce full.md or any Markdown output.",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )

        markdown_text = _safe_read_text(markdown_source).replace("\r\n", "\n").replace("\r", "\n")
        content_path = output_dir / "content.md"
        content_path.write_text(markdown_text, encoding="utf-8")

        layout_source = _find_layout_json(markdown_source, raw_dir)
        layout_path: Path | None = None
        if layout_source is not None:
            layout_path = output_dir / "layout.json"
            shutil.copy2(layout_source, layout_path)

        content_list_path = _find_content_list_json(markdown_source, raw_dir)
        image_refs = [match.group(1) for match in IMAGE_RE.finditer(markdown_text)]
        source_dir = markdown_source.parent

        metadata: dict[str, Any] = {
            "source_format": "pdf",
            "parser_backend": "mineru_cli",
            "source_dir": str(source_dir),
            "mineru_raw_dir": str(raw_dir),
            "mineru_markdown_source": str(markdown_source),
            "mineru_layout_source": str(layout_source) if layout_source else None,
            "mineru_exit_code": completed.returncode,
            "line_count": len(markdown_text.splitlines()),
            "char_count": len(markdown_text),
            "image_ref_count": len(image_refs),
            "layout_available": layout_path is not None,
            "content_list_available": content_list_path is not None,
            "original_filename": input_path.name,
        }

        warnings: list[str] = []
        if layout_path is None:
            warnings.append("mineru_layout_json_missing")
        if content_list_path is None:
            warnings.append("mineru_content_list_json_missing")

        return ParseResult(
            status=ParseStatus.READY,
            markdown_path=content_path,
            json_path=content_list_path,
            layout_path=layout_path,
            metadata=metadata,
            warnings=warnings,
        )
