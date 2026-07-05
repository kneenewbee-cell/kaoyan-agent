from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query, Request

from .security import resolve_user_id
from .system_practice_review import SystemPracticeReviewStore


router = APIRouter(prefix="/api/materials/system", tags=["materials"])


def _resolve_request_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    try:
        return resolve_user_id(explicit_user_id or request.headers.get("X-User-Id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _store() -> SystemPracticeReviewStore:
    return SystemPracticeReviewStore()


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
