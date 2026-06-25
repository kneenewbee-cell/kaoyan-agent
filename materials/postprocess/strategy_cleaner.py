from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .strategy_schema import CleaningStrategy, DocumentZones, HeadingFamily, HeadingRule, MainSectionRule, PatternToken


CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
MARKDOWN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
HTML_TABLE_START_RE = re.compile(r"<table\b", re.IGNORECASE)
HTML_TABLE_END_RE = re.compile(r"</table>", re.IGNORECASE)
IMAGE_RE = re.compile(r"^\s*!\[[^\]]*]\([^)]+\)\s*$")
FORMULA_BOUNDARY_RE = re.compile(r"^\s*(\$\$|\\\[|\\\])\s*$")
INLINE_FORMULA_RE = re.compile(r"\$[^$\n]+\$")
SETEXT_H1_RE = re.compile(r"^\s*=+\s*$")
SETEXT_H2_RE = re.compile(r"^\s*-+\s*$")
TOC_DOT_LEADER_RE = re.compile(r"\.{3,}|…{2,}")
SENTENCE_PUNCTUATION = ("。", "；", "？", "！", ";", "?", "!")

CHINESE_NUM = "零〇一二三四五六七八九十百千万两"
CHAPTER_SUMMARY_RE = re.compile(rf"^(?:第\s*[{CHINESE_NUM}\d]+\s*[篇章]\s*)?(?:本章)?(?:小结|总结)$")
CHAPTER_HEADING_RE = re.compile(rf"^第\s*[{CHINESE_NUM}\d]+\s*(?:篇|章|部分)\s*\S+")
SECTION_HEADING_RE = re.compile(rf"^第\s*[{CHINESE_NUM}\d]+\s*节\s*\S+")
CHINESE_OUTLINE_HEADING_RE = re.compile(rf"^[{CHINESE_NUM}]+、\s*\S+")
PAREN_CHINESE_HEADING_RE = re.compile(rf"^[（(]\s*[{CHINESE_NUM}]+\s*[）)]\s*\S+")
NUMBERED_HEADING_RE = re.compile(r"^(?:\d+[.．、]\s*|[（(]\d+[）)])\S+")
QUESTION_TYPE_HEADING_RE = re.compile(r"^题型\s*[一二三四五六七八九十百千万\d]+")
KNOWLEDGE_BLOCK_HEADING_RE = re.compile(
    r"^(?:知识组|重难点|考点|题组|典型|易错点|思想方法|出题角度)\s*[一二三四五六七八九十百千万\d①②③④⑤⑥⑦⑧⑨⑩]+"
)
MAJOR_SECTION_HEADING_RE = re.compile(
    r"^[A-Z]?(?:考情综述|基础知识完全解读|核心题型题组例解|高考高频考题详解|重点疑难专项突破|知识网络|本章概要)"
)
METADATA_HEADING_RE = re.compile(r"^(?P<label>难度|题型|考频|来源|备注|页码|年份|科目|类型)[:：]\s*(?P<rest>.*)$")
TRAILING_METADATA_RE = re.compile(
    r"\s+(?P<label>难度|题型|考频|来源|备注|页码|年份|科目|类型)[:：]\s*(?P<rest>\S.*?)\s*$"
)
COUNT_BADGE_HEADING_RE = re.compile(
    rf"^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d+|[{CHINESE_NUM}]+)\s*个"
    r"(?:知识点|重难点|必会题型|易错点|高考考点|思想方法|题型|考点)$"
)
CIRCLED_HEADING_RE = re.compile(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*\S+")
COMPACT_CHINESE_OUTLINE_HEADING_RE = re.compile(rf"^[{CHINESE_NUM}][^\s、，。；：:]{{1,28}}$")
SENTENCE_FRAGMENT_HEADING_RE = re.compile(
    r"(?:[，,].{0,16}(?:得|有|可知|所以|则|故)$|(?:代入|代人)[，,]?(?:得|有)$)"
)
EXPLANATORY_HEADING_RE = re.compile(
    r"(?:"
    r"(?:方法|思路|步骤|类型|情况|题型|模型|结论|性质|问题|解法|公式|函数|概念|定义|定理|关系|式子|角|值|图像|图象|变换|思想|应用)"
    r".{0,18}(?:有$|有(?:以下|如下|下列|若干|几|[零〇一二三四五六七八九十百千万两\d]+)种?|如下|包括|分为|可分为)"
    r"|"
    r"(?:是一种|是一个|是指|即为|称为|叫做|常用来|常用于|一般可|一般采用|通常采用|需要注意|要注意|应注意|常用下列|主要体现|就能|即可|可得到|可得出|问题即可得证)"
    r")"
)
TRANSITION_SENTENCE_HEADING_RE = re.compile(
    r"^(?:首先|先|然后|再|接着|其次|最后).{4,}(?:，|,|再|根据|利用|即可|可得|求得)"
)
LETTERED_SENTENCE_HEADING_RE = re.compile(r"^[A-Za-z][.．]\s*(?:若|如果|当|设|已知)\S+")
IMAGE_CAPTION_HEADING_RE = re.compile(r"^(?:图|表)\s*\d+(?:[-－—]\d+)*(?:\s*[:：]?.*)?$")
BODY_LIKE_HEADING_RE = re.compile(r"^(注|解|证明|分析|方法|答|提示|评注|说明)\b|\A(注|解|证明|分析|方法|答|提示|评注|说明)")
LOCAL_LABEL_PREFIXES = ("评注", "点评", "点拨", "证明", "解析", "分析", "提示", "说明", "答案", "答", "注", "解")
BRACKET_LOCAL_LABEL_RE = re.compile(r"^【\s*(注|解|证明|分析|解析|提示|说明|答案|答|评注|点评|点拨)\s*】\s*(.*)$")
STEP_LOCAL_LABEL_RE = re.compile(rf"^(第\s*[{CHINESE_NUM}\d]+\s*步)\s*[:：]\s*(.*)$")
METHOD_LOCAL_LABEL_RE = re.compile(
    rf"^(方法(?:[{CHINESE_NUM}\d]+|[（(][{CHINESE_NUM}\d]+[）)])?(?:如下)?)"
    r"(?=$|[\s:：、，,。；;（(])"
)
PAREN_METHOD_LOCAL_LABEL_RE = re.compile(rf"^[（(]\s*(方法(?:[{CHINESE_NUM}\d]+)?(?:如下)?)\s*[）)]")
SOLUTION_METHOD_LABEL_RE = re.compile(r"^(直接法|排除法|反证法|分析法|综合法|构造法|换元法|放缩法)(?=$|[\s:：、，,。；;（(])")
STRUCTURAL_LOCAL_LABEL_RE = re.compile(
    r"^(?:"
    r"注意事项|解题步骤|解题方法|解法总结|"
    r"常用方法|常用计算方法|"
    r"方法(?:总结|归纳|梳理|技巧|专题|思想|应用)|"
    r"证明(?:方法|技巧|专题|思路|思路总结|框架)|"
    r"分析(?:方法|思路|框架)"
    r")"
)
DEFAULT_MAIN_ALIASES = ["知识点", "考点", "要点", "专题", "模块"]
DEFAULT_SUBSECTION_ALIASES = [
    "核心概念",
    "基本概念",
    "常用方法",
    "常用计算方法",
    "经典例题",
    "典型例题",
    "易错提醒",
    "易错点",
    "注意事项",
    "应用举例",
    "常见题型",
]
SEMANTIC_SUBSECTION_ALIASES = set(DEFAULT_SUBSECTION_ALIASES) | {
    "定义",
    "基本定义",
    "命题特征",
    "解题步骤",
    "常见陷阱",
    "Common Patterns",
    "考试内容要点精讲",
    "常用公式",
    "常用的方法",
}
SUBSECTION_RULE_HINTS = (
    "concept",
    "definition",
    "method",
    "example",
    "warning",
    "summary",
    "subsection",
    "section",
)


@dataclass
class StrategyCleanResult:
    cleaned_markdown: str
    strategy: dict[str, Any]
    parse_report: dict[str, Any]
    warnings: list[str]


@dataclass
class OutlineFrame:
    level: int
    title: str
    family: str | None = None
    outline_family: str | None = None
    ordinal: int | None = None
    line_no: int = 0


def _line_is_protected(stripped: str, *, in_formula_block: bool) -> bool:
    if in_formula_block:
        return True
    return bool(
        TABLE_RE.match(stripped)
        or TABLE_SEPARATOR_RE.match(stripped)
        or IMAGE_RE.match(stripped)
        or FORMULA_BOUNDARY_RE.match(stripped)
        or INLINE_FORMULA_RE.search(stripped)
    )


def _make_heading(line: str, level: int) -> str:
    return f"{'#' * level} {line.strip()}"


def _parse_existing_heading(stripped: str) -> tuple[int, str] | None:
    match = MARKDOWN_HEADING_RE.match(stripped)
    if not match:
        return None
    marker = match.group(0).split(maxsplit=1)[0]
    title = stripped[len(marker):].strip()
    return len(marker), title


def _append_warning_once(warnings: list[str], warning: str) -> None:
    if warning not in warnings:
        warnings.append(warning)


def _is_structural_local_label_exception(title: str) -> bool:
    compact = re.sub(r"\s+", "", title.strip())
    if not compact:
        return False
    semantic_aliases = {re.sub(r"\s+", "", alias) for alias in SEMANTIC_SUBSECTION_ALIASES}
    return compact in semantic_aliases or bool(STRUCTURAL_LOCAL_LABEL_RE.match(compact))


def _format_local_label(label: str, rest: str) -> str:
    cleaned_rest = re.sub(r"^[\s:：、，,。；;\-—]+", "", rest.strip())
    return f"**{label}：**" + (f" {cleaned_rest}" if cleaned_rest else "")


def _body_like_heading_to_label(title: str) -> str | None:
    """Convert local solution labels to inline labels instead of headings."""
    stripped = title.strip()
    if not stripped or _is_structural_local_label_exception(stripped):
        return None

    bracket_match = BRACKET_LOCAL_LABEL_RE.match(stripped)
    if bracket_match:
        return _format_local_label(bracket_match.group(1), bracket_match.group(2))

    step_match = STEP_LOCAL_LABEL_RE.match(stripped)
    if step_match:
        return _format_local_label(re.sub(r"\s+", "", step_match.group(1)), step_match.group(2))

    method_match = PAREN_METHOD_LOCAL_LABEL_RE.match(stripped) or METHOD_LOCAL_LABEL_RE.match(stripped)
    if method_match:
        label = method_match.group(1)
        return _format_local_label(label, stripped[method_match.end():])

    solution_method_match = SOLUTION_METHOD_LABEL_RE.match(stripped)
    if solution_method_match:
        label = solution_method_match.group(1)
        return _format_local_label(label, stripped[solution_method_match.end():])

    for label in LOCAL_LABEL_PREFIXES:
        if not stripped.startswith(label):
            continue
        if label == "解":
            next_text = stripped[len(label):]
            if next_text and next_text.startswith(
                ("直接法", "排除法", "反证法", "分析法", "综合法", "构造法", "换元法", "放缩法")
            ):
                return _format_local_label(label, next_text)
            if next_text and not re.match(r"^[\s:：、，,。；;（(]|得|为|由", next_text):
                return None
        return _format_local_label(label, stripped[len(label):])

    return None


def _pseudo_heading_to_local_label(title: str) -> str | None:
    stripped = title.strip()
    metadata_match = METADATA_HEADING_RE.match(stripped)
    if metadata_match:
        return _format_local_label(metadata_match.group("label"), metadata_match.group("rest"))
    if COUNT_BADGE_HEADING_RE.match(stripped):
        return stripped
    return None


def _split_trailing_heading_metadata(title: str) -> tuple[str, str | None]:
    return title.strip(), None


def _emit_heading(
    *,
    output: list[str],
    title: str,
    level: int,
    raw: str,
    line_no: int,
    local_label_matches: list[dict[str, Any]],
    warnings: list[str],
) -> tuple[str, str]:
    heading_title, trailing_metadata = _split_trailing_heading_metadata(title)
    converted = _make_heading(heading_title, level)
    output.append(converted)
    if trailing_metadata is not None:
        output.append(trailing_metadata)
        local_label_matches.append(
            {
                "line_no": line_no,
                "raw": raw,
                "converted": trailing_metadata,
                "rule": "heading_trailing_metadata_to_local_label",
                "confidence": 0.88,
            }
        )
        _append_warning_once(warnings, "heading_trailing_metadata_demoted_to_label")
    return heading_title, converted


def _looks_like_sentence_fragment_heading(title: str) -> bool:
    stripped = title.strip()
    if not stripped:
        return False
    if _body_like_heading_to_label(stripped) is not None:
        return False
    if IMAGE_CAPTION_HEADING_RE.match(stripped):
        return True
    if _outline_marker(stripped) is not None and stripped.endswith(("，", ",", "。", ".", "：", ":")):
        return True
    if SENTENCE_FRAGMENT_HEADING_RE.search(stripped):
        return True
    if EXPLANATORY_HEADING_RE.search(stripped):
        return True
    if TRANSITION_SENTENCE_HEADING_RE.search(stripped):
        return True
    if LETTERED_SENTENCE_HEADING_RE.search(stripped):
        return True
    return False


def _chinese_ordinal_to_int(value: str) -> int | None:
    value = re.sub(r"\s+", "", value.strip())
    if not value:
        return None
    digits = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if value.isdigit():
        return int(value)
    if value in digits and digits[value] > 0:
        return digits[value]
    if value == "十":
        return 10
    if "十" in value:
        left, _, right = value.partition("十")
        tens = digits.get(left, 1) if left else 1
        ones = digits.get(right, 0) if right else 0
        return tens * 10 + ones
    return None


def _outline_marker(title: str) -> tuple[str, int | None] | None:
    stripped = title.strip()
    match = re.match(r"^([A-Z])\s*(?!已知|[为是若当设由在与和及的])(?=[\u4e00-\u9fff])\S+", stripped)
    if match:
        return "alpha_outline", ord(match.group(1)) - ord("A") + 1
    match = re.match(rf"^([{CHINESE_NUM}]+)\s*、\s*\S+", stripped)
    if match:
        return "chinese_outline", _chinese_ordinal_to_int(match.group(1))
    match = re.match(rf"^[（(]\s*([{CHINESE_NUM}]+)\s*[）)]\s*\S+", stripped)
    if match:
        return "paren_chinese", _chinese_ordinal_to_int(match.group(1))
    match = re.match(r"^(\d{1,2})[.．、]\s*\S+", stripped)
    if match:
        return "arabic_outline", int(match.group(1))
    match = re.match(r"^[（(]\s*(\d{1,2})\s*[）)]\s*\S+", stripped)
    if match:
        return "paren_arabic", int(match.group(1))
    circled_map = {char: index for index, char in enumerate("①②③④⑤⑥⑦⑧⑨⑩", start=1)}
    if stripped[:1] in circled_map:
        return "circled", circled_map[stripped[:1]]
    match = re.match(rf"^([{CHINESE_NUM}])([^\s、，。；：:]{{1,28}})$", stripped)
    if match:
        return "compact_chinese_outline", _chinese_ordinal_to_int(match.group(1))
    return None


def _outline_body(title: str) -> str:
    stripped = title.strip()
    patterns = [
        r"^[A-Z]\s*(?P<body>[\u4e00-\u9fff].+)$",
        rf"^[{CHINESE_NUM}]+\s*、\s*(?P<body>.+)$",
        rf"^[（(]\s*[{CHINESE_NUM}]+\s*[）)]\s*(?P<body>.+)$",
        r"^\d{1,2}[.．、]\s*(?P<body>.+)$",
        r"^[（(]\s*\d{1,2}\s*[）)]\s*(?P<body>.+)$",
        r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*(?P<body>.+)$",
        rf"^[{CHINESE_NUM}](?P<body>[^\s、，。；：:].+)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, stripped)
        if match:
            return match.group("body").strip()
    return stripped


def _outline_candidate_is_body_text(
    title: str,
    family: HeadingFamily | None = None,
    *,
    document_type: str | None = None,
) -> bool:
    marker = _outline_marker(title)
    if marker is None:
        return False
    if family is not None:
        if family.kind == "major_section":
            return False
        if family.anchors:
            return False
        if document_type == "exercise_notes" and family.kind in {"item", "block"}:
            return False
    body = _outline_body(title)
    compact = re.sub(r"\s+", "", body)
    if not compact:
        return True
    if len(compact) > 36:
        return True
    if re.search(r"[，,。；;？！?]", body):
        return True
    if re.search(r"^(?:请|若|如果|当|设|已知|根据|由|通过|按照|按一定|按.*规则).{2,}", body):
        return True
    if re.search(r"(?:判断|检验|观察|发现|得出|预测).{0,18}(?:是否|有无|多少|异常|变化|关系)", body):
        return True
    if len(compact) > 24 and re.search(r"(?:应|应该|需要|可以|能够|一般|通常|主要|从而|因此|所以|即可|就能)", body):
        return True
    return False


def _push_outline_frame(stack: list[OutlineFrame], frame: OutlineFrame) -> None:
    while stack and (stack[-1].level > frame.level or (stack[-1].level == frame.level and stack[-1].family == frame.family)):
        stack.pop()
    stack.append(frame)


def _outline_stack_level(
    title: str,
    suggested_level: int,
    *,
    outline_stack: list[OutlineFrame],
    latest_main_level: int | None,
    line_no: int,
) -> tuple[int, str | None]:
    marker = _outline_marker(title)
    if marker is None:
        return suggested_level, None
    family, ordinal = marker
    for frame in reversed(outline_stack):
        if frame.family != family and frame.outline_family != family:
            continue
        if ordinal is None or frame.ordinal is None or ordinal >= frame.ordinal:
            return frame.level, family
    if ordinal is not None and ordinal > 1:
        return min(max(suggested_level, 2), 6), family
    if outline_stack:
        level = min(max(outline_stack[-1].level + 1, 2), 6)
    elif latest_main_level is not None:
        level = min(max(latest_main_level + 1, 2), 6)
    else:
        level = min(max(suggested_level, 2), 6)
    return level, family


def _nearest_local_outline_level(outline_stack: list[OutlineFrame]) -> int | None:
    for frame in reversed(outline_stack):
        frame_family = frame.outline_family or frame.family
        if frame_family in {"chinese_outline", "compact_chinese_outline", "paren_chinese"}:
            return frame.level
    return None


def _should_demote_unmarked_existing_heading(title: str, current_level: int, outline_stack: list[OutlineFrame]) -> bool:
    if current_level > 2:
        return False
    if MAJOR_SECTION_HEADING_RE.match(title):
        return False
    if CHAPTER_HEADING_RE.match(title) or SECTION_HEADING_RE.match(title) or KNOWLEDGE_BLOCK_HEADING_RE.match(title):
        return False
    if _outline_marker(title) is not None:
        return False
    return _nearest_local_outline_level(outline_stack) is not None


def _apply_outline_decision(
    title: str,
    suggested_level: int,
    role: str,
    *,
    outline_stack: list[OutlineFrame],
    latest_main_level: int | None,
    line_no: int,
    warnings: list[str],
) -> tuple[int, str, str | None]:
    level, family = _outline_stack_level(
        title,
        suggested_level,
        outline_stack=outline_stack,
        latest_main_level=latest_main_level,
        line_no=line_no,
    )
    if family is not None:
        if level != suggested_level:
            _append_warning_once(warnings, "outline_stack_level_adjusted")
        if level > 2:
            role = "subsection"
    return level, role, family


def _remember_heading_in_outline_stack(
    outline_stack: list[OutlineFrame],
    *,
    title: str,
    level: int,
    family: str | None,
    line_no: int,
) -> None:
    ordinal = None
    marker = _outline_marker(title)
    outline_family = marker[0] if marker else None
    ordinal = marker[1] if marker else None
    _push_outline_frame(
        outline_stack,
        OutlineFrame(
            level=level,
            title=title,
            family=family,
            outline_family=outline_family,
            ordinal=ordinal,
            line_no=line_no,
        ),
    )


def _looks_like_semantic_subsection(line: str, rule: HeadingRule | None = None) -> bool:
    if line in SEMANTIC_SUBSECTION_ALIASES:
        return True
    if rule is None or rule.role != "subsection":
        return False
    rule_id = rule.id.lower()
    return any(hint in rule_id for hint in SUBSECTION_RULE_HINTS)


def _coerce_heading_level(
    line: str,
    requested_level: int,
    *,
    rule: HeadingRule | None,
    latest_rule_levels: dict[str, int],
    latest_main_level: int | None,
    warnings: list[str],
) -> tuple[int, str]:
    """Apply semantic hierarchy guardrails to LLM-declared heading levels."""
    level = requested_level
    role = rule.role if rule is not None else "main"

    parent_level = None
    if rule is not None and rule.parent_rule:
        parent_level = latest_rule_levels.get(rule.parent_rule)
        if parent_level is not None and level != parent_level + 1:
            level = parent_level + 1
            _append_warning_once(warnings, f"heading_level_coerced:{rule.id}")

    if rule is not None and role == "main" and level < 2:
        level = 2
        _append_warning_once(warnings, f"heading_level_coerced:{rule.id}")

    if CHAPTER_SUMMARY_RE.match(line):
        role = "subsection"
        floor_level = (latest_main_level + 1) if latest_main_level is not None else 3
        if level <= (latest_main_level or 2) or level < floor_level:
            level = floor_level
            _append_warning_once(warnings, f"chapter_summary_level_coerced:{rule.id if rule else 'legacy'}")
        if level > 4:
            level = 4
            _append_warning_once(warnings, f"chapter_summary_level_coerced:{rule.id if rule else 'legacy'}")

    if _looks_like_semantic_subsection(line, rule):
        role = "subsection"
        if parent_level is not None:
            expected = parent_level + 1
            if level != expected:
                level = expected
                _append_warning_once(warnings, f"semantic_subsection_level_coerced:{rule.id if rule else 'legacy'}")
        elif latest_main_level is not None and level <= latest_main_level:
            level = latest_main_level + 1
            _append_warning_once(warnings, f"semantic_subsection_level_coerced:{rule.id if rule else 'legacy'}")
        if level > 4:
            level = 4
            _append_warning_once(warnings, f"semantic_subsection_level_coerced:{rule.id if rule else 'legacy'}")

    return max(1, min(level, 6)), role


def _infer_existing_heading_level(
    title: str,
    current_level: int,
    *,
    latest_main_level: int | None,
    title_frequency: int = 1,
) -> tuple[int, str, str | None]:
    """Infer safer levels for Markdown headings produced by PDF/OCR converters."""
    if CHAPTER_SUMMARY_RE.match(title):
        return min(max((latest_main_level or 2) + 1, 3), 4), "subsection", "chapter_summary"
    if CHAPTER_HEADING_RE.match(title):
        return 2, "main", "chapter"
    if SECTION_HEADING_RE.match(title):
        return 3, "main", "section"
    if KNOWLEDGE_BLOCK_HEADING_RE.match(title):
        return min(max((latest_main_level or 2) + 1, 3), 4), "main", "knowledge_block"
    if CIRCLED_HEADING_RE.match(title) and latest_main_level is not None:
        return min(max(latest_main_level + 2, 4), 5), "subsection", "circled_outline"
    if COMPACT_CHINESE_OUTLINE_HEADING_RE.match(title) and latest_main_level is not None:
        return min(max(latest_main_level + 2, 4), 5), "subsection", "compact_chinese_outline"
    if title in SEMANTIC_SUBSECTION_ALIASES:
        return min(max((latest_main_level or 3) + 1, 3), 4), "subsection", "semantic_label"
    if BODY_LIKE_HEADING_RE.match(title):
        return min(max((latest_main_level or 3) + 1, 4), 5), "subsection", "body_like_heading"
    if QUESTION_TYPE_HEADING_RE.match(title):
        return min(max((latest_main_level or 3) + 1, 3), 4), "subsection", "question_type"
    if PAREN_CHINESE_HEADING_RE.match(title):
        return min(max((latest_main_level or 3) + 1, 4), 5), "subsection", "paren_chinese"
    if CHINESE_OUTLINE_HEADING_RE.match(title):
        return min(max((latest_main_level or 3) + 1, 3), 4), "subsection", "chinese_outline"
    if NUMBERED_HEADING_RE.match(title):
        return min(max((latest_main_level or 3) + 1, 4), 5), "subsection", "numbered"
    if current_level == 1 and latest_main_level is not None:
        if title_frequency >= 3:
            return 0, "subsection", "repeated_page_header"
        if re.search(r"(?:的方法有|如下|如下几种|有[一二三四五六七八九十两\d]+种)", title):
            return 0, "subsection", "sentence_like_h1"
        return min(max(latest_main_level + 1, 3), 4), "subsection", "untrusted_h1"
    return current_level, "main" if current_level <= 2 else "subsection", None


def _match_heading_rule(
    title: str,
    active_heading_rules: list[HeadingRule],
    heading_rule_matchers: dict[str, re.Pattern[str]],
    seen_rule_ids: set[str],
    active_rule_ids: set[str],
) -> HeadingRule | None:
    for rule in active_heading_rules:
        if rule.parent_rule and rule.parent_rule in active_rule_ids and rule.parent_rule not in seen_rule_ids:
            continue
        if _is_broad_title_text_rule(rule) and not _broad_title_text_rule_allows(title, rule):
            continue
        if heading_rule_matchers[rule.id].match(title):
            return rule
    return None


def _is_broad_title_text_rule(rule: HeadingRule) -> bool:
    return len(rule.pattern) == 1 and rule.pattern[0].type == "title_text"


def _broad_title_text_rule_allows(title: str, rule: HeadingRule) -> bool:
    compact = re.sub(r"\s+", "", title.strip())
    if not compact:
        return False
    example_compacts = {re.sub(r"\s+", "", example.strip()) for example in rule.examples}
    if compact in example_compacts:
        return True
    return bool(
        MAJOR_SECTION_HEADING_RE.match(title)
        or CHAPTER_HEADING_RE.match(title)
        or SECTION_HEADING_RE.match(title)
        or KNOWLEDGE_BLOCK_HEADING_RE.match(title)
        or QUESTION_TYPE_HEADING_RE.match(title)
    )


def _local_strong_boundary_level(title: str) -> int | None:
    if SECTION_HEADING_RE.match(title):
        return 3
    if CHAPTER_HEADING_RE.match(title):
        return 2
    return None


def _match_family_ordinal(text: str, styles: list[str]) -> re.Match[str] | None:
    for style in styles:
        if style == "arabic":
            match = re.match(r"\s*\d{1,3}", text)
        elif style == "alpha":
            match = re.match(r"\s*[A-Z]", text)
        elif style == "chinese":
            match = re.match(rf"\s*[{CHINESE_NUM}]+", text)
        elif style == "decimal":
            match = re.match(r"\s*\d+(?:[.．]\d+)+", text)
        elif style == "circled":
            match = re.match(r"\s*[①②③④⑤⑥⑦⑧⑨⑩]", text)
        elif style == "paren_arabic":
            match = re.match(r"\s*[（(]\s*\d{1,3}\s*[）)]", text)
        elif style == "paren_chinese":
            match = re.match(rf"\s*[（(]\s*[{CHINESE_NUM}]+\s*[）)]", text)
        else:
            match = None
        if match:
            return match
    return None


def _family_example_matches(title: str, family: HeadingFamily) -> bool:
    compact = re.sub(r"\s+", "", title.strip())
    return bool(compact) and compact in {re.sub(r"\s+", "", example.strip()) for example in family.examples}


def _family_outline_marker_allowed(title: str, family: HeadingFamily) -> bool:
    marker = _outline_marker(title)
    if marker is None:
        return False
    marker_family, _ = marker
    style_map = {
        "alpha_outline": "alpha",
        "chinese_outline": "chinese",
        "compact_chinese_outline": "chinese",
        "paren_chinese": "paren_chinese",
        "arabic_outline": "arabic",
        "paren_arabic": "paren_arabic",
        "circled": "circled",
    }
    return style_map.get(marker_family) in set(family.ordinal_styles)


def _family_matches(title: str, family: HeadingFamily) -> bool:
    stripped = title.strip()
    if not family.enabled or not stripped:
        return False
    if _family_example_matches(stripped, family):
        return True
    if not family.anchors and family.kind == "major_section" and family.ordinal_styles:
        marker = _outline_marker(stripped)
        return marker is not None and marker[0] != "compact_chinese_outline" and _family_outline_marker_allowed(stripped, family)
    if not family.anchors and family.kind in {"block", "item"} and family.ordinal_styles:
        return _family_outline_marker_allowed(stripped, family)
    if not family.anchors and family.kind == "outline":
        return _family_outline_marker_allowed(stripped, family)

    for anchor in family.anchors:
        if family.anchor_position == "exact":
            if stripped == anchor:
                return True
            continue

        rest = ""
        if stripped.startswith(anchor):
            rest = stripped[len(anchor):]
        elif family.kind == "major_section" and re.match(r"^[A-Z]" + re.escape(anchor), stripped):
            rest = stripped[len(anchor) + 1 :]
        else:
            continue

        if family.kind == "major_section" and not rest.strip():
            return True

        if family.ordinal_required:
            ordinal_match = _match_family_ordinal(rest, list(family.ordinal_styles))
            if not ordinal_match:
                continue
            rest = rest[ordinal_match.end():]
        elif family.ordinal_styles:
            ordinal_match = _match_family_ordinal(rest, list(family.ordinal_styles))
            if ordinal_match:
                rest = rest[ordinal_match.end():]

        if family.units:
            rest = rest.lstrip()
            matched_unit = False
            for unit in family.units:
                if rest.startswith(unit):
                    rest = rest[len(unit):]
                    matched_unit = True
                    break
            if not matched_unit:
                continue

        if family.separators:
            for separator in sorted(family.separators, key=len, reverse=True):
                if separator and rest.startswith(separator):
                    rest = rest[len(separator):]
                    break
        rest = rest.strip()
        if family.title_required and not rest:
            continue
        return True
    return False


def _family_parent_level(family: HeadingFamily, outline_stack: list[OutlineFrame]) -> int | None:
    parent_hints = set(family.parent_hints)
    if not parent_hints:
        return None
    for frame in reversed(outline_stack):
        if frame.family in parent_hints:
            return frame.level
    return None


def _family_suggested_level(
    title: str,
    family: HeadingFamily,
    *,
    latest_main_level: int | None,
    outline_stack: list[OutlineFrame],
) -> tuple[int, str]:
    parent_level = _family_parent_level(family, outline_stack)
    strong_level = _local_strong_boundary_level(title)
    if family.kind == "strong_boundary":
        return strong_level or 2, "main"
    if family.kind == "major_section":
        if parent_level is not None:
            return min(parent_level + 1, 6), "main"
        return min(max((latest_main_level or 1) + 1, 2), 3), "main"
    if family.kind == "block":
        if parent_level is not None:
            return min(parent_level + 1, 6), "main"
        return min(max((latest_main_level or 2) + 1, 3), 4), "main"
    if family.kind == "item":
        if parent_level is not None:
            return min(parent_level + 1, 6), "subsection"
        return min(max((latest_main_level or 3) + 1, 4), 5), "subsection"
    if family.kind == "outline":
        if parent_level is not None:
            return min(parent_level + 1, 6), "subsection"
        marker = _outline_marker(title)
        if marker and marker[0] in {"chinese_outline", "compact_chinese_outline"}:
            return min(max((latest_main_level or 2) + 1, 3), 4), "subsection"
        return min(max((latest_main_level or 3) + 1, 4), 5), "subsection"
    return 3, "subsection"


def _outline_sequence_required(family: HeadingFamily) -> bool:
    return family.kind == "outline" and not family.anchors and "circled" in family.ordinal_styles


def _outline_sequence_allowed_lines(lines: list[str], families: list[HeadingFamily]) -> dict[str, set[int]]:
    sequence_families = [family for family in families if family.enabled and _outline_sequence_required(family)]
    if not sequence_families:
        return {}

    candidates: dict[str, list[tuple[int, int]]] = {family.id: [] for family in sequence_families}
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    in_html_table = False
    for line_no, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
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
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula):
            continue

        existing_heading = _parse_existing_heading(stripped)
        candidate = existing_heading[1] if existing_heading else stripped
        if _pseudo_heading_to_local_label(candidate) is not None:
            continue
        if _body_like_heading_to_label(candidate) is not None:
            continue
        if _looks_like_sentence_fragment_heading(candidate):
            continue
        if not _eligible_plain_line(candidate):
            continue
        marker = _outline_marker(candidate)
        if marker is None or marker[1] is None:
            continue
        for family in sequence_families:
            if _family_matches(candidate, family):
                if _outline_candidate_is_body_text(candidate, family):
                    continue
                candidates[family.id].append((line_no, marker[1]))

    allowed: dict[str, set[int]] = {family.id: set() for family in sequence_families}
    for family_id, family_candidates in candidates.items():
        for index, (line_no, ordinal) in enumerate(family_candidates):
            previous_ordinal = family_candidates[index - 1][1] if index > 0 else None
            next_ordinal = family_candidates[index + 1][1] if index + 1 < len(family_candidates) else None
            if previous_ordinal is not None and ordinal == previous_ordinal + 1:
                allowed[family_id].add(line_no)
            if next_ordinal is not None and next_ordinal == ordinal + 1:
                allowed[family_id].add(line_no)
    return allowed


def _match_heading_family(
    title: str,
    active_families: list[HeadingFamily],
    *,
    line_no: int | None = None,
    outline_sequence_allowed: dict[str, set[int]] | None = None,
    document_type: str | None = None,
) -> HeadingFamily | None:
    sequence_allowed = outline_sequence_allowed or {}
    for family in active_families:
        if not _family_matches(title, family):
            continue
        if _outline_candidate_is_body_text(title, family, document_type=document_type):
            continue
        if _outline_sequence_required(family) and line_no is not None:
            if line_no not in sequence_allowed.get(family.id, set()):
                continue
        return family
    return None


def _record_heading_match(
    *,
    line_no: int,
    raw: str,
    converted: str,
    rule_name: str,
    role: str,
    main_matches: list[dict[str, Any]],
    subsection_matches: list[dict[str, Any]],
) -> None:
    record = {
        "line_no": line_no,
        "raw": raw,
        "converted": converted,
        "rule": rule_name,
        "confidence": 0.94 if role == "main" else 0.86,
    }
    if role == "main":
        main_matches.append(record)
    else:
        subsection_matches.append(record)


def _label_ordinal_re(aliases: list[str], requires_colon: bool) -> re.Pattern[str]:
    safe_aliases = aliases or DEFAULT_MAIN_ALIASES
    alias_pattern = "|".join(re.escape(alias) for alias in sorted(safe_aliases, key=len, reverse=True))
    sep = r"[:：]" if requires_colon else r"[:：、.]?"
    return re.compile(rf"^(?:{alias_pattern})\s*([{CHINESE_NUM}\d]+)\s*{sep}\s*\S+")


def _main_matcher(rule: MainSectionRule):
    marker_type = rule.marker_type
    if marker_type == "label_ordinal":
        pattern = _label_ordinal_re(rule.aliases, rule.requires_colon)
        return lambda text: bool(pattern.match(text))
    if marker_type == "chinese_outline":
        pattern = re.compile(rf"^[{CHINESE_NUM}]+、\s*\S+")
        return lambda text: bool(pattern.match(text))
    if marker_type == "arabic_outline":
        pattern = re.compile(r"^\d{1,2}[.、]\s+\S+")
        return lambda text: bool(pattern.match(text))
    if marker_type == "decimal_outline":
        pattern = re.compile(r"^\d+(?:\.\d+)+\s+\S+")
        return lambda text: bool(pattern.match(text))
    if marker_type == "chapter":
        pattern = re.compile(rf"^第\s*[{CHINESE_NUM}\d]+\s*[篇章节部分]\s*\S+")
        return lambda text: bool(pattern.match(text))
    return lambda text: False


def _token_pattern(token: PatternToken) -> str:
    if token.type in {"literal", "separator"}:
        values = sorted(token.values, key=len, reverse=True)
        pattern = "(?:" + "|".join(re.escape(value) for value in values) + ")"
    elif token.type == "ordinal":
        choices: list[str] = []
        if "chinese" in token.styles:
            choices.append(rf"[{CHINESE_NUM}]+")
        if "arabic" in token.styles:
            choices.append(r"\d+")
        if "decimal" in token.styles:
            choices.append(r"\d+(?:\.\d+)+")
        pattern = "(?:" + "|".join(choices) + ")"
    elif token.type == "whitespace":
        return r"\s*" if token.optional else r"\s+"
    elif token.type == "title_text":
        remainder_min = max(token.min_chars - 1, 0)
        remainder_max = max(token.max_chars - 1, 0)
        pattern = rf"\S.{{{remainder_min},{remainder_max}}}"
    else:  # guarded by the schema enum
        raise ValueError(f"unsupported pattern token: {token.type}")
    return f"(?:{pattern})?" if token.optional else pattern


def _heading_rule_matcher(rule: HeadingRule) -> re.Pattern[str]:
    return re.compile("^" + "".join(_token_pattern(token) for token in rule.pattern) + "$")


def _eligible_plain_line(stripped: str) -> bool:
    if not stripped or len(stripped) > 120:
        return False
    if MARKDOWN_HEADING_RE.match(stripped):
        return False
    if TOC_DOT_LEADER_RE.search(stripped):
        return False
    if any(mark in stripped for mark in SENTENCE_PUNCTUATION):
        return False
    if "." in stripped and len(stripped) > 48:
        return False
    return True


def _count_main_matches(lines: list[str], strategy: CleaningStrategy) -> int:
    rule = strategy.main_section_rule
    if not rule.enabled or rule.marker_type in {"none", "existing_markdown"}:
        return 0
    matches = 0
    matcher = _main_matcher(rule)
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    in_html_table = False
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
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
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula):
            continue
        existing_heading = _parse_existing_heading(stripped)
        candidate = existing_heading[1] if existing_heading else stripped
        if _pseudo_heading_to_local_label(candidate) is not None:
            continue
        if _body_like_heading_to_label(candidate) is not None:
            continue
        if _looks_like_sentence_fragment_heading(candidate):
            continue
        if _eligible_plain_line(candidate) and matcher(candidate):
            matches += 1
    return matches


