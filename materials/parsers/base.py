"""
materials/parsers/base.py — Parser 抽象基类。

所有 parser 必须继承 BaseMaterialParser 并实现 parse()。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..schemas import ParseResult, ParsedAsset


class BaseMaterialParser(ABC):
    """资料解析器抽象基类。"""

    parser_name: str = "base"

    @abstractmethod
    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """
        解析资料文件。

        参数
        ----
        input_path : Path
            输入文件路径。
        output_dir : Path
            输出目录（通常为该 material 的 parsed/ 目录）。
        context : dict | None
            额外上下文（user_id、material_id 等）。

        返回
        ----
        ParseResult : 解析结果。
        """
        ...

    def _make_asset(
        self,
        filename: str,
        relative_path: str,
        asset_type: str = "unknown",
        page_no: int | None = None,
        description: str | None = None,
    ) -> ParsedAsset:
        """快捷创建 ParsedAsset。"""
        return ParsedAsset(
            filename=filename,
            relative_path=relative_path,
            asset_type=asset_type,
            page_no=page_no,
            description=description,
        )
