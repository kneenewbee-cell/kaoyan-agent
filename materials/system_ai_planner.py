from __future__ import annotations

import json
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


DEFAULT_AI_REVIEW_PLAN_MODEL = "deepseek-v4-flash"
DEFAULT_AI_REVIEW_PLAN_TIMEOUT_SECONDS = 20.0
DEFAULT_AI_REVIEW_PLAN_MAX_TOKENS = 3200
ROOT = Path(__file__).resolve().parents[1]
DAILY_LOAD_TARGET_RATIO = 0.85
MIN_TOP_UP_REMAINING_MINUTES = 5
TOP_UP_CANDIDATE_TYPES = (
    "weak_topics",
    "wrong_questions",
    "draft_attempts",
    "unstarted_questions",
    "startup_candidates",
    "favorite_unmastered",
)
PLAN_ITEM_TYPE_BY_CANDIDATE_TYPE = {
    "weak_topics": "topic_review",
    "wrong_questions": "wrong_question",
    "draft_attempts": "continue_draft",
    "unstarted_questions": "unstarted_question",
    "startup_candidates": "startup_question",
    "favorite_unmastered": "favorite_review",
}
MERGEABLE_PLAN_ITEM_FAMILY_BY_CANDIDATE_TYPE = {
    "startup_candidates": "new_start",
    "unstarted_questions": "new_start",
    "wrong_questions": "wrong_questions",
    "favorite_unmastered": "favorite_unmastered",
}
MERGED_PLAN_ITEM_TYPE_BY_FAMILY = {
    "new_start": "unstarted_question",
    "wrong_questions": "wrong_question",
    "pending_review_items": "pending_review",
    "favorite_unmastered": "favorite_review",
}
MERGED_PLAN_ITEM_LABEL_BY_FAMILY = {
    "new_start": "新题启动",
    "wrong_questions": "错题回收",
    "pending_review_items": "待核对复习",
    "favorite_unmastered": "收藏题复习",
}


def generate_ai_review_plan_draft(
    *,
    context: dict[str, Any],
    model: str = DEFAULT_AI_REVIEW_PLAN_MODEL,
) -> dict[str, Any]:
    """Generate a review-plan draft from compressed learning context.

    This function is intentionally side-effect free. It returns a draft only;
    accepting and writing review tasks is a later explicit workflow step.
    """

    safe_model = str(model or DEFAULT_AI_REVIEW_PLAN_MODEL).strip() or DEFAULT_AI_REVIEW_PLAN_MODEL
    try:
        parsed = _call_planning_model_with_timeout(context=context, model=safe_model)
        return _normalize_ai_plan_payload(parsed, context=context, model=safe_model)
    except Exception as exc:
        return _fallback_review_plan_draft(
            context=context,
            model=safe_model,
            warning=f"AI planning fallback: {exc.__class__.__name__}",
        )


def build_blocked_ai_review_plan_draft(
    *,
    context: dict[str, Any],
    model: str = DEFAULT_AI_REVIEW_PLAN_MODEL,
    warning: str | None = None,
) -> dict[str, Any]:
    """Return an explicit no-model draft when the selected mode lacks usable data."""

    constraints = context.get("constraints") if isinstance(context.get("constraints"), dict) else {}
    readiness = context.get("readiness") if isinstance(context.get("readiness"), dict) else {}
    days_count = _safe_int(constraints.get("days"), 7, minimum=1, maximum=30)
    start_date = datetime.now(timezone.utc).date()
    reason = str(readiness.get("reason") or "Selected planning mode does not have enough usable data.")
    recommended_actions = [
        str(item).strip()
        for item in (readiness.get("recommended_actions") or [])
        if str(item).strip()
    ]
    days = [
        {
            "date": (start_date + timedelta(days=index)).isoformat(),
            "items": [],
        }
        for index in range(days_count)
    ]
    warnings = [warning] if warning else []
    warnings.append(reason)
    return {
        "plan_id": f"blocked_plan_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "model": str(model or DEFAULT_AI_REVIEW_PLAN_MODEL).strip() or DEFAULT_AI_REVIEW_PLAN_MODEL,
        "days": days,
        "warnings": warnings,
        "source": "blocked",
        "skipped_llm": True,
        "writes_review_tasks": False,
        "readiness_status": str(readiness.get("status") or "blocked"),
        "recommended_actions": recommended_actions,
    }


def _planning_timeout_seconds() -> float:
    try:
        parsed = float(os.getenv("AI_REVIEW_PLAN_TIMEOUT_SECONDS", ""))
    except ValueError:
        parsed = DEFAULT_AI_REVIEW_PLAN_TIMEOUT_SECONDS
    if parsed <= 0:
        return DEFAULT_AI_REVIEW_PLAN_TIMEOUT_SECONDS
    return min(parsed, 60.0)


def _planning_max_tokens() -> int:
    try:
        parsed = int(os.getenv("AI_REVIEW_PLAN_MAX_TOKENS", ""))
    except ValueError:
        parsed = DEFAULT_AI_REVIEW_PLAN_MAX_TOKENS
    if parsed <= 0:
        return DEFAULT_AI_REVIEW_PLAN_MAX_TOKENS
    return max(256, min(parsed, 4096))


def _call_planning_model_with_timeout(*, context: dict[str, Any], model: str) -> dict[str, Any]:
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_call_planning_model, context=context, model=model)
    try:
        return future.result(timeout=_planning_timeout_seconds())
    except FutureTimeoutError as exc:
        future.cancel()
        raise TimeoutError("ai review planning model timed out") from exc
    finally:
        executor.shutdown(wait=False, cancel_futures=True)


