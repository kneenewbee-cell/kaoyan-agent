from __future__ import annotations

import json
import re
from typing import Any

from .priority import source_priority
from .repository import CurrentAffairsStore, current_beijing_year


def search_current_affairs_store(
    args: dict[str, Any] | None = None,
    *,
    store: CurrentAffairsStore | None = None,
) -> dict[str, Any]:
    payload = args or {}
    store = store or CurrentAffairsStore()
    mode = str(payload.get("mode") or "").strip().lower()
    if not mode:
        mode = "detail" if payload.get("event_id") else "search"
    if mode == "detail":
        return detail(payload, store)
    return search(payload, store)


def detail(args: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any]:
    event_id = str(args.get("event_id") or "").strip()
    event = store.get_event(event_id) if event_id else None
    warnings: list[str] = []
    items: list[dict[str, Any]] = []
    if event:
        items.append(build_event_item(event, store))
    else:
        warnings.append("未在本地时政资料库找到该 event_id。")
    return {
        "type": "current_affairs_store",
        "mode": "detail",
        "query": event_id,
        "items": items,
        "total_results": len(items),
        "warnings": warnings,
    }


def search(args: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any]:
    query = str(args.get("query") or "").strip()
    year = str(args.get("year") or "").strip()
    category = str(args.get("category") or "").strip()
    try:
        top_k = max(1, min(20, int(args.get("top_k") or 5)))
    except (TypeError, ValueError):
        top_k = 5

    terms = query_terms(query)
    scored: list[tuple[float, dict[str, Any]]] = []
    for event in store.list_events():
        if year and str(event.get("event_date") or "")[:4] != year:
            continue
        if category and str(event.get("category") or "") != category:
            continue
        score = event_score(event, terms)
        if score > 0 or not terms:
            scored.append((score, event))

    scored.sort(
        key=lambda pair: (
            pair[0],
            str(pair[1].get("event_date") or ""),
            primary_source_score(pair[1], store),
        ),
        reverse=True,
    )
    items = [build_event_item(event, store) for _, event in scored[:top_k]]
    return {
        "type": "current_affairs_store",
        "mode": "search",
        "query": query,
        "year": year or current_beijing_year(),
        "category": category,
        "items": items,
        "total_results": len(items),
        "warnings": [] if items else ["本地时政资料库没有命中可用事件，需要补充联网检索。"],
    }


def build_event_item(event: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any]:
    source_ids = [str(item) for item in event.get("source_doc_ids") or [] if str(item).strip()]
    sources = [source for source_id in source_ids if (source := store.get_source(source_id))]
    primary_source = choose_primary_source(event, sources)
    supporting_sources = [source for source in sources if source.get("source_doc_id") != primary_source.get("source_doc_id")]
    source_doc_ids = [str(source.get("source_doc_id")) for source in sources if source.get("source_doc_id")]
    return {
        "event_id": event.get("event_id"),
        "title": event.get("title"),
        "category": event.get("category"),
        "event_date": event.get("event_date"),
        "published_at": primary_source.get("published_at") or event.get("published_at") or event.get("event_date"),
        "topics": event.get("topics") or [],
        "summary": event.get("summary") or primary_source.get("content_preview") or "",
        "source_doc_ids": source_doc_ids,
        "source_doc_id": primary_source.get("source_doc_id") or "",
        "primary_source_doc_id": primary_source.get("source_doc_id") or event.get("primary_source_doc_id") or "",
        "primary_source": slim_source(primary_source),
        "supporting_sources": [slim_source(source) for source in supporting_sources],
        "confidence": event.get("confidence") or "medium",
        "last_verified_at": event.get("last_verified_at"),
    }


def choose_primary_source(event: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    primary_id = str(event.get("primary_source_doc_id") or "")
    for source in sources:
        if source.get("source_doc_id") == primary_id:
            return source
    if not sources:
        return {}
    return sorted(
        sources,
        key=lambda source: (
            source_priority(str(source.get("source_domain") or ""), str(event.get("category") or "")),
            len(str(source.get("content_preview") or "")),
            str(source.get("published_at") or ""),
        ),
        reverse=True,
    )[0]


def slim_source(source: dict[str, Any]) -> dict[str, Any]:
    if not source:
        return {}
    return {
        "source_doc_id": source.get("source_doc_id"),
        "source_domain": source.get("source_domain"),
        "source_type": source.get("source_type"),
        "title": source.get("title"),
        "published_at": source.get("published_at"),
        "event_date": source.get("event_date"),
        "content_preview": source.get("content_preview"),
        "url_hash": source.get("url_hash"),
    }


def event_score(event: dict[str, Any], terms: list[str]) -> float:
    if not terms:
        return 1.0
    haystack = json.dumps(
        {
            "title": event.get("title"),
            "summary": event.get("summary"),
            "topics": event.get("topics"),
            "aliases": event.get("aliases"),
            "category": event.get("category"),
        },
        ensure_ascii=False,
    ).lower()
    score = 0.0
    for term in terms:
        if term in haystack:
            score += 2.0 if len(term) >= 4 else 1.0
    title = str(event.get("title") or "").lower()
    score += sum(1.5 for term in terms if term and term in title)
    return score


def primary_source_score(event: dict[str, Any], store: CurrentAffairsStore) -> int:
    primary = store.get_source(str(event.get("primary_source_doc_id") or ""))
    if not primary:
        return 0
    return source_priority(str(primary.get("source_domain") or ""), str(event.get("category") or ""))


def query_terms(query: str) -> list[str]:
    raw_terms = re.split(r"[\s,，。；;：:、]+", str(query or "").lower())
    terms: list[str] = []
    seen: set[str] = set()
    for term in raw_terms:
        cleaned = re.sub(r"^[\"'“”‘’（）()【】\[\]]+|[\"'“”‘’（）()【】\[\]]+$", "", term.strip())
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        terms.append(cleaned)
    return terms
