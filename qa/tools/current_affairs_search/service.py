from __future__ import annotations

from copy import deepcopy
from typing import Any

from .planner import plan_current_affairs_search
from .search_api import (
    build_api_request_previews,
    execute_news_searches,
    fallback_enabled,
    max_fallback_search_requests,
    min_evidence_count,
)
from .time_utils import beijing_time_info
from .trace import write_search_trace
from .utils import unique_strings
from .verify import clean_and_verify_hits, deduplicate_evidence_items
from ..current_affairs_store import CurrentAffairsStore, ingest_verified_evidence
from ..current_affairs_store.search import search_current_affairs_store as search_current_affairs_store_impl


def call_current_affairs_search(user_query: str) -> dict[str, Any]:
    current_time = beijing_time_info()
    planner_query = str(user_query or "").strip()
    display_query = planner_query
    plan = plan_current_affairs_search(planner_query, current_time)
    trace_record: dict[str, Any] = {
        "dry_run": False,
        "current_time": current_time,
        "user_query": display_query,
        "tool_query": user_query,
        "planner_query": planner_query,
        "plan": plan,
        "jobs": build_api_request_previews(plan),
        "fallback": None,
    }

    hits = execute_news_searches(plan)
    evidence = deduplicate_evidence_items(clean_and_verify_hits(plan, hits))
    fallback_plan: dict[str, Any] | None = None
    if fallback_enabled() and len(evidence) < min_evidence_count():
        fallback_plan = build_fallback_plan(plan)
        fallback_hits = execute_news_searches(fallback_plan, request_limit=max_fallback_search_requests())
        fallback_evidence = deduplicate_evidence_items(clean_and_verify_hits(fallback_plan, fallback_hits))
        evidence = merge_evidence(evidence, fallback_evidence)
        trace_record["fallback"] = {
            "plan": fallback_plan,
            "jobs": build_api_request_previews(fallback_plan, request_limit=max_fallback_search_requests()),
            "evidence_count": len(fallback_evidence),
        }

    if evidence:
        evidence = ingest_verified_evidence(evidence, store=CurrentAffairsStore())

    trace_record["evidence"] = summarize_evidence_for_trace(evidence)
    write_search_trace(trace_record)

    return build_current_affairs_evidence_result(
        display_query,
        current_time,
        fallback_plan or plan,
        evidence,
        fallback_used=fallback_plan is not None,
    )


def preview_current_affairs_search(
    user_query: str,
    provider: str = "tavily",
    request_limit: int | None = None,
) -> dict[str, Any]:
    current_time = beijing_time_info()
    plan = plan_current_affairs_search(user_query, current_time)
    record = {
        "dry_run": True,
        "current_time": current_time,
        "user_query": user_query,
        "plan": plan,
        "jobs": build_api_request_previews(plan, provider=provider, request_limit=request_limit),
    }
    write_search_trace(record)
    return record


def search_current_affairs_store(args: dict[str, Any]) -> dict[str, Any]:
    return search_current_affairs_store_impl(args, store=CurrentAffairsStore())


def build_fallback_plan(plan: dict[str, Any]) -> dict[str, Any]:
    fallback_plan = deepcopy(plan)
    task = fallback_plan.get("task", {}) or {}
    time_range = fallback_plan.get("time", {}).get("time_range") or {}
    year = str(time_range.get("from") or time_range.get("to") or "")[:4]
    if year:
        fallback_plan.setdefault("time", {}).setdefault("time_range", {})
        fallback_plan["time"]["time_range"]["from"] = f"{year}-01-01"

    source_groups = fallback_plan.get("source_groups", {}) or {}
    fallback_domains = unique_strings(
        list(source_groups.get("official") or [])
        + list(source_groups.get("authoritative_media") or [])
        + list(source_groups.get("all_authoritative") or [])
    )
    if not fallback_domains:
        fallback_domains = ["gov.cn", "news.cn", "people.com.cn", "cctv.com"]

    fallback_plan["query_groups"] = [
        {
            "name": "low_recall_broadened",
            "domains": fallback_domains[:8],
            "priority": 3,
            "quota": max_fallback_search_requests(),
            "queries": build_fallback_queries(task, year),
        }
    ]
    fallback_plan.setdefault("warnings", [])
    fallback_plan["warnings"].append("低召回补搜：已放宽域名、时间或机构词。")
    return fallback_plan


def build_fallback_queries(task: dict[str, Any], year: str) -> list[str]:
    original = str(task.get("original_query") or "").strip()
    topic_terms = [str(item).strip() for item in task.get("topic_terms") or [] if str(item).strip()]
    event_types = [str(item).strip() for item in task.get("event_or_document_types") or [] if str(item).strip()]
    institution_terms = [str(item).strip() for item in task.get("institution_terms") or [] if str(item).strip()]
    topic_text = " ".join(topic_terms[:4]) or original
    type_text = " ".join(event_types[:4])
    institution_text = " ".join(institution_terms[:3])
    prefix = year or ""
    queries = [
        " ".join(item for item in [prefix, topic_text, type_text] if item).strip(),
        " ".join(item for item in [prefix, topic_text, "权威发布"] if item).strip(),
        " ".join(item for item in [prefix, institution_text, topic_text] if item).strip(),
        original,
    ]
    if any(("部" in item or "委" in item or "局" in item) for item in institution_terms):
        queries.append(" ".join(item for item in [prefix, "国务院", topic_text, type_text] if item).strip())
    return unique_strings([query for query in queries if query])


def merge_evidence(primary: list[dict[str, Any]], fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return deduplicate_evidence_items([*primary, *fallback])


def build_current_affairs_evidence_result(
    query: str,
    current_time: dict[str, str],
    plan: dict[str, Any],
    evidence: list[dict[str, Any]],
    *,
    fallback_used: bool = False,
) -> dict[str, Any]:
    time_range = plan.get("time", {}).get("time_range") or {}
    warnings = list(plan.get("warnings") or [])
    if fallback_used:
        warnings.append("初次检索证据不足，已执行一次放宽条件补搜。")
    if not evidence:
        warnings.append("当前检索结果不足以确认。")
    return {
        "type": "current_affairs_evidence",
        "query": query,
        "current_time": current_time,
        "task": plan.get("task") or {},
        "search_scope": plan.get("search_scope") or {},
        "time_range": {
            "from": time_range.get("from"),
            "to": time_range.get("to"),
            "expression": plan.get("time", {}).get("expression"),
        },
        "source_groups": plan.get("source_groups") or {},
        "items": evidence,
        "warnings": unique_strings([str(item) for item in warnings if str(item).strip()]),
    }


def summarize_evidence_for_trace(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "title": item.get("title"),
            "url": item.get("url"),
            "source_domain": item.get("source_domain"),
            "query": item.get("query"),
            "group": item.get("group"),
            "published_at": item.get("published_at"),
            "extracted_dates": item.get("extracted_dates"),
            "event_id": item.get("event_id"),
            "source_doc_id": item.get("source_doc_id"),
            "primary_source_doc_id": item.get("primary_source_doc_id"),
        }
        for item in evidence
    ]
