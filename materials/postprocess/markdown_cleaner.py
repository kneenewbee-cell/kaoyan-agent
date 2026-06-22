"""
materials/postprocess/markdown_cleaner.py — Markdown 基础清洗。

职责：raw markdown → cleaner markdown 的第一层清洗。
原则：保守、可重复、不改写用户语义；保护代码块、公式块、表格、图片引用。
"""

from __future__ import annotations

import re
from pathlib import Path

CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
TRAILING_SPACE_RE = re.compile(r"[ \t]+$")


def normalize_newlines(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n")


def clean_markdown(content: str) -> str:
    """轻量清洗 Markdown。

    做：
    - 统一换行；
    - 去控制字符；
    - 去行尾空白；
    - 连续空行最多保留 2 个；
    - 保留代码块、公式块、图片、表格。
    """
    content = normalize_newlines(content)
    content = CONTROL_CHARS_RE.sub("", content)

    cleaned: list[str] = []
    blank_count = 0
    in_fenced_block = False
    fence_marker: str | None = None

    for raw_line in content.split("\n"):
        line = TRAILING_SPACE_RE.sub("", raw_line)
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fenced_block:
                in_fenced_block = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fenced_block = False
                fence_marker = None
            cleaned.append(line)
            blank_count = 0
            continue

        if in_fenced_block:
            cleaned.append(line)
            continue

        if stripped == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
            continue

        blank_count = 0
        cleaned.append(line)

    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return "\n".join(cleaned) + "\n"


def clean_markdown_file(input_path: Path, output_path: Path | None = None) -> str:
    content = input_path.read_text(encoding="utf-8")
    cleaned = clean_markdown(content)
    target = output_path or input_path
    target.write_text(cleaned, encoding="utf-8")
    return cleaned
