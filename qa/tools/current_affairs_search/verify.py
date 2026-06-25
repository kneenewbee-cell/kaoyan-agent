from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from .constants import OFFICIAL_SOURCE_DOMAINS
from .search_api import SearchHit, max_fetch_pages, max_search_workers
from .utils import clean_html, domain_allowed, extract_dates


LOW_VALUE_TITLES = {
    "中华人民共和国司法部",
    "国家能源局",
    "中华人民共和国生态环境部",
    "中国政府网",
}

TERM_STOPWORDS = {
    "2024",
    "2025",
    "2026",
    "2027",
    "4月",
    "5月",
    "6月",
    "近期",
    "最近",
    "政策",
    "文件",
    "新闻",
    "发布",
    "出台",
    "重要",
}


def clean_and_verify_hits(plan: dict[str, Any], hits: list[SearchHit]) -> list[dict[str, Any]]:
    allowed = plan.get("source_groups", {}).get("all_authoritative") or OFFICIAL_SOURCE_DOMAINS
    time_range = plan.get("time", {}).get("time_range") or {}
    from_date = str(time_range.get("from") or "")
    to_date = str(time_range.get("to") or "")

    candidates = [hit for hit in hits if domain_allowed(hit.source_domain, allowed)]
    candidates = rank_candidate_hits(plan, candidates)
    candidates = fetch_candidate_pages(candidates[: max_fetch_pages()])
    cleaned: list[dict[str, Any]] = []
    for hit in candidates:
        text = "\n".join([hit.title, hit.snippet, hit.fetched_text])
        score = relevance_score(plan, hit, text)
        if is_low_relevance_hit(hit, score):
            continue
        dates = extract_dates(text, from_date[:4])
        hit.extracted_dates = dates
        if dates and from_date and to_date and not any(from_date <= item <= to_date for item in dates):
            continue
        cleaned.append(
            {
                "title": hit.title,
                "url": hit.url,
                "snippet": hit.snippet,
                "source_domain": hit.source_domain,
                "query": hit.query,
                "group": hit.group,
                "published_at": hit.published_at,
                "extracted_dates": dates,
                "text_preview": hit.fetched_text[:1200],
                "relevance_score": score,
                "confidence_hint": source_confidence_hint(hit.source_domain),
            }
        )
    return deduplicate_evidence_items(cleaned)


def is_low_relevance_hit(hit: SearchHit, score: int) -> bool:
    title = clean_title(hit.title)
    if title in LOW_VALUE_TITLES and score < 2:
        return True
    if len(title) <= 6 and score < 2:
        return True
    if "首页" in title and score < 2:
        return True
    return score <= 0


def relevance_score(plan: dict[str, Any], hit: SearchHit, text: str) -> int:
    haystack = text.lower()
    terms = relevance_terms(plan, hit)
    score = 0
    for term in terms:
        if term and term.lower() in haystack:
            score += 1
    title = hit.title.lower()
    score += sum(1 for term in terms if term and term.lower() in title)
    return score


def relevance_terms(plan: dict[str, Any], hit: SearchHit) -> list[str]:
    task = plan.get("task", {}) or {}
    values: list[str] = []
    for key in ("topic_terms", "event_or_document_types", "institution_terms"):
        values.extend(str(item).strip() for item in task.get(key) or [])
    values.extend(split_query_terms(hit.query))
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        term = clean_term(value)
        if not term or term in seen:
            continue
        seen.add(term)
        result.append(term)
    return result


def split_query_terms(query: str) -> list[str]:
    cleaned = re.sub(r"\bsite:[a-z0-9.-]+\.[a-z]{2,}\b", " ", str(query or ""), flags=re.I)
    return re.split(r"\s+", cleaned)


def clean_term(value: str) -> str:
    term = str(value or "").strip().strip("，。；;:：、,.!?！？")
    term = re.sub(r"^20\d{2}年?$", "", term)
    if not term or term in TERM_STOPWORDS:
        return ""
    if re.fullmatch(r"\d+月", term):
        return ""
    return term if len(term) >= 2 else ""


def clean_title(title: str) -> str:
    return re.sub(r"\s+", "", str(title or "").strip())


