from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .format_probe import (
    ARABIC_OUTLINE_RE,
    CHAPTER_RE,
    CHINESE_OUTLINE_RE,
    DECIMAL_OUTLINE_RE,
    LABEL_ORDINAL_RE,
    FormatProbe,
    build_format_probe,
)
from .qwen_strategy_client import (
    QWEN_STRATEGY_MODEL,
    generate_document_zones_with_qwen,
    generate_strategy_bundle_with_qwen,
    generate_strategy_with_qwen,
    write_qwen_strategy_log,
    write_qwen_zone_log,
)
from .strategy_cleaner import DEFAULT_SUBSECTION_ALIASES, clean_with_strategy
from .document_zones import default_document_zones, validate_document_zones_payload
from .strategy_schema import CleaningStrategy, DocumentZones
from .strategy_validator import default_conservative_strategy, validate_cleaning_strategy


@dataclass
class CleanResult:
    cleaned_markdown: str
    format_probe: dict[str, Any]
    strategy: dict[str, Any]
    document_zones: dict[str, Any]
    zone_report: dict[str, Any]
    parse_report: dict[str, Any]
    warnings: list[str]


def _legacy_qwen_functions_are_mocked() -> bool:
    return hasattr(generate_strategy_with_qwen, "mock_calls") or hasattr(generate_document_zones_with_qwen, "mock_calls")


def _base_strategy_dict(
    *,
    marker_type: str,
    source: str,
    aliases: list[str] | None = None,
    examples: list[str] | None = None,
    confidence: float = 0.8,
) -> dict[str, Any]:
    return {
        "version": "1.0",
        "document_profile": {
            "subject": "unknown",
            "document_type": "knowledge_notes",
            "language": "zh",
            "confidence": confidence,
        },
        "main_section_rule": {
            "enabled": marker_type not in {"none", "existing_markdown"},
            "target_level": 2,
            "marker_type": marker_type,
            "aliases": aliases or [],
            "number_styles": ["chinese", "arabic"],
            "requires_line_start": True,
            "requires_colon": False,
            "min_repeats": 2,
            "examples": examples or [],
        },
        "subsection_rules": [],
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
        "strategy_source": source,
    }


def _add_subsection_rules(strategy: dict[str, Any], probe: FormatProbe) -> None:
    present = [alias for alias in DEFAULT_SUBSECTION_ALIASES if alias in set(probe.short_line_candidates)]
    if not present:
        return
    strategy["subsection_rules"] = [
        {
            "enabled": True,
            "target_level": 3,
            "type": "fixed_label",
            "aliases": present,
            "requires_line_start": True,
            "min_repeats": 1,
        }
    ]


def _label_aliases(lines: list[str]) -> list[str]:
    aliases: list[str] = []
    for line in lines:
        match = LABEL_ORDINAL_RE.match(line)
        if match and match.group(1) not in aliases:
            aliases.append(match.group(1))
    return aliases


