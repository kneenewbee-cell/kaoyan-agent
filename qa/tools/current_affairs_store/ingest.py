from __future__ import annotations

import hashlib
import re
from difflib import SequenceMatcher
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .priority import clean_domain, source_priority
from .repository import CurrentAffairsStore, date_compact


def ingest_verified_evidence(
    evidence: list[dict[str, Any]],
    *,
    store: CurrentAffairsStore | None = None,
) -> list[dict[str, Any]]:
    store = store or CurrentAffairsStore()
    enriched: list[dict[str, Any]] = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        enriched.append(ingest_one(item, store))
    return enriched


def ingest_one(item: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any]:
    normalized = normalize_evidence_item(item)
    existing_source = store.find_source_by_url(normalized["canonical_url"]) if normalized["canonical_url"] else None
    if existing_source:
        event = store.get_event(str(existing_source.get("event_id") or ""))
        event_id = str(existing_source.get("event_id") or "")
        source_doc_id = str(existing_source.get("source_doc_id") or "")
        if event:
            event = touch_event_source(event, source_doc_id, store)
        copied = dict(item)
        copied.update({
            "event_id": event_id,
            "source_doc_id": source_doc_id,
            "source_doc_ids": list((event or {}).get("source_doc_ids") or [source_doc_id]),
            "primary_source_doc_id": (event or {}).get("primary_source_doc_id") or source_doc_id,
        })
        return copied

    event = find_matching_event(normalized, store)
    if event is None:
        event = build_new_event(normalized, store)

    source = build_source(normalized, event)
    source = store.upsert_source(source)
    event = merge_source_into_event(event, source, normalized, store)

    copied = dict(item)
    copied.update({
        "event_id": event["event_id"],
        "source_doc_id": source["source_doc_id"],
        "source_doc_ids": list(event.get("source_doc_ids") or []),
        "primary_source_doc_id": event.get("primary_source_doc_id"),
    })
    return copied


def normalize_evidence_item(item: dict[str, Any]) -> dict[str, Any]:
    url = str(item.get("url") or "").strip()
    canon = canonical_url(url)
    domain = clean_domain(str(item.get("source_domain") or domain_from_url(canon)))
    published_at = first_date(str(item.get("published_at") or "")) or first_date_from_values(item.get("extracted_dates")) or ""
    event_date = str(item.get("event_date") or "").strip() or first_date_from_values(item.get("extracted_dates")) or published_at
    category = infer_category(item)
    return {
        **item,
        "url": url,
        "canonical_url": canon,
        "source_domain": domain,
        "published_at": published_at,
        "event_date": event_date,
        "category": category,
        "normalized_title": normalize_title(str(item.get("title") or "")),
        "content_signature": content_signature(str(item.get("text_preview") or item.get("snippet") or "")),
    }


