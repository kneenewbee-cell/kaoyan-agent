from __future__ import annotations

from typing import Any

from .system_review_plan_policy import (
    AI_REVIEW_PLAN_CANDIDATE_TYPES,
    assess_ai_review_plan_readiness,
    build_ai_review_plan_policy,
    filter_ai_review_plan_candidates,
)
from .system_review_plan_load import calculate_candidate_load


EVALUATION_MODES = ("balanced", "weak", "wrong", "startup", "sprint")

MODE_PREFERRED_TYPES: dict[str, tuple[str, ...]] = {
    "balanced": (
        "review_tasks",
        "wrong_questions",
        "weak_topics",
        "pending_review_items",
        "draft_attempts",
        "unstarted_questions",
        "startup_candidates",
        "favorite_unmastered",
    ),
    "weak": (
        "weak_topics",
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "favorite_unmastered",
    ),
    "wrong": (
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "draft_attempts",
        "favorite_unmastered",
    ),
    "startup": (
        "unstarted_questions",
        "startup_candidates",
        "review_tasks",
        "draft_attempts",
        "favorite_unmastered",
    ),
    "sprint": (
        "review_tasks",
        "wrong_questions",
        "pending_review_items",
        "weak_topics",
        "favorite_unmastered",
        "draft_attempts",
    ),
}

MODE_PRIMARY_BUDGET_TYPES: dict[str, tuple[str, ...]] = {
    "balanced": AI_REVIEW_PLAN_CANDIDATE_TYPES,
    "weak": (
        "weak_topics",
        "wrong_questions",
        "pending_review_items",
    ),
    "wrong": (
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "draft_attempts",
    ),
    "startup": (
        "unstarted_questions",
        "startup_candidates",
    ),
    "sprint": (
        "review_tasks",
        "wrong_questions",
        "pending_review_items",
        "weak_topics",
        "favorite_unmastered",
        "draft_attempts",
    ),
}

MODE_TOP_PRIMARY_RATIO_FLOOR: dict[str, float] = {
    "balanced": 0.0,
    "weak": 0.70,
    "wrong": 0.70,
    "startup": 0.70,
    "sprint": 0.80,
}


