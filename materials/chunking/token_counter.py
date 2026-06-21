"""
materials/chunking/token_counter.py — Token 估算。

简单的中英文混合 token 估算，不做精确 tokenization。
"""

from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """
    估算文本 token 数。

    简单规则：
    - 英文：~4 字符/token
    - 中文：~1.5 字符/token
    - 混合采用保守估算：~2 字符/token
    """
    if not text:
        return 0

    # 统计中文字符数
    chinese_chars = sum(1 for ch in text if "一" <= ch <= "鿿")
    other_chars = len(text) - chinese_chars

    # 中文约 1.5 字符/token，其他约 4 字符/token
    tokens = (chinese_chars / 1.5) + (other_chars / 4.0)
    return max(1, int(tokens))
