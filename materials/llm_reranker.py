from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from .postprocess.qwen_strategy_client import DEFAULT_BASE_URL, ROOT, _extract_content, _read_dotenv_value
from .schemas import MaterialSearchResult


VISIBLE_DECISIONS = {"primary", "related"}
DEFAULT_MATERIAL_SEARCH_RERANK_MODEL = "qwen3.5-plus-2026-04-20"

MATERIAL_SEARCH_RERANK_SYSTEM_PROMPT = """You judge retrieved study-material chunks for one user query.
Output JSON only.

Task:
- Keep only chunks that can directly answer the query or are useful adjacent context.
- Hide chunks that are off-topic, too generic, or only match accidental substrings.
- Prefer exact subject concepts, formulas, definitions, procedures, examples, and headings that match the user's intent.
- If the query asks for multiple concepts, rank representative chunks that cover different concepts before duplicates.
- Do not add new knowledge. Judge only the supplied candidates.

Output shape:
{
  "results": [
    {
      "chunk_id": "candidate chunk_id",
      "decision": "primary|related|hide",
      "rank": 1,
      "confidence": 0.0,
      "reason": "short Chinese reason"
    }
  ]
}
"""


def _score(result: MaterialSearchResult) -> float:
    metadata = dict(result.metadata or {})
    try:
        return float(metadata.get("rerank_score", result.score))
    except (TypeError, ValueError):
        try:
            return float(result.score)
        except (TypeError, ValueError):
            return 0.0


def _truncate_text(text: str, limit: int) -> str:
    value = str(text or "")
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "\n[TRUNCATED]"


def get_material_search_rerank_model(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "MATERIALS_SEARCH_RERANK_MODEL")
        or os.getenv("MATERIALS_SEARCH_RERANK_MODEL", "").strip()
        or _read_dotenv_value(target_env_path, "QWEN_CLEANING_STRATEGY_MODEL")
        or os.getenv("QWEN_CLEANING_STRATEGY_MODEL", "").strip()
        or DEFAULT_MATERIAL_SEARCH_RERANK_MODEL
    )


def _load_env(env_path: Path | str | None = None) -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(env_path) if env_path else ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass


def _api_key(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "QWEN_API_KEY")
        or _read_dotenv_value(target_env_path, "DASHSCOPE_API_KEY")
        or os.getenv("QWEN_API_KEY", "").strip()
        or os.getenv("DASHSCOPE_API_KEY", "").strip()
    )


def _usage_metrics(response: Any, *, model: str, started_at: float) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0) or prompt_tokens + completion_tokens
    latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
    return {
        "model": model,
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


class MaterialSearchRerankClient:
    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str,
        base_url: str | None = None,
        timeout_seconds: int = 60,
    ) -> None:
        self.model = model or get_material_search_rerank_model()
        self.api_key = api_key
        self.base_url = base_url or os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL)
        self.timeout_seconds = timeout_seconds

    def rerank(self, payload: dict[str, Any]) -> dict[str, Any]:
        return generate_material_search_rerank_with_qwen(
            payload,
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            timeout_seconds=self.timeout_seconds,
        )


def build_material_search_rerank_client_from_env(
    *,
    env_path: Path | str | None = None,
    timeout_seconds: int = 60,
) -> MaterialSearchRerankClient | None:
    _load_env(env_path)
    key = _api_key(env_path)
    if not key:
        return None
    return MaterialSearchRerankClient(
        model=get_material_search_rerank_model(env_path),
        api_key=key,
        base_url=os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout_seconds=timeout_seconds,
    )


def generate_material_search_rerank_with_qwen(
    payload: dict[str, Any],
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = 60,
    usage_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _load_env()
    key = api_key or _api_key()
    if not key:
        raise RuntimeError("Qwen API key is not configured")

    from openai import OpenAI

    selected_model = model or get_material_search_rerank_model()
    client = OpenAI(
        api_key=key,
        base_url=base_url or os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout=timeout_seconds,
        max_retries=0,
    )
    started_at = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=selected_model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": MATERIAL_SEARCH_RERANK_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Judge these retrieved material candidates for the query. Return JSON only.\n\n"
                        + json.dumps(payload, ensure_ascii=False)
                    ),
                },
            ],
        )
        metrics = _usage_metrics(response, model=selected_model, started_at=started_at)
        metrics.update(
            {
                "api_success": True,
                "query": payload.get("query"),
                "candidate_count": payload.get("candidate_count", len(payload.get("candidates") or [])),
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen material search rerank response is not a JSON object")
        return parsed
    except Exception as exc:
        if usage_metrics is not None:
            usage_metrics.update(
                {
                    "model": selected_model,
                    "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "api_success": False,
                    "query": payload.get("query"),
                    "candidate_count": payload.get("candidate_count", len(payload.get("candidates") or [])),
                    "error_type": exc.__class__.__name__,
                }
            )
        raise


def build_candidate_payload(
    query: str,
    results: list[MaterialSearchResult],
    *,
    max_text_chars: int = 900,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for index, result in enumerate(results, start=1):
        metadata = dict(result.metadata or {})
        candidates.append(
            {
                "candidate_id": index,
                "chunk_id": result.chunk_id,
                "material_id": result.material_id,
                "score": round(_score(result), 6),
                "section_title": result.section_title or "",
                "heading_path": list(result.heading_path or []),
                "matched_by": list(metadata.get("matched_by") or []),
                "search_mode": metadata.get("search_mode", ""),
                "rerank": metadata.get("rerank", {}),
                "text": _truncate_text(result.text or "", max_text_chars),
            }
        )
    return {
        "query": query,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "output_schema": {
            "results": [
                {
                    "chunk_id": "string",
                    "decision": "primary|related|hide",
                    "rank": 1,
                    "confidence": 0.0,
                    "reason": "short Chinese reason",
                }
            ]
        },
    }


def _decision_sort_key(item: tuple[MaterialSearchResult, dict[str, Any]]) -> tuple[int, int, float]:
    _result, decision = item
    group = 0 if decision.get("decision") == "primary" else 1
    try:
        rank = int(decision.get("rank") or 999)
    except (TypeError, ValueError):
        rank = 999
    try:
        confidence = float(decision.get("confidence") or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0
    return (group, rank, -confidence)


def apply_llm_decisions(
    results: list[MaterialSearchResult],
    decision_payload: dict[str, Any],
    *,
    top_k: int,
) -> list[MaterialSearchResult]:
    by_chunk_id = {result.chunk_id: result for result in results if result.chunk_id}
    selected: list[tuple[MaterialSearchResult, dict[str, Any]]] = []
    for item in decision_payload.get("results") or []:
        if not isinstance(item, dict):
            continue
        chunk_id = str(item.get("chunk_id") or "")
        decision = str(item.get("decision") or "").strip().lower()
        if decision not in VISIBLE_DECISIONS or chunk_id not in by_chunk_id:
            continue
        selected.append((by_chunk_id[chunk_id], item))

    selected.sort(key=_decision_sort_key)
    output: list[MaterialSearchResult] = []
    for rank, (result, decision) in enumerate(selected[:top_k], start=1):
        metadata = dict(result.metadata or {})
        metadata["base_search_mode"] = metadata.get("search_mode", "")
        metadata["search_mode"] = "llm"
        metadata["llm_rerank"] = {
            "decision": str(decision.get("decision") or "").strip().lower(),
            "rank": decision.get("rank"),
            "confidence": decision.get("confidence"),
            "reason": str(decision.get("reason") or ""),
        }
        result.metadata = metadata
        result.rank = rank
        output.append(result)
    return output
