"""Extract formula occurrences with verified Markdown boundaries.

This module is intentionally conservative. It only returns formulas whose
source span can be mapped back to the current Markdown text, and it records
boundary confidence so later LLM repair code can refuse unsafe fragments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Pattern


DEFAULT_RENDER_ISSUE_PATTERNS: tuple[str, ...] = (
    r"\\kern\s*-\s*delimiterspace",
)

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BEGIN_RE = re.compile(r"\\begin\{([^{}]+)\}")
END_RE = re.compile(r"\\end\{([^{}]+)\}")
LEFT_RE = re.compile(r"\\left(?:\.|[^\s{}])")
RIGHT_RE = re.compile(r"\\right(?:\.|[^\s{}])")
FORMULA_CANDIDATE_RE = re.compile(r"\\[A-Za-z]+|\\[{}]|[_^]\s*(?:\{|[A-Za-z0-9])|[=+\-*/]")
FORMULA_LINE_RE = re.compile(r"^[A-Za-z0-9_\\{}^()[\]|+\-*/.,\s=<>:;&]+$")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass(frozen=True)
class FormulaOccurrence:
    occurrence_id: str
    formula: str
    line_start: int
    line_end: int
    start_offset: int
    end_offset: int
    container: str
    markdown_line: str
    heading_path: list[str]
    extract_confidence: str
    completeness_errors: list[str]
    issue: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id,
            "formula": self.formula,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "container": self.container,
            "markdown_line": self.markdown_line,
            "heading_path": list(self.heading_path),
            "extract_confidence": self.extract_confidence,
            "completeness_errors": list(self.completeness_errors),
            "issue": self.issue,
        }


def _compile_patterns(issue_patterns: Iterable[str | Pattern[str]] | None) -> list[Pattern[str]]:
    patterns = issue_patterns if issue_patterns is not None else DEFAULT_RENDER_ISSUE_PATTERNS
    compiled: list[Pattern[str]] = []
    for pattern in patterns:
        compiled.append(pattern if hasattr(pattern, "search") else re.compile(str(pattern)))
    return compiled


def _matching_issue(text: str, patterns: list[Pattern[str]]) -> str | None:
    for pattern in patterns:
        if pattern.search(text):
            return pattern.pattern
    return None


def _is_escaped(text: str, index: int) -> bool:
    count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        count += 1
        cursor -= 1
    return count % 2 == 1


def _find_unescaped(text: str, marker: str, start: int = 0) -> int:
    index = text.find(marker, start)
    while index != -1 and _is_escaped(text, index):
        index = text.find(marker, index + len(marker))
    return index


def split_markdown_table_row(line: str) -> list[tuple[str, int, int]]:
    """Split a Markdown table row while preserving LaTeX pipes inside cells.

    Delimiters are unescaped pipes outside LaTeX brace groups. This handles
    OCR formulas such as ``\\vphantom { \\Biggl { \\| } }`` without cutting the
    cell in the middle.
    """

    def _looks_like_table_delimiter(index: int) -> bool:
        if index == 0 or index == len(line) - 1:
            return True
        previous_char = line[index - 1]
        next_char = line[index + 1]
        return previous_char.isspace() and next_char.isspace()

    cells: list[tuple[str, int, int]] = []
    start = 0
    brace_depth = 0
    for index, char in enumerate(line):
        if char == "{" and not _is_escaped(line, index):
            brace_depth += 1
        elif char == "}" and not _is_escaped(line, index):
            brace_depth = max(0, brace_depth - 1)
        elif (
            char == "|"
            and brace_depth == 0
            and not _is_escaped(line, index)
            and _looks_like_table_delimiter(index)
        ):
            cells.append((line[start:index], start, index))
            start = index + 1
    cells.append((line[start:], start, len(line)))

    if cells and cells[0][0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1][0].strip() == "":
        cells = cells[:-1]
    return cells


def _trim_span(text: str, start: int, end: int) -> tuple[str, int, int]:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return text[start:end], start, end


def _looks_like_formula_candidate(text: str) -> bool:
    stripped = text.strip()
    return bool(stripped and FORMULA_CANDIDATE_RE.search(stripped))


def _looks_like_formula_line(text: str) -> bool:
    stripped = text.strip()
    if not _looks_like_formula_candidate(stripped):
        return False
    if CHINESE_RE.search(stripped):
        return False
    if not FORMULA_LINE_RE.match(stripped):
        return False
    return bool(
        stripped.startswith("\\")
        or "\\begin" in stripped
        or "\\left" in stripped
        or "=" in stripped
    )


def _protected_ranges(line: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(line):
        if line[index] != "`":
            index += 1
            continue
        end_marker = index
        while end_marker < len(line) and line[end_marker] == "`":
            end_marker += 1
        marker = line[index:end_marker]
        end = line.find(marker, end_marker)
        if end == -1:
            ranges.append((index, len(line)))
            break
        ranges.append((index, end + len(marker)))
        index = end + len(marker)
    return ranges


def _inside_ranges(index: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in ranges)


def _inline_math_spans(line: str) -> list[tuple[str, int, int, str]]:
    spans: list[tuple[str, int, int, str]] = []
    protected = _protected_ranges(line)
    index = 0
    while index < len(line):
        if _inside_ranges(index, protected):
            index += 1
            continue
        if line.startswith(r"\(", index):
            end = line.find(r"\)", index + 2)
            if end != -1:
                spans.append((line[index + 2:end], index + 2, end, "inline_math"))
                index = end + 2
                continue
        if line.startswith(r"\[", index):
            end = line.find(r"\]", index + 2)
            if end != -1:
                spans.append((line[index + 2:end], index + 2, end, "display_math"))
                index = end + 2
                continue
        if line[index] == "$" and not _is_escaped(line, index):
            marker = "$$" if line.startswith("$$", index) else "$"
            start = index + len(marker)
            end = line.find(marker, start)
            while end != -1 and _is_escaped(line, end):
                end = line.find(marker, end + len(marker))
            if end != -1:
                spans.append((line[start:end], start, end, "display_math" if marker == "$$" else "inline_math"))
                index = end + len(marker)
                continue
        index += 1
    return spans


def validate_formula_boundary(formula: str) -> list[str]:
    errors: list[str] = []
    stripped = formula.strip()
    if re.match(r"^(?:\}\s*){2,}", stripped):
        errors.append("starts_with_closing_braces")

    depth = 0
    underflow = False
    for index, char in enumerate(formula):
        if char == "{" and not _is_escaped(formula, index):
            depth += 1
        elif char == "}" and not _is_escaped(formula, index):
            depth -= 1
            if depth < 0:
                underflow = True
                depth = 0
    if underflow:
        errors.append("brace_underflow")
    if depth != 0:
        errors.append("unbalanced_braces")

    begins = BEGIN_RE.findall(formula)
    ends = END_RE.findall(formula)
    if begins != ends:
        errors.append("begin_end_mismatch")

    left_count = len(LEFT_RE.findall(formula))
    right_count = len(RIGHT_RE.findall(formula))
    if left_count != right_count:
        errors.append("left_right_mismatch")

    return errors


def _heading_path_after_update(line: str, heading_stack: list[tuple[int, str]]) -> bool:
    match = HEADING_RE.match(line.strip())
    if not match:
        return False
    level = len(match.group(1))
    title = match.group(2).strip()
    while heading_stack and heading_stack[-1][0] >= level:
        heading_stack.pop()
    heading_stack.append((level, title))
    return True


def _append_occurrence(
    occurrences: list[FormulaOccurrence],
    *,
    formula: str,
    line_no: int,
    line_end: int | None = None,
    start_offset: int,
    end_offset: int,
    container: str,
    markdown_line: str,
    heading_path: list[str],
    issue: str,
) -> None:
    completeness_errors = validate_formula_boundary(formula)
    occurrence_id = f"formula_{len(occurrences) + 1:04d}"
    occurrences.append(
        FormulaOccurrence(
            occurrence_id=occurrence_id,
            formula=formula,
            line_start=line_no,
            line_end=line_end or line_no,
            start_offset=start_offset,
            end_offset=end_offset,
            container=container,
            markdown_line=markdown_line,
            heading_path=heading_path,
            extract_confidence="high" if not completeness_errors else "low",
            completeness_errors=completeness_errors,
            issue=issue,
        )
    )


def extract_formula_occurrences(
    markdown: str,
    *,
    issue_patterns: Iterable[str | Pattern[str]] | None = None,
) -> list[FormulaOccurrence]:
    """Return formula occurrences containing one of the render issue patterns."""

    patterns = _compile_patterns(issue_patterns)
    occurrences: list[FormulaOccurrence] = []
    heading_stack: list[tuple[int, str]] = []
    in_fence = False
    fence_marker: str | None = None
    absolute_offset = 0

    for line_no, raw_line in enumerate(markdown.splitlines(keepends=True), start=1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()
        fence_match = FENCE_RE.match(stripped)
        if in_fence:
            if fence_match and fence_match.group(1) == fence_marker:
                in_fence = False
                fence_marker = None
            absolute_offset += len(raw_line)
            continue
        if fence_match:
            in_fence = True
            fence_marker = fence_match.group(1)
            absolute_offset += len(raw_line)
            continue
        if _heading_path_after_update(line, heading_stack):
            absolute_offset += len(raw_line)
            continue

        current_heading_path = [title for _, title in heading_stack]
        line_issue = _matching_issue(line, patterns)
        if line_issue is None:
            absolute_offset += len(raw_line)
            continue

        extracted = False
        if stripped.startswith("|") and "|" in stripped[1:]:
            for cell, start, end in split_markdown_table_row(line):
                cell_text, trimmed_start, trimmed_end = _trim_span(line, start, end)
                issue = _matching_issue(cell_text, patterns)
                if issue is None:
                    continue
                _append_occurrence(
                    occurrences,
                    formula=cell_text,
                    line_no=line_no,
                    start_offset=absolute_offset + trimmed_start,
                    end_offset=absolute_offset + trimmed_end,
                    container="table_cell",
                    markdown_line=line,
                    heading_path=current_heading_path,
                    issue=issue,
                )
                extracted = True

        for formula, start, end, container in _inline_math_spans(line):
            issue = _matching_issue(formula, patterns)
            if issue is None:
                continue
            _append_occurrence(
                occurrences,
                formula=formula,
                line_no=line_no,
                start_offset=absolute_offset + start,
                end_offset=absolute_offset + end,
                container=container,
                markdown_line=line,
                heading_path=current_heading_path,
                issue=issue,
            )
            extracted = True

        if not extracted:
            fallback, start, end = _trim_span(line, 0, len(line))
            issue = _matching_issue(fallback, patterns)
            if issue is not None:
                _append_occurrence(
                    occurrences,
                    formula=fallback,
                    line_no=line_no,
                    start_offset=absolute_offset + start,
                    end_offset=absolute_offset + end,
                    container="formula_line",
                    markdown_line=line,
                    heading_path=current_heading_path,
                    issue=issue,
                )
        absolute_offset += len(raw_line)

    return occurrences


def extract_formula_candidates(markdown: str) -> list[FormulaOccurrence]:
    """Return formula-like spans with stable offsets, without judging renderability.

    Inline/display math delimiters are treated as authoritative boundaries. Markdown
    table cells are included only when the cell itself looks formula-like, which lets
    OCR table formulas be checked without sending ordinary prose cells to renderers.
    """

    occurrences: list[FormulaOccurrence] = []
    heading_stack: list[tuple[int, str]] = []
    in_fence = False
    fence_marker: str | None = None
    absolute_offset = 0
    in_display_math = False
    display_start_line = 0
    display_start_offset = 0
    display_parts: list[str] = []

    for line_no, raw_line in enumerate(markdown.splitlines(keepends=True), start=1):
        line = raw_line.rstrip("\r\n")
        ending = raw_line[len(line):]
        stripped = line.strip()
        fence_match = FENCE_RE.match(stripped)
        if in_fence:
            if fence_match and fence_match.group(1) == fence_marker:
                in_fence = False
                fence_marker = None
            absolute_offset += len(raw_line)
            continue

        if in_display_math:
            closing_index = _find_unescaped(line, "$$")
            if closing_index == -1:
                display_parts.append(raw_line)
                absolute_offset += len(raw_line)
                continue
            display_parts.append(line[:closing_index])
            formula = "".join(display_parts)
            _append_occurrence(
                occurrences,
                formula=formula,
                line_no=display_start_line,
                line_end=line_no,
                start_offset=display_start_offset,
                end_offset=absolute_offset + closing_index,
                container="display_math",
                markdown_line=formula,
                heading_path=[title for _, title in heading_stack],
                issue="candidate",
            )
            in_display_math = False
            display_start_line = 0
            display_start_offset = 0
            display_parts = []
            absolute_offset += len(raw_line)
            continue

        if fence_match:
            in_fence = True
            fence_marker = fence_match.group(1)
            absolute_offset += len(raw_line)
            continue
        if _heading_path_after_update(line, heading_stack):
            absolute_offset += len(raw_line)
            continue

        current_heading_path = [title for _, title in heading_stack]
        display_open = _find_unescaped(line, "$$")
        if display_open != -1 and _find_unescaped(line, "$$", display_open + 2) == -1:
            in_display_math = True
            display_start_line = line_no
            display_start_offset = absolute_offset + display_open + 2
            display_parts = [line[display_open + 2:] + ending]
            absolute_offset += len(raw_line)
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            for cell, start, end in split_markdown_table_row(line):
                cell_text, trimmed_start, trimmed_end = _trim_span(line, start, end)
                cell_inline_spans = _inline_math_spans(cell_text)
                if cell_inline_spans:
                    for formula, inline_start, inline_end, container in cell_inline_spans:
                        _append_occurrence(
                            occurrences,
                            formula=formula,
                            line_no=line_no,
                            start_offset=absolute_offset + trimmed_start + inline_start,
                            end_offset=absolute_offset + trimmed_start + inline_end,
                            container=container,
                            markdown_line=line,
                            heading_path=current_heading_path,
                            issue="candidate",
                        )
                    continue
                if not _looks_like_formula_candidate(cell_text):
                    continue
                _append_occurrence(
                    occurrences,
                    formula=cell_text,
                    line_no=line_no,
                    start_offset=absolute_offset + trimmed_start,
                    end_offset=absolute_offset + trimmed_end,
                    container="table_cell",
                    markdown_line=line,
                    heading_path=current_heading_path,
                    issue="candidate",
                )
            absolute_offset += len(raw_line)
            continue

        inline_spans = _inline_math_spans(line)
        for formula, start, end, container in inline_spans:
            _append_occurrence(
                occurrences,
                formula=formula,
                line_no=line_no,
                start_offset=absolute_offset + start,
                end_offset=absolute_offset + end,
                container=container,
                markdown_line=line,
                heading_path=current_heading_path,
                issue="candidate",
            )
        if not inline_spans and _looks_like_formula_line(line):
            formula, start, end = _trim_span(line, 0, len(line))
            _append_occurrence(
                occurrences,
                formula=formula,
                line_no=line_no,
                start_offset=absolute_offset + start,
                end_offset=absolute_offset + end,
                container="formula_line",
                markdown_line=line,
                heading_path=current_heading_path,
                issue="candidate",
            )
        absolute_offset += len(raw_line)

    return occurrences
