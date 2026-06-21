from __future__ import annotations

from typing import Any

from .search import search_user_materials
from .security import resolve_user_id
from .service import MaterialIngestionService


def get_current_user_id(user_id: str | None = None) -> str:
    return resolve_user_id(user_id)


def search_user_materials_tool(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    results = search_user_materials(
        user_id=resolve_user_id(user_id),
        query=query,
        top_k=top_k,
        filters=filters,
    )

    return [
        {
            "rank": result.rank,
            "material_id": result.material_id,
            "chunk_id": result.chunk_id,
            "score": result.score,
            "text": result.text,
            "text_preview": result.text[:200],
            "section_title": result.section_title,
            "heading_path": result.heading_path,
            "asset_paths": result.asset_paths,
            "source_markdown_path": result.source_markdown_path,
            "original_filename": result.metadata.get("original_filename", ""),
            "subject": result.metadata.get("subject", "unknown"),
            "material_type": result.metadata.get("material_type", "unknown"),
        }
        for result in results
    ]


def ingest_user_material(
    file_path: str,
    user_id: str = "tester",
    subject: str = "unknown",
    material_type: str = "unknown",
) -> dict[str, Any]:
    result = MaterialIngestionService().ingest_file(
        file_path=file_path,
        user_id=resolve_user_id(user_id),
        subject=subject,
        material_type=material_type,
    )

    return {
        "material_id": result.material_id,
        "user_id": result.user_id,
        "parse_status": result.parse_status.value,
        "manifest_path": result.manifest_path,
        "markdown_path": result.markdown_path,
        "chunk_count": result.chunk_count,
        "asset_count": result.asset_count,
        "error": result.error,
    }
