"""
materials/chunking/section_splitter.py — 按 Markdown 标题切分。

将 Markdown 内容按标题（#、##、### 等）拆分为 section。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# 匹配 Markdown ATX 标题行
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


@dataclass
class Section:
    """Markdown 的一个段落/章节。"""
    title: str | None = None          # 最近的标题文本
    level: int = 0                     # 标题级别 (1-6)，0 表示无标题
    heading_path: list[str] = field(default_factory=list)  # 标题路径
    content: str = ""                  # 该 section 的完整文本
    start_line: int = 0
    end_line: int = 0


def split_by_headings(markdown: str) -> list[Section]:
    """
    将 Markdown 按标题拆分为 section 列表。

    策略：
    1. 找到所有标题行。
    2. 每个标题后的内容归属于该标题的 section。
    3. 第一个标题之前的内容作为 preamble（level=0）。
    4. 维护 heading_path 以追踪父标题。
    """
    lines = markdown.splitlines()
    if not lines:
        return []

    # 找到所有标题行的位置和详情
    heading_positions: list[tuple[int, int, str]] = []  # (line_no, level, title)
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.strip())
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            heading_positions.append((i, level, title))

    if not heading_positions:
        # 没有标题，全文作为一个 section
        return [
            Section(
                title=None, level=0, heading_path=[],
                content=markdown, start_line=0, end_line=len(lines) - 1,
            )
        ]

    sections: list[Section] = []

    # 处理第一个标题之前的内容
    first_h_pos = heading_positions[0][0]
    if first_h_pos > 0:
        preamble_text = "\n".join(lines[:first_h_pos]).strip()
        if preamble_text:
            sections.append(Section(
                title=None, level=0, heading_path=[],
                content=preamble_text, start_line=0, end_line=first_h_pos - 1,
            ))

    # 维护标题路径栈
    heading_stack: list[tuple[int, str]] = []  # [(level, title), ...]

    for idx, (line_no, level, title) in enumerate(heading_positions):
        # 弹出不小于当前标题级别的栈元素
        while heading_stack and heading_stack[-1][0] >= level:
            heading_stack.pop()
        heading_stack.append((level, title))
        heading_path = [t for _, t in heading_stack]

        # 确定内容结束行
        if idx + 1 < len(heading_positions):
            end_line = heading_positions[idx + 1][0] - 1
        else:
            end_line = len(lines) - 1

        # 内容从当前标题行开始到下一个标题行之前
        content_lines = lines[line_no:end_line + 1]
        content = "\n".join(content_lines).strip()

        if content:
            sections.append(Section(
                title=title, level=level, heading_path=heading_path,
                content=content, start_line=line_no, end_line=end_line,
            ))

    return sections
