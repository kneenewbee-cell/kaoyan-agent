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
        "case_id": "hypothetical_tech_frame",
        "case_type": "题设背景答法",
        "question": "题干围绕科技自立自强推动高质量发展，政治大题应抓哪些考点",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "hypothetical_green_dialectics",
        "case_type": "题设背景映射理论",
        "question": "给定背景是绿色转型带动产业升级，可以套哪些唯物辩证法观点",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "hypothetical_digital_village",
        "case_type": "题设背景组织答案",
        "question": "一段题目设定为数字经济赋能乡村振兴，应该从哪些政治角度组织答案",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "concept_answer_frame",
        "case_type": "理论框架题",
        "question": "用新质生产力解释高质量发展，考研政治答题框架是什么",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "state_level_events",
        "case_type": "纯时政大事积累",
        "question": "今年五六月国家层面有哪些大事适合做时政积累",
        "expected_mode": "news_only",
    },
    {
        "case_id": "ecology_official_moves",
        "case_type": "纯时政官方动向",
        "question": "2025年4月生态文明领域有哪些官方动向",
        "expected_mode": "news_only",
    },
    {
        "case_id": "agriculture_official_actions",
        "case_type": "纯时政官方举措",
        "question": "过去两个月三农领域有什么值得关注的官方举措",
        "expected_mode": "news_only",
    },
    {
        "case_id": "single_day_events",
        "case_type": "单日时政大事",
        "question": "6月18日国内外有哪些值得记的时政大事",
        "expected_mode": "news_only",
    },
    {
        "case_id": "bri_principle_pairing",
        "case_type": "真实进展理论对应",
        "question": "把今年以来一带一路的重要进展和考研政治原理对应一下",
        "expected_mode": "combo",
    },
    {
        "case_id": "conditional_us_china",
        "case_type": "条件式事实理论题",
        "question": "2026年6月18日中美会谈若属实，可从哪些马原角度理解",
        "expected_mode": "combo",
    },
    {
        "case_id": "ecology_moves_dialectics",
        "case_type": "官方动向理论对应",
        "question": "拿4月到5月生态文明领域的官方动向举例，怎么对应唯物辩证法",
        "expected_mode": "combo",
    },
    {
        "case_id": "major_events_contradiction",
        "case_type": "时政大事理论筛选",
        "question": "今年国家层面的大事里，哪些能用矛盾分析法解读",
        "expected_mode": "combo",
    },
    {
        "case_id": "two_objects_principles",
        "case_type": "两个对象理论对应",
        "question": "上合组织峰会和中美会谈分别可对应哪些马原观点",
        "expected_mode": "combo",
    },
    {
        "case_id": "pure_theory_practice",
        "case_type": "纯理论概念",
        "question": "实践和认识的关系怎么背最稳",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "pure_theory_compare",
        "case_type": "纯理论辨析",
        "question": "主要矛盾和矛盾主要方面容易混，怎么区分",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "current_affairs_digest",
        "case_type": "时政积累清单",
        "question": "帮我做一份6月中旬国内外时政速记清单",
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


def second_layer_mode(rows: list[dict]) -> str | None:
    for row in rows:
        if row.get("source") == "second_layer_raw":
            return (row.get("raw_arguments") or {}).get("mode")
    return None


def compact_record(call: dict) -> dict:
    arguments = call.get("arguments") or {}
    if call.get("name") == "answer_politics_knowledge":
        return {"name": call.get("name"), "mode": arguments.get("mode")}
    return {"name": call.get("name"), "query": arguments.get("query")}


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
                session_id=f"eval_mode_generalization_{case['case_id']}",
                persist=False,
                output_format="ui",
            )
            rows = raw_answer_calls(result.messages)
            mode = second_layer_mode(rows)
            record = {
                **case,
                "second_layer_mode": mode,
                "status": "pass" if mode == case["expected_mode"] else ("missing" if mode is None else "fail"),
                "executed_records": [compact_record(call) for call in result.tool_calls],
                "raw_answer_calls": rows,
            }
            records.append(record)
            print(f"\n## {case['case_id']} | {case['case_type']}")
            print(case["question"])
            print(f"expected={case['expected_mode']} second_layer_mode={mode} status={record['status']}")
            print("executed:", " -> ".join(item["name"] for item in record["executed_records"]))

    path = OUT_DIR / f"politics_mode_generalization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
