"""
materials/postprocess/formula_cleaner.py — 公式文本轻度修复。

只处理高置信度的 LaTeX/OCR 噪声，默认不做数学语义改写。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable


MAX_SAMPLES_PER_RULE = 8
MAX_CHANGE_RECORDS = 80

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
IMAGE_RE = re.compile(r"^\s*!\[[^\]]*]\([^)]+\)\s*$")
BACKTICK_RE = re.compile(r"`+")

TEXTCIRCLED_RE = re.compile(r"\\textcircled\s*\{\s*([^{}]+?)\s*\}")
OPERATORNAME_LIM_RE = re.compile(r"\\operatorname\*?\s*\{\s*l\s*i\s*m\s*\}")
SP_RE = re.compile(r"\\sp\s*(\{[^{}\n]*\})")
DISPLAYLIMITS_RE = re.compile(r"\\displaylimits\b")
TEXTMU_RE = re.compile(r"\\textmu\b")
INVALID_HASH_TAG_RE = re.compile(r"\\tag\{#-?\d*\}")
FORMULA_LAYOUT_COMMAND_RE = re.compile(r"\\(?:hfill|medskip)\b")
MATHBB_BACKSLASH_RE = re.compile(r"\\mathbb\{\\\}")
OCR_NA_RE = re.compile(r"\\nA\b")
OCR_BACKSLASH_ONE_INTEGRAL_RE = re.compile(r"\\1\b(?=\s*_\s*\{[^{}\n]+\}\s*\^\s*\{[^{}\n]+\})")
LIMIT_INFINITY_RE = re.compile(r"(\\lim\s*_\s*\{\s*)([A-Za-z])\s+\\infty(\s*\})")
LIMIT_RIGHT_DOT_INFINITY_RE = re.compile(r"(\\lim\s*_\s*\{\s*)([A-Za-z])\s*\\right\.\s*\\infty(\s*\})")
BIG_INTEGRAL_RE = re.compile(r"\\Big\s+(\\int\b)")
TEXTBF_EM_SIMPLE_RE = re.compile(r"\\textbf\{\s*\\em\s+(?P<body>[^{}\s]+)\s*\}")
EM_SIMPLE_RE = re.compile(r"\\em\s+(?P<body>[A-Za-z])\b")
MATHRM_SPACED_WORD_RE = re.compile(r"\\mathrm\s*\{\s*(?P<body>(?:[A-Za-z]\s*){2,})\}")
OPERATORNAME_SPACED_WORD_RE = re.compile(r"\\operatorname(?P<star>\*)?\s*\{\s*(?P<body>(?:[A-Za-z]\s*){2,})\}")
OPERATORNAME_STAR_SPACE_RE = re.compile(r"\\operatorname\*\s+\{")
OPERATORNAME_STAR_ARGUMENT_EDGE_SPACE_RE = re.compile(r"\\operatorname\*\{\s*(?P<body>[^{}\n]*?\S)\s*\}")
OPERATORNAME_SINGLE_ROMAN_RE = re.compile(r"\\operatorname\{\s*(?P<body>[ed])\s*\}")
NESTED_STYLE_SINGLE_TOKEN_RE = re.compile(
    r"\\(?P<cmd>mathrm|mathit|mathbf|boldsymbol|textbf|mathcal|mathfrak|mathbb|pmb)"
    r"\{\s*\{\s*(?P<body>[^{}\s]+)\s*\}\s*\}"
)
SIMPLE_FRAC_ARGUMENT_SPACING_RE = re.compile(r"\\frac\{\s*(?P<num>[^{}\n]*?)\s*\}\s+\{\s*(?P<den>[^{}\n]*?)\s*\}")
COMMAND_SPACE_RE = re.compile(
    r"\\(?P<cmd>"
    r"mathbf|boldsymbol|textbf|mathrm|mathit|mathcal|mathfrak|mathbb|pmb|"
    r"sqrt|frac|overline|underline|operatorname"
    r")\s+\{"
)
COMMAND_ARGUMENT_EDGE_SPACE_RE = re.compile(
    r"\\(?P<cmd>"
    r"mathbf|boldsymbol|textbf|mathrm|mathit|mathcal|mathfrak|mathbb|pmb|"
    r"sqrt|frac|overline|underline|operatorname"
    r")\{\s*(?P<body>[^{}\n]*?\S)\s*\}"
)

REPORT_ONLY_PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("operatorname_star_ambiguous", "L3", re.compile(r"\\operatorname\*\s*\{\s*(?:[A-Za-z]|\\cdot)\s*\}")),
    ("atop_legacy_fraction", "L4", re.compile(r"\\atop\b")),
    ("negative_kern", "L4", re.compile(r"\\kern\s*-")),
    ("right_dot_infinity", "L3", re.compile(r"\\right\.\s*\\infty")),
    ("big_integral_spacing", "L3", re.compile(r"\\Big\s+\\int\b")),
    ("array_outer_group_candidate", "L3", re.compile(r"\{\s*\\begin\{array\}")),
)

CIRCLED_NUMBERS = {
    "1": "①",
    "2": "②",
    "3": "③",
    "4": "④",
    "5": "⑤",
    "6": "⑥",
    "7": "⑦",
    "8": "⑧",
    "9": "⑨",
    "10": "⑩",
    "11": "⑪",
    "12": "⑫",
    "13": "⑬",
    "14": "⑭",
    "15": "⑮",
    "16": "⑯",
    "17": "⑰",
    "18": "⑱",
    "19": "⑲",
    "20": "⑳",
    "一": "①",
    "二": "②",
    "三": "③",
    "四": "④",
    "五": "⑤",
    "六": "⑥",
    "七": "⑦",
    "八": "⑧",
    "九": "⑨",
    "十": "⑩",
}

MATHRM_FUNCTIONS = {
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
    "cot": r"\cot",
    "sec": r"\sec",
    "csc": r"\csc",
    "ln": r"\ln",
    "log": r"\log",
}

OPERATOR_FUNCTIONS = {
    "lim": r"\lim",
    "max": r"\max",
    "min": r"\min",
    "sup": r"\sup",
    "inf": r"\inf",
    "dim": r"\dim",
    "det": r"\det",
    "gcd": r"\gcd",
    "log": r"\log",
    "ln": r"\ln",
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
}


@dataclass
class FormulaCleanResult:
    cleaned_markdown: str
    stats: dict[str, Any]
    changes: list[dict[str, Any]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": True,
            "level": self.stats.get("level", "safe"),
            "stats": self.stats,
            "changes": self.changes,
            "warnings": self.warnings,
        }


class _FormulaCleanReporter:
    def __init__(self, level: str) -> None:
        self.stats: dict[str, Any] = {
            "level": level,
            "changed_count": 0,
            "reported_count": 0,
            "rules": {},
        }
        self.changes: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    def _rule(self, rule_id: str, level: str) -> dict[str, Any]:
        rules = self.stats["rules"]
        if rule_id not in rules:
            rules[rule_id] = {
                "level": level,
                "changed": 0,
                "reported": 0,
                "samples": [],
            }
        return rules[rule_id]

    def change(self, rule_id: str, level: str, before: str, after: str, line_no: int) -> None:
        if before == after:
            return
        rule = self._rule(rule_id, level)
        rule["changed"] += 1
        self.stats["changed_count"] += 1
        sample = {"line_no": line_no, "before": before, "after": after}
        if len(rule["samples"]) < MAX_SAMPLES_PER_RULE:
            rule["samples"].append(sample)
        if len(self.changes) < MAX_CHANGE_RECORDS:
            self.changes.append({"rule": rule_id, **sample})

    def report(self, rule_id: str, level: str, sample_text: str, line_no: int, warning: str) -> None:
        rule = self._rule(rule_id, level)
        rule["reported"] += 1
        self.stats["reported_count"] += 1
        sample = {"line_no": line_no, "before": sample_text, "after": None}
        if len(rule["samples"]) < MAX_SAMPLES_PER_RULE:
            rule["samples"].append(sample)
        if warning not in self.warnings:
            self.warnings.append(warning)


def _normalize_level(level: str) -> str:
    normalized = str(level or "safe").strip().lower()
    return normalized if normalized in {"safe", "experimental"} else "safe"


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def _inline_segments(line: str) -> list[tuple[str, bool]]:
    segments: list[tuple[str, bool]] = []
    index = 0
    while index < len(line):
        match = BACKTICK_RE.search(line, index)
        if not match:
            segments.append((line[index:], False))
            break
        if match.start() > index:
            segments.append((line[index:match.start()], False))
        marker = match.group(0)
        end = line.find(marker, match.end())
        if end == -1:
            segments.append((line[match.start():], True))
            break
        segments.append((line[match.start():end + len(marker)], True))
        index = end + len(marker)
    return segments or [(line, False)]


def _replace_with_report(
    text: str,
    pattern: re.Pattern[str],
    rule_id: str,
    level: str,
    line_no: int,
    reporter: _FormulaCleanReporter,
    replacement: str | Callable[[re.Match[str]], str],
) -> str:
    def _callback(match: re.Match[str]) -> str:
        after = replacement(match) if callable(replacement) else match.expand(replacement)
        reporter.change(rule_id, level, match.group(0), after, line_no)
        return after

    return pattern.sub(_callback, text)


def _replace_textcircled(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        value = re.sub(r"\s+", "", match.group(1))
        mapped = CIRCLED_NUMBERS.get(value)
        if mapped is None:
            reporter.report(
                "textcircled_unsupported",
                "L3",
                match.group(0),
                line_no,
                "formula_textcircled_unsupported",
            )
            return match.group(0)
        reporter.change("textcircled_unicode", "L2", match.group(0), mapped, line_no)
        return mapped

    return TEXTCIRCLED_RE.sub(_callback, text)


def _replace_command_spacing(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        after = f"\\{match.group('cmd')}{{"
        reporter.change("command_space_before_brace", "L1", match.group(0), after, line_no)
        return after

    return COMMAND_SPACE_RE.sub(_callback, text)


def _trim_command_argument_edges(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        after = f"\\{match.group('cmd')}{{{match.group('body')}}}"
        reporter.change("command_argument_edge_space", "L1", match.group(0), after, line_no)
        return after

    return COMMAND_ARGUMENT_EDGE_SPACE_RE.sub(_callback, text)


def _collapse_letters(value: str) -> str:
    return re.sub(r"\s+", "", value).lower()


def _replace_mathrm_spaced_functions(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        word = _collapse_letters(match.group("body"))
        mapped = MATHRM_FUNCTIONS.get(word)
        if mapped is None:
            return match.group(0)
        reporter.change("mathrm_spaced_function", "L2", match.group(0), mapped, line_no)
        return mapped

    return MATHRM_SPACED_WORD_RE.sub(_callback, text)


def _replace_operatorname_spaced_letters(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        word = _collapse_letters(match.group("body"))
        mapped = OPERATOR_FUNCTIONS.get(word)
        if mapped is None:
            mapped = f"\\operatorname{{{word}}}"
        reporter.change("operatorname_spaced_letters", "L2", match.group(0), mapped, line_no)
        return mapped

    return OPERATORNAME_SPACED_WORD_RE.sub(_callback, text)


def _replace_operatorname_star_spacing(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _space_callback(match: re.Match[str]) -> str:
        after = r"\operatorname*{"
        reporter.change("operatorname_star_space_before_brace", "L1", match.group(0), after, line_no)
        return after

    def _edge_callback(match: re.Match[str]) -> str:
        after = f"\\operatorname*{{{match.group('body')}}}"
        reporter.change("operatorname_star_argument_edge_space", "L1", match.group(0), after, line_no)
        return after

    text = OPERATORNAME_STAR_SPACE_RE.sub(_space_callback, text)
    return OPERATORNAME_STAR_ARGUMENT_EDGE_SPACE_RE.sub(_edge_callback, text)


def _replace_safe_visual_operator_noise(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _operator_callback(match: re.Match[str]) -> str:
        after = f"\\mathrm{{{match.group('body')}}}"
        reporter.change("operatorname_single_roman_to_mathrm", "L2", match.group(0), after, line_no)
        return after

    def _nested_style_callback(match: re.Match[str]) -> str:
        after = f"\\{match.group('cmd')}{{{match.group('body')}}}"
        reporter.change("nested_style_single_token", "L2", match.group(0), after, line_no)
        return after

    text = OPERATORNAME_SINGLE_ROMAN_RE.sub(_operator_callback, text)
    return NESTED_STYLE_SINGLE_TOKEN_RE.sub(_nested_style_callback, text)


def _replace_legacy_em(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _bold_callback(match: re.Match[str]) -> str:
        after = f"\\boldsymbol{{{match.group('body')}}}"
        reporter.change("textbf_em_to_boldsymbol", "L2", match.group(0), after, line_no)
        return after

    def _simple_callback(match: re.Match[str]) -> str:
        after = f"\\mathit{{{match.group('body')}}}"
        reporter.change("em_to_mathit", "L2", match.group(0), after, line_no)
        return after

    text = TEXTBF_EM_SIMPLE_RE.sub(_bold_callback, text)
    return EM_SIMPLE_RE.sub(_simple_callback, text)


def _replace_simple_frac_argument_spacing(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    def _callback(match: re.Match[str]) -> str:
        after = f"\\frac{{{match.group('num')}}}{{{match.group('den')}}}"
        reporter.change("simple_frac_argument_spacing", "L1", match.group(0), after, line_no)
        return after

    return SIMPLE_FRAC_ARGUMENT_SPACING_RE.sub(_callback, text)


def _replace_safe_render_error_noise(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    text = _replace_with_report(text, INVALID_HASH_TAG_RE, "invalid_hash_tag_removed", "L2", line_no, reporter, "")
    text = _replace_with_report(
        text,
        FORMULA_LAYOUT_COMMAND_RE,
        "formula_layout_command_removed",
        "L2",
        line_no,
        reporter,
        "",
    )
    text = _replace_with_report(text, MATHBB_BACKSLASH_RE, "mathbb_backslash_removed", "L2", line_no, reporter, "")
    text = _replace_with_report(text, OCR_NA_RE, "ocr_nA_to_quad", "L2", line_no, reporter, r"\\quad")
    return _replace_with_report(
        text,
        OCR_BACKSLASH_ONE_INTEGRAL_RE,
        "ocr_backslash_one_to_int",
        "L2",
        line_no,
        reporter,
        r"\\int",
    )


def _report_only_patterns(text: str, line_no: int, reporter: _FormulaCleanReporter) -> None:
    for rule_id, level, pattern in REPORT_ONLY_PATTERNS:
        for match in pattern.finditer(text):
            reporter.report(rule_id, level, match.group(0), line_no, f"formula_report_only:{rule_id}")


def _clean_unprotected_segment(text: str, line_no: int, reporter: _FormulaCleanReporter) -> str:
    _report_only_patterns(text, line_no, reporter)
    text = _replace_textcircled(text, line_no, reporter)
    text = _replace_with_report(text, OPERATORNAME_LIM_RE, "operatorname_lim", "L2", line_no, reporter, r"\\lim")
    text = _replace_with_report(text, SP_RE, "sp_to_superscript", "L2", line_no, reporter, lambda m: "^" + m.group(1))
    text = _replace_with_report(text, DISPLAYLIMITS_RE, "displaylimits_to_limits", "L2", line_no, reporter, r"\\limits")
    text = _replace_with_report(text, TEXTMU_RE, "textmu_to_mu", "L2", line_no, reporter, r"\\mu")
    text = _replace_safe_render_error_noise(text, line_no, reporter)
    text = _replace_with_report(
        text,
        LIMIT_INFINITY_RE,
        "limit_missing_to_infinity",
        "L2",
        line_no,
        reporter,
        lambda m: f"{m.group(1)}{m.group(2)} \\to \\infty{m.group(3)}",
    )
    text = _replace_command_spacing(text, line_no, reporter)
    text = _trim_command_argument_edges(text, line_no, reporter)
    text = _replace_with_report(
        text,
        LIMIT_RIGHT_DOT_INFINITY_RE,
        "limit_right_dot_infinity",
        "L2",
        line_no,
        reporter,
        lambda m: f"{m.group(1)}{m.group(2)} \\to \\infty{m.group(3)}",
    )
    text = _replace_with_report(text, BIG_INTEGRAL_RE, "big_integral_to_integral", "L2", line_no, reporter, r"\\1")
    text = _replace_mathrm_spaced_functions(text, line_no, reporter)
    text = _replace_operatorname_star_spacing(text, line_no, reporter)
    text = _replace_operatorname_spaced_letters(text, line_no, reporter)
    text = _replace_safe_visual_operator_noise(text, line_no, reporter)
    text = _replace_legacy_em(text, line_no, reporter)
    text = _replace_simple_frac_argument_spacing(text, line_no, reporter)
    return text


def clean_formulas_with_report(markdown: str, *, level: str = "safe") -> FormulaCleanResult:
    """
    清洗 Markdown 中高置信度的公式噪声，并返回修改统计。

    safe 级别只执行确定性渲染修复；当前 experimental 级别仅保留接口，
    L3/L4 模式先 report-only，不自动改写。
    """
    normalized_level = _normalize_level(level)
    reporter = _FormulaCleanReporter(normalized_level)
    output: list[str] = []
    in_fence = False
    fence_marker: str | None = None

    for line_no, raw_line in enumerate(markdown.splitlines(keepends=True), start=1):
        line, ending = _split_line_ending(raw_line)
        stripped = line.strip()
        fence_match = FENCE_RE.match(stripped)

        if in_fence:
            output.append(raw_line)
            if fence_match and fence_match.group(1) == fence_marker:
                in_fence = False
                fence_marker = None
            continue

        if fence_match:
            in_fence = True
            fence_marker = fence_match.group(1)
            output.append(raw_line)
            continue

        if TABLE_RE.match(stripped) or IMAGE_RE.match(stripped):
            output.append(raw_line)
            continue

        cleaned_parts: list[str] = []
        for segment, protected in _inline_segments(line):
            if protected:
                cleaned_parts.append(segment)
            else:
                cleaned_parts.append(_clean_unprotected_segment(segment, line_no, reporter))
        output.append("".join(cleaned_parts) + ending)

    return FormulaCleanResult(
        cleaned_markdown="".join(output),
        stats=reporter.stats,
        changes=reporter.changes,
        warnings=reporter.warnings,
    )


def clean_formulas(markdown: str, *, level: str = "safe") -> str:
    """兼容旧调用方：只返回清洗后的 Markdown。"""
    return clean_formulas_with_report(markdown, level=level).cleaned_markdown
