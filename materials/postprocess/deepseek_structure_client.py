"""DeepSeek client for local exercise-structure boundary judgement."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from .qwen_strategy_client import ROOT, _extract_content, _read_dotenv_value


DEFAULT_DEEPSEEK_STRUCTURE_MODEL = "deepseek-v4-flash"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_TIMEOUT_SECONDS = 90

BOUNDARY_SYSTEM_PROMPT = """You judge one local exercise problem-boundary candidate.
Output JSON only.

Task:
- Decide whether a missing problem was absorbed into the previous problem range.
- Do not rewrite the document.
- Do not invent content not present in candidate_lines.
- Return a split only when the local lines clearly contain the missing problem start.

Rules:
- Do not split on A/B/C/D option lines.
- Do not split on formula numbers such as (1.1).
- Do not split on sub-question markers such as (I), (II), Ⅰ, Ⅱ.
- If unsure, return decision="no_split" with confidence below 0.8.

Output shape:
{
  "decision": "split_previous_problem|no_split",
  "target_problem_index": 0,
  "start_line": null,
  "end_line": null,
  "confidence": 0.0,
  "title": "",
  "reason_codes": []
}
"""


def _load_env(env_path: Path | str | None = None) -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(env_path) if env_path else ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass


def get_deepseek_structure_model(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "MATERIALS_STRUCTURE_REPAIR_MODEL")
        or os.getenv("MATERIALS_STRUCTURE_REPAIR_MODEL", "").strip()
        or DEFAULT_DEEPSEEK_STRUCTURE_MODEL
    )


def _api_key(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "MATERIALS_STRUCTURE_REPAIR_API_KEY")
        or _read_dotenv_value(target_env_path, "DEEPSEEK_API_KEY")
        or os.getenv("MATERIALS_STRUCTURE_REPAIR_API_KEY", "").strip()
        or os.getenv("DEEPSEEK_API_KEY", "").strip()
    )


def _base_url(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "MATERIALS_STRUCTURE_REPAIR_BASE_URL")
        or _read_dotenv_value(target_env_path, "DEEPSEEK_BASE_URL")
        or os.getenv("MATERIALS_STRUCTURE_REPAIR_BASE_URL", "").strip()
        or os.getenv("DEEPSEEK_BASE_URL", "").strip()
        or DEFAULT_DEEPSEEK_BASE_URL
    )


def _usage_metrics(response: Any, *, model: str, started_at: float) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0) or prompt_tokens + completion_tokens
    return {
        "model": model,
        "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


class DeepSeekStructureRepairClient:
    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str,
        base_url: str | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.model = model or DEFAULT_DEEPSEEK_STRUCTURE_MODEL
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_DEEPSEEK_BASE_URL
        self.timeout_seconds = timeout_seconds
        self.last_usage: dict[str, Any] = {}

    def judge_problem_boundary(self, payload: dict[str, Any]) -> dict[str, Any]:
        usage: dict[str, Any] = {}
        result = generate_problem_boundary_judgement_with_deepseek(
            payload,
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            timeout_seconds=self.timeout_seconds,
            usage_metrics=usage,
        )
        self.last_usage = usage
        return result


def build_deepseek_structure_repair_client_from_env(
    *,
    env_path: Path | str | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> DeepSeekStructureRepairClient | None:
    _load_env(env_path)
    key = _api_key(env_path)
    if not key:
        return None
    return DeepSeekStructureRepairClient(
        model=get_deepseek_structure_model(env_path),
        api_key=key,
        base_url=_base_url(env_path),
        timeout_seconds=timeout_seconds,
    )


def generate_problem_boundary_judgement_with_deepseek(
    payload: dict[str, Any],
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    usage_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _load_env()
    key = api_key or _api_key()
    if not key:
        raise RuntimeError("DeepSeek API key is not configured")

    from openai import OpenAI

    selected_model = model or get_deepseek_structure_model()
    client = OpenAI(
        api_key=key,
        base_url=base_url or _base_url(),
        timeout=timeout_seconds,
        max_retries=0,
    )
    started_at = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=selected_model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"thinking": {"type": "disabled"}},
            messages=[
                {"role": "system", "content": BOUNDARY_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Judge this local exercise boundary candidate. Return JSON only.\n\n"
                        + json.dumps(payload, ensure_ascii=False)
                    ),
                },
            ],
        )
        metrics = _usage_metrics(response, model=selected_model, started_at=started_at)
        metrics.update(
            {
                "api_success": True,
                "target_missing_index": payload.get("target_missing_index"),
                "candidate_type": payload.get("candidate_type"),
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        parsed = json.loads(_extract_content(response).strip())
        if not isinstance(parsed, dict):
            raise ValueError("DeepSeek boundary judgement response is not a JSON object")
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
                    "target_missing_index": payload.get("target_missing_index"),
                    "candidate_type": payload.get("candidate_type"),
                    "error_type": exc.__class__.__name__,
                }
            )
        raise
