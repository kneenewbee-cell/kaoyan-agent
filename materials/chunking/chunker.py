from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..postprocess.structure_strategy import validate_structure_strategy
from ..schemas import Chunk
from .token_counter import estimate_tokens

MAX_CHUNK_TOKENS = 1024
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
FORMULA_BOUNDARY_RE = re.compile(r"^\s*(\$\$|\\\[|\\\])\s*$")
STRUCTURAL_TOPIC_TITLE_RE = re.compile(
    r"^(?:[\u2764\u2665\u2605\u2606\u25c6\u25cf\u25cb\u25b2\u25a0\s]*)"
    r"(?:\u8003\u70b9|\u77e5\u8bc6\u70b9|\u77e5\u8bc6\u7ec4|\u9898\u578b|"
    r"\u5178\u578b|\u91cd\u96be\u70b9|\u6613\u9519\u70b9|\u51fa\u9898\u89d2\u5ea6)"
    r"\s*(?:\d+|[一二三四五六七八九十百]+)"
    r"(?:\s*(?:[、,，.．\-—~～至到]\s*)(?:\d+|[一二三四五六七八九十百]+))*"
    r"(?:\s*[：:、.．)\uff09]\s*|\s+).{0,120}$"
)


@dataclass
class _MainSection:
    title: str | None
    heading_path: list[str]
    content: str
    start_line: int
    end_line: int
    level: int = 0
    split_reason: str = "section"


CATALOG_ZONE_MIN_CONFIDENCE = 0.65


def _extract_asset_paths_from_text(text: str) -> list[str]:
    return [match.group(2) for match in IMAGE_RE.finditer(text)]


def _make_chunk_id(material_id: str, chunk_index: int) -> str:
    return hashlib.sha256(f"{material_id}:{chunk_index}".encode("utf-8")).hexdigest()[:16]


def _document_zone_payload(document_zones: Any | None) -> dict[str, Any]:
    if document_zones is None:
        return {}
    if isinstance(document_zones, dict):
        return document_zones
    if hasattr(document_zones, "model_dump"):
        dumped = document_zones.model_dump(mode="json")
        return dumped if isinstance(dumped, dict) else {}
    return {}


def _single_catalog_zones(document_zones: Any | None, line_count: int) -> list[dict[str, Any]]:
    payload = _document_zone_payload(document_zones)
    zones = payload.get("front_matter_zones") or []
    if not isinstance(zones, list):
        return []

    catalog_zones: list[dict[str, Any]] = []
    max_index = max(line_count - 1, 0)
    for raw_zone in zones:
        if not isinstance(raw_zone, dict):
            continue
        if raw_zone.get("type") != "catalog_or_navigation":
            continue
        if raw_zone.get("chunk_policy") != "single_catalog_chunk":
            continue
        try:
            confidence = float(raw_zone.get("confidence", 0.0))
            start = int(raw_zone.get("start_line", 0)) - 1
            end = int(raw_zone.get("end_line", 0)) - 1
        except (TypeError, ValueError):
            continue
        if confidence < CATALOG_ZONE_MIN_CONFIDENCE or start < 0 or end < start:
            continue
        title = str(raw_zone.get("title") or "").strip() or "\u76ee\u5f55"
        if title.lower().startswith("front matter"):
            title = "\u76ee\u5f55"
        catalog_zones.append(
            {
                "start": max(0, min(start, max_index)),
                "end": max(0, min(end, max_index)),
                "title": title,
            }
        )

    catalog_zones.sort(key=lambda zone: (zone["start"], zone["end"]))
    merged: list[dict[str, Any]] = []
    for zone in catalog_zones:
        if not merged or zone["start"] > merged[-1]["end"] + 1:
            merged.append(zone)
            continue
        merged[-1]["end"] = max(merged[-1]["end"], zone["end"])
    return merged


def _zone_for_line(index: int, zones: list[dict[str, Any]]) -> dict[str, Any] | None:
    for zone in zones:
        if zone["start"] <= index <= zone["end"]:
            return zone
    return None


def _is_structural_topic_title(title: str) -> bool:
    stripped = title.strip()
    if not stripped or len(stripped) > 160:
        return False
    return bool(STRUCTURAL_TOPIC_TITLE_RE.match(stripped))


def _effective_heading_level(
    raw_level: int,
    title: str,
    main_level: int,
    heading_stack: dict[int, str] | None = None,
) -> int:
    if not _is_structural_topic_title(title):
        return raw_level
    if heading_stack:
        parent_levels = [
            level
            for level, existing_title in heading_stack.items()
            if level < raw_level and not _is_structural_topic_title(existing_title)
        ]
        if parent_levels:
            return max(parent_levels) + 1
    if raw_level > main_level:
        return main_level + 1
    return raw_level


