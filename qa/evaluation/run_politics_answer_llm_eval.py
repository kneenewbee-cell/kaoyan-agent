from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa import agent_runtime
from qa.tools.current_affairs_search.verify import deduplicate_evidence_items


OUT_DIR = Path("data/runtime/current_affairs_eval")
OUT_DIR.mkdir(parents=True, exist_ok=True)


QUESTIONS = [
    ("combo_1", "中央经济工作会议体现了马克思主义哪些原理"),
    ("combo_2", "最近两月的重要会议体现了哪些马原哲学原理"),
    ("combo_3", "4、5月份生态文明相关法案或文件体现哪些唯物辩证法原理"),
    ("combo_4", "今年以来一带一路重要时政可以联系哪些考研政治原理"),
    ("combo_5", "确认2026年6月18日中美是否举行重要会谈，如果有体现什么马原原理"),
    ("news_only", "最近两月的重要会议有哪些"),
    ("knowledge_only", "唯物辩证法有哪些核心原理"),
]


def item(
    *,
    title: str,
    url: str,
    domain: str,
    date: str,
    snippet: str,
    preview: str,
    query: str,
    score: int = 6,
) -> dict:
    return {
        "title": title,
        "url": url,
        "snippet": snippet,
        "source_domain": domain,
        "query": query,
        "group": "mock_authoritative",
        "published_at": date,
        "extracted_dates": [date],
        "text_preview": preview,
        "relevance_score": score,
        "confidence_hint": "high",
    }


def fake_current_affairs(query: str) -> dict:
    q = query
    if "中央经济工作会议" in q:
        items = [
            item(
                title="中央经济工作会议在北京举行",
                url="https://www.news.cn/politics/2025-12/12/c_mock_cewc.htm",
                domain="news.cn",
                date="2025-12-12",
                snippet="会议分析当前经济形势，部署下一年经济工作，强调坚持稳中求进、推动高质量发展。",
                preview=(
                    "中央经济工作会议在北京举行。会议强调，坚持稳中求进工作总基调，完整准确全面贯彻新发展理念，"
                    "加快构建新发展格局，扎实推动高质量发展，统筹扩大内需、深化改革、科技创新和防范化解重点领域风险。"
                ),
                query=q,
            )
        ]
    elif "生态文明" in q or "环境保护" in q or "污染防治" in q:
        items = [
            item(
                title="生态环境法典草案提请审议",
                url="https://www.npc.gov.cn/mock/2026-04/ecology-code-draft.htm",
                domain="npc.gov.cn",
                date="2026-04-26",
                snippet="草案围绕污染防治、生态保护、绿色低碳发展等内容进行制度整合。",
                preview=(
                    "生态环境法典草案提请审议。草案坚持系统观念，统筹山水林田湖草沙一体化保护和系统治理，"
                    "完善污染防治、生态保护修复、绿色低碳发展等制度。"
                ),
                query=q,
            ),
            item(
                title="关于加强生态环境分区管控的意见发布",
                url="https://www.gov.cn/zhengce/2026-05/mock-eco-zoning.htm",
                domain="gov.cn",
                date="2026-05-15",
                snippet="文件要求以生态保护红线、环境质量底线、资源利用上线为基础，实施差异化管控。",
                preview=(
                    "有关部门发布生态环境分区管控文件，要求坚持系统治理、源头预防、分类施策，"
                    "推动经济社会发展全面绿色转型。"
                ),
                query=q,
            ),
        ]
    elif "一带一路" in q:
        items = [
            item(
                title="共建“一带一路”合作项目稳步推进",
                url="https://www.news.cn/world/2026-05/mock-bri.htm",
                domain="news.cn",
                date="2026-05-20",
                snippet="多领域务实合作持续推进，互联互通、经贸合作和人文交流取得进展。",
                preview=(
                    "今年以来，共建“一带一路”合作继续推进，相关合作围绕基础设施互联互通、经贸往来、绿色发展和民生项目展开，"
                    "体现共商共建共享原则。"
                ),
                query=q,
            )
        ]
    elif "中美" in q:
        items = [
            item(
                title="中美双方举行经贸领域会谈",
                url="https://www.news.cn/politics/2026-06/18/c_mock_us_china.htm",
                domain="news.cn",
                date="2026-06-18",
                snippet="双方围绕经贸关系、沟通机制和分歧管控等议题交换意见。",
                preview=(
                    "新华社报道，中美双方代表于2026年6月18日举行会谈，就经贸关系、沟通渠道、分歧管控和务实合作交换意见。"
                    "双方表示将保持沟通，推动问题通过对话协商处理。"
                ),
                query=q,
            )
        ]
    else:
        items = [
            item(
                title="国务院常务会议研究部署重点工作",
                url="https://www.gov.cn/yaowen/liebiao/2026-05/mock-state-council.htm",
                domain="gov.cn",
                date="2026-05-09",
                snippet="会议研究促进就业、扩大内需和民生保障等重点工作。",
                preview="国务院常务会议研究部署促进就业、扩大内需、保障民生等工作，强调统筹发展和安全。",
                query=q,
            ),
            item(
                title="全国人大常委会会议审议多项法律草案",
                url="https://www.npc.gov.cn/mock/2026-06/npc-session.htm",
                domain="npc.gov.cn",
                date="2026-06-24",
                snippet="会议围绕法律草案审议、监督工作和制度完善开展议程。",
                preview="全国人大常委会会议审议多项法律草案，体现科学立法、民主立法、依法立法要求。",
                query=q,
            ),
        ]

    return {
        "type": "current_affairs_evidence",
        "query": q,
        "current_time": "2026-06-25 12:00:00 CST",
        "task": {"mock": True},
        "search_scope": {"mock": True},
        "time_range": {"from": "2026-04-25", "to": "2026-06-25", "expression": "mock"},
        "items": deduplicate_evidence_items(items),
        "warnings": [],
    }


