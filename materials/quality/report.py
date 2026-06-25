"""materials/quality/report.py — 生成 parsed/parse_report.json。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..schemas import Chunk, QualityReport, QualityStatus
from .confidence import clamp_score, status_from_score, weighted_average
from .validators import asset_metrics, chunk_metrics, heading_metrics, text_metrics


def _score_parse(metrics: dict[str, Any], warnings: list[str]) -> float:
    score = 1.0
    if metrics["char_count"] < 100:
        score -= 0.35
        warnings.append("content_too_short")
    if metrics["broken_char_ratio"] > 0.02:
        score -= 0.30
        warnings.append("high_broken_char_ratio")
    if metrics["repeat_line_ratio"] > 0.45:
        score -= 0.20
        warnings.append("high_repeat_line_ratio")
    return clamp_score(score)


def _score_structure(metrics: dict[str, Any], text_char_count: int, warnings: list[str]) -> float:
    score = 1.0
    if metrics["heading_count"] == 0:
        score -= 0.35
        warnings.append("no_markdown_heading")
    elif metrics["heading_count"] == 1 and text_char_count > 3000:
        score -= 0.18
        warnings.append("too_few_headings_for_long_document")
    if metrics["short_heading_count"] > 3:
        score -= 0.15
        warnings.append("many_short_headings")
    if metrics["heading_level_jump_count"] > 2:
        score -= 0.12
        warnings.append("heading_level_jumps")
    unmatched_strategy_rules = sum(
        1 for warning in warnings if warning.startswith("strategy_rule_not_matched:")
    )
    if unmatched_strategy_rules:
        score -= min(0.30, unmatched_strategy_rules * 0.12)
        warnings.append("strategy_execution_incomplete")
    if "main_section_matches_below_threshold" in warnings:
        score -= 0.20
    if "qwen_strategy_invalid_fallback_to_local" in warnings or "strategy_schema_validation_failed" in warnings:
        score -= 0.08
        warnings.append("llm_strategy_fallback")
    return clamp_score(score)


def _score_assets(metrics: dict[str, Any], warnings: list[str]) -> float:
    count = metrics["image_ref_count"]
    missing = metrics["missing_image_count"]
    if count == 0:
        return 1.0
    if missing:
        warnings.append("missing_image_refs")
    return clamp_score(1.0 - (missing / max(count, 1)) * 0.7)


def _score_chunks(metrics: dict[str, Any], warnings: list[str]) -> float:
    if metrics["chunk_count"] == 0:
        warnings.append("no_chunks_generated")
        return 0.0
    score = 1.0
    if metrics["empty_chunk_count"]:
        score -= 0.30
        warnings.append("empty_chunks")
    if metrics["long_chunk_count"]:
        score -= 0.18
        warnings.append("long_chunks")
    if metrics["duplicate_chunk_count"]:
        score -= 0.12
        warnings.append("duplicate_chunks")
    if metrics["missing_heading_path_count"] == metrics["chunk_count"] and metrics["chunk_count"] > 1:
        score -= 0.12
        warnings.append("chunks_missing_heading_path")
    if metrics.get("unique_heading_path_count", 0) <= 1 and metrics["chunk_count"] >= 10:
        score -= 0.12
        warnings.append("low_chunk_heading_path_diversity")
    return clamp_score(score)


def build_quality_report(
    markdown: str,
    material_dir: Path | None = None,
    chunks: list[Chunk] | None = None,
    parser_warnings: list[str] | None = None,
    postprocess_warnings: list[str] | None = None,
) -> QualityReport:
    warnings: list[str] = []
    warnings.extend(parser_warnings or [])
    warnings.extend(postprocess_warnings or [])

    tm = text_metrics(markdown)
    hm = heading_metrics(markdown)
    am = asset_metrics(markdown, material_dir=material_dir)
    cm = chunk_metrics(chunks)

    parse_confidence = _score_parse(tm, warnings)
    structure_confidence = _score_structure(hm, tm["char_count"], warnings)
    asset_confidence = _score_assets(am, warnings)
    chunk_confidence = _score_chunks(cm, warnings)
    overall = weighted_average({
        "parse": (parse_confidence, 0.35),
        "structure": (structure_confidence, 0.25),
        "asset": (asset_confidence, 0.20),
        "chunk": (chunk_confidence, 0.20),
    })
    status = QualityStatus(status_from_score(overall))

    return QualityReport(
        quality_status=status,
        overall_confidence=overall,
        parse_confidence=parse_confidence,
        structure_confidence=structure_confidence,
        asset_confidence=asset_confidence,
        chunk_confidence=chunk_confidence,
        warnings=sorted(set(warnings)),
        metrics={
            "text": tm,
            "headings": hm,
            "assets": am,
            "chunks": cm,
        },
    )


def save_quality_report(report: QualityReport, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
