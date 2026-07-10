from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


HEADING_RE = re.compile(r"^(?P<marker>#{1,6})\s+(?P<title>.+?)\s*$")
QUESTION_HEADING_RE = re.compile(
    r"^(?:"
    r"第\s*(?P<q1>\d{1,3}|[一二三四五六七八九十百千万两]+)\s*题"
    r"|[（(]\s*(?P<q2>\d{1,3})\s*[）)]\s*\S+"
    r"|(?P<q3>\d{1,3})[.．、]\s*\S+"
    r")"
)
QUESTION_LABEL_RE = re.compile(r"^第\s*(?P<number>\d{1,3}|[一二三四五六七八九十百千万两]+)\s*题")
PAREN_ARABIC_QUESTION_RE = re.compile(r"^[（(]\s*(?P<number>\d{1,3})\s*[）)]\s*\S+")
ARABIC_QUESTION_RE = re.compile(r"^(?P<number>\d{1,3})[.．、]\s*\S+")
DAMAGED_ARABIC_QUESTION_RE = re.compile(r"^(?P<number>\d(?:\s*\$?\s*\d){1,2})\s*[.．、]\s*\S+")
QUESTION_NUMBER_RE = re.compile(
    r"^(?:"
    r"第\s*(?P<q1>\d{1,3}|[一二三四五六七八九十百千万两]+)\s*题"
    r"|[（(]\s*(?P<q2>\d{1,3})\s*[）)]\s*\S+"
    r"|(?P<q3>\d{1,3})[.．、]\s*\S+"
    r")"
)
EXAMPLE_HEADING_RE = re.compile(
    r"^(?:"
    r"例\s*(?P<e1>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|例题\s*(?P<e2>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|典型例题\s*(?P<e3>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|【\s*例题\s*】"
    r")"
)
EXAMPLE_NUMBER_RE = re.compile(
    r"^(?:"
    r"例\s*(?P<e1>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|例题\s*(?P<e2>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|典型例题\s*(?P<e3>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r")"
)
LOCAL_LABELS = "解|答|答案|解析|分析|证明|评注|点评|点拨|提示|说明|变式|注意"
SOLUTION_LABEL_RE = re.compile(
    rf"^(?:\*\*(?:{LOCAL_LABELS})[:：]\*\*|(?:{LOCAL_LABELS})[:：])"
)
OPTION_MARKER_RE = re.compile(r"^[A-D][.．、]\s*\S+")
FORMULA_NUMBER_RE = re.compile(r"^[（(]\s*\d+(?:[.．]\d+)+\s*[）)]\s*$")
EXPECTED_COUNT_RE = re.compile(r"共\s*(?P<count>\d{1,3})\s*小题")


@dataclass
class _ProblemStart:
    line_no: int
    level: int
    title: str
    problem_kind: str
    problem_number: int | None
    number_style: str
    parent_path: list[str]
    heading_path: list[str]


@dataclass
class _ProblemRun:
    scope_id: str
    number_style: str
    groups: list[dict[str, Any]]

CHINESE_NUMBER_MAP = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


def _chinese_to_int(value: str) -> int | None:
    value = re.sub(r"\s+", "", value.strip())
    if not value:
        return None
    if value.isdigit():
        return int(value)
    if value in CHINESE_NUMBER_MAP:
        return CHINESE_NUMBER_MAP[value]
    if value == "十":
        return 10
    if "十" in value:
        left, _, right = value.partition("十")
        tens = CHINESE_NUMBER_MAP.get(left, 1) if left else 1
        ones = CHINESE_NUMBER_MAP.get(right, 0) if right else 0
        return tens * 10 + ones
    return None


def _quality_status(
    problem_count: int,
    solution_count: int,
    warnings: list[str],
    *,
    expected_problem_count: int | None = None,
) -> tuple[str, float]:
    if expected_problem_count:
        coverage = problem_count / max(expected_problem_count, 1)
        if coverage >= 0.95:
            return "high", 0.9
        warnings.append("exercise_problem_count_below_expected")
        if coverage >= 0.75:
            return "medium", 0.72
        if problem_count:
            return "low", 0.45
        return "failed", 0.2
    if problem_count >= 2:
        return "high", 0.9
    if problem_count == 1:
        return "medium", 0.72
    if solution_count:
        warnings.append("exercise_no_problem_groups")
        return "low", 0.45
    warnings.append("exercise_no_problem_signal")
    return "failed", 0.2