def _call_planning_model(*, context: dict[str, Any], model: str) -> dict[str, Any]:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    api_key = (
        os.getenv("AI_REVIEW_PLAN_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("ROUTER_API_KEY")
        or os.getenv("MATH_API_KEY")
    )
    base_url = (
        os.getenv("AI_REVIEW_PLAN_BASE_URL")
        or os.getenv("DEEPSEEK_BASE_URL")
        or os.getenv("ROUTER_BASE_URL")
        or os.getenv("MATH_BASE_URL")
    )
    if not api_key or not base_url:
        raise RuntimeError("missing deepseek api settings")

    from openai import OpenAI
    from qa.kaoyan_agent import parse_json_object
    from qa.usage_tracking import notify_usage

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=25.0, max_retries=0)
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=_planning_max_tokens(),
        response_format={"type": "json_object"},
        extra_body={"thinking": {"type": "disabled"}},
        messages=[
            {
                "role": "system",
                "content": (
                    "你是考研复习规划助手。只根据给定学习数据生成规划草案，"
                    "不要编造不存在的题目或任务。只输出 JSON。"
                ),
            },
            {"role": "user", "content": _planning_prompt(context)},
        ],
    )
    notify_usage(
        kind="chat",
        name="tool_llm:ai_review_plan",
        model=model,
        response=response,
        started_at=started,
        tool_name="ai_review_plan",
        provider="deepseek",
    )
    content = response.choices[0].message.content or ""
    if not content.strip():
        raise ValueError("ai review planning model returned empty content")
    return parse_json_object(content)


def _planning_prompt(context: dict[str, Any]) -> str:
    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    constraints = context.get("constraints") if isinstance(context.get("constraints"), dict) else {}
    priority = policy.get("type_priority") if isinstance(policy.get("type_priority"), list) else []
    priority_text = " > ".join(str(value) for value in priority if str(value).strip()) or "按 policy.enabled_types"
    daily_minutes = _safe_int(constraints.get("daily_minutes"), 60, minimum=15, maximum=240)
    daily_floor = int(math.ceil(daily_minutes * DAILY_LOAD_TARGET_RATIO))
    compact_context = json.dumps(context, ensure_ascii=False, sort_keys=True)
    return (
        "请基于下面的压缩学习画像生成一份复习规划草案。\n"
        "要求：\n"
        "1. days 数量必须等于 constraints.days。\n"
        f"2. 每天 estimated_minutes 总和要尽量接近 constraints.daily_minutes；候选足够时至少达到每日时长目标 {daily_floor} 分钟，且不要明显超过 {daily_minutes} 分钟。\n"
        "3. 优先处理到期/逾期任务、待核对题、错题和薄弱知识点。\n"
        "4. 每个 item 都要有 type、title、reason、estimated_minutes，可带 source_ids。\n"
        "5. 每天 item 数不是固定 3 个；不要按题数或 item 数设上限，单题较短时按预计分钟继续增加题数，或把同类单题合并到一个 item，直到接近每日时长目标。\n"
        "6. reason 用一句话说明，不要展开解题过程。\n"
        "7. 这是草案，不要声称已经写入复习任务。\n"
        "8. item.type 优先使用 policy.enabled_types 里的候选类型名，不要使用 policy.disabled_types 的类型。\n"
        "9. 规划模式以 constraints.mode 和 policy.intent 为准：错题回收不混入普通新题，新题启动优先未开始或起步候选。\n"
        f"10. 优先类型顺序：{priority_text}。前半段任务应主要来自靠前的 3 类；候选不足时再使用后续类型。\n"
        "11. 不要平均铺开所有类型；不要为了多样性牺牲当前模式目标。\n"
        "12. 如果当前模式没有可用候选，days 仍保留，但 items 可为空，并在 warnings 中建议切换更合适的模式。\n"
        "13. 以候选项里的 load_units 和 estimated_minutes 为准，不要自行发明耗时或裸按题数平均。\n"
        "14. 每天负载尽量接近；不区分周末/工作日，除非 constraints 里显式给出不同日预算。\n"
        "15. 题型会影响任务量：选择/填空/解答/证明/综合题不能简单按 1 题等价处理。\n"
        "16. 不要自行拆分练习单；如果候选里已有 part_index/part_count，只能选择这些预拆分片段。\n"
        "17. 选择练习单片段时保留 parent_practice_set_id、part_index、part_count、load_units。\n"
        "输出 JSON：{\"plan_id\":\"...\",\"model\":\"...\",\"days\":[{\"date\":\"YYYY-MM-DD\",\"items\":[{\"type\":\"...\",\"title\":\"...\",\"reason\":\"...\",\"estimated_minutes\":0,\"load_units\":0,\"source_ids\":[]}]}],\"warnings\":[]}\n\n"
        f"学习画像：\n{compact_context}"
    )


