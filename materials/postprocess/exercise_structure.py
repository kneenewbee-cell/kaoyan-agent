from __future__ import annotations

import re
from typing import Any


HEADING_RE = re.compile(r"^(?P<marker>#{1,6})\s+(?P<title>.+?)\s*$")
QUESTION_HEADING_RE = re.compile(
    r"^(?:"
    r"第\s*(?P<q1>\d{1,3}|[一二三四五六七八九十百千万两]+)\s*题"
    r"|[（(]\s*(?P<q2>\d{1,3})\s*[）)]\s*\S+"
    r"|(?P<q3>\d{1,3})[.．、]\s*\S+"
    r")"
)
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


def _heading_path_for_line(headings: list[dict[str, Any]], line_no: int) -> list[str]:
    stack: list[dict[str, Any]] = []
    for heading in headings:
        if heading["line_no"] > line_no:
            break
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        stack.append(heading)
    return [item["title"] for item in stack]


def _expected_problem_count(lines: list[str]) -> int | None:
    counts = []
    for line in lines:
        for match in EXPECTED_COUNT_RE.finditer(line):
            counts.append(int(match.group("count")))
    if not counts:
        return None
    return sum(counts)


def _missing_problem_indices(problem_numbers: list[int], expected_problem_count: int | None) -> list[int]:
    if not expected_problem_count:
        return []
    observed = {number for number in problem_numbers if 1 <= number <= expected_problem_count}
    return [number for number in range(1, expected_problem_count + 1) if number not in observed]


def analyze_exercise_structure(markdown: str, *, material_type: str) -> dict[str, Any]:
    if material_type != "exercise":
        return {
            "status": "skipped",
            "confidence": 0.0,
            "problem_count": 0,
            "solution_label_count": 0,
            "suspicious_option_marker_count": 0,
            "problem_groups": [],
            "warnings": [],
        }

    lines = markdown.splitlines()
    headings: list[dict[str, Any]] = []
    problem_starts: list[dict[str, Any]] = []
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
                problem_starts.append({**heading, "problem_kind": kind, "problem_number": _problem_number(title, kind)})
        else:
            kind = _problem_kind(stripped)
            if kind is not None:
                problem_starts.append(
                    {
                        "line_no": index,
                        "level": 0,
                        "title": stripped,
                        "problem_kind": kind,
                        "problem_number": _problem_number(stripped, kind),
                    }
                )
        if SOLUTION_LABEL_RE.match(stripped):
            solution_label_count += 1
        if OPTION_MARKER_RE.match(stripped):
            option_marker_count += 1

    problem_groups: list[dict[str, Any]] = []
    for group_index, start in enumerate(problem_starts, start=1):
        next_start_line = (
            problem_starts[group_index]["line_no"]
            if group_index < len(problem_starts)
            else len(lines) + 1
        )
        end_line = max(start["line_no"], next_start_line - 1)
        problem_index = start.get("problem_number") or group_index
        heading_path = _heading_path_for_line(headings, start["line_no"])
        if not heading_path or heading_path[-1] != start["title"]:
            heading_path = [*heading_path, start["title"]]
        problem_groups.append(
            {
                "problem_id": f"problem_{problem_index:03d}",
                "problem_index": problem_index,
                "problem_kind": start["problem_kind"],
                "title": start["title"],
                "start_line": start["line_no"],
                "end_line": end_line,
                "heading_path": heading_path,
            }
        )

    expected_problem_count = _expected_problem_count(lines)
    problem_numbers = [
        int(group["problem_index"])
        for group in problem_groups
        if isinstance(group.get("problem_index"), int)
    ]
    missing_problem_indices = _missing_problem_indices(problem_numbers, expected_problem_count)
    if missing_problem_indices:
        warnings.append("exercise_problem_indices_missing")
    status, confidence = _quality_status(
        len(problem_groups),
        solution_label_count,
        warnings,
        expected_problem_count=expected_problem_count,
    )
    return {
        "status": status,
        "confidence": confidence,
        "problem_count": len(problem_groups),
        "expected_problem_count": expected_problem_count,
        "missing_problem_indices": missing_problem_indices,
        "solution_label_count": solution_label_count,
        "suspicious_option_marker_count": option_marker_count,
        "problem_groups": problem_groups,
        "warnings": sorted(set(warnings)),
    }
