from __future__ import annotations

from collections import Counter
from typing import Any


MIN_QUESTION_LOAD_UNITS = 0.55
MAX_QUESTION_LOAD_UNITS = 2.8
MINUTES_PER_LOAD_UNIT = 7.2
PRACTICE_SHEET_SPLIT_RATIO = 1.15

MIN_QUESTION_MINUTES = 1.5
MAX_QUESTION_MINUTES = 30.0

QUESTION_TYPE_ALIASES: dict[str, str] = {
    "blank": "fill_blank",
    "calculation": "solution",
    "choice": "single_choice",
    "comprehensive": "solution",
    "fill_blank": "fill_blank",
    "proof": "solution",
    "short_answer": "solution",
    "single_choice": "single_choice",
    "solution": "solution",
    "true_false": "single_choice",
    "unknown": "single_choice",
}

QUESTION_BASE_MINUTES: dict[str, dict[str, float]] = {
    "single_choice": {
        "easy": 3.0,
        "medium": 4.0,
        "unknown": 4.0,
        "hard": 5.0,
        "very_hard": 5.0,
    },
    "fill_blank": {
        "easy": 4.0,
        "medium": 5.0,
        "unknown": 5.0,
        "hard": 6.0,
        "very_hard": 6.0,
    },
    "solution": {
        "easy": 10.0,
        "medium": 12.0,
        "unknown": 12.0,
        "hard": 15.0,
        "very_hard": 15.0,
    },
}

STATE_WEIGHTS: dict[str, float] = {
    "mastered_review": 0.7,
    "unstarted": 1.0,
    "not_started": 1.0,
    "learning": 1.0,
    "draft_unanswered": 1.05,
    "pending_review": 1.2,
    "favorite_unmastered": 1.15,
    "wrong": 1.3,
    "repeat_wrong": 1.5,
    "unknown": 1.0,
}

TASK_OVERHEAD_MINUTES: dict[str, float] = {
    "single_question": 0.0,
    "practice_set": 3.0,
    "continue_draft": 2.0,
    "topic_review": 5.0,
    "review_batch": 2.0,
}

CANDIDATE_TYPE_DEFAULT_STATE: dict[str, str] = {
    "weak_topics": "learning",
    "wrong_questions": "wrong",
    "pending_review_items": "pending_review",
    "review_tasks": "mastered_review",
    "draft_attempts": "draft_unanswered",
    "unstarted_questions": "unstarted",
    "startup_candidates": "unstarted",
    "favorite_unmastered": "favorite_unmastered",
}

CANDIDATE_TYPE_TASK_KIND: dict[str, str] = {
    "weak_topics": "topic_review",
    "wrong_questions": "single_question",
    "pending_review_items": "single_question",
    "review_tasks": "review_batch",
    "draft_attempts": "continue_draft",
    "unstarted_questions": "practice_set",
    "startup_candidates": "practice_set",
    "favorite_unmastered": "practice_set",
}


def calculate_question_load_units(question: dict[str, Any], state: str | None = None) -> float:
    question_type = _normalize_question_type(
        question.get("question_type")
        or question.get("type")
        or question.get("answer_type")
        or "unknown"
    )
    normalized_state = _normalize_state(state or question.get("state") or question.get("review_state"))
    difficulty = _normalize_difficulty(question.get("difficulty") or "unknown")
    base_minutes = QUESTION_BASE_MINUTES[question_type][difficulty]
    weighted_minutes = base_minutes * STATE_WEIGHTS.get(normalized_state, STATE_WEIGHTS["unknown"])
    clamped_minutes = max(MIN_QUESTION_MINUTES, min(MAX_QUESTION_MINUTES, weighted_minutes))
    return round(clamped_minutes / MINUTES_PER_LOAD_UNIT, 8)


def calculate_candidate_load(
    candidate: dict[str, Any],
    candidate_type: str | None = None,
) -> dict[str, Any]:
    safe_candidate_type = _normalize_key(candidate_type or candidate.get("candidate_type") or "")
    default_state = _candidate_state(candidate, safe_candidate_type)
    questions = _candidate_questions(candidate)
    question_count = len(questions)
    type_mix: Counter[str] = Counter()
    state_mix: Counter[str] = Counter()
    difficulty_mix: Counter[str] = Counter()
    question_units: list[float] = []

    for question in questions:
        question_state = _normalize_state(question.get("state") or default_state)
        question_type = _normalize_question_type(question.get("question_type") or question.get("type") or "unknown")
        difficulty = _normalize_key(question.get("difficulty") or "unknown")
        type_mix[question_type] += 1
        state_mix[question_state] += 1
        difficulty_mix[difficulty] += 1
        question_units.append(calculate_question_load_units(question, question_state))

    task_kind = _candidate_task_kind(candidate, safe_candidate_type, question_count)
    overhead_units = _candidate_overhead_minutes(task_kind, question_count) / MINUTES_PER_LOAD_UNIT
    raw_load_units = sum(question_units) + overhead_units
    load_units = round(raw_load_units, 2)
    estimated_minutes = estimate_minutes_from_load(raw_load_units)
    return {
        "question_count": question_count,
        "question_type_mix": dict(type_mix),
        "state_mix": dict(state_mix),
        "difficulty_mix": dict(difficulty_mix),
        "load_units": load_units,
        "estimated_minutes": estimated_minutes,
        "task_kind": task_kind,
        "splittable": question_count > 1,
    }


