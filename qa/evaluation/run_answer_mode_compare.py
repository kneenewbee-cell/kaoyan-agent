from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.politics_rag import answer_politics_knowledge


def main() -> None:
    os.environ.setdefault("POLITICS_ANSWER_MODEL", "deepseek-v4-flash")
    question = "确认2026年6月18日中美是否举行重要会谈，如果有体现什么马原原理"
    current_affairs_only = [
        {
            "tool": "get_current_affairs",
            "content": json.dumps(
                {
                    "type": "current_affairs_evidence",
                    "query": "2026年6月18日 中美 重要会谈",
                    "items": [
                        {
                            "title": "中美双方举行经贸领域会谈",
                            "url": "https://www.news.cn/politics/2026-06/18/c_mock_us_china.htm",
                            "source_domain": "news.cn",
                            "published_at": "2026-06-18",
                            "extracted_dates": ["2026-06-18"],
                            "snippet": "双方围绕经贸关系、沟通机制和分歧管控等议题交换意见。",
                            "text_preview": (
                                "新华社报道，中美双方代表于2026年6月18日举行会谈，"
                                "就经贸关系、沟通渠道、分歧管控和务实合作交换意见。"
                                "双方表示将保持沟通，推动问题通过对话协商处理。"
                            ),
                            "confidence_hint": "high",
                        }
                    ],
                    "warnings": [],
                },
                ensure_ascii=False,
            ),
        }
    ]
    records = []
    for mode in ("news_only", "combo"):
        answer = answer_politics_knowledge(
            question=question,
            tool_outputs=json.dumps(current_affairs_only, ensure_ascii=False),
            mode=mode,
            output_format="ui",
        )
        records.append({"mode": mode, "answer": answer})
        print(f"\n===== MODE {mode} =====")
        print(answer)

    out_dir = ROOT / "data/runtime/current_affairs_eval"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"answer_politics_scheme_c_mode_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps({"question": question, "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSAVED {path}")


if __name__ == "__main__":
    main()
