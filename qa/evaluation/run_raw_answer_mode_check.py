from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa import agent_runtime


OUT_DIR = ROOT / "data/runtime/current_affairs_eval"
OUT_DIR.mkdir(parents=True, exist_ok=True)


CASES = [
    {
        "case_id": "same_topic_combo",
        "case_type": "同一主题组合题",
        "question": "4、5月份生态文明相关法案或文件体现哪些唯物辩证法原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "two_events_compare_combo",
        "case_type": "两个独立事件比较组合题",
        "question": "比较2026年6月18日中美会谈和上合组织峰会分别体现了什么马原原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "two_month_groups_news",
        "case_type": "分时间分主题纯时政",
        "question": "分别整理4月农业、5月外交的重要时政",
        "expected_mode": "news_only",
    },
    {
        "case_id": "single_event_verify_combo",
        "case_type": "条件式事件核验组合题",
        "question": "确认2026年6月18日中美是否举行重要会谈，如果有体现什么马原原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "broad_topic_combo",
        "case_type": "宽泛专题时政映射题",
        "question": "今年以来一带一路重要时政可以联系哪些考研政治原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "recent_meetings_combo",
        "case_type": "时间范围会议映射题",
        "question": "最近两月的重要会议体现了哪些马原哲学原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "recent_meetings_news",
        "case_type": "时间范围纯时政整理",
        "question": "最近两月的重要会议有哪些",
        "expected_mode": "news_only",
    },
    {
        "case_id": "knowledge_concept",
        "case_type": "纯理论概念题",
        "question": "唯物辩证法有哪些核心原理",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "law_draft_news",
        "case_type": "法案文件纯时政",
        "question": "4、5月份生态文明相关的法案或者文件有哪些",
        "expected_mode": "news_only",
    },
    {
        "case_id": "agriculture_policy_news",
        "case_type": "政策文件纯时政",
        "question": "最近两个月农业农村相关政策文件有哪些",
        "expected_mode": "news_only",
    },
    {
        "case_id": "single_meeting_theory",
        "case_type": "单一会议理论映射题",
        "question": "中央经济工作会议体现了马克思主义哪些原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "two_documents_combo",
        "case_type": "两个文件比较组合题",
        "question": "比较生态环境法典草案和农业农村政策文件分别体现哪些唯物辩证法原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "single_date_news_verify",
        "case_type": "单日期事实核验",
        "question": "2026年6月18日国内外有什么重要时政事件",
        "expected_mode": "news_only",
    },
    {
        "case_id": "theory_difference",
        "case_type": "纯理论辨析题",
        "question": "矛盾的普遍性和特殊性有什么区别",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "subjective_answer_style",
        "case_type": "主观题答法题",
        "question": "如果材料讲科技创新推动高质量发展，考研政治分析题怎么答",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "historical_current_affairs",
        "case_type": "明确年份历史时政",
        "question": "2025年4月生态文明相关文件有哪些",
        "expected_mode": "news_only",
    },
]


def fake_current_affairs(query: str) -> dict:
    return {
        "type": "current_affairs_evidence",
        "query": query,
        "items": [
            {
                "title": f"权威时政材料：{query}",
                "url": "https://news.cn/mock",
                "source_domain": "news.cn",
                "published_at": "2026-06-18",
                "extracted_dates": ["2026-06-18"],
                "snippet": f"围绕 {query} 的权威时政摘要。",
                "text_preview": f"这是关于 {query} 的模拟权威时政材料，用于测试第二层 mode 输出，不代表真实新闻。",
                "confidence_hint": "high",
            }
        ],
        "warnings": [],
    }


def fake_retrieve(query: str, top_k: int = 3) -> list[dict]:
    return [
        {
            "content": f"知识库命中：{query}。这里提供考研政治标准表述，用于测试第二层 mode 输出。",
            "heading_path": ["考研政治", "马克思主义基本原理"],
            "score": 9.0,
        }
    ]


def fake_answer(question: str, tool_outputs, history_brief: str = "", mode: str = "auto", output_format: str = "ui") -> str:
    return f"mock answer mode={mode}"


def raw_answer_calls(messages: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for index, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue
        for call in message.get("tool_calls") or []:
            function = call.get("function") or {}
            if function.get("name") != "answer_politics_knowledge":
                continue
            try:
                arguments = json.loads(function.get("arguments") or "{}")
            except json.JSONDecodeError as exc:
                arguments = {"_parse_error": str(exc), "_raw": function.get("arguments")}
            source = "runtime_auto" if str(call.get("id") or "").startswith("auto_answer_politics_knowledge") else "second_layer_raw"
            rows.append({"message_index": index, "source": source, "raw_arguments": arguments})
    return rows


def compact_record(call: dict) -> dict:
    arguments = call.get("arguments") or {}
    if call.get("name") == "answer_politics_knowledge":
        return {
            "name": call.get("name"),
            "mode": arguments.get("mode"),
            "question": arguments.get("question"),
        }
    return {"name": call.get("name"), "query": arguments.get("query")}


def second_layer_mode(rows: list[dict]) -> str | None:
    for row in rows:
        if row.get("source") == "second_layer_raw":
            args = row.get("raw_arguments") or {}
            return args.get("mode")
    return None


def main() -> None:
    records = []
    with patch("qa.agent_runtime.classify_subject", return_value="politics"), patch(
        "qa.kaoyan_agent.call_current_affairs_search", side_effect=fake_current_affairs
    ), patch("qa.politics_rag.retrieve_politics", side_effect=fake_retrieve), patch(
        "qa.politics_rag.answer_politics_knowledge", side_effect=fake_answer
    ):
        for case in CASES:
            result = agent_runtime.run_standard_message_loop(
                case["question"],
                session_id=f"eval_raw_mode_{case['case_id']}",
                persist=False,
                output_format="ui",
            )
            raw_rows = raw_answer_calls(result.messages)
            mode = second_layer_mode(raw_rows)
            record = {
                **case,
                "second_layer_mode": mode,
                "status": "pass" if mode == case["expected_mode"] else ("no_second_layer_answer" if mode is None else "fail"),
                "raw_answer_calls": raw_rows,
                "executed_records": [compact_record(call) for call in result.tool_calls],
            }
            records.append(record)

            print(f"\n## {case['case_id']} | {case['case_type']}")
            print(case["question"])
            print(f"expected={case['expected_mode']} second_layer_mode={mode} status={record['status']}")
            print("executed:", " -> ".join(item["name"] for item in record["executed_records"]))

    path = OUT_DIR / f"politics_second_layer_modes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
