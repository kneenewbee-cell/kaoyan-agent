from __future__ import annotations

import math
from typing import Any


AI_REVIEW_PLAN_CANDIDATE_TYPES = (
    "weak_topics",
    "wrong_questions",
    "pending_review_items",
    "review_tasks",
    "draft_attempts",
    "unstarted_questions",
    "startup_candidates",
    "favorite_unmastered",
)


FRONTEND_INCLUDE_TYPE_ALIASES: dict[str, str] = {
    "due_tasks": "review_tasks",
    "review": "review_tasks",
    "reviews": "review_tasks",
    "pending_review": "pending_review_items",
    "pending_reviews": "pending_review_items",
    "wrong": "wrong_questions",
    "wrong_book": "wrong_questions",
    "mistakes": "wrong_questions",
    "weak": "weak_topics",
    "weakness": "weak_topics",
    "topic": "weak_topics",
    "topics": "weak_topics",
    "unstarted": "unstarted_questions",
    "new_questions": "unstarted_questions",
    "not_started": "unstarted_questions",
    "startup": "startup_candidates",
    "startup_questions": "startup_candidates",
    "draft": "draft_attempts",
    "drafts": "draft_attempts",
    "unfinished_practice": "draft_attempts",
    "favorite": "favorite_unmastered",
    "favorites": "favorite_unmastered",
}


AI_CANDIDATE_LIMIT_FIELD_BY_TYPE: dict[str, str] = {
    "weak_topics": "ai_weak_topic_limit",
    "wrong_questions": "ai_wrong_question_limit",
    "pending_review_items": "ai_pending_review_limit",
    "review_tasks": "ai_review_task_limit",
    "draft_attempts": "ai_draft_attempt_limit",
    "unstarted_questions": "ai_unstarted_question_limit",
    "startup_candidates": "ai_startup_candidate_limit",
    "favorite_unmastered": "ai_favorite_unmastered_limit",
}


AI_CANDIDATE_LIMIT_BOUNDS: dict[str, tuple[int, int]] = {
    "weak_topics": (5, 24),
    "wrong_questions": (8, 90),
    "pending_review_items": (5, 60),
    "review_tasks": (5, 60),
    "draft_attempts": (4, 50),
    "unstarted_questions": (8, 120),
    "startup_candidates": (8, 100),
    "favorite_unmastered": (4, 50),
}


MODE_CANDIDATE_TYPE_WEIGHTS: dict[str, dict[str, float]] = {
    "balanced": {
        "review_tasks": 1.00,
        "wrong_questions": 1.05,
        "weak_topics": 1.00,
        "pending_review_items": 0.85,
        "draft_attempts": 0.80,
        "favorite_unmastered": 0.55,
        "unstarted_questions": 0.55,
        "startup_candidates": 0.45,
    },
    "weak": {
        "weak_topics": 1.50,
        "wrong_questions": 1.15,
        "pending_review_items": 0.85,
        "review_tasks": 0.70,
        "draft_attempts": 0.65,
        "favorite_unmastered": 0.50,
    },
    "wrong": {
        "wrong_questions": 1.50,
        "pending_review_items": 1.05,
        "review_tasks": 0.75,
        "draft_attempts": 0.55,
        "favorite_unmastered": 0.45,
    },
    "startup": {
        "unstarted_questions": 1.45,
        "startup_candidates": 1.15,
        "review_tasks": 0.45,
        "draft_attempts": 0.45,
        "favorite_unmastered": 0.35,
    },
    "sprint": {
        "review_tasks": 1.35,
        "wrong_questions": 1.25,
        "weak_topics": 1.05,
        "pending_review_items": 0.85,
        "favorite_unmastered": 0.75,
        "draft_attempts": 0.65,
    },
}


MODE_TYPE_PRIORITY: dict[str, list[str]] = {
    "balanced": [
        "review_tasks",
        "wrong_questions",
        "weak_topics",
        "pending_review_items",
        "draft_attempts",
        "favorite_unmastered",
        "unstarted_questions",
        "startup_candidates",
    ],
    "weak": [
        "weak_topics",
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "draft_attempts",
        "favorite_unmastered",
    ],
    "wrong": [
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "draft_attempts",
        "favorite_unmastered",
    ],
    "startup": [
        "unstarted_questions",
        "startup_candidates",
        "review_tasks",
        "draft_attempts",
        "favorite_unmastered",
    ],
    "sprint": [
        "review_tasks",
        "wrong_questions",
        "pending_review_items",
        "weak_topics",
        "favorite_unmastered",
        "draft_attempts",
    ],
}


