from __future__ import annotations

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv

from ...usage_tracking import notify_usage
from .constants import OFFICIAL_SOURCE_DOMAINS, ROOT
from .utils import clean_html, domain_of, unique_strings


SCOPE_JOB_BUDGETS = {
    "simple": {"min": 2, "target": 3, "max": 4},
    "normal": {"min": 5, "target": 6, "max": 8},
    "broad": {"min": 8, "target": 10, "max": 12},
    "complex": {"min": 12, "target": 12, "max": 20},
}


@dataclass
class SearchHit:
    title: str
    url: str
    snippet: str
    source_domain: str
    query: str
    provider: str
    group: str = ""
    published_at: str | None = None
    fetched_text: str = ""
    extracted_dates: list[str] | None = None


@dataclass
class SearchJob:
    query: str
    domain: str = ""
    group: str = ""
    priority: int = 1

    @property
    def rendered_query(self) -> str:
        if self.domain and "site:" not in self.query:
            return f"site:{self.domain} {self.query}"
        return self.query


def search_provider_name() -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return (os.getenv("NEWS_SEARCH_PROVIDER") or "").strip().lower()


def search_api_key(provider: str) -> str | None:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    specific = {
        "brave": "BRAVE_SEARCH_API_KEY",
        "bing": "BING_SEARCH_API_KEY",
        "tavily": "TAVILY_API_KEY",
    }.get(provider)
    return os.getenv("NEWS_SEARCH_API_KEY") or (os.getenv(specific) if specific else None)


def max_search_workers() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        return max(1, min(8, int(os.getenv("NEWS_SEARCH_MAX_WORKERS", "5"))))
    except ValueError:
        return 5


def max_search_requests() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        value = os.getenv("NEWS_SEARCH_QUERY_BUDGET") or os.getenv("NEWS_SEARCH_MAX_REQUESTS", "12")
        return max(1, min(30, int(value)))
    except ValueError:
        return 12


def max_fallback_search_requests() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        value = os.getenv("NEWS_SEARCH_FALLBACK_QUERY_BUDGET") or os.getenv("NEWS_SEARCH_FALLBACK_MAX_REQUESTS", "6")
        return max(1, min(20, int(value)))
    except ValueError:
        return 6


def search_results_per_query() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        return max(1, min(20, int(os.getenv("NEWS_SEARCH_RESULTS_PER_QUERY", "5"))))
    except ValueError:
        return 5


def max_fetch_pages() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        value = os.getenv("NEWS_SEARCH_FETCH_PAGES") or os.getenv("NEWS_FETCH_MAX_PAGES", "8")
        return max(0, min(20, int(value)))
    except ValueError:
        return 8


def min_evidence_count() -> int:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    try:
        return max(1, min(10, int(os.getenv("NEWS_SEARCH_MIN_EVIDENCE", "3"))))
    except ValueError:
        return 3


def fallback_enabled() -> bool:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    value = (os.getenv("NEWS_SEARCH_ENABLE_FALLBACK", "true") or "").strip().lower()
    return value not in {"0", "false", "no", "off"}


def resolve_job_budget(plan: dict[str, Any], request_limit: int | None = None) -> int:
    if request_limit is not None:
        return max(1, min(30, int(request_limit)))

    search_scope = plan.get("search_scope") or {}
    level = str(search_scope.get("level") or "normal").strip().lower()
    budget_rule = SCOPE_JOB_BUDGETS.get(level, SCOPE_JOB_BUDGETS["normal"])
    suggested = safe_int(search_scope.get("suggested_queries"))
    budget = suggested if suggested else int(budget_rule["target"])
    budget = clamp_int(budget, int(budget_rule["min"]), int(budget_rule["max"]))
    budget = adjust_budget_by_time_range(plan, level, budget)
    return min(budget, max_search_requests())


def adjust_budget_by_time_range(plan: dict[str, Any], level: str, budget: int) -> int:
    days = time_range_days(plan)
    if days <= 0:
        return budget
    if level == "simple" and days <= 7:
        return min(budget, 4)
    if level == "normal" and days >= 90:
        return max(budget, 7)
    if level == "broad" and days >= 90:
        return max(budget, 10)
    if level == "complex":
        return max(budget, 12)
    return budget


