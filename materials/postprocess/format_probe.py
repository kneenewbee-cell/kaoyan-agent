from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any


HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S+")
IMAGE_RE = re.compile(r"^\s*!\[[^\]]*]\([^)]+\)\s*$")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
HTML_TABLE_START_RE = re.compile(r"<table\b", re.IGNORECASE)
HTML_TABLE_END_RE = re.compile(r"</table>", re.IGNORECASE)
FORMULA_LINE_RE = re.compile(r"^\s*(\$\$|\\\[|\\\]|\\begin\{|\\end\{)|.*\$\S.*\$")
FORMULA_BOUNDARY_RE = re.compile(r"^\s*(\$\$|\\\[|\\\])\s*$")
LABEL_ORDINAL_RE = re.compile(r"^(知识点|考点|要点|专题|模块)\s*([一二三四五六七八九十百千万\d]+)\s*[:：、.]?\s*\S+")
CHINESE_OUTLINE_RE = re.compile(r"^[一二三四五六七八九十百千万]+、\s*\S+")
ARABIC_OUTLINE_RE = re.compile(r"^\d{1,2}[.、]\s*\S+")
DECIMAL_OUTLINE_RE = re.compile(r"^\d+(?:\.\d+)+\s+\S+")
CHAPTER_RE = re.compile(r"^第\s*[一二三四五六七八九十百千万\d]+\s*[篇章节部分]\s*\S+")
HEADING_MARKER_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
NORMAL_CHAPTER_RE = re.compile(r"^第\s*[一二三四五六七八九十百千万\d]+\s*[篇章节部]\s*\S+")
NORMAL_CHINESE_OUTLINE_RE = re.compile(r"^[一二三四五六七八九十百千万]+、\s*\S+")
NORMAL_ARABIC_OUTLINE_RE = re.compile(r"^\d{1,2}[.、]\s*\S+")
METADATA_HEADING_RE = re.compile(r"^(?:难度|题型|考频|来源|备注|页码|年份|科目|类型)[:：]\s*\S*")
NORMAL_METADATA_RE = re.compile(r"^(?:难度|题型|考频|来源|备注|页码|年份|科目|类型)[:：]\s*\S*")
COUNT_BADGE_RE = re.compile(
    r"^(?:[①②③④⑤⑥⑦⑧⑨⑩]\s*)?\d+\s*个(?:知识点|重难点|必会题型|易错点|高考考点|思想方法|题型|考点)$"
)
CIRCLED_OUTLINE_RE = re.compile(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*\S+")
COMPACT_CHINESE_OUTLINE_RE = re.compile(r"^[一二三四五六七八九十][^\s、，。；：:]{1,28}$")
QUESTION_GROUP_RE = re.compile(r"^(?:题组|出题角度|典型|例题|变式|探究)\s*[一二三四五六七八九十百千万\d]+")
SEMANTIC_TITLE_RE = re.compile(
    r"^(?:知识组|重难点|高考高频考题详解|基础知识完全解读|考情综述|函数图像的作法与确定|"
    r"考点|易错点|思想方法|常用方法|解题方法|方法总结)"
)
NORMAL_COUNT_BADGE_RE = re.compile(
    r"^(?:[①②③④⑤⑥⑦⑧⑨]\s*)?(?:\d+|[一二三四五六七八九十百千万]+)\s*个"
    r"(?:知识点|重难点|必会题型|易错点|高考考点|思想方法|题型|考点)$"
)
NORMAL_CIRCLED_OUTLINE_RE = re.compile(r"^[①②③④⑤⑥⑦⑧⑨]\s*\S+")
NORMAL_QUESTION_GROUP_RE = re.compile(r"^(?:题组|出题角度|典型|例题|变式|探究)\s*[一二三四五六七八九十百千万\d①②③④⑤⑥⑦⑧⑨]+")
SHORT_LINE_MAX = 24
SENTENCE_PUNCTUATION = ("。", "；", "？", "！", ";", "?", "!")
TOC_DOT_LEADER_RE = re.compile(r"\.{3,}|…{2,}")


FRONT_INDEX_MAX_LINES = 600
FRONT_INDEX_MAX_BLOCKS = 140
FRONT_BODY_PREVIEW_CHARS = 60


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
    heading_outline: list[dict[str, Any]] = field(default_factory=list)
    heading_level_counts: dict[str, int] = field(default_factory=dict)
    heading_pattern_counts: dict[str, int] = field(default_factory=dict)
    metadata_like_headings: list[str] = field(default_factory=list)
    circled_heading_candidates: list[str] = field(default_factory=list)
    compact_outline_candidates: list[str] = field(default_factory=list)
    front_block_index: list[dict[str, Any]] = field(default_factory=list)
    repeated_heading_candidates: list[dict[str, Any]] = field(default_factory=list)
    body_start_candidates: list[dict[str, Any]] = field(default_factory=list)
    layout_summary: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _collapse_probe_excerpt_lines(lines: list[str]) -> list[str]:
    collapsed: list[str] = []
    in_html_table = False
    table_lines = 0
    table_chars = 0

    def flush_table() -> None:
        nonlocal table_lines, table_chars
        if table_lines:
            collapsed.append(f"[HTML_TABLE_BLOCK omitted lines={table_lines} chars={table_chars}]")
            table_lines = 0
            table_chars = 0

    for line in lines:
        stripped = line.strip()
        starts_table = bool(HTML_TABLE_START_RE.search(stripped))
        if in_html_table or starts_table:
            in_html_table = True
            table_lines += 1
            table_chars += len(line)
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
                flush_table()
            continue
        collapsed.append(line)
    flush_table()
    return collapsed


def _join_excerpt(lines: list[str], limit: int = 4000) -> str:
    text = "\n".join(_collapse_probe_excerpt_lines(lines)).strip()
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


def _sample_sequence(items: list[Any], *, max_count: int, head_count: int, tail_count: int) -> list[Any]:
    if len(items) <= max_count:
        return items
    middle_count = max(max_count - head_count - tail_count, 0)
    head = items[:head_count]
    tail = items[-tail_count:] if tail_count else []
    middle_source = items[head_count : len(items) - tail_count if tail_count else len(items)]
    if not middle_source or middle_count <= 0:
        return head + tail
    if len(middle_source) <= middle_count:
        middle = middle_source
    else:
        step = len(middle_source) / middle_count
        middle = [middle_source[min(int(index * step), len(middle_source) - 1)] for index in range(middle_count)]
    return head + middle + tail


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
        or NORMAL_CHINESE_OUTLINE_RE.match(stripped)
        or ARABIC_OUTLINE_RE.match(stripped)
        or NORMAL_ARABIC_OUTLINE_RE.match(stripped)
        or DECIMAL_OUTLINE_RE.match(stripped)
        or CHAPTER_RE.match(stripped)
        or NORMAL_CHAPTER_RE.match(stripped)
        or NORMAL_QUESTION_GROUP_RE.match(stripped)
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


def _parse_heading(stripped: str) -> tuple[int, str] | None:
    match = HEADING_MARKER_RE.match(stripped)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def _classify_heading_title(title: str) -> str:
    if METADATA_HEADING_RE.match(title) or COUNT_BADGE_RE.match(title) or NORMAL_METADATA_RE.match(title) or NORMAL_COUNT_BADGE_RE.match(title):
        return "metadata_badge"
    if CHAPTER_RE.match(title) or NORMAL_CHAPTER_RE.match(title):
        return "chapter_unit"
    if LABEL_ORDINAL_RE.match(title):
        return "label_ordinal"
    if DECIMAL_OUTLINE_RE.match(title):
        return "decimal_outline"
    if CHINESE_OUTLINE_RE.match(title) or NORMAL_CHINESE_OUTLINE_RE.match(title):
        return "chinese_outline"
    if ARABIC_OUTLINE_RE.match(title) or NORMAL_ARABIC_OUTLINE_RE.match(title):
        return "arabic_outline"
    if CIRCLED_OUTLINE_RE.match(title) or NORMAL_CIRCLED_OUTLINE_RE.match(title):
        return "circled_outline"
    if QUESTION_GROUP_RE.match(title) or NORMAL_QUESTION_GROUP_RE.match(title):
        return "question_group"
    if SEMANTIC_TITLE_RE.match(title):
        return "semantic_title"
    if COMPACT_CHINESE_OUTLINE_RE.match(title):
        return "compact_chinese_outline"
    return "other_heading"


def _strip_heading_marker(text: str) -> str:
    parsed = _parse_heading(text.strip())
    return parsed[1] if parsed else text.strip()


def _normalize_repeated_title(title: str) -> str:
    title = _strip_heading_marker(title)
    title = re.sub(r"[\s#：:、.，,。；;|（）()\[\]【】《》<>-]+", "", title)
    return title.lower()


def _front_kind_for_line(stripped: str) -> tuple[str, dict[str, Any]]:
    parsed_heading = _parse_heading(stripped)
    if parsed_heading:
        level, title = parsed_heading
        return "heading", {
            "level": level,
            "text": stripped[:160],
            "title": title[:120],
            "pattern": _classify_heading_title(title),
        }
    if IMAGE_RE.match(stripped):
        return "image", {"text": stripped[:120]}
    if METADATA_HEADING_RE.match(stripped) or NORMAL_METADATA_RE.match(stripped):
        return "metadata", {"text": stripped[:120]}
    if COUNT_BADGE_RE.match(stripped) or NORMAL_COUNT_BADGE_RE.match(stripped):
        return "count_badge", {"text": stripped[:120]}
    if _is_candidate_marker(stripped):
        return "candidate_heading", {
            "text": stripped[:160],
            "pattern": _classify_heading_title(stripped),
        }
    return "body_preview", {}


def _append_front_block(
    blocks: list[dict[str, Any]],
    *,
    start_line: int,
    end_line: int,
    kind: str,
    **extra: Any,
) -> None:
    if len(blocks) >= FRONT_INDEX_MAX_BLOCKS:
        return
    block = {"start_line": start_line, "end_line": end_line, "kind": kind}
    block.update({key: value for key, value in extra.items() if value not in (None, "", [])})
    blocks.append(block)


def _build_front_block_index(lines: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    max_lines = min(len(lines), FRONT_INDEX_MAX_LINES)
    body_start: int | None = None
    body_parts: list[str] = []
    in_html_table = False
    html_start = 0
    html_lines = 0
    html_chars = 0
    in_formula = False
    formula_start = 0
    formula_lines = 0

    def flush_body(end_line: int) -> None:
        nonlocal body_start, body_parts
        if body_start is None:
            return
        preview = re.sub(r"\s+", " ", " ".join(body_parts)).strip()[:FRONT_BODY_PREVIEW_CHARS]
        _append_front_block(
            blocks,
            start_line=body_start,
            end_line=end_line,
            kind="body_preview",
            text_preview=preview,
            line_count=end_line - body_start + 1,
        )
        body_start = None
        body_parts = []

    index = 0
    while index < max_lines:
        line_no = index + 1
        line = lines[index]
        stripped = line.strip()

        if in_html_table:
            html_lines += 1
            html_chars += len(line)
            if HTML_TABLE_END_RE.search(stripped):
                _append_front_block(
                    blocks,
                    start_line=html_start,
                    end_line=line_no,
                    kind="html_table_block",
                    line_count=html_lines,
                    char_count=html_chars,
                )
                in_html_table = False
            index += 1
            continue

        if in_formula:
            formula_lines += 1
            if FORMULA_BOUNDARY_RE.match(stripped):
                _append_front_block(
                    blocks,
                    start_line=formula_start,
                    end_line=line_no,
                    kind="formula_block",
                    line_count=formula_lines,
                )
                in_formula = False
            index += 1
            continue

        if not stripped:
            flush_body(line_no - 1)
            index += 1
            continue

        if HTML_TABLE_START_RE.search(stripped):
            flush_body(line_no - 1)
            if HTML_TABLE_END_RE.search(stripped):
                _append_front_block(
                    blocks,
                    start_line=line_no,
                    end_line=line_no,
                    kind="html_table_block",
                    line_count=1,
                    char_count=len(line),
                )
            else:
                in_html_table = True
                html_start = line_no
                html_lines = 1
                html_chars = len(line)
            index += 1
            continue

        if FORMULA_BOUNDARY_RE.match(stripped):
            flush_body(line_no - 1)
            in_formula = True
            formula_start = line_no
            formula_lines = 1
            index += 1
            continue

        if TABLE_RE.match(stripped):
            flush_body(line_no - 1)
            table_start = line_no
            table_lines = 0
            while index < max_lines and TABLE_RE.match(lines[index].strip()):
                table_lines += 1
                index += 1
            _append_front_block(
                blocks,
                start_line=table_start,
                end_line=table_start + table_lines - 1,
                kind="markdown_table_block",
                line_count=table_lines,
            )
            continue

        kind, extra = _front_kind_for_line(stripped)
        if kind == "body_preview":
            if body_start is None:
                body_start = line_no
            body_parts.append(stripped[:FRONT_BODY_PREVIEW_CHARS])
        else:
            flush_body(line_no - 1)
            _append_front_block(blocks, start_line=line_no, end_line=line_no, kind=kind, **extra)
        index += 1

    flush_body(max_lines)
    if in_html_table:
        _append_front_block(
            blocks,
            start_line=html_start,
            end_line=max_lines,
            kind="html_table_block",
            line_count=html_lines,
            char_count=html_chars,
        )
    if in_formula:
        _append_front_block(
            blocks,
            start_line=formula_start,
            end_line=max_lines,
            kind="formula_block",
            line_count=formula_lines,
        )
    return blocks[:FRONT_INDEX_MAX_BLOCKS]


def _collect_repeated_heading_candidates(lines: list[str]) -> list[dict[str, Any]]:
    locations: dict[str, dict[str, Any]] = {}
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        title = ""
        pattern = ""
        parsed = _parse_heading(stripped)
        if parsed:
            title = parsed[1]
            pattern = _classify_heading_title(title)
        elif _is_candidate_marker(stripped):
            title = stripped
            pattern = _classify_heading_title(stripped)
        if not title or pattern not in {
            "chapter_unit",
            "label_ordinal",
            "chinese_outline",
            "arabic_outline",
            "question_group",
            "semantic_title",
        }:
            continue
        normalized = _normalize_repeated_title(title)
        if len(normalized) < 4:
            continue
        record = locations.setdefault(
            normalized,
            {
                "title_norm": normalized[:80],
                "sample_title": title[:120],
                "pattern": pattern,
                "line_nos": [],
            },
        )
        if len(record["line_nos"]) < 8:
            record["line_nos"].append(line_no)

    repeated = []
    for record in locations.values():
        line_nos = record["line_nos"]
        if len(line_nos) < 2:
            continue
        first = line_nos[0]
        later = next((line_no for line_no in line_nos[1:] if line_no > first + 5), None)
        if later is None:
            continue
        repeated.append({**record, "likely_front_duplicate": first <= FRONT_INDEX_MAX_LINES})
    repeated.sort(key=lambda item: (item["line_nos"][0], item["line_nos"][1]))
    return repeated[:80]


def _build_body_start_candidates(lines: list[str], repeated: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_lines: set[int] = set()
    for item in repeated:
        line_nos = item.get("line_nos", [])
        if not isinstance(line_nos, list) or len(line_nos) < 2:
            continue
        for line_no in line_nos[1:]:
            if not isinstance(line_no, int) or line_no in seen_lines:
                continue
            start = max(0, line_no - 4)
            end = min(len(lines), line_no + 80)
            candidates.append(
                {
                    "line_no": line_no,
                    "reason": "front_heading_reappears_with_following_content",
                    "sample_title": item.get("sample_title"),
                    "excerpt": _join_excerpt(lines[start:end], limit=1200),
                }
            )
            seen_lines.add(line_no)
            break
        if len(candidates) >= 3:
            break
    return candidates


def build_format_probe(
    raw_markdown: str,
    filename: str | None = None,
    *,
    layout_summary: dict[str, Any] | None = None,
) -> FormatProbe:
    text = raw_markdown.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    existing_headings: list[str] = []
    heading_outline: list[dict[str, Any]] = []
    heading_level_counts: Counter[str] = Counter()
    heading_pattern_counts: Counter[str] = Counter()
    metadata_like_headings: list[str] = []
    circled_heading_candidates: list[str] = []
    compact_outline_candidates: list[str] = []
    candidate_marker_lines: list[str] = []
    short_counter: Counter[str] = Counter()
    table_count = 0
    formula_count = 0
    image_count = 0
    code_fence_count = 0
    in_code = False
    fence_marker: str | None = None
    in_html_table = False

    for line_no, line in enumerate(lines, start=1):
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
        if in_html_table:
            table_count += 1
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            table_count += 1
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
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
        parsed_heading = _parse_heading(stripped)
        if parsed_heading:
            level, title = parsed_heading
            pattern = _classify_heading_title(title)
            existing_headings.append(stripped)
            heading_level_counts[f"h{level}"] += 1
            heading_pattern_counts[pattern] += 1
            if len(heading_outline) < 300:
                heading_outline.append(
                    {
                        "line_no": line_no,
                        "level": level,
                        "title": title[:120],
                        "pattern": pattern,
                    }
                )
            if pattern == "metadata_badge" and len(metadata_like_headings) < 80:
                metadata_like_headings.append(stripped)
            elif pattern == "circled_outline" and len(circled_heading_candidates) < 80:
                circled_heading_candidates.append(stripped)
            elif pattern == "compact_chinese_outline" and len(compact_outline_candidates) < 80:
                compact_outline_candidates.append(stripped)
            if _is_candidate_marker(title):
                candidate_marker_lines.append(title)
            continue
        if _is_candidate_marker(stripped):
            candidate_marker_lines.append(stripped)
        if _is_short_line_candidate(stripped):
            short_counter[stripped] += 1

    short_candidates = [
        item for item, _ in short_counter.most_common(80)
    ]
    sampled_existing_headings = _sample_sequence(
        existing_headings,
        max_count=180,
        head_count=70,
        tail_count=40,
    )
    sampled_heading_outline = _sample_sequence(
        heading_outline,
        max_count=180,
        head_count=70,
        tail_count=40,
    )
    repeated_heading_candidates = _collect_repeated_heading_candidates(lines)
    return FormatProbe(
        version="1.0",
        filename=filename,
        char_count=len(text),
        line_count=len(lines),
        head_excerpt=_join_excerpt(lines[:120]),
        middle_excerpts=_middle_excerpts(lines),
        tail_excerpt=_join_excerpt(lines[-80:]),
        existing_headings=sampled_existing_headings,
        candidate_marker_lines=candidate_marker_lines[:200],
        short_line_candidates=short_candidates[:120],
        table_like_lines_count=table_count,
        formula_like_lines_count=formula_count,
        image_lines_count=image_count,
        code_fence_count=code_fence_count,
        heading_outline=sampled_heading_outline,
        heading_level_counts=dict(heading_level_counts),
        heading_pattern_counts=dict(heading_pattern_counts),
        metadata_like_headings=metadata_like_headings,
        circled_heading_candidates=circled_heading_candidates,
        compact_outline_candidates=compact_outline_candidates,
        front_block_index=_build_front_block_index(lines),
        repeated_heading_candidates=repeated_heading_candidates,
        body_start_candidates=_build_body_start_candidates(lines, repeated_heading_candidates),
        layout_summary=layout_summary,
    )
