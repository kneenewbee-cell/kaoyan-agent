from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .strategy_schema import CleaningStrategy, HeadingRule, MainSectionRule, PatternToken


CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
MARKDOWN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
IMAGE_RE = re.compile(r"^\s*!\[[^\]]*]\([^)]+\)\s*$")
FORMULA_BOUNDARY_RE = re.compile(r"^\s*(\$\$|\\\[|\\\])\s*$")
INLINE_FORMULA_RE = re.compile(r"\$[^$\n]+\$")
SETEXT_H1_RE = re.compile(r"^\s*=+\s*$")
SETEXT_H2_RE = re.compile(r"^\s*-+\s*$")
TOC_DOT_LEADER_RE = re.compile(r"\.{3,}|…{2,}")
SENTENCE_PUNCTUATION = ("。", "；", "？", "！", ";", "?", "!")

CHINESE_NUM = "零〇一二三四五六七八九十百千万两"
CHAPTER_SUMMARY_RE = re.compile(rf"^(?:第\s*[{CHINESE_NUM}\d]+\s*章\s*)?(?:本章)?(?:小结|总结)$")
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


def _append_warning_once(warnings: list[str], warning: str) -> None:
    if warning not in warnings:
        warnings.append(warning)


def _looks_like_semantic_subsection(line: str, rule: HeadingRule | None = None) -> bool:
    if line in SEMANTIC_SUBSECTION_ALIASES:
        return True
    if rule is None:
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
        if parent_level is not None and level > parent_level + 1:
            level = parent_level + 1
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
        pattern = re.compile(rf"^第\s*[{CHINESE_NUM}\d]+\s*[章节部分]\s*\S+")
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
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula):
            continue
        if _eligible_plain_line(stripped) and matcher(stripped):
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
        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            continue
        if _line_is_protected(stripped, in_formula_block=in_formula) or not _eligible_plain_line(stripped):
            continue
        for rule_id, matcher in matchers.items():
            if matcher.match(stripped):
                counts[rule_id] += 1
    return counts, matchers


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


def clean_with_strategy(
    raw_markdown: str,
    strategy: CleaningStrategy,
    *,
    source_name: str | None = None,
) -> StrategyCleanResult:
    cleanup = strategy.cleanup_rules
    text = raw_markdown.replace("\r\n", "\n").replace("\r", "\n")
    if cleanup.remove_control_chars:
        text = CONTROL_CHARS_RE.sub("", text)
    lines = text.splitlines()
    lines, setext_converted = _normalize_setext_headings(lines)
    warnings: list[str] = []
    use_heading_rules = bool(strategy.heading_rules)
    heading_rule_counts: dict[str, int] = {}
    heading_rule_matchers: dict[str, re.Pattern[str]] = {}
    active_heading_rules: list[HeadingRule] = []
    if use_heading_rules:
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
    output: list[str] = []
    main_matches: list[dict[str, Any]] = []
    subsection_matches: list[dict[str, Any]] = []
    in_code = False
    fence_marker: str | None = None
    in_formula = False
    seen_rule_ids: set[str] = set()
    latest_rule_levels: dict[str, int] = {}
    latest_main_level: int | None = None

    for index, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
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

        if FORMULA_BOUNDARY_RE.match(stripped):
            in_formula = not in_formula
            output.append(raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line)
            continue

        line = raw_line.rstrip() if cleanup.strip_trailing_spaces else raw_line
        stripped = line.strip()
        if _line_is_protected(stripped, in_formula_block=in_formula) or not _eligible_plain_line(stripped):
            output.append(line)
            continue

        if use_heading_rules:
            matched_rule: HeadingRule | None = None
            for rule in active_heading_rules:
                if rule.parent_rule and rule.parent_rule not in seen_rule_ids:
                    continue
                if heading_rule_matchers[rule.id].match(stripped):
                    matched_rule = rule
                    break
            if matched_rule is not None:
                coerced_level, coerced_role = _coerce_heading_level(
                    stripped,
                    matched_rule.target_level,
                    rule=matched_rule,
                    latest_rule_levels=latest_rule_levels,
                    latest_main_level=latest_main_level,
                    warnings=warnings,
                )
                converted = _make_heading(stripped, coerced_level)
                output.append(converted)
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
                continue

        if not use_heading_rules and main_enabled and main_matcher(stripped):
            coerced_level, _ = _coerce_heading_level(
                stripped,
                strategy.main_section_rule.target_level,
                rule=None,
                latest_rule_levels=latest_rule_levels,
                latest_main_level=latest_main_level,
                warnings=warnings,
            )
            converted = _make_heading(stripped, coerced_level)
            output.append(converted)
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
            continue

        output.append(line)

    if cleanup.normalize_blank_lines:
        output = _normalize_blank_lines(output)
    cleaned = "\n".join(output).strip() + "\n"
    converted_count = len(main_matches) + len(subsection_matches)
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
            "setext_headings_converted": setext_converted,
            "warnings_count": len(warnings),
            "configured_heading_rules": len(strategy.heading_rules),
            "active_heading_rules": len(active_heading_rules),
        },
        "main_section_matches": main_matches,
        "subsection_matches": subsection_matches,
        "warnings": [{"message": warning} for warning in warnings],
        "rule_execution": {
            "candidate_counts": heading_rule_counts,
            "active_rule_ids": [rule.id for rule in active_heading_rules],
        },
        "fallback_used": (
            not main_enabled
            and (
                any(rule.enabled and rule.role == "main" for rule in strategy.heading_rules)
                if use_heading_rules
                else strategy.main_section_rule.marker_type not in {"none", "existing_markdown"}
            )
        ),
    }
    return StrategyCleanResult(
        cleaned_markdown=cleaned,
        strategy=strategy.to_dict(),
        parse_report=parse_report,
        warnings=warnings,
    )
