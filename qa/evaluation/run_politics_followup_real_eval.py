from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.agent_runtime import delete_runtime_session_artifacts, run_standard_message_loop


OUT_DIR = ROOT / "data/runtime/current_affairs_eval"
OUT_DIR.mkdir(parents=True, exist_ok=True)


SCENARIOS = [
    {
        "id": "knowledge_followup",
        "label": "纯理论连续追问",
        "turns": [
            "矛盾的普遍性和特殊性有什么区别",
            "那主要矛盾和矛盾主要方面呢",
            "把这两组概念用一张表帮我区分",
        ],
    },
    {
        "id": "news_followup",
        "label": "纯时政连续追问",
        "turns": [
            "最近两月的重要会议有哪些",
            "其中和经济工作关系最密切的是哪个",
            "把它整理成考研时政速记版",
        ],
    },
    {
        "id": "combo_followup",
        "label": "时政理论混合追问",
        "turns": [
            "中央经济工作会议体现了马克思主义哪些原理",
            "其中矛盾分析法怎么展开",
            "再联系今年国家层面的两个大事举例说明",
        ],
    },
]


def safe_json_loads(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def summarize_tool_result(name: str, result: Any) -> dict[str, Any]:
    result = safe_json_loads(result)
    summary: dict[str, Any] = {"name": name}
    if name == "get_current_affairs" and isinstance(result, dict):
        items = result.get("items") or []
        summary["query"] = result.get("query")
        summary["queries"] = result.get("queries") or []
        summary["item_count"] = len(items)
        summary["items"] = [
            {
                "title": item.get("title"),
                "domain": item.get("source_domain") or item.get("domain"),
                "published_at": item.get("published_at"),
                "url": item.get("url"),
            }
            for item in items[:5]
            if isinstance(item, dict)
        ]
    elif name == "search_politics_knowledge" and isinstance(result, list):
        summary["item_count"] = len(result)
        summary["items"] = [
            {
                "heading": item.get("heading_path") or item.get("heading"),
                "score": item.get("score"),
                "preview": str(item.get("content") or "")[:140],
            }
            for item in result[:4]
            if isinstance(item, dict)
        ]
    elif name == "answer_politics_knowledge" and isinstance(result, str):
        summary["answer_chars"] = len(result)
        summary["preview"] = result[:180]
    else:
        summary["preview"] = str(result)[:300]
    return summary


def summarize_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for message in messages:
        if message.get("role") != "tool":
            continue
        name = str(message.get("name") or "")
        content = safe_json_loads(message.get("content") or "{}")
        ok = content.get("ok") if isinstance(content, dict) else None
        result = content.get("result") if isinstance(content, dict) else content
        row = summarize_tool_result(name, result)
        row["ok"] = ok
        rows.append(row)
    return rows


def compact_tool_call(record: dict[str, Any]) -> dict[str, Any]:
    args = record.get("arguments") or {}
    compact: dict[str, Any] = {
        "name": record.get("name"),
        "ok": record.get("ok"),
    }
    if isinstance(args, dict):
        for key in ("query", "mode", "question"):
            if key in args:
                compact[key] = args[key]
        if "tool_outputs" in args:
            compact["tool_outputs_len"] = len(str(args.get("tool_outputs") or ""))
    return compact


def route_steps(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    wanted = {
        "route_classifier",
        "subject_classifier",
        "followup_route_classifier",
        "llm_dag_followup_final",
        "llm_followup_clarification",
    }
    rows = []
    for step in metrics.get("steps") or []:
        if step.get("name") in wanted:
            rows.append({
                "name": step.get("name"),
                "subject": step.get("subject"),
                "category": step.get("category"),
                "parent_turn_id": step.get("parent_turn_id"),
                "parent_turn_ids": step.get("parent_turn_ids"),
                "error": step.get("error"),
            })
    return rows


def run_scenario(scenario: dict[str, Any], stamp: str) -> dict[str, Any]:
    session_id = f"politics_followup_eval_{scenario['id']}_{stamp}"
    delete_runtime_session_artifacts(session_id)
    turns = []
    for index, question in enumerate(scenario["turns"], start=1):
        print(f"\n[{scenario['id']}] turn {index}: {question}", flush=True)
        started = time.perf_counter()
        result = run_standard_message_loop(
            question,
            session_id=session_id,
            persist=True,
            output_format="ui",
        )
        elapsed = time.perf_counter() - started
        turn = {
            "index": index,
            "question": question,
            "elapsed_sec": round(elapsed, 2),
            "subject": result.subject,
            "route_steps": route_steps(result.metrics),
            "tool_calls": [compact_tool_call(record) for record in result.tool_calls],
            "tool_messages": summarize_messages(result.messages),
            "answer": result.answer,
            "answer_chars": len(result.answer),
        }
        turns.append(turn)
        print(f"  elapsed={turn['elapsed_sec']}s subject={turn['subject']} answer_chars={turn['answer_chars']}")
        print("  route:", turn["route_steps"])
        print("  tools:", " -> ".join(call.get("name") or "" for call in turn["tool_calls"]) or "none")
        print("  answer_preview:", result.answer.replace("\n", " ")[:240])
    return {
        "id": scenario["id"],
        "label": scenario["label"],
        "session_id": session_id,
        "turns": turns,
    }


def main() -> None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = [run_scenario(scenario, stamp) for scenario in SCENARIOS]

    json_path = OUT_DIR / f"politics_followup_real_eval_{stamp}.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# Politics Follow-up Real Eval",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        "- mode: real runtime chain, persisted sessions",
        "",
    ]
    for scenario in results:
        md_lines.extend([
            f"## {scenario['label']}",
            "",
            f"- session_id: `{scenario['session_id']}`",
            "",
        ])
        for turn in scenario["turns"]:
            md_lines.extend([
                f"### Turn {turn['index']}",
                "",
                f"- question: {turn['question']}",
                f"- subject: {turn['subject']}",
                f"- elapsed_sec: {turn['elapsed_sec']}",
                f"- route_steps: `{json.dumps(turn['route_steps'], ensure_ascii=False)}`",
                "- tools: "
                + (" -> ".join(call.get("name") or "" for call in turn["tool_calls"]) or "none"),
                "",
                turn["answer"].strip(),
                "",
            ])
    md_path = OUT_DIR / f"politics_followup_real_eval_{stamp}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nSAVED_JSON {json_path}")
    print(f"SAVED_MD {md_path}")


if __name__ == "__main__":
    main()
