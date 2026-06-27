from __future__ import annotations

import json
from collections import Counter, defaultdict
from math import log
from pathlib import Path
from typing import Any

from ..schemas import Chunk
from .query_processor import TOKENIZER_VERSION, process_query, tokenize_document, tokenize_query


TERM_CONTRIBUTION_CAP = 8.0
PHRASE_BONUS_CAP = 0.8
COVERAGE_BONUS_CAP = 0.6


def tokenize(text: str, *, drop_function_words: bool = True) -> list[str]:
    return tokenize_document(text, drop_function_words=drop_function_words)


def build_search_index(chunks: list[Chunk]) -> dict[str, Any]:
    postings: dict[str, dict[str, int]] = defaultdict(dict)
    texts: dict[str, str] = {}
    chunk_lengths: dict[str, int] = {}

    for chunk in chunks:
        terms = tokenize(chunk.text)
        term_counts = Counter(terms)
        texts[chunk.chunk_id] = chunk.text[:240]
        chunk_lengths[chunk.chunk_id] = len(terms)
        for term, frequency in term_counts.items():
            postings[term][chunk.chunk_id] = frequency

    avg_chunk_length = (
        sum(chunk_lengths.values()) / len(chunk_lengths) if chunk_lengths else 0.0
    )

    return {
        "tokenizer": TOKENIZER_VERSION,
        "chunk_count": len(chunks),
        "texts": texts,
        "postings": {term: docs for term, docs in postings.items()},
        "chunk_lengths": chunk_lengths,
        "avg_chunk_length": avg_chunk_length,
    }


def save_search_index(index_data: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_search_index(index_path: Path) -> dict[str, Any]:
    return json.loads(index_path.read_text(encoding="utf-8"))


def search_in_index(
    query: str,
    index_data: dict[str, Any],
    chunks: list[Chunk],
    top_k: int = 5,
) -> list[tuple[Chunk, float]]:
    query_plan = process_query(query)
    query_terms = list(query_plan.terms)
    if not query_terms:
        return []

    postings: dict[str, dict[str, int]] = index_data.get("postings", {})
    chunk_lengths: dict[str, int] = index_data.get("chunk_lengths", {})
    avg_chunk_length = float(index_data.get("avg_chunk_length") or 0.0)
    total_chunks = int(index_data.get("chunk_count") or 0)
    chunk_map = {chunk.chunk_id: chunk for chunk in chunks}

    scores: dict[str, float] = defaultdict(float)
    matched_terms: dict[str, set[str]] = defaultdict(set)
    k1 = 1.5
    b = 0.75

    for term in query_terms:
        weight = query_plan.term_weights.get(term, 1.0)
        if weight <= 0:
            continue
        docs = postings.get(term)
        if not docs:
            continue
        doc_freq = len(docs)
        idf = log(1 + (total_chunks - doc_freq + 0.5) / (doc_freq + 0.5))
        for chunk_id, term_freq in docs.items():
            doc_len = max(chunk_lengths.get(chunk_id, 0), 1)
            norm = term_freq + k1 * (1 - b + b * (doc_len / avg_chunk_length if avg_chunk_length else 1.0))
            term_score = weight * idf * ((term_freq * (k1 + 1)) / norm)
            scores[chunk_id] += min(term_score, TERM_CONTRIBUTION_CAP)
            matched_terms[chunk_id].add(term)

    if not scores:
        return []

    results: list[tuple[Chunk, float]] = []
    core_terms = set(query_plan.core_terms or query_terms)
    phrase_terms = set(query_plan.phrase_terms)
    for chunk_id, score in scores.items():
        chunk = chunk_map.get(chunk_id)
        if chunk is None:
            continue
        matched = matched_terms[chunk_id]
        phrase_matched = bool(phrase_terms & matched) or any(term in chunk.text for term in phrase_terms)
        if phrase_terms and not phrase_matched:
            continue
        covered_core = len(core_terms & matched)
        coverage_ratio = covered_core / len(core_terms) if core_terms else 0.0
        coverage_bonus = min(COVERAGE_BONUS_CAP, 0.15 * score * coverage_ratio)
        phrase_bonus = min(PHRASE_BONUS_CAP, 0.12 * score + 0.2) if phrase_matched else 0.0
        results.append((chunk, score + coverage_bonus + phrase_bonus))

    results.sort(key=lambda item: item[1], reverse=True)
    return results[:top_k]
