from __future__ import annotations

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch

from materials.postprocess.raw_markdown_cleaner import clean_raw_markdown
from materials.postprocess.qwen_strategy_client import write_qwen_strategy_log
from materials.postprocess.document_zones import validate_document_zones_payload
from materials.postprocess.document_zones import default_document_zones
from materials.postprocess.strategy_cleaner import clean_with_strategy
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


def dsl_strategy(*legacy_rules: dict) -> dict:
    strategy = valid_strategy()
    strategy["version"] = "1.1"
    strategy["main_section_rule"]["enabled"] = False
    strategy["main_section_rule"]["marker_type"] = "none"
    strategy["subsection_rules"] = []
    strategy["heading_families"] = []
    strategy["relation_hints"] = []
    for rule in legacy_rules:
        family_payload = _family_from_legacy_rule(rule)
        strategy["heading_families"].append(family_payload)
        if rule.get("parent_rule"):
            strategy["relation_hints"].append(_relation_hint(str(rule["parent_rule"]), family_payload["id"]))
    return strategy


def family_strategy(*heading_families: dict) -> dict:
    strategy = valid_strategy()
    strategy["version"] = "1.2"
    strategy["main_section_rule"]["enabled"] = False
    strategy["main_section_rule"]["marker_type"] = "none"
    strategy["subsection_rules"] = []
    strategy["heading_families"] = list(heading_families)
    return strategy


def token(token_type: str, **kwargs) -> dict:
    return {"type": token_type, **kwargs}


def _relation_hint(parent: str, child: str) -> dict:
    return {
        "relation_type": "direct_parent",
        "parent": parent,
        "child": child,
        "score": 90,
        "certainty": "strong",
        "score_breakdown": {
            "interval_structure": 20,
            "coverage_density": 20,
            "numbering_anchor": 15,
            "sample_evidence": 15,
            "counter_evidence": 0,
        },
        "evidence": [f"{parent}>{child}"],
    }


