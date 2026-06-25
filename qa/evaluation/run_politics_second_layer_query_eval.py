from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa import agent_runtime


OUT_DIR = Path("data/runtime/current_affairs_eval")
OUT_DIR.mkdir(parents=True, exist_ok=True)


CASES = [
    ("same_topic_combo", "同一主题组合题", "4、5月份生态文明相关法案或文件体现哪些唯物辩证法原理"),
    ("two_events_compare_combo", "两个独立事件比较组合题", "比较2026年6月18日中美会谈和上合组织峰会分别体现了什么马原原理"),
    ("two_month_groups_news", "分时间分主题纯时政", "分别整理4月农业、5月外交的重要时政"),
    ("single_event_verify_combo", "条件式事件核验组合题", "确认2026年6月18日中美是否举行重要会谈，如果有体现什么马原原理"),
    ("broad_topic_combo", "宽泛专题时政映射题", "今年以来一带一路重要时政可以联系哪些考研政治原理"),
    ("recent_meetings_combo", "时间范围会议映射题", "最近两月的重要会议体现了哪些马原哲学原理"),
    ("recent_meetings_news", "时间范围纯时政整理", "最近两月的重要会议有哪些"),
    ("knowledge_concept", "纯理论概念题", "唯物辩证法有哪些核心原理"),
    ("law_draft_news", "法案文件纯时政", "4、5月份生态文明相关的法案或者文件有哪些"),
    ("agriculture_policy_news", "政策文件纯时政", "最近两个月农业农村相关政策文件有哪些"),
    ("single_meeting_theory", "单一会议理论映射题", "中央经济工作会议体现了马克思主义哪些原理"),
    ("two_documents_combo", "两个文件比较组合题", "比较生态环境法典草案和农业农村政策文件分别体现哪些唯物辩证法原理"),
    ("single_date_news_verify", "单日期事实核验", "2026年6月18日国内外有什么重要时政事件"),
    ("theory_difference", "纯理论辨析题", "矛盾的普遍性和特殊性有什么区别"),
    ("subjective_answer_style", "主观题答法题", "如果材料讲科技创新推动高质量发展，考研政治分析题怎么答"),
    ("historical_current_affairs", "明确年份历史时政", "2025年4月生态文明相关文件有哪些"),
]


def tool_call_item(call: dict[str, Any]) -> dict[str, Any]:
    function = call.get("function") or {}
    name = str(function.get("name") or "")
    raw_arguments = function.get("arguments") or "{}"
    try:
        arguments = json.loads(raw_arguments)
    except json.JSONDecodeError:
        arguments = {"_raw": raw_arguments}
    item = {"name": name}
    if "query" in arguments:
        item["query"] = arguments["query"]
    if "mode" in arguments:
        item["mode"] = arguments["mode"]
    return item


def run_case(case_id: str, case_type: str, question: str, client: Any, tools: list[dict[str, Any]], model: str) -> dict[str, Any]:
    messages = agent_runtime.build_tool_selection_messages(
        question,
        history=[],
        output_format="ui",
        subject="politics",
    )
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.0,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    assistant_message = agent_runtime.normalize_message(response.choices[0].message)
    tool_calls = [tool_call_item(call) for call in assistant_message.get("tool_calls") or []]
    return {
        "case_id": case_id,
        "case_type": case_type,
        "question": question,
        "tool_calls": tool_calls,
        "direct_answer": str(assistant_message.get("content") or "").strip(),
        "elapsed_ms": elapsed_ms,
    }


def main() -> None:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    tools = [tool.openai_schema() for tool in agent_runtime.select_tools("politics").values()]
    client = agent_runtime.make_global_client()
    model = os.getenv("ROUTER_MODEL") or agent_runtime.global_model_name()
    records = [run_case(case_id, case_type, question, client, tools, model) for case_id, case_type, question in CASES]
    path = OUT_DIR / f"politics_second_layer_queries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    for record in records:
        print(f"\n## {record['case_id']} | {record['case_type']} | {record['question']}")
        if record["tool_calls"]:
            for call in record["tool_calls"]:
                suffix = f" query={call.get('query')}" if call.get("query") else ""
                mode = f" mode={call.get('mode')}" if call.get("mode") else ""
                print(f"- {call['name']}{suffix}{mode}")
        else:
            print(f"- direct: {record['direct_answer'][:120]}")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
