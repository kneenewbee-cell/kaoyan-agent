from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from dotenv import load_dotenv

from .constants import ROOT


def trace_enabled() -> bool:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    value = (os.getenv("NEWS_SEARCH_LOG_ENABLED", "true") or "").strip().lower()
    return value not in {"0", "false", "no", "off"}


def write_search_trace(record: dict[str, Any]) -> None:
    if not trace_enabled():
        return
    now = datetime.now(timezone(timedelta(hours=8)))
    log_dir = ROOT / "data" / "runtime" / "current_affairs_search_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{now.date().isoformat()}.jsonl"
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
