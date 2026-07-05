from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse

from .security import resolve_material_id
from .service import MaterialIngestionService
from .storage import MaterialStorage
from .system_library import SystemQuestionLibrary
from .tools import get_current_user_id, search_user_materials_tool
from .user_state import UserSystemQuestionStateStore
from .upload_jobs import UPLOAD_JOBS

router = APIRouter(prefix="/api/materials", tags=["materials"])
ROOT = Path(__file__).resolve().parents[1]
UPLOAD_JOB_DIR = ROOT / "data" / "runtime" / "uploads" / "material_jobs"
SYSTEM_ASSET_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
ACTIVE_MATERIAL_TYPE_PATTERN = "^(textbook|lecture|exercise)$"
UPLOAD_MATERIAL_TYPE_PATTERN = "^(auto|unknown|textbook|lecture|exercise)$"


def _resolve_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    try:
        return get_current_user_id(explicit_user_id or request.headers.get("X-User-Id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _result_payload(result) -> dict[str, Any]:
    return {
        "ok": result.error is None,
        "material_id": result.material_id,
        "user_id": result.user_id,
        "parse_status": result.parse_status.value,
        "manifest_path": result.manifest_path,
        "markdown_path": result.markdown_path,
        "chunk_count": result.chunk_count,
        "quality_status": result.quality_status,
        "warnings": result.warnings,
        "metadata": result.metadata,
        "error": result.error,
    }


def _parse_optional_json_object(raw_value: str | None, field_name: str) -> dict[str, Any] | None:
    if raw_value in (None, ""):
        return None
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"{field_name} must be valid JSON") from exc
    if not isinstance(value, dict):
        raise HTTPException(status_code=400, detail=f"{field_name} must be a JSON object")
    return value


def _with_system_question_states(response: dict[str, Any], user_id: str) -> dict[str, Any]:
    payload = dict(response)
    items = [dict(item) for item in payload.get("items") or []]
    question_ids = [str(item.get("question_id") or "") for item in items if item.get("question_id")]
    states = UserSystemQuestionStateStore().list_question_states(user_id, question_ids)
    for item in items:
        question_id = str(item.get("question_id") or "")
        if question_id in states:
            item["personal_state"] = states[question_id]
    payload["items"] = items
    payload["user_id"] = user_id
    return payload


def _with_system_question_state(detail: dict[str, Any], user_id: str) -> dict[str, Any]:
    payload = dict(detail)
    question_id = str(payload.get("question_id") or "")
    if question_id:
        payload["personal_state"] = UserSystemQuestionStateStore().get_question_state(user_id, question_id)
    payload["user_id"] = user_id
    return payload


def _matches_system_user_status(state: dict[str, Any], user_status: str) -> bool:
    if user_status in {"not_started", "learning", "mastered"}:
        return state.get("mastery_status") == user_status
    if user_status == "favorite":
        return bool(state.get("is_favorite"))
    if user_status == "wrong_book":
        return bool(state.get("in_wrong_book"))
    if user_status == "noted":
        return bool(str(state.get("personal_note") or "").strip())
    return True


def _collect_system_question_items(
    library: SystemQuestionLibrary,
    *,
    subject: str,
    exam_type: str,
    library_name: str | None = None,
    year: int | None = None,
    question_type: str | None = None,
    topic: str | None = None,
    query: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    return library.list_all_questions(
        subject=subject,
        exam_type=exam_type,
        library_name=library_name,
        year=year,
        question_type=question_type,
        topic=topic,
        query=query,
    )


def _summarize_system_question_states(items: list[dict[str, Any]], user_id: str) -> dict[str, int]:
    summary = {
        "all": 0,
        "not_started": 0,
        "learning": 0,
        "mastered": 0,
        "favorite": 0,
        "wrong_book": 0,
        "noted": 0,
    }
    question_ids = [str(item.get("question_id") or "") for item in items if item.get("question_id")]
    states = UserSystemQuestionStateStore().list_question_states(user_id, question_ids)
    for item in items:
        question_id = str(item.get("question_id") or "")
        state = states.get(question_id) or {}
        mastery_status = str(state.get("mastery_status") or "not_started")
        summary["all"] += 1
        if mastery_status in {"not_started", "learning", "mastered"}:
            summary[mastery_status] += 1
        else:
            summary["not_started"] += 1
        if bool(state.get("is_favorite")):
            summary["favorite"] += 1
        if bool(state.get("in_wrong_book")):
            summary["wrong_book"] += 1
        if str(state.get("personal_note") or "").strip():
            summary["noted"] += 1
    return summary


def _paginate_system_response(
    response: dict[str, Any],
    *,
    items: list[dict[str, Any]],
    page: int,
    page_size: int,
    user_id: str,
) -> dict[str, Any]:
    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    start = (page - 1) * page_size
    payload = dict(response)
    payload["items"] = items[start : start + page_size]
    payload["total"] = total
    payload["page"] = page
    payload["page_size"] = page_size
    payload["total_pages"] = total_pages
    payload["user_id"] = user_id
    return payload


def _metadata_payload(
    *,
    allow_metadata_mismatch: bool,
    use_llm_formula_cleanup: bool = False,
    llm_formula_min_confidence: float = 0.8,
    cleaning_strategy_override: dict[str, Any] | None = None,
    document_zones_override: dict[str, Any] | None = None,
    metadata_profile_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "allow_metadata_mismatch": allow_metadata_mismatch,
        "use_llm_formula_cleanup": use_llm_formula_cleanup,
        "llm_formula_min_confidence": llm_formula_min_confidence,
    }
    if cleaning_strategy_override is not None:
        payload["cleaning_strategy_override"] = cleaning_strategy_override
    if document_zones_override is not None:
        payload["document_zones_override"] = document_zones_override
    if metadata_profile_override is not None:
        payload["metadata_profile_override"] = metadata_profile_override
    return payload


def _run_upload_job(
    *,
    job_id: str,
    temp_dir: Path,
    temp_path: Path,
    user_id: str,
    subject: str,
    material_type: str,
    use_llm_cleanup: bool,
    use_formula_cleanup: bool,
    formula_cleanup_level: str,
    use_llm_formula_cleanup: bool,
    llm_formula_min_confidence: float,
    enable_vector_index: bool,
    allow_metadata_mismatch: bool,
    metadata_overrides: dict[str, Any] | None = None,
) -> None:
    def on_progress(event: dict[str, Any]) -> None:
        UPLOAD_JOBS.apply_pipeline_event(job_id, event)

    try:
        UPLOAD_JOBS.update(
            job_id,
            status="processing",
            stage="ingest",
            message="正在准备入库",
            progress=5,
        )
        result = MaterialIngestionService().ingest_file(
            file_path=temp_path,
            user_id=user_id,
            subject=subject,
            material_type=material_type,
            metadata={
                **(metadata_overrides or {}),
                "allow_metadata_mismatch": allow_metadata_mismatch,
                "use_llm_formula_cleanup": use_llm_formula_cleanup,
                "llm_formula_min_confidence": llm_formula_min_confidence,
            },
            use_llm_cleanup=use_llm_cleanup,
            use_formula_cleanup=use_formula_cleanup,
            formula_cleanup_level=formula_cleanup_level,
            enable_vector_index=enable_vector_index,
            progress_callback=on_progress,
        )
        payload = _result_payload(result)
        if result.error:
            UPLOAD_JOBS.update(
                job_id,
                status="failed",
                stage="ingest",
                message=f"入库失败：{result.error}",
                error=result.error,
                result=payload,
            )
        else:
            UPLOAD_JOBS.update(
                job_id,
                status="completed",
                stage="ingest",
                message="入库完成",
                progress=100,
                material_id=result.material_id,
                result=payload,
            )
    except Exception as exc:
        UPLOAD_JOBS.update(
            job_id,
            status="failed",
            stage="ingest",
            message=f"入库失败：{exc}",
            error=str(exc),
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/upload")
async def upload_material(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str | None = Form(None),
    subject: str = Form("unknown"),
    material_type: str = Form("unknown", pattern=UPLOAD_MATERIAL_TYPE_PATTERN),
    use_llm_cleanup: bool = Form(True),
    use_formula_cleanup: bool = Form(True),
    formula_cleanup_level: str = Form("safe"),
    use_llm_formula_cleanup: bool = Form(False),
    llm_formula_min_confidence: float = Form(0.8),
    enable_vector_index: bool = Form(True),
    allow_metadata_mismatch: bool = Form(False),
    cleaning_strategy_override: str | None = Form(None),
    document_zones_override: str | None = Form(None),
    metadata_profile_override: str | None = Form(None),
    async_upload: bool = Form(False),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    filename = Path(file.filename).name
    temp_root = UPLOAD_JOB_DIR if async_upload else Path(tempfile.gettempdir())
    temp_root.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix="materials_upload_", dir=str(temp_root)))
    temp_path = temp_dir / filename
    metadata_overrides = _metadata_payload(
        allow_metadata_mismatch=allow_metadata_mismatch,
        use_llm_formula_cleanup=use_llm_formula_cleanup,
        llm_formula_min_confidence=llm_formula_min_confidence,
        cleaning_strategy_override=_parse_optional_json_object(cleaning_strategy_override, "cleaning_strategy_override"),
        document_zones_override=_parse_optional_json_object(document_zones_override, "document_zones_override"),
        metadata_profile_override=_parse_optional_json_object(metadata_profile_override, "metadata_profile_override"),
    )
    try:
        with temp_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)
        if async_upload:
            job = UPLOAD_JOBS.create(filename=filename, user_id=uid)
            background_tasks.add_task(
                _run_upload_job,
                job_id=job["job_id"],
                temp_dir=temp_dir,
                temp_path=temp_path,
                user_id=uid,
                subject=subject,
                material_type=material_type,
                use_llm_cleanup=use_llm_cleanup,
                use_formula_cleanup=use_formula_cleanup,
                formula_cleanup_level=formula_cleanup_level,
                use_llm_formula_cleanup=use_llm_formula_cleanup,
                llm_formula_min_confidence=llm_formula_min_confidence,
                enable_vector_index=enable_vector_index,
                allow_metadata_mismatch=allow_metadata_mismatch,
                metadata_overrides=metadata_overrides,
            )
            return {
                "ok": True,
                "async": True,
                "job_id": job["job_id"],
                "status": job["status"],
                "stage": job["stage"],
                "message": job["message"],
                "progress": job["progress"],
                "error": None,
            }

        result = await run_in_threadpool(
            MaterialIngestionService().ingest_file,
            file_path=temp_path,
            user_id=uid,
            subject=subject,
            material_type=material_type,
            metadata=metadata_overrides,
            use_llm_cleanup=use_llm_cleanup,
            use_formula_cleanup=use_formula_cleanup,
            formula_cleanup_level=formula_cleanup_level,
            enable_vector_index=enable_vector_index,
        )
    finally:
        if not async_upload:
            shutil.rmtree(temp_dir, ignore_errors=True)

    if result.error in {"metadata_conflict", "metadata_detection_required"}:
        return _result_payload(result)
    if result.error:
        raise HTTPException(status_code=400, detail=result.error)

    return _result_payload(result)


@router.get("/upload-jobs/{job_id}")
async def get_upload_job(job_id: str) -> dict[str, Any]:
    job = UPLOAD_JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Upload job not found")
    return {"ok": True, "job": job}


@router.get("/list")
async def list_materials(
    request: Request,
    user_id: str | None = Query(None),
    subject: str = Query(..., pattern="^(math|politics|english|408|other)$"),
    material_type: str | None = Query(None, pattern=ACTIVE_MATERIAL_TYPE_PATTERN),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    filters = {
        key: value
        for key, value in {"subject": subject, "material_type": material_type}.items()
        if value
    }
    items = MaterialIngestionService().list_materials(uid, filters=filters or None)
    return {"ok": True, "user_id": uid, "items": items}


@router.get("/search")
async def search_materials(
    request: Request,
    query: str = Query(..., min_length=1),
    user_id: str | None = Query(None),
    top_k: int = Query(5, ge=1, le=50),
    mode: str = Query("hybrid", pattern="^(keyword|vector|hybrid|llm|hybrid_llm)$"),
    material_id: str | None = Query(None),
    subject: str | None = Query(None, pattern="^(math|politics|english|408|other)$"),
    material_type: str | None = Query(None, pattern=ACTIVE_MATERIAL_TYPE_PATTERN),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    filters = {
        key: value
        for key, value in {
            "material_id": material_id,
            "subject": subject,
            "material_type": material_type,
        }.items()
        if value
    }
    results = search_user_materials_tool(uid, query, top_k=top_k, filters=filters or None, mode=mode)
    return {
        "ok": True,
        "user_id": uid,
        "query": query,
        "mode": mode,
        "total_results": len(results),
        "results": results,
    }


@router.get("/system/questions")
async def list_system_questions(
    request: Request,
    user_id: str | None = Query(None),
    subject: str = Query("math", pattern="^(math|politics|english|408|other)$"),
    exam_type: str = Query("math1"),
    library_name: str | None = Query(None),
    year: int | None = Query(None),
    question_type: str | None = Query(None),
    topic: str | None = Query(None),
    query: str | None = Query(None),
    user_status: str | None = Query(None, pattern="^(not_started|learning|mastered|favorite|wrong_book|noted)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    library = SystemQuestionLibrary()
    if user_status:
        base_response, all_items = _collect_system_question_items(
            library,
            subject=subject,
            exam_type=exam_type,
            library_name=library_name,
            year=year,
            question_type=question_type,
            topic=topic,
            query=query,
        )
        question_ids = [str(item.get("question_id") or "") for item in all_items if item.get("question_id")]
        states = UserSystemQuestionStateStore().list_question_states(uid, question_ids)
        filtered_items = []
        for item in all_items:
            question_id = str(item.get("question_id") or "")
            state = states.get(question_id)
            if not state or not _matches_system_user_status(state, user_status):
                continue
            item["personal_state"] = state
            filtered_items.append(item)
        return _paginate_system_response(
            base_response,
            items=filtered_items,
            page=page,
            page_size=page_size,
            user_id=uid,
        )

    response = library.list_questions(
        subject=subject,
        exam_type=exam_type,
        library_name=library_name,
        year=year,
        question_type=question_type,
        topic=topic,
        query=query,
        page=page,
        page_size=page_size,
    )
    return _with_system_question_states(response, uid)


@router.get("/system/questions/state-summary")
async def summarize_system_question_states(
    request: Request,
    user_id: str | None = Query(None),
    subject: str = Query("math", pattern="^(math|politics|english|408|other)$"),
    exam_type: str = Query("math1"),
    library_name: str | None = Query(None),
    year: int | None = Query(None),
    question_type: str | None = Query(None),
    topic: str | None = Query(None),
    query: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    base_response, all_items = _collect_system_question_items(
        SystemQuestionLibrary(),
        subject=subject,
        exam_type=exam_type,
        library_name=library_name,
        year=year,
        question_type=question_type,
        topic=topic,
        query=query,
    )
    return {
        "ok": True,
        "user_id": uid,
        "subject": subject,
        "exam_type": exam_type,
        "total": len(all_items),
        "topic_options": base_response.get("topic_options") or [],
        "state_summary": _summarize_system_question_states(all_items, uid),
    }


@router.get("/system/questions/{question_id}")
async def get_system_question(
    question_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    try:
        detail = SystemQuestionLibrary().get_question(question_id)
    except (FileNotFoundError, KeyError) as exc:
        raise HTTPException(status_code=404, detail="System question not found") from exc
    return _with_system_question_state(detail, uid)


@router.patch("/system/questions/{question_id}/state")
async def update_system_question_state(
    question_id: str,
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    try:
        SystemQuestionLibrary().get_question(question_id)
    except (FileNotFoundError, KeyError) as exc:
        raise HTTPException(status_code=404, detail="System question not found") from exc
    try:
        state = UserSystemQuestionStateStore().update_question_state(uid, question_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "ok": True,
        "user_id": uid,
        "question_id": question_id,
        "personal_state": state,
    }


@router.get("/system/assets/{exam_type}/{year}/{asset_path:path}")
async def get_system_asset(exam_type: str, year: int, asset_path: str) -> FileResponse:
    if Path(asset_path).suffix.lower() not in SYSTEM_ASSET_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="System asset must be an image file")
    try:
        path = SystemQuestionLibrary().asset_path(exam_type, year, asset_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="System asset not found") from exc
    return FileResponse(path)


@router.delete("/{material_id}")
async def delete_material(
    material_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    safe_material_id = resolve_material_id(material_id)
    try:
        return MaterialIngestionService().delete_material(uid, safe_material_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to delete material: {exc}") from exc


@router.get("/{material_id}")
async def get_material_status(
    material_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    safe_material_id = resolve_material_id(material_id)
    manifest = MaterialStorage().load_manifest(uid, safe_material_id)
    if manifest is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return manifest.to_dict()
