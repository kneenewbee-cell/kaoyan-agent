from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.politics_rag import retrieve_politics


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python scripts/query_politics.py "主要矛盾和矛盾的主要方面有什么区别"')

    for index, row in enumerate(retrieve_politics(question), start=1):
        print(f"\n[{index}] {row['heading']} | {row['source']} | score={row['score']:.4f}")
        print(row["content"])


if __name__ == "__main__":
    main()
