"""
materials/parsers/markdown_parser.py — Markdown 文件解析器。

MarkdownParser 的职责：
- 读取 .md 文件；
- 统一编码和换行；
- 提取基础 metadata；
- 输出 parsed/content.md 的“基础 Markdown”。

注意：
清洗整理、标题规范化、图片复制改写、质量评估不在 parser 中完成，统一交给 postprocess/quality。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def _read_text_with_fallback(path: Path) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    for encoding in ("utf-8-sig", "utf-8", "gbk", "cp936"):
        try:
            return path.read_text(encoding=encoding), encoding, warnings
        except UnicodeDecodeError:
            continue
    warnings.append("decode_fallback_replace")
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8-replace", warnings


def _extract_front_matter(markdown: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER_RE.match(markdown)
    if not match:
        return {}, markdown

    metadata: dict[str, str] = {}
    body = markdown[match.end():]
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"\'')
    return metadata, body


class MarkdownParser(BaseMaterialParser):
    parser_name = "markdown"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        if not input_path.exists():
            return ParseResult(status=ParseStatus.FAILED, error=f"输入文件不存在: {input_path}")

        try:
            content, encoding, warnings = _read_text_with_fallback(input_path)
            content = content.replace("\r\n", "\n").replace("\r", "\n")
            front_matter, body = _extract_front_matter(content)

            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "content.md"
            output_path.write_text(body, encoding="utf-8")

            headings = [m.group(2).strip() for m in HEADING_RE.finditer(body)]
            image_refs = [m.group(2) for m in IMAGE_RE.finditer(body)]
            metadata: dict[str, Any] = {
                "source_format": "markdown",
                "source_dir": str(input_path.parent),
                "original_filename": input_path.name,
                "encoding": encoding,
                "line_count": len(body.splitlines()),
                "char_count": len(body),
                "heading_count": len(headings),
                "image_ref_count": len(image_refs),
                "front_matter": front_matter,
            }
            if headings:
                metadata["first_heading"] = headings[0]

            return ParseResult(
                status=ParseStatus.READY,
                markdown_path=output_path,
                metadata=metadata,
                warnings=warnings,
            )
        except Exception as exc:
            return ParseResult(status=ParseStatus.FAILED, error=f"读取 Markdown 文件失败: {exc}")
