from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from ..postprocess.structure_strategy import validate_structure_strategy
from ..schemas import Chunk
from .token_counter import estimate_tokens

MAX_CHUNK_TOKENS = 1024
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
FORMULA_BOUNDARY_RE = re.compile(r"^\s*(\$\$|\\\[|\\\])\s*$")


@dataclass
class _MainSection:
    title: str | None
    heading_path: list[str]
    content: str
    start_line: int
    end_line: int


def _extract_asset_paths_from_text(text: str) -> list[str]:
    return [match.group(2) for match in IMAGE_RE.finditer(text)]


def _make_chunk_id(material_id: str, chunk_index: int) -> str:
    return hashlib.sha256(f"{material_id}:{chunk_index}".encode("utf-8")).hexdigest()[:16]


def _split_main_sections(markdown: str, main_level: int) -> list[_MainSection]:
    """只在 H1 和策略指定的主层级处分段；H3 等显式子标题留在主块内。"""
    lines = markdown.splitlines()
    doc_title: str | None = None
    starts: list[tuple[int, str | None, list[str]]] = []
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        fence_match = FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_code:
                in_code = True
                fence_marker = marker
            elif fence_marker == marker:
                in_code = False
                fence_marker = None
            continue
        if in_code:
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if in_formula:
            continue

        match = HEADING_RE.match(stripped)
        if not match:
            continue
        level, title = len(match.group(1)), match.group(2).strip()
        if level == 1:
            doc_title = title
            if not starts:
                starts.append((index, title, [title]))
        elif level == main_level:
            starts.append((index, title, ([doc_title] if doc_title else []) + [title]))

    if not starts:
        return [_MainSection(None, [], markdown, 0, max(len(lines) - 1, 0))]

    sections: list[_MainSection] = []
    for pos, (start, title, path) in enumerate(starts):
        end = starts[pos + 1][0] - 1 if pos + 1 < len(starts) else len(lines) - 1
        content = "\n".join(lines[start : end + 1]).strip()
        if content:
            sections.append(_MainSection(title, path, content, start, end))
    if len(sections) > 1 and sections[0].heading_path and len(sections[0].heading_path) == 1:
        first_lines = sections[0].content.splitlines()
        if len(first_lines) == 1 and HEADING_RE.match(first_lines[0].strip()):
            sections.pop(0)
    return sections


def _hard_split(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    paragraphs = re.split(r"\n\s*\n", text)
    parts: list[str] = []
    current = ""
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and len(candidate) > max_chars:
            parts.append(current)
            current = (current[-overlap_chars:] + "\n\n" + paragraph).strip() if overlap_chars else paragraph
        else:
            current = candidate
        while len(current) > max_chars:
            parts.append(current[:max_chars].strip())
            step = max_chars - overlap_chars
            current = current[max(step, 1):].strip()
    if current:
        parts.append(current)
    return parts or [text]


def chunk_markdown(
    markdown: str,
    material_id: str,
    user_id: str,
    max_tokens: int = MAX_CHUNK_TOKENS,
    *,
    strategy: dict | None = None,
) -> list[Chunk]:
    validated = validate_structure_strategy(strategy)
    main_level = int(validated["main_section_rule"].get("target_level", 2))
    chunk_rule = validated["chunk_rule"]
    max_chars = int(chunk_rule["max_chars"])
    overlap_chars = min(int(chunk_rule.get("overlap_chars", 0)), max_chars // 2)
    sections = _split_main_sections(markdown, main_level)
    chunks: list[Chunk] = []

    for section in sections:
        parts = _hard_split(section.content, max_chars, overlap_chars)
        # 保留旧 token 上限：极端长英文/数字段落仍可继续拆分。
        token_safe_parts: list[str] = []
        for part in parts:
            if estimate_tokens(part) <= max_tokens:
                token_safe_parts.append(part)
            else:
                token_safe_parts.extend(_hard_split(part, max(500, max_chars // 2), overlap_chars))

        for part_index, text in enumerate(token_safe_parts, start=1):
            chunk_index = len(chunks)
            split_reason = "length" if len(token_safe_parts) > 1 else "section"
            chunks.append(
                Chunk(
                    chunk_id=_make_chunk_id(material_id, chunk_index),
                    material_id=material_id,
                    user_id=user_id,
                    chunk_index=chunk_index,
                    text=text,
                    section_title=section.title,
                    heading_path=list(section.heading_path),
                    asset_paths=_extract_asset_paths_from_text(text),
                    token_count=estimate_tokens(text),
                    metadata={
                        "start_line": section.start_line,
                        "end_line": section.end_line,
                        "level": main_level if len(section.heading_path) > 1 else 1,
                        "part_index": part_index,
                        "split_reason": split_reason,
                    },
                )
            )
    return chunks


def chunk_markdown_file(
    markdown_path: Path,
    material_id: str,
    user_id: str,
    max_tokens: int = MAX_CHUNK_TOKENS,
    *,
    strategy: dict | None = None,
) -> list[Chunk]:
    return chunk_markdown(
        markdown_path.read_text(encoding="utf-8"),
        material_id,
        user_id,
        max_tokens,
        strategy=strategy,
    )