_CATEGORY_SPECS: tuple[tuple[str, int, dict[str, Any]], ...] = (
    (
        "cold_start",
        10,
        {
            "practice_volume": 0,
            "wrong_level": "none",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "none",
            "manual_state_level": "none",
        },
    ),
    (
        "strong",
        8,
        {
            "practice_volume": 80,
            "wrong_level": "low",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "low",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
        },
    ),
    (
        "heavy_wrong",
        10,
        {
            "practice_volume": 60,
            "wrong_level": "high",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "high",
            "manual_state_level": "medium",
        },
    ),
    (
        "low_volume_concentrated",
        6,
        {
            "practice_volume": 8,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "none",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "high",
            "manual_state_level": "low",
        },
    ),
    (
        "review_pressure",
        9,
        {
            "practice_volume": 35,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "high",
            "draft_level": "medium",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
        },
    ),
    (
        "skip_unanswered",
        6,
        {
            "practice_volume": 30,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "high",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "low",
        },
    ),
    (
        "scope_bias",
        6,
        {
            "practice_volume": 45,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "narrow",
            "manual_state_level": "high",
        },
    ),
    (
        "edge_cases",
        5,
        {
            "practice_volume": 15,
            "wrong_level": "mixed",
            "pending_review_level": "high",
            "overdue_level": "mixed",
            "draft_level": "mixed",
            "unstarted_level": "mixed",
            "topic_concentration": "mixed",
            "manual_state_level": "mixed",
        },
    ),
    (
        "all_done_no_new",
        4,
        {
            "practice_volume": 120,
            "wrong_level": "low",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "none",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "all_done",
            "scope_profile": "full_coverage",
            "learning_trait": "no_new_questions_left",
        },
    ),
    (
        "no_wrong_history",
        4,
        {
            "practice_volume": 45,
            "wrong_level": "none",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "balanced",
            "manual_state_level": "low",
            "completion_state": "has_practice_no_wrong",
            "scope_profile": "normal",
            "learning_trait": "wrong_mode_mismatch",
        },
    ),
    (
        "pending_review_heavy",
        4,
        {
            "practice_volume": 35,
            "wrong_level": "low",
            "pending_review_level": "high",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "low",
            "completion_state": "submitted_needs_confirmation",
            "scope_profile": "normal",
            "learning_trait": "grading_uncertain",
        },
    ),
    (
        "favorite_unmastered_heavy",
        4,
        {
            "practice_volume": 55,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "narrow",
            "manual_state_level": "high",
            "completion_state": "manual_focus",
            "scope_profile": "favorite_clustered",
            "learning_trait": "收藏多但未掌握",
        },
    ),
    (
        "overdue_neglect",
        4,
        {
            "practice_volume": 20,
            "wrong_level": "low",
            "pending_review_level": "low",
            "overdue_level": "high",
            "draft_level": "medium",
            "unstarted_level": "high",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "review_backlog",
            "scope_profile": "normal",
            "learning_trait": "复习任务长期拖延",
        },
    ),
    (
        "high_volume_unstable",
        4,
        {
            "practice_volume": 120,
            "wrong_level": "high",
            "pending_review_level": "high",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "low",
            "topic_concentration": "high",
            "manual_state_level": "high",
            "completion_state": "high_volume_many_errors",
            "scope_profile": "advanced",
            "learning_trait": "做得多但不稳定",
        },
    ),
    (
        "high_volume_stable",
        4,
        {
            "practice_volume": 150,
            "wrong_level": "low",
            "pending_review_level": "none",
            "overdue_level": "low",
            "draft_level": "none",
            "unstarted_level": "none",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "high_volume_stable",
            "scope_profile": "advanced",
            "learning_trait": "做得多且稳定",
        },
    ),
    (
        "low_volume_accurate",
        4,
        {
            "practice_volume": 6,
            "wrong_level": "none",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "balanced",
            "manual_state_level": "low",
            "completion_state": "low_volume_clean",
            "scope_profile": "early_stage",
            "learning_trait": "做得少但目前正确",
        },
    ),
    (
        "low_volume_wrong",
        4,
        {
            "practice_volume": 5,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "high",
            "manual_state_level": "low",
            "completion_state": "low_volume_risky",
            "scope_profile": "early_stage",
            "learning_trait": "做得少且早期出错",
        },
    ),
    (
        "draft_abandoner",
        4,
        {
            "practice_volume": 25,
            "wrong_level": "low",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "high",
            "unstarted_level": "high",
            "topic_concentration": "medium",
            "manual_state_level": "low",
            "completion_state": "many_unsubmitted_drafts",
            "scope_profile": "normal",
            "learning_trait": "多次开始但未提交",
        },
    ),
    (
        "math2_scope",
        4,
        {
            "practice_volume": 28,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "medium",
            "manual_state_level": "low",
            "completion_state": "math2_partial",
            "scope_profile": "math2_only",
            "learning_trait": "math2_scope_planning",
        },
    ),
    (
        "math3_scope",
        4,
        {
            "practice_volume": 32,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "medium",
            "manual_state_level": "low",
            "completion_state": "math3_partial",
            "scope_profile": "math3_only",
            "learning_trait": "math3_scope_planning",
        },
    ),
    (
        "cross_subject_mixed",
        4,
        {
            "practice_volume": 50,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "medium",
            "unstarted_level": "medium",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "multi_subject_active",
            "scope_profile": "cross_subject",
            "learning_trait": "multi_subject_load",
        },
    ),
    (
        "wrong_resolved_history",
        4,
        {
            "practice_volume": 70,
            "wrong_level": "low",
            "pending_review_level": "none",
            "overdue_level": "low",
            "draft_level": "none",
            "unstarted_level": "medium",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "wrong_history_mostly_resolved",
            "scope_profile": "normal",
            "learning_trait": "past_wrong_but_recent_clean",
        },
    ),
    (
        "wrong_still_frequent_after_review",
        4,
        {
            "practice_volume": 90,
            "wrong_level": "high",
            "pending_review_level": "low",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "low",
            "topic_concentration": "high",
            "manual_state_level": "medium",
            "completion_state": "reviewed_but_wrong_repeats",
            "scope_profile": "normal",
            "learning_trait": "repeat_wrong_after_review",
        },
    ),
    (
        "ai_corrected_pending",
        4,
        {
            "practice_volume": 38,
            "wrong_level": "low",
            "pending_review_level": "high",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
            "completion_state": "ai_judgement_needed",
            "scope_profile": "normal",
            "learning_trait": "ai_correctable_pending",
        },
    ),
    (
        "manual_override_heavy",
        4,
        {
            "practice_volume": 42,
            "wrong_level": "medium",
            "pending_review_level": "high",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "high",
            "completion_state": "manual_judgement_active",
            "scope_profile": "normal",
            "learning_trait": "manual_override_frequent",
        },
    ),
    (
        "favorite_never_practiced",
        4,
        {
            "practice_volume": 0,
            "wrong_level": "none",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "narrow",
            "manual_state_level": "high",
            "completion_state": "favorite_without_practice",
            "scope_profile": "favorite_clustered",
            "learning_trait": "favorite_but_never_started",
        },
    ),
    (
        "short_daily_budget",
        4,
        {
            "practice_volume": 26,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "medium",
            "draft_level": "medium",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
            "completion_state": "time_constrained",
            "scope_profile": "normal",
            "learning_trait": "short_daily_budget",
            "daily_budget_profile": "short",
        },
    ),
    (
        "long_daily_budget",
        4,
        {
            "practice_volume": 65,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "large_daily_capacity",
            "scope_profile": "normal",
            "learning_trait": "long_daily_budget",
            "daily_budget_profile": "long",
        },
    ),
    (
        "exam_sprint_week",
        4,
        {
            "practice_volume": 85,
            "wrong_level": "high",
            "pending_review_level": "medium",
            "overdue_level": "high",
            "draft_level": "medium",
            "unstarted_level": "low",
            "topic_concentration": "high",
            "manual_state_level": "high",
            "completion_state": "last_week_sprint",
            "scope_profile": "exam_week",
            "learning_trait": "exam_sprint_pressure",
        },
    ),
    (
        "repeat_postpone",
        4,
        {
            "practice_volume": 30,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "high",
            "draft_level": "high",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
            "completion_state": "tasks_repeatedly_postponed",
            "scope_profile": "normal",
            "learning_trait": "repeat_postpone",
        },
    ),
    (
        "recent_improving",
        4,
        {
            "practice_volume": 55,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "balanced",
            "manual_state_level": "medium",
            "completion_state": "recent_accuracy_improved",
            "scope_profile": "normal",
            "learning_trait": "recent_improving",
            "trend_profile": "improving",
        },
    ),
    (
        "recent_declining",
        4,
        {
            "practice_volume": 58,
            "wrong_level": "high",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
            "completion_state": "recent_accuracy_declined",
            "scope_profile": "normal",
            "learning_trait": "recent_declining",
            "trend_profile": "declining",
        },
    ),
    (
        "choice_only_bias",
        4,
        {
            "practice_volume": 48,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "narrow",
            "manual_state_level": "low",
            "completion_state": "choice_only_practice",
            "scope_profile": "choice_only",
            "learning_trait": "choice_only_bias",
        },
    ),
    (
        "solution_avoidance",
        4,
        {
            "practice_volume": 44,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "high",
            "unstarted_level": "medium",
            "topic_concentration": "high",
            "manual_state_level": "low",
            "completion_state": "solution_questions_avoided",
            "scope_profile": "solution_avoidance",
            "learning_trait": "avoid_solution_questions",
        },
    ),
    (
        "all_done_wrong_backlog",
        4,
        {
            "practice_volume": 130,
            "wrong_level": "high",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "none",
            "unstarted_level": "none",
            "topic_concentration": "high",
            "manual_state_level": "medium",
            "completion_state": "all_done_with_wrong_backlog",
            "scope_profile": "full_coverage",
            "learning_trait": "all_done_but_wrong_backlog",
        },
    ),
    (
        "chapter_cold_start",
        4,
        {
            "practice_volume": 0,
            "wrong_level": "none",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "high",
            "manual_state_level": "low",
            "completion_state": "chapter_selected_no_history",
            "scope_profile": "chapter_focus",
            "learning_trait": "cold_start_with_chapter_preference",
        },
    ),
    (
        "scattered_wrong",
        4,
        {
            "practice_volume": 72,
            "wrong_level": "high",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "medium",
            "topic_concentration": "scattered",
            "manual_state_level": "medium",
            "completion_state": "wrong_questions_scattered",
            "scope_profile": "wide_coverage",
            "learning_trait": "scattered_wrong_topics",
        },
    ),
    (
        "unstarted_foundation",
        4,
        {
            "practice_volume": 4,
            "wrong_level": "low",
            "pending_review_level": "none",
            "overdue_level": "none",
            "draft_level": "none",
            "unstarted_level": "high",
            "topic_concentration": "foundation",
            "manual_state_level": "low",
            "completion_state": "foundation_unstarted",
            "scope_profile": "foundation",
            "learning_trait": "unstarted_foundation",
        },
    ),
    (
        "unstarted_advanced",
        4,
        {
            "practice_volume": 40,
            "wrong_level": "low",
            "pending_review_level": "low",
            "overdue_level": "low",
            "draft_level": "low",
            "unstarted_level": "high",
            "topic_concentration": "advanced",
            "manual_state_level": "medium",
            "completion_state": "advanced_unstarted",
            "scope_profile": "advanced",
            "learning_trait": "unstarted_advanced",
        },
    ),
    (
        "reviewed_but_unmastered",
        4,
        {
            "practice_volume": 78,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "low",
            "unstarted_level": "low",
            "topic_concentration": "medium",
            "manual_state_level": "high",
            "completion_state": "reviewed_not_mastered",
            "scope_profile": "normal",
            "learning_trait": "reviewed_but_unmastered",
        },
    ),
    (
        "oversized_practice_sheet",
        4,
        {
            "practice_volume": 36,
            "wrong_level": "medium",
            "pending_review_level": "low",
            "overdue_level": "medium",
            "draft_level": "high",
            "unstarted_level": "medium",
            "topic_concentration": "medium",
            "manual_state_level": "medium",
            "completion_state": "large_sheet_partially_done",
            "scope_profile": "large_practice_sheet",
            "learning_trait": "oversized_practice_sheet",
        },
    ),
    (
        "proof_heavy_backlog",
        4,
        {
            "practice_volume": 64,
            "wrong_level": "high",
            "pending_review_level": "medium",
            "overdue_level": "medium",
            "draft_level": "medium",
            "unstarted_level": "low",
            "topic_concentration": "high",
            "manual_state_level": "medium",
            "completion_state": "proof_questions_backlog",
            "scope_profile": "advanced",
            "learning_trait": "proof_heavy_backlog",
        },
    ),
    (
        "mixed_type_load_gap",
        4,
        {
            "practice_volume": 52,
            "wrong_level": "medium",
            "pending_review_level": "medium",
            "overdue_level": "low",
            "draft_level": "medium",
            "unstarted_level": "medium",
            "topic_concentration": "scattered",
            "manual_state_level": "medium",
            "completion_state": "same_question_count_different_load",
            "scope_profile": "mixed_question_types",
            "learning_trait": "mixed_type_load_gap",
        },
    ),
)