def _count_heading_rule_matches(
    lines: list[str],
    rules: list[HeadingRule],
) -> tuple[dict[str, int], dict[str, re.Pattern[str]]]:
    matchers = {rule.id: _heading_rule_matcher(rule) for rule in rules if rule.enabled}
    counts = {rule.id: 0 for rule in rules if rule.enabled}
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    in_html_table = False
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
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
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula):
            continue
        existing_heading = _parse_existing_heading(stripped)
        candidate = existing_heading[1] if existing_heading else stripped
        if _pseudo_heading_to_local_label(candidate) is not None:
            continue
        if _body_like_heading_to_label(candidate) is not None:
            continue
        if _looks_like_sentence_fragment_heading(candidate):
            continue
        if not _eligible_plain_line(candidate):
            continue
        for rule in rules:
            if not rule.enabled:
                continue
            if _is_broad_title_text_rule(rule) and not _broad_title_text_rule_allows(candidate, rule):
                continue
            if matchers[rule.id].match(candidate):
                counts[rule.id] += 1
    return counts, matchers


def _count_heading_family_matches(
    lines: list[str],
    families: list[HeadingFamily],
    *,
    outline_sequence_allowed: dict[str, set[int]] | None = None,
    document_type: str | None = None,
) -> dict[str, int]:
    active_families = [family for family in families if family.enabled]
    sequence_allowed = outline_sequence_allowed or {}
    counts = {family.id: 0 for family in active_families}
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    in_html_table = False
    for line_no, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
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
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula):
            continue
        existing_heading = _parse_existing_heading(stripped)
        candidate = existing_heading[1] if existing_heading else stripped
        if _pseudo_heading_to_local_label(candidate) is not None:
            continue
        matched_any_family = False
        for family in active_families:
            if not _family_matches(candidate, family):
                continue
            if _outline_candidate_is_body_text(candidate, family, document_type=document_type):
                continue
            if _outline_sequence_required(family) and line_no not in sequence_allowed.get(family.id, set()):
                continue
            counts[family.id] += 1
            matched_any_family = True
        if matched_any_family:
            continue
        if _body_like_heading_to_label(candidate) is not None:
            continue
        if existing_heading is None and document_type != "exercise_notes":
            if _looks_like_sentence_fragment_heading(candidate):
                continue
            if not _eligible_plain_line(candidate):
                continue
    return counts


