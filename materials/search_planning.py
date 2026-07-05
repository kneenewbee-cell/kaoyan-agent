from __future__ import annotations

import re
from dataclasses import dataclass

from .indexing.query_processor import process_query


FORMULA_QUERY_RE = re.compile(r"[A-Za-z]\s*(?:\(|\||\\mid|=|\^|_)|\\[A-Za-z]+|[{}]")


@dataclass(frozen=True)
class RetrievalPlan:
    chunk_count: int
    recall_limit: int
    llm_candidate_limit: int
    keyword_top_k: int
    vector_top_k: int
    heading_top_k: int
    formula_top_k: int
    per_intent_top_k: int
    is_multi_intent: bool
    is_formula_query: bool


def _clamp(value: int, *, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def _is_multi_intent_query(query: str) -> bool:
    plan = process_query(query)
    terms = tuple(term for term in (plan.phrase_terms or plan.core_terms or plan.terms) if len(term) > 1)
    if len(terms) >= 3:
        return True
    compact = str(query or "").strip()
    return bool(re.search(r"[\s、,，/]+", compact)) and len(terms) >= 2


def _is_formula_query(query: str) -> bool:
    return bool(FORMULA_QUERY_RE.search(query or ""))


def build_retrieval_plan(
    *,
    chunk_count: int,
    query: str,
    scope: str = "subject",
) -> RetrievalPlan:
    total = max(int(chunk_count or 0), 0)
    multi_intent = _is_multi_intent_query(query)
    formula_query = _is_formula_query(query)

    if multi_intent:
        recall_ratio = 0.10
        llm_ratio = 0.05
    elif formula_query:
        recall_ratio = 0.08
        llm_ratio = 0.04
    else:
        recall_ratio = 0.08
        llm_ratio = 0.03

    recall_max = 40 if scope == "material" else 80
    llm_max = 16 if scope == "material" else 32
    recall_limit = _clamp(round(total * recall_ratio), minimum=12, maximum=recall_max)
    llm_candidate_limit = _clamp(round(total * llm_ratio), minimum=6, maximum=llm_max)

    half_recall = max(1, recall_limit // 2)
    heading_top_k = min(12, max(3, recall_limit // 6))
    formula_top_k = min(12, max(2, recall_limit // 5)) if formula_query else min(6, max(1, recall_limit // 10))
    per_intent_top_k = min(10, max(2, recall_limit // 8))

    return RetrievalPlan(
        chunk_count=total,
        recall_limit=recall_limit,
        llm_candidate_limit=llm_candidate_limit,
        keyword_top_k=half_recall,
        vector_top_k=recall_limit - half_recall,
        heading_top_k=heading_top_k,
        formula_top_k=formula_top_k,
        per_intent_top_k=per_intent_top_k,
        is_multi_intent=multi_intent,
        is_formula_query=formula_query,
    )