def rank_candidate_hits(plan: dict[str, Any], hits: list[SearchHit]) -> list[SearchHit]:
    allowed = plan.get("source_groups", {}).get("all_authoritative") or OFFICIAL_SOURCE_DOMAINS
    time_range = plan.get("time", {}).get("time_range") or {}
    from_date = str(time_range.get("from") or "")
    to_date = str(time_range.get("to") or "")
    task = plan.get("task", {}) or {}
    terms = [
        *[str(item) for item in task.get("topic_terms") or []],
        *[str(item) for item in task.get("event_or_document_types") or []],
        *[str(item) for item in task.get("institution_terms") or []],
    ]
    group_priority = {
        str(group.get("name") or ""): int(group.get("priority") or 1)
        for group in plan.get("query_groups") or []
        if isinstance(group, dict)
    }

    def score(hit: SearchHit) -> tuple[int, str]:
        text = f"{hit.title} {hit.snippet} {hit.query}".lower()
        domain_score = domain_rank_score(hit.source_domain, allowed)
        term_score = sum(1 for term in terms if str(term).strip().lower() and str(term).strip().lower() in text)
        date_score = 0
        if hit.published_at and from_date <= hit.published_at[:10] <= to_date:
            date_score += 3
        dates = extract_dates(f"{hit.title} {hit.snippet} {hit.published_at or ''}", from_date[:4])
        if any(from_date <= item <= to_date for item in dates):
            date_score += 2
        priority_score = group_priority.get(hit.group, 1)
        return (domain_score + term_score * 3 + date_score + priority_score, hit.title)

    return sorted(hits, key=score, reverse=True)


def domain_rank_score(domain: str, allowed_domains: list[str]) -> int:
    clean = domain.lower().removeprefix("www.")
    for index, allowed in enumerate(allowed_domains):
        if clean == allowed:
            return max(1, 30 - index)
        if clean.endswith("." + allowed):
            if allowed == "gov.cn":
                return max(1, 12 - index)
            return max(1, 20 - index)
    return 0


def source_confidence_hint(domain: str) -> str:
    clean = domain.lower().removeprefix("www.")
    if clean in OFFICIAL_SOURCE_DOMAINS[:8]:
        return "high"
    if any(clean == item for item in OFFICIAL_SOURCE_DOMAINS):
        return "high"
    if clean.endswith(".gov.cn"):
        return "medium"
    if any(clean.endswith("." + item) for item in OFFICIAL_SOURCE_DOMAINS):
        return "medium"
    return "medium"


def deduplicate_evidence_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[tuple[str, ...], dict[str, Any]] = {}
    order: list[tuple[str, ...]] = []
    for item in items:
        key = evidence_dedupe_key(item)
        if key not in deduped:
            copied = dict(item)
            copied["matched_queries"] = unique_list([str(item.get("query") or "")])
            copied["matched_groups"] = unique_list([str(item.get("group") or "")])
            deduped[key] = copied
            order.append(key)
            continue
        merged = merge_duplicate_evidence(deduped[key], item)
        deduped[key] = merged
    return [deduped[key] for key in order]


def evidence_dedupe_key(item: dict[str, Any]) -> tuple[str, ...]:
    url = canonical_url(str(item.get("url") or ""))
    if url:
        return ("url", url)
    domain = str(item.get("source_domain") or "").lower().removeprefix("www.")
    title = clean_title(str(item.get("title") or ""))
    return ("title", domain, title)


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


def merge_duplicate_evidence(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    merged["matched_queries"] = unique_list(
        [*as_list(existing.get("matched_queries")), str(existing.get("query") or ""), str(incoming.get("query") or "")]
    )
    merged["matched_groups"] = unique_list(
        [*as_list(existing.get("matched_groups")), str(existing.get("group") or ""), str(incoming.get("group") or "")]
    )
    merged["extracted_dates"] = unique_list([
        *as_list(existing.get("extracted_dates")),
        *as_list(incoming.get("extracted_dates")),
    ])
    if evidence_quality_score(incoming) > evidence_quality_score(existing):
        for key, value in incoming.items():
            if key not in {"matched_queries", "matched_groups", "extracted_dates"}:
                merged[key] = value
    return merged


def evidence_quality_score(item: dict[str, Any]) -> tuple[float, int]:
    confidence_weight = {"high": 3, "medium": 2, "low": 1}
    confidence = confidence_weight.get(str(item.get("confidence_hint") or "").lower(), 1)
    relevance = float(item.get("relevance_score") or 0)
    preview_len = len(str(item.get("text_preview") or ""))
    return (relevance + confidence, preview_len)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def unique_list(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value is None:
            continue
        key = str(value).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def fetch_candidate_pages(hits: list[SearchHit]) -> list[SearchHit]:
    with ThreadPoolExecutor(max_workers=max_search_workers()) as executor:
        future_map = {executor.submit(fetch_page_text, hit.url): hit for hit in hits}
        for future in as_completed(future_map):
            hit = future_map[future]
            try:
                hit.fetched_text = future.result()
            except Exception:
                hit.fetched_text = ""
    return hits


def fetch_page_text(url: str) -> str:
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
        timeout=15,
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    html = response.text
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    return clean_html(html)[:5000]
