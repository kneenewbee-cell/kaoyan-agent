"""
materials/parsers/image_parser.py — 图片文件解析器。

MVP 阶段占位，返回明确 NotImplemented。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


class ImageParser(BaseMaterialParser):
    """图片解析器 — 当前阶段占位。"""

    parser_name = "image"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """返回图片解析暂不支持的明确信息。"""
        return ParseResult(
            status=ParseStatus.FAILED,
            error=(
                f"Image parsing is not implemented yet. "
                f"File: {input_path.name}. "
                f"Images can be parsed via MinerU when MINERU_ENABLED=1."
            ),
        )
