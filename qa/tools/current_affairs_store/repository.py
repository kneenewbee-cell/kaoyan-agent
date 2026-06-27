from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CURRENT_AFFAIRS_DIR = ROOT / "data" / "raw" / "current_affairs"


def now_beijing_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


class CurrentAffairsStore:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = Path(base_dir or DEFAULT_CURRENT_AFFAIRS_DIR)

    @property
    def current_year_dir(self) -> Path:
        return self.base_dir / "current_year"

    @property
    def history_dir(self) -> Path:
        return self.base_dir / "history"

    @property
    def current_sources_path(self) -> Path:
        return self.current_year_dir / "sources.jsonl"

    @property
    def history_events_path(self) -> Path:
        return self.history_dir / "events_history.jsonl"

    @property
    def history_sources_path(self) -> Path:
        return self.history_dir / "sources_history.jsonl"

    def list_events(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for path in sorted(self.current_year_dir.glob("*/events.jsonl")):
            events.extend(read_jsonl(path))
        events.extend(read_jsonl(self.history_events_path))
        return events

    def list_sources(self) -> list[dict[str, Any]]:
        return [*read_jsonl(self.current_sources_path), *read_jsonl(self.history_sources_path)]

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        for event in self.list_events():
            if event.get("event_id") == event_id or event_id in (event.get("merged_from") or []):
                return event
        return None

    def get_source(self, source_doc_id: str) -> dict[str, Any] | None:
        for source in self.list_sources():
            if source.get("source_doc_id") == source_doc_id:
                return source
        return None

    def find_source_by_url(self, canonical_url: str) -> dict[str, Any] | None:
        for source in self.list_sources():
            if source.get("canonical_url") == canonical_url:
                return source
        return None

    def upsert_source(self, source: dict[str, Any]) -> dict[str, Any]:
        path = self.source_path_for_date(str(source.get("published_at") or source.get("event_date") or ""))
        sources = read_jsonl(path)
        source = dict(source)
        source.setdefault("first_seen_at", now_beijing_iso())
        source["last_seen_at"] = now_beijing_iso()
        for index, existing in enumerate(sources):
            if existing.get("source_doc_id") == source.get("source_doc_id"):
                merged = {**existing, **source, "first_seen_at": existing.get("first_seen_at") or source["first_seen_at"]}
                sources[index] = merged
                write_jsonl(path, sources)
                return merged
        sources.append(source)
        write_jsonl(path, sources)
        return source

    def upsert_event(self, event: dict[str, Any]) -> dict[str, Any]:
        path = self.event_path_for(event)
        events = read_jsonl(path)
        event = dict(event)
        event.setdefault("first_seen_at", now_beijing_iso())
        event["last_verified_at"] = now_beijing_iso()
        for index, existing in enumerate(events):
            if existing.get("event_id") == event.get("event_id"):
                merged = {**existing, **event, "first_seen_at": existing.get("first_seen_at") or event["first_seen_at"]}
                events[index] = merged
                write_jsonl(path, events)
                return merged
        events.append(event)
        write_jsonl(path, events)
        return event

    def next_event_id(self, event_date: str) -> str:
        compact = date_compact(event_date)
        max_seq = 0
        prefix = f"cae_{compact}_"
        for event in self.list_events():
            event_id = str(event.get("event_id") or "")
            if not event_id.startswith(prefix):
                continue
            try:
                max_seq = max(max_seq, int(event_id.rsplit("_", 1)[1]))
            except (IndexError, ValueError):
                continue
        return f"{prefix}{max_seq + 1:04d}"

    def event_path_for(self, event: dict[str, Any]) -> Path:
        event_date = str(event.get("event_date") or "")
        category = safe_segment(str(event.get("category") or "other"))
        if is_current_year(event_date):
            return self.current_year_dir / category / "events.jsonl"
        return self.history_events_path

    def source_path_for_date(self, value: str) -> Path:
        if is_current_year(value):
            return self.current_sources_path
        return self.history_sources_path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.write_text(f"{content}\n" if content else "", encoding="utf-8")


def current_beijing_year() -> str:
    return str(datetime.now(timezone(timedelta(hours=8))).year)


def is_current_year(value: str) -> bool:
    year = str(value or "")[:4]
    return not year or year == current_beijing_year()


def date_compact(value: str) -> str:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10].replace("-", "")
    if len(text) >= 8 and text[:8].isdigit():
        return text[:8]
    return f"{current_beijing_year()}0101"


def safe_segment(value: str) -> str:
    text = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value.strip().lower())
    return text or "other"
