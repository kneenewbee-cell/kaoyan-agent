from __future__ import annotations

import json
import os
import re
import time
from dataclasses import asdict
from typing import Any

from .embeddings.qwen_embedding import embed_texts, embedding_api_available, load_embedding_settings
from .indexing.material_indexer import (
    TOKENIZER_VERSION,
    build_search_index,
    load_search_index,
    save_search_index,
    search_in_index,
)
from .indexing.query_processor import QueryPlan, process_query
from .llm_reranker import apply_llm_decisions, build_candidate_payload, build_material_search_rerank_client_from_env
from .pipeline_logger import monotonic_ms
from .schemas import Chunk, MaterialSearchResult
from .search_logger import write_material_search_log
from .search_planning import build_retrieval_plan
from .security import resolve_user_id
from .storage import MaterialStorage
from .vectorstores.chroma_store import ChromaUnavailableError, ChromaVectorStore


SearchMode = str
TABLE_COMMENT_RE = re.compile(r"<!--\s*table:\s*([^\s>]+).*?source=layout\.json.*?-->", re.IGNORECASE)
VECTOR_SCORE_BONUS_WEIGHT = 0.020
VECTOR_SCORE_BONUS_CAP = 0.024
TITLE_HIT_BONUS_CAP = 0.105
TEXT_HIT_BONUS_CAP = 0.020
SPECIFIC_TABLE_PENALTY = 0.025
SPECIFIC_OVERVIEW_TABLE_PENALTY = 0.060
OVERVIEW_TABLE_BONUS = 0.030
HYBRID_DISPLAY_MIN_SCORE = 0.040
QUERY_GATE_MIN_TERM_MATCHES = 2
QUERY_GATE_MIN_TERM_MATCH_RATIO = 0.50
EXACT_QUERY_HEADING_BONUS = 0.035
EXACT_QUERY_TEXT_BONUS = 0.012
OVERVIEW_QUERY_RE = re.compile(
    r"(考试要求|考试内容|目录|概览|总览|汇总|一览|对比|区别|表格|列表|清单|范围)"
)
OVERVIEW_TABLE_RE = re.compile(r"(考试要求|考试内容|目录|概览|总览|汇总|一览|知识清单|知识网络|范围)")


def _vector_min_score() -> float:
    raw = os.getenv("MATERIALS_VECTOR_MIN_SCORE", "0.60")
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
    if normalized not in {"keyword", "vector", "hybrid", "llm", "hybrid_llm"}:
        return "hybrid"
    return normalized


def _search_scope(filters: dict[str, Any]) -> str:
    return "material" if filters.get("material_id") else "subject"


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


def _search_scope_chunk_count(storage: MaterialStorage, user_id: str, filters: dict[str, Any]) -> int:
    total = 0
    for manifest in _filtered_ready_manifests(storage, user_id, filters):
        manifest_count = int(getattr(manifest, "chunk_count", 0) or 0)
        if manifest_count > 0:
            total += manifest_count
            continue
        try:
            total += len(_load_material_chunks(storage, user_id, manifest))
        except Exception:
            continue
    return total


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


def _vector_score_bonus(score: float) -> float:
    try:
        value = float(score)
    except (TypeError, ValueError):
        return 0.0
    if value <= 0:
        return 0.0
    return min(VECTOR_SCORE_BONUS_CAP, value * VECTOR_SCORE_BONUS_WEIGHT)


def _query_intent(query: str) -> str:
    return "overview" if OVERVIEW_QUERY_RE.search(query or "") else "specific"


def _contains_compact(haystack: str, needle: str) -> bool:
    if not haystack or not needle:
        return False
    return needle.lower() in "".join(str(haystack).lower().split())


def _compact_text(text: str) -> str:
    return "".join(str(text or "").lower().split())


def _result_heading_text(result: MaterialSearchResult) -> str:
    return " ".join([*(result.heading_path or []), result.section_title or ""])


def _result_query_text(result: MaterialSearchResult) -> str:
    return " ".join([_result_heading_text(result), result.text or ""])


def _matched_query_terms(result: MaterialSearchResult, terms: tuple[str, ...]) -> tuple[str, ...]:
    text = _result_query_text(result)
    return tuple(term for term in terms if _contains_compact(text, term))


