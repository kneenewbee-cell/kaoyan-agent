from __future__ import annotations

import unittest

from materials.chunking.chunker import chunk_markdown
from materials.postprocess.marker_parser import (
    parse_decimal_outline_marker,
    parse_label_ordinal_marker,
)
from materials.postprocess.structure_normalizer import normalize_markdown_structure
from materials.postprocess.structure_strategy import (
    get_default_structure_strategy,
    validate_structure_strategy,
)


KNOWLEDGE_SAMPLE = """考研数学高等数学五大核心知识点及讲解
=====================================

知识点一：极限的计算（七种未定式）

【考频】★★★★★
【难度】★★★☆☆

核心概念
极限是高等数学的基石。

常用计算方法
（1）等价无穷小替换
（2）洛必达法则

经典例题
求 lim...

易错提醒
不要乱用等价无穷小。

知识点二：导数的定义与微分中值定理

导数定义
f'(x0)=...
"""


class StructureStrategyTest(unittest.TestCase):
    def _normalize(self, text: str, strategy: dict | None = None) -> tuple[str, dict]:
        return normalize_markdown_structure(text, strategy=strategy)

    def test_knowledge_point_sections_and_chunks(self) -> None:
        normalized, report = self._normalize(KNOWLEDGE_SAMPLE)
        self.assertIn("# 考研数学高等数学五大核心知识点及讲解", normalized)
        self.assertIn("## 知识点一：极限的计算（七种未定式）", normalized)
        self.assertIn("## 知识点二：导数的定义与微分中值定理", normalized)
        self.assertNotIn("### 核心概念", normalized)
        self.assertNotIn("### 常用计算方法", normalized)
        self.assertIn("（1）等价无穷小替换", normalized)
        self.assertEqual(report["main_section_count"], 2)

        chunks = chunk_markdown(normalized, "mat_test", "tester")
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["split_reason"], "section")

    def test_custom_key_point_strategy(self) -> None:
        sample = """考研数学高等数学五大核心要点（新版）
=====================================

要点一：极限的求解策略

未定式识别
直接代入得到 0/0 时需要特殊方法。

核心方法
（1）等价无穷小
（2）洛必达

要点二：导数定义与中值定理的综合应用

导数定义的变形
...
"""
        strategy = get_default_structure_strategy()
        strategy["main_section_rule"].update({"aliases": ["要点"], "number_styles": ["chinese"]})
        normalized, _ = self._normalize(sample, strategy)
        self.assertIn("## 要点一：极限的求解策略", normalized)
        self.assertIn("## 要点二：导数定义与中值定理的综合应用", normalized)
        for short_line in ("未定式识别", "核心方法", "导数定义的变形"):
            self.assertNotIn(f"### {short_line}", normalized)
        self.assertEqual(len([c for c in chunk_markdown(normalized, "mat", "tester", strategy=strategy) if len(c.heading_path) == 2]), 2)

    def test_decimal_outline_without_synthetic_parents(self) -> None:
        sample = """考研数学高等数学五大难点突破
============================

1.1 极限计算中的陷阱

等价无穷小替换的黄金法则
只能在乘除因子中替换。

1.2 导数定义与分段函数可导性的判定

导数定义的多种形式
...

2.1 微分中值定理

辅助函数构造
...
"""
        strategy = get_default_structure_strategy()
        strategy["main_section_rule"] = {
            "family": "decimal_outline_marker",
            "target_level": 2,
            "observed_depth": 2,
            "treat_observed_depth_as_main_level": True,
            "do_not_create_missing_parent_sections": True,
        }
        normalized, report = self._normalize(sample, strategy)
        for title in ("1.1 极限计算中的陷阱", "1.2 导数定义与分段函数可导性的判定", "2.1 微分中值定理"):
            self.assertIn(f"## {title}", normalized)
        self.assertNotRegex(normalized, r"(?m)^## [12]$")
        self.assertNotIn("### 辅助函数构造", normalized)
        self.assertEqual(report["main_section_count"], 3)
        self.assertEqual(len([c for c in chunk_markdown(normalized, "mat", "tester", strategy=strategy) if len(c.heading_path) == 2]), 3)

    def test_partial_strategy_is_safely_merged(self) -> None:
        partial = {
            "main_section_rule": {
                "family": "decimal_outline_marker",
                "target_level": 2,
                "observed_depth": 2,
                "min_repeats": 1,
            }
        }
        validated = validate_structure_strategy(partial)
        self.assertEqual(validated["main_section_rule"]["family"], "decimal_outline_marker")
        self.assertEqual(validated["chunk_rule"]["max_chars"], 1800)

    def test_marker_anchoring_and_strategy_fallback(self) -> None:
        self.assertIsNotNone(parse_label_ordinal_marker("知识点1：极限", ["知识点"]))
        self.assertIsNone(parse_label_ordinal_marker("正文中的知识点1：极限", ["知识点"]))
        self.assertIsNone(parse_label_ordinal_marker("  知识点1：极限", ["知识点"]))
        self.assertIsNotNone(parse_decimal_outline_marker("1.2 标题"))
        self.assertIsNone(parse_decimal_outline_marker("版本 1.2.0 已发布"))
        invalid = get_default_structure_strategy()
        invalid["chunk_rule"]["max_chars"] = 99
        validated = validate_structure_strategy(invalid)
        self.assertEqual(validated["chunk_rule"]["max_chars"], 1800)
        self.assertTrue(validated["_validation_warnings"])


if __name__ == "__main__":
    unittest.main()
