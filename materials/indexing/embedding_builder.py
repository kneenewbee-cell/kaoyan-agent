"""
materials/indexing/embedding_builder.py — Embedding 构建。

MVP 阶段使用 mock/local hash，不强制依赖外部 embedding 服务。
"""

from __future__ import annotations

import hashlib
import os


def build_embedding(text: str) -> list[float]:
    """
    构建文本 embedding。

    MVP 阶段使用 hash-based mock：
    - 基于文本的 SHA-256 生成确定性的 float 序列。
    - 不是真正的语义 embedding，但保证同一文本每次生成相同结果。

    后续可替换为调用 embedding API 或加载本地模型。
    """
    # 尝试使用项目现有 embedding
    # 例如：dashscope API、Qwen embedding 等
    # 此处先使用 mock hash

    hash_bytes = hashlib.sha256(text.encode("utf-8")).digest()
    # 将 32 字节转为 32 维 float 向量
    dim = 32
    embedding: list[float] = []
    for i in range(dim):
        val = hash_bytes[i] / 255.0
        embedding.append(val)
    return embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度。"""
    if len(a) != len(b) or len(a) == 0:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)
