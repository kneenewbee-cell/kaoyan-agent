"""由受控 strategy 驱动的 Markdown 结构规范化。"""

from __future__ import annotations

import re
from typing import Any

from .section_builder import blockize, build_sections, render_sections
from .structure_profile import build_structure_profile
from .structure_strategy import validate_structure_strategy

ATX_NO_SPACE_RE = re.compile(r"^(#{1,6})([^#\s].*)$", re.MULTILINE)


def normalize_markdown_structure(
    markdown_text: str,
    fallback_title: str | None = None,
    *,
    filename_stem: str | None = None,
    strategy: dict | None = None,
) -> tuple[str, dict[str, Any]]:
    """返回规范化 Markdown 与可写入质量报告的结构元数据。"""
    warnings: list[str] = []

    def fix_heading(match: re.Match[str]) -> str:
        warnings.append("fixed_heading_missing_space")
        return f"{match.group(1)} {match.group(2).strip()}"

    prepared = markdown_text.replace("\r\n", "\n").replace("\r", "\n")
    prepared = ATX_NO_SPACE_RE.sub(fix_heading, prepared)
    validated = validate_structure_strategy(strategy)
    warnings.extend(validated.pop("_validation_warnings", []))

    blocks = blockize(prepared)
    sections, section_warnings = build_sections(blocks, validated)
    warnings.extend(section_warnings)
    title = next((section.title for section in sections if section.level == 1), None)
    title = title or filename_stem or fallback_title or "未命名资料"
    normalized = render_sections(sections, doc_title=title)

    profile = build_structure_profile(sections, validated["main_section_rule"].get("target_level", 2))
    report: dict[str, Any] = {
        "strategy_name": validated.get("strategy_name"),
        "strategy_schema_version": validated.get("schema_version"),
        "warnings": sorted(set(warnings)),
        **profile,
    }
    return normalized, report
