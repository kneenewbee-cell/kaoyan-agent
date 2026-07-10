from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


DEFAULT_MIN_CONFIDENCE = 0.8
OPTION_LINE_RE = re.compile(r"^[A-D][.、．]\s*\S+")
FORMULA_NUMBER_LINE_RE = re.compile(r"^[（(]\s*\d+(?:[.\-]\d+)+\s*[)）]\s*$")
SUBQUESTION_LINE_RE = re.compile(r"^[（(]\s*(?:I{1,3}|IV|V|Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|一|二|三|四)\s*[)）]")
LOW_PAREN_ARABIC_LINE_RE = re.compile(r"^[（(]\s*(?P<number>\d{1,2})\s*[)）]")
PROBLEM_LIKE_START_RE = re.compile(r"^(?:设|已知|若|求|证明|计算|令|记|设函数|设平面|设区域|设曲线)\S*")


def _line_text(lines: list[str], line_no: int) -> str:
    if line_no < 1 or line_no > len(lines):
        return ""
    return lines[line_no - 1].strip()


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _sorted_groups(report: dict[str, Any]) -> list[dict[str, Any]]:
    groups = [dict(group) for group in list(report.get("problem_groups") or [])]
    return sorted(groups, key=lambda group: (int(group.get("start_line") or 0), int(group.get("problem_index") or 0)))