def _normalize_ai_plan_payload(
    payload: Any,
    *,
    context: dict[str, Any],
    model: str,
) -> dict[str, Any]:
    data = payload if isinstance(payload, dict) else {}
    constraints = context.get("constraints") if isinstance(context.get("constraints"), dict) else {}
    expected_days = _safe_int(constraints.get("days"), 7, minimum=1, maximum=30)
    raw_days = data.get("days") if isinstance(data.get("days"), list) else []
    title_lookup = _context_title_lookup(context)
    candidate_lookup = _context_candidate_lookup(context)
    valid_source_ids = _context_source_id_set(context)
    normalized_days: list[dict[str, Any]] = []
    fallback: dict[str, Any] | None = None

    def fallback_day_items(day_index: int) -> list[dict[str, Any]]:
        nonlocal fallback
        if fallback is None:
            fallback = _fallback_review_plan_draft(context=context, model=model, warning="")
        fallback_days = fallback.get("days") if isinstance(fallback.get("days"), list) else []
        if day_index >= len(fallback_days):
            return []
        items = fallback_days[day_index].get("items") if isinstance(fallback_days[day_index], dict) else []
        return items if isinstance(items, list) else []

    for day_index, raw_day in enumerate(raw_days[:expected_days]):
        if not isinstance(raw_day, dict):
            continue
        items = raw_day.get("items") if isinstance(raw_day.get("items"), list) else []
        normalized_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            normalized = _normalize_plan_item(
                item,
                title_lookup=title_lookup,
                candidate_lookup=candidate_lookup,
            )
            if _plan_item_has_valid_sources(normalized, context=context, valid_source_ids=valid_source_ids):
                normalized_items.append(normalized)
        if not normalized_items:
            normalized_items = fallback_day_items(day_index)
        normalized_days.append(
            {
                "date": str(raw_day.get("date") or ""),
                "items": normalized_items,
            }
        )
    if len(normalized_days) < expected_days:
        if fallback is None:
            fallback = _fallback_review_plan_draft(context=context, model=model, warning="")
        normalized_days = (normalized_days + fallback["days"][len(normalized_days) :])[:expected_days]
    normalized_days = _ensure_requested_draft_attempt_item(
        normalized_days,
        context=context,
        title_lookup=title_lookup,
        valid_source_ids=valid_source_ids,
    )
    normalized_days = _dedupe_plan_days_by_source(normalized_days)
    normalized_days = _rebalance_plan_days_by_load(normalized_days, context=context)
    normalized_days = _top_up_underfilled_plan_days(normalized_days, context=context)
    normalized_days = _merge_plan_day_items_by_family(normalized_days)
    warnings = data.get("warnings") if isinstance(data.get("warnings"), list) else []
    return {
        "plan_id": str(data.get("plan_id") or f"ai_plan_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"),
        "model": model,
        "days": normalized_days,
        "warnings": [str(item) for item in warnings if str(item).strip()][:5],
        "source": "llm",
        "writes_review_tasks": False,
    }


