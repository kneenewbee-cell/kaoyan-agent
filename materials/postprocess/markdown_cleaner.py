"""
materials/postprocess/markdown_cleaner.py — Markdown 后处理清洗。

清理多余空行、轻量噪声，不破坏公式和图片引用。
"""

from __future__ import annotations

import re
from pathlib import Path


def clean_markdown(content: str) -> str:
    """
    对 Markdown 内容做轻量清洗。

    规则：
    1. 合并连续多个空行为最多两个空行。
    2. 去除行首行尾空白。
    3. 不删除图片引用 ![...](...)。
    4. 不破坏数学公式 $$...$$ / $...$。
    5. 不删除表格。
    6. 不强行改写任何结构。

    参数
    ----
    content : str
        原始 Markdown 字符串。

    返回
    ----
    str : 清洗后的 Markdown。
    """
    lines = content.splitlines()
    cleaned: list[str] = []
    blank_count = 0

    for line in lines:
        stripped = line.rstrip()

        if stripped == "":
            blank_count += 1
            # 最多保留 2 个连续空行
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(stripped)

    # 去掉末尾多余空行
    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return "\n".join(cleaned)


def clean_markdown_file(input_path: Path, output_path: Path | None = None) -> str:
    """
    读取 Markdown 文件并清洗后保存。

    参数
    ----
    input_path : Path
        输入 Markdown 文件路径。
    output_path : Path | None
        输出路径，为 None 则覆盖原文件。

    返回
    ----
    str : 清洗后的 Markdown 内容。
    """
    content = input_path.read_text(encoding="utf-8")
    cleaned = clean_markdown(content)

    target = output_path or input_path
    target.write_text(cleaned, encoding="utf-8")

    return cleaned
