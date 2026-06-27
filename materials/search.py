from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from .embeddings.qwen_embedding import embed_texts, embedding_api_available, load_embedding_settings
from .indexing.material_indexer import (
    TOKENIZER_VERSION,
    build_search_index,
    load_search_index,
    save_search_index,
    search_in_index,
)
from .pipeline_logger import monotonic_ms
from .schemas import Chunk, MaterialSearchResult
from .search_logger import write_material_search_log
from .security import resolve_user_id
from .storage import MaterialStorage
from .vectorstores.chroma_store import ChromaUnavailableError, ChromaVectorStore


SearchMode = str
TABLE_COMMENT_RE = re.compile(r"<!--\s*table:\s*([^\s>]+).*?source=layout\.json.*?-->", re.IGNORECASE)


def _vector_min_score() -> float:
    raw = os.getenv("MATERIALS_VECTOR_MIN_SCORE", "0.55")
    try:
        return float(raw)
    except ValueError:
        return 0.55


def _diversify_headings_enabled() -> bool:
    return os.getenv("MATERIALS_SEARCH_DIVERSIFY_HEADINGS", "1").strip().lower() not in {
        "0",
        "false",
        "no",
        "off",
    }


def _max_results_per_table() -> int:
    raw = os.getenv("MATERIALS_SEARCH_MAX_RESULTS_PER_TABLE", "1")
    try:
        return max(int(raw), 0)
    except ValueError:
        return 1


def _split_context_enabled() -> bool:
    raw = os.getenv("MATERIALS_SEARCH_EXPAND_SPLIT_CONTEXT", "1").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def _split_context_max_chars() -> int:
    raw = os.getenv("MATERIALS_SEARCH_SPLIT_CONTEXT_MAX_CHARS", "4200")
    try:
        return max(int(raw), 0)
    except ValueError:
        return 4200


def _normalize_search_mode(mode: str | None) -> SearchMode:
    normalized = (mode or "hybrid").strip().lower()
    if normalized not in {"keyword", "vector", "hybrid"}:
        return "hybrid"
    return normalized


def _load_material_chunks(
    storage: MaterialStorage,
    user_id: str,
    manifest,
) -> list[Chunk]:
    chunks_path = manifest.paths.get("chunks")
    if not chunks_path:
        return []

    chunks_file = storage.material_dir(user_id, manifest.material_id) / chunks_path
    if not chunks_file.exists():
        chunks_file = storage.material_dir(user_id, manifest.material_id) / "chunks" / "chunks.jsonl"
        if not chunks_file.exists():
            return []

    chunks: list[Chunk] = []
    with chunks_file.open(encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                chunks.append(Chunk.from_dict(json.loads(line)))
    return chunks


def _filtered_ready_manifests(
    storage: MaterialStorage,
    user_id: str,
    filters: dict[str, Any],
):
    manifests = storage.list_user_manifests(user_id)
    if filters.get("material_id"):
        manifests = [manifest for manifest in manifests if manifest.material_id == filters["material_id"]]
    if filters.get("subject"):
        manifests = [manifest for manifest in manifests if manifest.subject.value == filters["subject"]]
    if filters.get("material_type"):
        manifests = [manifest for manifest in manifests if manifest.material_type.value == filters["material_type"]]
    return [manifest for manifest in manifests if manifest.parse_status.value == "ready"]


def _table_id_from_text(text: str) -> str:
    match = TABLE_COMMENT_RE.search(text or "")
    return match.group(1).strip() if match else ""


def _chunk_result_metadata(chunk: Chunk, manifest, search_mode: str) -> dict[str, Any]:
    metadata = dict(chunk.metadata or {})
    table_id = str(metadata.get("table_id") or _table_id_from_text(chunk.text) or "")
    if table_id:
        metadata.setdefault("source_type", "table")
        metadata["table_id"] = table_id
    metadata.update(
        {
            "subject": metadata.get("subject") or manifest.subject.value,
            "material_type": metadata.get("material_type") or manifest.material_type.value,
            "original_filename": metadata.get("original_filename") or manifest.original_filename,
            "search_mode": search_mode,
            "chunk_index": chunk.chunk_index,
        }
    )
    return metadata


def search_user_materials_keyword(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    storage: MaterialStorage | None = None,
) -> list[MaterialSearchResult]:
    storage = storage or MaterialStorage()
    safe_user_id = resolve_user_id(user_id)
    filters = filters or {}

    results: list[MaterialSearchResult] = []
    for manifest in _filtered_ready_manifests(storage, safe_user_id, filters):
        index_path = manifest.paths.get("search_index")
        index_file = (
            storage.material_dir(safe_user_id, manifest.material_id) / index_path
            if index_path
            else storage.material_dir(safe_user_id, manifest.material_id) / "index" / "search_index.json"
        )
        if not index_file.exists():
            continue

        try:
            chunks = _load_material_chunks(storage, safe_user_id, manifest)
        except Exception:
            continue

        if not chunks:
            continue

        try:
            index_data = load_search_index(index_file)
        except Exception:
            continue
        if index_data.get("tokenizer") != TOKENIZER_VERSION:
            index_data = build_search_index(chunks)
            try:
                save_search_index(index_data, index_file)
            except Exception:
                pass

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
                    metadata=_chunk_result_metadata(chunk, manifest, "keyword"),
                )
            )

    results.sort(key=lambda item: item.score, reverse=True)
    return results[:top_k]