def _problem_kind(title: str) -> str | None:
    stripped = title.strip()
    if FORMULA_NUMBER_RE.match(stripped):
        return None
    if EXAMPLE_HEADING_RE.match(stripped):
        return "example"
    if QUESTION_HEADING_RE.match(stripped):
        return "question"
    return None


def _problem_number(title: str, kind: str | None) -> int | None:
    if kind == "example":
        match = EXAMPLE_NUMBER_RE.match(title.strip())
        if not match:
            return None
        value = match.group("e1") or match.group("e2") or match.group("e3")
        return _chinese_to_int(value or "")
    if kind == "question":
        match = QUESTION_NUMBER_RE.match(title.strip())
        if not match:
            return None
        value = match.group("q1") or match.group("q2") or match.group("q3")
        return _chinese_to_int(value or "")
    return None


def _question_number_style(title: str) -> tuple[str, int | None] | None:
    stripped = title.strip()
    match = QUESTION_LABEL_RE.match(stripped)
    if match:
        return "question_label", _chinese_to_int(match.group("number") or "")
    match = PAREN_ARABIC_QUESTION_RE.match(stripped)
    if match:
        return "paren_arabic", _chinese_to_int(match.group("number") or "")
    match = ARABIC_QUESTION_RE.match(stripped)
    if match:
        return "arabic", _chinese_to_int(match.group("number") or "")
    match = DAMAGED_ARABIC_QUESTION_RE.match(stripped)
    if match:
        digits = re.sub(r"\D", "", match.group("number") or "")
        return "arabic", _chinese_to_int(digits)
    return None


def _problem_number_and_style(title: str, kind: str | None) -> tuple[int | None, str]:
    if kind == "example":
        return _problem_number(title, kind), "example"
    if kind == "question":
        styled = _question_number_style(title)
        if styled is not None:
            style, number = styled
            return number, style
        return _problem_number(title, kind), "question"
    return None, "unknown"


def _heading_path_for_line(headings: list[dict[str, Any]], line_no: int, *, include_current: bool = True) -> list[str]:
    stack: list[dict[str, Any]] = []
    for heading in headings:
        if heading["line_no"] > line_no or (not include_current and heading["line_no"] == line_no):
            break
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        stack.append(heading)
    return [item["title"] for item in stack]


def _heading_parent_path_for_heading(headings: list[dict[str, Any]], line_no: int, level: int) -> list[str]:
    stack: list[dict[str, Any]] = []
    for heading in headings:
        if heading["line_no"] >= line_no:
            break
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        stack.append(heading)
    while stack and stack[-1]["level"] >= level:
        stack.pop()
    return [item["title"] for item in stack]


def _expected_problem_count(lines: list[str]) -> int | None:
    # Do not infer problem counts from parent headings such as "17-22小题" or "共4小题".
    # The exercise chunking goal is to split by actual detected problem units.
    return None


def _missing_problem_indices(problem_numbers: list[int], expected_problem_count: int | None) -> list[int]:
    if not expected_problem_count:
        return []
    observed = {number for number in problem_numbers if 1 <= number <= expected_problem_count}
    return [number for number in range(1, expected_problem_count + 1) if number not in observed]


def _parent_contains_problem(parent_path: list[str], accepted_titles: set[str]) -> bool:
    return any(title in accepted_titles for title in parent_path)


def _same_parent_scope(left: list[str], right: list[str]) -> bool:
    return tuple(left) == tuple(right)


def _should_start_new_scope(start: _ProblemStart, previous: dict[str, Any] | None) -> bool:
    if previous is None:
        return True
    previous_number = previous.get("display_problem_index")
    if not isinstance(previous_number, int) or start.problem_number is None:
        return False
    if start.problem_number == 1 and previous_number > 1:
        return not _same_parent_scope(start.parent_path, list(previous.get("problem_parent_path") or []))
    return False


def _should_demote_nested_marker(
    start: _ProblemStart,
    previous: dict[str, Any] | None,
    *,
    accepted_titles: set[str],
) -> bool:
    if previous is None:
        return False
    if _parent_contains_problem(start.parent_path, accepted_titles):
        return True
    previous_number = previous.get("display_problem_index")
    previous_style = str(previous.get("problem_family") or "")
    if not isinstance(previous_number, int) or start.problem_number is None:
        return False
    parent_changed = not _same_parent_scope(start.parent_path, list(previous.get("problem_parent_path") or []))
    if parent_changed:
        return False
    if start.number_style != previous_style and start.problem_number <= 3 and previous_number >= 3:
        return True
    if start.number_style == previous_style and start.problem_number <= previous_number:
        return True
    return False