def _strip_markdown_heading_marker(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("#"):
        return stripped.lstrip("#").strip()
    return stripped


def detect_local_strategy(format_probe: dict[str, Any] | FormatProbe, user_hints: dict | None = None) -> CleaningStrategy:
    probe = format_probe if isinstance(format_probe, FormatProbe) else FormatProbe(**format_probe)
    existing_h2_count = sum(1 for heading in probe.existing_headings if heading.lstrip().startswith("## "))
    existing_heading_titles = [_strip_markdown_heading_marker(heading) for heading in probe.existing_headings]
    existing_structural_count = sum(
        1
        for title in existing_heading_titles
        if CHAPTER_RE.match(title) or CHINESE_OUTLINE_RE.match(title) or ARABIC_OUTLINE_RE.match(title)
    )
    if existing_h2_count >= 2 or (len(existing_heading_titles) >= 5 and existing_structural_count >= 3):
        strategy = _base_strategy_dict(marker_type="existing_markdown", source="local", confidence=0.85)
        _add_subsection_rules(strategy, probe)
        validated, _, _ = validate_cleaning_strategy(strategy, fallback_source="local")
        return validated

    candidates = probe.candidate_marker_lines
    counters = {
        "label_ordinal": [line for line in candidates if LABEL_ORDINAL_RE.match(line)],
        "chinese_outline": [line for line in candidates if CHINESE_OUTLINE_RE.match(line)],
        "chapter": [line for line in candidates if CHAPTER_RE.match(line)],
        "decimal_outline": [line for line in candidates if DECIMAL_OUTLINE_RE.match(line)],
        "arabic_outline": [line for line in candidates if ARABIC_OUTLINE_RE.match(line)],
    }
    for marker_type in ("label_ordinal", "chinese_outline", "chapter", "decimal_outline", "arabic_outline"):
        matches = counters[marker_type]
        if len(matches) >= 2:
            strategy = _base_strategy_dict(
                marker_type=marker_type,
                source="local",
                aliases=_label_aliases(matches) if marker_type == "label_ordinal" else [],
                examples=matches[:5],
                confidence=0.86,
            )
            _add_subsection_rules(strategy, probe)
            if user_hints:
                subject = user_hints.get("subject")
                material_type = user_hints.get("material_type")
                if subject in {"math", "politics", "english", "cs408", "408", "unknown"}:
                    strategy["document_profile"]["subject"] = subject
                if material_type and material_type != "unknown":
                    strategy["document_profile"]["document_type"] = "mixed"
            validated, _, _ = validate_cleaning_strategy(strategy, fallback_source="local")
            return validated

    default_strategy = default_conservative_strategy(reason="本地探测未发现可信主标题结构")
    default_strategy.strategy_source = "default"
    return default_strategy


def clean_raw_markdown(
    raw_markdown: str,
    *,
    source_name: str | None = None,
    use_llm_profile: bool = False,
    user_hints: dict | None = None,
    layout_summary: dict[str, Any] | None = None,
) -> CleanResult:
    probe = build_format_probe(raw_markdown, filename=source_name, layout_summary=layout_summary)
    probe_dict = probe.to_dict()
    warnings: list[str] = []
    strategy: CleaningStrategy | None = None
    document_zones: DocumentZones = default_document_zones()
    qwen_usage: dict[str, Any] = {}
    zone_usage: dict[str, Any] = {}
    strategy_validation: dict[str, Any] = {}
    zone_validation: dict[str, Any] = {}

    if use_llm_profile:
        use_legacy_profile = _legacy_qwen_functions_are_mocked()
        if not use_legacy_profile:
            try:
                bundle_payload = generate_strategy_bundle_with_qwen(
                    probe_dict,
                    model=QWEN_STRATEGY_MODEL,
                    usage_metrics=qwen_usage,
                )
                qwen_payload = bundle_payload.get("cleaning_strategy")
                zone_payload = bundle_payload.get("document_zones")
                strategy, validation_warnings, used_fallback = validate_cleaning_strategy(
                    qwen_payload,
                    fallback_source="qwen",
                    diagnostics=strategy_validation,
                )
                warnings.extend(validation_warnings)
                document_zones, zone_warnings, zone_used_fallback = validate_document_zones_payload(
                    zone_payload,
                    diagnostics=zone_validation,
                )
                warnings.extend(zone_warnings)
                qwen_usage["schema_valid"] = not used_fallback
                qwen_usage["strategy_schema_valid"] = not used_fallback
                qwen_usage["zone_schema_valid"] = not zone_used_fallback
                if strategy_validation:
                    qwen_usage["strategy_validation"] = strategy_validation
                if zone_validation:
                    qwen_usage["zone_validation"] = zone_validation
                if used_fallback:
                    warnings.append("qwen_strategy_invalid_fallback_to_local")
                    strategy = None
                if zone_used_fallback:
                    warnings.append("qwen_document_zones_invalid_fallback_to_empty")
            except Exception as exc:
                warnings.append("qwen_strategy_bundle_unavailable_fallback_to_legacy")
                warnings.append(f"qwen_strategy_bundle_error:{exc.__class__.__name__}")
                qwen_usage.setdefault("schema_valid", False)
                use_legacy_profile = True

        if use_legacy_profile:
            try:
                qwen_payload = generate_strategy_with_qwen(
                    probe_dict,
                    model=QWEN_STRATEGY_MODEL,
                    usage_metrics=qwen_usage,
                )
                strategy, validation_warnings, used_fallback = validate_cleaning_strategy(
                    qwen_payload,
                    fallback_source="qwen",
                    diagnostics=strategy_validation,
                )
                warnings.extend(validation_warnings)
                qwen_usage["schema_valid"] = not used_fallback
                if strategy_validation:
                    qwen_usage["strategy_validation"] = strategy_validation
                if used_fallback:
                    warnings.append("qwen_strategy_invalid_fallback_to_local")
                    strategy = None
            except Exception as legacy_exc:
                warnings.append("qwen_strategy_unavailable_fallback_to_local")
                warnings.append(f"qwen_strategy_error:{legacy_exc.__class__.__name__}")

            try:
                zone_payload = generate_document_zones_with_qwen(
                    probe_dict,
                    model=QWEN_STRATEGY_MODEL,
                    usage_metrics=zone_usage,
                )
                document_zones, zone_warnings, zone_used_fallback = validate_document_zones_payload(
                    zone_payload,
                    diagnostics=zone_validation,
                )
                warnings.extend(zone_warnings)
                zone_usage["schema_valid"] = not zone_used_fallback
                if zone_validation:
                    zone_usage["zone_validation"] = zone_validation
                if zone_used_fallback:
                    warnings.append("qwen_document_zones_invalid_fallback_to_empty")
            except Exception as legacy_exc:
                warnings.append("qwen_document_zones_unavailable_fallback_to_empty")
                warnings.append(f"qwen_document_zones_error:{legacy_exc.__class__.__name__}")
                zone_usage.setdefault("schema_valid", False)

    if strategy is None:
        strategy = detect_local_strategy(probe, user_hints=user_hints)
        if strategy.strategy_source == "default":
            warnings.append("local_strategy_fallback_to_default")

    clean_result = clean_with_strategy(
        raw_markdown,
        strategy,
        source_name=source_name,
        document_zones=document_zones,
    )
    if strategy.strategy_source == "qwen" and clean_result.parse_report.get("fallback_used"):
        warnings.append("qwen_strategy_not_supported_by_probe_fallback_to_local")
        qwen_usage["strategy_matches_document"] = False
        strategy = detect_local_strategy(probe, user_hints=user_hints)
        clean_result = clean_with_strategy(
            raw_markdown,
            strategy,
            source_name=source_name,
            document_zones=document_zones,
        )
        if strategy.strategy_source == "default":
            warnings.append("local_strategy_fallback_to_default")
    elif qwen_usage:
        qwen_usage["strategy_matches_document"] = strategy.strategy_source == "qwen"

    all_warnings = sorted(set(warnings + clean_result.warnings))
    parse_report = dict(clean_result.parse_report)
    parse_report["warnings"] = list(parse_report.get("warnings", [])) + [{"message": warning} for warning in warnings]
    parse_report["stats"]["warnings_count"] = len(parse_report["warnings"])
    parse_report["strategy_source"] = strategy.strategy_source
    if strategy_validation:
        parse_report["strategy_validation"] = strategy_validation
    if qwen_usage:
        qwen_usage["final_strategy_source"] = strategy.strategy_source
        qwen_usage["fallback_used"] = strategy.strategy_source != "qwen"
        parse_report["qwen_usage"] = dict(qwen_usage)
        if "api_success" in qwen_usage or "error_type" in qwen_usage:
            try:
                write_qwen_strategy_log(qwen_usage)
            except OSError:
                all_warnings.append("qwen_usage_log_write_failed")
                parse_report["warnings"].append({"message": "qwen_usage_log_write_failed"})
                parse_report["stats"]["warnings_count"] = len(parse_report["warnings"])
    zone_qwen_usage = dict(zone_usage) if zone_usage else (
        dict(qwen_usage) if qwen_usage.get("call_mode") == "bundle" else {}
    )
    zone_report = {
        "document_zones": document_zones.model_dump(mode="json"),
        "warnings": [warning for warning in all_warnings if warning.startswith("qwen_document_zones") or warning.startswith("document_zones") or warning.startswith("front_matter_zone")],
        "validation": zone_validation,
        "qwen_usage": zone_qwen_usage,
    }
    if zone_usage:
        parse_report["qwen_zone_usage"] = dict(zone_usage)
        try:
            write_qwen_zone_log(zone_usage)
        except OSError:
            all_warnings.append("qwen_zone_usage_log_write_failed")
            parse_report["warnings"].append({"message": "qwen_zone_usage_log_write_failed"})
            parse_report["stats"]["warnings_count"] = len(parse_report["warnings"])

    return CleanResult(
        cleaned_markdown=clean_result.cleaned_markdown,
        format_probe=probe_dict,
        strategy=strategy.to_dict(),
        document_zones=document_zones.model_dump(mode="json"),
        zone_report=zone_report,
        parse_report=parse_report,
        warnings=all_warnings,
    )
