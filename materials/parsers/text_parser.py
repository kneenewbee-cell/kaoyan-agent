"""
materials/parsers/text_parser.py — 纯文本文件解析器。

TextParser 的职责：
- 读取 .txt；
- 统一编码和换行；
- 将纯文本轻量转换为 Markdown；
- 输出 parsed/content.md 的“基础 Markdown”。

后续的清洗、结构规范化、质量报告和切块交给 postprocess/quality/chunking。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus

def _read_text_with_fallback(path: Path) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    for encoding in ("utf-8-sig", "utf-8", "gbk", "cp936"):
        try:
            return path.read_text(encoding=encoding), encoding, warnings
        except UnicodeDecodeError:
            continue
    warnings.append("decode_fallback_replace")
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8-replace", warnings


def text_to_markdown(raw: str, fallback_title: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]

    md_lines: list[str] = []
    fallback_title = fallback_title.strip() or "未命名资料"

    # 原文已有显式 H1/Setext H1 时尊重原文，否则仅补文件名根标题。
    first_nonblank = next((i for i, line in enumerate(lines) if line.strip()), None)
    has_source_h1 = bool(
        first_nonblank is not None
        and (
            lines[first_nonblank].lstrip().startswith("# ")
            or (
                first_nonblank + 1 < len(lines)
                and lines[first_nonblank + 1].strip().startswith("=")
            )
        )
    )
    if not has_source_h1:
        md_lines.extend([f"# {fallback_title}", ""])

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if md_lines and md_lines[-1] != "":
                md_lines.append("")
            continue

        md_lines.append(stripped)

    while md_lines and md_lines[-1] == "":
        md_lines.pop()

    warnings.append("txt_structure_deferred_to_postprocess")
    return "\n".join(md_lines) + "\n", warnings


class TextParser(BaseMaterialParser):
    parser_name = "text"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        if not input_path.exists():
            return ParseResult(status=ParseStatus.FAILED, error=f"输入文件不存在: {input_path}")

        try:
            raw, encoding, warnings = _read_text_with_fallback(input_path)
            markdown, structure_warnings = text_to_markdown(raw, input_path.stem)
            warnings.extend(structure_warnings)

            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "content.md"
            output_path.write_text(markdown, encoding="utf-8")

            return ParseResult(
                status=ParseStatus.READY,
                markdown_path=output_path,
                metadata={
                    "source_format": "text",
                    "source_dir": str(input_path.parent),
                    "original_filename": input_path.name,
                    "encoding": encoding,
                    "line_count": len(markdown.splitlines()),
                    "char_count": len(markdown),
                    "generated_root_title": input_path.stem,
                },
                warnings=warnings,
            )
        except Exception as exc:
            return ParseResult(status=ParseStatus.FAILED, error=f"读取文本文件失败: {exc}")