def _find_previous_next(groups: list[dict[str, Any]], missing_index: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    previous = None
    next_group = None
    for group in groups:
        problem_index = _safe_int(group.get("problem_index"))
        if problem_index is None:
            continue
        if problem_index < missing_index:
            previous = group
        elif problem_index > missing_index:
            next_group = group
            break
    return previous, next_group


def _find_group_by_unit_id(groups: list[dict[str, Any]], unit_id: Any) -> dict[str, Any] | None:
    if not unit_id:
        return None
    for group in groups:
        if group.get("problem_unit_id") == unit_id:
            return group
    return None


def _candidate_lines(lines: list[str], start_line: int, end_line: int) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for line_no in range(max(start_line, 1), min(end_line, len(lines)) + 1):
        output.append({"line_no": line_no, "text": lines[line_no - 1]})
    if len(output) <= 45:
        return output
    return output[:8] + [{"line_no": -1, "text": "[TRUNCATED_MIDDLE_LINES]"}] + output[-36:]


def _marker_evidence(lines: list[str], start_line: int, end_line: int, missing_index: int) -> list[dict[str, Any]]:
    marker = re.compile(rf"[（(]\s*{missing_index}\s*[)）]")
    evidence = []
    for line_no in range(max(start_line, 1), min(end_line, len(lines)) + 1):
        text = lines[line_no - 1].strip()
        if marker.search(text):
            evidence.append({"line_no": line_no, "text": text[:500], "signal": "contains_missing_index_marker"})
    return evidence


def _range_cue_nearby(lines: list[str], line_no: int, missing_index: int) -> list[str]:
    cues: list[str] = []
    cue_pattern = re.compile(rf"(?:{missing_index}\s*[-~—－]\s*\d+|\d+\s*[-~—－]\s*{missing_index}|{missing_index})\s*题")
    for nearby in range(max(1, line_no - 1), min(len(lines), line_no + 2) + 1):
        text = lines[nearby - 1].strip()
        if cue_pattern.search(text):
            cues.append(f"near_line_{nearby}_problem_range_cue")
    return cues


def _orphan_evidence(lines: list[str], start_line: int, end_line: int, missing_index: int) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for line_no in range(max(start_line + 1, 1), min(end_line, len(lines)) + 1):
        text = lines[line_no - 1].strip()
        if not text or _is_non_problem_start(text):
            continue
        if PROBLEM_LIKE_START_RE.match(text):
            nearby_cues = _range_cue_nearby(lines, line_no, missing_index)
            previous_blank = not _line_text(lines, line_no - 1)
            if line_no <= start_line + 1 and not nearby_cues:
                continue
            if not previous_blank and not nearby_cues:
                continue
            signals = ["problem_like_sentence_start"]
            signals.extend(nearby_cues)
            evidence.append({"line_no": line_no, "text": text[:500], "signals": signals})
    return evidence


def _low_paren_sequence_evidence(lines: list[str], start_line: int, end_line: int) -> list[dict[str, Any]]:
    sequence: list[dict[str, Any]] = []
    expected = 1
    for line_no in range(max(start_line + 1, 1), min(end_line, len(lines)) + 1):
        text = lines[line_no - 1].strip()
        if not text:
            continue
        match = LOW_PAREN_ARABIC_LINE_RE.match(text)
        if not match:
            if sequence:
                break
            continue
        number = _safe_int(match.group("number"))
        if number != expected:
            if sequence:
                break
            continue
        sequence.append({"line_no": line_no, "text": text[:500], "number": number})
        expected += 1
    if len(sequence) < 2:
        return []
    return [
        {
            "sequence_start_line": sequence[0]["line_no"],
            "sequence_count": len(sequence),
            "items": sequence[:5],
            "signals": ["low_paren_sequence_after_previous_problem"],
        }
    ]


def _build_candidate(
    *,
    lines: list[str],
    missing_index: int,
    previous: dict[str, Any],
    next_group: dict[str, Any] | None,
    candidate_type: str = "previous_problem_absorption",
) -> dict[str, Any]:
    start_line = int(previous.get("start_line") or 1)
    end_line = int(previous.get("end_line") or start_line)
    return {
        "candidate_type": candidate_type,
        "target_missing_index": missing_index,
        "previous_problem": {
            "problem_index": previous.get("problem_index"),
            "problem_id": previous.get("problem_id"),
            "title": previous.get("title"),
            "start_line": start_line,
            "end_line": end_line,
        },
        "next_problem": (
            {
                "problem_index": next_group.get("problem_index"),
                "problem_id": next_group.get("problem_id"),
                "title": next_group.get("title"),
                "start_line": next_group.get("start_line"),
                "end_line": next_group.get("end_line"),
            }
            if next_group
            else None
        ),
        "candidate_lines": _candidate_lines(lines, start_line, end_line),
        "marker_evidence": _marker_evidence(lines, start_line, end_line, missing_index),
        "suspected_orphan_lines": _orphan_evidence(lines, start_line, end_line, missing_index),
        "low_paren_sequence_evidence": _low_paren_sequence_evidence(lines, start_line, end_line),
        "local_rules": [
            "The missing problem is usually absorbed into the previous problem range.",
            "For tail_problem_absorption, judge whether the last recognized problem contains another independent problem after its own title.",
            "If suspected_orphan_lines is present, judge whether that line starts the missing problem even without an explicit number marker.",
            "If low_paren_sequence_evidence is present in a single-number gap, judge whether the missing problem stem was lost but its numbered statements remain.",
            "Do not split on A/B/C/D option lines.",
            "Do not split on formula numbers such as (1.1).",
            "Do not split on sub-question markers such as (I), (II), Ⅰ, Ⅱ.",
            "Return JSON only; do not rewrite source text.",
        ],
    }


def _candidate_from_descriptor(
    *,
    lines: list[str],
    groups: list[dict[str, Any]],
    descriptor: dict[str, Any],
) -> dict[str, Any] | None:
    missing_index = _safe_int(descriptor.get("target_problem_index"))
    if missing_index is None:
        return None
    previous = _find_group_by_unit_id(groups, descriptor.get("previous_problem_unit_id"))
    next_group = _find_group_by_unit_id(groups, descriptor.get("next_problem_unit_id"))
    if previous is None:
        previous, fallback_next = _find_previous_next(groups, missing_index)
        if next_group is None:
            next_group = fallback_next
    if previous is None:
        return None
    return _build_candidate(
        lines=lines,
        missing_index=missing_index,
        previous=previous,
        next_group=next_group,
        candidate_type=str(descriptor.get("candidate_type") or "previous_problem_absorption"),
    )


def _repair_candidate_descriptors(exercise_report: dict[str, Any], groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    descriptors: list[dict[str, Any]] = []
    for raw_candidate in list(exercise_report.get("sequence_gap_candidates") or []):
        if isinstance(raw_candidate, dict):
            descriptors.append(dict(raw_candidate))
    tail_candidate = exercise_report.get("tail_problem_candidate")
    if isinstance(tail_candidate, dict):
        descriptors.append(dict(tail_candidate))
    if descriptors:
        seen: set[tuple[Any, Any, Any]] = set()
        unique: list[dict[str, Any]] = []
        for descriptor in descriptors:
            key = (
                descriptor.get("candidate_type"),
                descriptor.get("target_problem_index"),
                descriptor.get("previous_problem_unit_id"),
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(descriptor)
        return unique

    fallback: list[dict[str, Any]] = []
    for missing_index in [
        int(value)
        for value in list(exercise_report.get("missing_problem_indices") or [])
        if _safe_int(value) is not None
    ]:
        previous, next_group = _find_previous_next(groups, missing_index)
        fallback.append(
            {
                "candidate_type": "previous_problem_absorption",
                "target_problem_index": missing_index,
                "previous_problem_unit_id": previous.get("problem_unit_id") if previous else None,
                "next_problem_unit_id": next_group.get("problem_unit_id") if next_group else None,
            }
        )
    return fallback


def _is_non_problem_start(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    return bool(
        OPTION_LINE_RE.match(stripped)
        or FORMULA_NUMBER_LINE_RE.match(stripped)
        or SUBQUESTION_LINE_RE.match(stripped)
    )


def _validate_judgement(
    judgement: dict[str, Any],
    *,
    candidate: dict[str, Any],
    lines: list[str],
    min_confidence: float,
) -> tuple[bool, str, dict[str, Any]]:
    target = _safe_int(judgement.get("target_problem_index"))
    expected = int(candidate["target_missing_index"])
    if target != expected:
        return False, "target_problem_index_mismatch", {}
    if str(judgement.get("decision") or "").strip() not in {"split_previous_problem", "split"}:
        return False, "decision_not_split", {}
    confidence = float(judgement.get("confidence") or 0.0)
    if confidence < min_confidence:
        return False, "confidence_below_threshold", {"confidence": confidence}

    start_line = _safe_int(judgement.get("start_line") or judgement.get("split_start_line"))
    end_line = _safe_int(judgement.get("end_line"))
    previous = candidate["previous_problem"]
    previous_start = int(previous["start_line"])
    previous_end = int(previous["end_line"])
    if start_line is None:
        return False, "missing_start_line", {"confidence": confidence}
    if end_line is None:
        end_line = previous_end
    if start_line <= previous_start or start_line > previous_end:
        return False, "start_line_outside_previous_problem", {"confidence": confidence, "start_line": start_line}
    if end_line < start_line or end_line > previous_end:
        return False, "end_line_outside_previous_problem", {"confidence": confidence, "end_line": end_line}
    if _is_non_problem_start(_line_text(lines, start_line)):
        return False, "candidate_starts_on_non_problem_line", {"confidence": confidence, "start_line": start_line}

    title = str(judgement.get("title") or _line_text(lines, start_line)).strip()
    return True, "accepted", {
        "target_problem_index": expected,
        "start_line": start_line,
        "end_line": end_line,
        "confidence": confidence,
        "title": title,
        "reason_codes": list(judgement.get("reason_codes") or []),
    }


def _local_high_confidence_repair(candidate: dict[str, Any], *, lines: list[str]) -> dict[str, Any] | None:
    if candidate.get("candidate_type") != "sequence_gap":
        return None
    target = int(candidate["target_missing_index"])
    previous = candidate["previous_problem"]
    previous_start = int(previous["start_line"])
    previous_end = int(previous["end_line"])
    evidence_line: int | None = None
    reason_codes: list[str] = ["local_high_confidence_sequence_gap"]

    marker_evidence = list(candidate.get("marker_evidence") or [])
    if marker_evidence:
        evidence_line = _safe_int(marker_evidence[0].get("line_no"))
        reason_codes.append("contains_missing_index_marker")
    if evidence_line is None:
        for orphan in list(candidate.get("suspected_orphan_lines") or []):
            signals = [str(signal) for signal in list(orphan.get("signals") or [])]
            if any(signal.startswith("near_line_") and "problem_range_cue" in signal for signal in signals):
                evidence_line = _safe_int(orphan.get("line_no"))
                reason_codes.extend(["orphan_problem_like_block", "nearby_problem_range_cue"])
                break
    if evidence_line is None:
        previous_number = _safe_int(candidate.get("previous_problem", {}).get("problem_index"))
        next_number = _safe_int((candidate.get("next_problem") or {}).get("problem_index"))
        single_gap = previous_number is not None and next_number is not None and previous_number + 2 == next_number == target + 1
        if single_gap:
            for sequence in list(candidate.get("low_paren_sequence_evidence") or []):
                sequence_count = _safe_int(sequence.get("sequence_count"))
                if sequence_count is not None and sequence_count >= 2:
                    evidence_line = _safe_int(sequence.get("sequence_start_line"))
                    reason_codes.append("low_paren_sequence_after_previous_problem")
                    break
    if evidence_line is None:
        return None
    if evidence_line <= previous_start or evidence_line > previous_end:
        return None
    if _is_non_problem_start(_line_text(lines, evidence_line)) and "low_paren_sequence_after_previous_problem" not in reason_codes:
        return None
    title_text = _line_text(lines, evidence_line)
    if not re.match(r"^[（(]?\s*" + re.escape(str(target)), title_text):
        title_text = f"({target}) {title_text}"
    return {
        "target_problem_index": target,
        "start_line": evidence_line,
        "end_line": previous_end,
        "confidence": 0.82,
        "title": title_text,
        "reason_codes": reason_codes,
    }


def _apply_repairs(groups: list[dict[str, Any]], repairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not repairs:
        return groups
    result = [dict(group) for group in groups]
    for repair in sorted(repairs, key=lambda item: int(item["start_line"])):
        target = int(repair["target_problem_index"])
        split_start = int(repair["start_line"])
        split_end = int(repair["end_line"])
        previous_position = None
        for index, group in enumerate(result):
            problem_index = _safe_int(group.get("problem_index"))
            start_line = int(group.get("start_line") or 0)
            end_line = int(group.get("end_line") or 0)
            if problem_index is not None and problem_index < target and start_line < split_start <= end_line:
                previous_position = index
        if previous_position is None:
            continue
        previous = result[previous_position]
        original_end = int(previous.get("end_line") or split_end)
        previous["end_line"] = split_start - 1
        new_group = {
            "problem_id": f"problem_{target:03d}",
            "problem_unit_id": f"problem_unit_repaired_{target:03d}",
            "problem_index": target,
            "display_problem_index": target,
            "problem_scope_id": previous.get("problem_scope_id"),
            "problem_parent_path": list(previous.get("problem_parent_path") or []),
            "problem_family": previous.get("problem_family"),
            "problem_kind": previous.get("problem_kind", "question"),
            "title": repair["title"],
            "start_line": split_start,
            "end_line": min(split_end, original_end),
            "heading_path": [*list(previous.get("heading_path") or [])[:-1], repair["title"]],
            "repaired": True,
            "repair_type": "previous_problem_absorption",
        }
        result.insert(previous_position + 1, new_group)
    return sorted(result, key=lambda group: (int(group.get("start_line") or 0), int(group.get("problem_index") or 0)))


def repair_exercise_structure(
    markdown: str,
    exercise_report: dict[str, Any],
    *,
    llm_client: Any | None = None,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
) -> dict[str, Any]:
    lines = markdown.splitlines()
    groups = _sorted_groups(exercise_report)
    descriptors = _repair_candidate_descriptors(exercise_report, groups)
    report: dict[str, Any] = {
        "enabled": llm_client is not None,
        "model": getattr(llm_client, "model", None) if llm_client is not None else None,
        "candidate_count": 0,
        "applied_count": 0,
        "skipped_count": 0,
        "candidates": [],
        "applied": [],
        "skipped": [],
        "warnings": [],
    }

    repairs: list[dict[str, Any]] = []
    for descriptor in descriptors:
        missing_index = _safe_int(descriptor.get("target_problem_index"))
        if missing_index is None:
            report["skipped"].append({"target_problem_index": None, "reason": "missing_target_problem_index"})
            continue
        candidate = _candidate_from_descriptor(lines=lines, groups=groups, descriptor=descriptor)
        if candidate is None:
            report["skipped"].append({"target_problem_index": missing_index, "reason": "missing_previous_problem"})
            continue
        previous = candidate["previous_problem"]
        next_group = candidate.get("next_problem")
        report["candidate_count"] += 1
        report["candidates"].append(
            {
                "target_problem_index": missing_index,
                "candidate_type": candidate["candidate_type"],
                "previous_problem_index": previous.get("problem_index"),
                "next_problem_index": next_group.get("problem_index") if next_group else None,
                "marker_evidence_count": len(candidate["marker_evidence"]),
            }
        )
        if llm_client is None:
            report["skipped"].append({"target_problem_index": missing_index, "reason": "llm_client_unavailable"})
            continue
        try:
            judgement = llm_client.judge_problem_boundary(deepcopy(candidate))
        except Exception as exc:
            report["warnings"].append(f"llm_boundary_judgement_error:{exc.__class__.__name__}")
            report["skipped"].append({"target_problem_index": missing_index, "reason": "llm_error"})
            continue
        accepted, reason, normalized = _validate_judgement(
            judgement if isinstance(judgement, dict) else {},
            candidate=candidate,
            lines=lines,
            min_confidence=min_confidence,
        )
        if not accepted:
            local_repair = _local_high_confidence_repair(candidate, lines=lines)
            if local_repair is not None:
                repairs.append(local_repair)
                report["applied"].append(
                    {
                        "target_problem_index": local_repair["target_problem_index"],
                        "start_line": local_repair["start_line"],
                        "end_line": local_repair["end_line"],
                        "confidence": local_repair["confidence"],
                        "title": local_repair["title"],
                        "reason_codes": local_repair["reason_codes"],
                    }
                )
                continue
            skipped = {"target_problem_index": missing_index, "reason": reason}
            skipped.update(normalized)
            report["skipped"].append(skipped)
            continue
        repairs.append(normalized)
        report["applied"].append(
            {
                "target_problem_index": normalized["target_problem_index"],
                "start_line": normalized["start_line"],
                "end_line": normalized["end_line"],
                "confidence": normalized["confidence"],
                "title": normalized["title"],
                "reason_codes": normalized["reason_codes"],
            }
        )

    repaired_groups = _apply_repairs(groups, repairs)
    report["applied_count"] = len(report["applied"])
    report["skipped_count"] = len(report["skipped"])
    if report["candidate_count"] and report["applied_count"] == 0:
        report["warnings"].append("exercise_structure_repair_no_candidates_applied")

    return {"problem_groups": repaired_groups, "report": report}