def _dedupe_plan_days_by_source(days: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen_source_ids: set[str] = set()
    deduped_days: list[dict[str, Any]] = []
    for day in days:
        if not isinstance(day, dict):
            continue
        next_items: list[dict[str, Any]] = []
        items = day.get("items") if isinstance(day.get("items"), list) else []
        for item in items:
            if not isinstance(item, dict):
                continue
            candidate_type = _plan_item_candidate_type(str(item.get("type") or ""))
            source_ids = [
                str(value).strip()
                for value in item.get("source_ids") or []
                if str(value).strip()
            ]
            if not candidate_type or not source_ids:
                next_items.append(item)
                continue
            unused_source_ids = [source_id for source_id in source_ids if source_id not in seen_source_ids]
            if not unused_source_ids:
                continue
            seen_source_ids.update(unused_source_ids)
            if len(unused_source_ids) != len(source_ids):
                item = {**item, "source_ids": unused_source_ids}
            next_items.append(item)
        deduped_days.append({**day, "items": next_items})
    return deduped_days


def _ensure_requested_draft_attempt_item(
    days: list[dict[str, Any]],
    *,
    context: dict[str, Any],
    title_lookup: dict[str, str],
    valid_source_ids: set[str],
) -> list[dict[str, Any]]:
    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    enabled_types = set(str(value) for value in policy.get("enabled_types") or [])
    requested_types = set(str(value) for value in policy.get("requested_types") or [])
    if "draft_attempts" not in enabled_types:
        return days
    if requested_types and "draft_attempts" not in requested_types:
        return days

    for day in days:
        items = day.get("items") if isinstance(day.get("items"), list) else []
        if any(_plan_item_candidate_type(str(item.get("type") or "")) == "draft_attempts" for item in items if isinstance(item, dict)):
            return days

    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    drafts = candidates.get("draft_attempts") if isinstance(candidates.get("draft_attempts"), list) else []
    if not drafts or not days:
        return days

    draft = next((item for item in drafts if isinstance(item, dict)), None)
    if not draft:
        return days
    attempt_id = _candidate_source_id(draft, "attempt_id")
    if not attempt_id:
        return days
    title = str(draft.get("title") or draft.get("practice_set_title") or "继续未提交练习").strip()
    unanswered_count = _safe_int(draft.get("unanswered_count"), 0, minimum=0, maximum=999)
    question_count = _safe_int(draft.get("question_count"), 0, minimum=0, maximum=999)
    reason = "你已勾选未提交练习，先收尾这份草稿，避免练习记录长期悬空。"
    if unanswered_count:
        reason = f"你已勾选未提交练习，这份草稿还有 {unanswered_count} 题未完成，适合先继续作答。"
    elif question_count:
        reason = f"你已勾选未提交练习，这份草稿共 {question_count} 题，适合先收尾。"
    item = _normalize_plan_item(
        {
            "type": "continue_draft",
            "title": title,
            "reason": reason,
            "estimated_minutes": min(30, max(10, unanswered_count * 6 if unanswered_count else 20)),
            "source_ids": [attempt_id],
        },
        title_lookup=title_lookup,
    )
    if not _plan_item_has_valid_sources(item, context=context, valid_source_ids=valid_source_ids):
        return days

    first_day = days[0]
    first_items = first_day.get("items") if isinstance(first_day.get("items"), list) else []
    first_day["items"] = first_items + [item]
    return days


def _rebalance_plan_days_by_load(
    days: list[dict[str, Any]],
    *,
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    """Keep mixed planning drafts from bunching one candidate type on later days."""

    if len(days) < 2:
        return days

    movable_candidate_types = {
        "weak_topics",
        "wrong_questions",
        "draft_attempts",
        "unstarted_questions",
        "startup_candidates",
        "favorite_unmastered",
    }
    normalized_days = [
        {
            **day,
            "items": [
                dict(item)
                for item in (day.get("items") if isinstance(day.get("items"), list) else [])
                if isinstance(item, dict)
            ],
        }
        for day in days
        if isinstance(day, dict)
    ]
    if len(normalized_days) < 2:
        return normalized_days

    pinned_by_day: list[list[dict[str, Any]]] = [[] for _ in normalized_days]
    movable_items: list[tuple[int, int, dict[str, Any]]] = []
    pending_items: list[dict[str, Any]] = []

    for day_index, day in enumerate(normalized_days):
        for item_index, item in enumerate(day.get("items") or []):
            candidate_type = _plan_item_candidate_type(str(item.get("type") or ""))
            if candidate_type == "pending_review_items":
                pending_items.append(item)
            elif candidate_type in movable_candidate_types:
                movable_items.append((day_index, item_index, item))
            else:
                pinned_by_day[day_index].append(item)

    if pending_items:
        pinned_by_day[0] = pending_items + pinned_by_day[0]

    candidate_lookup = _context_candidate_lookup(context)
    if len(movable_items) < 2:
        for day_index, day in enumerate(normalized_days):
            day["items"] = (
                pinned_by_day[day_index]
                + [item for original_day_index, _, item in movable_items if original_day_index == day_index]
            )
        return normalized_days

    day_loads = [
        sum(_plan_item_load_minutes(item, candidate_lookup=candidate_lookup) for item in day_items)
        for day_items in pinned_by_day
    ]
    day_items = [list(items) for items in pinned_by_day]
    sorted_movable = sorted(
        movable_items,
        key=lambda row: (-_plan_item_load_minutes(row[2], candidate_lookup=candidate_lookup), row[0], row[1]),
    )

    for _, _, item in sorted_movable:
        target_indexes = list(range(len(day_items)))
        target_index = min(
            target_indexes,
            key=lambda index: (day_loads[index], len(day_items[index]), index),
        )
        day_items[target_index].append(item)
        day_loads[target_index] += _plan_item_load_minutes(item, candidate_lookup=candidate_lookup)

    for day_index, day in enumerate(normalized_days):
        day["items"] = day_items[day_index]
    return normalized_days


def _top_up_underfilled_plan_days(
    days: list[dict[str, Any]],
    *,
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    constraints = context.get("constraints") if isinstance(context.get("constraints"), dict) else {}
    daily_minutes = _safe_int(constraints.get("daily_minutes"), 60, minimum=15, maximum=240)
    target_floor = int(math.ceil(daily_minutes * DAILY_LOAD_TARGET_RATIO))
    candidate_lookup = _context_candidate_lookup(context)
    used_source_ids = _plan_used_source_ids(days)
    topped_days = [
        {
            **day,
            "items": [
                dict(item)
                for item in (day.get("items") if isinstance(day.get("items"), list) else [])
                if isinstance(item, dict)
            ],
        }
        for day in days
        if isinstance(day, dict)
    ]

    for day in topped_days:
        items = day.get("items") if isinstance(day.get("items"), list) else []
        day_load = sum(_plan_item_load_minutes(item, candidate_lookup=candidate_lookup) for item in items)
        while day_load < target_floor:
            remaining_minutes = daily_minutes - day_load
            if remaining_minutes < MIN_TOP_UP_REMAINING_MINUTES:
                break
            top_up_item = _next_top_up_plan_item(
                context,
                used_source_ids=used_source_ids,
                remaining_minutes=remaining_minutes,
            )
            if not top_up_item:
                break
            item_minutes = _plan_item_load_minutes(top_up_item, candidate_lookup=candidate_lookup)
            if item_minutes <= 0 or day_load + item_minutes > daily_minutes:
                break
            items.append(top_up_item)
            used_source_ids.update(
                str(source_id).strip()
                for source_id in top_up_item.get("source_ids") or []
                if str(source_id).strip()
            )
            day_load += item_minutes
        day["items"] = items
    return topped_days


def _next_top_up_plan_item(
    context: dict[str, Any],
    *,
    used_source_ids: set[str],
    remaining_minutes: int,
) -> dict[str, Any] | None:
    if remaining_minutes < MIN_TOP_UP_REMAINING_MINUTES:
        return None
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    for candidate_type in _top_up_candidate_type_order(context):
        values = candidates.get(candidate_type) if isinstance(candidates.get(candidate_type), list) else []
        if candidate_type == "draft_attempts":
            for candidate in values:
                if not isinstance(candidate, dict):
                    continue
                source_id = _candidate_source_id(candidate)
                if not source_id or source_id in used_source_ids:
                    continue
                candidate_minutes = _candidate_plan_minutes(candidate)
                if 0 < candidate_minutes <= remaining_minutes:
                    return _build_top_up_plan_item(candidate_type, [candidate])
            continue
        batch: list[dict[str, Any]] = []
        batch_minutes = 0
        for candidate in values:
            if not isinstance(candidate, dict):
                continue
            source_id = _candidate_source_id(candidate)
            if not source_id or source_id in used_source_ids:
                continue
            candidate_minutes = _candidate_plan_minutes(candidate)
            if candidate_minutes <= 0:
                continue
            if batch and batch_minutes + candidate_minutes > remaining_minutes:
                break
            if not batch and candidate_minutes > remaining_minutes:
                continue
            batch.append(candidate)
            batch_minutes += candidate_minutes
        if batch:
            return _build_top_up_plan_item(candidate_type, batch)
    return None


def _top_up_candidate_type_order(context: dict[str, Any]) -> list[str]:
    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    enabled = set(str(value) for value in policy.get("enabled_types") or [])
    ordered = [
        str(value)
        for value in (policy.get("type_priority") or policy.get("enabled_types") or [])
        if str(value) in TOP_UP_CANDIDATE_TYPES and (not enabled or str(value) in enabled)
    ]
    seen = set(ordered)
    ordered.extend(
        candidate_type
        for candidate_type in TOP_UP_CANDIDATE_TYPES
        if candidate_type not in seen and (not enabled or candidate_type in enabled)
    )
    return ordered


def _build_top_up_plan_item(candidate_type: str, batch: list[dict[str, Any]]) -> dict[str, Any]:
    source_ids = [_candidate_source_id(candidate) for candidate in batch]
    source_ids = [source_id for source_id in source_ids if source_id]
    total_minutes = sum(_candidate_plan_minutes(candidate) for candidate in batch)
    total_load = sum(_candidate_plan_load_units(candidate) for candidate in batch)
    question_count = sum(max(1, _candidate_effective_question_count(candidate)) for candidate in batch)
    title = _top_up_plan_item_title(candidate_type, batch, question_count)
    reason = "当天计划低于每日时长目标，补入同模式候选以接近时间预算。"
    item: dict[str, Any] = {
        "type": PLAN_ITEM_TYPE_BY_CANDIDATE_TYPE.get(candidate_type, candidate_type),
        "title": title,
        "reason": reason,
        "estimated_minutes": total_minutes,
        "source_ids": source_ids,
        "question_count": question_count,
    }
    if total_load > 0:
        item["load_units"] = round(total_load, 2)
    if len(batch) == 1:
        candidate = batch[0]
        for key in (
            "parent_practice_set_id",
            "parent_source_id",
            "plan_segment_id",
            "part_index",
            "part_count",
            "planned_question_ids",
            "question_type_mix",
            "state_mix",
            "difficulty_mix",
        ):
            if key in candidate:
                item[key] = candidate[key]
    return item


def _top_up_plan_item_title(candidate_type: str, batch: list[dict[str, Any]], question_count: int) -> str:
    if len(batch) == 1:
        title = str(batch[0].get("title") or batch[0].get("question_title") or batch[0].get("topic") or "").strip()
        if title:
            return title
    labels = {
        "weak_topics": "薄弱知识点复习",
        "wrong_questions": "错题回收",
        "draft_attempts": "继续未提交练习",
        "unstarted_questions": "新题启动",
        "startup_candidates": "新题启动",
        "favorite_unmastered": "收藏题复习",
    }
    label = labels.get(candidate_type, "复习任务")
    unit = "项" if candidate_type in {"weak_topics", "draft_attempts"} else "道题"
    count = question_count if question_count > 0 else len(batch)
    return f"{label} {count} {unit}"


def _candidate_plan_minutes(candidate: dict[str, Any]) -> int:
    minutes = _safe_int(candidate.get("estimated_minutes"), 0, minimum=0, maximum=180)
    if minutes > 0:
        return minutes
    question_count = _candidate_effective_question_count(candidate)
    if question_count > 0:
        return min(180, max(5, question_count * 6))
    return 0


def _candidate_plan_load_units(candidate: dict[str, Any]) -> float:
    try:
        parsed = float(candidate.get("load_units") or 0)
    except (TypeError, ValueError):
        parsed = 0.0
    return max(0.0, parsed)


def _plan_used_source_ids(days: list[dict[str, Any]]) -> set[str]:
    source_ids: set[str] = set()
    for day in days:
        if not isinstance(day, dict):
            continue
        items = day.get("items") if isinstance(day.get("items"), list) else []
        for item in items:
            if not isinstance(item, dict):
                continue
            source_ids.update(
                str(source_id).strip()
                for source_id in item.get("source_ids") or []
                if str(source_id).strip()
            )
    return source_ids


def _plan_item_load_minutes(
    item: dict[str, Any],
    *,
    candidate_lookup: dict[str, dict[str, Any]] | None = None,
) -> int:
    base_minutes = _safe_int(item.get("estimated_minutes"), 20, minimum=5, maximum=180)
    candidate_type = _plan_item_candidate_type(str(item.get("type") or ""))
    lookup = candidate_lookup or {}
    source_ids = [str(value).strip() for value in item.get("source_ids") or [] if str(value).strip()]
    candidate_minutes = _candidate_source_estimated_minutes(source_ids, lookup)
    if candidate_minutes > 0:
        return min(180, candidate_minutes)

    if candidate_type in {
        "wrong_questions",
        "unstarted_questions",
        "startup_candidates",
        "favorite_unmastered",
        "pending_review_items",
    }:
        effective_question_count = 0
        for source_id in source_ids:
            candidate = lookup.get(source_id)
            if candidate:
                effective_question_count += max(1, _candidate_effective_question_count(candidate))
            else:
                effective_question_count += 1
        if effective_question_count > 0:
            question_load_minutes = min(180, max(10, effective_question_count * 6))
            return max(base_minutes, question_load_minutes)
        return base_minutes

    if candidate_type not in {"draft_attempts"}:
        return base_minutes

    effective_question_count = 0
    for source_id in source_ids:
        candidate = lookup.get(source_id)
        if not candidate:
            continue
        effective_question_count += _candidate_effective_question_count(candidate)

    if effective_question_count <= 0:
        return base_minutes
    question_load_minutes = min(180, max(10, effective_question_count * 6))
    return max(base_minutes, question_load_minutes)


def _candidate_source_estimated_minutes(
    source_ids: list[str],
    candidate_lookup: dict[str, dict[str, Any]],
) -> int:
    total = 0
    for source_id in source_ids:
        candidate = candidate_lookup.get(source_id)
        if not isinstance(candidate, dict):
            continue
        minutes = _safe_int(candidate.get("estimated_minutes"), 0, minimum=0, maximum=180)
        if minutes > 0:
            total += minutes
    return total


def _candidate_source_load_units(
    source_ids: list[str],
    candidate_lookup: dict[str, dict[str, Any]],
) -> float:
    total = 0.0
    for source_id in source_ids:
        candidate = candidate_lookup.get(source_id)
        if not isinstance(candidate, dict):
            continue
        total += _candidate_plan_load_units(candidate)
    return round(total, 2)


def _candidate_source_question_count(
    source_ids: list[str],
    candidate_lookup: dict[str, dict[str, Any]],
) -> int:
    total = 0
    for source_id in source_ids:
        candidate = candidate_lookup.get(source_id)
        if isinstance(candidate, dict):
            total += max(1, _candidate_effective_question_count(candidate))
        elif source_id:
            total += 1
    return total


def _candidate_effective_question_count(candidate: dict[str, Any]) -> int:
    unanswered_count = _safe_int(candidate.get("unanswered_count"), 0, minimum=0, maximum=999)
    question_count = _safe_int(candidate.get("question_count"), 0, minimum=0, maximum=999)
    question_ids = candidate.get("question_ids") if isinstance(candidate.get("question_ids"), list) else []
    return unanswered_count or question_count or len(question_ids)


def _normalize_plan_item(
    item: dict[str, Any],
    *,
    title_lookup: dict[str, str] | None = None,
    candidate_lookup: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    source_ids = [str(value) for value in item.get("source_ids") or [] if str(value).strip()]
    title = _repair_title_from_sources(str(item.get("title") or ""), source_ids, title_lookup or {})
    lookup = candidate_lookup or {}
    candidate = _first_candidate_for_source_ids(source_ids, lookup)
    if candidate and candidate.get("part_index"):
        title = str(candidate.get("title") or title).strip() or title
    estimated_minutes = _safe_int(item.get("estimated_minutes"), 20, minimum=5, maximum=180)
    source_minutes = _candidate_source_estimated_minutes(source_ids, lookup)
    source_load_units = _candidate_source_load_units(source_ids, lookup)
    source_question_count = _candidate_source_question_count(source_ids, lookup)
    if source_minutes > 0:
        estimated_minutes = source_minutes
    elif candidate and candidate.get("estimated_minutes") is not None:
        estimated_minutes = _safe_int(candidate.get("estimated_minutes"), estimated_minutes, minimum=5, maximum=180)
    normalized = {
        "type": str(item.get("type") or "review"),
        "title": title or "复习任务",
        "reason": str(item.get("reason") or ""),
        "estimated_minutes": estimated_minutes,
        "source_ids": source_ids,
    }
    if source_load_units > 0:
        normalized["load_units"] = source_load_units
    if source_question_count > 0:
        normalized["question_count"] = source_question_count
    if candidate:
        for key in (
            "load_units",
            "parent_practice_set_id",
            "parent_source_id",
            "plan_segment_id",
            "part_index",
            "part_count",
            "planned_question_ids",
            "question_count",
            "question_type_mix",
            "state_mix",
            "difficulty_mix",
        ):
            if key in candidate and key not in normalized:
                normalized[key] = candidate[key]
    elif item.get("load_units") is not None:
        normalized["load_units"] = item.get("load_units")
    return normalized


def _normalize_plan_day_items(
    days: list[dict[str, Any]],
    *,
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    title_lookup = _context_title_lookup(context)
    candidate_lookup = _context_candidate_lookup(context)
    normalized_days: list[dict[str, Any]] = []
    for day in days:
        if not isinstance(day, dict):
            continue
        items = day.get("items") if isinstance(day.get("items"), list) else []
        normalized_days.append(
            {
                **day,
                "items": [
                    _normalize_plan_item(
                        item,
                        title_lookup=title_lookup,
                        candidate_lookup=candidate_lookup,
                    )
                    for item in items
                    if isinstance(item, dict)
                ],
            }
        )
    return normalized_days


def _merge_plan_day_items_by_family(days: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged_days: list[dict[str, Any]] = []
    for day in days:
        if not isinstance(day, dict):
            continue
        merged_items: list[dict[str, Any]] = []
        family_index: dict[str, int] = {}
        items = day.get("items") if isinstance(day.get("items"), list) else []
        for item in items:
            if not isinstance(item, dict):
                continue
            family = _plan_item_merge_family(item)
            if not family:
                merged_items.append(item)
                continue
            if family in family_index:
                existing_index = family_index[family]
                merged_items[existing_index] = _merge_plan_items(merged_items[existing_index], item, family)
            else:
                family_index[family] = len(merged_items)
                merged_items.append(_normalize_merged_plan_item(item, family))
        merged_days.append({**day, "items": merged_items})
    return merged_days


def _plan_item_merge_family(item: dict[str, Any]) -> str:
    candidate_type = _plan_item_candidate_type(str(item.get("type") or ""))
    family = MERGEABLE_PLAN_ITEM_FAMILY_BY_CANDIDATE_TYPE.get(candidate_type, "")
    source_ids = [str(value).strip() for value in item.get("source_ids") or [] if str(value).strip()]
    return family if family and source_ids else ""


def _normalize_merged_plan_item(item: dict[str, Any], family: str) -> dict[str, Any]:
    normalized = dict(item)
    normalized["type"] = str(item.get("type") or MERGED_PLAN_ITEM_TYPE_BY_FAMILY.get(family, "review"))
    normalized["title"] = _merged_plan_item_title(family, _plan_item_question_count(normalized))
    return normalized


def _merge_plan_items(left: dict[str, Any], right: dict[str, Any], family: str) -> dict[str, Any]:
    source_ids = _unique_plan_values(list(left.get("source_ids") or []) + list(right.get("source_ids") or []))
    planned_question_ids = _unique_plan_values(
        list(left.get("planned_question_ids") or []) + list(right.get("planned_question_ids") or [])
    )
    question_count = _plan_item_question_count(left) + _plan_item_question_count(right)
    merged = {
        **left,
        "type": str(left.get("type") or MERGED_PLAN_ITEM_TYPE_BY_FAMILY.get(family, "review")),
        "source_ids": source_ids,
        "estimated_minutes": _plan_item_estimated_minutes(left) + _plan_item_estimated_minutes(right),
        "question_count": question_count,
        "title": _merged_plan_item_title(family, question_count),
        "reason": _merged_plan_item_reason(family),
    }
    load_units = _plan_item_load_units_value(left) + _plan_item_load_units_value(right)
    if load_units > 0:
        merged["load_units"] = round(load_units, 2)
    if planned_question_ids:
        merged["planned_question_ids"] = planned_question_ids
    for key in ("question_type_mix", "state_mix", "difficulty_mix"):
        merged_mix = _merge_plan_count_maps(left.get(key), right.get(key))
        if merged_mix:
            merged[key] = merged_mix
    return merged


def _merged_plan_item_title(family: str, question_count: int) -> str:
    label = MERGED_PLAN_ITEM_LABEL_BY_FAMILY.get(family, "复习任务")
    count = max(1, int(question_count or 0))
    return f"{label} {count} 道题"


def _merged_plan_item_reason(family: str) -> str:
    label = MERGED_PLAN_ITEM_LABEL_BY_FAMILY.get(family, "同类任务")
    return f"同一天的{label}已合并，按预计分钟一起完成。"


def _plan_item_question_count(item: dict[str, Any]) -> int:
    parsed = _safe_int(item.get("question_count"), 0, minimum=0, maximum=9999)
    if parsed > 0:
        return parsed
    planned_question_ids = item.get("planned_question_ids") if isinstance(item.get("planned_question_ids"), list) else []
    if planned_question_ids:
        return len(planned_question_ids)
    source_ids = item.get("source_ids") if isinstance(item.get("source_ids"), list) else []
    return len(source_ids)


def _plan_item_estimated_minutes(item: dict[str, Any]) -> int:
    return _safe_int(item.get("estimated_minutes") or item.get("minutes"), 0, minimum=0, maximum=24 * 60)


def _plan_item_load_units_value(item: dict[str, Any]) -> float:
    try:
        parsed = float(item.get("load_units") or 0)
    except (TypeError, ValueError):
        parsed = 0.0
    return max(0.0, parsed)


def _merge_plan_count_maps(left: Any, right: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in (left, right):
        if not isinstance(value, dict):
            continue
        for key, count in value.items():
            try:
                parsed = int(count)
            except (TypeError, ValueError):
                parsed = 0
            if parsed > 0:
                safe_key = str(key)
                counts[safe_key] = counts.get(safe_key, 0) + parsed
    return counts


def _unique_plan_values(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        unique.append(text)
    return unique


def _first_candidate_for_source_ids(
    source_ids: list[str],
    candidate_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    for source_id in source_ids:
        candidate = candidate_lookup.get(source_id)
        if isinstance(candidate, dict):
            return candidate
    return None


def _plan_item_has_valid_sources(
    item: dict[str, Any],
    *,
    context: dict[str, Any],
    valid_source_ids: set[str],
) -> bool:
    candidate_type = _plan_item_candidate_type(str(item.get("type") or ""))
    if not candidate_type:
        return str(item.get("type") or "") in {"maintain", "review"}

    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    enabled_types = set(str(value) for value in policy.get("enabled_types") or [])
    if enabled_types and candidate_type not in enabled_types:
        return False

    source_ids = [str(value).strip() for value in item.get("source_ids") or [] if str(value).strip()]
    if candidate_type in _source_required_candidate_types():
        return bool(source_ids) and all(source_id in valid_source_ids for source_id in source_ids)
    return all(source_id in valid_source_ids for source_id in source_ids)


def _source_required_candidate_types() -> set[str]:
    return {
        "weak_topics",
        "wrong_questions",
        "pending_review_items",
        "review_tasks",
        "draft_attempts",
        "unstarted_questions",
        "startup_candidates",
        "favorite_unmastered",
    }


def _plan_item_candidate_type(item_type: str) -> str:
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
    if item_type in _source_required_candidate_types():
        return item_type
    return mapping.get(item_type, "")


def _context_source_id_set(context: dict[str, Any]) -> set[str]:
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    source_ids: set[str] = set()
    for values in candidates.values():
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
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
                value = str(item.get(key) or "").strip()
                if value:
                    source_ids.add(value)
    return source_ids


def _context_candidate_lookup(context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    lookup: dict[str, dict[str, Any]] = {}
    for values in candidates.values():
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
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
                identifier = str(item.get(key) or "").strip()
                if identifier and identifier not in lookup:
                    lookup[identifier] = item
    return lookup


def _context_title_lookup(context: dict[str, Any]) -> dict[str, str]:
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    lookup: dict[str, str] = {}
    for value in candidates.values():
        if not isinstance(value, list):
            continue
        for item in value:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or item.get("question_title") or item.get("name") or "").strip()
            if not title:
                title = str(item.get("topic") or "").strip()
            if not title:
                continue
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
                identifier = str(item.get(key) or "").strip()
                if identifier:
                    lookup[identifier] = title
    return lookup


def _repair_title_from_sources(title: str, source_ids: list[str], title_lookup: dict[str, str]) -> str:
    stripped = title.strip()
    if not _title_needs_repair(stripped):
        return stripped
    repaired = [title_lookup[source_id] for source_id in source_ids if source_id in title_lookup]
    if not repaired:
        return stripped
    if len(repaired) == 1:
        return repaired[0]
    return "、".join(repaired[:3])


def _title_needs_repair(title: str) -> bool:
    if not title:
        return True
    question_marks = title.count("?")
    return "??" in title or question_marks >= max(2, len(title) // 4)


def _fallback_review_plan_draft(
    *,
    context: dict[str, Any],
    model: str,
    warning: str,
) -> dict[str, Any]:
    constraints = context.get("constraints") if isinstance(context.get("constraints"), dict) else {}
    days_count = _safe_int(constraints.get("days"), 7, minimum=1, maximum=30)
    daily_minutes = _safe_int(constraints.get("daily_minutes"), 60, minimum=15, maximum=240)
    candidates = context.get("ai_candidates") if isinstance(context.get("ai_candidates"), dict) else {}
    policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
    mode = str(policy.get("mode") or constraints.get("mode") or "balanced")
    weak_topics = candidates.get("weak_topics") if isinstance(candidates.get("weak_topics"), list) else []
    wrong_questions = candidates.get("wrong_questions") if isinstance(candidates.get("wrong_questions"), list) else []
    pending_items = candidates.get("pending_review_items") if isinstance(candidates.get("pending_review_items"), list) else []
    review_tasks = candidates.get("review_tasks") if isinstance(candidates.get("review_tasks"), list) else []
    drafts = candidates.get("draft_attempts") if isinstance(candidates.get("draft_attempts"), list) else []
    startup_candidates = (
        candidates.get("startup_candidates") if isinstance(candidates.get("startup_candidates"), list) else []
    )
    unstarted_questions = (
        candidates.get("unstarted_questions") if isinstance(candidates.get("unstarted_questions"), list) else []
    )

    start_date = datetime.now(timezone.utc).date()
    days: list[dict[str, Any]] = []
    for index in range(days_count):
        items: list[dict[str, Any]] = []
        should_use_startup_candidates = mode == "startup" or (
            mode == "balanced"
            and not (review_tasks or pending_items or weak_topics or wrong_questions or drafts)
        )
        if should_use_startup_candidates and (startup_candidates or unstarted_questions):
            startup_slice = (startup_candidates or unstarted_questions)[index * 3 : index * 3 + 3]
            if not startup_slice and index == 0:
                startup_slice = (startup_candidates or unstarted_questions)[:3]
            source_ids = [_candidate_source_id(item, "question_id") for item in startup_slice]
            source_ids = [source_id for source_id in source_ids if source_id]
            if source_ids:
                startup_reason = (
                    "当前模式是新题启动，优先安排未开始或起步候选题。"
                    if mode == "startup"
                    else "当前没有更高优先级的错题或到期任务，先用起步候选题建立练习记录。"
                )
                items.append(
                    {
                        "type": "startup_question",
                        "title": f"启动 {len(source_ids)} 道新题",
                        "reason": startup_reason,
                        "estimated_minutes": min(daily_minutes, max(15, len(source_ids) * 10)),
                        "source_ids": source_ids,
                    }
                )
        if index == 0 and review_tasks:
            due_ids = [_candidate_source_id(item, "task_id") for item in review_tasks[:3]]
            due_ids = [source_id for source_id in due_ids if source_id]
            items.append(
                {
                    "type": "review_due",
                    "title": f"处理 {len(due_ids) or min(len(review_tasks), 3)} 个到期复习任务",
                    "reason": "到期和逾期任务应先完成，避免复习计划继续堆积。",
                    "estimated_minutes": min(daily_minutes, 20 + 10 * max(len(due_ids), 1)),
                    "source_ids": due_ids,
                }
            )
        if index == 0 and pending_items:
            pending_ids = [_candidate_source_id(item, "question_id") for item in pending_items[:5]]
            pending_ids = [source_id for source_id in pending_ids if source_id]
            items.append(
                {
                    "type": "pending_review",
                    "title": f"确认 {len(pending_ids) or min(len(pending_items), 5)} 道待核对题",
                    "reason": "待核对题会影响薄弱知识点判断，应先用 AI 或人工确认。",
                    "estimated_minutes": min(30, max(10, 5 * max(len(pending_ids), 1))),
                    "source_ids": pending_ids,
                }
            )
        topic = weak_topics[index % len(weak_topics)] if weak_topics else {}
        if isinstance(topic, dict) and topic:
            topic_name = str(topic.get("topic") or topic.get("title") or "薄弱知识点")
            topic_source_id = _candidate_source_id(topic, "topic", "title")
            items.append(
                {
                    "type": "topic_review",
                    "title": f"复习 {topic_name}",
                    "reason": str(topic.get("primary_reason") or "该知识点优先级较高。"),
                    "estimated_minutes": min(35, max(15, daily_minutes // 2)),
                    "source_ids": [topic_source_id] if topic_source_id else [],
                }
            )
        wrong_slice = wrong_questions[index * 3 : index * 3 + 3]
        if wrong_slice:
            source_ids = [_candidate_source_id(item, "question_id") for item in wrong_slice]
            source_ids = [source_id for source_id in source_ids if source_id]
            items.append(
                {
                    "type": "wrong_pool",
                    "title": f"复习 {len(source_ids)} 道错题",
                    "reason": "这些题近期风险较高，适合组成小练习单。",
                    "estimated_minutes": min(35, max(15, len(source_ids) * 8)),
                    "source_ids": source_ids,
                }
            )
        if index == 0 and drafts:
            draft_slice = [item for item in drafts[:3] if isinstance(item, dict)]
            for draft in draft_slice:
                draft_item = _build_top_up_plan_item("draft_attempts", [draft])
                if not draft_item.get("source_ids"):
                    continue
                draft_item["reason"] = "未提交练习已经占用题目池，先收尾能减少遗留记录。"
                items.append(draft_item)
        if not items:
            items.append(
                {
                    "type": "maintain",
                    "title": "保持基础练习",
                    "reason": "当前数据不足以生成强优先级任务，先维持低负担复习。",
                    "estimated_minutes": min(daily_minutes, 20),
                    "source_ids": [],
                }
            )
        days.append(
            {
                "date": (start_date + timedelta(days=index)).isoformat(),
                "items": items,
            }
        )
    planned_days = _rebalance_plan_days_by_load(days, context=context)
    planned_days = _top_up_underfilled_plan_days(planned_days, context=context)
    planned_days = _normalize_plan_day_items(planned_days, context=context)
    planned_days = _merge_plan_day_items_by_family(planned_days)
    warnings = [warning] if warning else []
    return {
        "plan_id": f"fallback_plan_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "model": model,
        "days": planned_days,
        "warnings": warnings,
        "source": "fallback",
        "writes_review_tasks": False,
    }


def _candidate_source_id(item: dict[str, Any], *preferred_keys: str) -> str:
    for key in (
        "source_id",
        *preferred_keys,
        "candidate_id",
        "plan_segment_id",
        "question_id",
        "task_id",
        "attempt_id",
        "set_id",
        "practice_set_id",
        "topic",
    ):
        value = str(item.get(key) or "").strip()
        if value:
            return value
    return ""


def _safe_int(value: Any, default: int, *, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))