def _vector_filters(user_id: str, filters: dict[str, Any]) -> dict[str, Any]:
    vector_filters = {"user_id": user_id}
    for key in ("material_id", "subject", "material_type"):
        if filters.get(key):
            vector_filters[key] = filters[key]
    return vector_filters


def _allowed_material_ids(storage: MaterialStorage, user_id: str, filters: dict[str, Any]) -> set[str]:
    return {manifest.material_id for manifest in _filtered_ready_manifests(storage, user_id, filters)}


def _score_from_distance(distance: Any) -> float:
    try:
        value = float(distance)
    except (TypeError, ValueError):
        return 0.0
    return 1.0 - value


def _heading_path_from_metadata(metadata: dict[str, Any]) -> list[str]:
    text = str(metadata.get("heading_path_text") or "").strip()
    return [item.strip() for item in text.split(">") if item.strip()]


def _result_fingerprint(text: str) -> str:
    compact = "".join(str(text or "").split())
    return compact[:1200]


def _table_group_key(result: MaterialSearchResult) -> str:
    metadata = dict(result.metadata or {})
    table_id = str(metadata.get("table_id") or _table_id_from_text(result.text) or "")
    if not table_id:
        return ""
    return f"{result.material_id}:{table_id}"


def _finalize_results(results: list[MaterialSearchResult], top_k: int) -> list[MaterialSearchResult]:
    max_per_table = _max_results_per_table()
    output: list[MaterialSearchResult] = []
    table_counts: dict[str, int] = {}

    for result in results:
        table_key = _table_group_key(result)
        if table_key and max_per_table > 0:
            count = table_counts.get(table_key, 0)
            if count >= max_per_table:
                continue
            table_counts[table_key] = count + 1
        output.append(result)
        if len(output) >= top_k:
            break

    for rank, result in enumerate(output, start=1):
        result.rank = rank
    return output


def _same_split_group(left: Chunk, right: Chunk) -> bool:
    return (
        left.material_id == right.material_id
        and left.user_id == right.user_id
        and (left.section_title or "") == (right.section_title or "")
        and list(left.heading_path or []) == list(right.heading_path or [])
        and left.metadata.get("split_reason") == "length"
        and right.metadata.get("split_reason") == "length"
    )


def _merge_contiguous_texts(parts: list[str]) -> str:
    merged = ""
    for part in parts:
        part = str(part or "").strip()
        if not part:
            continue
        if not merged:
            merged = part
            continue
        overlap = 0
        max_overlap = min(len(merged), len(part), 700)
        for size in range(max_overlap, 20, -1):
            if merged[-size:] == part[:size]:
                overlap = size
                break
        addition = part[overlap:].strip() if overlap else part
        if addition:
            merged = f"{merged}\n\n{addition}".strip()
    return merged