def build_persona_catalog() -> list[dict[str, Any]]:
    """Return a deterministic persona catalog for AI review-plan strategy checks."""

    personas: list[dict[str, Any]] = []
    for category, count, base in _CATEGORY_SPECS:
        for index in range(1, count + 1):
            persona = dict(base)
            persona["persona_id"] = f"{category}_{index:03d}"
            persona["category"] = category
            persona["practice_volume"] = int(persona.get("practice_volume") or 0) + index - 1
            persona["variant"] = index
            persona["expected_modes"] = _expected_modes_for_category(category)
            personas.append(persona)
    return personas


def evaluate_mode_policy_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    if not personas:
        raise ValueError("personas must not be empty")

    selected_modes = tuple(modes or EVALUATION_MODES)
    cases: list[dict[str, Any]] = []
    hard_violation_count = 0
    for persona in personas:
        for mode in selected_modes:
            policy = build_ai_review_plan_policy(mode)
            violations = _policy_violations(persona, policy)
            hard_violation_count += len(violations)
            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": policy["mode"],
                    "enabled_types": list(policy.get("enabled_types") or []),
                    "disabled_types": list(policy.get("disabled_types") or []),
                    "expected_modes": list(persona.get("expected_modes") or []),
                    "violations": violations,
                }
            )

    return {
        "modes": list(selected_modes),
        "persona_count": len(personas),
        "case_count": len(cases),
        "candidate_types": list(AI_REVIEW_PLAN_CANDIDATE_TYPES),
        "summary": {
            "hard_violation_count": hard_violation_count,
            "hard_violation_rate": hard_violation_count / max(1, len(cases)),
        },
        "cases": cases,
    }


def evaluate_deterministic_planner_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    if not personas:
        raise ValueError("personas must not be empty")

    selected_modes = tuple(modes or EVALUATION_MODES)
    cases: list[dict[str, Any]] = []
    invalid_task_count = 0
    mode_fit_total = 0.0
    for persona in personas:
        candidates = _synthetic_candidates_for_persona(persona)
        for mode in selected_modes:
            policy = build_ai_review_plan_policy(mode)
            filtered = filter_ai_review_plan_candidates(candidates, policy)
            tasks = _deterministic_plan_tasks(filtered, policy, limit=6)
            invalid_tasks = [
                task
                for task in tasks
                if task.get("candidate_type") not in set(policy.get("enabled_types") or [])
            ]
            invalid_task_count += len(invalid_tasks)
            mode_fit = _mode_fit_score(tasks, policy)
            mode_fit_total += mode_fit
            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": policy["mode"],
                    "task_count": len(tasks),
                    "mode_fit_score": mode_fit,
                    "invalid_task_count": len(invalid_tasks),
                    "tasks": tasks,
                }
            )

    return {
        "modes": list(selected_modes),
        "persona_count": len(personas),
        "case_count": len(cases),
        "summary": {
            "invalid_task_count": invalid_task_count,
            "mode_fit_score": mode_fit_total / max(1, len(cases)),
        },
        "cases": cases,
    }