def estimate_minutes_from_load(load_units: float) -> int:
    try:
        parsed = float(load_units)
    except (TypeError, ValueError):
        parsed = 0.0
    return max(0, int(round((parsed * MINUTES_PER_LOAD_UNIT) + 1e-6)))


def split_candidate_into_plan_segments(
    candidate: dict[str, Any],
    *,
    daily_minutes: int,
    days: int,
    candidate_type: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    safe_daily_minutes = max(15, int(daily_minutes or 60))
    safe_days = max(1, int(days or 1))
    safe_candidate_type = _normalize_key(candidate_type or candidate.get("candidate_type") or "")
    questions = _candidate_questions(candidate)
    enriched = _candidate_with_load(candidate, safe_candidate_type, questions)
    daily_target_units = safe_daily_minutes / MINUTES_PER_LOAD_UNIT
    if (
        enriched["load_units"] <= daily_target_units * PRACTICE_SHEET_SPLIT_RATIO
        or len(questions) <= 1
    ):
        return [enriched], []

    default_state = _candidate_state(candidate, safe_candidate_type)
    parent_id = _candidate_identifier(candidate)
    parent_practice_set_id = str(
        candidate.get("parent_practice_set_id")
        or candidate.get("practice_set_id")
        or candidate.get("set_id")
        or parent_id
    ).strip()
    max_part_units = daily_target_units * 0.98
    buckets: list[list[dict[str, Any]]] = []
    current_bucket: list[dict[str, Any]] = []
    current_units = 0.0
    for question in questions:
        question_units = calculate_question_load_units(question, question.get("state") or default_state)
        if current_bucket and current_units + question_units > max_part_units:
            buckets.append(current_bucket)
            current_bucket = []
            current_units = 0.0
        current_bucket.append(dict(question))
        current_units += question_units
    if current_bucket:
        buckets.append(current_bucket)

    all_segments = [
        _build_segment_candidate(
            candidate,
            safe_candidate_type,
            bucket,
            parent_id=parent_id,
            parent_practice_set_id=parent_practice_set_id,
            part_index=index,
            part_count=len(buckets),
            status="planned",
        )
        for index, bucket in enumerate(buckets, start=1)
    ]

    planned: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    capacity_units = safe_days * daily_target_units
    used_units = 0.0
    for segment in all_segments:
        segment_units = float(segment.get("load_units") or 0)
        if planned and used_units + segment_units > capacity_units:
            pending.append({**segment, "status": "later_pending"})
            continue
        planned.append(segment)
        used_units += segment_units
    return planned, pending


def _candidate_with_load(
    candidate: dict[str, Any],
    candidate_type: str,
    questions: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = calculate_candidate_load({**candidate, "questions": questions}, candidate_type)
    source_id = _candidate_identifier(candidate)
    enriched = {
        **candidate,
        "candidate_type": candidate.get("candidate_type") or candidate_type or "",
        "candidate_pool_type": candidate_type or candidate.get("candidate_type") or "",
        "source_id": source_id,
        "candidate_id": str(candidate.get("candidate_id") or source_id),
        **loaded,
    }
    if questions:
        enriched["question_ids"] = [str(q.get("question_id") or q.get("id") or "") for q in questions if str(q.get("question_id") or q.get("id") or "").strip()]
    return enriched


def _build_segment_candidate(
    candidate: dict[str, Any],
    candidate_type: str,
    questions: list[dict[str, Any]],
    *,
    parent_id: str,
    parent_practice_set_id: str,
    part_index: int,
    part_count: int,
    status: str,
) -> dict[str, Any]:
    safe_parent_id = _safe_segment_token(parent_id)
    segment_id = f"{safe_parent_id}__seg_{part_index}"
    title = str(candidate.get("title") or candidate.get("practice_set_title") or parent_id or "Practice sheet").strip()
    planned_question_ids = [
        str(question.get("question_id") or question.get("id") or "").strip()
        for question in questions
        if str(question.get("question_id") or question.get("id") or "").strip()
    ]
    loaded = calculate_candidate_load(
        {
            **candidate,
            "questions": questions,
            "question_ids": planned_question_ids,
        },
        candidate_type,
    )
    return {
        **candidate,
        "candidate_type": candidate.get("candidate_type") or candidate_type or "",
        "candidate_pool_type": candidate_type or candidate.get("candidate_type") or "",
        "source_id": segment_id,
        "candidate_id": segment_id,
        "plan_segment_id": segment_id,
        "parent_source_id": parent_id,
        "parent_practice_set_id": parent_practice_set_id,
        "part_index": part_index,
        "part_count": part_count,
        "planned_question_ids": planned_question_ids,
        "question_ids": planned_question_ids,
        "questions": questions,
        "title": f"{title} - Part {part_index}/{part_count}",
        "status": status,
        **loaded,
    }


def _candidate_questions(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("questions", "question_details", "items"):
        values = candidate.get(key)
        if isinstance(values, list) and values:
            return [dict(item) for item in values if isinstance(item, dict)]

    question_ids = candidate.get("question_ids") if isinstance(candidate.get("question_ids"), list) else []
    count = _positive_count(
        candidate.get("unanswered_count")
        or candidate.get("question_count")
        or len(question_ids)
        or 1
    )
    questions: list[dict[str, Any]] = []
    for index in range(count):
        question_id = str(question_ids[index]).strip() if index < len(question_ids) else ""
        questions.append(
            {
                "question_id": question_id,
                "question_type": candidate.get("question_type") or candidate.get("type") or "unknown",
                "difficulty": candidate.get("difficulty") or "unknown",
                "state": candidate.get("state") or candidate.get("review_state") or "unknown",
            }
        )
    return questions


def _candidate_identifier(candidate: dict[str, Any]) -> str:
    for key in (
        "source_id",
        "candidate_id",
        "plan_segment_id",
        "question_id",
        "task_id",
        "attempt_id",
        "set_id",
        "practice_set_id",
        "topic",
    ):
        value = str(candidate.get(key) or "").strip()
        if value:
            return value
    return "candidate"


def _candidate_state(candidate: dict[str, Any], candidate_type: str) -> str:
    explicit = candidate.get("state") or candidate.get("review_state")
    if explicit:
        return _normalize_state(explicit)
    if candidate.get("repeat_wrong_count") or candidate.get("consecutive_wrong_count"):
        return "repeat_wrong"
    return CANDIDATE_TYPE_DEFAULT_STATE.get(candidate_type, "unknown")


def _candidate_task_kind(candidate: dict[str, Any], candidate_type: str, question_count: int) -> str:
    explicit_value = candidate.get("task_kind") or candidate.get("task_type")
    if explicit_value:
        return _normalize_key(explicit_value)
    if candidate_type == "weak_topics":
        return "topic_review"
    if candidate_type == "review_tasks":
        return "review_batch"
    if candidate_type == "draft_attempts":
        return "continue_draft"
    if question_count <= 1:
        return "single_question"
    return CANDIDATE_TYPE_TASK_KIND.get(candidate_type, "practice_set" if question_count > 1 else "single_question")


def _candidate_overhead_minutes(task_kind: str, question_count: int) -> float:
    if task_kind == "single_question" or question_count <= 1:
        return 0.0
    if task_kind == "practice_set":
        return 1.0 if question_count <= 3 else TASK_OVERHEAD_MINUTES["practice_set"]
    return TASK_OVERHEAD_MINUTES.get(task_kind, 0.0)


def _normalize_state(value: Any) -> str:
    normalized = _normalize_key(value or "unknown")
    if normalized in {"incorrect", "wrong_question"}:
        return "wrong"
    if normalized in {"consecutive_wrong", "repeat_incorrect", "repeated_wrong"}:
        return "repeat_wrong"
    if normalized in {"pending", "needs_review", "needs_grading"}:
        return "pending_review"
    return normalized


def _normalize_question_type(value: Any) -> str:
    normalized = _normalize_key(value or "unknown")
    return QUESTION_TYPE_ALIASES.get(normalized, "single_choice")


def _normalize_difficulty(value: Any) -> str:
    normalized = _normalize_key(value or "unknown")
    if normalized in {"easy", "hard", "very_hard"}:
        return normalized
    return "medium" if normalized in {"normal", "medium"} else "unknown"


def _normalize_key(value: Any) -> str:
    return str(value or "unknown").strip().lower().replace("-", "_").replace(" ", "_") or "unknown"


def _positive_count(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = 1
    return max(1, min(999, parsed))


def _safe_segment_token(value: Any) -> str:
    token = str(value or "candidate").strip()
    safe = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in token).strip("_")
    return safe or "candidate"
