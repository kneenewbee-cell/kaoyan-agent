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
    mode: str = "hybrid",
) -> list[dict[str, Any]]:
    results = search_user_materials(
        user_id=resolve_user_id(user_id),
        query=query,
        top_k=top_k,
        filters=filters,
        mode=mode,
    )

    return [
        {
            "rank": result.rank,
            "material_id": result.material_id,
            "chunk_id": result.chunk_id,
            "score": result.score,
            "text": result.text,
            "text_preview": "",
            "text_excerpt": result.text[:200],
            "section_title": result.section_title,
            "heading_path": result.heading_path,
            "asset_paths": result.asset_paths,
            "source_markdown_path": result.source_markdown_path,
            "original_filename": result.metadata.get("original_filename", ""),
            "subject": result.metadata.get("subject", "unknown"),
            "material_type": result.metadata.get("material_type", "unknown"),
            "search_mode": result.metadata.get("search_mode", mode),
            "matched_by": result.metadata.get("matched_by", []),
            "score_kind": _score_kind(str(result.metadata.get("search_mode", mode))),
            "chunk_index": result.metadata.get("chunk_index", ""),
            "split_reason": result.metadata.get("split_reason", ""),
            "part_index": result.metadata.get("part_index", ""),
            "context_expanded": result.metadata.get("context_expanded", False),
            "context_chunk_ids": result.metadata.get("context_chunk_ids", []),
            "context_part_indexes": result.metadata.get("context_part_indexes", []),
            "source_type": result.metadata.get("source_type", ""),
            "table_id": result.metadata.get("table_id", ""),
            "table_row_index": result.metadata.get("table_row_index", ""),
            "page": result.metadata.get("page", ""),
        }
        for result in results
    ]


def _score_kind(search_mode: str) -> str:
    if search_mode == "vector":
        return "vector_similarity"
    if search_mode == "hybrid":
        return "rank_fusion"
    return "keyword_score"


def ingest_user_material(
    file_path: str,
    user_id: str = "tester",
    subject: str = "unknown",
    material_type: str = "unknown",
    use_llm_cleanup: bool = True,
    enable_vector_index: bool = True,
) -> dict[str, Any]:
    result = MaterialIngestionService().ingest_file(
        file_path=file_path,
        user_id=resolve_user_id(user_id),
        subject=subject,
        material_type=material_type,
        use_llm_cleanup=use_llm_cleanup,
        enable_vector_index=enable_vector_index,
    )

    return {
        "material_id": result.material_id,
        "user_id": result.user_id,
        "parse_status": result.parse_status.value,
        "manifest_path": result.manifest_path,
        "markdown_path": result.markdown_path,
        "chunk_count": result.chunk_count,
        "asset_count": result.asset_count,
        "vector_index": result.metadata.get("vector_index", {}),
        "error": result.error,
    }