def evaluate_full_ai_plan_flow_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
    *,
    days: int = 7,
    daily_minutes: int = 60,
) -> dict[str, Any]:
    """Evaluate the local planning pipeline before real LLM calls.

    This checks the full local handoff: mode policy -> candidate filtering ->
    readiness gate -> deterministic draft shape -> source/type/load validation.
    The deterministic draft stands in for the AI response so we can catch
    policy and data-prep bugs without spending tokens.
    """

    if not personas:
        raise ValueError("personas must not be empty")

    selected_modes = tuple(modes or EVALUATION_MODES)
    cases: list[dict[str, Any]] = []
    ready_case_count = 0
    weak_case_count = 0
    blocked_case_count = 0
    should_call_llm_count = 0
    invalid_source_count = 0
    invalid_item_count = 0
    duplicate_source_count = 0
    daily_overload_count = 0
    mode_fit_total = 0.0
    mode_fit_case_count = 0
    by_mode: dict[str, dict[str, Any]] = {
        mode: {
            "case_count": 0,
            "ready_case_count": 0,
            "weak_case_count": 0,
            "blocked_case_count": 0,
            "should_call_llm_count": 0,
            "task_count": 0,
            "invalid_source_count": 0,
            "invalid_item_count": 0,
            "duplicate_source_count": 0,
            "daily_overload_count": 0,
            "mode_fit_total": 0.0,
            "mode_fit_case_count": 0,
        }
        for mode in selected_modes
    }

    for persona in personas:
        source_candidates = _synthetic_candidates_for_persona(persona)
        for mode in selected_modes:
            policy = build_ai_review_plan_policy(mode)
            filtered = filter_ai_review_plan_candidates(source_candidates, policy)
            readiness = assess_ai_review_plan_readiness(
                filtered,
                policy,
                days=days,
                daily_minutes=daily_minutes,
                practice_volume=int(persona.get("practice_volume") or 0),
            )
            readiness_status = str(readiness.get("status") or "")
            ready_case_count += 1 if readiness_status == "ready" else 0
            weak_case_count += 1 if readiness_status == "weak" else 0
            blocked_case_count += 1 if readiness_status == "blocked" else 0

            should_call_llm = readiness_status != "blocked"
            should_call_llm_count += 1 if should_call_llm else 0
            plan_slots = max(1, int(readiness.get("plan_slots") or 1))
            tasks_per_day = max(1, int(readiness.get("tasks_per_day") or 1))
            tasks = (
                _deterministic_plan_tasks(filtered, policy, limit=plan_slots)
                if should_call_llm
                else []
            )
            draft = _draft_from_evaluation_tasks(tasks, days=days, tasks_per_day=tasks_per_day)
            context = {
                "policy": policy,
                "ai_candidates": filtered,
            }
            item_checks = _evaluate_plan_items_against_context(draft, context)
            task_source_ids = [_candidate_source_id(task) for task in tasks]
            duplicate_source_ids = _duplicate_values(task_source_ids)
            daily_counts = [
                len(day.get("items") or [])
                for day in draft.get("days", [])
                if isinstance(day, dict)
            ]
            daily_overloaded = any(count > tasks_per_day for count in daily_counts)
            invalid_sources = len(item_checks["invalid_source_ids"])
            invalid_items = item_checks["total_item_count"] - item_checks["valid_item_count"]

            invalid_source_count += invalid_sources
            invalid_item_count += invalid_items
            duplicate_source_count += len(duplicate_source_ids)
            daily_overload_count += 1 if daily_overloaded else 0
            mode_fit_score = float(item_checks["mode_fit_score"])
            if tasks:
                mode_fit_total += mode_fit_score
                mode_fit_case_count += 1

            mode_summary = by_mode[mode]
            mode_summary["case_count"] += 1
            mode_summary["ready_case_count"] += 1 if readiness_status == "ready" else 0
            mode_summary["weak_case_count"] += 1 if readiness_status == "weak" else 0
            mode_summary["blocked_case_count"] += 1 if readiness_status == "blocked" else 0
            mode_summary["should_call_llm_count"] += 1 if should_call_llm else 0
            mode_summary["task_count"] += len(tasks)
            mode_summary["invalid_source_count"] += invalid_sources
            mode_summary["invalid_item_count"] += invalid_items
            mode_summary["duplicate_source_count"] += len(duplicate_source_ids)
            mode_summary["daily_overload_count"] += 1 if daily_overloaded else 0
            if tasks:
                mode_summary["mode_fit_total"] += mode_fit_score
                mode_summary["mode_fit_case_count"] += 1

            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": policy["mode"],
                    "readiness_status": readiness_status,
                    "should_call_llm": should_call_llm,
                    "task_count": len(tasks),
                    "daily_counts": daily_counts,
                    "tasks_per_day": tasks_per_day,
                    "daily_overloaded": daily_overloaded,
                    "duplicate_source_ids": duplicate_source_ids,
                    "invalid_source_ids": item_checks["invalid_source_ids"],
                    "invalid_item_count": invalid_items,
                    "mode_fit_score": mode_fit_score,
                    "readiness": readiness,
                }
            )

    for mode_summary in by_mode.values():
        scored = int(mode_summary["mode_fit_case_count"])
        mode_summary["average_mode_fit_score"] = mode_summary["mode_fit_total"] / max(1, scored)
        mode_summary.pop("mode_fit_total", None)

    case_count = len(cases)
    return {
        "modes": list(selected_modes),
        "persona_count": len(personas),
        "case_count": case_count,
        "summary": {
            "ready_case_count": ready_case_count,
            "weak_case_count": weak_case_count,
            "blocked_case_count": blocked_case_count,
            "should_call_llm_count": should_call_llm_count,
            "invalid_source_count": invalid_source_count,
            "invalid_source_rate": invalid_source_count / max(1, case_count),
            "invalid_item_count": invalid_item_count,
            "invalid_item_rate": invalid_item_count / max(1, case_count),
            "duplicate_source_count": duplicate_source_count,
            "duplicate_source_rate": duplicate_source_count / max(1, case_count),
            "daily_overload_count": daily_overload_count,
            "daily_overload_rate": daily_overload_count / max(1, case_count),
            "average_mode_fit_score": mode_fit_total / max(1, mode_fit_case_count),
        },
        "by_mode": by_mode,
        "cases": cases,
    }


def evaluate_mode_candidate_budget_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
    *,
    top_limit: int = 8,
) -> dict[str, Any]:
    if not personas:
        raise ValueError("personas must not be empty")

    selected_modes = tuple(modes or EVALUATION_MODES)
    safe_top_limit = max(1, int(top_limit or 8))
    cases: list[dict[str, Any]] = []
    hard_policy_violation_count = 0
    top_budget_violation_count = 0
    evaluable_budget_count = 0
    top_primary_ratio_total = 0.0
    by_mode: dict[str, dict[str, Any]] = {
        mode: {
            "case_count": 0,
            "hard_policy_violation_count": 0,
            "top_budget_violation_count": 0,
            "evaluable_budget_count": 0,
            "top_primary_ratio_total": 0.0,
        }
        for mode in selected_modes
    }

    for persona in personas:
        source_candidates = _synthetic_candidates_for_persona(persona)
        for mode in selected_modes:
            policy = build_ai_review_plan_policy(mode)
            filtered = filter_ai_review_plan_candidates(source_candidates, policy)
            input_counts = _candidate_counts_by_type(filtered)
            top_candidates = _deterministic_plan_tasks(filtered, policy, limit=safe_top_limit)
            top_counts = _flat_candidate_counts_by_type(top_candidates)

            enabled = set(str(value) for value in policy.get("enabled_types") or [])
            disabled = set(str(value) for value in policy.get("disabled_types") or [])
            disabled_present = {
                candidate_type: count
                for candidate_type, count in input_counts.items()
                if candidate_type in disabled and count > 0
            }
            disabled_present_count = sum(disabled_present.values())
            hard_policy_violation_count += disabled_present_count

            primary_types = set(MODE_PRIMARY_BUDGET_TYPES.get(policy["mode"], AI_REVIEW_PLAN_CANDIDATE_TYPES))
            top_total = sum(count for candidate_type, count in top_counts.items() if candidate_type in enabled)
            top_primary_count = sum(count for candidate_type, count in top_counts.items() if candidate_type in primary_types)
            top_primary_ratio = top_primary_count / max(1, top_total) if top_total > 0 else 1.0

            readiness = assess_ai_review_plan_readiness(
                filtered,
                policy,
                practice_volume=int(persona.get("practice_volume") or 0),
            )
            budget_floor = MODE_TOP_PRIMARY_RATIO_FLOOR.get(policy["mode"], 0.0)
            budget_evaluable = (
                top_total > 0
                and budget_floor > 0
                and str(readiness.get("status") or "") == "ready"
            )
            top_budget_violation = budget_evaluable and top_primary_ratio < budget_floor
            if budget_evaluable:
                evaluable_budget_count += 1
                top_primary_ratio_total += top_primary_ratio
            if top_budget_violation:
                top_budget_violation_count += 1

            mode_summary = by_mode[mode]
            mode_summary["case_count"] += 1
            mode_summary["hard_policy_violation_count"] += disabled_present_count
            if budget_evaluable:
                mode_summary["evaluable_budget_count"] += 1
                mode_summary["top_primary_ratio_total"] += top_primary_ratio
            if top_budget_violation:
                mode_summary["top_budget_violation_count"] += 1

            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": policy["mode"],
                    "input_counts": input_counts,
                    "top_counts": top_counts,
                    "top_total": top_total,
                    "top_primary_count": top_primary_count,
                    "top_primary_ratio": round(top_primary_ratio, 4),
                    "budget_floor": budget_floor,
                    "budget_evaluable": budget_evaluable,
                    "top_budget_violation": top_budget_violation,
                    "disabled_present": disabled_present,
                    "disabled_present_count": disabled_present_count,
                    "readiness_status": str(readiness.get("status") or ""),
                }
            )

    case_count = len(cases)
    for mode_summary in by_mode.values():
        evaluable = int(mode_summary["evaluable_budget_count"])
        mode_summary["average_top_primary_ratio"] = (
            mode_summary["top_primary_ratio_total"] / max(1, evaluable)
        )
        mode_summary["top_budget_violation_rate"] = (
            mode_summary["top_budget_violation_count"] / max(1, evaluable)
        )
        mode_summary.pop("top_primary_ratio_total", None)

    return {
        "modes": list(selected_modes),
        "persona_count": len(personas),
        "case_count": case_count,
        "top_limit": safe_top_limit,
        "primary_budget_types": {
            mode: list(MODE_PRIMARY_BUDGET_TYPES.get(mode, ()))
            for mode in selected_modes
        },
        "summary": {
            "hard_policy_violation_count": hard_policy_violation_count,
            "hard_policy_violation_rate": hard_policy_violation_count / max(1, case_count),
            "top_budget_violation_count": top_budget_violation_count,
            "top_budget_violation_rate": top_budget_violation_count / max(1, evaluable_budget_count),
            "evaluable_budget_count": evaluable_budget_count,
            "average_top_primary_ratio": top_primary_ratio_total / max(1, evaluable_budget_count),
        },
        "by_mode": by_mode,
        "cases": cases,
    }


