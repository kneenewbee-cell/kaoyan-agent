from __future__ import annotations

import time
from contextvars import ContextVar
from typing import Any, Callable

UsageCallback = Callable[[dict[str, Any]], None]

_USAGE_CALLBACK: ContextVar[UsageCallback | None] = ContextVar("usage_callback", default=None)


def set_usage_callback(callback: UsageCallback | None):
    return _USAGE_CALLBACK.set(callback)


def reset_usage_callback(token: Any) -> None:
    _USAGE_CALLBACK.reset(token)


def _field(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _usage_tokens(response: Any) -> tuple[int, int, int]:
    usage = _field(response, "usage")
    if usage is None:
        return 0, 0, 0
    prompt_tokens = int(_field(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(_field(usage, "completion_tokens", 0) or 0)
    total_tokens = int(_field(usage, "total_tokens", 0) or 0)
    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens
    return prompt_tokens, completion_tokens, total_tokens


def notify_usage(
    *,
    kind: str,
    name: str,
    model: str | None = None,
    response: Any | None = None,
    started_at: float | None = None,
    ok: bool = True,
    **extra: Any,
) -> dict[str, Any]:
    prompt_tokens, completion_tokens, total_tokens = _usage_tokens(response)
    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2) if started_at is not None else None
    elapsed_seconds = elapsed_ms / 1000 if elapsed_ms else 0.0
    item: dict[str, Any] = {
        "name": name,
        "kind": kind,
        "ok": ok,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }
    if model:
        item["model"] = model
    if elapsed_ms is not None:
        item["latency_ms"] = elapsed_ms
        item["tokens_per_second"] = round(total_tokens / elapsed_seconds, 2) if elapsed_seconds and total_tokens else 0.0
        item["completion_tokens_per_second"] = (
            round(completion_tokens / elapsed_seconds, 2) if elapsed_seconds and completion_tokens else 0.0
        )
    for key, value in extra.items():
        if value is not None:
            item[key] = value

    callback = _USAGE_CALLBACK.get()
    if callback is not None:
        callback(item)
    return item