def _expand_result_split_context(
    results: list[MaterialSearchResult],
    *,
    storage: MaterialStorage,
    user_id: str,
    filters: dict[str, Any],
) -> list[MaterialSearchResult]:
    if not _split_context_enabled():
        return results
    max_chars = _split_context_max_chars()
    if max_chars <= 0:
        return results

    material_chunks: dict[str, list[Chunk]] = {}
    material_chunk_index: dict[str, dict[str, int]] = {}
    for manifest in _filtered_ready_manifests(storage, user_id, filters):
        try:
            chunks = _load_material_chunks(storage, user_id, manifest)
        except Exception:
            chunks = []
        material_chunks[manifest.material_id] = chunks
        material_chunk_index[manifest.material_id] = {
            chunk.chunk_id: index for index, chunk in enumerate(chunks)
        }

    for result in results:
        chunks = material_chunks.get(result.material_id) or []
        index_map = material_chunk_index.get(result.material_id) or {}
        index = index_map.get(result.chunk_id)
        if index is None:
            continue
        current = chunks[index]
        if current.metadata.get("split_reason") != "length":
            continue

        selected: list[Chunk] = [current]
        total_chars = len(current.text)

        previous_index = index - 1
        if previous_index >= 0 and _same_split_group(chunks[previous_index], current):
            previous = chunks[previous_index]
            if total_chars + len(previous.text) <= max_chars:
                selected.insert(0, previous)
                total_chars += len(previous.text)

        next_index = index + 1
        while next_index < len(chunks):
            candidate = chunks[next_index]
            if not _same_split_group(current, candidate):
                break
            if total_chars + len(candidate.text) > max_chars:
                break
            selected.append(candidate)
            total_chars += len(candidate.text)
            next_index += 1

        if len(selected) <= 1:
            continue
        result.text = _merge_contiguous_texts([chunk.text for chunk in selected])
        metadata = dict(result.metadata or {})
        metadata["context_expanded"] = True
        metadata["context_chunk_ids"] = [chunk.chunk_id for chunk in selected]
        metadata["context_part_indexes"] = [chunk.metadata.get("part_index") for chunk in selected]
        metadata["context_max_chars"] = max_chars
        result.metadata = metadata
    return results