def evaluate_mode_readiness_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
    *,
    days: int = 7,
    daily_minutes: int = 60,
) -> dict[str, Any]:
    if not personas:
        raise ValueError("personas must not be empty")

    selected_modes = tuple(modes or EVALUATION_MODES)
    cases: list[dict[str, Any]] = []
    ready_count = 0
    weak_count = 0
    blocked_count = 0
    false_ready_count = 0
    false_block_count = 0
    for persona in personas:
        candidates = _synthetic_candidates_for_persona(persona)
        for mode in selected_modes:
            policy = build_ai_review_plan_policy(mode)
            filtered = filter_ai_review_plan_candidates(candidates, policy)
            readiness = assess_ai_review_plan_readiness(
                filtered,
                policy,
                days=days,
                daily_minutes=daily_minutes,
                practice_volume=int(persona.get("practice_volume") or 0),
            )
            status = str(readiness.get("status") or "")
            ready_count += 1 if status == "ready" else 0
            weak_count += 1 if status == "weak" else 0
            blocked_count += 1 if status == "blocked" else 0
            expected = _expected_readiness_for_category(str(persona.get("category") or ""), str(mode))
            false_ready = status == "ready" and "ready" not in expected
            false_block = status == "blocked" and "blocked" not in expected
            false_ready_count += 1 if false_ready else 0
            false_block_count += 1 if false_block else 0
            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": str(mode),
                    "expected_statuses": sorted(expected),
                    "readiness": readiness,
                    "false_ready": false_ready,
                    "false_block": false_block,
                }
            )

    case_count = len(cases)
    return {
        "modes": list(selected_modes),
        "persona_count": len(personas),
        "case_count": case_count,
        "summary": {
            "ready_count": ready_count,
            "weak_count": weak_count,
            "blocked_count": blocked_count,
            "false_ready_count": false_ready_count,
            "false_ready_rate": false_ready_count / max(1, case_count),
            "false_block_count": false_block_count,
            "false_block_rate": false_block_count / max(1, case_count),
        },
        "cases": cases,
    }


def evaluate_ai_planner_sample_for_personas(
    personas: list[dict[str, Any]],
    modes: list[str] | tuple[str, ...] | None = None,
    *,
    max_cases: int = 20,
    planner: Any = None,
    model: str = "deepseek-v4-flash",
    days: int = 3,
    daily_minutes: int = 60,
) -> dict[str, Any]:
    if not personas:
        raise ValueError("personas must not be empty")
    if planner is None:
        from .system_ai_planner import generate_ai_review_plan_draft

        planner = generate_ai_review_plan_draft

    selected_modes = tuple(modes or EVALUATION_MODES)
    case_inputs = _sample_persona_mode_pairs(personas, selected_modes, max_cases=max_cases)
    cases: list[dict[str, Any]] = []
    llm_success_count = 0
    llm_skipped_count = 0
    valid_item_count = 0
    total_item_count = 0
    mode_fit_total = 0.0
    mode_fit_case_count = 0
    for persona, mode in case_inputs:
        context = build_synthetic_ai_planning_context(
            persona,
            mode=mode,
            days=days,
            daily_minutes=daily_minutes,
        )
        policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
        candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
        readiness = assess_ai_review_plan_readiness(
            candidates,
            policy,
            days=days,
            daily_minutes=daily_minutes,
            practice_volume=int(persona.get("practice_volume") or 0),
        )
        readiness_status = str(readiness.get("status") or "")
        if readiness_status == "blocked":
            llm_skipped_count += 1
            cases.append(
                {
                    "persona_id": str(persona.get("persona_id") or ""),
                    "category": str(persona.get("category") or ""),
                    "mode": str(mode),
                    "source": "skipped",
                    "readiness_status": readiness_status,
                    "valid_item_count": 0,
                    "total_item_count": 0,
                    "mode_fit_score": 0.0,
                    "invalid_source_ids": [],
                    "skip_reason": readiness.get("reason"),
                }
            )
            continue
        draft = planner(context=context, model=model)
        if isinstance(draft, dict) and draft.get("source") == "llm":
            llm_success_count += 1
        item_checks = _evaluate_plan_items_against_context(draft, context)
        valid_item_count += item_checks["valid_item_count"]
        total_item_count += item_checks["total_item_count"]
        mode_fit_total += item_checks["mode_fit_score"]
        mode_fit_case_count += 1
        cases.append(
            {
                "persona_id": str(persona.get("persona_id") or ""),
                "category": str(persona.get("category") or ""),
                "mode": str(mode),
                "source": draft.get("source") if isinstance(draft, dict) else "invalid",
                "readiness_status": readiness_status,
                "valid_item_count": item_checks["valid_item_count"],
                "total_item_count": item_checks["total_item_count"],
                "mode_fit_score": item_checks["mode_fit_score"],
                "invalid_source_ids": item_checks["invalid_source_ids"],
            }
        )

    return {
        "modes": list(selected_modes),
        "persona_count": len({str(persona.get("persona_id") or "") for persona, _ in case_inputs}),
        "case_count": len(cases),
        "summary": {
            "llm_success_count": llm_success_count,
            "llm_skipped_count": llm_skipped_count,
            "candidate_validity_rate": valid_item_count / max(1, total_item_count),
            "mode_fit_score": mode_fit_total / max(1, mode_fit_case_count),
            "invalid_item_count": total_item_count - valid_item_count,
        },
        "cases": cases,
    }


