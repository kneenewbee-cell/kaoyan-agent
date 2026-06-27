from __future__ import annotations

import copy
import json
import re
from typing import Any

from pydantic import ValidationError

from ..pipeline_logger import sanitize_for_log
from .strategy_schema import CleaningStrategy, HeadingFamily, RelationHint


DANGEROUS_TOKENS = ("eval", "exec", "import", "subprocess", "os.system", "open(", "__")
CHINESE_NUM = "零〇一二三四五六七八九十百千万两"
HEADING_FAMILY_KEYS = {
    "id",
    "enabled",
    "kind",
    "anchors",
    "anchor_position",
    "ordinal_styles",
    "ordinal_required",
    "units",
    "separators",
    "title_required",
    "parent_hints",
    "min_repeats",
    "examples",
}
RELATION_HINT_KEYS = {
    "relation_type",
    "parent",
    "child",
    "score",
    "certainty",
    "score_breakdown",
    "evidence",
    "scope",
}


def _strip_markdown_heading_marker(value: str) -> str:
    return re.sub(r"^\s*#{1,6}\s+", "", value.strip())


def _family_examples(family: dict[str, Any]) -> list[str]:
    examples = family.get("examples")
    if not isinstance(examples, list):
        return []
    return [_strip_markdown_heading_marker(str(example)) for example in examples if str(example).strip()]


def _looks_like_alpha_outline_family(family: dict[str, Any]) -> bool:
    family_id = str(family.get("id") or "").lower()
    if any(hint in family_id for hint in ("alpha", "letter", "字母")):
        return True
    for example in _family_examples(family):
        if re.match(r"^[A-Z]\s*[\u4e00-\u9fff]\S+", example.strip()):
            return True
    return False


def _family_has_matcher_shape(family: dict[str, Any]) -> bool:
    return bool(family.get("anchors") or family.get("ordinal_styles") or family.get("units"))