def _query_gate_terms(plan: QueryPlan) -> tuple[str, ...]:
    return tuple(
        term
        for term in (plan.core_terms or plan.phrase_terms or plan.terms)
        if term and len(term) > 1
    )


def _passes_query_match_gate(result: MaterialSearchResult, plan: QueryPlan) -> bool:
    terms = _query_gate_terms(plan)
    if len(terms) < 3:
        return True

    matched_terms = _matched_query_terms(result, terms)
    required_count = max(
        QUERY_GATE_MIN_TERM_MATCHES,
        int(len(terms) * QUERY_GATE_MIN_TERM_MATCH_RATIO + 0.999),
    )
    if len(matched_terms) >= required_count:
        return True

    phrase_terms = tuple(term for term in plan.phrase_terms if term and len(term) > 1)
    if phrase_terms and _matched_query_terms(result, phrase_terms):
        return True

    metadata = dict(result.metadata or {})
    metadata["query_gate"] = {
        "matched_terms": list(matched_terms),
        "matched_count": len(matched_terms),
        "total_count": len(terms),
        "required_count": required_count,
    }
    result.metadata = metadata
    return False


def _filter_query_match_gate(
    results: list[MaterialSearchResult],
    plan: QueryPlan,
) -> list[MaterialSearchResult]:
    if not results:
        return results
    filtered = [result for result in results if _passes_query_match_gate(result, plan)]
    return filtered


def _exact_query_bonus(result: MaterialSearchResult, query: str) -> float:
    compact_query = _compact_text(query)
    if len(compact_query) < 3:
        return 0.0
    if compact_query in _compact_text(_result_heading_text(result)):
        return EXACT_QUERY_HEADING_BONUS
    if compact_query in _compact_text(result.text or ""):
        return EXACT_QUERY_TEXT_BONUS
    return 0.0


def _is_table_result(result: MaterialSearchResult) -> bool:
    metadata = dict(result.metadata or {})
    return bool(
        str(metadata.get("source_type") or "").lower() == "table"
        or metadata.get("table_id")
        or _table_id_from_text(result.text)
    )


def _is_overview_table_result(result: MaterialSearchResult) -> bool:
    if not _is_table_result(result):
        return False
    metadata = dict(result.metadata or {})
    marker_text = " ".join(
        [
            str(metadata.get("kind_guess") or ""),
            str(metadata.get("title") or ""),
            result.section_title or "",
            " ".join(result.heading_path or []),
            (result.text or "")[:500],
        ]
    )
    return bool(OVERVIEW_TABLE_RE.search(marker_text))


def _rerank_adjustment(
    result: MaterialSearchResult,
    plan: QueryPlan,
    intent: str,
    query: str,
) -> tuple[float, dict[str, Any]]:
    heading_text = _result_heading_text(result)
    body_text = result.text or ""
    terms = tuple(
        term
        for term in (plan.core_terms or plan.phrase_terms or plan.terms)
        if term and len(term) > 1
    )

    title_bonus = 0.0
    text_bonus = 0.0
    title_hits: list[str] = []
    text_hits: list[str] = []
    for term in terms:
        weight = max(float(plan.term_weights.get(term, 1.0)), 1.0)
        if _contains_compact(heading_text, term):
            title_hits.append(term)
            title_bonus += min(0.028 * weight, 0.04)
        elif _contains_compact(body_text, term):
            text_hits.append(term)
            text_bonus += min(0.006 * weight, 0.01)

    title_bonus = min(title_bonus, TITLE_HIT_BONUS_CAP)
    text_bonus = min(text_bonus, TEXT_HIT_BONUS_CAP)

    table_penalty = 0.0
    table_bonus = 0.0
    is_table = _is_table_result(result)
    is_overview_table = _is_overview_table_result(result)
    if intent == "specific":
        if is_overview_table:
            table_penalty = SPECIFIC_OVERVIEW_TABLE_PENALTY
        elif is_table:
            table_penalty = SPECIFIC_TABLE_PENALTY
    elif intent == "overview" and is_table:
        table_bonus = OVERVIEW_TABLE_BONUS

    exact_query_bonus = _exact_query_bonus(result, query)
    adjustment = title_bonus + text_bonus + table_bonus + exact_query_bonus - table_penalty
    return adjustment, {
        "intent": intent,
        "title_hits": title_hits,
        "text_hits": text_hits[:5],
        "title_bonus": round(title_bonus, 6),
        "text_bonus": round(text_bonus, 6),
        "table_bonus": round(table_bonus, 6),
        "table_penalty": round(table_penalty, 6),
        "exact_query_bonus": round(exact_query_bonus, 6),
        "is_table": is_table,
        "is_overview_table": is_overview_table,
        "adjustment": round(adjustment, 6),
    }