def build_synthetic_ai_planning_context(
    persona: dict[str, Any],
    *,
    mode: str,
    days: int = 3,
    daily_minutes: int = 60,
) -> dict[str, Any]:
    policy = build_ai_review_plan_policy(mode)
    candidates = filter_ai_review_plan_candidates(_synthetic_candidates_for_persona(persona), policy)
    return {
        "persona": {
            "persona_id": str(persona.get("persona_id") or ""),
            "category": str(persona.get("category") or ""),
            "practice_volume": persona.get("practice_volume"),
        },
        "constraints": {
            "subject": "math",
            "days": days,
            "daily_minutes": daily_minutes,
            "mode": policy["mode"],
            "goal": policy["label"],
        },
        "policy": policy,
        "ai_candidates": candidates,
    }


def _expected_modes_for_category(category: str) -> list[str]:
    mapping = {
        "cold_start": ["startup", "balanced"],
        "strong": ["balanced", "sprint"],
        "heavy_wrong": ["wrong", "weak", "sprint"],
        "low_volume_concentrated": ["startup", "weak"],
        "review_pressure": ["sprint", "balanced"],
        "skip_unanswered": ["balanced", "startup"],
        "scope_bias": ["weak", "startup"],
        "edge_cases": ["balanced"],
        "all_done_no_new": ["balanced", "sprint"],
        "no_wrong_history": ["balanced", "startup"],
        "pending_review_heavy": ["wrong", "sprint", "balanced"],
        "favorite_unmastered_heavy": ["sprint", "weak", "balanced"],
        "overdue_neglect": ["sprint", "balanced", "wrong"],
        "high_volume_unstable": ["wrong", "weak", "sprint"],
        "high_volume_stable": ["balanced", "sprint"],
        "low_volume_accurate": ["startup", "balanced"],
        "low_volume_wrong": ["weak", "startup"],
        "draft_abandoner": ["balanced", "startup"],
        "math2_scope": ["startup", "balanced", "weak"],
        "math3_scope": ["startup", "balanced", "weak"],
        "cross_subject_mixed": ["balanced", "sprint"],
        "wrong_resolved_history": ["balanced", "sprint"],
        "wrong_still_frequent_after_review": ["wrong", "weak", "sprint"],
        "ai_corrected_pending": ["wrong", "balanced"],
        "manual_override_heavy": ["wrong", "balanced"],
        "favorite_never_practiced": ["startup", "balanced"],
        "short_daily_budget": ["balanced", "sprint"],
        "long_daily_budget": ["balanced", "startup"],
        "exam_sprint_week": ["sprint", "wrong", "weak"],
        "repeat_postpone": ["sprint", "balanced"],
        "recent_improving": ["balanced", "sprint"],
        "recent_declining": ["weak", "wrong", "sprint"],
        "choice_only_bias": ["balanced", "weak"],
        "solution_avoidance": ["balanced", "wrong", "sprint"],
        "all_done_wrong_backlog": ["wrong", "weak", "sprint"],
        "chapter_cold_start": ["startup", "balanced"],
        "scattered_wrong": ["wrong", "balanced"],
        "unstarted_foundation": ["startup", "balanced"],
        "unstarted_advanced": ["startup", "balanced"],
        "reviewed_but_unmastered": ["weak", "sprint", "balanced"],
    }
    return list(mapping.get(category, ["balanced"]))