def search_user_materials_vector(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    storage: MaterialStorage | None = None,
    *,
    store: ChromaVectorStore | None = None,
) -> list[MaterialSearchResult]:
    safe_user_id = resolve_user_id(user_id)
    filters = filters or {}
    storage = storage or MaterialStorage()
    allowed_material_ids = _allowed_material_ids(storage, safe_user_id, filters)
    if not allowed_material_ids:
        return []
    settings = load_embedding_settings()
    if not embedding_api_available(settings):
        return []

    try:
        vector_store = store or ChromaVectorStore()
        vector_store.collection()
        query_embedding = embed_texts([query], settings=settings)[0]
        payload = vector_store.query(
            query_embedding,
            top_k=max(top_k * 5, 20),
            filters=_vector_filters(safe_user_id, filters),
        )
    except (ChromaUnavailableError, Exception):
        return []

    documents = (payload.get("documents") or [[]])[0] or []
    metadatas = (payload.get("metadatas") or [[]])[0] or []
    distances = (payload.get("distances") or [[]])[0] or []
    min_score = _vector_min_score()

    results: list[MaterialSearchResult] = []
    seen_texts: set[str] = set()
    seen_heading_paths: set[str] = set()
    diversify_headings = _diversify_headings_enabled()
    for rank, document in enumerate(documents, start=1):
        metadata = dict(metadatas[rank - 1] if rank - 1 < len(metadatas) and metadatas[rank - 1] else {})
        material_id = str(metadata.get("material_id") or "")
        if material_id not in allowed_material_ids:
            continue
        heading_key = str(metadata.get("heading_path_text") or metadata.get("section_title") or "").strip()
        if diversify_headings and heading_key and heading_key in seen_heading_paths:
            continue
        fingerprint = _result_fingerprint(str(document or ""))
        if fingerprint and fingerprint in seen_texts:
            continue
        distance = distances[rank - 1] if rank - 1 < len(distances) else None
        score = _score_from_distance(distance)
        if score < min_score:
            continue
        if fingerprint:
            seen_texts.add(fingerprint)
        if heading_key:
            seen_heading_paths.add(heading_key)
        results.append(
            MaterialSearchResult(
                rank=len(results) + 1,
                material_id=material_id,
                user_id=safe_user_id,
                chunk_id=str(metadata.get("chunk_id") or ""),
                score=score,
                text=str(document or ""),
                section_title=str(metadata.get("section_title") or "") or None,
                heading_path=_heading_path_from_metadata(metadata),
                asset_paths=[],
                source_markdown_path=str(metadata.get("source_markdown_path") or "") or None,
                metadata={
                    "subject": metadata.get("subject", "unknown"),
                    "material_type": metadata.get("material_type", "unknown"),
                    "original_filename": metadata.get("original_filename", ""),
                    "title": metadata.get("title", ""),
                    "chunk_index": metadata.get("chunk_index", ""),
                    "split_reason": metadata.get("split_reason", ""),
                    "part_index": metadata.get("part_index", ""),
                    "start_line": metadata.get("start_line", ""),
                    "end_line": metadata.get("end_line", ""),
                    "source_type": metadata.get("source_type", ""),
                    "table_id": metadata.get("table_id", ""),
                    "table_row_index": metadata.get("table_row_index", ""),
                    "page": metadata.get("page", ""),
                    "kind_guess": metadata.get("kind_guess", ""),
                    "distance": distance,
                    "vector_min_score": min_score,
                    "search_mode": "vector",
                },
            )
        )
    return results[:top_k]


def _rrf(rank: int, k: int = 60) -> float:
    return 1.0 / (k + rank)


def _hybrid_results(keyword_results: list[MaterialSearchResult], vector_results: list[MaterialSearchResult], top_k: int) -> list[MaterialSearchResult]:
    merged: dict[str, MaterialSearchResult] = {}
    scores: dict[str, float] = {}
    sources: dict[str, set[str]] = {}
    fingerprints: dict[str, str] = {}
    fingerprint_sources: dict[str, set[str]] = {}

    for rank, result in enumerate(keyword_results, start=1):
        key = result.chunk_id or f"keyword:{rank}:{result.material_id}"
        fingerprint = _result_fingerprint(result.text)
        duplicate_key = fingerprints.get(fingerprint) if fingerprint else None
        if duplicate_key:
            seen_sources = fingerprint_sources.setdefault(fingerprint, set())
            if "keyword" not in seen_sources:
                scores[duplicate_key] = scores.get(duplicate_key, 0.0) + _rrf(rank)
                sources.setdefault(duplicate_key, set()).add("keyword")
                seen_sources.add("keyword")
            continue
        merged[key] = result
        if fingerprint:
            fingerprints[fingerprint] = key
            fingerprint_sources.setdefault(fingerprint, set()).add("keyword")
        scores[key] = scores.get(key, 0.0) + _rrf(rank)
        sources.setdefault(key, set()).add("keyword")

    for rank, result in enumerate(vector_results, start=1):
        key = result.chunk_id or f"vector:{rank}:{result.material_id}"
        fingerprint = _result_fingerprint(result.text)
        duplicate_key = fingerprints.get(fingerprint) if fingerprint else None
        if duplicate_key:
            seen_sources = fingerprint_sources.setdefault(fingerprint, set())
            if "vector" not in seen_sources:
                scores[duplicate_key] = scores.get(duplicate_key, 0.0) + _rrf(rank)
                sources.setdefault(duplicate_key, set()).add("vector")
                seen_sources.add("vector")
            continue
        merged.setdefault(key, result)
        if fingerprint:
            fingerprints[fingerprint] = key
            fingerprint_sources.setdefault(fingerprint, set()).add("vector")
        scores[key] = scores.get(key, 0.0) + _rrf(rank)
        sources.setdefault(key, set()).add("vector")

    ranked = sorted(merged.items(), key=lambda item: scores.get(item[0], 0.0), reverse=True)
    output: list[MaterialSearchResult] = []
    for rank, (key, result) in enumerate(ranked[:top_k], start=1):
        metadata = dict(result.metadata or {})
        metadata["search_mode"] = "hybrid"
        metadata["matched_by"] = sorted(sources.get(key, set()))
        result.metadata = metadata
        result.score = scores.get(key, result.score)
        result.rank = rank
        output.append(result)
    return output