def _reranked_hybrid_scores(
    merged: dict[str, MaterialSearchResult],
    scores: dict[str, float],
    query: str,
) -> tuple[dict[str, float], dict[str, dict[str, Any]]]:
    if not (query or "").strip():
        return dict(scores), {}
    plan = process_query(query)
    intent = _query_intent(query)
    final_scores: dict[str, float] = {}
    details: dict[str, dict[str, Any]] = {}
    for key, result in merged.items():
        base_score = scores.get(key, 0.0)
        adjustment, detail = _rerank_adjustment(result, plan, intent, query)
        final_score = base_score + adjustment
        final_scores[key] = final_score
        detail["base_score"] = round(base_score, 6)
        detail["final_score"] = round(final_score, 6)
        details[key] = detail
    return final_scores, details


def _specific_phrase_terms(
    results: list[MaterialSearchResult],
    phrase_terms: tuple[str, ...],
) -> tuple[str, ...]:
    if not results or not phrase_terms:
        return ()
    counts: dict[str, int] = {}
    for term in phrase_terms:
        counts[term] = sum(1 for result in results if _contains_compact(_result_query_text(result), term))
    total = len(results)
    selected = [
        term
        for term, count in counts.items()
        if count > 0 and (count == 1 or count / total <= 0.35)
    ]
    return tuple(selected)


def _filter_hybrid_relevance(
    ranked: list[tuple[str, MaterialSearchResult]],
    *,
    plan: QueryPlan,
    intent: str,
) -> list[tuple[str, MaterialSearchResult]]:
    if intent != "specific" or not ranked:
        return ranked

    results = [result for _, result in ranked]
    phrase_gate_terms = _specific_phrase_terms(results, tuple(term for term in plan.phrase_terms if len(term) > 1))
    if phrase_gate_terms:
        filtered = [
            item
            for item in ranked
            if _matched_query_terms(item[1], phrase_gate_terms)
        ]
        if filtered:
            return filtered

    query_terms = _query_gate_terms(plan)
    if len(query_terms) < 3:
        return ranked

    match_counts = [len(_matched_query_terms(result, query_terms)) for _, result in ranked]
    minimum_count = max(
        QUERY_GATE_MIN_TERM_MATCHES,
        int(len(query_terms) * QUERY_GATE_MIN_TERM_MATCH_RATIO + 0.999),
    )
    filtered = [
        item
        for item, matched_count in zip(ranked, match_counts)
        if matched_count >= minimum_count
    ]
    return filtered


def _hybrid_results(
    keyword_results: list[MaterialSearchResult],
    vector_results: list[MaterialSearchResult],
    top_k: int,
    *,
    query: str = "",
    apply_relevance_filter: bool = True,
    apply_display_filter: bool = True,
) -> list[MaterialSearchResult]:
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
                scores[duplicate_key] = scores.get(duplicate_key, 0.0) + _rrf(rank) + _vector_score_bonus(result.score)
                sources.setdefault(duplicate_key, set()).add("vector")
                seen_sources.add("vector")
            continue
        merged.setdefault(key, result)
        if fingerprint:
            fingerprints[fingerprint] = key
            fingerprint_sources.setdefault(fingerprint, set()).add("vector")
        scores[key] = scores.get(key, 0.0) + _rrf(rank) + _vector_score_bonus(result.score)
        sources.setdefault(key, set()).add("vector")

    plan = process_query(query) if (query or "").strip() else None
    intent = _query_intent(query)
    final_scores, rerank_details = _reranked_hybrid_scores(merged, scores, query)
    ranked = sorted(merged.items(), key=lambda item: final_scores.get(item[0], 0.0), reverse=True)
    if plan is not None and apply_relevance_filter:
        ranked = _filter_hybrid_relevance(ranked, plan=plan, intent=intent)
    if plan is not None and apply_display_filter and HYBRID_DISPLAY_MIN_SCORE > 0:
        ranked = [
            item
            for item in ranked
            if final_scores.get(item[0], 0.0) >= HYBRID_DISPLAY_MIN_SCORE
        ]
    output: list[MaterialSearchResult] = []
    for rank, (key, result) in enumerate(ranked[:top_k], start=1):
        metadata = dict(result.metadata or {})
        metadata["search_mode"] = "hybrid"
        metadata["matched_by"] = sorted(sources.get(key, set()))
        if key in rerank_details:
            metadata["rerank"] = rerank_details[key]
            metadata["rerank_score"] = rerank_details[key]["final_score"]
        result.metadata = metadata
        result.score = final_scores.get(key, result.score)
        result.rank = rank
        output.append(result)
    return output


