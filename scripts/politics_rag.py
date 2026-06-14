from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
RAW_POLITICS_DIR = ROOT / "data" / "raw" / "politics"
PROCESSED_DIR = ROOT / "data" / "processed"
VECTOR_FILE = PROCESSED_DIR / "politics_vectors.jsonl"
COLLECTION_NAME = "politics_knowledge"


def load_settings() -> dict[str, str | int | None]:
    load_dotenv(ROOT / ".env")
    return {
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "model": os.getenv("EMBEDDING_MODEL", "text-embedding-v4"),
        "dimensions": int(os.getenv("EMBEDDING_DIMENSIONS", "1024")),
        "chat_model": os.getenv("QWEN_CHAT_MODEL", "qwen-max"),
    }


def iter_markdown_files() -> Iterable[Path]:
    return sorted(RAW_POLITICS_DIR.glob("*.md"))


def parse_markdown_sections(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    chunks: list[dict[str, str]] = []
    current_heading = title
    current_lines: list[str] = []

    for line in text.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            if current_lines:
                chunks.extend(split_text("\n".join(current_lines), path, current_heading))
                current_lines = []
            current_heading = heading.group(2).strip()
            continue
        current_lines.append(line)

    if current_lines:
        chunks.extend(split_text("\n".join(current_lines), path, current_heading))

    return chunks


def split_text(text: str, path: Path, heading: str, max_chars: int = 700) -> list[dict[str, str]]:
    cleaned = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not cleaned:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    chunks: list[dict[str, str]] = []
    buffer = ""

    for paragraph in paragraphs:
        candidate = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph
        if len(candidate) <= max_chars:
            buffer = candidate
            continue
        if buffer:
            chunks.append(make_chunk(buffer, path, heading, len(chunks)))
        buffer = paragraph

    if buffer:
        chunks.append(make_chunk(buffer, path, heading, len(chunks)))
    return chunks


def make_chunk(content: str, path: Path, heading: str, index: int) -> dict[str, str]:
    rel_path = path.relative_to(ROOT).as_posix()
    raw_id = f"{rel_path}:{heading}:{index}"
    chunk_id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()
    return {
        "id": chunk_id,
        "content": content,
        "source": rel_path,
        "subject": "politics",
        "heading": heading,
    }


def embed_texts(texts: list[str]) -> list[list[float]]:
    settings = load_settings()
    api_key = settings["api_key"]
    dimensions = int(settings["dimensions"])

    if api_key:
        from openai import OpenAI

        client = OpenAI(api_key=str(api_key), base_url=str(settings["base_url"]))
        embeddings: list[list[float]] = []
        batch_size = 10
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            response = client.embeddings.create(
                model=str(settings["model"]),
                input=batch,
                dimensions=dimensions,
                encoding_format="float",
            )
            embeddings.extend(item.embedding for item in response.data)
        return embeddings

    return [local_hash_embedding(text, dimensions) for text in texts]


def local_hash_embedding(text: str, dimensions: int = 1024) -> list[float]:
    vector = [0.0] * dimensions
    tokens = re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9_]+", text.lower())
    for token in tokens:
        digest = hashlib.md5(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Vector file not found: {path}. Run: python scripts/build_politics_db.py")
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def retrieve_politics(question: str, top_k: int = 3) -> list[dict]:
    rows = read_jsonl(VECTOR_FILE)
    query_embedding = embed_texts([question])[0]
    ranked = sorted(
        rows,
        key=lambda row: cosine_similarity(query_embedding, row["embedding"]),
        reverse=True,
    )
    results = []
    for row in ranked[:top_k]:
        results.append({**row, "score": cosine_similarity(query_embedding, row["embedding"])})
    return results


def answer_with_qwen(question: str, contexts: list[dict]) -> str:
    settings = load_settings()
    api_key = settings["api_key"]
    if not api_key:
        raise SystemExit("Please set DASHSCOPE_API_KEY in .env before using qwen-max.")

    from openai import OpenAI

    context_text = "\n\n".join(
        f"Context {index}: {item['heading']}\nSource: {item['source']}\nContent: {item['content']}"
        for index, item in enumerate(contexts, start=1)
    )
    client = OpenAI(api_key=str(api_key), base_url=str(settings["base_url"]))
    response = client.chat.completions.create(
        model=str(settings["chat_model"]),
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个严谨的考研政治 RAG 答疑助手。必须只依据用户提供的参考资料回答，"
                    "不得使用参考资料之外的案例、题目、年份、政策表述、历史阶段或背景知识。"
                    "如果参考资料没有给出具体例子，就明确写“资料中未提供具体例子”，不要自行编造。"
                    "回答应包含：概念、核心区别、易混点、资料不足。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"问题：{question}\n\n"
                    f"参考资料如下，请严格限定在这些资料内回答：\n{context_text}\n\n"
                    "输出要求：\n"
                    "1. 不要编写资料外的例子或模拟题。\n"
                    "2. 每个要点都尽量贴合参考资料中的原意。\n"
                    "3. 如果某部分资料不足，直接说明缺少什么资料。"
                ),
            },
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