def search_user_materials(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    storage: MaterialStorage | None = None,
    mode: str = "hybrid",
) -> list[MaterialSearchResult]:
    started_at = time.perf_counter()
    safe_user_id = resolve_user_id(user_id)
    filters = filters or {}
    mode = _normalize_search_mode(mode)
    active_storage = storage or MaterialStorage()
    results: list[MaterialSearchResult] = []
    logged_error = False
    try:
        if mode == "keyword":
            raw_results = search_user_materials_keyword(
                safe_user_id,
                query,
                top_k=max(top_k * 8, 40),
                filters=filters,
                storage=active_storage,
            )
            results = _finalize_results(raw_results, top_k)
            results = _expand_result_split_context(
                results,
                storage=active_storage,
                user_id=safe_user_id,
                filters=filters,
            )
            return results
        if mode == "vector":
            raw_results = search_user_materials_vector(
                safe_user_id,
                query,
                top_k=max(top_k * 8, 40),
                filters=filters,
                storage=active_storage,
            )
            results = _finalize_results(raw_results, top_k)
            results = _expand_result_split_context(
                results,
                storage=active_storage,
                user_id=safe_user_id,
                filters=filters,
            )
            return results

        keyword_results = search_user_materials_keyword(
            safe_user_id,
            query,
            top_k=max(top_k * 8, 40),
            filters=filters,
            storage=active_storage,
        )
        vector_results = search_user_materials_vector(
            safe_user_id,
            query,
            top_k=max(top_k * 8, 40),
            filters=filters,
            storage=active_storage,
        )
        if not vector_results:
            results = _finalize_results(keyword_results, top_k)
            results = _expand_result_split_context(
                results,
                storage=active_storage,
                user_id=safe_user_id,
                filters=filters,
            )
            return results
        if not keyword_results:
            results = _finalize_results(vector_results, top_k)
            results = _expand_result_split_context(
                results,
                storage=active_storage,
                user_id=safe_user_id,
                filters=filters,
            )
            return results
        results = _finalize_results(
            _hybrid_results(keyword_results, vector_results, max(top_k * 8, 40)),
            top_k,
        )
        results = _expand_result_split_context(
            results,
            storage=active_storage,
            user_id=safe_user_id,
            filters=filters,
        )
        return results
    except Exception as exc:
        write_material_search_log(
            user_id=safe_user_id,
            query=query,
            mode=mode,
            top_k=top_k,
            filters=filters,
            results=[],
            elapsed_ms=monotonic_ms(started_at),
            error=str(exc),
        )
        logged_error = True
        raise
    finally:
        if not logged_error:
            if results:
                write_material_search_log(
                    user_id=safe_user_id,
                    query=query,
                    mode=mode,
                    top_k=top_k,
                    filters=filters,
                    results=results,
                    elapsed_ms=monotonic_ms(started_at),
                )
            elif mode in {"keyword", "vector", "hybrid"}:
                write_material_search_log(
                    user_id=safe_user_id,
                    query=query,
                    mode=mode,
                    top_k=top_k,
                    filters=filters,
                    results=[],
                    elapsed_ms=monotonic_ms(started_at),
                )
