from __future__ import annotations

import json
from typing import Any

from .indexing.material_indexer import load_search_index, search_in_index
from .schemas import Chunk, MaterialSearchResult
from .security import resolve_user_id
from .storage import MaterialStorage


def search_user_materials(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    storage: MaterialStorage | None = None,
) -> list[MaterialSearchResult]:
    storage = storage or MaterialStorage()
    safe_user_id = resolve_user_id(user_id)
    filters = filters or {}

    manifests = storage.list_user_manifests(safe_user_id)
    if filters.get("material_id"):
        manifests = [manifest for manifest in manifests if manifest.material_id == filters["material_id"]]
    if filters.get("subject"):
        manifests = [manifest for manifest in manifests if manifest.subject.value == filters["subject"]]
    if filters.get("material_type"):
        manifests = [manifest for manifest in manifests if manifest.material_type.value == filters["material_type"]]

    results: list[MaterialSearchResult] = []
    for manifest in manifests:
        if manifest.parse_status.value != "ready":
            continue

        chunks_path = manifest.paths.get("chunks")
        if not chunks_path:
            continue

        chunks_file = storage.material_dir(safe_user_id, manifest.material_id) / chunks_path
        if not chunks_file.exists():
            chunks_file = storage.material_dir(safe_user_id, manifest.material_id) / "chunks" / "chunks.jsonl"
            if not chunks_file.exists():
                continue

        index_path = manifest.paths.get("search_index")
        index_file = (
            storage.material_dir(safe_user_id, manifest.material_id) / index_path
            if index_path
            else storage.material_dir(safe_user_id, manifest.material_id) / "index" / "search_index.json"
        )
        if not index_file.exists():
            continue

        chunks: list[Chunk] = []
        try:
            with chunks_file.open(encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        chunks.append(Chunk.from_dict(json.loads(line)))
        except Exception:
            continue

        if not chunks:
            continue

        try:
            index_data = load_search_index(index_file)
        except Exception:
            continue

        chunk_scores = search_in_index(query, index_data, chunks, top_k=top_k)
        for rank, (chunk, score) in enumerate(chunk_scores, start=1):
            results.append(
                MaterialSearchResult(
                    rank=rank,
                    material_id=manifest.material_id,
                    user_id=safe_user_id,
                    chunk_id=chunk.chunk_id,
                    score=score,
                    text=chunk.text,
                    section_title=chunk.section_title,
                    heading_path=chunk.heading_path,
                    asset_paths=chunk.asset_paths,
                    source_markdown_path=manifest.paths.get("markdown"),
                    metadata={
                        "subject": manifest.subject.value,
                        "material_type": manifest.material_type.value,
                        "original_filename": manifest.original_filename,
                    },
                )
            )

    results.sort(key=lambda item: item.score, reverse=True)
    return results[:top_k]