def _scope_id(scope_index: int) -> str:
    return f"problem_scope_{scope_index:03d}"


def _group_from_start(
    start: _ProblemStart,
    *,
    unit_index: int,
    end_line: int,
    scope_id: str,
) -> dict[str, Any]:
    display_index = start.problem_number or unit_index
    return {
        "problem_id": f"problem_{display_index:03d}",
        "problem_unit_id": f"problem_unit_{unit_index:03d}",
        "problem_index": display_index,
        "display_problem_index": display_index,
        "problem_scope_id": scope_id,
        "problem_parent_path": list(start.parent_path),
        "problem_family": start.number_style,
        "problem_kind": start.problem_kind,
        "title": start.title,
        "start_line": start.line_no,
        "end_line": end_line,
        "heading_path": list(start.heading_path),
    }


def _select_problem_starts(starts: list[_ProblemStart], warnings: list[str]) -> list[_ProblemStart]:
    accepted: list[_ProblemStart] = []
    accepted_titles: set[str] = set()
    nested_demotions = 0
    for start in starts:
        previous = None
        if accepted:
            previous_start = accepted[-1]
            previous = {
                "display_problem_index": previous_start.problem_number,
                "problem_family": previous_start.number_style,
                "problem_parent_path": previous_start.parent_path,
            }
        if _should_demote_nested_marker(start, previous, accepted_titles=accepted_titles):
            nested_demotions += 1
            continue
        accepted.append(start)
        accepted_titles.add(start.title)
    if nested_demotions:
        warnings.append("exercise_nested_question_markers_demoted")
    return accepted


def _build_problem_groups(starts: list[_ProblemStart], line_count: int) -> tuple[list[dict[str, Any]], list[_ProblemRun]]:
    groups: list[dict[str, Any]] = []
    runs: list[_ProblemRun] = []
    current_scope = _scope_id(1)
    current_style = starts[0].number_style if starts else "unknown"
    current_run = _ProblemRun(current_scope, current_style, [])
    scope_index = 1

    for position, start in enumerate(starts):
        previous_group = groups[-1] if groups else None
        if (
            groups
            and (
                _should_start_new_scope(start, previous_group)
                or (start.number_style != current_style and start.problem_number == 1)
            )
        ):
            runs.append(current_run)
            scope_index += 1
            current_scope = _scope_id(scope_index)
            current_style = start.number_style
            current_run = _ProblemRun(current_scope, current_style, [])
        elif start.problem_number is not None and previous_group is not None:
            previous_number = previous_group.get("display_problem_index")
            if isinstance(previous_number, int) and start.problem_number == previous_number + 1:
                current_style = start.number_style

        next_start_line = starts[position + 1].line_no if position + 1 < len(starts) else line_count + 1
        group = _group_from_start(
            start,
            unit_index=len(groups) + 1,
            end_line=max(start.line_no, next_start_line - 1),
            scope_id=current_scope,
        )
        groups.append(group)
        current_run.groups.append(group)

    if current_run.groups:
        runs.append(current_run)
    return groups, runs


