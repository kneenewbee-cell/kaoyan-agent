"""
materials/parsers/text_parser.py — 纯文本文件解析器。

读取 .txt 文件，转为简单 Markdown 格式保存。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


class TextParser(BaseMaterialParser):
    """纯文本文件解析器。"""

    parser_name = "text"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """
        读取 .txt 文件，转成 Markdown 保存。

        策略：
        - 保留原始文本结构
        - 空行之间视为段落
        - 如果一行以 # 开头，保留为标题
        """
        if not input_path.exists():
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"输入文件不存在: {input_path}",
            )

        try:
            raw = input_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # 尝试常见中文编码
            try:
                raw = input_path.read_text(encoding="gbk")
            except Exception as e:
                return ParseResult(
                    status=ParseStatus.FAILED,
                    error=f"无法解码文本文件: {e}",
                )
        except Exception as e:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"读取文本文件失败: {e}",
            )

        # 基本 Markdown 转换
        lines = raw.splitlines()
        md_lines: list[str] = []

        for line in lines:
            stripped = line.rstrip()
            # 保留原有 Markdown 语法
            md_lines.append(stripped)

        md_content = "\n".join(md_lines)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "content.md"
        output_path.write_text(md_content, encoding="utf-8")

        return ParseResult(
            status=ParseStatus.READY,
            markdown_path=output_path,
            json_path=None,
            layout_path=None,
            metadata={
                "line_count": len(md_lines),
                "char_count": len(md_content),
                "original_filename": input_path.name,
            },
        )
