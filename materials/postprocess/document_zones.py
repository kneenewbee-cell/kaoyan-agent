from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from ..pipeline_logger import sanitize_for_log
from .strategy_schema import DocumentZones


DANGEROUS_TOKENS = ("eval", "exec", "import", "subprocess", "os.system", "open(", "__")
CATALOG_NAVIGATION_SIGNALS = {
    "catalog",
    "toc",
    "navigation",
    "目录",
    "dense_chapter_headings",
    "repeated_chapter_headings",
    "chapter_heading_reappears_later",
    "page_references",
    "count_badges",
    "difficulty_labels",
    "chapter_overview",
    "section_overview",
}


def default_document_zones() -> DocumentZones:
    return DocumentZones(front_matter_zones=[], body_start_line=None, confidence=0.0)


def _contains_dangerous_token(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_dangerous_token(k) or _contains_dangerous_token(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_dangerous_token(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in DANGEROUS_TOKENS)
    return False


def parse_document_zones_payload(payload: str | dict[str, Any] | DocumentZones) -> tuple[dict[str, Any] | None, list[str]]:
    if isinstance(payload, DocumentZones):
        return payload.model_dump(mode="json"), []
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return None, ["document_zones_payload_not_json"]
    if not isinstance(payload, dict):
        return None, ["document_zones_payload_not_object"]
    if "document_zones" in payload and isinstance(payload.get("document_zones"), dict):
        payload = payload["document_zones"]
    return payload, []


def summarize_document_zones_payload(payload: dict[str, Any]) -> dict[str, Any]:
    zones = payload.get("front_matter_zones", []) or []
    if not isinstance(zones, list):
        zones = []
    return sanitize_for_log(
        {
            "body_start_line": payload.get("body_start_line"),
            "confidence": payload.get("confidence"),
            "front_matter_zone_count": len(zones),
            "front_matter_zones": [
                {
                    "type": zone.get("type"),
                    "start_line": zone.get("start_line"),
                    "end_line": zone.get("end_line"),
                    "action": zone.get("action"),
                    "chunk_policy": zone.get("chunk_policy"),
                    "confidence": zone.get("confidence"),
                }
                for zone in zones[:8]
                if isinstance(zone, dict)
            ],
        }
    )


def _validation_errors_for_log(exc: ValidationError) -> list[dict[str, Any]]:
    return [
        {
            "loc": ".".join(str(part) for part in error.get("loc", ())),
            "type": error.get("type"),
            "msg": error.get("msg"),
        }
        for error in exc.errors()
    ]


def _catalog_zone_has_navigation_signal(zone: dict[str, Any]) -> bool:
    title = str(zone.get("title") or "").lower()
    if "目录" in title or "catalog" in title or "toc" in title or "navigation" in title:
        return True
    signals = zone.get("signals") or []
    if not isinstance(signals, list):
        return False
    normalized = {str(signal).strip().lower() for signal in signals}
    return bool(normalized & {signal.lower() for signal in CATALOG_NAVIGATION_SIGNALS})


def _repair_document_zones_payload(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    zones = data.get("front_matter_zones")
    if not isinstance(zones, list):
        return data, warnings

    repaired_zones: list[Any] = []
    for zone in zones:
        if not isinstance(zone, dict):
            repaired_zones.append(zone)
            continue
        confidence = zone.get("confidence")
        high_confidence = isinstance(confidence, (int, float)) and float(confidence) >= 0.65
        if zone.get("type") == "catalog_or_navigation" and high_confidence and not _catalog_zone_has_navigation_signal(zone):
            warnings.append("document_zones_catalog_without_navigation_signal_dropped")
            continue
        repaired_zones.append(zone)

    if len(repaired_zones) != len(zones):
        data = {**data, "front_matter_zones": repaired_zones}
    return data, warnings


def validate_document_zones_payload(
    payload: str | dict[str, Any] | DocumentZones,
    *,
    diagnostics: dict[str, Any] | None = None,
) -> tuple[DocumentZones, list[str], bool]:
    warnings: list[str] = []
    data, parse_warnings = parse_document_zones_payload(payload)
    warnings.extend(parse_warnings)
    if diagnostics is not None:
        diagnostics["parse_warnings"] = list(parse_warnings)
    if data is None:
        if diagnostics is not None:
            diagnostics["result"] = "payload_parse_failed"
        return default_document_zones(), warnings, True

    if diagnostics is not None:
        diagnostics["payload_summary"] = summarize_document_zones_payload(data)

    if _contains_dangerous_token(data):
        warnings.append("document_zones_rejected_dangerous_token")
        if diagnostics is not None:
            diagnostics["result"] = "dangerous_token_rejected"
        return default_document_zones(), warnings, True

    data, repair_warnings = _repair_document_zones_payload(data)
    warnings.extend(repair_warnings)
    if diagnostics is not None and repair_warnings:
        diagnostics["repair_warnings"] = list(repair_warnings)
        diagnostics["repaired_payload_summary"] = summarize_document_zones_payload(data)

    try:
        zones = DocumentZones.model_validate(data)
    except ValidationError as exc:
        warnings.append("document_zones_schema_validation_failed")
        if diagnostics is not None:
            schema_errors = _validation_errors_for_log(exc)
            diagnostics["result"] = "schema_validation_failed"
            diagnostics["schema_error_count"] = len(schema_errors)
            diagnostics["schema_errors"] = schema_errors[:20]
        return default_document_zones(), warnings, True

    if diagnostics is not None:
        diagnostics["result"] = "valid"
    return zones, warnings, False