def fake_retrieve_politics(query: str, top_k: int = 3) -> list[dict]:
    if "一带一路" in query:
        chunks = [
            "共建“一带一路”体现开放发展理念和推动构建人类命运共同体的要求，坚持共商共建共享。",
            "联系具有普遍性，世界各国在经济、科技、文化等方面相互联系、相互影响。",
            "实践是认识的来源和发展动力，国际合作要在实践中不断完善机制、解决问题。",
        ]
    elif "唯物辩证法" in query or "辩证法" in query:
        chunks = [
            "唯物辩证法认为，联系具有普遍性、客观性和多样性，要用联系的观点看问题。",
            "发展是前进性与曲折性的统一，要用发展的观点看问题。",
            "矛盾是事物发展的根本动力，矛盾具有普遍性和特殊性，要坚持两点论和重点论统一。",
        ]
    elif "中美" in query or "矛盾" in query:
        chunks = [
            "矛盾具有普遍性和特殊性，分析问题既要承认矛盾、正视分歧，又要具体问题具体分析。",
            "联系具有普遍性，事物处在相互联系、相互作用之中，应坚持用联系的观点看问题。",
            "实践观点是马克思主义认识论的首要和基本观点，解决问题要在实践中检验和发展认识。",
        ]
    else:
        chunks = [
            "生产力决定生产关系，经济基础决定上层建筑；生产关系和上层建筑对生产力、经济基础具有反作用。",
            "社会存在决定社会意识，社会意识对社会存在具有能动反作用。",
            "矛盾分析方法要求坚持两点论和重点论统一，在复杂问题中抓主要矛盾和矛盾的主要方面。",
        ]
    return [
        {
            "content": text,
            "heading_path": ["考研政治", "马克思主义基本原理"],
            "score": 9.0 - index,
            "source": "mock_politics_knowledge.md",
        }
        for index, text in enumerate(chunks[:top_k])
    ]


def compact_tool_call(call: dict) -> dict:
    args = call.get("arguments") or {}
    item = {"name": call.get("name"), "ok": call.get("ok")}
    if "query" in args:
        item["query"] = args.get("query")
    if call.get("name") == "answer_politics_knowledge":
        item["mode"] = args.get("mode")
        try:
            outputs = json.loads(args.get("tool_outputs") or "[]")
            item["tool_output_tools"] = [output.get("tool") for output in outputs]
            for output in outputs:
                if output.get("tool") == "get_current_affairs":
                    content = json.loads(output.get("content") or "{}")
                    item["current_affairs_queries"] = content.get("queries") or [content.get("query")]
                    item["current_affairs_item_count"] = len(content.get("items") or [])
                    item["current_affairs_merged_tool_calls"] = content.get("merged_tool_calls")
        except Exception as exc:
            item["parse_error"] = str(exc)
    return item


def main() -> None:
    os.environ.setdefault("POLITICS_ANSWER_MODEL", "deepseek-v4-flash")
    records = []
    with patch("qa.kaoyan_agent.call_current_affairs_search", side_effect=fake_current_affairs), patch(
        "qa.politics_rag.retrieve_politics", side_effect=fake_retrieve_politics
    ):
        for index, (case_id, question) in enumerate(QUESTIONS, start=1):
            result = agent_runtime.run_standard_message_loop(
                question,
                session_id=f"eval_answer_llm_{case_id}_{index}",
                persist=False,
                output_format="ui",
            )
            record = {
                "case_id": case_id,
                "question": question,
                "answer": result.answer,
                "tool_calls": [compact_tool_call(call) for call in result.tool_calls],
                "metrics": result.metrics,
            }
            records.append(record)
            print(f"\n## {case_id} {question}")
            print(json.dumps(record["tool_calls"], ensure_ascii=False, indent=2))
            print(result.answer[:1200])

    path = OUT_DIR / f"politics_answer_llm_deepseek_mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
