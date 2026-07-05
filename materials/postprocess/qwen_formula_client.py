"""Qwen client for residual formula repair variants."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from .qwen_strategy_client import DEFAULT_BASE_URL, ROOT, _extract_content, _read_dotenv_value


DEFAULT_QWEN_FORMULA_MODEL = "qwen3.5-plus-2026-04-20"
DEFAULT_QWEN_MAX_ATTEMPTS = 3
RETRYABLE_QWEN_ERROR_TYPES = {
    "APITimeoutError",
    "APIConnectionError",
    "RateLimitError",
    "InternalServerError",
}

FORMULA_VARIANTS_SYSTEM_PROMPT = """You repair one broken LaTeX formula extracted from parsed Markdown.
Output JSON only.

Rules:
- Return exactly one JSON object.
- Produce exactly three direct replacement formulas in variants.
- Each variant.formula must be only LaTeX math content, without Markdown delimiters.
- Do not include prose around the formula.
- Prefer formulas that both render and preserve the likely math meaning from context.
- If the original is noisy, use the surrounding line/context to infer the most likely formula.

Output shape:
{
  "formula_id": "...",
  "variants": [
    {
      "formula": "...",
      "confidence": 0.0,
      "reason": "short reason"
    }
  ]
}
"""

HEADING_REVIEW_SYSTEM_PROMPT = """You review a cleaned Markdown heading tree.
Output JSON only.

Rules:
- Do not rewrite the full document.
- Do not invent missing source content.
- Review heading_tree and heading_events from local dynamic-stack extraction.
- Report suspicious level jumps, body text recognized as headings, repeated headings, empty sections, and structure that may hurt chunk/search.
- If no clear issue exists, return quality="ok".

Output shape:
{
  "quality": "ok|warning|bad",
  "issues": [],
  "summary": "short summary"
}
"""


def get_qwen_formula_model(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "QWEN_FORMULA_REPAIR_MODEL")
        or os.getenv("QWEN_FORMULA_REPAIR_MODEL", "").strip()
        or _read_dotenv_value(target_env_path, "QWEN_CLEANING_STRATEGY_MODEL")
        or os.getenv("QWEN_CLEANING_STRATEGY_MODEL", "").strip()
        or DEFAULT_QWEN_FORMULA_MODEL
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


def _is_retryable_qwen_error(exc: Exception) -> bool:
    return exc.__class__.__name__ in RETRYABLE_QWEN_ERROR_TYPES


def _create_chat_completion_with_retries(completions: Any, **kwargs: Any) -> Any:
    for attempt in range(1, DEFAULT_QWEN_MAX_ATTEMPTS + 1):
        try:
            return completions.create(**kwargs)
        except Exception as exc:
            if attempt >= DEFAULT_QWEN_MAX_ATTEMPTS or not _is_retryable_qwen_error(exc):
                raise
            time.sleep(float(attempt))


class QwenFormulaRepairClient:
    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str,
        base_url: str | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.model = model or get_qwen_formula_model()
        self.api_key = api_key
        self.base_url = base_url or os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL)
        self.timeout_seconds = timeout_seconds

    def repair_formula_variants(self, payload: dict[str, Any]) -> dict[str, Any]:
        return generate_formula_variants_with_qwen(
            payload,
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            timeout_seconds=self.timeout_seconds,
        )

    def review_headings(self, payload: dict[str, Any]) -> dict[str, Any]:
        return generate_heading_review_with_qwen(
            payload,
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            timeout_seconds=self.timeout_seconds,
        )


def build_qwen_formula_repair_client_from_env(
    *,
    env_path: Path | str | None = None,
    timeout_seconds: int = 120,
) -> QwenFormulaRepairClient | None:
    _load_env(env_path)
    key = _api_key(env_path)
    if not key:
        return None
    return QwenFormulaRepairClient(
        model=get_qwen_formula_model(env_path),
        api_key=key,
        base_url=os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout_seconds=timeout_seconds,
    )


def generate_formula_variants_with_qwen(
    payload: dict[str, Any],
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = 120,
    usage_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _load_env()
    key = api_key or _api_key()
    if not key:
        raise RuntimeError("Qwen API key is not configured")

    from openai import OpenAI

    selected_model = model or get_qwen_formula_model()
    client = OpenAI(
        api_key=key,
        base_url=base_url or os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout=timeout_seconds,
        max_retries=0,
    )
    started_at = time.perf_counter()
    try:
        response = _create_chat_completion_with_retries(
            client.chat.completions,
            model=selected_model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": FORMULA_VARIANTS_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Repair this formula payload with three direct formula variants. Return JSON only.\n\n"
                        + json.dumps(payload, ensure_ascii=False)
                    ),
                },
            ],
        )
        metrics = _usage_metrics(response, model=selected_model, started_at=started_at)
        metrics.update(
            {
                "api_success": True,
                "formula_id": payload.get("formula_id"),
                "line_start": payload.get("line_start"),
                "mode": "direct_variants",
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen formula variants response is not a JSON object")
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
                    "formula_id": payload.get("formula_id"),
                    "line_start": payload.get("line_start"),
                    "mode": "direct_variants",
                    "error_type": exc.__class__.__name__,
                }
            )
        raise


def generate_heading_review_with_qwen(
    payload: dict[str, Any],
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = 120,
    usage_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _load_env()
    key = api_key or _api_key()
    if not key:
        raise RuntimeError("Qwen API key is not configured")

    from openai import OpenAI

    selected_model = model or get_qwen_formula_model()
    client = OpenAI(
        api_key=key,
        base_url=base_url or os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout=timeout_seconds,
        max_retries=0,
    )
    started_at = time.perf_counter()
    try:
        response = _create_chat_completion_with_retries(
            client.chat.completions,
            model=selected_model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": HEADING_REVIEW_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Review this heading context. Return JSON only.\n\n"
                        + json.dumps(payload, ensure_ascii=False)
                    ),
                },
            ],
        )
        metrics = _usage_metrics(response, model=selected_model, started_at=started_at)
        metrics.update(
            {
                "api_success": True,
                "heading_count": payload.get("heading_context", {}).get("heading_count"),
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen heading review response is not a JSON object")
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
                    "heading_count": payload.get("heading_context", {}).get("heading_count"),
                    "error_type": exc.__class__.__name__,
                }
            )
        raise