def _search_user_materials_with_llm(
    *,
    user_id: str,
    query: str,
    top_k: int,
    filters: dict[str, Any],
    storage: MaterialStorage,
    rerank_client: Any | None,
) -> list[MaterialSearchResult] | None:
    chunk_count = _search_scope_chunk_count(storage, user_id, filters)
    plan = build_retrieval_plan(
        chunk_count=chunk_count,
        query=query,
        scope=_search_scope(filters),
    )
    keyword_results = search_user_materials_keyword(
        user_id,
        query,
        top_k=max(plan.keyword_top_k, top_k),
        filters=filters,
        storage=storage,
    )
    vector_results = search_user_materials_vector(
        user_id,
        query,
        top_k=max(plan.vector_top_k, top_k),
        filters=filters,
        storage=storage,
    )
    candidates = _hybrid_results(
        keyword_results,
        vector_results,
        top_k=plan.recall_limit,
        query=query,
        apply_relevance_filter=False,
        apply_display_filter=False,
    )
    if not candidates:
        return []

    candidates = candidates[: plan.llm_candidate_limit]
    plan_metadata = asdict(plan)
    for result in candidates:
        metadata = dict(result.metadata or {})
        metadata["retrieval_plan"] = plan_metadata
        result.metadata = metadata

    active_client = rerank_client
    if active_client is None:
        active_client = build_material_search_rerank_client_from_env()
    if active_client is None:
        return None

    payload = build_candidate_payload(query, candidates)
    payload["retrieval_plan"] = plan_metadata
    try:
        decision_payload = active_client.rerank(payload)
    except Exception:
        return None
    if not isinstance(decision_payload, dict) or not isinstance(decision_payload.get("results"), list):
        return None

    ranked = apply_llm_decisions(candidates, decision_payload, top_k=top_k)
    return _finalize_results(ranked, top_k)


def search_user_materials(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    storage: MaterialStorage | None = None,
    mode: str = "hybrid",
    *,
    rerank_client: Any | None = None,
) -> list[MaterialSearchResult]:
    started_at = time.perf_counter()
    safe_user_id = resolve_user_id(user_id)
    filters = filters or {}
    mode = _normalize_search_mode(mode)
    active_storage = storage or MaterialStorage()
    results: list[MaterialSearchResult] = []
    logged_error = False
    try:
        if mode in {"llm", "hybrid_llm"}:
            llm_results = _search_user_materials_with_llm(
                user_id=safe_user_id,
                query=query,
                top_k=top_k,
                filters=filters,
                storage=active_storage,
                rerank_client=rerank_client,
            )
            if llm_results is not None:
                results = _expand_result_split_context(
                    llm_results,
                    storage=active_storage,
                    user_id=safe_user_id,
                    filters=filters,
                )
                return results
            mode = "hybrid"

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
            if (query or "").strip():
                keyword_results = _filter_query_match_gate(keyword_results, process_query(query))
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
            _hybrid_results(keyword_results, vector_results, max(top_k * 8, 40), query=query),
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
            elif mode in {"keyword", "vector", "hybrid", "llm", "hybrid_llm"}:
                write_material_search_log(
                    user_id=safe_user_id,
                    query=query,
                    mode=mode,
                    top_k=top_k,
                    filters=filters,
                    results=[],
                    elapsed_ms=monotonic_ms(started_at),
                )
