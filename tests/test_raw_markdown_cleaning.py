from __future__ import annotations

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from materials.postprocess.raw_markdown_cleaner import clean_raw_markdown
from materials.postprocess.qwen_strategy_client import write_qwen_strategy_log
from materials.postprocess.strategy_validator import validate_cleaning_strategy
from materials.chunking.chunker import chunk_markdown
from materials.quality.report import build_quality_report
from materials.schemas import Chunk


def valid_strategy() -> dict:
    return {
        "version": "1.0",
        "document_profile": {
            "subject": "math",
            "document_type": "knowledge_notes",
            "language": "zh",
            "confidence": 0.9,
        },
        "main_section_rule": {
            "enabled": True,
            "target_level": 2,
            "marker_type": "label_ordinal",
            "aliases": ["知识点"],
            "number_styles": ["chinese"],
            "requires_line_start": True,
            "requires_colon": False,
            "min_repeats": 2,
            "examples": ["知识点一：极限", "知识点二：导数"],
        },
        "subsection_rules": [
            {
                "enabled": True,
                "target_level": 3,
                "type": "fixed_label",
                "aliases": ["核心概念", "经典例题", "易错提醒"],
                "requires_line_start": True,
                "min_repeats": 1,
            }
        ],
        "metadata_rules": {
            "recognize_bracket_fields": True,
            "fields": ["考频", "难度", "题型", "来源", "备注"],
        },
        "cleanup_rules": {
            "normalize_blank_lines": True,
            "strip_trailing_spaces": True,
            "remove_control_chars": True,
            "preserve_tables": True,
            "preserve_code_blocks": True,
            "preserve_formulas": True,
            "preserve_images": True,
        },
        "fallback_policy": {
            "if_main_sections_less_than": 2,
            "action": "keep_original_structure",
            "chunk_by": "length",
            "reason": "主标题命中不足时不强行改写结构",
        },
        "safety_rules": {
            "do_not_rewrite_content": True,
            "do_not_summarize": True,
            "do_not_translate": True,
            "do_not_delete_unknown_lines": True,
        },
    }


def dsl_strategy(*heading_rules: dict) -> dict:
    strategy = valid_strategy()
    strategy["version"] = "1.1"
    strategy["main_section_rule"]["enabled"] = False
    strategy["main_section_rule"]["marker_type"] = "none"
    strategy["subsection_rules"] = []
    strategy["heading_rules"] = list(heading_rules)
    return strategy


def token(token_type: str, **kwargs) -> dict:
    return {"type": token_type, **kwargs}