def build_source(item: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    source_doc_id = source_id(item)
    return {
        "source_doc_id": source_doc_id,
        "event_id": event["event_id"],
        "title": item.get("title") or "",
        "source_domain": item.get("source_domain") or "",
        "source_type": source_type(str(item.get("source_domain") or "")),
        "url": item.get("url") or "",
        "canonical_url": item.get("canonical_url") or "",
        "published_at": item.get("published_at") or "",
        "event_date": item.get("event_date") or "",
        "content_preview": item.get("text_preview") or item.get("snippet") or "",
        "content_signature": item.get("content_signature") or "",
        "extracted_dates": item.get("extracted_dates") or [],
        "url_hash": source_doc_id.rsplit("_", 1)[-1],
        "confidence_hint": item.get("confidence_hint") or "",
    }


def build_new_event(item: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any]:
    event_date = item.get("event_date") or item.get("published_at") or ""
    return {
        "event_id": store.next_event_id(str(event_date)),
        "title": item.get("title") or "",
        "category": item.get("category") or "other",
        "event_date": event_date,
        "event_date_precision": "day" if event_date else "unknown",
        "topics": infer_topics(item),
        "summary": item.get("text_preview") or item.get("snippet") or "",
        "source_doc_ids": [],
        "supporting_source_doc_ids": [],
        "primary_source_doc_id": "",
        "confidence": item.get("confidence_hint") or "medium",
        "fingerprints": [event_fingerprint(item)],
        "aliases": infer_aliases(item),
        "merged_from": [],
    }


def find_matching_event(item: dict[str, Any], store: CurrentAffairsStore) -> dict[str, Any] | None:
    candidates = [
        event for event in store.list_events()
        if event_candidate_match(item, event)
    ]
    if not candidates:
        return None
    scored = sorted(((event_similarity(item, event), event) for event in candidates), key=lambda pair: pair[0], reverse=True)
    if scored and scored[0][0] >= 0.78:
        return scored[0][1]
    return None


def event_candidate_match(item: dict[str, Any], event: dict[str, Any]) -> bool:
    if str(item.get("event_date") or "") and str(event.get("event_date") or ""):
        if str(item["event_date"])[:10] != str(event["event_date"])[:10]:
            return False
    if str(item.get("category") or "other") != str(event.get("category") or "other"):
        return False
    return True


def event_similarity(item: dict[str, Any], event: dict[str, Any]) -> float:
    title_a = str(item.get("normalized_title") or normalize_title(str(item.get("title") or "")))
    title_b = normalize_title(str(event.get("title") or ""))
    title_score = SequenceMatcher(None, title_a, title_b).ratio()
    topics_a = set(infer_topics(item))
    topics_b = set(str(topic) for topic in event.get("topics") or [])
    topic_score = len(topics_a & topics_b) / max(1, len(topics_a | topics_b))
    fingerprint_score = 1.0 if event_fingerprint(item) in set(event.get("fingerprints") or []) else 0.0
    return max(title_score, topic_score, fingerprint_score)


def merge_source_into_event(
    event: dict[str, Any],
    source: dict[str, Any],
    item: dict[str, Any],
    store: CurrentAffairsStore,
) -> dict[str, Any]:
    source_ids = unique_strings([*event.get("source_doc_ids", []), source["source_doc_id"]])
    existing_primary = str(event.get("primary_source_doc_id") or "")
    primary = choose_primary_source(existing_primary, source, event, store)
    supporting = [source_id for source_id in source_ids if source_id != primary]
    fingerprints = unique_strings([*event.get("fingerprints", []), event_fingerprint(item)])
    aliases = unique_strings([*event.get("aliases", []), *infer_aliases(item)])
    updated = {
        **event,
        "source_doc_ids": source_ids,
        "supporting_source_doc_ids": supporting,
        "primary_source_doc_id": primary,
        "fingerprints": fingerprints,
        "aliases": aliases,
    }
    if primary == source["source_doc_id"]:
        updated["title"] = source.get("title") or updated.get("title") or ""
        updated["summary"] = source.get("content_preview") or updated.get("summary") or ""
        updated["event_date"] = source.get("event_date") or updated.get("event_date") or ""
    return store.upsert_event(updated)


def touch_event_source(event: dict[str, Any], source_doc_id: str, store: CurrentAffairsStore) -> dict[str, Any]:
    updated = {**event, "source_doc_ids": unique_strings([*event.get("source_doc_ids", []), source_doc_id])}
    if not updated.get("primary_source_doc_id"):
        updated["primary_source_doc_id"] = source_doc_id
    return store.upsert_event(updated)


def choose_primary_source(current_primary_id: str, incoming_source: dict[str, Any], event: dict[str, Any], store: CurrentAffairsStore) -> str:
    if not current_primary_id:
        return str(incoming_source["source_doc_id"])
    current_source = store.get_source(current_primary_id)
    if not current_source:
        return str(incoming_source["source_doc_id"])
    incoming_rank = source_quality(incoming_source, str(event.get("category") or ""))
    current_rank = source_quality(current_source, str(event.get("category") or ""))
    if incoming_rank > current_rank:
        return str(incoming_source["source_doc_id"])
    return current_primary_id


def source_quality(source: dict[str, Any], category: str) -> tuple[int, int, str, str]:
    priority = source_priority(str(source.get("source_domain") or ""), category)
    preview_len = len(str(source.get("content_preview") or ""))
    published = str(source.get("published_at") or "9999-99-99")
    source_id = str(source.get("source_doc_id") or "")
    return priority, preview_len, invert_for_earlier_date(published), "".join(chr(255 - ord(ch)) for ch in source_id[:64])


def source_id(item: dict[str, Any]) -> str:
    compact_date = date_compact(str(item.get("published_at") or item.get("event_date") or ""))
    domain = re.sub(r"[^a-z0-9]+", "_", clean_domain(str(item.get("source_domain") or "unknown"))).strip("_") or "unknown"
    seed = item.get("canonical_url") or item.get("url") or f"{item.get('title')}|{item.get('source_domain')}"
    digest = hashlib.sha1(str(seed).encode("utf-8")).hexdigest()[:8]
    return f"cas_{compact_date}_{domain}_{digest}"


def event_fingerprint(item: dict[str, Any]) -> str:
    parts = [
        str(item.get("event_date") or "")[:10],
        str(item.get("category") or ""),
        normalize_title(str(item.get("title") or "")),
    ]
    return "|".join(part for part in parts if part)


def infer_category(item: dict[str, Any]) -> str:
    title = str(item.get("title") or "")
    group = str(item.get("group") or "")
    matched_groups = " ".join(str(value or "") for value in item.get("matched_groups") or [])
    group_text = f"{group} {matched_groups}".lower()
    if any(token in group_text for token in ("law_or_draft", "law_draft", "legislation", "npc_law", "draft_review")):
        return "law_or_draft"
    if any(token in group_text for token in ("meeting", "forum", "conference", "npc_cppcc", "summit", "davos")):
        return "meeting"
    if any(token in group_text for token in ("policy", "document", "notice", "guideline", "regulation")):
        return "policy_document"
    if any(token in group_text for token in ("international", "diplomacy", "foreign", "weforum")):
        return "international_event"
    if any(token in group_text for token in ("speech", "article", "address")):
        return "speech"
    text = f"{title} {group}"
    if any(word in text for word in ("草案", "法律", "法案", "审议")):
        return "law_or_draft"
    if any(word in text for word in ("会议", "常委会", "论坛", "峰会")):
        return "meeting"
    if any(word in text for word in ("文件", "政策", "通知", "意见", "方案", "办法")):
        return "policy_document"
    if any(word in text for word in ("会见", "外交", "访问", "国际")):
        return "international_event"
    if any(word in text for word in ("讲话", "文章", "致辞")):
        return "speech"
    return "other"


def infer_topics(item: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("topics", "matched_groups", "extracted_dates"):
        for value in item.get(key) or []:
            text = str(value or "").strip()
            if text and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
                values.append(text)
    title = str(item.get("title") or "")
    for token in re.split(r"[丨｜：:，,。；;、\s]+", title):
        token = token.strip()
        if len(token) >= 4:
            values.append(token)
    return unique_strings(values[:12])


def infer_aliases(item: dict[str, Any]) -> list[str]:
    aliases = [str(item.get("title") or "").strip()]
    aliases.extend(str(value or "").strip() for value in item.get("matched_groups") or [])
    return unique_strings([alias for alias in aliases if alias])


def normalize_title(title: str) -> str:
    return re.sub(r"[\s\-—_·丨｜：:，,。；;、\"“”'‘’（）()【】\[\]]+", "", str(title or "").lower())


def content_signature(text: str) -> str:
    compact = normalize_title(str(text or "")[:800])
    return hashlib.sha1(compact.encode("utf-8")).hexdigest()[:12] if compact else ""


def first_date(value: str) -> str:
    match = re.search(r"(20\d{2})[-年/](\d{1,2})[-月/](\d{1,2})", str(value or ""))
    if not match:
        return ""
    return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"


def first_date_from_values(values: Any) -> str:
    if not isinstance(values, list):
        return ""
    for value in values:
        date = first_date(str(value))
        if date:
            return date
    return ""


def domain_from_url(url: str) -> str:
    match = re.search(r"https?://([^/]+)", str(url or ""), flags=re.I)
    return match.group(1).lower().removeprefix("www.") if match else ""


def canonical_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    parts = urlsplit(value.split("#", 1)[0])
    query_items = [
        (key, val)
        for key, val in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
        and key.lower() not in {"spm", "from", "source", "share", "timestamp"}
    ]
    normalized_path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower().removeprefix("www."), normalized_path, urlencode(query_items), ""))


def source_type(domain: str) -> str:
    priority = source_priority(domain)
    if priority >= 100:
        return "official"
    if priority >= 80:
        return "authoritative_media"
    if priority >= 70:
        return "local_official"
    if priority >= 40:
        return "clue_only"
    return "other"


def unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def invert_for_earlier_date(value: str) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())[:8] or "99999999"
    return "".join(chr(255 - ord(ch)) for ch in digits)
