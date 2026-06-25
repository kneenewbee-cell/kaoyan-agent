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
        "case_id": "exam_stem_tech",
        "case_type": "题干背景考点",
        "question": "题干围绕科技自立自强推动高质量发展，政治大题应抓哪些考点",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "green_transition_viewpoints",
        "case_type": "抽象背景套观点",
        "question": "绿色转型带动产业升级这类设问，可以套哪些辩证法观点",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "digital_village_angles",
        "case_type": "抽象背景组织思路",
        "question": "数字经济赋能乡村振兴，政治大题从哪些角度展开",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "new_quality_answer_path",
        "case_type": "理论关系组织思路",
        "question": "新质生产力和高质量发展这组关系，考场上怎么组织思路",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "state_events_memory",
        "case_type": "当前大事积累",
        "question": "今年五六月国家层面有哪些值得记的大事",
        "expected_mode": "news_only",
    },
    {
        "case_id": "ecology_public_moves",
        "case_type": "历史官方动向",
        "question": "2025年4月生态文明领域有哪些官方动向",
        "expected_mode": "news_only",
    },
    {
        "case_id": "agriculture_public_actions",
        "case_type": "当前官方举措",
        "question": "过去两个月三农领域有哪些值得关注的官方举措",
        "expected_mode": "news_only",
    },
    {
        "case_id": "single_day_events",
        "case_type": "单日大事",
        "question": "6月18日国内外有哪些值得记的大事",
        "expected_mode": "news_only",
    },
    {
        "case_id": "bri_principle_pairing",
        "case_type": "真实进展对应理论",
        "question": "今年以来一带一路有哪些进展可对应考研政治原理",
        "expected_mode": "combo",
    },
    {
        "case_id": "us_china_if_true",
        "case_type": "条件式事实理论题",
        "question": "2026年6月18日中美接触若属实，可从哪些马原角度理解",
        "expected_mode": "combo",
    },
    {
        "case_id": "ecology_moves_dialectics",
        "case_type": "官方动向对应理论",
        "question": "拿4月到5月生态文明领域的官方动向举例，怎么对应唯物辩证法",
        "expected_mode": "combo",
    },
    {
        "case_id": "state_events_contradiction",
        "case_type": "当前大事理论筛选",
        "question": "今年国家层面的大事里，哪些能用矛盾分析法解读",
        "expected_mode": "combo",
    },
    {
        "case_id": "two_objects_principles",
        "case_type": "两个对象理论对应",
        "question": "上合组织活动和中美接触分别可对应哪些马原观点",
        "expected_mode": "combo",
    },
    {
        "case_id": "practice_cognition_memory",
        "case_type": "纯理论记忆",
        "question": "实践和认识的关系怎么背最稳",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "main_contradiction_compare",
        "case_type": "纯理论辨析",
        "question": "主要矛盾和矛盾主要方面怎么区分",
        "expected_mode": "knowledge_only",
    },
    {
        "case_id": "mid_june_digest",
        "case_type": "大事速记清单",
        "question": "帮我做一份6月中旬国内外大事速记清单",
        "expected_mode": "news_only",
    },
]


def fake_current_affairs(query: str) -> dict:
    return {
        "type": "current_affairs_evidence",
        "query": query,
        "items": [
            {
                "title": f"权威公开材料：{query}",
                "url": "https://news.cn/mock",
                "source_domain": "news.cn",
                "published_at": "2026-06-18",
                "extracted_dates": ["2026-06-18"],
                "snippet": f"围绕 {query} 的公开摘要。",
                "text_preview": f"这是关于 {query} 的模拟公开材料，用于测试第二层 mode 输出，不代表真实内容。",
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
                session_id=f"eval_mode_paraphrase_{case['case_id']}",
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

    path = OUT_DIR / f"politics_mode_paraphrase_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
