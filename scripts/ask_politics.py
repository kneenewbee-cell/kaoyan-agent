from __future__ import annotations

import sys

from politics_rag import answer_with_qwen, retrieve_politics


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python scripts/ask_politics.py "主要矛盾和矛盾的主要方面有什么区别"')

    contexts = retrieve_politics(question)
    answer = answer_with_qwen(question, contexts)

    print(answer)
    print("\n参考资料：")
    for index, item in enumerate(contexts, start=1):
        print(f"{index}. {item['heading']} | {item['source']} | score={item['score']:.4f}")


if __name__ == "__main__":
    main()
