from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_LOG_DIR = ROOT / "data" / "runtime" / "logs"
REDACTED_KEYS = {
    "api_key",
    "authorization",
    "password",
    "secret",
    "access_token",
    "refresh_token",
    "qwen_api_key",
    "dashscope_api_key",
}


def _truncate_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"...[truncated {len(value) - limit} chars]"


def sanitize_for_log(value: Any, *, max_string: int = 300, max_list: int = 30, depth: int = 0) -> Any:
    if depth > 8:
        return "[max_depth]"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in REDACTED_KEYS or key_lower.endswith("_api_key"):
                result[key_text] = "[redacted]"
            else:
                result[key_text] = sanitize_for_log(
                    item,
                    max_string=max_string,
                    max_list=max_list,
                    depth=depth + 1,
                )
        return result
    if isinstance(value, list):
        result = [
            sanitize_for_log(item, max_string=max_string, max_list=max_list, depth=depth + 1)
            for item in value[:max_list]
        ]
        if len(value) > max_list:
            result.append(f"[truncated {len(value) - max_list} items]")
        return result
    if isinstance(value, str):
        return _truncate_text(value, max_string)
    return value


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def monotonic_ms(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000, 2)


def write_material_pipeline_log(record: dict[str, Any], *, material_log_path: Path | None = None) -> Path:
    PIPELINE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = PIPELINE_LOG_DIR / f"material_pipeline_{datetime.now().date().isoformat()}.jsonl"
    payload = {
        "time": now_utc_iso(),
        "event": "material_pipeline",
        **sanitize_for_log(record),
    }
    line = json.dumps(payload, ensure_ascii=False)
    with target.open("a", encoding="utf-8") as file:
        file.write(line + "\n")
    if material_log_path is not None:
        material_log_path.parent.mkdir(parents=True, exist_ok=True)
        with material_log_path.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
    return target


class MaterialPipelineLogger:
    def __init__(
        self,
        *,
        material_id: str,
        user_id: str,
        source_name: str | None = None,
        material_log_path: Path | None = None,
        run_id: str | None = None,
    ) -> None:
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:12]}"
        self.material_id = material_id
        self.user_id = user_id
        self.source_name = source_name
        self.material_log_path = material_log_path

    def bind_material_log(self, material_log_path: Path) -> None:
        self.material_log_path = material_log_path

    def log(self, stage: str, status: str = "completed", **fields: Any) -> None:
        record = {
            "run_id": self.run_id,
            "material_id": self.material_id,
            "user_id": self.user_id,
            "source_name": self.source_name,
            "stage": stage,
            "status": status,
            **fields,
        }
        try:
            write_material_pipeline_log(record, material_log_path=self.material_log_path)
        except OSError:
            # Logging must never break ingestion.
            return
