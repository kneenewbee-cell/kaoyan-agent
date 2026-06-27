from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


@dataclass(frozen=True)
class EmbeddingSettings:
    api_key: str | None
    base_url: str
    model: str
    dimensions: int
    batch_size: int
    timeout_seconds: int


def load_embedding_settings() -> EmbeddingSettings:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass

    dimensions_raw = os.getenv("MATERIALS_EMBEDDING_DIMENSIONS") or os.getenv("EMBEDDING_DIMENSIONS") or "1024"
    batch_size_raw = os.getenv("MATERIALS_EMBEDDING_BATCH_SIZE") or "10"
    timeout_raw = os.getenv("MATERIALS_EMBEDDING_TIMEOUT_SECONDS") or "120"

    return EmbeddingSettings(
        api_key=os.getenv("MATERIALS_EMBEDDING_API_KEY")
        or os.getenv("DASHSCOPE_API_KEY")
        or os.getenv("QWEN_API_KEY"),
        base_url=os.getenv("MATERIALS_EMBEDDING_BASE_URL")
        or os.getenv("DASHSCOPE_BASE_URL")
        or DEFAULT_BASE_URL,
        model=os.getenv("MATERIALS_EMBEDDING_MODEL")
        or os.getenv("EMBEDDING_MODEL")
        or "text-embedding-v4",
        dimensions=int(dimensions_raw),
        batch_size=max(1, int(batch_size_raw)),
        timeout_seconds=max(10, int(timeout_raw)),
    )


def embedding_api_available(settings: EmbeddingSettings | None = None) -> bool:
    settings = settings or load_embedding_settings()
    return bool(settings.api_key)


def embed_texts(
    texts: list[str],
    *,
    settings: EmbeddingSettings | None = None,
    usage_metrics: dict[str, Any] | None = None,
) -> list[list[float]]:
    if not texts:
        return []

    settings = settings or load_embedding_settings()
    if not settings.api_key:
        raise RuntimeError("DashScope embedding API key is not configured")

    from openai import OpenAI

    client = OpenAI(
        api_key=settings.api_key,
        base_url=settings.base_url,
        timeout=settings.timeout_seconds,
        max_retries=0,
    )

    embeddings: list[list[float]] = []
    prompt_tokens = 0
    total_tokens = 0
    started_at = time.perf_counter()

    for start in range(0, len(texts), settings.batch_size):
        batch = texts[start : start + settings.batch_size]
        response = client.embeddings.create(
            model=settings.model,
            input=batch,
            dimensions=settings.dimensions,
            encoding_format="float",
        )
        usage = getattr(response, "usage", None)
        prompt_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
        total_tokens += int(getattr(usage, "total_tokens", 0) or 0)
        embeddings.extend([list(item.embedding) for item in response.data])

    if len(embeddings) != len(texts):
        raise RuntimeError("Embedding response count does not match input count")

    if usage_metrics is not None:
        latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
        usage_metrics.update(
            {
                "model": settings.model,
                "dimensions": settings.dimensions,
                "input_count": len(texts),
                "prompt_tokens": prompt_tokens,
                "total_tokens": total_tokens or prompt_tokens,
                "latency_ms": latency_ms,
            }
        )

    return embeddings
