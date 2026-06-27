from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.concurrency import run_in_threadpool

from .security import resolve_material_id
from .service import MaterialIngestionService
from .storage import MaterialStorage
from .tools import get_current_user_id, search_user_materials_tool
from .upload_jobs import UPLOAD_JOBS

router = APIRouter(prefix="/api/materials", tags=["materials"])
ROOT = Path(__file__).resolve().parents[1]
UPLOAD_JOB_DIR = ROOT / "data" / "runtime" / "uploads" / "material_jobs"


def _resolve_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    return get_current_user_id(explicit_user_id or request.headers.get("X-User-Id"))


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


def _run_upload_job(
    *,
    job_id: str,
    temp_dir: Path,
    temp_path: Path,
    user_id: str,
    subject: str,
    material_type: str,
    use_llm_cleanup: bool,
    enable_vector_index: bool,
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
            use_llm_cleanup=use_llm_cleanup,
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
    material_type: str = Form("unknown"),
    use_llm_cleanup: bool = Form(True),
    enable_vector_index: bool = Form(True),
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
                enable_vector_index=enable_vector_index,
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
            use_llm_cleanup=use_llm_cleanup,
            enable_vector_index=enable_vector_index,
        )
    finally:
        if not async_upload:
            shutil.rmtree(temp_dir, ignore_errors=True)

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
    subject: str | None = Query(None),
    material_type: str | None = Query(None),
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
    mode: str = Query("hybrid", pattern="^(keyword|vector|hybrid)$"),
    material_id: str | None = Query(None),
    subject: str | None = Query(None),
    material_type: str | None = Query(None),
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