def _split_main_sections(markdown: str, main_level: int, *, document_zones: Any | None = None) -> list[_MainSection]:
    """按目标层级切块，同时保留更高层级标题下未被子标题覆盖的正文。"""
    lines = markdown.splitlines()
    heading_stack: dict[int, str] = {}
    catalog_zones = _single_catalog_zones(document_zones, len(lines))
    starts: list[tuple[int, int | None, int, str | None, list[str], str]] = [
        (zone["start"], zone["end"], 1, zone["title"], [zone["title"]], "catalog_zone")
        for zone in catalog_zones
    ]
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    for index, line in enumerate(lines):
        if _zone_for_line(index, catalog_zones) is not None:
            continue
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
        if match:
            raw_level, title = len(match.group(1)), match.group(2).strip()
        elif _is_structural_topic_title(stripped):
            raw_level, title = main_level + 1, stripped
        else:
            continue
        is_structural_topic = _is_structural_topic_title(title)
        level = _effective_heading_level(raw_level, title, main_level, heading_stack)
        for existing_level in list(heading_stack):
            if existing_level >= level:
                del heading_stack[existing_level]
        heading_stack[level] = title
        if level <= main_level or is_structural_topic:
            path = [heading_stack[item_level] for item_level in sorted(heading_stack) if item_level <= level]
            starts.append((index, None, level, title, path, "section"))

    if not starts:
        return [_MainSection(None, [], markdown, 0, max(len(lines) - 1, 0), 0)]

    starts.sort(key=lambda item: (item[0], item[1] if item[1] is not None else len(lines)))
    sections: list[_MainSection] = []
    for pos, (start, fixed_end, level, title, path, split_reason) in enumerate(starts):
        next_end = starts[pos + 1][0] - 1 if pos + 1 < len(starts) else len(lines) - 1
        end = min(fixed_end, next_end) if fixed_end is not None else next_end
        content = "\n".join(lines[start : end + 1]).strip()
        if not content:
            continue
        content_lines = content.splitlines()
        if split_reason != "catalog_zone" and content_lines and HEADING_RE.match(content_lines[0].strip()):
            body_lines = [line for line in content_lines[1:] if line.strip()]
            if not body_lines:
                continue
        if split_reason != "catalog_zone" and content_lines and _is_structural_topic_title(content_lines[0].strip()):
            body_lines = [line for line in content_lines[1:] if line.strip()]
            if not body_lines:
                continue
        sections.append(_MainSection(title, path, content, start, end, level, split_reason))
    return sections


def _section_path_diversity(sections: list[_MainSection]) -> int:
    return len({tuple(section.heading_path) for section in sections if section.heading_path})


def _max_section_chars(sections: list[_MainSection]) -> int:
    return max((len(section.content) for section in sections), default=0)


def _sections_need_finer_split(sections: list[_MainSection], max_chars: int) -> bool:
    if len(sections) <= 1:
        return True
    return any(len(section.content) > int(max_chars * 1.5) for section in sections)


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
    document_zones: Any | None = None,
) -> list[Chunk]:
    validated = validate_structure_strategy(strategy)
    main_level = int(validated["main_section_rule"].get("target_level", 2))
    chunk_rule = validated["chunk_rule"]
    max_chars = int(chunk_rule["max_chars"])
    overlap_chars = min(int(chunk_rule.get("overlap_chars", 0)), max_chars // 2)
    effective_main_level = main_level
    sections = _split_main_sections(markdown, main_level, document_zones=document_zones)
    current_diversity = _section_path_diversity(sections)
    current_max_chars = _max_section_chars(sections)
    if main_level < 5:
        for candidate_level in range(main_level + 1, 6):
            if not _sections_need_finer_split(sections, max_chars):
                break
            finer_sections = _split_main_sections(markdown, candidate_level, document_zones=document_zones)
            finer_diversity = _section_path_diversity(finer_sections)
            finer_max_chars = _max_section_chars(finer_sections)
            improves_count = len(finer_sections) > len(sections)
            improves_size = bool(finer_sections) and (not sections or finer_max_chars < current_max_chars)
            if (
                (improves_count or improves_size)
                and len(finer_sections) <= 200
                and (finer_diversity > current_diversity or improves_size)
            ):
                sections = finer_sections
                effective_main_level = candidate_level
                current_diversity = finer_diversity
                current_max_chars = finer_max_chars
    chunks: list[Chunk] = []

    for section in sections:
        parts = [section.content] if section.split_reason == "catalog_zone" else _hard_split(section.content, max_chars, overlap_chars)
        # 保留旧 token 上限：极端长英文/数字段落仍可继续拆分。
        token_safe_parts: list[str] = []
        if section.split_reason == "catalog_zone":
            token_safe_parts = parts
        else:
            for part in parts:
                if estimate_tokens(part) <= max_tokens:
                    token_safe_parts.append(part)
                else:
                    token_safe_parts.extend(_hard_split(part, max(500, max_chars // 2), overlap_chars))

        for part_index, text in enumerate(token_safe_parts, start=1):
            chunk_index = len(chunks)
            split_reason = section.split_reason if section.split_reason != "section" else ("length" if len(token_safe_parts) > 1 else "section")
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
                        "level": section.level or 1,
                        "effective_main_level": effective_main_level,
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
    document_zones: Any | None = None,
) -> list[Chunk]:
    return chunk_markdown(
        markdown_path.read_text(encoding="utf-8"),
        material_id,
        user_id,
        max_tokens,
        strategy=strategy,
        document_zones=document_zones,
    )
