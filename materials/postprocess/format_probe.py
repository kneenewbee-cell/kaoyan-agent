from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass


HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S+")
IMAGE_RE = re.compile(r"^\s*!\[[^\]]*]\([^)]+\)\s*$")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
FORMULA_LINE_RE = re.compile(r"^\s*(\$\$|\\\[|\\\]|\\begin\{|\\end\{)|.*\$\S.*\$")
LABEL_ORDINAL_RE = re.compile(r"^(知识点|考点|要点|专题|模块)\s*([一二三四五六七八九十百千万\d]+)\s*[:：、.]?\s*\S+")
CHINESE_OUTLINE_RE = re.compile(r"^[一二三四五六七八九十百千万]+、\s*\S+")
ARABIC_OUTLINE_RE = re.compile(r"^\d{1,2}[.、]\s*\S+")
DECIMAL_OUTLINE_RE = re.compile(r"^\d+(?:\.\d+)+\s+\S+")
CHAPTER_RE = re.compile(r"^第\s*[一二三四五六七八九十百千万\d]+\s*[章节部分]\s*\S+")
SHORT_LINE_MAX = 24
SENTENCE_PUNCTUATION = ("。", "；", "？", "！", ";", "?", "!")
TOC_DOT_LEADER_RE = re.compile(r"\.{3,}|…{2,}")


@dataclass
class FormatProbe:
    version: str
    filename: str | None
    char_count: int
    line_count: int
    head_excerpt: str
    middle_excerpts: list[str]
    tail_excerpt: str
    existing_headings: list[str]
    candidate_marker_lines: list[str]
    short_line_candidates: list[str]
    table_like_lines_count: int
    formula_like_lines_count: int
    image_lines_count: int
    code_fence_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def _join_excerpt(lines: list[str], limit: int = 4000) -> str:
    text = "\n".join(lines).strip()
    return text[:limit]


def _middle_excerpts(lines: list[str]) -> list[str]:
    if len(lines) <= 220:
        return []
    excerpts: list[str] = []
    anchors = [len(lines) // 3, (len(lines) * 2) // 3]
    for anchor in anchors:
        start = max(0, anchor - 30)
        end = min(len(lines), anchor + 30)
        excerpt = _join_excerpt(lines[start:end], limit=2500)
        if excerpt:
            excerpts.append(excerpt)
    return excerpts


def _is_candidate_marker(stripped: str) -> bool:
    if not stripped or len(stripped) > 120:
        return False
    if TOC_DOT_LEADER_RE.search(stripped):
        return False
    if any(mark in stripped for mark in SENTENCE_PUNCTUATION):
        return False
    if "." in stripped and len(stripped) > 48:
        return False
    return bool(
        LABEL_ORDINAL_RE.match(stripped)
        or CHINESE_OUTLINE_RE.match(stripped)
        or ARABIC_OUTLINE_RE.match(stripped)
        or DECIMAL_OUTLINE_RE.match(stripped)
        or CHAPTER_RE.match(stripped)
    )


def _is_short_line_candidate(stripped: str) -> bool:
    if not stripped or len(stripped) > SHORT_LINE_MAX:
        return False
    if any(token in stripped for token in ("。", "，", "；", "、")) and stripped not in {"注意事项"}:
        return False
    if HEADING_RE.match(stripped) or _is_candidate_marker(stripped):
        return False
    if TABLE_RE.match(stripped) or IMAGE_RE.match(stripped) or FORMULA_LINE_RE.match(stripped):
        return False
    return True


def build_format_probe(raw_markdown: str, filename: str | None = None) -> FormatProbe:
    text = raw_markdown.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    existing_headings: list[str] = []
    candidate_marker_lines: list[str] = []
    short_counter: Counter[str] = Counter()
    table_count = 0
    formula_count = 0
    image_count = 0
    code_fence_count = 0
    in_code = False
    fence_marker: str | None = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            code_fence_count += 1
            if not in_code:
                in_code = True
                fence_marker = marker
            elif fence_marker == marker:
                in_code = False
                fence_marker = None
            continue
        if in_code:
            continue
        if TABLE_RE.match(stripped):
            table_count += 1
            continue
        if IMAGE_RE.match(stripped):
            image_count += 1
            continue
        if FORMULA_LINE_RE.match(stripped):
            formula_count += 1
            continue
        if HEADING_RE.match(stripped):
            existing_headings.append(stripped)
            continue
        if _is_candidate_marker(stripped):
            candidate_marker_lines.append(stripped)
        if _is_short_line_candidate(stripped):
            short_counter[stripped] += 1

    short_candidates = [
        item for item, _ in short_counter.most_common(80)
    ]
    return FormatProbe(
        version="1.0",
        filename=filename,
        char_count=len(text),
        line_count=len(lines),
        head_excerpt=_join_excerpt(lines[:120]),
        middle_excerpts=_middle_excerpts(lines),
        tail_excerpt=_join_excerpt(lines[-80:]),
        existing_headings=existing_headings[:120],
        candidate_marker_lines=candidate_marker_lines[:200],
        short_line_candidates=short_candidates[:120],
        table_like_lines_count=table_count,
        formula_like_lines_count=formula_count,
        image_lines_count=image_count,
        code_fence_count=code_fence_count,
    )
