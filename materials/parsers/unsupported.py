"""
materials/parsers/unsupported.py — 不支持的格式处理。

对不支持的格式返回明确错误信息。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus
from ..detector import get_ext_description


class UnsupportedParser(BaseMaterialParser):
    """不支持格式的解析器，始终返回 FAILED。"""

    parser_name = "unsupported"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        ext = input_path.suffix.lower()
        return ParseResult(
            status=ParseStatus.FAILED,
            error=f"Unsupported file type: {ext} ({get_ext_description(ext)})",
        )
