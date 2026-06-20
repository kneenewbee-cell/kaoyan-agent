from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.politics_rag import VECTOR_FILE, embed_texts, iter_markdown_files, parse_markdown_sections, write_jsonl


def main() -> None:
    chunks = []
    for path in iter_markdown_files():
        chunks.extend(parse_markdown_sections(path))

    if not chunks:
        raise SystemExit("没有找到政治资料，请先把 .md 文件放到 data/raw/politics/")

    texts = [chunk.get("embedding_text") or chunk["content"] for chunk in chunks]
    embeddings = embed_texts(texts)
    rows = []
    for chunk, embedding in zip(chunks, embeddings):
        rows.append({**chunk, "embedding": embedding})

    write_jsonl(VECTOR_FILE, rows)
    print(f"已写入 {len(chunks)} 个政治知识块 -> {VECTOR_FILE}")


if __name__ == "__main__":
    main()
