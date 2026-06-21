"""
materials/parsers/markdown_parser.py — Markdown 文件解析器。

读取 .md 文件，复制内容到 parsed/content.md，保留图片引用。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


class MarkdownParser(BaseMaterialParser):
    """Markdown 文件解析器。"""

    parser_name = "markdown"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """
        读取 .md 文件，输出 parsed/content.md。

        保留原始图片引用，不做额外处理。
        """
        if not input_path.exists():
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"输入文件不存在: {input_path}",
            )

        try:
            content = input_path.read_text(encoding="utf-8")
        except Exception as e:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"读取 Markdown 文件失败: {e}",
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "content.md"
        output_path.write_text(content, encoding="utf-8")

        return ParseResult(
            status=ParseStatus.READY,
            markdown_path=output_path,
            json_path=None,
            layout_path=None,
            metadata={
                "line_count": len(content.splitlines()),
                "char_count": len(content),
                "original_filename": input_path.name,
            },
        )