def _expected_readiness_for_category(category: str, mode: str) -> set[str]:
    if category == "cold_start":
        return {
            "balanced": {"ready", "weak"},
            "startup": {"ready", "weak"},
            "wrong": {"blocked"},
            "weak": {"blocked", "weak"},
            "sprint": {"blocked", "weak"},
        }.get(mode, {"weak"})
    if category == "heavy_wrong":
        return {
            "wrong": {"ready"},
            "weak": {"ready", "weak"},
            "sprint": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "startup": {"ready", "weak"},
        }.get(mode, {"weak"})
    if category == "review_pressure":
        return {
            "sprint": {"ready"},
            "balanced": {"ready", "weak"},
            "wrong": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "startup": {"ready", "weak"},
        }.get(mode, {"weak"})
    if category == "low_volume_concentrated":
        return {
            "startup": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "wrong": {"weak", "blocked"},
            "sprint": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "strong":
        return {
            "balanced": {"ready", "weak"},
            "sprint": {"ready", "weak"},
            "wrong": {"weak", "blocked"},
            "weak": {"weak", "blocked"},
            "startup": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "all_done_no_new":
        return {
            "balanced": {"ready", "weak"},
            "sprint": {"ready", "weak"},
            "startup": {"blocked"},
            "wrong": {"weak", "blocked"},
            "weak": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "no_wrong_history":
        return {
            "balanced": {"ready", "weak"},
            "startup": {"ready", "weak"},
            "wrong": {"weak", "blocked"},
            "weak": {"weak", "blocked"},
            "sprint": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "pending_review_heavy":
        return {
            "wrong": {"ready", "weak"},
            "sprint": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "startup": {"ready", "weak"},
        }.get(mode, {"weak"})
    if category == "favorite_unmastered_heavy":
        return {
            "sprint": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "wrong": {"ready", "weak"},
            "startup": {"ready", "weak"},
        }.get(mode, {"weak"})
    if category == "overdue_neglect":
        return {
            "sprint": {"ready"},
            "balanced": {"ready", "weak"},
            "wrong": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "startup": {"ready", "weak"},
        }.get(mode, {"weak"})
    if category == "high_volume_unstable":
        return {
            "wrong": {"ready"},
            "weak": {"ready", "weak"},
            "sprint": {"ready"},
            "balanced": {"ready", "weak"},
            "startup": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "high_volume_stable":
        return {
            "balanced": {"ready", "weak"},
            "sprint": {"ready", "weak"},
            "startup": {"blocked"},
            "wrong": {"weak", "blocked"},
            "weak": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "low_volume_accurate":
        return {
            "startup": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "wrong": {"blocked"},
            "weak": {"blocked", "weak"},
            "sprint": {"blocked", "weak"},
        }.get(mode, {"weak"})
    if category == "low_volume_wrong":
        return {
            "weak": {"ready", "weak"},
            "startup": {"ready", "weak"},
            "balanced": {"ready", "weak"},
            "wrong": {"weak", "blocked"},
            "sprint": {"weak", "blocked"},
        }.get(mode, {"weak"})
    if category == "draft_abandoner":
        return {
            "balanced": {"ready", "weak"},
            "startup": {"ready", "weak"},
            "wrong": {"ready", "weak"},
            "weak": {"ready", "weak"},
            "sprint": {"ready", "weak"},
        }.get(mode, {"weak"})
    return {"ready", "weak", "blocked"}


def _policy_violations(persona: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    enabled = set(str(value) for value in policy.get("enabled_types") or [])
    disabled = set(str(value) for value in policy.get("disabled_types") or [])
    mode = str(policy.get("mode") or "")
    violations: list[str] = []

    if mode == "wrong" and {"unstarted_questions", "startup_candidates"} & enabled:
        violations.append("wrong_mode_includes_new_start_candidates")
    if mode == "startup" and {"startup_candidates", "unstarted_questions"} & disabled:
        violations.append("startup_mode_blocks_new_start_candidates")
    if mode in {"weak", "sprint"} and {"unstarted_questions", "startup_candidates"} & enabled:
        violations.append(f"{mode}_mode_includes_ordinary_new_start_candidates")
    if str(persona.get("category") or "") == "cold_start" and mode == "startup" and "startup_candidates" not in enabled:
        violations.append("cold_start_startup_mode_has_no_startup_candidates")
    return violations


def _sample_persona_mode_pairs(
    personas: list[dict[str, Any]],
    modes: tuple[str, ...],
    *,
    max_cases: int,
) -> list[tuple[dict[str, Any], str]]:
    max_cases = max(1, int(max_cases or 1))
    grouped: dict[str, list[dict[str, Any]]] = {}
    for persona in personas:
        grouped.setdefault(str(persona.get("category") or "unknown"), []).append(persona)
    ordered_categories = sorted(grouped)
    pairs: list[tuple[dict[str, Any], str]] = []
    offset = 0
    while len(pairs) < max_cases and offset < max(len(values) for values in grouped.values()):
        for category in ordered_categories:
            values = grouped[category]
            if offset >= len(values):
                continue
            for mode in modes:
                pairs.append((values[offset], mode))
                if len(pairs) >= max_cases:
                    return pairs
        offset += 1
    return pairs


def _evaluate_plan_items_against_context(draft: Any, context: dict[str, Any]) -> dict[str, Any]:
    valid_source_ids = _context_source_ids(context)
    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    enabled_types = set(str(value) for value in policy.get("enabled_types") or [])
    available_types = _available_candidate_types(context, enabled_types)
    priority_types = _priority_candidate_types(policy, available_types)
    total_item_count = 0
    valid_item_count = 0
    mapped_types: list[str] = []
    invalid_source_ids: list[str] = []
    days = draft.get("days") if isinstance(draft, dict) and isinstance(draft.get("days"), list) else []
    for day in days:
        items = day.get("items") if isinstance(day, dict) and isinstance(day.get("items"), list) else []
        for item in items:
            if not isinstance(item, dict):
                continue
            total_item_count += 1
            mapped_type = _plan_item_type_to_candidate_type(str(item.get("type") or ""))
            mapped_types.append(mapped_type)
            source_ids = [str(value) for value in item.get("source_ids") or [] if str(value).strip()]
            source_ids_valid = all(source_id in valid_source_ids for source_id in source_ids)
            if mapped_type in set(AI_REVIEW_PLAN_CANDIDATE_TYPES):
                source_ids_valid = bool(source_ids) and source_ids_valid
            type_valid = mapped_type in enabled_types if mapped_type else True
            if source_ids_valid and type_valid:
                valid_item_count += 1
            else:
                invalid_source_ids.extend(source_id for source_id in source_ids if source_id not in valid_source_ids)
    return {
        "total_item_count": total_item_count,
        "valid_item_count": valid_item_count,
        "invalid_source_ids": invalid_source_ids,
        "mode_fit_score": _plan_item_mode_fit_score(
            mapped_types,
            policy=policy,
            priority_types=priority_types,
            available_types=available_types,
            valid_item_count=valid_item_count,
            total_item_count=total_item_count,
        ),
    }


def _priority_candidate_types(policy: dict[str, Any], available_types: set[str]) -> list[str]:
    configured = policy.get("type_priority")
    if isinstance(configured, list) and configured:
        priority = [str(value) for value in configured]
    else:
        priority = list(MODE_PREFERRED_TYPES.get(str(policy.get("mode") or "balanced"), ()))
    return [candidate_type for candidate_type in priority if candidate_type in available_types]


def _plan_item_mode_fit_score(
    mapped_types: list[str],
    *,
    policy: dict[str, Any],
    priority_types: list[str],
    available_types: set[str],
    valid_item_count: int,
    total_item_count: int,
) -> float:
    if total_item_count <= 0:
        return 1.0 if not available_types else 0.0

    valid_ratio = valid_item_count / max(1, total_item_count)
    if not priority_types:
        return round(valid_ratio, 4)

    early_types = [candidate_type for candidate_type in mapped_types[: min(3, len(mapped_types))] if candidate_type]
    top_priority = set(priority_types[:3])
    early_priority_ratio = (
        sum(1 for candidate_type in early_types if candidate_type in top_priority) / max(1, len(early_types))
        if early_types
        else valid_ratio
    )

    mode = str(policy.get("mode") or "balanced")
    unique_types = {candidate_type for candidate_type in mapped_types if candidate_type}
    if mode == "balanced":
        coverage_pool = set(priority_types)
        coverage_target = min(4, max(1, len(priority_types)))
    else:
        coverage_pool = set(priority_types[: max(3, min(4, len(priority_types)))])
        coverage_target = min(3, max(1, len(coverage_pool)))
    coverage_score = min(1.0, len(unique_types & coverage_pool) / max(1, coverage_target))

    return round((valid_ratio * 0.55) + (early_priority_ratio * 0.35) + (coverage_score * 0.10), 4)


def _available_candidate_types(context: dict[str, Any], enabled_types: set[str]) -> set[str]:
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    available: set[str] = set()
    for candidate_type, values in candidates.items():
        if enabled_types and str(candidate_type) not in enabled_types:
            continue
        if isinstance(values, list) and values:
            available.add(str(candidate_type))
    return available


def _context_source_ids(context: dict[str, Any]) -> set[str]:
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    source_ids: set[str] = set()
    for values in candidates.values():
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
            for key in ("source_id", "question_id", "task_id", "attempt_id", "set_id", "practice_set_id", "topic"):
                value = str(item.get(key) or "").strip()
                if value:
                    source_ids.add(value)
    return source_ids


def _plan_item_type_to_candidate_type(item_type: str) -> str:
    mapping = {
        "topic_review": "weak_topics",
        "wrong_pool": "wrong_questions",
        "wrong_question": "wrong_questions",
        "pending_review": "pending_review_items",
        "pending_item": "pending_review_items",
        "review_due": "review_tasks",
        "review_task": "review_tasks",
        "continue_draft": "draft_attempts",
        "draft_attempt": "draft_attempts",
        "startup_question": "startup_candidates",
        "new_start": "startup_candidates",
        "unstarted_question": "unstarted_questions",
        "favorite_review": "favorite_unmastered",
    }
    if item_type in AI_REVIEW_PLAN_CANDIDATE_TYPES:
        return item_type
    return mapping.get(item_type, "")


def _synthetic_candidates_for_persona(persona: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    wrong_count = _level_count(persona.get("wrong_level"), high=8, medium=4, low=1)
    pending_count = _level_count(persona.get("pending_review_level"), high=6, medium=3, low=1)
    overdue_count = _level_count(persona.get("overdue_level"), high=5, medium=2, low=1)
    draft_count = _level_count(persona.get("draft_level"), high=5, medium=2, low=1)
    unstarted_count = _level_count(persona.get("unstarted_level"), high=10, medium=5, low=1)
    manual_count = _level_count(persona.get("manual_state_level"), high=4, medium=2, low=1)
    weak_count = 0 if str(persona.get("category") or "") == "cold_start" else max(1, wrong_count // 2)

    startup_count = max(3, unstarted_count) if unstarted_count > 0 else 0

    return {
        "weak_topics": _candidate_rows("weak_topics", weak_count, persona),
        "wrong_questions": _candidate_rows("wrong_questions", wrong_count, persona),
        "pending_review_items": _candidate_rows("pending_review_items", pending_count, persona),
        "review_tasks": _candidate_rows("review_tasks", overdue_count, persona),
        "draft_attempts": _candidate_rows("draft_attempts", draft_count, persona),
        "unstarted_questions": _candidate_rows("unstarted_questions", unstarted_count, persona),
        "startup_candidates": _candidate_rows("startup_candidates", startup_count, persona),
        "favorite_unmastered": _candidate_rows("favorite_unmastered", manual_count, persona),
    }


def _deterministic_plan_tasks(
    candidates: dict[str, list[dict[str, Any]]],
    policy: dict[str, Any],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    mode = str(policy.get("mode") or "balanced")
    ordered_types = MODE_PREFERRED_TYPES.get(mode, MODE_PREFERRED_TYPES["balanced"])
    tasks: list[dict[str, Any]] = []
    for candidate_type in ordered_types:
        for candidate in candidates.get(candidate_type) or []:
            tasks.append({**candidate, "candidate_type": candidate_type})
            if len(tasks) >= limit:
                return tasks
    return tasks


def _draft_from_evaluation_tasks(
    tasks: list[dict[str, Any]],
    *,
    days: int,
    tasks_per_day: int,
) -> dict[str, Any]:
    safe_days = max(1, int(days or 1))
    safe_tasks_per_day = max(1, int(tasks_per_day or 1))
    draft_days: list[dict[str, Any]] = []
    task_index = 0
    for day_index in range(safe_days):
        items: list[dict[str, Any]] = []
        for _ in range(safe_tasks_per_day):
            if task_index >= len(tasks):
                break
            task = tasks[task_index]
            task_index += 1
            source_id = _candidate_source_id(task)
            items.append(
                {
                    "type": str(task.get("candidate_type") or ""),
                    "title": str(task.get("title") or source_id or "synthetic task"),
                    "reason": "synthetic evaluation",
                    "estimated_minutes": 20,
                    "source_ids": [source_id] if source_id else [],
                }
            )
        draft_days.append({"date": f"synthetic-day-{day_index + 1}", "items": items})
    return {"days": draft_days}


def _candidate_source_id(candidate: dict[str, Any]) -> str:
    for key in ("source_id", "question_id", "task_id", "attempt_id", "set_id", "practice_set_id", "topic"):
        value = str(candidate.get(key) or "").strip()
        if value:
            return value
    return ""


def _duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    duplicate_seen: set[str] = set()
    for value in values:
        if not value:
            continue
        if value in seen and value not in duplicate_seen:
            duplicates.append(value)
            duplicate_seen.add(value)
        seen.add(value)
    return duplicates


def _candidate_counts_by_type(candidates: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    return {
        candidate_type: len(candidates.get(candidate_type) or [])
        for candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES
    }


def _flat_candidate_counts_by_type(candidates: list[dict[str, Any]]) -> dict[str, int]:
    counts = {candidate_type: 0 for candidate_type in AI_REVIEW_PLAN_CANDIDATE_TYPES}
    for candidate in candidates:
        candidate_type = str(candidate.get("candidate_type") or "")
        if candidate_type in counts:
            counts[candidate_type] += 1
    return counts


def _mode_fit_score(tasks: list[dict[str, Any]], policy: dict[str, Any]) -> float:
    if not tasks:
        return 0.0
    mode = str(policy.get("mode") or "balanced")
    preferred = set(MODE_PREFERRED_TYPES.get(mode, MODE_PREFERRED_TYPES["balanced"])[:3])
    enabled = set(str(value) for value in policy.get("enabled_types") or [])
    valid_ratio = sum(1 for task in tasks if task.get("candidate_type") in enabled) / len(tasks)
    preferred_ratio = sum(1 for task in tasks[:3] if task.get("candidate_type") in preferred) / min(3, len(tasks))
    return round((valid_ratio * 0.55) + (preferred_ratio * 0.45), 4)


def _candidate_rows(candidate_type: str, count: int, persona: dict[str, Any]) -> list[dict[str, Any]]:
    persona_id = str(persona.get("persona_id") or "persona")
    rows: list[dict[str, Any]] = []
    for index in range(1, max(0, count) + 1):
        row = {
            "candidate_type": candidate_type,
            "source_id": f"{persona_id}:{candidate_type}:{index}",
            "title": f"{persona_id} {candidate_type} {index}",
            "priority": max(0.1, 1.0 - index * 0.03),
        }
        row.update(_synthetic_candidate_load_fields(row, candidate_type, index, persona))
        rows.append(row)
    return rows


def _synthetic_candidate_load_fields(
    row: dict[str, Any],
    candidate_type: str,
    index: int,
    persona: dict[str, Any],
) -> dict[str, Any]:
    question_count = 1
    if candidate_type == "weak_topics":
        question_count = 3
    elif candidate_type == "review_tasks":
        question_count = 2
    elif candidate_type == "draft_attempts":
        question_count = 8 + (index % 4)
    elif candidate_type in {"unstarted_questions", "startup_candidates"}:
        question_count = 4
    if str(persona.get("scope_profile") or "") == "large_practice_sheet" and candidate_type in {
        "draft_attempts",
        "unstarted_questions",
        "startup_candidates",
    }:
        question_count = max(question_count, 16 + (index % 5))
    question_type = "single_choice"
    if str(persona.get("scope_profile") or "") in {"advanced", "solution_avoidance"}:
        question_type = "solution"
    if str(persona.get("scope_profile") or "") == "mixed_question_types":
        question_type = ("single_choice", "fill_blank", "solution", "proof")[index % 4]
    if str(persona.get("learning_trait") or "").startswith("proof"):
        question_type = "proof"
    candidate = {
        **row,
        "question_count": question_count,
        "question_ids": [
            f"{row['source_id']}:q{question_index}"
            for question_index in range(1, question_count + 1)
        ],
        "question_type": question_type,
        "difficulty": "unknown",
    }
    return calculate_candidate_load(candidate, candidate_type)


def _level_count(value: Any, *, high: int, medium: int, low: int) -> int:
    key = str(value or "none").strip().lower()
    if key == "high":
        return high
    if key == "medium":
        return medium
    if key == "low":
        return low
    if key == "mixed":
        return max(1, medium)
    return 0