def _sequence_gap_candidates(runs: list[_ProblemRun]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for run in runs:
        groups = [
            group
            for group in run.groups
            if isinstance(group.get("display_problem_index"), int)
        ]
        if len(groups) < 2:
            continue
        for previous, next_group in zip(groups, groups[1:]):
            previous_number = int(previous["display_problem_index"])
            next_number = int(next_group["display_problem_index"])
            if next_number <= previous_number + 1:
                continue
            for missing in range(previous_number + 1, next_number):
                candidates.append(
                    {
                        "candidate_type": "sequence_gap",
                        "problem_scope_id": run.scope_id,
                        "problem_family": run.number_style,
                        "target_problem_index": missing,
                        "previous_problem_unit_id": previous.get("problem_unit_id"),
                        "next_problem_unit_id": next_group.get("problem_unit_id"),
                        "previous_problem_index": previous_number,
                        "next_problem_index": next_number,
                    }
                )
    return candidates


def _tail_problem_candidate(lines: list[str], groups: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not groups:
        return None
    last = groups[-1]
    start_line = int(last.get("start_line") or 1)
    end_line = int(last.get("end_line") or start_line)
    tail_lines = [line for line in lines[start_line:end_line] if line.strip()]
    if len(tail_lines) < 4:
        return None
    display_index = last.get("display_problem_index")
    target_index = int(display_index) + 1 if isinstance(display_index, int) else None
    return {
        "candidate_type": "tail_problem_absorption",
        "problem_scope_id": last.get("problem_scope_id"),
        "problem_family": last.get("problem_family"),
        "target_problem_index": target_index,
        "previous_problem_unit_id": last.get("problem_unit_id"),
        "previous_problem_index": display_index,
    }


def analyze_exercise_structure(markdown: str, *, material_type: str) -> dict[str, Any]:
    if material_type != "exercise":
        return {
            "status": "skipped",
            "confidence": 0.0,
            "problem_count": 0,
            "expected_problem_count": None,
            "missing_problem_indices": [],
            "solution_label_count": 0,
            "suspicious_option_marker_count": 0,
            "sequence_gap_candidates": [],
            "tail_problem_candidate": None,
            "problem_groups": [],
            "warnings": [],
        }

    lines = markdown.splitlines()
    headings: list[dict[str, Any]] = []
    problem_starts: list[_ProblemStart] = []
    solution_label_count = 0
    option_marker_count = 0
    warnings: list[str] = []

    for index, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            title = heading_match.group("title").strip()
            level = len(heading_match.group("marker"))
            heading = {"line_no": index, "level": level, "title": title}
            headings.append(heading)
            kind = _problem_kind(title)
            if kind is not None:
                problem_number, number_style = _problem_number_and_style(title, kind)
                parent_path = _heading_parent_path_for_heading(headings, index, level)
                heading_path = _heading_path_for_line(headings, index)
                problem_starts.append(
                    _ProblemStart(
                        line_no=index,
                        level=level,
                        title=title,
                        problem_kind=kind,
                        problem_number=problem_number,
                        number_style=number_style,
                        parent_path=parent_path,
                        heading_path=heading_path,
                    )
                )
        else:
            kind = _problem_kind(stripped)
            if kind is not None:
                problem_number, number_style = _problem_number_and_style(stripped, kind)
                parent_path = _heading_path_for_line(headings, index)
                problem_starts.append(
                    _ProblemStart(
                        line_no=index,
                        level=0,
                        title=stripped,
                        problem_kind=kind,
                        problem_number=problem_number,
                        number_style=number_style,
                        parent_path=parent_path,
                        heading_path=[*parent_path, stripped],
                    )
                )
        if SOLUTION_LABEL_RE.match(stripped):
            solution_label_count += 1
        if OPTION_MARKER_RE.match(stripped):
            option_marker_count += 1

    selected_starts = _select_problem_starts(problem_starts, warnings)
    problem_groups, problem_runs = _build_problem_groups(selected_starts, len(lines)) if selected_starts else ([], [])
    sequence_gap_candidates = _sequence_gap_candidates(problem_runs)
    tail_problem_candidate = _tail_problem_candidate(lines, problem_groups)

    expected_problem_count = _expected_problem_count(lines)
    missing_problem_indices = sorted(
        {
            int(candidate["target_problem_index"])
            for candidate in sequence_gap_candidates
            if isinstance(candidate.get("target_problem_index"), int)
        }
    )
    if missing_problem_indices:
        warnings.append("exercise_problem_indices_missing")
    status, confidence = _quality_status(
        len(problem_groups),
        solution_label_count,
        warnings,
        expected_problem_count=expected_problem_count,
    )
    if missing_problem_indices and status == "high":
        status, confidence = "medium", 0.72
    return {
        "status": status,
        "confidence": confidence,
        "problem_count": len(problem_groups),
        "expected_problem_count": expected_problem_count,
        "missing_problem_indices": missing_problem_indices,
        "solution_label_count": solution_label_count,
        "suspicious_option_marker_count": option_marker_count,
        "sequence_gap_candidates": sequence_gap_candidates,
        "tail_problem_candidate": tail_problem_candidate,
        "problem_groups": problem_groups,
        "warnings": sorted(set(warnings)),
    }
