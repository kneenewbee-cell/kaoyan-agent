"""受控的 Markdown 结构策略。

策略只描述允许的结构原语；它不是可执行规则，也不接受任意正则或路径。
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

ALLOWED_FAMILIES = {
    "markdown_heading",
    "setext_heading",
    "label_ordinal_marker",
    "chinese_outline_marker",
    "arabic_outline_marker",
    "decimal_outline_marker",
    "chapter_marker",
    "letter_marker",
}

ALLOWED_SHORT_LINE_POLICIES = {
    "attach_to_current_section",
    "promote_to_subheading",
    "ignore",
}


def get_default_structure_strategy() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "strategy_name": "generic_outline_strategy",
        "confidence": 0.9,
        "document_title_rule": {
            "use_setext_heading_as_h1": True,
            "remove_duplicate_filename_title": True,
        },
        "main_section_rule": {
            "family": "label_ordinal_marker",
            "target_level": 2,
            "aliases": ["知识点", "要点", "考点", "专题", "知识", "模块"],
            "number_styles": ["chinese", "arabic"],
            "require_line_start": True,
            "min_repeats": 2,
            "examples": [],
        },
        "secondary_section_rules": [],
        "plain_short_line_policy": {"mode": "attach_to_current_section"},
        "metadata_rule": {
            "enabled": True,
            "patterns": ["【考频】", "【考查频率】", "【难度】", "【核心难点】"],
            "attach_to_current_section": True,
        },
        "inline_number_policy": {
            "paren_arabic_as_body": True,
            "right_paren_arabic_as_body": True,
            "letter_marker_as_body_unless_configured": True,
        },
        "ignore_line_patterns": ["--- 全文结束 ---"],
        "chunk_rule": {
            "split_by": "main_section",
            "max_chars": 1800,
            "overlap_chars": 150,
            "keep_heading_path": True,
            "if_section_too_long": "split_by_length_keep_heading_path",
        },
        "fallback_rule": {
            "on_invalid_strategy": "use_default_local_strategy",
            "on_uncertain_structure": "preserve_original",
            "write_warning": True,
        },
    }


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def validate_structure_strategy(strategy: dict | None) -> dict[str, Any]:
    """校验并返回可安全使用的策略。

    非法输入整体回退到默认策略，并通过 ``_validation_warnings`` 暴露原因，
    从而不让一次外部策略错误中断入库。
    """
    default = get_default_structure_strategy()
    if strategy is None:
        return default

    errors: list[str] = []
    if not isinstance(strategy, dict):
        errors.append("strategy_not_object")
    else:
        merged = deepcopy(default)
        for key, value in strategy.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key].update(deepcopy(value))
            else:
                merged[key] = deepcopy(value)

        main_rule = merged.get("main_section_rule")
        if not isinstance(main_rule, dict):
            errors.append("missing_main_section_rule")
        else:
            if main_rule.get("family") not in ALLOWED_FAMILIES:
                errors.append("invalid_main_section_family")
            level = main_rule.get("target_level", 2)
            if not isinstance(level, int) or not 1 <= level <= 6:
                errors.append("invalid_target_level")
            if "aliases" in main_rule and not _is_string_list(main_rule["aliases"]):
                errors.append("invalid_aliases")

        secondary = merged.get("secondary_section_rules", [])
        if not isinstance(secondary, list) or any(
            not isinstance(rule, dict) or rule.get("family") not in ALLOWED_FAMILIES
            for rule in secondary
        ):
            errors.append("invalid_secondary_section_rules")

        short_policy = merged.get("plain_short_line_policy", {}).get("mode")
        if short_policy not in ALLOWED_SHORT_LINE_POLICIES:
            errors.append("invalid_plain_short_line_policy")

        chunk_rule = merged.get("chunk_rule")
        max_chars = chunk_rule.get("max_chars") if isinstance(chunk_rule, dict) else None
        if not isinstance(max_chars, int) or not 500 <= max_chars <= 5000:
            errors.append("invalid_chunk_max_chars")

        for key in ("ignore_line_patterns",):
            if key in merged and not _is_string_list(merged[key]):
                errors.append(f"invalid_{key}")

    if errors:
        default["_validation_warnings"] = [
            "invalid_structure_strategy_fallback:" + ",".join(errors)
        ]
        return default

    return merged
