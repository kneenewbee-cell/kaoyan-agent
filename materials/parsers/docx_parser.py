"""
materials/parsers/docx_parser.py — DOCX 文件解析器。

MVP 阶段占位，返回明确 NotImplemented。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


class DocxParser(BaseMaterialParser):
    """DOCX 解析器 — 当前阶段占位。"""

    parser_name = "docx"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """返回 DOCX 暂不支持的明确信息。"""
        return ParseResult(
            status=ParseStatus.FAILED,
            error=(
                f"DOCX parsing is not implemented yet. "
                f"File: {input_path.name}. "
                f"Please convert to Markdown or PDF first."
            ),
        )