def _normalize_outline_family_shape(family: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for key in list(family):
        if key in HEADING_FAMILY_KEYS:
            continue
        normalized_key = re.sub(r"[^A-Za-z_]", "", str(key))
        if normalized_key == "separators":
            if "separators" not in family and isinstance(family.get(key), list):
                family["separators"] = family[key]
            family.pop(key, None)
            warnings.append("strategy_family_malformed_key_repaired")
            continue
        family.pop(key, None)
        warnings.append("strategy_family_extra_key_dropped")

    original_kind = family.get("kind")
    anchors = family.get("anchors")
    styles = family.get("ordinal_styles")
    units = family.get("units")
    if not isinstance(anchors, list):
        anchors = []
    if not isinstance(styles, list):
        styles = []
    if not isinstance(units, list):
        units = []

    cleaned_anchors = [str(anchor).strip() for anchor in anchors if str(anchor).strip()]
    cleaned_units = [str(unit).strip() for unit in units if str(unit).strip()]
    anchor_set = set(cleaned_anchors)

    examples = family.get("examples")
    if isinstance(examples, list):
        cleaned_examples = [_strip_markdown_heading_marker(str(example)) for example in examples]
        cleaned_examples = [example for example in cleaned_examples if example]
        if cleaned_examples != examples:
            family["examples"] = cleaned_examples
            warnings.append("strategy_family_examples_heading_markers_stripped")

    if family.get("kind") == "strong_boundary" and cleaned_anchors and cleaned_units:
        boundary_units = {"篇", "章", "节", "部分", "卷", "课"}
        normalized_anchors: list[str] = []
        changed = False
        for anchor in cleaned_anchors:
            normalized = anchor
            for unit in cleaned_units:
                if unit in boundary_units and anchor.startswith("第") and anchor.endswith(unit) and anchor != "第":
                    normalized = anchor[: -len(unit)] or "第"
                    changed = True
                    break
            normalized_anchors.append(normalized)
        if changed:
            family["anchors"] = list(dict.fromkeys(normalized_anchors))
            cleaned_anchors = [str(anchor).strip() for anchor in family["anchors"] if str(anchor).strip()]
            anchor_set = set(cleaned_anchors)
            warnings.append("strategy_family_chapter_anchor_repaired")

    if family.get("kind") != "strong_boundary" and cleaned_anchors and cleaned_units and family.get("ordinal_required"):
        overlapped_units = {
            unit
            for unit in cleaned_units
            if any(anchor.endswith(unit) and len(anchor) > len(unit) for anchor in cleaned_anchors)
        }
        if overlapped_units:
            family["units"] = [unit for unit in cleaned_units if unit not in overlapped_units]
            warnings.append("strategy_family_anchor_unit_overlap_repaired")

    if family.get("kind") == "strong_boundary" and not family.get("units") and styles:
        family["kind"] = "major_section"
        warnings.append("strategy_family_strong_boundary_without_units_repaired")

    chinese_outline = all(re.fullmatch(rf"[{CHINESE_NUM}]+、", anchor) for anchor in cleaned_anchors) if cleaned_anchors else False
    paren_chinese = all(
        re.fullmatch(rf"[（(]\s*[{CHINESE_NUM}]+\s*[）)]", anchor) for anchor in cleaned_anchors
    ) if cleaned_anchors else False
    paren_arabic = all(re.fullmatch(r"[（(]\s*\d+\s*[）)]", anchor) for anchor in cleaned_anchors) if cleaned_anchors else False
    arabic_outline = all(re.fullmatch(r"\d+[.．、]", anchor) for anchor in cleaned_anchors) if cleaned_anchors else False

    if not cleaned_anchors and not cleaned_units and not styles and _looks_like_alpha_outline_family(family):
        family["anchors"] = []
        if original_kind not in {"major_section", "block", "item", "strong_boundary"}:
            family["kind"] = "major_section"
        family["ordinal_styles"] = ["alpha"]
        family["ordinal_required"] = True
        family["separators"] = ["", " "]
        warnings.append("strategy_family_alpha_outline_repaired")
    elif chinese_outline:
        family["anchors"] = []
        if original_kind not in {"major_section", "block", "item", "strong_boundary"}:
            family["kind"] = "outline"
        family["ordinal_styles"] = ["chinese"]
        family["ordinal_required"] = True
        family["separators"] = ["、"]
        warnings.append("strategy_family_outline_anchors_normalized")
    elif paren_chinese or (bool(cleaned_anchors) and anchor_set <= {"(", "（"} and "chinese" in styles):
        family["anchors"] = []
        if original_kind not in {"major_section", "block", "item", "strong_boundary"}:
            family["kind"] = "outline"
        family["ordinal_styles"] = ["paren_chinese"]
        family["ordinal_required"] = True
        family["separators"] = ["", " "]
        warnings.append("strategy_family_outline_anchors_normalized")
    elif paren_arabic or (bool(cleaned_anchors) and anchor_set <= {"(", "（"} and "arabic" in styles):
        family["anchors"] = []
        if original_kind not in {"major_section", "block", "item", "strong_boundary"}:
            family["kind"] = "outline"
        family["ordinal_styles"] = ["paren_arabic"]
        family["ordinal_required"] = True
        family["separators"] = ["", " "]
        warnings.append("strategy_family_outline_anchors_normalized")
    elif arabic_outline:
        family["anchors"] = []
        if original_kind not in {"major_section", "block", "item", "strong_boundary"}:
            family["kind"] = "outline"
        family["ordinal_styles"] = ["arabic"]
        family["ordinal_required"] = True
        family["separators"] = [".", "．", "、"]
        warnings.append("strategy_family_outline_anchors_normalized")

    if not family.get("anchors") and family.get("kind") not in {"outline", "strong_boundary", "major_section", "block", "item"}:
        family["kind"] = "outline"
        family["ordinal_required"] = True
        warnings.append("strategy_family_kind_normalized_to_outline")

    return warnings


def _has_relation_path(
    graph: dict[str, list[str]],
    start: str,
    target: str,
    *,
    skip_edge: tuple[str, str] | None = None,
) -> bool:
    stack = [start]
    seen: set[str] = set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        for next_node in graph.get(node, []):
            if skip_edge == (node, next_node):
                continue
            if next_node == target:
                return True
            stack.append(next_node)
    return False


def _repair_relation_hints(
    relation_hints: object,
    *,
    family_ids: set[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if relation_hints in (None, ""):
        return [], warnings
    if not isinstance(relation_hints, list):
        return [], ["strategy_relation_hints_invalid_dropped"]

    candidate_hints: list[RelationHint] = []
    seen_edges: set[tuple[str, str]] = set()
    for raw_hint in relation_hints:
        if not isinstance(raw_hint, dict):
            warnings.append("strategy_relation_hint_invalid_entry_dropped")
            continue
        hint = {key: value for key, value in raw_hint.items() if key in RELATION_HINT_KEYS}
        if hint != raw_hint:
            warnings.append("strategy_relation_hint_extra_key_dropped")
        if hint.get("relation_type") in (None, ""):
            hint["relation_type"] = "direct_parent"
        if hint.get("certainty") in (None, ""):
            hint["certainty"] = "strong"
        if hint.get("scope") in (None, ""):
            hint["scope"] = "body"
        try:
            validated_hint = RelationHint.model_validate(hint)
        except ValidationError:
            warnings.append("strategy_relation_hint_invalid_dropped")
            continue
        if validated_hint.parent not in family_ids or validated_hint.child not in family_ids:
            warnings.append("strategy_relation_hint_unknown_family_dropped")
            continue
        edge = (validated_hint.parent, validated_hint.child)
        if edge in seen_edges:
            warnings.append("strategy_relation_hint_duplicate_dropped")
            continue
        seen_edges.add(edge)
        candidate_hints.append(validated_hint)

    graph: dict[str, list[str]] = {}
    for hint in candidate_hints:
        graph.setdefault(hint.parent, []).append(hint.child)

    repaired_hints: list[RelationHint] = []
    for hint in candidate_hints:
        edge = (hint.parent, hint.child)
        if _has_relation_path(graph, hint.child, hint.parent):
            warnings.append("strategy_relation_hint_cycle_dropped")
            continue
        if _has_relation_path(graph, hint.parent, hint.child, skip_edge=edge):
            warnings.append("strategy_relation_hint_transitive_dropped")
            continue
        repaired_hints.append(hint)

    return [hint.model_dump(mode="json") for hint in repaired_hints], warnings


def default_conservative_strategy(*, reason: str = "No reliable structure strategy") -> CleaningStrategy:
    return CleaningStrategy(
        document_profile={"subject": "unknown", "document_type": "unknown", "language": "zh", "confidence": 0.3},
        main_section_rule={
            "enabled": False,
            "target_level": 2,
            "marker_type": "none",
            "aliases": [],
            "number_styles": [],
            "requires_line_start": True,
            "requires_colon": False,
            "min_repeats": 2,
            "examples": [],
        },
        subsection_rules=[],
        fallback_policy={
            "if_main_sections_less_than": 2,
            "action": "keep_original_structure",
            "chunk_by": "length",
            "reason": reason,
        },
        strategy_source="default",
    )


def _contains_dangerous_token(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_dangerous_token(k) or _contains_dangerous_token(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_dangerous_token(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in DANGEROUS_TOKENS)
    return False


def parse_strategy_payload(payload: str | dict[str, Any] | CleaningStrategy) -> tuple[dict[str, Any] | None, list[str]]:
    if isinstance(payload, CleaningStrategy):
        return payload.to_dict(), []
    if isinstance(payload, dict):
        return payload, []
    if not isinstance(payload, str):
        return None, ["strategy_payload_not_json_or_dict"]
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return None, ["strategy_payload_not_json"]
    if not isinstance(parsed, dict):
        return None, ["strategy_payload_not_object"]
    return parsed, []


def summarize_strategy_payload(data: dict[str, Any]) -> dict[str, Any]:
    heading_families = data.get("heading_families", []) or []
    relation_hints = data.get("relation_hints", []) or []
    document_zones = data.get("document_zones") or {}
    front_matter_zones = []
    if isinstance(document_zones, dict):
        raw_zones = document_zones.get("front_matter_zones", []) or []
        if isinstance(raw_zones, list):
            front_matter_zones = [
                {
                    "type": zone.get("type"),
                    "start_line": zone.get("start_line"),
                    "end_line": zone.get("end_line"),
                    "action": zone.get("action"),
                    "chunk_policy": zone.get("chunk_policy"),
                    "confidence": zone.get("confidence"),
                }
                for zone in raw_zones
                if isinstance(zone, dict)
            ]
    return sanitize_for_log(
        {
            "top_level_keys": sorted(str(key) for key in data.keys()),
            "version": data.get("version"),
            "strategy_source": data.get("strategy_source"),
            "document_profile": data.get("document_profile"),
            "document_zones": {
                "body_start_line": document_zones.get("body_start_line") if isinstance(document_zones, dict) else None,
                "confidence": document_zones.get("confidence") if isinstance(document_zones, dict) else None,
                "front_matter_zones": front_matter_zones[:8],
            },
            "main_section_rule": data.get("main_section_rule"),
            "subsection_rule_count": len(data.get("subsection_rules", []) or []),
            "heading_family_count": len(heading_families),
            "heading_families": [
                {
                    "id": family.get("id"),
                    "kind": family.get("kind"),
                    "anchors": family.get("anchors"),
                    "ordinal_styles": family.get("ordinal_styles"),
                    "ordinal_required": family.get("ordinal_required"),
                    "units": family.get("units"),
                    "parent_hints": family.get("parent_hints"),
                    "min_repeats": family.get("min_repeats"),
                }
                for family in heading_families
                if isinstance(family, dict)
            ],
            "relation_hint_count": len(relation_hints),
            "relation_hints": [
                {
                    "parent": hint.get("parent"),
                    "child": hint.get("child"),
                    "score": hint.get("score"),
                    "certainty": hint.get("certainty"),
                    "scope": hint.get("scope"),
                }
                for hint in relation_hints
                if isinstance(hint, dict)
            ],
        }
    )


def _validation_errors_for_log(exc: ValidationError) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for error in exc.errors():
        loc = ".".join(str(part) for part in error.get("loc", ()))
        errors.append(
            {
                "loc": loc,
                "type": error.get("type"),
                "msg": error.get("msg"),
            }
        )
    return errors


def _repair_strategy_payload(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    repaired = copy.deepcopy(data)
    warnings: list[str] = []
    if "document_zones" in repaired:
        repaired.pop("document_zones", None)
        warnings.append("strategy_document_zones_ignored")
    if "heading_rules" in repaired:
        repaired.pop("heading_rules", None)
        warnings.append("strategy_legacy_heading_rules_dropped")
    families = repaired.get("heading_families")
    if isinstance(families, list):
        candidate_families: list[dict[str, Any]] = []
        dropped_family_ids: set[str] = set()
        for family in families:
            if not isinstance(family, dict):
                warnings.append("strategy_family_invalid_entry_dropped")
                continue
            warnings.extend(_normalize_outline_family_shape(family))
            examples = family.get("examples")
            if isinstance(examples, list) and len(examples) > 8:
                family["examples"] = examples[:8]
                warnings.append("strategy_family_examples_truncated")
            separators = family.get("separators")
            if separators == []:
                family["separators"] = ["", " ", "、", ".", "．", "|", "：", ":"]
                warnings.append("strategy_family_separators_defaulted")
            if _family_has_matcher_shape(family):
                candidate_families.append(family)
            else:
                family_id = family.get("id")
                if isinstance(family_id, str):
                    dropped_family_ids.add(family_id)
                warnings.append("strategy_family_without_matcher_dropped")

        repaired_families: list[dict[str, Any]] = []
        seen_family_ids: set[str] = set()
        for family in candidate_families:
            family_id = family.get("id")
            family_id_text = family_id.strip() if isinstance(family_id, str) else ""
            if family_id_text and family_id_text in seen_family_ids:
                dropped_family_ids.add(family_id_text)
                warnings.append("strategy_family_duplicate_id_dropped")
                continue
            try:
                validated_family = HeadingFamily.model_validate(family)
            except ValidationError:
                if family_id_text:
                    dropped_family_ids.add(family_id_text)
                warnings.append("strategy_family_invalid_dropped")
                continue
            if family_id_text:
                seen_family_ids.add(family_id_text)
            repaired_families.append(validated_family.model_dump(mode="json"))

        if dropped_family_ids:
            for family in repaired_families:
                parent_hints = family.get("parent_hints")
                if not isinstance(parent_hints, list):
                    continue
                cleaned_parent_hints = [
                    hint
                    for hint in parent_hints
                    if not (isinstance(hint, str) and hint in dropped_family_ids)
                ]
                if cleaned_parent_hints != parent_hints:
                    family["parent_hints"] = cleaned_parent_hints
                    warnings.append("strategy_family_parent_hints_repaired")
        repaired["heading_families"] = repaired_families
        family_ids = {
            family.get("id")
            for family in repaired_families
            if isinstance(family.get("id"), str)
        }
        repaired_relation_hints, relation_warnings = _repair_relation_hints(
            repaired.get("relation_hints"),
            family_ids={str(family_id) for family_id in family_ids if family_id},
        )
        warnings.extend(relation_warnings)
        repaired["relation_hints"] = repaired_relation_hints
    elif "relation_hints" in repaired:
        repaired.pop("relation_hints", None)
        warnings.append("strategy_relation_hints_without_families_dropped")
    return repaired, sorted(set(warnings))


def validate_cleaning_strategy(
    payload: str | dict[str, Any] | CleaningStrategy,
    *,
    fallback_source: str = "default",
    diagnostics: dict[str, Any] | None = None,
) -> tuple[CleaningStrategy, list[str], bool]:
    warnings: list[str] = []
    data, parse_warnings = parse_strategy_payload(payload)
    warnings.extend(parse_warnings)
    if diagnostics is not None:
        diagnostics["parse_warnings"] = list(parse_warnings)
    if data is None:
        if diagnostics is not None:
            diagnostics["result"] = "payload_parse_failed"
        strategy = default_conservative_strategy(reason="strategy payload is not valid JSON")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    if diagnostics is not None:
        diagnostics["payload_summary"] = summarize_strategy_payload(data)

    if _contains_dangerous_token(data):
        warnings.append("strategy_rejected_dangerous_token")
        if diagnostics is not None:
            diagnostics["result"] = "dangerous_token_rejected"
        strategy = default_conservative_strategy(reason="strategy contains dangerous tokens")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    data, repair_warnings = _repair_strategy_payload(data)
    warnings.extend(repair_warnings)
    if diagnostics is not None and repair_warnings:
        diagnostics["repair_warnings"] = list(repair_warnings)
        diagnostics["repaired_payload_summary"] = summarize_strategy_payload(data)

    try:
        strategy = CleaningStrategy.model_validate(data)
    except ValidationError as exc:
        warnings.append("strategy_schema_validation_failed")
        warnings.extend(error["type"] for error in exc.errors()[:5])
        if diagnostics is not None:
            schema_errors = _validation_errors_for_log(exc)
            diagnostics["result"] = "schema_validation_failed"
            diagnostics["schema_error_count"] = len(schema_errors)
            diagnostics["schema_errors"] = schema_errors[:20]
        strategy = default_conservative_strategy(reason="strategy schema validation failed")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    if strategy.strategy_source == "default" and fallback_source in {"qwen", "local"}:
        strategy.strategy_source = fallback_source
    if diagnostics is not None:
        diagnostics["result"] = "valid"
        diagnostics["validated_strategy_source"] = strategy.strategy_source
    return strategy, warnings, False