def time_range_days(plan: dict[str, Any]) -> int:
    from datetime import date

    time_range = plan.get("time", {}).get("time_range") or {}
    try:
        start = date.fromisoformat(str(time_range.get("from") or ""))
        end = date.fromisoformat(str(time_range.get("to") or ""))
    except ValueError:
        return 0
    return max(0, (end - start).days + 1)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def clamp_int(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def build_search_jobs(plan: dict[str, Any], request_limit: int | None = None) -> list[SearchJob]:
    limit = resolve_job_budget(plan, request_limit=request_limit)
    groups = normalize_query_groups(plan)
    if not groups:
        original = str(plan.get("task", {}).get("original_query") or "").strip()
        if not original:
            return []
        groups = [{"name": "fallback", "domains": [], "queries": [original], "priority": 1, "quota": limit}]

    group_candidates: list[dict[str, Any]] = []
    for group in groups:
        candidates = build_group_candidates(group)
        if candidates:
            group_candidates.append(
                {
                    "name": group["name"],
                    "priority": int(group.get("priority") or 1),
                    "quota": max(1, int(group.get("quota") or limit)),
                    "used": 0,
                    "items": candidates,
                    "cursor": 0,
                }
            )
    group_candidates.sort(key=lambda item: (-item["priority"], item["name"]))

    jobs: list[SearchJob] = []
    seen: set[tuple[str, str]] = set()
    while len(jobs) < limit:
        progressed = False
        for group in group_candidates:
            if len(jobs) >= limit:
                break
            if group["used"] >= group["quota"]:
                continue
            items = group["items"]
            if group["cursor"] >= len(items):
                continue
            job = items[group["cursor"]]
            group["cursor"] += 1
            key = (job.query, job.domain)
            if key in seen:
                continue
            seen.add(key)
            jobs.append(job)
            group["used"] += 1
            progressed = True
        if not progressed:
            break
    return jobs


def normalize_query_groups(plan: dict[str, Any]) -> list[dict[str, Any]]:
    fallback_domains = plan.get("source_groups", {}).get("all_authoritative") or OFFICIAL_SOURCE_DOMAINS
    groups: list[dict[str, Any]] = []
    for index, group in enumerate(plan.get("query_groups") or []):
        if not isinstance(group, dict):
            continue
        queries = unique_strings([str(query or "").strip() for query in group.get("queries") or []])
        if not queries:
            continue
        domains = unique_strings([str(domain or "").strip() for domain in group.get("domains") or []])
        if not domains:
            domains = list(fallback_domains[:4])
        groups.append(
            {
                "name": str(group.get("name") or f"group_{index + 1}"),
                "queries": queries,
                "domains": domains,
                "priority": int(group.get("priority") or max(1, 5 - index)),
                "quota": int(group.get("quota") or 4),
            }
        )
    return groups


def build_group_candidates(group: dict[str, Any]) -> list[SearchJob]:
    queries = list(group.get("queries") or [])
    domains = list(group.get("domains") or [])
    name = str(group.get("name") or "")
    priority = int(group.get("priority") or 1)
    candidates: list[SearchJob] = []
    plain_queries: list[str] = []
    for query in queries:
        cleaned_query, query_domain = split_query_domain(str(query))
        if query_domain:
            candidates.append(SearchJob(query=cleaned_query, domain=query_domain, group=name, priority=priority))
        elif cleaned_query:
            plain_queries.append(cleaned_query)
    if not domains:
        for query in plain_queries:
            candidates.append(SearchJob(query=query, domain="", group=name, priority=priority))
        return candidates

    seen_pairs: set[tuple[str, str]] = set()
    for query_index, query in enumerate(plain_queries):
        domain = domains[query_index % len(domains)]
        seen_pairs.add((query, domain))
        candidates.append(SearchJob(query=query, domain=domain, group=name, priority=priority))
    for offset in range(1, len(domains)):
        for query_index, query in enumerate(plain_queries):
            domain = domains[(query_index + offset) % len(domains)]
            if (query, domain) in seen_pairs:
                continue
            seen_pairs.add((query, domain))
            candidates.append(SearchJob(query=query, domain=domain, group=name, priority=priority))
    return candidates


def split_query_domain(query: str) -> tuple[str, str]:
    text = str(query or "").strip()
    site_match = re.search(r"\bsite:([a-z0-9.-]+\.[a-z]{2,})\b", text, flags=re.I)
    if site_match:
        domain = site_match.group(1).lower().removeprefix("www.")
        cleaned = re.sub(r"\bsite:[a-z0-9.-]+\.[a-z]{2,}\b", " ", text, flags=re.I)
        return clean_query_text(cleaned), domain

    bare_match = re.search(r"\b([a-z0-9-]+(?:\.[a-z0-9-]+)+)\b", text, flags=re.I)
    if bare_match:
        domain = bare_match.group(1).lower().removeprefix("www.")
        if "." in domain:
            cleaned = text.replace(bare_match.group(1), " ")
            return clean_query_text(cleaned), domain
    return clean_query_text(text), ""


def clean_query_text(query: str) -> str:
    return " ".join(str(query or "").split())


def build_api_request_previews(
    plan: dict[str, Any],
    provider: str | None = None,
    request_limit: int | None = None,
) -> list[dict[str, Any]]:
    selected_provider = (provider or search_provider_name() or "tavily").strip().lower()
    return [
        build_api_request_preview(selected_provider, job, plan)
        for job in build_search_jobs(plan, request_limit=request_limit)
    ]


def build_api_request_preview(provider: str, job: SearchJob, plan: dict[str, Any]) -> dict[str, Any]:
    if provider == "tavily":
        payload = build_tavily_payload("<redacted>", job, plan)
        return {
            "provider": "tavily",
            "method": "POST",
            "url": "https://api.tavily.com/search",
            "group": job.group,
            "priority": job.priority,
            "domain": job.domain,
            "payload": payload,
        }
    if provider == "brave":
        return {
            "provider": "brave",
            "method": "GET",
            "url": "https://api.search.brave.com/res/v1/web/search",
            "group": job.group,
            "priority": job.priority,
            "domain": job.domain,
            "params": {
                "q": job.rendered_query,
                "count": search_results_per_query(),
                "country": "CN",
                "search_lang": "zh-hans",
            },
        }
    if provider == "bing":
        return {
            "provider": "bing",
            "method": "GET",
            "url": "https://api.bing.microsoft.com/v7.0/search",
            "group": job.group,
            "priority": job.priority,
            "domain": job.domain,
            "params": {
                "q": job.rendered_query,
                "count": search_results_per_query(),
                "mkt": "zh-CN",
                "responseFilter": "Webpages",
            },
        }
    return {
        "provider": provider,
        "method": "",
        "url": "",
        "group": job.group,
        "priority": job.priority,
        "domain": job.domain,
        "query": job.rendered_query,
    }


def execute_news_searches(plan: dict[str, Any], request_limit: int | None = None) -> list[SearchHit]:
    provider = search_provider_name()
    if not provider:
        raise RuntimeError(
            "Please configure NEWS_SEARCH_PROVIDER=brave|bing|tavily and NEWS_SEARCH_API_KEY "
            "or the provider-specific API key."
        )
    api_key = search_api_key(provider)
    if not api_key:
        raise RuntimeError(f"Please configure NEWS_SEARCH_API_KEY or the provider-specific key for {provider}.")

    jobs = build_search_jobs(plan, request_limit=request_limit)
    started = time.perf_counter()
    hits: list[SearchHit] = []
    with ThreadPoolExecutor(max_workers=max_search_workers()) as executor:
        future_map = {executor.submit(search_one, provider, api_key, job, plan): job for job in jobs}
        for future in as_completed(future_map):
            try:
                hits.extend(future.result())
            except Exception:
                continue
    notify_usage(
        kind="external_tool_api",
        name=f"tool_api:get_current_affairs:search:{provider}",
        model=provider,
        started_at=started,
        tool_name="get_current_affairs",
        provider=provider,
        query_count=len(jobs),
        result_count=len(hits),
    )
    return dedupe_hits(hits)


def search_one(provider: str, api_key: str, job: SearchJob, plan: dict[str, Any]) -> list[SearchHit]:
    if provider == "brave":
        return search_brave(api_key, job)
    if provider == "bing":
        return search_bing(api_key, job)
    if provider == "tavily":
        return search_tavily(api_key, job, plan)
    raise RuntimeError(f"Unsupported NEWS_SEARCH_PROVIDER={provider}; use brave, bing, or tavily.")


def search_brave(api_key: str, job: SearchJob) -> list[SearchHit]:
    query = job.rendered_query
    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
        params={"q": query, "count": search_results_per_query(), "country": "CN", "search_lang": "zh-hans"},
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("web", {}).get("results") or []
    return [
        SearchHit(
            title=str(item.get("title") or ""),
            url=str(item.get("url") or ""),
            snippet=clean_html(str(item.get("description") or "")),
            source_domain=domain_of(str(item.get("url") or "")),
            query=query,
            provider="brave",
            group=job.group,
            published_at=str(item.get("page_age") or "") or None,
        )
        for item in results
        if item.get("url")
    ]


def search_bing(api_key: str, job: SearchJob) -> list[SearchHit]:
    query = job.rendered_query
    response = requests.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key": api_key},
        params={"q": query, "count": search_results_per_query(), "mkt": "zh-CN", "responseFilter": "Webpages"},
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("webPages", {}).get("value") or []
    return [
        SearchHit(
            title=str(item.get("name") or ""),
            url=str(item.get("url") or ""),
            snippet=clean_html(str(item.get("snippet") or "")),
            source_domain=domain_of(str(item.get("url") or "")),
            query=query,
            provider="bing",
            group=job.group,
            published_at=str(item.get("dateLastCrawled") or "")[:10] or None,
        )
        for item in results
        if item.get("url")
    ]


def build_tavily_payload(api_key: str, job: SearchJob, plan: dict[str, Any]) -> dict[str, Any]:
    time_range = plan.get("time", {}).get("time_range") or {}
    payload: dict[str, Any] = {
        "api_key": api_key,
        "query": job.query,
        "search_depth": "basic",
        "topic": "news",
        "max_results": search_results_per_query(),
        "include_answer": False,
        "include_raw_content": False,
    }
    if job.domain:
        payload["include_domains"] = [job.domain]
    if time_range.get("from"):
        payload["start_date"] = str(time_range.get("from"))
    if time_range.get("to"):
        payload["end_date"] = str(time_range.get("to"))
    return payload


def search_tavily(api_key: str, job: SearchJob, plan: dict[str, Any]) -> list[SearchHit]:
    response = requests.post(
        "https://api.tavily.com/search",
        json=build_tavily_payload(api_key, job, plan),
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("results") or []
    return [
        SearchHit(
            title=str(item.get("title") or ""),
            url=str(item.get("url") or ""),
            snippet=clean_html(str(item.get("content") or "")),
            source_domain=domain_of(str(item.get("url") or "")),
            query=job.rendered_query,
            provider="tavily",
            group=job.group,
            published_at=str(item.get("published_date") or "")[:10] or None,
        )
        for item in results
        if item.get("url")
    ]


def dedupe_hits(hits: list[SearchHit]) -> list[SearchHit]:
    result: list[SearchHit] = []
    seen_urls: set[str] = set()
    seen_title_domain: set[tuple[str, str]] = set()
    for hit in hits:
        url_key = hit.url.split("#", 1)[0].rstrip("/")
        if url_key in seen_urls:
            continue
        title_key = normalize_title(hit.title)
        title_domain_key = (title_key, hit.source_domain)
        if title_key and title_domain_key in seen_title_domain:
            continue
        seen_urls.add(url_key)
        if title_key:
            seen_title_domain.add(title_domain_key)
        result.append(hit)
    return result


def normalize_title(title: str) -> str:
    return " ".join(str(title or "").lower().split())