class RawMarkdownCleaningTest(unittest.TestCase):
    def test_valid_strategy_json_passes_validation(self) -> None:
        strategy, warnings, used_fallback = validate_cleaning_strategy(valid_strategy(), fallback_source="qwen")
        self.assertFalse(used_fallback)
        self.assertEqual(warnings, [])
        self.assertEqual(strategy.main_section_rule.marker_type, "label_ordinal")

    def test_non_json_qwen_output_falls_back(self) -> None:
        text = "知识点一：极限\n正文\n知识点二：导数\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value="not json",
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 知识点一：极限", result.cleaned_markdown)
        self.assertEqual(result.strategy["strategy_source"], "local")
        self.assertIn("qwen_strategy_invalid_fallback_to_local", result.warnings)

    def test_dangerous_strategy_is_rejected(self) -> None:
        strategy, warnings, used_fallback = validate_cleaning_strategy({"eval": "print(1)"})
        self.assertTrue(used_fallback)
        self.assertEqual(strategy.main_section_rule.marker_type, "none")
        self.assertIn("strategy_rejected_dangerous_token", warnings)

    def test_knowledge_point_lines_convert_to_h2(self) -> None:
        result = clean_raw_markdown("知识点一：极限\n正文\n知识点二 导数的定义\n正文\n")
        self.assertIn("## 知识点一：极限", result.cleaned_markdown)
        self.assertIn("## 知识点二 导数的定义", result.cleaned_markdown)

    def test_fixed_labels_convert_to_h3(self) -> None:
        result = clean_raw_markdown(
            "知识点一：极限\n核心概念\n正文\n知识点二：导数\n经典例题\n题目\n易错提醒\n正文\n"
        )
        self.assertIn("### 核心概念", result.cleaned_markdown)
        self.assertIn("### 经典例题", result.cleaned_markdown)
        self.assertIn("### 易错提醒", result.cleaned_markdown)

    def test_chinese_outline_converts_to_h2(self) -> None:
        result = clean_raw_markdown("一、函数\n正文\n二、极限\n正文\n三、导数\n正文\n")
        self.assertIn("## 一、函数", result.cleaned_markdown)
        self.assertIn("## 二、极限", result.cleaned_markdown)
        self.assertIn("## 三、导数", result.cleaned_markdown)

    def test_existing_markdown_headings_are_not_duplicated(self) -> None:
        result = clean_raw_markdown("# 总标题\n\n## 第一节\n正文\n\n## 第二节\n正文\n")
        self.assertIn("# 总标题", result.cleaned_markdown)
        self.assertIn("## 第一节", result.cleaned_markdown)
        self.assertNotIn("## ## 第一节", result.cleaned_markdown)

    def test_code_block_is_protected(self) -> None:
        result = clean_raw_markdown(
            "知识点一：极限\n正文\n知识点二：导数\n正文\n```python\n知识点一：不要识别我\n```\n"
        )
        self.assertIn("```python\n知识点一：不要识别我\n```", result.cleaned_markdown)
        self.assertNotIn("## 知识点一：不要识别我", result.cleaned_markdown)

    def test_table_line_is_protected(self) -> None:
        result = clean_raw_markdown(
            "知识点一：极限\n正文\n知识点二：导数\n正文\n| 知识点一：不要识别我 | 内容 |\n| --- | --- |\n"
        )
        self.assertIn("| 知识点一：不要识别我 | 内容 |", result.cleaned_markdown)
        self.assertNotIn("## | 知识点一：不要识别我 | 内容 |", result.cleaned_markdown)

    def test_single_main_candidate_does_not_force_structure(self) -> None:
        result = clean_raw_markdown("知识点一：极限\n正文\n")
        self.assertNotIn("## 知识点一：极限", result.cleaned_markdown)
        self.assertIn("知识点一：极限", result.cleaned_markdown)
        self.assertEqual(result.strategy["strategy_source"], "default")

    def test_qwen_usage_is_written_to_report_and_jsonl(self) -> None:
        payload = valid_strategy()

        def fake_generate(probe, **kwargs):
            kwargs["usage_metrics"].update(
                {
                    "model": "qwen3.6-plus-2026-04-02",
                    "latency_ms": 123.4,
                    "prompt_tokens": 100,
                    "completion_tokens": 20,
                    "total_tokens": 120,
                    "api_success": True,
                }
            )
            return payload

        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            side_effect=fake_generate,
        ), patch(
            "materials.postprocess.qwen_strategy_client.QWEN_LOG_DIR",
            Path(temp_dir),
        ):
            result = clean_raw_markdown(
                "知识点一：极限\n正文\n知识点二：导数\n正文\n",
                source_name="test.txt",
                use_llm_profile=True,
            )
            usage = result.parse_report["qwen_usage"]
            self.assertEqual(usage["total_tokens"], 120)
            self.assertEqual(usage["final_strategy_source"], "qwen")
            log_files = list(Path(temp_dir).glob("material_cleaning_qwen_*.jsonl"))
            self.assertEqual(len(log_files), 1)
            record = json.loads(log_files[0].read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(record["latency_ms"], 123.4)
            self.assertEqual(record["prompt_tokens"], 100)

    def test_declarative_rules_support_mixed_408_heading_styles(self) -> None:
        payload = dsl_strategy(
            {
                "id": "module",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["模块"]),
                    token("ordinal", styles=["chinese"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "exam_point",
                "role": "main",
                "target_level": 3,
                "parent_rule": "module",
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["考点"]),
                    token("ordinal", styles=["arabic"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "chinese_outline",
                "role": "main",
                "target_level": 3,
                "parent_rule": "module",
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("ordinal", styles=["chinese"]),
                    token("separator", values=["、"]),
                    token("title_text"),
                ],
            },
            {
                "id": "arabic_outline",
                "role": "main",
                "target_level": 3,
                "parent_rule": "module",
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("ordinal", styles=["arabic"]),
                    token("separator", values=[".", "、"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
        )
        text = """# 408 笔记
模块一 数据结构
考点1 线性表
正文
考点2 栈
正文
模块二 树
一、二叉树
正文
二、遍历
正文
模块三 组成原理
1. 存储系统
正文
2. 指令系统
正文
"""
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 模块一 数据结构", result.cleaned_markdown)
        self.assertIn("### 考点1 线性表", result.cleaned_markdown)
        self.assertIn("### 一、二叉树", result.cleaned_markdown)
        self.assertIn("### 1. 存储系统", result.cleaned_markdown)
        self.assertEqual(result.parse_report["stats"]["active_heading_rules"], 4)

    def test_declarative_rules_keep_chapter_and_section_hierarchy(self) -> None:
        payload = dsl_strategy(
            {
                "id": "chapter",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese", "arabic"]),
                    token("literal", values=["章"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "section",
                "role": "main",
                "target_level": 3,
                "parent_rule": "chapter",
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese", "arabic"]),
                    token("literal", values=["节"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
        )
        text = "第一章 函数\n第一节 定义\n正文\n第二节 性质\n正文\n第二章 极限\n第一节 概念\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 第一章 函数", result.cleaned_markdown)
        self.assertIn("### 第一节 定义", result.cleaned_markdown)
        self.assertNotIn("## 第一节 定义", result.cleaned_markdown.splitlines())

    def test_unmatched_strategy_rule_reduces_quality_confidence(self) -> None:
        chunks = [
            Chunk(
                chunk_id="c1",
                material_id="m1",
                user_id="tester",
                chunk_index=0,
                text="正文" * 60,
                heading_path=["标题"],
                token_count=60,
            )
        ]
        report = build_quality_report(
            "# 标题\n\n" + "正文" * 60,
            chunks=chunks,
            postprocess_warnings=["strategy_rule_not_matched:section"],
        )
        self.assertLess(report.structure_confidence, 1.0)
        self.assertIn("strategy_execution_incomplete", report.warnings)

    def test_sentence_like_numbered_body_lines_are_not_headings(self) -> None:
        payload = dsl_strategy(
            {
                "id": "exam_point",
                "role": "main",
                "target_level": 2,
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["考点"]),
                    token("ordinal", styles=["arabic"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
        )
        text = (
            "考点1 线性表\n"
            "考点1 线性表 第1段：本段是正文，不应被提升为标题。\n"
            "考点2 栈和队列\n"
            "考点2 栈和队列 第1段：本段是正文，不应被提升为标题。\n"
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 考点1 线性表", result.cleaned_markdown)
        self.assertIn("考点1 线性表 第1段：本段是正文，不应被提升为标题。", result.cleaned_markdown)
        self.assertNotIn("## 考点1 线性表 第1段", result.cleaned_markdown)

    def test_long_english_example_sentence_is_not_heading(self) -> None:
        payload = dsl_strategy(
            {
                "id": "example",
                "role": "subsection",
                "target_level": 3,
                "priority": 80,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["Example:"]),
                    token("whitespace", optional=False),
                    token("title_text"),
                ],
            },
        )
        text = (
            "Example: The argument is valid only when the hidden assumption is accepted.\n"
            "正文\n"
            "Example: The option is wrong because it changes the original condition.\n"
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertNotIn("### Example: The argument", result.cleaned_markdown)

    def test_chapter_summary_level_is_coerced_below_chapter(self) -> None:
        payload = dsl_strategy(
            {
                "id": "chapter",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 2,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese"]),
                    token("literal", values=["章"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "summary",
                "role": "main",
                "target_level": 2,
                "parent_rule": "chapter",
                "priority": 95,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese"]),
                    token("literal", values=["章"]),
                    token("literal", values=["小结"]),
                ],
            },
        )
        text = "第一章 函数与极限\n正文\n第一章小结\n正文\n第二章 导数与微分\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 第一章 函数与极限", result.cleaned_markdown)
        self.assertIn("### 第一章小结", result.cleaned_markdown)
        self.assertNotIn("## 第一章小结", result.cleaned_markdown.splitlines())

    def test_fixed_concept_labels_are_coerced_from_h5_to_h4(self) -> None:
        payload = dsl_strategy(
            {
                "id": "chapter",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese"]),
                    token("literal", values=["章"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "section",
                "role": "main",
                "target_level": 3,
                "parent_rule": "chapter",
                "priority": 80,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["第"]),
                    token("ordinal", styles=["chinese"]),
                    token("literal", values=["节"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "concept_block",
                "role": "subsection",
                "target_level": 5,
                "parent_rule": "section",
                "priority": 70,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["定义", "核心概念", "经典例题"]),
                ],
            },
        )
        text = "第一章 函数\n第一节 基本概念\n定义\n正文\n核心概念\n正文\n经典例题\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("#### 定义", result.cleaned_markdown)
        self.assertIn("#### 核心概念", result.cleaned_markdown)
        self.assertIn("#### 经典例题", result.cleaned_markdown)
        self.assertNotIn("##### 定义", result.cleaned_markdown)

    def test_chunker_ignores_headings_inside_code_fences(self) -> None:
        markdown = (
            "# 保护场景\n\n"
            "## 知识点一：函数极限\n\n"
            "```python\n"
            "# 知识点三：代码块里的标题\n"
            "print('核心概念')\n"
            "```\n\n"
            "## 知识点二：导数应用\n\n"
            "正文\n"
        )
        chunks = chunk_markdown(markdown, "mat_test", "tester")
        paths = [chunk.heading_path for chunk in chunks]
        self.assertIn(["保护场景", "知识点一：函数极限"], paths)
        self.assertIn(["保护场景", "知识点二：导数应用"], paths)
        self.assertFalse(any("代码块里的标题" in " / ".join(path) for path in paths))


if __name__ == "__main__":
    unittest.main()