MODE_POLICIES: dict[str, dict[str, Any]] = {
    "balanced": {
        "label": "balanced",
        "enabled_types": list(AI_REVIEW_PLAN_CANDIDATE_TYPES),
        "disabled_types": [],
        "intent": "Mix due reviews, weak topics, wrong questions, drafts, and a small amount of new-start work.",
    },
    "weak": {
        "label": "weak_first",
        "enabled_types": [
            "weak_topics",
            "wrong_questions",
            "pending_review_items",
            "review_tasks",
            "draft_attempts",
            "favorite_unmastered",
        ],
        "disabled_types": ["unstarted_questions", "startup_candidates"],
        "intent": "Prioritize weak topics and their related risky questions.",
    },
    "wrong": {
        "label": "wrong_recycle",
        "enabled_types": [
            "wrong_questions",
            "pending_review_items",
            "review_tasks",
            "draft_attempts",
            "favorite_unmastered",
        ],
        "disabled_types": ["weak_topics", "unstarted_questions", "startup_candidates"],
        "intent": "Recycle wrong and pending-review work without introducing ordinary new questions.",
    },
    "startup": {
        "label": "new_start",
        "enabled_types": [
            "unstarted_questions",
            "startup_candidates",
            "review_tasks",
            "draft_attempts",
            "favorite_unmastered",
        ],
        "disabled_types": ["weak_topics", "wrong_questions", "pending_review_items"],
        "intent": "Use unstarted candidates when the user has little or no history.",
    },
    "sprint": {
        "label": "exam_sprint",
        "enabled_types": [
            "weak_topics",
            "wrong_questions",
            "pending_review_items",
            "review_tasks",
            "draft_attempts",
            "favorite_unmastered",
        ],
        "disabled_types": ["unstarted_questions", "startup_candidates"],
        "intent": "Prefer due work, wrong questions, weak topics, and favorite-unmastered items.",
    },
}


MODE_READINESS_RULES: dict[str, dict[str, Any]] = {
    "balanced": {
        "core_types": list(AI_REVIEW_PLAN_CANDIDATE_TYPES),
        "core_ratio": 0.30,
        "ready_coverage": 0.35,
        "weak_coverage": 0.05,
    },
    "weak": {
        "core_types": ["weak_topics", "wrong_questions", "pending_review_items", "draft_attempts"],
        "core_ratio": 0.60,
        "ready_coverage": 0.60,
        "weak_coverage": 0.10,
    },
    "wrong": {
        "core_types": ["wrong_questions", "pending_review_items", "review_tasks", "draft_attempts"],
        "core_ratio": 0.70,
        "ready_coverage": 0.60,
        "weak_coverage": 0.10,
    },
    "startup": {
        "core_types": ["unstarted_questions", "startup_candidates"],
        "core_ratio": 0.70,
        "ready_coverage": 0.60,
        "weak_coverage": 0.10,
    },
    "sprint": {
        "core_types": [
            "review_tasks",
            "wrong_questions",
            "pending_review_items",
            "weak_topics",
            "favorite_unmastered",
            "draft_attempts",
        ],
        "core_ratio": 0.60,
        "ready_coverage": 0.60,
        "weak_coverage": 0.10,
    },
}


