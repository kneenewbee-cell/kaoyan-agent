from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .pipeline_logger import PIPELINE_LOG_DIR, now_utc_iso, sanitize_for_log


SEARCH_LOG_EVENT = "material_search"
DEFAULT_PREVIEW_CHARS = 240
_LOG_LOCK = threading.Lock()


def search_log_enabled() -> bool:
    raw = os.getenv("MATERIALS_SEARCH_LOG_ENABLED", "1").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def material_search_log_dir() -> Path:
    configured = os.getenv("MATERIALS_SEARCH_LOG_DIR")
    return Path(configured) if configured else PIPELINE_LOG_DIR


def material_search_log_path() -> Path:
    return material_search_log_dir() / f"material_search_{datetime.now().date().isoformat()}.jsonl"


def _safe_float(value: Any) -> float | Any:
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return value


def _text_preview(text: Any, limit: int = DEFAULT_PREVIEW_CHARS) -> str:
    value = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    value = "\n".join(line.strip() for line in value.splitlines() if line.strip())
    if len(value) <= limit:
        return value
    return value[:limit] + f"...[truncated {len(value) - limit} chars]"


def _result_summary(result: Any) -> dict[str, Any]:
    metadata = getattr(result, "metadata", {}) or {}
    if not isinstance(metadata, dict):
        metadata = {}

    return {
        "rank": getattr(result, "rank", None),
        "material_id": getattr(result, "material_id", ""),
        "user_id": getattr(result, "user_id", ""),
        "chunk_id": getattr(result, "chunk_id", ""),
        "score": _safe_float(getattr(result, "score", None)),
        "section_title": getattr(result, "section_title", None),
        "heading_path": getattr(result, "heading_path", []) or [],
        "source_markdown_path": getattr(result, "source_markdown_path", None),
        "asset_paths": getattr(result, "asset_paths", []) or [],
        "original_filename": metadata.get("original_filename", ""),
        "subject": metadata.get("subject", "unknown"),
        "material_type": metadata.get("material_type", "unknown"),
        "search_mode": metadata.get("search_mode", ""),
        "matched_by": metadata.get("matched_by", []),
        "source_type": metadata.get("source_type", ""),
        "table_id": metadata.get("table_id", ""),
        "table_row_index": metadata.get("table_row_index", ""),
        "page": metadata.get("page", ""),
        "distance": _safe_float(metadata.get("distance")),
        "text_preview": _text_preview(getattr(result, "text", "")),
    }


def write_material_search_log(
    *,
    user_id: str,
    query: str,
    mode: str,
    top_k: int,
    filters: dict[str, Any] | None,
    results: Iterable[Any],
    elapsed_ms: float | None = None,
    error: str | None = None,
) -> Path | None:
    if not search_log_enabled():
        return None

    result_list = list(results)
    payload = {
        "time": now_utc_iso(),
        "event": SEARCH_LOG_EVENT,
        "user_id": user_id,
        "query": query,
        "mode": mode,
        "top_k": top_k,
        "filters": filters or {},
        "result_count": len(result_list),
        "elapsed_ms": elapsed_ms,
        "error": error,
        "results": [_result_summary(result) for result in result_list],
    }

    target = material_search_log_path()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(sanitize_for_log(payload, max_string=500, max_list=100), ensure_ascii=False)
        with _LOG_LOCK:
            with target.open("a", encoding="utf-8") as file:
                file.write(line + "\n")
    except Exception:
        return None
    return target