def _heading_family_sort_key(family: HeadingFamily) -> tuple[int, int, str]:
    kind_rank = {
        "strong_boundary": 0,
        "major_section": 1,
        "block": 2,
        "outline": 3,
        "item": 4,
    }
    longest_anchor = max((len(anchor) for anchor in family.anchors), default=0)
    return kind_rank.get(family.kind, 9), -longest_anchor, family.id


def _subsection_aliases(strategy: CleaningStrategy) -> dict[str, int]:
    aliases: dict[str, int] = {}
    for rule in strategy.subsection_rules:
        if not rule.enabled or rule.type != "fixed_label":
            continue
        for alias in rule.aliases:
            aliases[alias.strip()] = rule.target_level
    return aliases


def _normalize_blank_lines(lines: list[str]) -> list[str]:
    normalized: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            normalized.append(line)
            continue
        blank_count += 1
        if blank_count <= 2:
            normalized.append("")
    while normalized and normalized[-1] == "":
        normalized.pop()
    return normalized


def _normalize_setext_headings(lines: list[str]) -> tuple[list[str], int]:
    normalized: list[str] = []
    converted = 0
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_code:
                in_code = True
                fence_marker = marker
            elif fence_marker == marker:
                in_code = False
                fence_marker = None
            normalized.append(line)
            i += 1
            continue
        if in_code:
            normalized.append(line)
            i += 1
            continue
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            normalized.append(line)
            i += 1
            continue
        if (
            not in_formula
            and stripped
            and not _line_is_protected(stripped, in_formula_block=False)
            and not MARKDOWN_HEADING_RE.match(stripped)
            and i + 1 < len(lines)
        ):
            next_stripped = lines[i + 1].strip()
            if SETEXT_H1_RE.match(next_stripped):
                normalized.append(f"# {stripped}")
                converted += 1
                i += 2
                continue
            if SETEXT_H2_RE.match(next_stripped) and not TABLE_SEPARATOR_RE.match(next_stripped):
                normalized.append(f"## {stripped}")
                converted += 1
                i += 2
                continue
        normalized.append(line)
        i += 1
    return normalized, converted