def _family_from_legacy_rule(rule: dict) -> dict:
    pattern = [item for item in (rule.get("pattern") or []) if isinstance(item, dict)]
    anchors: list[str] = []
    anchor_position = "line_start"
    ordinal_styles: list[str] = []
    ordinal_required = False
    units: list[str] = []
    separators = ["", " ", "、", ".", "．", "：", ":"]
    title_required = True
    kind = "block" if rule.get("role") == "main" else "item"

    if len(pattern) == 1 and pattern[0].get("type") == "title_text":
        anchors = list(rule.get("examples") or [])
        anchor_position = "exact"
        title_required = False
        kind = "major_section"
    elif len(pattern) == 1 and pattern[0].get("type") == "literal":
        anchors = list(pattern[0].get("values") or [])
        anchor_position = "exact"
        title_required = False
    elif (
        len(pattern) >= 3
        and pattern[0].get("type") == "literal"
        and pattern[1].get("type") == "ordinal"
        and pattern[2].get("type") == "literal"
        and (pattern[0].get("values") or [None])[0] in {"(", "（"}
        and (pattern[2].get("values") or [None])[0] in {")", "）"}
    ):
        ordinal_styles = ["paren_arabic" if "arabic" in pattern[1].get("styles", []) else "paren_chinese"]
        kind = "outline"
    elif pattern and pattern[0].get("type") == "literal":
        anchors = list(pattern[0].get("values") or [])
        if anchors and all(str(value)[:1] in "①②③④⑤⑥⑦⑧⑨" for value in anchors):
            anchors = []
            ordinal_styles = ["circled"]
            kind = "outline"
        elif any(item.get("type") == "ordinal" for item in pattern):
            ordinal_token = next(item for item in pattern if item.get("type") == "ordinal")
            ordinal_styles = list(ordinal_token.get("styles") or [])
            ordinal_required = True
            literal_tokens = [item for item in pattern[1:] if item.get("type") == "literal"]
            if literal_tokens and anchors == ["第"]:
                units = list(literal_tokens[0].get("values") or [])
                kind = "strong_boundary"
    elif pattern and pattern[0].get("type") == "ordinal":
        ordinal_styles = list(pattern[0].get("styles") or [])
        kind = "outline"
        for item in pattern:
            if item.get("type") == "separator":
                separators = list(item.get("values") or separators)

    return {
        "id": str(rule.get("id") or "legacy_family"),
        "enabled": True,
        "kind": kind,
        "anchors": anchors,
        "anchor_position": anchor_position,
        "ordinal_styles": ordinal_styles,
        "ordinal_required": ordinal_required,
        "units": units,
        "separators": separators,
        "title_required": title_required,
        "parent_hints": [rule["parent_rule"]] if rule.get("parent_rule") else [],
        "min_repeats": int(rule.get("min_repeats") or 1),
        "examples": list(rule.get("examples") or [])[:8],
    }


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

    def test_legacy_heading_rules_are_dropped_from_strategy_output(self) -> None:
        payload = valid_strategy()
        payload["heading_rules"] = [
            {
                "id": "legacy",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [token("literal", values=["LEGACY"]), token("title_text")],
            }
        ]
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback)
        self.assertNotIn("heading_rules", strategy.to_dict())
        self.assertIn("strategy_legacy_heading_rules_dropped", warnings)

    def test_legacy_heading_rules_do_not_drive_cleaning(self) -> None:
        payload = valid_strategy()
        payload["main_section_rule"]["enabled"] = False
        payload["main_section_rule"]["marker_type"] = "none"
        payload["subsection_rules"] = []
        payload["heading_rules"] = [
            {
                "id": "legacy",
                "role": "main",
                "target_level": 2,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [token("literal", values=["LEGACY"]), token("title_text")],
            }
        ]
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown("LEGACY Title\nbody\n", use_llm_profile=True)
        self.assertIn("LEGACY Title", result.cleaned_markdown.splitlines())
        self.assertNotIn("## LEGACY Title", result.cleaned_markdown.splitlines())
        self.assertNotIn("heading_rules", result.strategy)

    def test_qwen_strategy_model_reads_dotenv_lazily(self) -> None:
        from materials.postprocess.qwen_strategy_client import get_qwen_strategy_model

        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text("QWEN_CLEANING_STRATEGY_MODEL=glm-test-model\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(get_qwen_strategy_model(env_path=env_path), "glm-test-model")

    def test_parse_report_records_actual_qwen_strategy_model(self) -> None:
        with (
            patch("materials.postprocess.raw_markdown_cleaner.get_qwen_strategy_model", return_value="glm-test-model"),
            patch("materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen", return_value=valid_strategy()),
            patch(
                "materials.postprocess.raw_markdown_cleaner.generate_document_zones_with_qwen",
                return_value=default_document_zones().model_dump(mode="json"),
            ),
        ):
            result = clean_raw_markdown("知识点一：极限\n正文\n知识点二：导数\n正文\n", use_llm_profile=True)
        self.assertEqual(result.parse_report["qwen_model"], "glm-test-model")

    def test_strategy_validator_repairs_benign_qwen_shape_errors(self) -> None:
        payload = dsl_strategy(
            {
                "id": "parent",
                "role": "main",
                "target_level": 3,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [token("literal", values=["一、"]), token("title_text")],
            },
            {
                "id": "child",
                "role": "subsection",
                "target_level": 2,
                "parent_rule": "parent",
                "priority": 80,
                "min_repeats": 1,
                "pattern": [token("literal", values=["（一）"]), token("title_text")],
                "examples": [f"例{i}" for i in range(12)],
            },
        )
        diagnostics: dict = {}
        strategy, warnings, used_fallback = validate_cleaning_strategy(
            payload,
            fallback_source="qwen",
            diagnostics=diagnostics,
        )
        self.assertFalse(used_fallback)
        self.assertNotIn("heading_rules", strategy.to_dict())
        self.assertEqual(len(strategy.heading_families), 2)
        self.assertEqual(strategy.heading_families[1].parent_hints, ["parent"])
        self.assertEqual(diagnostics["result"], "valid")

    def test_strategy_validator_drops_impossible_h6_parent_rule(self) -> None:
        payload = dsl_strategy(
            {
                "id": "parent",
                "role": "subsection",
                "target_level": 6,
                "priority": 80,
                "min_repeats": 1,
                "pattern": [token("literal", values=["1."]), token("title_text")],
            },
            {
                "id": "child",
                "role": "subsection",
                "target_level": 6,
                "parent_rule": "parent",
                "priority": 70,
                "min_repeats": 1,
                "pattern": [token("literal", values=["(1)"]), token("title_text")],
            },
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback)
        self.assertNotIn("heading_rules", strategy.to_dict())
        self.assertEqual(len(strategy.heading_families), 2)
        self.assertEqual(strategy.relation_hints[0].parent, "parent")

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
        self.assertEqual(result.parse_report["stats"]["active_heading_families"], 4)

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

    def test_llm_repeated_chapter_rules_are_not_allowed_to_create_h1(self) -> None:
        payload = dsl_strategy(
            {
                "id": "chapter",
                "role": "main",
                "target_level": 1,
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
                "target_level": 2,
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
        )
        text = "# 第一章 函数极限连续\n正文\n# 第一节 函数\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 第一章 函数极限连续", result.cleaned_markdown)
        self.assertIn("### 第一节 函数", result.cleaned_markdown)
        self.assertNotIn("# 第一章 函数极限连续", result.cleaned_markdown.splitlines())
        self.assertNotIn("## 第一节 函数", result.cleaned_markdown.splitlines())

    def test_inactive_parent_rule_does_not_leave_existing_children_as_h1(self) -> None:
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
                "id": "outline",
                "role": "main",
                "target_level": 4,
                "parent_rule": "section",
                "priority": 70,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["一、"]),
                    token("title_text"),
                ],
            },
            {
                "id": "paren_outline",
                "role": "subsection",
                "target_level": 5,
                "parent_rule": "outline",
                "priority": 60,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["("]),
                    token("ordinal", styles=["chinese"]),
                    token("literal", values=[")"]),
                    token("title_text"),
                ],
            },
        )
        text = "# 第一章 函数\n# 第一节 函数\n# 一、考试内容\n# (一)函数概念\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        self.assertIn("## 第一章 函数", result.cleaned_markdown)
        self.assertIn("### 第一节 函数", result.cleaned_markdown)
        self.assertIn("#### 一、考试内容", result.cleaned_markdown)
        self.assertIn("##### (一)函数概念", result.cleaned_markdown)
        self.assertNotIn("# (一)函数概念", result.cleaned_markdown.splitlines())

    def test_untrusted_existing_h1_is_demoted_to_plain_or_local_label(self) -> None:
        text = (
            "# 第二章 一元函数微分学\n"
            "# 第一节 导数与微分\n"
            "# 高等数学辅导讲义\n"
            "正文\n"
            "# 高等数学辅导讲义\n"
            "正文\n"
            "# 高等数学辅导讲义\n"
            "正文\n"
            "# 常用的方法有三种\n"
            "正文\n"
            "# （方法二）直接法\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("高等数学辅导讲义", lines)
        self.assertIn("常用的方法有三种", lines)
        self.assertIn("**方法二：** 直接法", lines)
        self.assertNotIn("# 高等数学辅导讲义", lines)
        self.assertNotIn("# 常用的方法有三种", lines)
        self.assertNotIn("# （方法二）直接法", lines)
        self.assertGreaterEqual(result.parse_report["stats"]["untrusted_headings_demoted"], 4)

    def test_local_detector_prefers_existing_markdown_over_plain_arabic_items(self) -> None:
        text = (
            "# 第一章 函数\n"
            "# 第一节 函数\n"
            "# 一、考试内容\n"
            "# （一）函数概念\n"
            "# 二、常考题型\n"
            "1. 普通条目\n"
            "正文\n"
            "2. 普通条目\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        self.assertEqual(result.strategy["main_section_rule"]["marker_type"], "existing_markdown")
        self.assertNotIn("## 1. 普通条目", result.cleaned_markdown.splitlines())
        self.assertNotIn("## 2. 普通条目", result.cleaned_markdown.splitlines())

    def test_existing_mineru_like_headings_are_releveled(self) -> None:
        text = (
            "## 第二章 一元函数微分学\n"
            "正文\n"
            "## 第一节 导数与微分\n"
            "正文\n"
            "## 考试内容要点精讲\n"
            "正文\n"
            "## （一）导数概念\n"
            "正文\n"
            "## 注类似地，\n"
            "正文\n"
            "## 题型二 导数的几何意义\n"
            "正文\n"
            "## 解 （方法一）直接法\n"
            "正文\n"
            "## 证明由泰勒公式知\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        self.assertIn("## 第二章 一元函数微分学", result.cleaned_markdown)
        self.assertIn("### 第一节 导数与微分", result.cleaned_markdown)
        self.assertIn("#### 考试内容要点精讲", result.cleaned_markdown)
        self.assertIn("#### （一）导数概念", result.cleaned_markdown)
        self.assertNotIn("## 注类似地，", result.cleaned_markdown.splitlines())
        self.assertNotIn("#### 注类似地，", result.cleaned_markdown.splitlines())
        self.assertIn("**注：** 类似地，", result.cleaned_markdown)
        self.assertNotIn("## 题型二 导数的几何意义", result.cleaned_markdown.splitlines())
        self.assertIn("#### 题型二 导数的几何意义", result.cleaned_markdown)
        self.assertNotIn("## 解 （方法一）直接法", result.cleaned_markdown.splitlines())
        self.assertNotIn("#### 解 （方法一）直接法", result.cleaned_markdown.splitlines())
        self.assertIn("**解：** （方法一）直接法", result.cleaned_markdown)
        self.assertNotIn("## 证明由泰勒公式知", result.cleaned_markdown.splitlines())
        self.assertNotIn("#### 证明由泰勒公式知", result.cleaned_markdown.splitlines())
        self.assertIn("**证明：** 由泰勒公式知", result.cleaned_markdown)
        self.assertEqual(result.parse_report["stats"]["local_labels_demoted"], 3)

    def test_body_like_labels_are_demoted_but_structural_method_titles_remain(self) -> None:
        text = (
            "## 常用方法\n"
            "正文\n"
            "## 方法一 直接法\n"
            "正文\n"
            "## 分析这是一个1°型极限\n"
            "正文\n"
            "## 证明方法总结\n"
            "正文\n"
            "## 注意事项\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        self.assertIn("#### 常用方法", result.cleaned_markdown)
        self.assertIn("**方法一：** 直接法", result.cleaned_markdown)
        self.assertIn("**分析：** 这是一个1°型极限", result.cleaned_markdown)
        self.assertIn("#### 证明方法总结", result.cleaned_markdown)
        self.assertIn("#### 注意事项", result.cleaned_markdown)
        self.assertNotIn("#### 方法一 直接法", result.cleaned_markdown.splitlines())
        self.assertNotIn("#### 分析这是一个1°型极限", result.cleaned_markdown.splitlines())

    def test_html_table_blocks_are_counted_collapsed_and_protected(self) -> None:
        from materials.postprocess.format_probe import build_format_probe

        text = (
            "# 表格资料\n\n"
            "<table><tr><td>知识点一：表格里的内容</td></tr></table>\n\n"
            "知识点一：正文标题\n"
            "正文\n"
            "知识点二：正文标题\n"
            "正文\n"
        )
        probe = build_format_probe(text, filename="table.md").to_dict()
        self.assertEqual(probe["table_like_lines_count"], 1)
        self.assertIn("[HTML_TABLE_BLOCK omitted", probe["head_excerpt"])

        result = clean_raw_markdown(text, use_llm_profile=False)
        self.assertIn("<table><tr><td>知识点一：表格里的内容</td></tr></table>", result.cleaned_markdown)
        self.assertNotIn("## <table>", result.cleaned_markdown)
        self.assertIn("## 知识点一：正文标题", result.cleaned_markdown)

    def test_format_probe_exposes_heading_outline_patterns(self) -> None:
        from materials.postprocess.format_probe import build_format_probe

        probe = build_format_probe(
            "## 第2篇函数\n"
            "## 难度：中\n"
            "## 一函数\n"
            "## ①平移变换\n"
            "正文\n",
            filename="pdf.md",
        ).to_dict()
        self.assertGreaterEqual(probe["heading_pattern_counts"]["chapter_unit"], 1)
        self.assertGreaterEqual(probe["heading_pattern_counts"]["metadata_badge"], 1)
        self.assertGreaterEqual(probe["heading_pattern_counts"]["compact_chinese_outline"], 1)
        self.assertGreaterEqual(probe["heading_pattern_counts"]["circled_outline"], 1)
        self.assertEqual(probe["heading_outline"][0]["title"], "第2篇函数")

    def test_existing_metadata_and_count_badge_headings_are_demoted(self) -> None:
        text = (
            "## 第2篇函数\n"
            "正文\n"
            "## 难度：中\n"
            "正文\n"
            "## 4个知识点\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 第2篇函数", lines)
        self.assertIn("**难度：** 中", lines)
        self.assertIn("4个知识点", lines)
        self.assertNotIn("## 难度：中", lines)
        self.assertNotIn("## 4个知识点", lines)
        self.assertIn("metadata_heading_demoted_to_label", result.warnings)

    def test_existing_circled_and_compact_pdf_headings_are_releveled(self) -> None:
        text = (
            "## 第2篇函数\n"
            "正文\n"
            "## 知识组1 函数的概念及其表示\n"
            "正文\n"
            "## 一函数\n"
            "正文\n"
            "## ①平移变换\n"
            "正文\n"
            "## ②伸缩变换\n"
            "正文\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 第2篇函数", lines)
        self.assertIn("#### 一函数", lines)
        self.assertIn("##### ①平移变换", lines)
        self.assertIn("##### ②伸缩变换", lines)
        self.assertNotIn("## 一函数", lines)
        self.assertNotIn("## ①平移变换", lines)

    def test_sentence_fragment_is_not_promoted_by_compact_chinese_rule(self) -> None:
        payload = dsl_strategy(
            {
                "id": "compact_chinese_outline",
                "role": "subsection",
                "target_level": 4,
                "priority": 80,
                "min_repeats": 1,
                "pattern": [
                    token("ordinal", styles=["chinese"]),
                    token("title_text"),
                ],
            },
        )
        text = "## 第2篇函数\n三点的坐标代人，得\n正文\n一函数\n正文\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("三点的坐标代人，得", lines)
        self.assertIn("### 一函数", lines)
        self.assertNotIn("#### 三点的坐标代人，得", lines)

    def test_existing_sentence_fragment_heading_is_demoted_to_plain(self) -> None:
        text = "## 第2篇函数\n## 三点的坐标代人，得\n正文\n"
        result = clean_raw_markdown(text, use_llm_profile=False)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("三点的坐标代人，得", lines)
        self.assertNotIn("## 三点的坐标代人，得", lines)
        self.assertIn("sentence_fragment_heading_demoted_to_plain", result.warnings)

    def test_outline_stack_keeps_late_chinese_outline_from_deep_arabic_list(self) -> None:
        payload = dsl_strategy(
            {
                "id": "section",
                "role": "main",
                "target_level": 3,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["第一节"]),
                    token("whitespace", optional=True),
                    token("title_text"),
                ],
            },
            {
                "id": "paren",
                "role": "subsection",
                "target_level": 5,
                "priority": 80,
                "min_repeats": 1,
                "pattern": [token("literal", values=["（六）"]), token("title_text")],
            },
            {
                "id": "arabic",
                "role": "subsection",
                "target_level": 6,
                "parent_rule": "paren",
                "priority": 70,
                "min_repeats": 1,
                "pattern": [
                    token("ordinal", styles=["arabic"]),
                    token("separator", values=["．"]),
                    token("title_text"),
                ],
            },
            {
                "id": "chinese_outline",
                "role": "subsection",
                "target_level": 4,
                "priority": 60,
                "min_repeats": 1,
                "pattern": [
                    token("ordinal", styles=["chinese"]),
                    token("separator", values=["、"]),
                    token("title_text"),
                ],
            },
        )
        text = "第一节 导数\n（六）求导法则\n1．有理运算法则\n2．复合函数求导法\n二、常考题型的方法与技巧\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("#### 二、常考题型的方法与技巧", lines)
        self.assertNotIn("###### 二、常考题型的方法与技巧", lines)

    def test_unmarked_existing_h2_inside_local_outline_is_demoted(self) -> None:
        text = (
            "## 第2篇函数\n"
            "## 基础知识完全解读\n"
            "## 知识组1函数的概念及其表示\n"
            "## 一函数\n"
            "## 1. 函数的概念\n"
            "## 函数的三要素\n"
            "## 1. 定义域\n"
        )
        result = clean_raw_markdown(text, use_llm_profile=False)
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("#### 一函数", lines)
        self.assertIn("#### 函数的三要素", lines)
        self.assertIn("##### 1. 定义域", lines)
        self.assertNotIn("## 函数的三要素", lines)

    def test_outline_stack_keeps_h6_parent_when_child_also_renders_h6(self) -> None:
        payload = dsl_strategy(
            {
                "id": "paren_arabic",
                "role": "subsection",
                "target_level": 6,
                "priority": 80,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["("]),
                    token("ordinal", styles=["arabic"]),
                    token("literal", values=[")"]),
                    token("title_text"),
                ],
            },
            {
                "id": "circled",
                "role": "subsection",
                "target_level": 6,
                "priority": 70,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["①", "②"]),
                    token("title_text"),
                ],
            },
        )
        text = "(1)画函数图像\n①平移变换\n②伸缩变换\n(2)确定函数图像\n"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(text, use_llm_profile=True)
        lines = result.cleaned_markdown.splitlines()
        self.assertTrue(any(line.startswith("## (1)") for line in lines))
        self.assertTrue(any(line.startswith("### ") for line in lines))
        self.assertTrue(any(line.startswith("## (2)") for line in lines))

    def test_numeric_sentence_fragment_headings_are_demoted(self) -> None:
        result = clean_raw_markdown(
            "## 第二章 一元函数微分学\n"
            "## 第一节 导数与微分\n"
            "## （3）利用泰勒级数（或泰勒公式）：\n"
            "正文\n"
            "## 2.设f（x）连续，\n"
            "正文\n",
            use_llm_profile=False,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("（3）利用泰勒级数（或泰勒公式）：", lines)
        self.assertIn("2.设f（x）连续，", lines)
        self.assertNotIn("#### （3）利用泰勒级数（或泰勒公式）：", lines)
        self.assertNotIn("#### 2.设f（x）连续，", lines)

    def test_solution_label_with_method_name_is_demoted(self) -> None:
        result = clean_raw_markdown("## 第一章 函数\n## 解直接法\n正文\n", use_llm_profile=False)
        self.assertIn("**解：** 直接法", result.cleaned_markdown)
        self.assertNotIn("## 解直接法", result.cleaned_markdown.splitlines())

    def test_explanatory_method_sentence_heading_is_demoted(self) -> None:
        result = clean_raw_markdown(
            "## 第一章 函数\n"
            "## 第二节 极限\n"
            "##### 常用的方法有三种\n"
            "(1) 洛必达法则\n"
            "##### 常用的方法有两种\n"
            "(1) 通分\n"
            "##### 常用的方法有\n"
            "(1) 有理化\n",
            use_llm_profile=False,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("常用的方法有三种", lines)
        self.assertIn("常用的方法有两种", lines)
        self.assertIn("常用的方法有", lines)
        self.assertNotIn("##### 常用的方法有三种", lines)
        self.assertNotIn("##### 常用的方法有两种", lines)
        self.assertNotIn("##### 常用的方法有", lines)

    def test_explanatory_sentence_heading_is_demoted_but_nominal_headings_remain(self) -> None:
        result = clean_raw_markdown(
            "## 第一章 函数\n"
            "#### 解函数应用题的步骤\n"
            "正文\n"
            "#### 函数零点的性质\n"
            "正文\n"
            "#### 二次函数是一种重要的函数模型，常用来解决与利润有关的最大值问题\n"
            "正文\n"
            "#### 典型16利用函数的性质解决恒成立问题一般采用分离变量法，常用下列结论\n"
            "正文\n",
            use_llm_profile=False,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("#### 解函数应用题的步骤", lines)
        self.assertIn("#### 函数零点的性质", lines)
        self.assertIn("二次函数是一种重要的函数模型，常用来解决与利润有关的最大值问题", lines)
        self.assertIn("典型16利用函数的性质解决恒成立问题一般采用分离变量法，常用下列结论", lines)
        self.assertNotIn("#### 二次函数是一种重要的函数模型，常用来解决与利润有关的最大值问题", lines)
        self.assertNotIn("#### 典型16利用函数的性质解决恒成立问题一般采用分离变量法，常用下列结论", lines)

    def test_explanatory_sentence_is_not_promoted_by_legacy_heading_rule(self) -> None:
        payload = valid_strategy()
        payload["main_section_rule"]["enabled"] = False
        payload["main_section_rule"]["marker_type"] = "none"
        payload["subsection_rules"] = []
        payload["heading_rules"] = [
            {
                "id": "method_sentence",
                "role": "subsection",
                "target_level": 4,
                "priority": 90,
                "min_repeats": 1,
                "pattern": [
                    token("literal", values=["常用的方法有三种"]),
                ],
            }
        ]
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "## 第一章 函数\n常用的方法有三种\n(1) 洛必达法则\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("常用的方法有三种", lines)
        self.assertNotIn("#### 常用的方法有三种", lines)

    def test_numbered_explanatory_sentence_heading_is_demoted(self) -> None:
        result = clean_raw_markdown(
            "## 第三篇 三角函数\n"
            "#### 2. 诱导公式\n"
            "##### (1)诱导公式可分为两大类：一类是三角函数名不变\n"
            "正文\n"
            "### (2)利用单位圆定义三角函数\n"
            "正文\n",
            use_llm_profile=False,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("(1)诱导公式可分为两大类：一类是三角函数名不变", lines)
        self.assertTrue(any(line.endswith("(2)利用单位圆定义三角函数") and line.startswith("#") for line in lines))
        self.assertNotIn("##### (1)诱导公式可分为两大类：一类是三角函数名不变", lines)

    def test_transition_sentence_caption_and_bracket_label_headings_are_demoted(self) -> None:
        result = clean_raw_markdown(
            "## 第三篇 三角函数\n"
            "### 首先利用诱导公式化简已知式子，再根据题目类型进行求值\n"
            "正文\n"
            "### 图3-1-10\n"
            "正文\n"
            "### 【分析】观察问题的条件和结论，问题即可得证\n"
            "正文\n"
            "### 【答案】ABD\n"
            "正文\n"
            "### 第四步:利用函数周期性，通过左右平移得到整个图像\n"
            "正文\n",
            use_llm_profile=False,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("首先利用诱导公式化简已知式子，再根据题目类型进行求值", lines)
        self.assertIn("图3-1-10", lines)
        self.assertIn("**分析：** 观察问题的条件和结论，问题即可得证", lines)
        self.assertIn("**答案：** ABD", lines)
        self.assertIn("**第四步：** 利用函数周期性，通过左右平移得到整个图像", lines)
        self.assertNotIn("### 首先利用诱导公式化简已知式子，再根据题目类型进行求值", lines)
        self.assertNotIn("### 图3-1-10", lines)
        self.assertNotIn("### 【分析】观察问题的条件和结论，问题即可得证", lines)
        self.assertNotIn("### 【答案】ABD", lines)
        self.assertNotIn("### 第四步:利用函数周期性，通过左右平移得到整个图像", lines)

    def test_broad_title_text_rule_only_matches_examples_or_strong_headings(self) -> None:
        payload = dsl_strategy(
            {
                "id": "semantic_main",
                "role": "main",
                "target_level": 2,
                "priority": 50,
                "min_repeats": 1,
                "pattern": [token("title_text")],
                "examples": ["考情综述"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "考情综述\n"
                "首先利用诱导公式化简已知式子，再根据题目类型进行求值\n"
                "部分(如图3-2-15),求φ.\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 考情综述", lines)
        self.assertIn("首先利用诱导公式化简已知式子，再根据题目类型进行求值", lines)
        self.assertIn("部分(如图3-2-15),求φ.", lines)
        self.assertNotIn("## 首先利用诱导公式化简已知式子，再根据题目类型进行求值", lines)
        self.assertNotIn("## 部分(如图3-2-15),求φ.", lines)

    def test_empty_layout_html_table_does_not_emit_raw_html(self) -> None:
        from materials.postprocess.layout_sidecar import parse_html_table, render_table_markdown

        raw_html = "<table><tr><td></td></tr><tr><td></td></tr></table>"
        parsed = parse_html_table(raw_html)
        rendered = render_table_markdown(
            {
                "table_id": "table_empty",
                "title": "空表",
                "columns": parsed["columns"],
                "rows": parsed["rows"],
                "raw_html": raw_html,
            }
        )
        self.assertIn("空表，已忽略", rendered)
        self.assertNotIn("<table>", rendered)

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


    def test_layout_sidecar_parses_and_replaces_html_table(self) -> None:
        from materials.postprocess.layout_sidecar import (
            build_layout_context,
            replace_html_tables_with_layout_markdown,
            save_layout_artifacts,
        )

        raw_html = (
            "<table><tr><td rowspan='2'>Exam Content</td><td colspan='2'>Requirement</td></tr>"
            "<tr><td>Math A</td><td>Math B</td></tr>"
            "<tr><td>Derivative concept</td><td>Understand</td><td>Master</td></tr></table>"
        )
        layout = {
            "pdf_info": [
                {
                    "preproc_blocks": [
                        {
                            "type": "title",
                            "level": 2,
                            "bbox": [1, 2, 3, 4],
                            "lines": [{"spans": [{"type": "text", "content": "Chapter 2"}]}],
                        },
                        {
                            "type": "table",
                            "bbox": [10, 20, 30, 40],
                            "blocks": [
                                {
                                    "lines": [
                                        {
                                            "spans": [
                                                {
                                                    "type": "table",
                                                    "html": raw_html,
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                    ]
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            layout_path = Path(temp_dir) / "layout.json"
            layout_path.write_text(json.dumps(layout), encoding="utf-8")
            context = build_layout_context(layout_path)
            self.assertEqual(context["summary"]["block_counts"]["table"], 1)
            self.assertEqual(context["tables"][0]["columns"], ["Exam Content", "Math A", "Math B"])
            self.assertEqual(context["tables"][0]["rows"][0]["Math B"], "Master")
            artifacts = save_layout_artifacts(Path(temp_dir) / "parsed", context)
            self.assertTrue((artifacts["tables_dir"] / "table_001.json").exists())
            replaced, warnings = replace_html_tables_with_layout_markdown(raw_html, context["tables"])
            self.assertEqual(warnings, [])
            self.assertIn("| Exam Content | Math A | Math B |", replaced)
            self.assertIn("| Derivative concept | Understand | Master |", replaced)

    def test_html_table_replacement_falls_back_to_raw_html_parser_when_layout_table_is_missing(self) -> None:
        from materials.postprocess.layout_sidecar import replace_html_tables_with_layout_markdown

        raw_html = "<table><tr><td>A</td><td>B</td></tr><tr><td>1</td><td>2</td></tr></table>"
        replaced, warnings = replace_html_tables_with_layout_markdown(raw_html, [])
        self.assertIn("layout_table_replacement_missing_table", warnings)
        self.assertNotIn("<table", replaced)
        self.assertIn("| A | B |", replaced)
        self.assertIn("| 1 | 2 |", replaced)

    def test_chunker_uses_h3_when_single_h2_document_has_sections(self) -> None:
        markdown = (
            "## Chapter 2\n\n"
            "### Section A\n\n"
            "body A\n\n"
            "### Section B\n\n"
            "body B\n"
        )
        chunks = chunk_markdown(markdown, "mat_test", "tester")
        paths = [chunk.heading_path for chunk in chunks]
        self.assertIn(["Chapter 2", "Section A"], paths)
        self.assertIn(["Chapter 2", "Section B"], paths)

    def test_chunker_uses_finer_headings_when_sections_are_long(self) -> None:
        long_body = "正文" * 1200
        markdown = (
            "## Chapter\n\n"
            "### Section A\n\n"
            "#### Topic A1\n\n"
            f"{long_body}\n\n"
            "#### Topic A2\n\n"
            f"{long_body}\n\n"
            "### Section B\n\n"
            "#### Topic B1\n\n"
            f"{long_body}\n"
        )
        chunks = chunk_markdown(markdown, "mat_test", "tester")
        paths = [chunk.heading_path for chunk in chunks]
        self.assertIn(["Chapter", "Section A", "Topic A1"], paths)
        self.assertIn(["Chapter", "Section A", "Topic A2"], paths)
        self.assertIn(["Chapter", "Section B", "Topic B1"], paths)

    def test_chunker_preserves_parent_body_when_using_finer_headings(self) -> None:
        long_body = "正文" * 1500
        markdown = (
            "## Chapter\n\n"
            "### Group\n\n"
            "#### Topic Without Child\n\n"
            "orphan parent body must stay searchable\n\n"
            "#### Topic With Child\n\n"
            "##### Detail\n\n"
            f"{long_body}\n"
        )
        chunks = chunk_markdown(markdown, "mat_test", "tester")
        texts = "\n".join(chunk.text for chunk in chunks)
        paths = [chunk.heading_path for chunk in chunks]
        self.assertIn("orphan parent body must stay searchable", texts)
        self.assertIn(["Chapter", "Group", "Topic Without Child"], paths)
        self.assertIn(["Chapter", "Group", "Topic With Child", "Detail"], paths)

    def test_asset_metrics_resolves_images_from_parsed_content_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            material_dir = Path(temp_dir)
            image_path = material_dir / "assets" / "images" / "img_001.png"
            image_path.parent.mkdir(parents=True)
            image_path.write_bytes(b"fake")
            report = build_quality_report(
                "![img](../assets/images/img_001.png)",
                material_dir=material_dir,
                chunks=[
                    Chunk(
                        chunk_id="c1",
                        material_id="m1",
                        user_id="tester",
                        chunk_index=0,
                        text="image",
                        heading_path=["root"],
                        token_count=1,
                    )
                ],
            )
            self.assertEqual(report.metrics["assets"]["missing_image_count"], 0)
            self.assertNotIn("missing_image_refs", report.warnings)

    def test_ingestion_uses_layout_sidecar_tables(self) -> None:
        from materials.service import MaterialIngestionService
        from materials.storage import MaterialStorage

        raw_html = (
            "<table><tr><td>Name</td><td>Value</td></tr>"
            "<tr><td>Rolle theorem</td><td>Understand</td></tr></table>"
        )
        layout = {
            "pdf_info": [
                {
                    "preproc_blocks": [
                        {
                            "type": "table",
                            "bbox": [1, 2, 3, 4],
                            "blocks": [{"lines": [{"spans": [{"type": "table", "html": raw_html}]}]}],
                        }
                    ]
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir) / "mineru"
            source_dir.mkdir()
            source_file = source_dir / "full.md"
            source_file.write_text("## Chapter\n\n" + raw_html + "\n\n### Section\n\nbody", encoding="utf-8")
            (source_dir / "layout.json").write_text(json.dumps(layout), encoding="utf-8")

            storage = MaterialStorage(base_dir=Path(temp_dir) / "materials")
            result = MaterialIngestionService(storage=storage).ingest_file(
                source_file,
                user_id="tester",
                subject="math",
                material_type="note",
                use_llm_cleanup=False,
            )
            self.assertEqual(result.parse_status.value, "ready")
            material_dir = storage.material_dir("tester", result.material_id)
            content = (material_dir / "parsed" / "content.md").read_text(encoding="utf-8")
            probe = json.loads((material_dir / "parsed" / "format_probe.json").read_text(encoding="utf-8"))
            chunks = [
                json.loads(line)
                for line in (material_dir / "chunks" / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertNotIn("<table", content)
            self.assertIn("<!-- table: table_001", content)
            self.assertTrue((material_dir / "parsed" / "tables" / "table_001.json").exists())
            self.assertEqual(probe["layout_summary"]["block_counts"]["table"], 1)
            self.assertTrue(any(chunk.get("metadata", {}).get("source_type") == "table" for chunk in chunks))
            pipeline_log = material_dir / "parsed" / "pipeline_events.jsonl"
            self.assertTrue(pipeline_log.exists())
            events = [
                json.loads(line)
                for line in pipeline_log.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(any(event.get("stage") == "parse" for event in events))
            self.assertTrue(any(event.get("stage") == "raw_markdown_cleaning" for event in events))
            self.assertTrue(any(event.get("stage") == "quality_report" for event in events))

    def test_strategy_validation_diagnostics_include_schema_error_details(self) -> None:
        bad = valid_strategy()
        bad["unexpected_field"] = {"not": "allowed"}
        diagnostics: dict[str, object] = {}
        _, warnings, used_fallback = validate_cleaning_strategy(
            bad,
            fallback_source="qwen",
            diagnostics=diagnostics,
        )
        self.assertTrue(used_fallback)
        self.assertIn("strategy_schema_validation_failed", warnings)
        self.assertEqual(diagnostics["result"], "schema_validation_failed")
        errors = diagnostics["schema_errors"]
        self.assertTrue(any("unexpected_field" in error["loc"] for error in errors))

    def test_heading_family_allows_qwen_reserved_local_label_anchors(self) -> None:
        payload = family_strategy(
            {
                "id": "answer",
                "kind": "item",
                "anchors": ["答案"],
                "anchor_position": "line_start",
                "ordinal_styles": [],
                "ordinal_required": False,
                "units": [],
                "separators": ["", " ", "：", ":"],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["答案：ABD"],
            }
        )
        _, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertNotIn("strategy_schema_validation_failed", warnings)

    def test_strategy_validator_repairs_qwen_outline_family_shapes(self) -> None:
        payload = family_strategy(
            {
                "id": "chinese_outline_major",
                "kind": "major_section",
                "anchors": ["一、", "二、", "三、"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 2,
                "examples": ["一、函数"],
            },
            {
                "id": "arabic_outline_deep",
                "kind": "item",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": [],
                "title_required": True,
                "parent_hints": ["chinese_outline_major"],
                "min_repeats": 2,
                "examples": ["1. 函数定义"],
            },
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback)
        self.assertEqual(strategy.heading_families[0].kind, "major_section")
        self.assertEqual(strategy.heading_families[0].anchors, [])
        self.assertEqual(strategy.heading_families[1].kind, "item")
        self.assertIn("strategy_family_outline_anchors_normalized", warnings)
        self.assertNotIn("strategy_family_kind_normalized_to_outline", warnings)

    def test_strategy_validator_repairs_alpha_outline_family(self) -> None:
        payload = family_strategy(
            {
                "id": "section_alpha",
                "kind": "major_section",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": [],
                "ordinal_required": True,
                "units": [],
                "separators": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb"],
            },
            {
                "id": "knowledge_group",
                "kind": "block",
                "anchors": ["\u77e5\u8bc6\u7ec4"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": ["section_alpha"],
                "min_repeats": 1,
                "examples": ["\u77e5\u8bc6\u7ec41\u6570\u5217\u7684\u5b9a\u4e49\u53ca\u8868\u793a\u6cd5"],
            },
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(strategy.heading_families[0].ordinal_styles, ["alpha"])
        self.assertIn("strategy_family_alpha_outline_repaired", warnings)

        result = clean_with_strategy(
            "A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb\n"
            "\u77e5\u8bc6\u7ec41\u6570\u5217\u7684\u5b9a\u4e49\u53ca\u8868\u793a\u6cd5\n"
            "\u6b63\u6587\n"
            "B\u91cd\u70b9\u7591\u96be\u4e13\u9879\u7a81\u7834\n"
            "\u77e5\u8bc6\u7ec42\u7b49\u5dee\u6570\u5217\n"
            "\u6b63\u6587\n",
            strategy,
        )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb", lines)
        self.assertIn("### \u77e5\u8bc6\u7ec41\u6570\u5217\u7684\u5b9a\u4e49\u53ca\u8868\u793a\u6cd5", lines)
        self.assertIn("## B\u91cd\u70b9\u7591\u96be\u4e13\u9879\u7a81\u7834", lines)
        self.assertIn("### \u77e5\u8bc6\u7ec42\u7b49\u5dee\u6570\u5217", lines)

    def test_alpha_family_does_not_promote_math_variable_statement(self) -> None:
        payload = family_strategy(
            {
                "id": "section_alpha",
                "kind": "major_section",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["alpha"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 2,
                "examples": ["A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb", "B\u91cd\u70b9\u7591\u96be\u4e13\u9879\u7a81\u7834"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb\n"
                "\u6b63\u6587\n"
                "B\u91cd\u70b9\u7591\u96be\u4e13\u9879\u7a81\u7834\n"
                "\u6b63\u6587\n"
                "## A\u4e3a\u9510\u89d2\n"
                "\u8868\u683c\u5185\u5bb9\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## A\u57fa\u7840\u77e5\u8bc6\u5b8c\u5168\u89e3\u8bfb", lines)
        self.assertIn("## B\u91cd\u70b9\u7591\u96be\u4e13\u9879\u7a81\u7834", lines)
        self.assertIn("A\u4e3a\u9510\u89d2", lines)
        self.assertFalse(any(line.startswith("#") and "A\u4e3a\u9510\u89d2" in line for line in lines))

    def test_strategy_validator_drops_bad_family_but_keeps_valid_family(self) -> None:
        payload = family_strategy(
            {
                "id": "bad_empty",
                "kind": "block",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": [],
                "ordinal_required": False,
                "units": [],
                "separators": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": [],
            },
            {
                "id": "knowledge_group",
                "kind": "block",
                "anchors": ["\u77e5\u8bc6\u7ec4"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": ["bad_empty"],
                "min_repeats": 1,
                "examples": ["\u77e5\u8bc6\u7ec41\u6570\u5217\u7684\u5b9a\u4e49"],
            },
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual([family.id for family in strategy.heading_families], ["knowledge_group"])
        self.assertEqual(strategy.heading_families[0].parent_hints, [])
        self.assertIn("strategy_family_without_matcher_dropped", warnings)
        self.assertIn("strategy_family_parent_hints_repaired", warnings)

    def test_strategy_validator_drops_invalid_family_fields_but_keeps_valid_family(self) -> None:
        payload = family_strategy(
            {
                "id": "bad_style",
                "kind": "block",
                "anchors": ["bad"],
                "anchor_position": "line_start",
                "ordinal_styles": ["letter"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["bad1 title"],
            },
            {
                "id": "knowledge_group",
                "kind": "block",
                "anchors": ["\u77e5\u8bc6\u7ec4"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": ["bad_style"],
                "min_repeats": 1,
                "examples": ["\u77e5\u8bc6\u7ec41\u6570\u5217\u7684\u5b9a\u4e49"],
            },
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual([family.id for family in strategy.heading_families], ["knowledge_group"])
        self.assertEqual(strategy.heading_families[0].parent_hints, [])
        self.assertIn("strategy_family_invalid_dropped", warnings)
        self.assertIn("strategy_family_parent_hints_repaired", warnings)

    def test_strategy_validator_repairs_qwen_anchor_unit_overlap(self) -> None:
        payload = family_strategy(
            {
                "id": "problem_type",
                "kind": "block",
                "anchors": ["题型"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": ["型"],
                "separators": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["# 题型二 函数性态"],
            }
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(strategy.heading_families[0].units, [])
        self.assertEqual(strategy.heading_families[0].examples, ["题型二 函数性态"])
        self.assertIn("strategy_family_anchor_unit_overlap_repaired", warnings)
        self.assertIn("strategy_family_examples_heading_markers_stripped", warnings)

        result = clean_with_strategy(
            "题型二 函数性态\n正文\n题型三 求极限\n正文\n",
            strategy,
        )
        self.assertRegex(result.cleaned_markdown, r"(?m)^#{2,6} 题型二 函数性态$")
        self.assertRegex(result.cleaned_markdown, r"(?m)^#{2,6} 题型三 求极限$")

    def test_strategy_validator_drops_malformed_qwen_family_key(self) -> None:
        payload = family_strategy(
            {
                "id": "chinese_outline_major",
                "kind": "major_section",
                "anchors": ["一、", "二、"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": [],
                "separators [],": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 2,
                "examples": ["一、函数", "二、极限"],
            }
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(strategy.heading_families[0].anchors, [])
        self.assertIn("strategy_family_malformed_key_repaired", warnings)

    def test_strategy_validator_repairs_qwen_chapter_anchor_shape(self) -> None:
        payload = family_strategy(
            {
                "id": "chapter_unit",
                "kind": "strong_boundary",
                "anchors": ["第章", "第节"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": ["章", "节"],
                "separators": [],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["# 第一章 函数", "# 第一节 基本概念"],
            }
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(strategy.heading_families[0].anchors, ["第"])
        self.assertEqual(strategy.heading_families[0].examples, ["第一章 函数", "第一节 基本概念"])
        self.assertIn("strategy_family_chapter_anchor_repaired", warnings)

        result = clean_with_strategy(
            "第一章 函数\n正文\n第一节 基本概念\n正文\n",
            strategy,
        )
        self.assertIn("## 第一章 函数", result.cleaned_markdown)
        self.assertIn("### 第一节 基本概念", result.cleaned_markdown)

    def test_heading_family_whitelist_demotes_unlisted_existing_headings(self) -> None:
        payload = family_strategy(
            {
                "id": "strong_boundary",
                "kind": "strong_boundary",
                "anchors": ["第"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic", "chinese"],
                "ordinal_required": True,
                "units": ["篇", "章", "节"],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["第4篇 平面向量及其应用"],
            },
            {
                "id": "major",
                "kind": "major_section",
                "anchors": ["核心题型题组例解"],
                "anchor_position": "line_start",
                "ordinal_styles": [],
                "ordinal_required": False,
                "units": [],
                "separators": ["", " "],
                "title_required": False,
                "parent_hints": ["strong_boundary"],
                "min_repeats": 1,
                "examples": ["C核心题型题组例解"],
            },
            {
                "id": "question_group",
                "kind": "block",
                "anchors": ["题组"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic", "chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " ", "、", "：", ":"],
                "title_required": True,
                "parent_hints": ["major"],
                "min_repeats": 1,
                "examples": ["题组1平面向量基本概念"],
            },
            {
                "id": "example",
                "kind": "item",
                "anchors": ["典型"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic", "circled"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " ", "、", "：", ":"],
                "title_required": True,
                "parent_hints": ["question_group"],
                "min_repeats": 1,
                "examples": ["典型2用有向线段表示向量"],
            },
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "## 第4篇 平面向量及其应用\n"
                "## C核心题型题组例解\n"
                "## 题组1平面向量基本概念\n"
                "## 典型2用有向线段表示向量\n"
                "## 【答案】ABD\n"
                "正文\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 第4篇 平面向量及其应用", lines)
        self.assertIn("### C核心题型题组例解", lines)
        self.assertIn("#### 题组1平面向量基本概念", lines)
        self.assertIn("##### 典型2用有向线段表示向量", lines)
        self.assertIn("**答案：** ABD", lines)
        self.assertNotIn("## 【答案】ABD", lines)
        self.assertEqual(result.parse_report["stats"]["active_heading_families"], 4)
        self.assertIn("example", result.parse_report["rule_execution"]["active_family_ids"])

    def test_heading_family_mode_does_not_promote_compact_chinese_sentence_fragments(self) -> None:
        payload = family_strategy(
            {
                "id": "chapter_unit",
                "kind": "strong_boundary",
                "anchors": ["第"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese", "arabic"],
                "ordinal_required": True,
                "units": ["章"],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["第四章 常微分方程"],
            },
            {
                "id": "chinese_outline",
                "kind": "major_section",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": ["、"],
                "title_required": True,
                "parent_hints": ["chapter_unit"],
                "min_repeats": 2,
                "examples": ["一、考试内容要点精讲", "二、常微分方程的应用"],
            },
            {
                "id": "paren_chinese_section",
                "kind": "block",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["paren_chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": ["chinese_outline"],
                "min_repeats": 1,
                "examples": ["（四）高阶线性微分方程"],
            },
            {
                "id": "arabic_item",
                "kind": "item",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": [".", "．", "、", " "],
                "title_required": True,
                "parent_hints": ["paren_chinese_section"],
                "min_repeats": 2,
                "examples": ["3.常系数非齐次线性微分方程", "4. 欧拉方程"],
            },
        )
        payload["relation_hints"] = [
            _relation_hint("chapter_unit", "chinese_outline"),
            _relation_hint("chinese_outline", "paren_chinese_section"),
            _relation_hint("paren_chinese_section", "arabic_item"),
        ]
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "第四章 常微分方程\n"
                "一、考试内容要点精讲\n"
                "（四）高阶线性微分方程\n"
                "1.一阶微分方程\n"
                "正文\n"
                "2.可降阶微分方程\n"
                "正文\n"
                "3.常系数非齐次线性微分方程\n"
                "二阶常系数线性非齐次微分方程的一般形式为\n"
                "正文\n"
                "4. 欧拉方程(仅数学一要求)\n"
                "正文\n"
                "(五）差分方程(仅数学三要求)\n"
                "两端再对x求导得\n"
                "正文\n"
                "二、常微分方程的应用\n"
                "正文\n",
                use_llm_profile=True,
            )

        lines = result.cleaned_markdown.splitlines()
        self.assertIn("二阶常系数线性非齐次微分方程的一般形式为", lines)
        self.assertIn("两端再对x求导得", lines)
        self.assertFalse(any(line.startswith("#") and "二阶常系数线性非齐次微分方程" in line for line in lines))
        self.assertFalse(any(line.startswith("#") and "两端再对x求导得" in line for line in lines))
        self.assertIn("##### 3.常系数非齐次线性微分方程", lines)
        self.assertIn("##### 4. 欧拉方程(仅数学一要求)", lines)

    def test_heading_family_mode_demotes_unlisted_markdown_short_titles(self) -> None:
        payload = family_strategy(
            {
                "id": "example",
                "kind": "item",
                "anchors": ["典型"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " ", "：", ":"],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["典型1例题"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "## 第1章 函数\n"
                "## 常用的方法有三种\n"
                "## 图4-1-1\n"
                "## 典型1例题\n"
                "正文\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 第1章 函数", lines)
        self.assertIn("常用的方法有三种", lines)
        self.assertIn("图4-1-1", lines)
        self.assertTrue(any(line.endswith("典型1例题") and line.startswith("#") for line in lines))
        self.assertNotIn("## 常用的方法有三种", lines)
        self.assertNotIn("## 图4-1-1", lines)

    def test_circled_outline_requires_sequence_and_skips_count_badges(self) -> None:
        payload = family_strategy(
            {
                "id": "circled_outline",
                "kind": "outline",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["circled"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " ", "、", "：", ":"],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 2,
                "examples": ["①平移变换", "②伸缩变换", "③对称变换"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "①平移变换\n"
                "正文\n"
                "②伸缩变换\n"
                "正文\n"
                "③对称变换\n"
                "正文\n"
                "③个易错点\n"
                "⑥个高考考点\n"
                "⑤个思想方法\n"
                "⑤特殊情况\n"
                "正文\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertTrue(any(line.endswith("①平移变换") and line.startswith("#") for line in lines))
        self.assertTrue(any(line.endswith("②伸缩变换") and line.startswith("#") for line in lines))
        self.assertTrue(any(line.endswith("③对称变换") and line.startswith("#") for line in lines))
        self.assertIn("③个易错点", lines)
        self.assertIn("⑥个高考考点", lines)
        self.assertIn("⑤个思想方法", lines)
        self.assertIn("⑤特殊情况", lines)
        self.assertFalse(any(line.startswith("#") and "③个易错点" in line for line in lines))
        self.assertFalse(any(line.startswith("#") and "⑥个高考考点" in line for line in lines))
        self.assertFalse(any(line.startswith("#") and "⑤个思想方法" in line for line in lines))
        self.assertFalse(any(line.startswith("#") and "⑤特殊情况" in line for line in lines))
        self.assertEqual(
            result.parse_report["rule_execution"]["outline_sequence_allowed_counts"]["circled_outline"],
            3,
        )

    def test_heading_trailing_metadata_is_preserved_in_title(self) -> None:
        payload = family_strategy(
            {
                "id": "chapter_unit",
                "kind": "strong_boundary",
                "anchors": ["第"],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic", "chinese"],
                "ordinal_required": True,
                "units": ["章"],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["第4章 随机变量及其分布"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "## 第4章 随机变量及其分布 难度：易、中\n正文\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 第4章 随机变量及其分布 难度：易、中", lines)
        self.assertNotIn("## 第4章 随机变量及其分布", lines)
        self.assertNotIn("**难度：** 易、中", lines)
        self.assertNotIn("heading_trailing_metadata_demoted_to_label", result.warnings)

    def test_exam_section_existing_heading_can_be_long_when_qwen_declares_family(self) -> None:
        payload = family_strategy(
            {
                "id": "exam_section_chinese",
                "kind": "major_section",
                "anchors": ["一、", "二、", "三、"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": ["、"],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 2,
                "examples": ["一、单项选择题", "二、多项选择题"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "# 2025年全国硕士研究生招生考试思想政治理论试题\n"
                "## 一、单项选择题：第1~16小题，每小题1分，共16分。下列每题给出的四个选项中，只有一个选项是最符合题目要求的。\n"
                "1.题干很长很长，包含句号。A.选项\n"
                "## 二、多项选择题：第17~33小题，每小题2分，共34分。多选、少选或错选均不得分。\n"
                "17.题干很长很长，包含句号。A.选项\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("# 2025年全国硕士研究生招生考试思想政治理论试题", lines)
        self.assertIn(
            "## 一、单项选择题：第1~16小题，每小题1分，共16分。下列每题给出的四个选项中，只有一个选项是最符合题目要求的。",
            lines,
        )
        self.assertIn(
            "## 二、多项选择题：第17~33小题，每小题2分，共34分。多选、少选或错选均不得分。",
            lines,
        )
        self.assertEqual(result.strategy["strategy_source"], "qwen")
        self.assertIn("exam_section_chinese", result.parse_report["rule_execution"]["active_family_ids"])

    def test_exam_question_items_can_use_long_question_text_as_heading(self) -> None:
        payload = family_strategy(
            {
                "id": "exam_section_chinese",
                "kind": "major_section",
                "anchors": ["一、"],
                "anchor_position": "line_start",
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "units": [],
                "separators": ["、"],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["一、单项选择题"],
            },
            {
                "id": "question_item_arabic",
                "kind": "item",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["."],
                "title_required": True,
                "parent_hints": ["exam_section_chinese"],
                "min_repeats": 2,
                "examples": ["1.题干很长很长", "2.题干也很长"],
            },
        )
        payload["document_profile"]["document_type"] = "exercise_notes"
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "# 政治真题\n"
                "## 一、单项选择题：第1~16小题，每小题1分。\n"
                "1.题干很长很长，包含句号。A.选项 B.选项 C.选项 D.选项\n"
                "2.题干也很长很长，包含句号。A.选项 B.选项 C.选项 D.选项\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertIn("## 一、单项选择题：第1~16小题，每小题1分。", lines)
        self.assertIn("### 1.题干很长很长，包含句号。A.选项 B.选项 C.选项 D.选项", lines)
        self.assertIn("### 2.题干也很长很长，包含句号。A.选项 B.选项 C.选项 D.选项", lines)
        self.assertIn("question_item_arabic", result.parse_report["rule_execution"]["active_family_ids"])

    def test_paren_arabic_outline_demotes_long_body_sentence(self) -> None:
        payload = family_strategy(
            {
                "id": "paren_arabic_outline",
                "kind": "outline",
                "anchors": [],
                "anchor_position": "line_start",
                "ordinal_styles": ["paren_arabic"],
                "ordinal_required": True,
                "units": [],
                "separators": ["", " "],
                "title_required": True,
                "parent_hints": [],
                "min_repeats": 1,
                "examples": ["(1)阶乘的定义", "(2)排列数公式"],
            }
        )
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ):
            result = clean_raw_markdown(
                "(1)阶乘的定义\n"
                "正文\n"
                "(2)排列数公式\n"
                "正文\n"
                "(3)判断一个具体问题是否为排列问题应着重判断取出的元素对顺序有没有要求\n"
                "正文\n"
                "(4)按一定规则估计经验回归方\n"
                "程中的参数。\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertTrue(any(line.startswith("#") and line.endswith("(1)阶乘的定义") for line in lines))
        self.assertTrue(any(line.startswith("#") and line.endswith("(2)排列数公式") for line in lines))
        self.assertIn("(3)判断一个具体问题是否为排列问题应着重判断取出的元素对顺序有没有要求", lines)
        self.assertFalse(
            any(
                line.startswith("#")
                and "判断一个具体问题是否为排列问题应着重判断取出的元素对顺序有没有要求" in line
                for line in lines
            )
        )
        self.assertIn("(4)按一定规则估计经验回归方", lines)
        self.assertFalse(any(line.startswith("#") and "按一定规则估计经验回归方" in line for line in lines))


    def test_front_matter_zone_schema_validates(self) -> None:
        document_zones = {
            "front_matter_zones": [
                {
                    "type": "catalog_or_navigation",
                    "start_line": 2,
                    "end_line": 6,
                    "title": "目录与章节概览",
                    "action": "preserve_unprocessed",
                    "chunk_policy": "single_catalog_chunk",
                    "confidence": 0.86,
                    "signals": ["dense_chapter_headings"],
                }
            ],
            "body_start_line": 7,
            "confidence": 0.86,
        }
        parsed, warnings, used_fallback = validate_document_zones_payload(document_zones)
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(parsed.body_start_line, 7)
        self.assertEqual(parsed.front_matter_zones[0].chunk_policy, "single_catalog_chunk")

    def test_catalog_zone_requires_navigation_signal(self) -> None:
        document_zones = {
            "front_matter_zones": [
                {
                    "type": "catalog_or_navigation",
                    "start_line": 3,
                    "end_line": 5,
                    "title": "考试内容表",
                    "action": "preserve_unprocessed",
                    "chunk_policy": "single_catalog_chunk",
                    "confidence": 0.9,
                    "signals": ["html_table_block", "front_block_index"],
                }
            ],
            "body_start_line": 7,
            "confidence": 0.9,
        }
        parsed, warnings, used_fallback = validate_document_zones_payload(document_zones)
        self.assertFalse(used_fallback, warnings)
        self.assertEqual(parsed.front_matter_zones, [])
        self.assertIn("document_zones_catalog_without_navigation_signal_dropped", warnings)

    def test_front_matter_zone_preserves_catalog_without_cleaning_body(self) -> None:
        strategy = valid_strategy()
        document_zones = {
            "front_matter_zones": [
                {
                    "type": "catalog_or_navigation",
                    "start_line": 1,
                    "end_line": 6,
                    "title": "目录与章节概览",
                    "action": "preserve_unprocessed",
                    "chunk_policy": "single_catalog_chunk",
                    "confidence": 0.9,
                    "signals": ["chapter_heading_reappears_later"],
                }
            ],
            "body_start_line": 7,
            "confidence": 0.9,
        }
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=strategy,
        ), patch(
            "materials.postprocess.raw_markdown_cleaner.generate_document_zones_with_qwen",
            return_value=document_zones,
        ):
            result = clean_raw_markdown(
                "## 第1章 函数的概念与性质\n"
                "![](images/chapter1.png)\n"
                "4个知识点\n"
                "## 第2章 指数函数与对数函数\n"
                "难度：中\n"
                "18个必会题型\n"
                "# 第1章 函数的概念与性质\n"
                "## 知识组1 函数的概念\n"
                "正文\n",
                use_llm_profile=True,
            )
        lines = result.cleaned_markdown.splitlines()
        self.assertEqual(lines[0], "## 第1章 函数的概念与性质")
        self.assertEqual(lines[3], "## 第2章 指数函数与对数函数")
        self.assertIn("难度：中", lines)
        self.assertTrue(any(line.startswith("#") and "第1章 函数的概念与性质" in line for line in lines[6:]))
        self.assertNotIn("document_zones", result.strategy)
        self.assertEqual(result.document_zones["body_start_line"], 7)
        zones = result.parse_report["document_zones"]["front_matter_zones_applied"]
        self.assertEqual(zones[0]["start_line"], 1)
        self.assertEqual(zones[0]["end_line"], 6)
        self.assertEqual(zones[0]["chunk_policy"], "single_catalog_chunk")
        self.assertFalse(any(match["line_no"] <= 6 for match in result.parse_report["main_section_matches"]))

    def test_low_confidence_front_matter_zone_is_not_applied(self) -> None:
        strategy = valid_strategy()
        document_zones = {
            "front_matter_zones": [
                {
                    "type": "catalog_or_navigation",
                    "start_line": 1,
                    "end_line": 2,
                    "action": "preserve_unprocessed",
                    "chunk_policy": "single_catalog_chunk",
                    "confidence": 0.2,
                }
            ],
            "body_start_line": 3,
            "confidence": 0.2,
        }
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=strategy,
        ), patch(
            "materials.postprocess.raw_markdown_cleaner.generate_document_zones_with_qwen",
            return_value=document_zones,
        ):
            result = clean_raw_markdown(
                "## 第1章 函数\n"
                "目录说明\n"
                "# 第1章 函数\n"
                "正文\n",
                use_llm_profile=True,
            )
        self.assertEqual(result.parse_report["document_zones"]["front_matter_zones_applied"], [])
        self.assertIn("front_matter_zone_skipped_low_confidence", result.warnings)

    def test_qwen_heading_family_anchor_takes_priority_over_reserved_label(self) -> None:
        payload = family_strategy(
            {
                "id": "method_block",
                "kind": "block",
                "anchors": ["方法"],
                "ordinal_styles": ["arabic"],
                "ordinal_required": True,
                "min_repeats": 2,
                "examples": ["方法1 利用有理运算法则求极限", "方法2 利用基本极限求极限"],
            }
        )
        strategy, warnings, used_fallback = validate_cleaning_strategy(payload, fallback_source="qwen")
        self.assertFalse(used_fallback, warnings)
        with patch(
            "materials.postprocess.raw_markdown_cleaner.generate_strategy_with_qwen",
            return_value=payload,
        ), patch(
            "materials.postprocess.raw_markdown_cleaner.generate_document_zones_with_qwen",
            return_value={"front_matter_zones": [], "body_start_line": 1, "confidence": 0.8},
        ):
            result = clean_raw_markdown(
                "方法1 利用有理运算法则求极限\n正文\n方法2 利用基本极限求极限\n正文\n",
                use_llm_profile=True,
            )
        self.assertIn("## 方法1 利用有理运算法则求极限", result.cleaned_markdown)
        self.assertIn("## 方法2 利用基本极限求极限", result.cleaned_markdown)


if __name__ == "__main__":
    unittest.main()
