from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schemas import DetectedFile


DEFAULT_LARGE_PDF_THRESHOLD_MB = 180.0
DEFAULT_LARGE_PDF_PAGE_THRESHOLD = 180
DEFAULT_PDF_MODE = "auto"
VALID_PDF_MODES = {"auto", "normal", "split"}


@dataclass(frozen=True)
class PdfRouteDecision:
    is_pdf: bool
    mode: str
    selected_route: str
    reason: str
    size_bytes: int
    size_mb: float
    threshold_mb: float
    page_count: int | None
    page_threshold: int

    @property
    def use_large_pdf_route(self) -> bool:
        return self.selected_route == "large_pdf_split"

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_pdf": self.is_pdf,
            "mode": self.mode,
            "selected_route": self.selected_route,
            "reason": self.reason,
            "size_bytes": self.size_bytes,
            "size_mb": round(self.size_mb, 4),
            "threshold_mb": self.threshold_mb,
            "page_count": self.page_count,
            "page_threshold": self.page_threshold,
        }


def _metadata_float(metadata: dict[str, Any], key: str) -> float | None:
    value = metadata.get(key)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value in (None, ""):
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _metadata_int(metadata: dict[str, Any], key: str) -> int | None:
    value = metadata.get(key)
    if value in (None, ""):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value in (None, ""):
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _normalize_mode(value: Any) -> str:
    mode = str(value or DEFAULT_PDF_MODE).strip().lower()
    return mode if mode in VALID_PDF_MODES else DEFAULT_PDF_MODE


def decide_pdf_route(detected: DetectedFile, metadata: dict[str, Any] | None = None) -> PdfRouteDecision:
    metadata = metadata or {}
    threshold_mb = (
        _metadata_float(metadata, "large_pdf_threshold_mb")
        or _env_float("MATERIALS_LARGE_PDF_THRESHOLD_MB", DEFAULT_LARGE_PDF_THRESHOLD_MB)
    )
    page_threshold = (
        _metadata_int(metadata, "large_pdf_page_threshold")
        or _env_int("MATERIALS_LARGE_PDF_PAGE_THRESHOLD", DEFAULT_LARGE_PDF_PAGE_THRESHOLD)
    )
    mode = _normalize_mode(metadata.get("pdf_mode") or os.environ.get("MATERIALS_PDF_MODE"))
    size_mb = detected.size_bytes / (1024 * 1024)
    is_pdf = detected.file_ext.lower() == ".pdf"
    page_count = detected.page_count

    if not is_pdf:
        return PdfRouteDecision(
            is_pdf=False,
            mode=mode,
            selected_route="current",
            reason="not_pdf",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    if mode == "normal":
        return PdfRouteDecision(
            is_pdf=True,
            mode=mode,
            selected_route="current",
            reason="forced_normal",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    if mode == "split":
        return PdfRouteDecision(
            is_pdf=True,
            mode=mode,
            selected_route="large_pdf_split",
            reason="forced_split",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    size_exceeded = size_mb >= threshold_mb
    page_exceeded = page_count is not None and page_count >= page_threshold
    if size_exceeded and page_exceeded:
        return PdfRouteDecision(
            is_pdf=True,
            mode=mode,
            selected_route="large_pdf_split",
            reason="size_and_page_threshold",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    if size_mb >= threshold_mb:
        return PdfRouteDecision(
            is_pdf=True,
            mode=mode,
            selected_route="large_pdf_split",
            reason="size_threshold",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    if page_exceeded:
        return PdfRouteDecision(
            is_pdf=True,
            mode=mode,
            selected_route="large_pdf_split",
            reason="page_threshold",
            size_bytes=detected.size_bytes,
            size_mb=size_mb,
            threshold_mb=threshold_mb,
            page_count=page_count,
            page_threshold=page_threshold,
        )

    return PdfRouteDecision(
        is_pdf=True,
        mode=mode,
        selected_route="current",
        reason="below_threshold",
        size_bytes=detected.size_bytes,
        size_mb=size_mb,
        threshold_mb=threshold_mb,
        page_count=page_count,
        page_threshold=page_threshold,
    )


def write_large_pdf_route_plan(
    material_dir: Path,
    detected: DetectedFile,
    decision: PdfRouteDecision,
) -> Path:
    parsed_dir = material_dir / "parsed"
    parsed_dir.mkdir(parents=True, exist_ok=True)
    target = parsed_dir / "large_pdf_route_plan.json"
    plan = {
        "version": "0.1",
        "route": "large_pdf_split",
        "status": "pending_implementation",
        "small_pdf_path_unchanged": True,
        "decision": decision.to_dict(),
        "source": {
            "original_filename": detected.original_filename,
            "file_ext": detected.file_ext,
            "mime_type": detected.mime_type,
            "sha256": detected.sha256,
            "size_bytes": detected.size_bytes,
            "page_count": detected.page_count,
        },
        "sample_strategy": {
            "first_pass": "Build front/middle/tail PDF samples, parse those samples with MinerU, then reuse the current format_probe/Qwen input budget.",
            "toc_detail_pass": "Only when first-pass Qwen cannot recover chapter pages, send raw uncompressed toc line ranges to a second Qwen call.",
            "layout_policy": "Send sample layout summaries only; do not send full global layout.json to Qwen.",
        },
        "future_outputs": [
            "sample_markdown",
            "sample_format_probe",
            "cleaning_strategy",
            "document_zones",
            "toc_line_ranges",
            "chapter_page_plan",
            "chapter_pdf_files",
        ],
    }
    target.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return target
