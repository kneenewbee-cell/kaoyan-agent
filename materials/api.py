from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.concurrency import run_in_threadpool

from .security import resolve_material_id
from .service import MaterialIngestionService
from .storage import MaterialStorage
from .tools import get_current_user_id, search_user_materials_tool

router = APIRouter(prefix="/api/materials", tags=["materials"])


def _resolve_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    return get_current_user_id(explicit_user_id or request.headers.get("X-User-Id"))


@router.post("/upload")
async def upload_material(
    request: Request,
    file: UploadFile = File(...),
    user_id: str | None = Form(None),
    subject: str = Form("unknown"),
    material_type: str = Form("unknown"),
    use_llm_cleanup: bool = Form(True),
) -> dict[str, Any]:
    uid = _resolve_user_id(request, user_id)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    temp_dir = Path(tempfile.mkdtemp(prefix="materials_upload_"))
    temp_path = temp_dir / file.filename
    try:
        with temp_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)
        result = await run_in_threadpool(
            MaterialIngestionService().ingest_file,
            file_path=temp_path,
            user_id=uid,
            subject=subject,
            material_type=material_type,
            use_llm_cleanup=use_llm_cleanup,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    if result.error:
        raise HTTPException(status_code=400, detail=result.error)

    return {
        "ok": True,
        "material_id": result.material_id,
        "user_id": result.user_id,
        "parse_status": result.parse_status.value,
        "manifest_path": result.manifest_path,
        "markdown_path": result.markdown_path,
        "chunk_count": result.chunk_count,
        "quality_status": result.quality_status,
        "warnings": result.warnings,
        "metadata": result.metadata,
        "error": None,
    }


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
    results = search_user_materials_tool(uid, query, top_k=top_k, filters=filters or None)
    return {
        "ok": True,
        "user_id": uid,
        "query": query,
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
