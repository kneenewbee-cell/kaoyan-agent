"""
materials/router.py — Parser 路由器。

根据文件扩展名选择对应的 parser。
"""

from __future__ import annotations

from pathlib import Path

from .parsers.base import BaseMaterialParser
from .parsers.markdown_parser import MarkdownParser
from .parsers.text_parser import TextParser
from .parsers.mineru_parser import MinerUParser
from .parsers.docx_parser import DocxParser
from .parsers.image_parser import ImageParser
from .parsers.unsupported import UnsupportedParser

# 扩展名 → Parser 类映射
ROUTING_TABLE: dict[str, type[BaseMaterialParser]] = {
    ".md": MarkdownParser,
    ".txt": TextParser,
    ".pdf": MinerUParser,
    ".docx": DocxParser,
    ".png": ImageParser,
    ".jpg": ImageParser,
    ".jpeg": ImageParser,
    ".webp": ImageParser,
}


def get_parser(ext: str) -> BaseMaterialParser:
    """
    根据文件扩展名返回对应的 parser 实例。

    参数
    ----
    ext : str
        文件扩展名，含点号（如 ".md"）。

    返回
    ----
    BaseMaterialParser : parser 实例。
    """
    ext = ext.lower()
    parser_cls = ROUTING_TABLE.get(ext)
    if parser_cls is None:
        return UnsupportedParser()
    return parser_cls()