def normalize_ai_review_plan_mode(mode: Any) -> str:
    normalized = str(mode or "balanced").strip().lower()
    aliases = {
        "balance": "balanced",
        "weak_first": "weak",
        "weakness": "weak",
        "wrong_recycle": "wrong",
        "mistakes": "wrong",
        "new": "startup",
        "new_start": "startup",
        "start": "startup",
        "exam": "sprint",
        "exam_sprint": "sprint",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in MODE_POLICIES else "balanced"


def normalize_include_types(include_types: Any) -> list[str]:
    if include_types is None:
        return []
    raw_values: list[Any]
    if isinstance(include_types, str):
        raw_values = include_types.split(",")
    elif isinstance(include_types, (list, tuple, set)):
        raw_values = list(include_types)
    else:
        raw_values = [include_types]
    allowed = set(AI_REVIEW_PLAN_CANDIDATE_TYPES)
    seen: set[str] = set()
    normalized: list[str] = []
    for value in raw_values:
        key = str(value or "").strip()
        key = FRONTEND_INCLUDE_TYPE_ALIASES.get(key, key)
        if not key or key not in allowed or key in seen:
            continue
        seen.add(key)
        normalized.append(key)
    return normalized


def _ordered_enabled_types(normalized_mode: str, enabled: list[str]) -> list[str]:
    enabled_set = set(enabled)
    ordered: list[str] = [
        candidate_type
        for candidate_type in MODE_TYPE_PRIORITY.get(normalized_mode, [])
        if candidate_type in enabled_set
    ]
    ordered_set = set(ordered)
    ordered.extend(candidate_type for candidate_type in enabled if candidate_type not in ordered_set)
    return ordered


def build_ai_review_plan_policy(mode: Any, include_types: Any = None) -> dict[str, Any]:
    normalized_mode = normalize_ai_review_plan_mode(mode)
    base = MODE_POLICIES[normalized_mode]
    enabled = [str(value) for value in base.get("enabled_types") or []]
    disabled = [str(value) for value in base.get("disabled_types") or []]
    requested = normalize_include_types(include_types)
    ignored_requested: list[str] = []
    if requested:
        enabled = [value for value in enabled if value in requested]
        ignored_requested = [value for value in requested if value not in set(enabled)]
        disabled = sorted(set(disabled).union(set(ignored_requested)))
    enabled_set = set(enabled)
    disabled = [value for value in AI_REVIEW_PLAN_CANDIDATE_TYPES if value in set(disabled) or value not in enabled_set]
    return {
        "mode": normalized_mode,
        "label": str(base.get("label") or normalized_mode),
        "intent": str(base.get("intent") or ""),
        "requested_types": requested,
        "enabled_types": enabled,
        "ignored_requested_types": ignored_requested,
        "disabled_types": disabled,
        "type_priority": _ordered_enabled_types(normalized_mode, enabled),
    }


def filter_ai_review_plan_candidates(
    candidates: dict[str, list[dict[str, Any]]],
    policy: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    enabled = set(str(value) for value in policy.get("enabled_types") or [])
    return {
        candidate_type: list(candidates.get(candidate_type) or []) if candidate_type in enabled else []
        for candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES
    }


def _planning_tasks_per_day(daily_minutes: int) -> int:
    safe_daily_minutes = max(15, min(int(daily_minutes or 60), 240))
    if safe_daily_minutes <= 30:
        return 4
    if safe_daily_minutes <= 45:
        return 6
    if safe_daily_minutes <= 90:
        return 8
    return 10


def _planning_candidate_budget(days: int, daily_minutes: int) -> int:
    safe_days = max(1, min(int(days or 7), 30))
    safe_daily_minutes = max(15, min(int(daily_minutes or 60), 240))
    plan_slots = safe_days * _planning_tasks_per_day(safe_daily_minutes)
    # More days need a wider planning context, but cap it so the LLM input stays bounded.
    return min(220, max(30, math.ceil(20 + plan_slots * 4.0 + math.sqrt(safe_days) * 3.0)))


def build_ai_candidate_limits(
    policy: dict[str, Any],
    *,
    days: int = 7,
    daily_minutes: int = 60,
) -> dict[str, Any]:
    """Build mode-aware, user-selection-aware candidate limits for the AI context."""

    mode = normalize_ai_review_plan_mode(policy.get("mode"))
    safe_days = max(1, min(int(days or 7), 30))
    safe_daily_minutes = max(15, min(int(daily_minutes or 60), 240))
    tasks_per_day = _planning_tasks_per_day(safe_daily_minutes)
    total_budget = _planning_candidate_budget(safe_days, safe_daily_minutes)
    enabled = [
        candidate_type
        for candidate_type in (policy.get("type_priority") or policy.get("enabled_types") or [])
        if candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES
    ]
    enabled_set = set(enabled)
    weights = MODE_CANDIDATE_TYPE_WEIGHTS.get(mode, MODE_CANDIDATE_TYPE_WEIGHTS["balanced"])
    weight_sum = sum(max(0.1, float(weights.get(candidate_type, 0.35))) for candidate_type in enabled)
    type_limits = {candidate_type: 0 for candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES}
    type_weights: dict[str, float] = {}

    if weight_sum > 0:
        for candidate_type in enabled:
            min_limit, max_limit = AI_CANDIDATE_LIMIT_BOUNDS[candidate_type]
            weight = max(0.1, float(weights.get(candidate_type, 0.35)))
            type_weights[candidate_type] = weight
            share = math.ceil(total_budget * weight / weight_sum)
            type_limits[candidate_type] = max(min_limit, min(max_limit, share))

    limits: dict[str, Any] = {
        "ui_weak_topic_limit": 5,
        "ui_action_limit": 5,
        "ai_total_candidate_budget": total_budget,
        "candidate_type_limits": type_limits,
        "candidate_type_weights": {
            candidate_type: round(type_weights.get(candidate_type, 0.0), 4)
            for candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES
        },
        "candidate_budget_basis": {
            "days": safe_days,
            "daily_minutes": safe_daily_minutes,
            "tasks_per_day": tasks_per_day,
            "plan_slots": safe_days * tasks_per_day,
            "enabled_type_count": len(enabled_set),
        },
    }
    for candidate_type, field_name in AI_CANDIDATE_LIMIT_FIELD_BY_TYPE.items():
        limits[field_name] = type_limits[candidate_type]
    return limits


def assess_ai_review_plan_readiness(
    candidates: dict[str, list[dict[str, Any]]],
    policy: dict[str, Any],
    *,
    days: int = 7,
    daily_minutes: int = 60,
    practice_volume: int | None = None,
) -> dict[str, Any]:
    """Score whether the selected planning mode has enough data to call the LLM."""

    mode = normalize_ai_review_plan_mode(policy.get("mode"))
    rule = MODE_READINESS_RULES.get(mode, MODE_READINESS_RULES["balanced"])
    enabled = set(str(value) for value in policy.get("enabled_types") or [])
    core_types = [value for value in rule["core_types"] if not enabled or value in enabled]
    safe_days = max(1, min(int(days or 7), 30))
    safe_daily_minutes = max(15, min(int(daily_minutes or 60), 240))
    tasks_per_day = _planning_tasks_per_day(safe_daily_minutes)
    plan_slots = safe_days * tasks_per_day
    readiness_slots = safe_days * min(tasks_per_day, 3)
    core_required = max(1, math.ceil(readiness_slots * float(rule["core_ratio"])))
    core_available = sum(_candidate_count(candidates.get(candidate_type)) for candidate_type in core_types)
    enabled_available = sum(
        _candidate_count(candidates.get(candidate_type))
        for candidate_type in (enabled or set(AI_REVIEW_PLAN_CANDIDATE_TYPES))
    )
    coverage = min(1.0, core_available / max(1, core_required))
    ready_coverage = float(rule["ready_coverage"])
    weak_coverage = float(rule["weak_coverage"])
    safe_practice_volume = max(0, int(practice_volume or 0))

    if enabled_available <= 0:
        status = "blocked"
        reason = "当前范围没有可用于该模式的候选数据。"
    elif core_available <= 0:
        status = "blocked"
        reason = "当前模式的核心数据为空，继续生成会缺少依据。"
    elif coverage >= ready_coverage:
        status = "ready"
        reason = "当前数据足以支撑该模式生成规划。"
    elif coverage >= weak_coverage:
        status = "weak"
        reason = "当前核心数据偏少，适合生成短计划或允许混入其他类型。"
    else:
        status = "blocked"
        reason = "当前核心数据过少，建议先换模式、缩短计划或扩大范围。"

    if mode == "sprint" and status == "ready" and safe_practice_volume < 15:
        status = "weak"
        reason = "当前练习记录偏少，考前冲刺可以生成，但应按短计划或诊断计划处理。"

    return {
        "status": status,
        "should_call_llm": status in {"ready", "weak"},
        "mode": mode,
        "plan_slots": plan_slots,
        "tasks_per_day": tasks_per_day,
        "core_types": core_types,
        "core_available": core_available,
        "core_required": core_required,
        "enabled_available": enabled_available,
        "practice_volume": safe_practice_volume,
        "coverage": round(coverage, 4),
        "reason": reason,
        "recommended_actions": _readiness_recommended_actions(status, mode),
    }


def _candidate_count(values: Any) -> int:
    return len(values) if isinstance(values, list) else 0


def _readiness_recommended_actions(status: str, mode: str) -> list[str]:
    if status == "ready":
        return ["生成规划"]
    if status == "weak":
        actions = ["缩短计划天数", "允许混入其他类型", "扩大题库范围"]
        if mode != "balanced":
            actions.append("切换到均衡推进")
        return actions
    if mode == "wrong":
        return ["切换到均衡推进", "切换到新题启动", "扩大题库范围"]
    if mode == "startup":
        return ["扩大题库范围", "切换到均衡推进", "复习已做题"]
    if mode == "weak":
        return ["先做诊断练习", "切换到新题启动", "扩大题库范围"]
    return ["切换模式", "扩大题库范围", "缩短计划天数"]
