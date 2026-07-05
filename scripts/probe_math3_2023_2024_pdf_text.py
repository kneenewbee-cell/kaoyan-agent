from __future__ import annotations

from pathlib import Path

import pdfplumber


FILES = [
    Path(r"D:\百度网盘\高数资料\2023年考研数学三真题.pdf"),
    Path(r"D:\百度网盘\高数资料\2023考研数学三答案解析（一二三合集）.pdf"),
    Path(r"D:\百度网盘\高数资料\2024考研数学三真题.pdf"),
    Path(r"D:\百度网盘\高数资料\2024考研数学三真题答案解析.pdf"),
]


def main() -> None:
    for path in FILES:
        print(f"--- {path.name}")
        with pdfplumber.open(str(path)) as doc:
            print("pages", len(doc.pages))
            for index, page in enumerate(doc.pages[:4], 1):
                text = page.extract_text() or ""
                print(f"page {index}")
                print(repr(text[:1500]))


if __name__ == "__main__":
    main()
