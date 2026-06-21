"""
materials/postprocess/formula_cleaner.py — 公式文本轻度修复。

MVP 阶段做最小处理：不破坏 LaTeX，不删除公式。
"""

from __future__ import annotations


def clean_formulas(markdown: str) -> str:
    """
    对 Markdown 中 LaTeX 公式做轻度修复。

    规则（保守）：
    1. 确保 $$ 和 $ 成对出现的基本合理性标记。
    2. 不改变公式内容。
    3. 不做大规模改写。

    MVP 阶段基本原样返回。
    """
    # TODO: 后续可添加公式块完整性修复
    return markdown