FRONT_ZONE_MIN_CONFIDENCE = 0.65


def _front_zone_limit(line_count: int) -> int:
    return min(line_count, max(300, min(800, int(line_count * 0.25) if line_count else 0)))


def _coerce_document_zones(document_zones: DocumentZones | dict[str, Any] | None) -> DocumentZones:
    if isinstance(document_zones, DocumentZones):
        return document_zones
    if isinstance(document_zones, dict):
        return DocumentZones.model_validate(document_zones)
    return DocumentZones()


def _validated_front_matter_zones(document_zones: DocumentZones, line_count: int) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    zones: list[dict[str, Any]] = []
    max_end_line = _front_zone_limit(line_count)
    for zone in document_zones.front_matter_zones:
        if zone.confidence < FRONT_ZONE_MIN_CONFIDENCE:
            warnings.append("front_matter_zone_skipped_low_confidence")
            continue
        start_line = max(1, int(zone.start_line))
        end_line = min(int(zone.end_line), line_count)
        if end_line < start_line:
            warnings.append("front_matter_zone_skipped_invalid_range")
            continue
        if start_line > max_end_line or end_line > max_end_line:
            warnings.append("front_matter_zone_skipped_outside_front_window")
            continue
        if end_line - start_line + 1 > 800:
            warnings.append("front_matter_zone_skipped_too_large")
            continue
        zones.append(
            {
                "type": zone.type,
                "start_line": start_line,
                "end_line": end_line,
                "title": zone.title,
                "action": zone.action,
                "chunk_policy": zone.chunk_policy,
                "confidence": zone.confidence,
                "signals": list(zone.signals),
            }
        )
    zones.sort(key=lambda item: (item["start_line"], item["end_line"]))
    merged: list[dict[str, Any]] = []
    for zone in zones:
        if not merged or zone["start_line"] > merged[-1]["end_line"] + 1:
            merged.append(zone)
            continue
        previous = merged[-1]
        previous["end_line"] = max(previous["end_line"], zone["end_line"])
        previous["confidence"] = max(previous["confidence"], zone["confidence"])
        previous["signals"] = sorted(set(previous.get("signals", []) + zone.get("signals", [])))
        if previous["type"] != "catalog_or_navigation" and zone["type"] == "catalog_or_navigation":
            previous["type"] = zone["type"]
            previous["chunk_policy"] = zone["chunk_policy"]
            previous["title"] = zone.get("title") or previous.get("title", "")
    return merged, warnings


