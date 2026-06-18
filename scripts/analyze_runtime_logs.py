from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "data" / "runtime" / "logs" / "2026-05-29.jsonl"


def load_records(log_path: Path, session_id: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not log_path.exists():
        return records
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        metrics = item.get("metrics") or {}
        if metrics.get("session_id") != session_id:
            continue
        messages = item.get("messages") or []
        users = [message.get("content", "") for message in messages if message.get("role") == "user"]
        query = users[-1].replace("\n", " ") if users else ""
        records.append({
            "time": item.get("time", ""),
            "query": query,
            "metrics": metrics,
            "tool_calls": item.get("tool_calls") or [],
        })
    return records


def print_records(records: list[dict[str, Any]], details: bool) -> None:
    for index, record in enumerate(records, start=1):
        metrics = record["metrics"]
        steps = metrics.get("steps") or []
        slowest = max(steps, key=lambda step: step.get("latency_ms", 0), default={})
        tools = ",".join(call.get("name", "") for call in record["tool_calls"]) or "-"
        print(
            f"{index:02d}. {record['time']} "
            f"{metrics.get('elapsed_ms', 0) / 1000:7.2f}s "
            f"tokens={metrics.get('total_tokens', 0):5} "
            f"llm={metrics.get('llm_calls', 0)} "
            f"tools={metrics.get('tool_calls', 0)} "
            f"tool={tools} "
            f"slow={slowest.get('name', '-')}:"
            f"{slowest.get('latency_ms', 0) / 1000:.2f}s"
        )
        print(f"    q: {record['query'][:100]}")
        if details:
            for step in steps:
                print(f"      - {step.get('name', '-')}: {step.get('latency_ms', 0) / 1000:.2f}s {step}")


def print_aggregate(records: list[dict[str, Any]]) -> None:
    if not records:
        return
    elapsed = [record["metrics"].get("elapsed_ms", 0) for record in records]
    tokens = [record["metrics"].get("total_tokens", 0) for record in records]
    print()
    print(
        f"aggregate: n={len(records)} "
        f"avg_elapsed={sum(elapsed) / len(elapsed) / 1000:.2f}s "
        f"max_elapsed={max(elapsed) / 1000:.2f}s "
        f"avg_tokens={sum(tokens) / len(tokens):.0f} "
        f"max_tokens={max(tokens)}"
    )
    by_step: dict[str, list[float]] = defaultdict(list)
    for record in records:
        for step in record["metrics"].get("steps") or []:
            by_step[step.get("name", "-")].append(step.get("latency_ms", 0))
    for name, values in sorted(by_step.items(), key=lambda item: sum(item[1]) / len(item[1]), reverse=True):
        print(
            f"  {name:42s} "
            f"n={len(values):2d} avg={sum(values) / len(values) / 1000:7.2f}s "
            f"max={max(values) / 1000:7.2f}s"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize runtime latency logs by session.")
    parser.add_argument("--session", default="default", help="session id, e.g. default, 1, 2")
    parser.add_argument("--limit", type=int, default=20, help="number of recent records to show")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="runtime jsonl log path")
    parser.add_argument("--details", action="store_true", help="print every step in each record")
    args = parser.parse_args()

    records = load_records(args.log, args.session)
    selected = records[-args.limit:]
    print(f"session={args.session} records={len(records)} showing={len(selected)} log={args.log}")
    print_records(selected, args.details)
    print_aggregate(selected)


if __name__ == "__main__":
    main()
