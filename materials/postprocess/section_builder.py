"""将 Markdown 建模为 block，并按受控强标记构建主 section。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .marker_parser import parse_marker_for_rule

ATX_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SETEXT_RE = re.compile(r"^\s*(=+|-+)\s*$")


@dataclass
class Block:
    type: str
    text: str
    start_line: int
    end_line: int


@dataclass
class Section:
    title: str
    level: int
    blocks: list[str] = field(default_factory=list)
    heading_path: list[str] = field(default_factory=list)


def blockize(raw_markdown: str) -> list[Block]:
    lines = raw_markdown.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    blocks: list[Block] = []
    paragraph: list[str] = []
    paragraph_start = 0

    def flush(end_line: int) -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block("paragraph", "\n".join(paragraph), paragraph_start, end_line))
            paragraph = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            flush(i - 1)
            marker = stripped[:3]
            start = i
            code = [line.rstrip()]
            i += 1
            while i < len(lines):
                code.append(lines[i].rstrip())
                if lines[i].strip().startswith(marker):
                    break
                i += 1
            blocks.append(Block("code", "\n".join(code), start, min(i, len(lines) - 1)))
            i += 1
            continue

        atx = ATX_RE.match(stripped)
        if atx:
            flush(i - 1)
            blocks.append(Block(f"atx_heading_{len(atx.group(1))}", atx.group(2).strip(), i, i))
            i += 1
            continue

        if stripped and i + 1 < len(lines) and SETEXT_RE.match(lines[i + 1]):
            flush(i - 1)
            underline = lines[i + 1].strip()
            level = 1 if underline.startswith("=") else 2
            blocks.append(Block(f"setext_heading_{level}", stripped, i, i + 1))
            i += 2
            continue

        if not stripped:
            flush(i - 1)
        else:
            if not paragraph:
                paragraph_start = i
            paragraph.append(line.rstrip())
        i += 1
    flush(len(lines) - 1)
    return blocks


def _filtered_text(text: str, ignored: list[str]) -> str:
    return "\n".join(line for line in text.splitlines() if line.strip() not in ignored).strip()


def build_sections(blocks: list[Block], strategy: dict) -> tuple[list[Section], list[str]]:
    warnings: list[str] = []
    main_rule = strategy["main_section_rule"]
    target_level = int(main_rule.get("target_level", 2))
    ignored = list(strategy.get("ignore_line_patterns", []))
    short_mode = strategy.get("plain_short_line_policy", {}).get("mode", "attach_to_current_section")
    sections: list[Section] = []
    doc_title: str | None = None
    current: Section | None = None
    marker_count = sum(
        bool(parse_marker_for_rule(block.text.splitlines()[0].rstrip(), main_rule))
        for block in blocks
        if block.type == "paragraph" and block.text.strip()
    )
    min_repeats = max(1, int(main_rule.get("min_repeats", 1)))
    markers_are_confident = marker_count >= min_repeats
    if marker_count and not markers_are_confident:
        warnings.append("main_section_markers_below_min_repeats_preserved")

    def intro_or_current() -> Section:
        nonlocal current
        if current is None:
            current = Section("", 0, heading_path=[doc_title] if doc_title else [])
            sections.append(current)
        return current

    for block in blocks:
        text = _filtered_text(block.text, ignored)
        if not text:
            continue
        if block.type in {"setext_heading_1", "atx_heading_1"}:
            if doc_title is None:
                doc_title = text
                sections.append(Section(text, 1, heading_path=[text]))
                current = sections[-1]
            elif text != doc_title:
                intro_or_current().blocks.append(f"# {text}")
            continue

        first, *remaining = text.splitlines()
        marker = (
            parse_marker_for_rule(first.rstrip(), main_rule)
            if block.type == "paragraph" and markers_are_confident
            else None
        )
        explicit_level: int | None = None
        if block.type.startswith(("atx_heading_", "setext_heading_")):
            explicit_level = int(block.type.rsplit("_", 1)[1])

        if marker or explicit_level == target_level:
            title = marker.title if marker else text
            path = ([doc_title] if doc_title else []) + [title]
            current = Section(title, target_level, heading_path=path)
            sections.append(current)
            if marker and remaining:
                current.blocks.append("\n".join(remaining).strip())
            continue

        if explicit_level is not None:
            intro_or_current().blocks.append(f"{'#' * explicit_level} {text}")
            continue

        if short_mode == "ignore" and len(text.splitlines()) == 1:
            continue
        if short_mode == "promote_to_subheading" and len(text.splitlines()) == 1:
            intro_or_current().blocks.append(f"{'#' * min(target_level + 1, 6)} {text}")
        else:
            intro_or_current().blocks.append(text)

    if not any(section.level == target_level for section in sections):
        warnings.append("no_main_section_marker_detected")
    return sections, warnings


def render_sections(sections: list[Section], doc_title: str | None = None) -> str:
    rendered: list[str] = []
    if doc_title and not any(section.level == 1 for section in sections):
        rendered.append(f"# {doc_title}")
    for section in sections:
        if section.level > 0 and section.title:
            rendered.append(f"{'#' * section.level} {section.title}")
        rendered.extend(block for block in section.blocks if block.strip())
    return "\n\n".join(rendered).strip() + "\n"
