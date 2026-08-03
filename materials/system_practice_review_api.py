from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query, Request

from .security import resolve_user_id
from .system_ai_planner import (
    DEFAULT_AI_REVIEW_PLAN_MODEL,
    build_blocked_ai_review_plan_draft,
    generate_ai_review_plan_draft,
)
from .system_practice_review import SystemPracticeReviewStore


router = APIRouter(prefix="/api/materials/system", tags=["materials"])


def _resolve_request_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    try:
        return resolve_user_id(explicit_user_id or request.headers.get("X-User-Id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _store() -> SystemPracticeReviewStore:
    return SystemPracticeReviewStore()


def _parse_include_types(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_values = value.split(",")
    elif isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        raw_values = [value]
    parsed: list[str] = []
    seen: set[str] = set()
    for raw_value in raw_values:
        item = str(raw_value or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        parsed.append(item)
    return parsed


def _ai_review_plan_commit_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    body = payload if isinstance(payload, dict) else {}
    items: list[dict[str, Any]] = []
    raw_items = body.get("items")
    if isinstance(raw_items, list):
        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                continue
            copied = dict(item)
            copied.setdefault("_commit_key", str(index))
            items.append(copied)
    else:
        draft = body.get("draft") if isinstance(body.get("draft"), dict) else {}
        days = draft.get("days") if isinstance(draft.get("days"), list) else []
        for day_index, day in enumerate(days):
            if not isinstance(day, dict):
                continue
            day_items = day.get("items") if isinstance(day.get("items"), list) else []
            for item_index, item in enumerate(day_items):
                if not isinstance(item, dict):
                    continue
                copied = dict(item)
                copied.setdefault("date", day.get("date") or day.get("label"))
                copied["_commit_key"] = f"{day_index}:{item_index}"
                items.append(copied)
    selected_keys = body.get("selected_item_keys")
    if isinstance(selected_keys, list):
        selected = {str(value) for value in selected_keys}
        items = [item for item in items if str(item.get("_commit_key")) in selected]
    return items


@router.post("/practice-sets")
async def create_practice_set(
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_set = _store().create_practice_set(
            uid,
            source_question_id=str(payload.get("source_question_id") or ""),
            count=payload.get("count", 5),
            same_type_only=bool(payload.get("same_type_only", False)),
            exclude_mastered=bool(payload.get("exclude_mastered", True)),
            topic_filters=payload.get("topic_filters"),
            source_scope=str(payload.get("source_scope") or "exam_type"),
            title=payload.get("title"),
            subject=str(payload.get("subject") or "math"),
            exam_type=str(payload.get("exam_type") or "math1"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_set": practice_set}


@router.post("/practice-sets/from-wrong-pool")
async def create_practice_set_from_wrong_pool(
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_set = _store().create_practice_set_from_wrong_pool(
            uid,
            question_ids=payload.get("question_ids") or [],
            title=payload.get("title"),
            subject=str(payload.get("subject") or "math"),
            exam_type=str(payload.get("exam_type") or ""),
            filters=payload.get("filters") if isinstance(payload.get("filters"), dict) else {},
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_set": practice_set}


@router.post("/practice-sets/from-question-ids")
async def create_practice_set_from_question_ids(
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_set = _store().create_practice_set_from_question_ids(
            uid,
            question_ids=payload.get("question_ids") or [],
            title=payload.get("title"),
            subject=str(payload.get("subject") or "math"),
            exam_type=str(payload.get("exam_type") or ""),
            source_type=str(payload.get("source_type") or "question_selection"),
            filters=payload.get("filters") if isinstance(payload.get("filters"), dict) else {},
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_set": practice_set}


@router.post("/practice-candidates")
async def preview_practice_candidates(
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        preview = _store().preview_practice_candidates(
            uid,
            source_question_id=str(payload.get("source_question_id") or ""),
            count=payload.get("count", 5),
            same_type_only=bool(payload.get("same_type_only", False)),
            exclude_mastered=bool(payload.get("exclude_mastered", True)),
            topic_filters=payload.get("topic_filters"),
            source_scope=str(payload.get("source_scope") or "exam_type"),
            subject=str(payload.get("subject") or "math"),
            exam_type=str(payload.get("exam_type") or "math1"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, **preview}


@router.get("/wrong-question-pool")
async def list_wrong_question_pool(
    request: Request,
    user_id: str | None = Query(None),
    subject: str = Query("math"),
    exam_type: str = Query(""),
    topic: str | None = Query(None),
    question_type: str | None = Query(None),
    risk_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        pool = _store().list_wrong_question_pool(
            uid,
            subject=subject,
            exam_type=exam_type,
            topic=topic,
            question_type=question_type,
            risk_type=risk_type,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "pool": pool}


@router.get("/pending-review-items")
async def list_pending_review_items(
    request: Request,
    user_id: str | None = Query(None),
    subject: str = Query("math"),
    exam_type: str = Query(""),
    topic: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        pending_review = _store().list_pending_review_items(
            uid,
            subject=subject,
            exam_type=exam_type,
            topic=topic,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "pending_review": pending_review}


@router.get("/practice-sets")
async def list_practice_sets(
    request: Request,
    user_id: str | None = Query(None),
    status: str | None = Query(None, pattern="^(active|archived)$"),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        items = _store().list_practice_sets(uid, status=status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "total": len(items), "items": items}


@router.get("/practice-sets/{practice_set_id}")
async def get_practice_set(
    practice_set_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_set = _store().get_practice_set(uid, practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_set": practice_set}


@router.delete("/practice-sets/{practice_set_id}")
async def delete_practice_set(
    practice_set_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        deleted = _store().delete_practice_set(uid, practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_set_id": practice_set_id, "deleted": deleted}


@router.post("/practice-sets/{practice_set_id}/attempts")
async def create_practice_attempt(
    practice_set_id: str,
    request: Request,
    payload: dict[str, Any] | None = Body(None),
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_attempt = _store().create_practice_attempt(uid, practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": practice_attempt}


@router.patch("/practice-attempts/{attempt_id}/answers")
async def update_practice_attempt_answers(
    attempt_id: str,
    request: Request,
    payload: dict[str, Any] = Body(...),
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    answers = payload.get("answers") if isinstance(payload, dict) and "answers" in payload else payload
    try:
        practice_attempt = _store().update_practice_attempt_answers(uid, attempt_id, answers)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": practice_attempt}


@router.post("/practice-attempts/{attempt_id}/submit")
async def submit_practice_attempt(
    attempt_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_attempt = _store().submit_practice_attempt(uid, attempt_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": practice_attempt}


@router.post("/practice-attempts/{attempt_id}/items/{question_id}/grade")
async def grade_practice_attempt_item(
    attempt_id: str,
    question_id: str,
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        store = _store()
        judge_method = str(payload.get("judge_method") or "")
        if judge_method == "ai" and not payload.get("final_status"):
            practice_attempt = store.request_practice_item_ai_grade(uid, attempt_id, question_id)
        else:
            practice_attempt = store.apply_practice_item_grade(
                uid,
                attempt_id,
                question_id,
                judge_method=judge_method,
                final_status=str(payload.get("final_status") or ""),
                judge_confidence=payload.get("judge_confidence"),
                judge_reason=payload.get("judge_reason"),
                ai_feedback=payload.get("ai_feedback"),
                manual_override=payload.get("manual_override"),
            )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": practice_attempt}


@router.get("/practice-attempts/{attempt_id}")
async def get_practice_attempt(
    attempt_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        store = _store()
        practice_attempt = store.get_practice_attempt(uid, attempt_id)
        items = store.list_practice_attempt_items(uid, attempt_id=attempt_id)
        insights = store.build_practice_attempt_insights(uid, attempt_id)
        return {
            "ok": True,
            "user_id": uid,
            "practice_attempt": practice_attempt,
            "items": items,
            "summary": practice_attempt.get("summary") or {},
            "question_stats": store.list_user_question_stats(uid),
            "topic_stats": store.list_user_topic_stats(uid),
            "insights": insights,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/questions/{question_id}/learning-snapshot")
async def question_learning_snapshot(
    question_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        snapshot = _store().build_question_learning_snapshot(uid, question_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "snapshot": snapshot}


@router.get("/learning-insights")
async def learning_insights(
    request: Request,
    user_id: str | None = Query(None),
    subject: str | None = Query(None),
    limit: int = Query(5, ge=1, le=10),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        insights = _store().build_learning_insights(uid, subject=subject, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "insights": insights}


@router.get("/ai-planning-context")
async def ai_planning_context(
    request: Request,
    user_id: str | None = Query(None),
    subject: str | None = Query("math"),
    days: int = Query(7, ge=1, le=30),
    daily_minutes: int = Query(60, ge=15, le=240),
    mode: str | None = Query("balanced"),
    include_types: str | None = Query(None),
    goal: str | None = Query("补弱"),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        context = _store().build_ai_planning_context(
            uid,
            subject=subject,
            days=days,
            daily_minutes=daily_minutes,
            goal=goal,
            mode=mode,
            include_types=_parse_include_types(include_types),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "context": context}


@router.post("/ai-review-plan/draft")
async def ai_review_plan_draft(
    request: Request,
    payload: dict[str, Any] | None = Body(None),
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    body = payload or {}
    try:
        context = _store().build_ai_planning_context(
            uid,
            subject=body.get("subject") or "math",
            days=body.get("days") or 7,
            daily_minutes=body.get("daily_minutes") or 60,
            mode=body.get("mode") or "balanced",
            include_types=_parse_include_types(body.get("include_types")),
            goal=body.get("goal") or "补弱",
        )
        model = str(body.get("model") or DEFAULT_AI_REVIEW_PLAN_MODEL).strip() or DEFAULT_AI_REVIEW_PLAN_MODEL
        readiness = context.get("readiness") if isinstance(context.get("readiness"), dict) else {}
        if readiness.get("should_call_llm") is False:
            draft = build_blocked_ai_review_plan_draft(context=context, model=model)
        else:
            draft = generate_ai_review_plan_draft(context=context, model=model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "ok": True,
        "user_id": uid,
        "context": context,
        "draft": draft,
        "writes_review_tasks": False,
    }


@router.post("/ai-review-plan/commit")
async def ai_review_plan_commit(
    request: Request,
    payload: dict[str, Any] | None = Body(None),
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    body = payload or {}
    draft = body.get("draft") if isinstance(body.get("draft"), dict) else {}
    plan_id = body.get("plan_id") or draft.get("plan_id")
    draft_constraints = draft.get("constraints") if isinstance(draft.get("constraints"), dict) else {}
    draft_policy = draft.get("policy") if isinstance(draft.get("policy"), dict) else {}
    plan_mode = body.get("mode") or draft.get("mode") or draft_constraints.get("mode") or draft_policy.get("mode")
    plan_model = body.get("model") or draft.get("model")
    plan_source = body.get("source") or draft.get("source")
    try:
        items = _ai_review_plan_commit_items(body)
        result = _store().create_review_tasks_from_ai_plan(
            uid,
            plan_id=str(plan_id or ""),
            items=items,
            subject=str(body.get("subject") or "math"),
            daily_minutes=body.get("daily_minutes"),
            plan_mode=str(plan_mode or ""),
            plan_model=str(plan_model or ""),
            plan_source=str(plan_source or ""),
            plan_batch_title=str(draft.get("title") or draft.get("summary") or ""),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "result": result}


@router.post("/ai-review-plan/validate")
async def ai_review_plan_validate(
    request: Request,
    payload: dict[str, Any] | None = Body(None),
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    body = payload or {}
    try:
        items = _ai_review_plan_commit_items(body)
        validation = _store().validate_ai_review_plan_items(
            uid,
            items=items,
            daily_minutes=body.get("daily_minutes"),
            subject=str(body.get("subject") or "math"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "validation": validation}


@router.get("/practice-attempts")
async def list_practice_attempts(
    request: Request,
    user_id: str | None = Query(None),
    practice_set_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        practice_attempts = _store().list_practice_attempts(uid, practice_set_id=practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "ok": True,
        "user_id": uid,
        "total": len(practice_attempts),
        "practice_attempts": practice_attempts,
    }


@router.post("/review-tasks")
async def create_review_task(
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        review_task = _store().create_review_task(
            uid,
            target_type=str(payload.get("target_type") or ""),
            target_id=str(payload.get("target_id") or ""),
            title=payload.get("title"),
            due_at=payload.get("due_at"),
            priority=payload.get("priority", 2),
            note=payload.get("note"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (FileNotFoundError, KeyError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "review_task": review_task}


@router.get("/review-tasks")
async def list_review_tasks(
    request: Request,
    user_id: str | None = Query(None),
    status: str | None = Query(None, pattern="^(pending|completed|cancelled)$"),
    subject: str | None = Query(None),
    target_type: str | None = Query(None, pattern="^(question|practice_set|knowledge_point)$"),
    date_group: str | None = Query(None, pattern="^(overdue|today|future|completed|cancelled|unscheduled)$"),
    keyword: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        items = _store().list_review_tasks(
            uid,
            status=status,
            subject=subject,
            target_type=target_type,
            date_group=date_group,
            keyword=keyword,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "total": len(items), "items": items}


@router.get("/review-tasks/summary")
async def review_task_summary(
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    summary = _store().review_task_summary(uid)
    return {"ok": True, "user_id": uid, "summary": summary}


@router.patch("/review-tasks/{review_task_id}")
async def update_review_task(
    review_task_id: str,
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        review_task = _store().update_review_task(uid, review_task_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "review_task": review_task}


@router.delete("/review-tasks/{review_task_id}")
async def delete_review_task(
    review_task_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        deleted = _store().delete_review_task(uid, review_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "review_task_id": review_task_id, "deleted": deleted}