def _front_zone_for_line(line_no: int, zones: list[dict[str, Any]]) -> dict[str, Any] | None:
    for zone in zones:
        if zone["start_line"] <= line_no <= zone["end_line"]:
            return zone
    return None


def clean_with_strategy(
    raw_markdown: str,
    strategy: CleaningStrategy,
    *,
    source_name: str | None = None,
    document_zones: DocumentZones | dict[str, Any] | None = None,
) -> StrategyCleanResult:
    cleanup = strategy.cleanup_rules
    text = raw_markdown.replace("\r\n", "\n").replace("\r", "\n")
    if cleanup.remove_control_chars:
        text = CONTROL_CHARS_RE.sub("", text)
    lines = text.splitlines()
    lines, setext_converted = _normalize_setext_headings(lines)
    warnings: list[str] = []
    zones_config = _coerce_document_zones(document_zones)
    front_matter_zones, zone_warnings = _validated_front_matter_zones(zones_config, len(lines))
    warnings.extend(zone_warnings)
    document_type = strategy.document_profile.document_type
    use_heading_families = bool(strategy.heading_families)
    use_heading_rules = bool(strategy.heading_rules) and not use_heading_families
    heading_family_counts: dict[str, int] = {}
    heading_family_sequence_allowed: dict[str, set[int]] = {}
    active_heading_families: list[HeadingFamily] = []
    heading_rule_counts: dict[str, int] = {}
    heading_rule_matchers: dict[str, re.Pattern[str]] = {}
    active_heading_rules: list[HeadingRule] = []
    if use_heading_families:
        heading_family_sequence_allowed = _outline_sequence_allowed_lines(lines, strategy.heading_families)
        heading_family_counts = _count_heading_family_matches(
            lines,
            strategy.heading_families,
            outline_sequence_allowed=heading_family_sequence_allowed,
            document_type=document_type,
        )
        active_heading_families = sorted(
            [
                family
                for family in strategy.heading_families
                if family.enabled and heading_family_counts.get(family.id, 0) >= family.min_repeats
            ],
            key=_heading_family_sort_key,
        )
        for family in strategy.heading_families:
            if family.enabled and heading_family_counts.get(family.id, 0) == 0:
                warnings.append(f"strategy_family_not_matched:{family.id}")
        if strategy.heading_families and not active_heading_families:
            warnings.append("heading_family_matches_below_threshold")
        main_enabled = bool(active_heading_families)
        main_matcher = lambda text: False
    elif use_heading_rules:
        heading_rule_counts, heading_rule_matchers = _count_heading_rule_matches(lines, strategy.heading_rules)
        active_heading_rules = sorted(
            [
                rule
                for rule in strategy.heading_rules
                if rule.enabled and heading_rule_counts.get(rule.id, 0) >= rule.min_repeats
            ],
            key=lambda rule: (-rule.priority, rule.target_level),
        )
        for rule in strategy.heading_rules:
            if rule.enabled and heading_rule_counts.get(rule.id, 0) == 0:
                warnings.append(f"strategy_rule_not_matched:{rule.id}")
        main_rules = [rule for rule in strategy.heading_rules if rule.enabled and rule.role == "main"]
        main_enabled = any(rule.role == "main" for rule in active_heading_rules)
        if main_rules and not main_enabled:
            warnings.append("main_section_matches_below_threshold")
        main_matcher = lambda text: False
    else:
        main_matches_total = _count_main_matches(lines, strategy)
        main_enabled = (
            strategy.main_section_rule.enabled
            and strategy.main_section_rule.marker_type not in {"none", "existing_markdown"}
            and main_matches_total >= strategy.fallback_policy.if_main_sections_less_than
            and main_matches_total >= strategy.main_section_rule.min_repeats
        )
        if strategy.main_section_rule.enabled and not main_enabled and strategy.main_section_rule.marker_type not in {"none", "existing_markdown"}:
            warnings.append("main_section_matches_below_threshold")
        main_matcher = _main_matcher(strategy.main_section_rule)

    subsection_aliases = _subsection_aliases(strategy)
    active_rule_ids = {rule.id for rule in active_heading_rules}
    existing_heading_title_counts: dict[str, int] = {}
    for raw_line in lines:
        parsed_heading = _parse_existing_heading(raw_line.strip())
        if parsed_heading:
            existing_heading_title_counts[parsed_heading[1]] = existing_heading_title_counts.get(parsed_heading[1], 0) + 1
    output: list[str] = []
    main_matches: list[dict[str, Any]] = []
    subsection_matches: list[dict[str, Any]] = []
    local_label_matches: list[dict[str, Any]] = []
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    in_html_table = False
    seen_rule_ids: set[str] = set()
    latest_rule_levels: dict[str, int] = {}
    latest_main_level: int | None = None
    outline_stack: list[OutlineFrame] = []

    for index, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if _front_zone_for_line(index, front_matter_zones) is not None:
            output.append(raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line)
            continue
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_code:
                in_code = True
                fence_marker = marker
            elif fence_marker == marker:
                in_code = False
                fence_marker = None
            output.append(raw_line)
            continue
        if in_code:
            output.append(raw_line)
            continue

        if in_html_table:
            output.append(raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line)
            if HTML_TABLE_END_RE.search(stripped):
                in_html_table = False
            continue
        if HTML_TABLE_START_RE.search(stripped):
            output.append(raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line)
            if not HTML_TABLE_END_RE.search(stripped):
                in_html_table = True
            continue

        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            output.append(raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line)
            continue

        line = raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line
        stripped = line.strip()

        existing_heading = _parse_existing_heading(stripped)
        if existing_heading and not in_formula:
            current_level, title = existing_heading
            pseudo_label = _pseudo_heading_to_local_label(title)
            if pseudo_label is not None:
                output.append(pseudo_label)
                local_label_matches.append(
                    {
                        "line_no": index,
                        "raw": stripped,
                        "converted": pseudo_label,
                        "rule": "existing_markdown:metadata_or_badge_to_local_label",
                        "confidence": 0.9,
                    }
                )
                _append_warning_once(warnings, "metadata_heading_demoted_to_label")
                continue

            qwen_family_pre_match = None
            if use_heading_families:
                qwen_family_pre_match = _match_heading_family(
                    _split_trailing_heading_metadata(title)[0],
                    active_heading_families,
                    line_no=index,
                    outline_sequence_allowed=heading_family_sequence_allowed,
                    document_type=document_type,
                )

            if qwen_family_pre_match is None:
                local_label = _body_like_heading_to_label(title)
                if local_label is not None:
                    output.append(local_label)
                    local_label_matches.append(
                        {
                            "line_no": index,
                            "raw": stripped,
                            "converted": local_label,
                            "rule": "body_like_heading_to_local_label",
                            "confidence": 0.9,
                        }
                    )
                    _append_warning_once(warnings, "body_like_heading_demoted_to_label")
                    continue

            if use_heading_families:
                match_title = _split_trailing_heading_metadata(title)[0]
                matched_family = _match_heading_family(
                    match_title,
                    active_heading_families,
                    line_no=index,
                    outline_sequence_allowed=heading_family_sequence_allowed,
                    document_type=document_type,
                )
                local_strong_level = _local_strong_boundary_level(match_title)
                if matched_family is not None or local_strong_level is not None:
                    if matched_family is not None:
                        coerced_level, coerced_role = _family_suggested_level(
                            match_title,
                            matched_family,
                            latest_main_level=latest_main_level,
                            outline_stack=outline_stack,
                        )
                        rule_name = f"existing_markdown:family:{matched_family.id}"
                        frame_family = matched_family.id
                    else:
                        coerced_level, coerced_role = local_strong_level or 2, "main"
                        rule_name = "existing_markdown:local_strong_boundary"
                        frame_family = "local_strong_boundary"
                    coerced_level, coerced_role, _ = _apply_outline_decision(
                        match_title,
                        coerced_level,
                        coerced_role,
                        outline_stack=outline_stack,
                        latest_main_level=latest_main_level,
                        line_no=index,
                        warnings=warnings,
                    )
                    emitted_title, converted = _emit_heading(
                        output=output,
                        title=title,
                        level=coerced_level,
                        raw=stripped,
                        line_no=index,
                        local_label_matches=local_label_matches,
                        warnings=warnings,
                    )
                    _record_heading_match(
                        line_no=index,
                        raw=stripped,
                        converted=converted,
                        rule_name=rule_name,
                        role=coerced_role,
                        main_matches=main_matches,
                        subsection_matches=subsection_matches,
                    )
                    if coerced_role == "main":
                        latest_main_level = coerced_level
                    _remember_heading_in_outline_stack(
                        outline_stack,
                        title=emitted_title,
                        level=coerced_level,
                        family=frame_family,
                        line_no=index,
                    )
                    if coerced_level != current_level:
                        _append_warning_once(warnings, "existing_heading_level_normalized")
                    continue

                if current_level == 1 and index <= 3:
                    converted = _make_heading(title, current_level)
                    output.append(converted)
                    latest_main_level = current_level
                    _remember_heading_in_outline_stack(
                        outline_stack,
                        title=title,
                        level=current_level,
                        family="existing_document_title",
                        line_no=index,
                    )
                    continue

                output.append(title)
                local_label_matches.append(
                    {
                        "line_no": index,
                        "raw": stripped,
                        "converted": title,
                        "rule": "existing_markdown:not_in_heading_family",
                        "confidence": 0.82,
                    }
                )
                _append_warning_once(warnings, "unlisted_existing_heading_demoted_to_plain")
                continue

            if _looks_like_sentence_fragment_heading(title):
                output.append(title)
                local_label_matches.append(
                    {
                        "line_no": index,
                        "raw": stripped,
                        "converted": title,
                        "rule": "existing_markdown:sentence_fragment_to_plain",
                        "confidence": 0.84,
                    }
                )
                _append_warning_once(warnings, "sentence_fragment_heading_demoted_to_plain")
                continue

            matched_rule: HeadingRule | None = None
            if use_heading_rules:
                matched_rule = _match_heading_rule(
                    title,
                    active_heading_rules,
                    heading_rule_matchers,
                    seen_rule_ids,
                    active_rule_ids,
                )
            if matched_rule is not None:
                match_title = _split_trailing_heading_metadata(title)[0]
                coerced_level, coerced_role = _coerce_heading_level(
                    match_title,
                    matched_rule.target_level,
                    rule=matched_rule,
                    latest_rule_levels=latest_rule_levels,
                    latest_main_level=latest_main_level,
                    warnings=warnings,
                )
                coerced_level, coerced_role, outline_family = _apply_outline_decision(
                    match_title,
                    coerced_level,
                    coerced_role,
                    outline_stack=outline_stack,
                    latest_main_level=latest_main_level,
                    line_no=index,
                    warnings=warnings,
                )
                emitted_title, converted = _emit_heading(
                    output=output,
                    title=title,
                    level=coerced_level,
                    raw=stripped,
                    line_no=index,
                    local_label_matches=local_label_matches,
                    warnings=warnings,
                )
                _record_heading_match(
                    line_no=index,
                    raw=stripped,
                    converted=converted,
                    rule_name=f"existing_markdown:{matched_rule.id}",
                    role=coerced_role,
                    main_matches=main_matches,
                    subsection_matches=subsection_matches,
                )
                if coerced_role == "main":
                    latest_main_level = coerced_level
                seen_rule_ids.add(matched_rule.id)
                latest_rule_levels[matched_rule.id] = coerced_level
                _remember_heading_in_outline_stack(
                    outline_stack,
                    title=emitted_title,
                    level=coerced_level,
                    family=outline_family,
                    line_no=index,
                )
                if coerced_level != current_level:
                    _append_warning_once(warnings, "existing_heading_level_normalized")
                continue

            inferred_level, inferred_role, inferred_reason = _infer_existing_heading_level(
                title,
                current_level,
                latest_main_level=latest_main_level,
                title_frequency=existing_heading_title_counts.get(title, 1),
            )
            if _should_demote_unmarked_existing_heading(title, current_level, outline_stack):
                local_level = _nearest_local_outline_level(outline_stack)
                if local_level is not None:
                    inferred_level = min(max(local_level, 3), 5)
                    inferred_role = "subsection"
                    inferred_reason = "unmarked_existing_heading_under_local_outline"
            if inferred_level <= 0:
                converted = title
                output.append(converted)
                local_label_matches.append(
                    {
                        "line_no": index,
                        "raw": stripped,
                        "converted": converted,
                        "rule": f"existing_markdown:{inferred_reason or 'demoted_plain'}",
                        "confidence": 0.78,
                    }
                )
                _append_warning_once(warnings, "untrusted_h1_demoted_to_plain")
                continue

            inferred_level, inferred_role, outline_family = _apply_outline_decision(
                title,
                inferred_level,
                inferred_role,
                outline_stack=outline_stack,
                latest_main_level=latest_main_level,
                line_no=index,
                warnings=warnings,
            )
            emitted_title, converted = _emit_heading(
                output=output,
                title=title,
                level=inferred_level,
                raw=stripped,
                line_no=index,
                local_label_matches=local_label_matches,
                warnings=warnings,
            )
            if inferred_reason is not None or inferred_level != current_level:
                _record_heading_match(
                    line_no=index,
                    raw=stripped,
                    converted=converted,
                    rule_name=f"existing_markdown:{inferred_reason or 'level'}",
                    role=inferred_role,
                    main_matches=main_matches,
                    subsection_matches=subsection_matches,
                )
                _append_warning_once(warnings, "existing_heading_level_normalized")
            if inferred_role == "main":
                latest_main_level = inferred_level
            _remember_heading_in_outline_stack(
                outline_stack,
                title=emitted_title,
                level=inferred_level,
                family=outline_family,
                line_no=index,
            )
            continue

        if _line_is_protected(stripped, in_formula_block=in_formula):
            output.append(line)
            continue

        pseudo_label = _pseudo_heading_to_local_label(stripped)
        if pseudo_label is not None:
            output.append(pseudo_label)
            local_label_matches.append(
                {
                    "line_no": index,
                    "raw": stripped,
                    "converted": pseudo_label,
                    "rule": "plain_line:metadata_or_badge_to_local_label",
                    "confidence": 0.84,
                }
            )
            _append_warning_once(warnings, "metadata_heading_demoted_to_label")
            continue

        qwen_family_pre_match = None
        if use_heading_families:
            qwen_family_pre_match = _match_heading_family(
                _split_trailing_heading_metadata(stripped)[0],
                active_heading_families,
                line_no=index,
                outline_sequence_allowed=heading_family_sequence_allowed,
                document_type=document_type,
            )

        allow_exercise_family_candidate = document_type == "exercise_notes" and use_heading_families

        if (
            qwen_family_pre_match is None
            and _looks_like_sentence_fragment_heading(stripped)
            and not allow_exercise_family_candidate
        ):
            output.append(line)
            continue

        if qwen_family_pre_match is None:
            local_label = _body_like_heading_to_label(stripped)
            if local_label is not None:
                output.append(local_label)
                local_label_matches.append(
                    {
                        "line_no": index,
                        "raw": stripped,
                        "converted": local_label,
                        "rule": "body_like_plain_line_to_local_label",
                        "confidence": 0.86,
                    }
                )
                _append_warning_once(warnings, "body_like_heading_demoted_to_label")
                continue

        if not _eligible_plain_line(stripped) and not allow_exercise_family_candidate:
            output.append(line)
            continue

        if use_heading_families:
            match_title = _split_trailing_heading_metadata(stripped)[0]
            matched_family = _match_heading_family(
                match_title,
                active_heading_families,
                line_no=index,
                outline_sequence_allowed=heading_family_sequence_allowed,
                document_type=document_type,
            )
            local_strong_level = _local_strong_boundary_level(match_title)
            if matched_family is not None or local_strong_level is not None:
                if matched_family is not None:
                    coerced_level, coerced_role = _family_suggested_level(
                        match_title,
                        matched_family,
                        latest_main_level=latest_main_level,
                        outline_stack=outline_stack,
                    )
                    rule_name = f"family:{matched_family.id}"
                    frame_family = matched_family.id
                else:
                    coerced_level, coerced_role = local_strong_level or 2, "main"
                    rule_name = "local_strong_boundary"
                    frame_family = "local_strong_boundary"
                coerced_level, coerced_role, _ = _apply_outline_decision(
                    match_title,
                    coerced_level,
                    coerced_role,
                    outline_stack=outline_stack,
                    latest_main_level=latest_main_level,
                    line_no=index,
                    warnings=warnings,
                )
                emitted_title, converted = _emit_heading(
                    output=output,
                    title=stripped,
                    level=coerced_level,
                    raw=stripped,
                    line_no=index,
                    local_label_matches=local_label_matches,
                    warnings=warnings,
                )
                _record_heading_match(
                    line_no=index,
                    raw=stripped,
                    converted=converted,
                    rule_name=rule_name,
                    role=coerced_role,
                    main_matches=main_matches,
                    subsection_matches=subsection_matches,
                )
                if coerced_role == "main":
                    latest_main_level = coerced_level
                _remember_heading_in_outline_stack(
                    outline_stack,
                    title=emitted_title,
                    level=coerced_level,
                    family=frame_family,
                    line_no=index,
                )
                continue

        if use_heading_rules:
            matched_rule: HeadingRule | None = None
            match_title = _split_trailing_heading_metadata(stripped)[0]
            matched_rule = _match_heading_rule(
                match_title,
                active_heading_rules,
                heading_rule_matchers,
                seen_rule_ids,
                active_rule_ids,
            )
            if matched_rule is not None:
                coerced_level, coerced_role = _coerce_heading_level(
                    match_title,
                    matched_rule.target_level,
                    rule=matched_rule,
                    latest_rule_levels=latest_rule_levels,
                    latest_main_level=latest_main_level,
                    warnings=warnings,
                )
                coerced_level, coerced_role, outline_family = _apply_outline_decision(
                    match_title,
                    coerced_level,
                    coerced_role,
                    outline_stack=outline_stack,
                    latest_main_level=latest_main_level,
                    line_no=index,
                    warnings=warnings,
                )
                emitted_title, converted = _emit_heading(
                    output=output,
                    title=stripped,
                    level=coerced_level,
                    raw=stripped,
                    line_no=index,
                    local_label_matches=local_label_matches,
                    warnings=warnings,
                )
                match_record = {
                    "line_no": index,
                    "raw": stripped,
                    "converted": converted,
                    "rule": matched_rule.id,
                    "confidence": 0.94 if coerced_role == "main" else 0.86,
                }
                if coerced_role == "main":
                    main_matches.append(match_record)
                    latest_main_level = coerced_level
                else:
                    subsection_matches.append(match_record)
                seen_rule_ids.add(matched_rule.id)
                latest_rule_levels[matched_rule.id] = coerced_level
                _remember_heading_in_outline_stack(
                    outline_stack,
                    title=emitted_title,
                    level=coerced_level,
                    family=outline_family,
                    line_no=index,
                )
                continue

        match_title = _split_trailing_heading_metadata(stripped)[0]
        if not use_heading_rules and main_enabled and main_matcher(match_title):
            coerced_level, _ = _coerce_heading_level(
                match_title,
                strategy.main_section_rule.target_level,
                rule=None,
                latest_rule_levels=latest_rule_levels,
                latest_main_level=latest_main_level,
                warnings=warnings,
            )
            emitted_title, converted = _emit_heading(
                output=output,
                title=stripped,
                level=coerced_level,
                raw=stripped,
                line_no=index,
                local_label_matches=local_label_matches,
                warnings=warnings,
            )
            main_matches.append(
                {
                    "line_no": index,
                    "raw": stripped,
                    "converted": converted,
                    "rule": strategy.main_section_rule.marker_type,
                    "confidence": 0.94,
                }
            )
            latest_main_level = coerced_level
            _remember_heading_in_outline_stack(
                outline_stack,
                title=emitted_title,
                level=coerced_level,
                family=None,
                line_no=index,
            )
            continue

        subsection_level = None if use_heading_rules else subsection_aliases.get(stripped)
        if subsection_level is not None:
            coerced_level, _ = _coerce_heading_level(
                stripped,
                subsection_level,
                rule=None,
                latest_rule_levels=latest_rule_levels,
                latest_main_level=latest_main_level,
                warnings=warnings,
            )
            converted = _make_heading(stripped, coerced_level)
            output.append(converted)
            subsection_matches.append(
                {
                    "line_no": index,
                    "raw": stripped,
                    "converted": converted,
                    "rule": "fixed_label",
                    "confidence": 0.82,
                }
            )
            _remember_heading_in_outline_stack(
                outline_stack,
                title=stripped,
                level=coerced_level,
                family=None,
                line_no=index,
            )
            continue

        output.append(line)

    if cleanup.normalize_blank_lines:
        output = _normalize_blank_lines(output)
    cleaned = "\n".join(output).strip() + "\n"
    converted_count = len(main_matches) + len(subsection_matches)
    untrusted_heading_demotions = sum(
        1 for record in local_label_matches if str(record.get("rule", "")).startswith("existing_markdown:")
    )
    parse_report = {
        "source_name": source_name,
        "strategy_source": strategy.strategy_source,
        "qwen_model": "qwen3.6-plus-2026-04-02",
        "document_profile": strategy.document_profile.model_dump(mode="json"),
        "stats": {
            "line_count": len(lines),
            "char_count": len(text),
            "main_sections_detected": len(main_matches),
            "subsections_detected": len(subsection_matches),
            "existing_markdown_headings": sum(1 for line in lines if MARKDOWN_HEADING_RE.match(line.strip())),
            "converted_headings": converted_count,
            "local_labels_demoted": len(local_label_matches) - untrusted_heading_demotions,
            "untrusted_headings_demoted": untrusted_heading_demotions,
            "setext_headings_converted": setext_converted,
            "warnings_count": len(warnings),
            "configured_heading_rules": len(strategy.heading_rules),
            "active_heading_rules": len(active_heading_rules),
            "configured_heading_families": len(strategy.heading_families),
            "active_heading_families": len(active_heading_families),
            "front_matter_zone_count": len(front_matter_zones),
            "front_matter_lines_preserved_unprocessed": sum(
                zone["end_line"] - zone["start_line"] + 1 for zone in front_matter_zones
            ),
        },
        "document_zones": {
            "front_matter_zones_applied": front_matter_zones,
            "body_start_line": zones_config.body_start_line,
            "confidence": zones_config.confidence,
        },
        "main_section_matches": main_matches,
        "subsection_matches": subsection_matches,
        "local_label_matches": local_label_matches,
        "warnings": [{"message": warning} for warning in warnings],
        "rule_execution": {
            "candidate_counts": heading_rule_counts,
            "active_rule_ids": [rule.id for rule in active_heading_rules],
            "family_candidate_counts": heading_family_counts,
            "active_family_ids": [family.id for family in active_heading_families],
            "outline_sequence_allowed_counts": {
                family_id: len(line_numbers)
                for family_id, line_numbers in heading_family_sequence_allowed.items()
            },
        },
        "fallback_used": (
            not main_enabled
            and (
                bool(strategy.heading_families)
                if use_heading_families
                else (
                    any(rule.enabled and rule.role == "main" for rule in strategy.heading_rules)
                    if use_heading_rules
                    else strategy.main_section_rule.marker_type not in {"none", "existing_markdown"}
                )
            )
        ),
    }
    return StrategyCleanResult(
        cleaned_markdown=cleaned,
        strategy=strategy.to_dict(),
        parse_report=parse_report,
        warnings=warnings,
    )
