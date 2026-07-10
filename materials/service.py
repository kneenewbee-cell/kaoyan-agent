from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from .chunking.chunker import chunk_markdown_file
from .detector import detect_file
from .indexing.material_indexer import build_search_index
from .indexing.vector_indexer import build_material_vector_index, delete_material_vector_index
from .large_pdf_pipeline import run_large_pdf_split_pipeline
from .large_pdf_chapters import restore_large_pdf_chapter_headings
from .postprocess.asset_rewriter import save_and_rewrite_images
from .postprocess.formula_cleaner import clean_formulas_with_report
from .postprocess.layout_sidecar import (
    build_layout_context,
    build_table_chunks,
    replace_html_tables_with_layout_markdown,
    save_layout_artifacts,
)
from .postprocess.llm_cleaner import clean_markdown_with_llm_patches
from .postprocess.metadata_extractor import (
    extract_title_from_markdown,
    infer_material_type_from_markdown,
    infer_subject_from_markdown,
)
from .postprocess.qwen_formula_client import build_qwen_formula_repair_client_from_env
from .postprocess.raw_markdown_cleaner import clean_raw_markdown
from .postprocess.exercise_structure import analyze_exercise_structure
from .postprocess.exercise_structure_repair import repair_exercise_structure
from .postprocess.deepseek_structure_client import build_deepseek_structure_repair_client_from_env
from .postprocess.structure_profile import infer_material_structure_profile
from .quality.report import build_quality_report, save_quality_report
from .pipeline_logger import MaterialPipelineLogger, monotonic_ms
from .pdf_routing import decide_pdf_route, write_large_pdf_route_plan
from .resolver import resolve_upload_path
from .router import get_parser
from .schemas import (
    MaterialIngestionResult,
    MaterialManifest,
    MaterialType,
    ParseStatus,
    ParserName,
    Subject,
    normalize_material_type_value,
)
from .security import resolve_material_id, resolve_user_id
from .storage import MaterialStorage


def _generate_material_id() -> str:
    return f"mat_{uuid.uuid4().hex[:16]}"


def _safe_relative(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


AUTO_VALUES = {"", "auto", "unknown", None}
METADATA_CONFIDENCE_THRESHOLD = 0.75


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    return bool(value)


def _normalize_formula_cleanup_level(value: Any) -> str:
    normalized = str(value or "safe").strip().lower()
    return normalized if normalized in {"safe", "experimental"} else "safe"


def _refresh_exercise_structure_summary(report: dict[str, Any], problem_groups: list[dict[str, Any]], repair_report: dict[str, Any]) -> dict[str, Any]:
    updated = dict(report)
    expected = updated.get("expected_problem_count")
    expected_count = int(expected) if isinstance(expected, int) else None
    problem_indices = {
        int(group["problem_index"])
        for group in problem_groups
        if isinstance(group.get("problem_index"), int)
    }
    applied_targets = {
        int(item["target_problem_index"])
        for item in list(repair_report.get("applied") or [])
        if isinstance(item, dict) and isinstance(item.get("target_problem_index"), int)
    }
    if expected_count:
        missing = [index for index in range(1, expected_count + 1) if index not in problem_indices]
    else:
        missing = [
            int(index)
            for index in list(updated.get("missing_problem_indices") or [])
            if isinstance(index, int) and int(index) not in applied_targets
        ]
    warnings = set(updated.get("warnings") or [])
    if int(repair_report.get("applied_count") or 0) > 0:
        warnings.add("exercise_structure_repaired")
    if missing:
        warnings.add("exercise_problem_indices_missing")
    else:
        warnings.discard("exercise_problem_count_below_expected")
        warnings.discard("exercise_problem_indices_missing")
    updated["problem_groups"] = problem_groups
    updated["problem_count"] = len(problem_groups)
    updated["missing_problem_indices"] = missing
    updated["repair_applied_count"] = int(repair_report.get("applied_count") or 0)
    if expected_count:
        coverage = len(problem_indices) / max(expected_count, 1)
        if coverage >= 0.95 and not missing:
            updated["status"] = "high"
            updated["confidence"] = max(float(updated.get("confidence") or 0.0), 0.9)
        elif coverage >= 0.75:
            updated["status"] = "medium"
            updated["confidence"] = max(float(updated.get("confidence") or 0.0), 0.72)
    elif not missing and len(problem_groups) >= 2:
        updated["status"] = "high"
        updated["confidence"] = max(float(updated.get("confidence") or 0.0), 0.9)
    updated["warnings"] = sorted(warnings)
    return updated


class MaterialIngestionService:
    """资料入库服务。

    当前纵向主链路：
    parser(.md/.txt) → raw markdown → clean/normalize → parsed/content.md
    → quality report → chunks → keyword index → manifest。
    """

    def __init__(self, storage: MaterialStorage | None = None):
        self.storage = storage or MaterialStorage()

    @staticmethod
    def _normalize_subject(subject: str, filename: str) -> Subject:
        if subject and subject not in {"unknown", "auto"}:
            try:
                return Subject(subject)
            except ValueError:
                pass
        return Subject.OTHER

    @staticmethod
    def _normalize_material_type(material_type: str, filename: str) -> MaterialType:
        return normalize_material_type_value(material_type)

    @staticmethod
    def _failure_result(
        material_id: str,
        user_id: str,
        error: str,
        manifest_path: Path | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MaterialIngestionResult:
        return MaterialIngestionResult(
            material_id=material_id,
            user_id=user_id,
            parse_status=ParseStatus.FAILED,
            manifest_path=str(manifest_path) if manifest_path else None,
            quality_status="failed",
            error=error,
            metadata=metadata or {},
        )

    @staticmethod
    def _is_auto_value(value: str | None) -> bool:
        return value in AUTO_VALUES

    @staticmethod
    def _metadata_profile_is_confident(profile: dict[str, Any]) -> bool:
        return str(profile.get("source") or "") == "qwen" and float(profile.get("confidence") or 0.0) >= METADATA_CONFIDENCE_THRESHOLD

    def _resolve_metadata_selection(
        self,
        *,
        selected_subject: str,
        selected_material_type: str,
        current_subject: Subject,
        current_material_type: MaterialType,
        metadata_profile: dict[str, Any],
        allow_metadata_mismatch: bool,
        use_llm_cleanup: bool,
    ) -> tuple[Subject | None, MaterialType | None, dict[str, Any] | None, str | None]:
        subject_auto = self._is_auto_value(selected_subject)
        type_auto = self._is_auto_value(selected_material_type)
        confident = self._metadata_profile_is_confident(metadata_profile)
        detected_subject = str(metadata_profile.get("subject") or "unknown")
        detected_type = str(metadata_profile.get("material_type") or "unknown")

        if use_llm_cleanup and (subject_auto or type_auto) and not confident:
            return None, None, {
                "reason": "qwen metadata profile is required for auto classification",
                "metadata_profile": metadata_profile,
            }, "metadata_detection_required"

        final_subject = current_subject
        final_type = current_material_type
        conflicts: list[dict[str, Any]] = []

        if confident and detected_subject in Subject._value2member_map_ and detected_subject != Subject.UNKNOWN.value:
            detected_subject_enum = Subject(detected_subject)
            if subject_auto:
                final_subject = detected_subject_enum
            elif detected_subject_enum != current_subject:
                conflicts.append(
                    {
                        "field": "subject",
                        "selected": current_subject.value,
                        "detected": detected_subject_enum.value,
                        "confidence": metadata_profile.get("confidence"),
                    }
                )

        if confident and detected_type in {
            MaterialType.TEXTBOOK.value,
            MaterialType.LECTURE.value,
            MaterialType.EXERCISE.value,
        }:
            detected_type_enum = MaterialType(detected_type)
            if type_auto:
                final_type = detected_type_enum
            elif detected_type_enum != current_material_type:
                conflicts.append(
                    {
                        "field": "material_type",
                        "selected": current_material_type.value,
                        "detected": detected_type_enum.value,
                        "confidence": metadata_profile.get("confidence"),
                    }
                )

        if conflicts and not allow_metadata_mismatch:
            first_conflict = dict(conflicts[0])
            first_conflict["conflicts"] = conflicts
            first_conflict["metadata_profile"] = metadata_profile
            return None, None, first_conflict, "metadata_conflict"

        return final_subject, final_type, {
            "metadata_profile": metadata_profile,
            "metadata_conflict": {
                "accepted_by_user": True,
                "conflicts": conflicts,
            } if conflicts else None,
        }, None

    def ingest_file(
        self,
        file_path: Path | str,
        user_id: str = "tester",
        subject: str = "unknown",
        material_type: str = "unknown",
        metadata: dict[str, Any] | None = None,
        use_llm_cleanup: bool = True,
        use_formula_cleanup: bool = True,
        formula_cleanup_level: str = "safe",
        enable_vector_index: bool | None = None,
        progress_callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> MaterialIngestionResult:
        """入库一个资料文件。

        use_llm_cleanup 表示是否允许 Qwen 读取 format_probe.json 生成 cleaning_strategy.json。
        即使启用，全文清洗仍由本地规则执行。
        use_formula_cleanup 表示是否启用本地公式渲染修复，默认只执行 safe 规则。
        """
        file_path = Path(file_path)
        safe_user_id = resolve_user_id(user_id)
        extra_metadata = dict(metadata or {})
        extra_metadata["use_llm_cleanup"] = bool(use_llm_cleanup)
        formula_cleanup_enabled = _coerce_bool(extra_metadata.get("use_formula_cleanup"), use_formula_cleanup)
        formula_cleanup_level_value = _normalize_formula_cleanup_level(
            extra_metadata.get("formula_cleanup_level", formula_cleanup_level)
        )
        llm_formula_cleanup_requested = _coerce_bool(extra_metadata.get("use_llm_formula_cleanup"), False)
        try:
            llm_formula_min_confidence = float(extra_metadata.get("llm_formula_min_confidence", 0.8))
        except (TypeError, ValueError):
            llm_formula_min_confidence = 0.8
        extra_metadata["use_formula_cleanup"] = formula_cleanup_enabled
        extra_metadata["formula_cleanup_level"] = formula_cleanup_level_value
        extra_metadata["use_llm_formula_cleanup"] = llm_formula_cleanup_requested
        extra_metadata["llm_formula_min_confidence"] = llm_formula_min_confidence
        material_id = _generate_material_id()
        manifest_path: Path | None = None
        pipeline_logger = MaterialPipelineLogger(
            material_id=material_id,
            user_id=safe_user_id,
            source_name=file_path.name,
            progress_callback=progress_callback,
        )
        ingest_started = time.perf_counter()
        pipeline_logger.log(
            "ingest",
            "started",
            input_path=str(file_path),
            subject=subject,
            material_type=material_type,
            use_llm_cleanup=bool(use_llm_cleanup),
            use_formula_cleanup=formula_cleanup_enabled,
            formula_cleanup_level=formula_cleanup_level_value,
            use_llm_formula_cleanup=llm_formula_cleanup_requested,
        )

        try:
            stage_started = time.perf_counter()
            resolved_items = resolve_upload_path(file_path)
            item = resolved_items[0]
            pipeline_logger.log(
                "resolve_upload",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                resolved_count=len(resolved_items),
                is_supported=item.is_supported,
                error=item.error,
            )
            if not item.is_supported:
                error = item.error or "Unsupported file type"
                pipeline_logger.log("ingest", "failed", duration_ms=monotonic_ms(ingest_started), error=error)
                return self._failure_result(material_id, safe_user_id, error)

            stage_started = time.perf_counter()
            detected = detect_file(file_path)
            pipeline_logger.log(
                "detect_file",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                original_filename=detected.original_filename,
                file_ext=detected.file_ext,
                mime_type=detected.mime_type,
                size_bytes=detected.size_bytes,
                page_count=detected.page_count,
                sha256=detected.sha256,
            )
            pdf_route_decision = decide_pdf_route(detected, extra_metadata)
            extra_metadata["pdf_route_decision"] = pdf_route_decision.to_dict()
            pipeline_logger.log(
                "pdf_route_decision",
                "completed",
                selected_route=pdf_route_decision.selected_route,
                reason=pdf_route_decision.reason,
                mode=pdf_route_decision.mode,
                size_mb=round(pdf_route_decision.size_mb, 4),
                threshold_mb=pdf_route_decision.threshold_mb,
                page_count=pdf_route_decision.page_count,
                page_threshold=pdf_route_decision.page_threshold,
            )
            normalized_subject = self._normalize_subject(subject, detected.original_filename)
            normalized_material_type = self._normalize_material_type(material_type, detected.original_filename)

            stage_started = time.perf_counter()
            material_dir = self.storage.create_material_dir(safe_user_id, material_id, subject=normalized_subject)
            manifest_path = material_dir / "manifest.json"
            pipeline_log_path = material_dir / "parsed" / "pipeline_events.jsonl"
            pipeline_logger.bind_material_log(pipeline_log_path)
            pipeline_logger.log(
                "create_material_dir",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                material_dir=str(material_dir),
                pipeline_log=str(pipeline_log_path),
            )
            parser = None if pdf_route_decision.use_large_pdf_route else get_parser(detected.file_ext)
            parser_name = (
                ParserName.MINERU
                if pdf_route_decision.use_large_pdf_route
                else (
                    ParserName(parser.parser_name)
                    if parser and parser.parser_name in ParserName._value2member_map_
                    else ParserName.UNSUPPORTED
                )
            )

            manifest = MaterialManifest(
                material_id=material_id,
                user_id=safe_user_id,
                original_filename=detected.original_filename,
                file_ext=detected.file_ext,
                mime_type=detected.mime_type,
                sha256=detected.sha256,
                subject=normalized_subject,
                material_type=normalized_material_type,
                parser_name=parser_name,
                parse_status=ParseStatus.PROCESSING,
                paths={
                    "original": f"original/{detected.original_filename}",
                    "markdown": None,
                    "json": None,
                    "layout": None,
                    "layout_summary": None,
                    "tables": None,
                    "chunks": None,
                    "search_index": None,
                    "parse_report": None,
                    "format_probe": None,
                    "cleaning_strategy": None,
                    "document_zones": None,
                    "metadata_profile": None,
                    "zone_report": None,
                    "large_pdf_route_plan": None,
                    "large_pdf_sample_pages": None,
                    "large_pdf_chapter_plan": None,
                    "llm_cleaning_report": None,
                    "pipeline_log": _safe_relative(pipeline_log_path, material_dir),
                },
                metadata=extra_metadata.copy(),
            )
            stage_started = time.perf_counter()
            self.storage.save_manifest(safe_user_id, material_id, manifest)
            pipeline_logger.log(
                "save_manifest",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                phase="initial",
                manifest_path=str(manifest_path),
            )
            stage_started = time.perf_counter()
            self.storage.save_original(safe_user_id, material_id, file_path)
            pipeline_logger.log(
                "save_original",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                target=manifest.paths["original"],
            )

            large_pdf_layout_context: dict[str, Any] | None = None
            if pdf_route_decision.use_large_pdf_route:
                stage_started = time.perf_counter()
                plan_path = write_large_pdf_route_plan(material_dir, detected, pdf_route_decision)
                manifest.paths["large_pdf_route_plan"] = _safe_relative(plan_path, material_dir)
                parser = get_parser(detected.file_ext)
                large_pdf_result = run_large_pdf_split_pipeline(
                    source_pdf=file_path,
                    material_dir=material_dir,
                    parser=parser,
                    source_name=detected.original_filename,
                    use_llm_cleanup=use_llm_cleanup,
                    user_hints={
                        "subject": manifest.subject.value,
                        "material_type": manifest.material_type.value,
                    },
                )
                parse_result = large_pdf_result.parse_result
                large_pdf_layout_context = large_pdf_result.layout_context
                if large_pdf_result.sample_pages_path:
                    manifest.paths["large_pdf_sample_pages"] = _safe_relative(large_pdf_result.sample_pages_path, material_dir)
                if large_pdf_result.chapter_plan_path:
                    manifest.paths["large_pdf_chapter_plan"] = _safe_relative(large_pdf_result.chapter_plan_path, material_dir)
                extra_metadata.update(large_pdf_result.metadata)
                route_payload = json.loads(plan_path.read_text(encoding="utf-8"))
                route_payload["status"] = "samples_and_chapters_ready"
                route_payload["outputs"] = {
                    "sample_pages": manifest.paths.get("large_pdf_sample_pages"),
                    "chapter_plan": manifest.paths.get("large_pdf_chapter_plan"),
                    "sample_strategy_artifacts": {
                        key: _safe_relative(path, material_dir)
                        for key, path in large_pdf_result.sample_artifacts.items()
                    },
                }
                plan_path.write_text(json.dumps(route_payload, ensure_ascii=False, indent=2), encoding="utf-8")
                pipeline_logger.log(
                    "large_pdf_route",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    route_plan=manifest.paths["large_pdf_route_plan"],
                    sample_pages=manifest.paths.get("large_pdf_sample_pages"),
                    chapter_plan=manifest.paths.get("large_pdf_chapter_plan"),
                    reason=pdf_route_decision.reason,
                    warnings=large_pdf_result.warnings,
                )
            else:
                stage_started = time.perf_counter()
                if parser is None:
                    parser = get_parser(detected.file_ext)
                pipeline_logger.log("parse", "started", parser_name=parser.parser_name)
                parse_result = parser.parse(
                    input_path=file_path,
                    output_dir=material_dir / "parsed",
                    context={"user_id": safe_user_id, "material_id": material_id},
                )
                pipeline_logger.log(
                    "parse",
                    "completed" if parse_result.status == ParseStatus.READY else "failed",
                    duration_ms=monotonic_ms(stage_started),
                    parser_name=parser.parser_name,
                    parse_status=parse_result.status.value if isinstance(parse_result.status, ParseStatus) else parse_result.status,
                    markdown_path=str(parse_result.markdown_path) if parse_result.markdown_path else None,
                    json_path=str(parse_result.json_path) if parse_result.json_path else None,
                    layout_path=str(parse_result.layout_path) if parse_result.layout_path else None,
                    warnings=parse_result.warnings,
                    error=parse_result.error,
                    metadata_summary={
                        "line_count": parse_result.metadata.get("line_count"),
                        "char_count": parse_result.metadata.get("char_count"),
                        "heading_count": parse_result.metadata.get("heading_count"),
                        "image_ref_count": parse_result.metadata.get("image_ref_count"),
                        "source_format": parse_result.metadata.get("source_format"),
                    },
                )
            extra_metadata.update(parse_result.metadata)

            if parse_result.status != ParseStatus.READY or not parse_result.markdown_path:
                raise RuntimeError(parse_result.error or "Failed to parse material")

            markdown_path = parse_result.markdown_path
            manifest.paths["markdown"] = _safe_relative(markdown_path, material_dir)

            if parse_result.json_path:
                manifest.paths["json"] = _safe_relative(parse_result.json_path, material_dir)
            if parse_result.layout_path:
                manifest.paths["layout"] = _safe_relative(parse_result.layout_path, material_dir)

            # postprocess：所有 parser 统一进入这条 Markdown 清洗整理链路。
            postprocess_warnings: list[str] = []
            stage_started = time.perf_counter()
            markdown_text = markdown_path.read_text(encoding="utf-8")
            original_markdown_chars = len(markdown_text)
            formula_cleaning_report: dict[str, Any] = {
                "enabled": False,
                "level": formula_cleanup_level_value,
                "stats": {
                    "level": formula_cleanup_level_value,
                    "changed_count": 0,
                    "reported_count": 0,
                    "rules": {},
                },
                "changes": [],
                "warnings": [],
            }
            if formula_cleanup_enabled:
                formula_result = clean_formulas_with_report(
                    markdown_text,
                    level=formula_cleanup_level_value,
                )
                markdown_text = formula_result.cleaned_markdown
                formula_cleaning_report = formula_result.to_dict()
                postprocess_warnings.extend(formula_result.warnings)
                pipeline_logger.log(
                    "formula_clean",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    input_chars=original_markdown_chars,
                    output_chars=len(markdown_text),
                    changed_count=formula_result.stats.get("changed_count", 0),
                    reported_count=formula_result.stats.get("reported_count", 0),
                    rules=formula_result.stats.get("rules", {}),
                    warnings=formula_result.warnings,
                )
            else:
                pipeline_logger.log(
                    "formula_clean",
                    "skipped",
                    duration_ms=monotonic_ms(stage_started),
                    input_chars=original_markdown_chars,
                    output_chars=len(markdown_text),
                    reason="disabled",
                )
            extra_metadata["formula_cleaning"] = formula_cleaning_report

            source_dir_raw = parse_result.metadata.get("source_dir")
            source_dir = Path(source_dir_raw) if source_dir_raw else file_path.parent
            layout_context: dict[str, Any] | None = None
            layout_path = Path(parse_result.layout_path) if parse_result.layout_path else source_dir / "layout.json"
            if large_pdf_layout_context:
                stage_started = time.perf_counter()
                layout_context = large_pdf_layout_context
                layout_artifacts = save_layout_artifacts(material_dir / "parsed", layout_context)
                manifest.paths["layout_summary"] = _safe_relative(layout_artifacts["summary_path"], material_dir)
                manifest.paths["tables"] = _safe_relative(layout_artifacts["tables_dir"], material_dir)
                layout_summary = layout_context.get("summary", {})
                extra_metadata["layout_sidecar"] = {
                    "source": layout_summary.get("source", "large_pdf_chapter_layouts"),
                    "layout_path": None,
                    "table_count": len(layout_context.get("tables", [])),
                    "block_counts": layout_summary.get("block_counts", {}),
                }
                pipeline_logger.log(
                    "layout_sidecar",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    layout_path=None,
                    source=layout_summary.get("source", "large_pdf_chapter_layouts"),
                    table_count=len(layout_context.get("tables", [])),
                    block_counts=layout_summary.get("block_counts", {}),
                    layout_summary_path=manifest.paths["layout_summary"],
                    tables_path=manifest.paths["tables"],
                )
            elif layout_path.exists() and layout_path.is_file():
                stage_started = time.perf_counter()
                try:
                    layout_context = build_layout_context(layout_path)
                    layout_artifacts = save_layout_artifacts(material_dir / "parsed", layout_context)
                    manifest.paths["layout_summary"] = _safe_relative(layout_artifacts["summary_path"], material_dir)
                    manifest.paths["tables"] = _safe_relative(layout_artifacts["tables_dir"], material_dir)
                    extra_metadata["layout_sidecar"] = {
                        "source": "mineru_layout",
                        "layout_path": str(layout_path),
                        "table_count": len(layout_context.get("tables", [])),
                        "block_counts": layout_context.get("summary", {}).get("block_counts", {}),
                    }
                    pipeline_logger.log(
                        "layout_sidecar",
                        "completed",
                        duration_ms=monotonic_ms(stage_started),
                        layout_path=str(layout_path),
                        table_count=len(layout_context.get("tables", [])),
                        block_counts=layout_context.get("summary", {}).get("block_counts", {}),
                        layout_summary_path=manifest.paths["layout_summary"],
                        tables_path=manifest.paths["tables"],
                    )
                except Exception as exc:
                    postprocess_warnings.append(f"layout_sidecar_unavailable:{exc.__class__.__name__}")
                    pipeline_logger.log(
                        "layout_sidecar",
                        "failed",
                        duration_ms=monotonic_ms(stage_started),
                        layout_path=str(layout_path),
                        error_type=exc.__class__.__name__,
                        error_message=str(exc),
                    )
                    layout_context = None
            else:
                pipeline_logger.log("layout_sidecar", "skipped", layout_path=str(layout_path))
            stage_started = time.perf_counter()
            markdown_text, saved_images = save_and_rewrite_images(
                markdown_text,
                source_dir,
                material_dir / "assets" / "images",
            )
            pipeline_logger.log(
                "asset_rewrite",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                source_dir=str(source_dir),
                saved_image_count=len(saved_images),
                output_chars=len(markdown_text),
            )

            stage_started = time.perf_counter()
            pipeline_logger.log("raw_markdown_cleaning", "started")
            cleaning_user_hints: dict[str, Any] = {
                "subject": manifest.subject.value,
                "material_type": manifest.material_type.value,
            }
            for override_key in (
                "cleaning_strategy_override",
                "document_zones_override",
                "metadata_profile_override",
            ):
                if override_key in extra_metadata:
                    cleaning_user_hints[override_key] = extra_metadata[override_key]
            clean_result = clean_raw_markdown(
                markdown_text,
                source_name=detected.original_filename,
                use_llm_profile=use_llm_cleanup,
                user_hints=cleaning_user_hints,
                layout_summary=layout_context.get("summary") if layout_context else None,
            )
            pipeline_logger.log(
                "raw_markdown_cleaning",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                strategy_source=clean_result.strategy.get("strategy_source"),
                cleaned_chars=len(clean_result.cleaned_markdown),
                warnings=clean_result.warnings,
                stats=clean_result.parse_report.get("stats", {}),
                qwen_usage=clean_result.parse_report.get("qwen_usage"),
                qwen_zone_usage=clean_result.parse_report.get("qwen_zone_usage"),
                metadata_profile=clean_result.metadata_profile,
                strategy_validation=clean_result.parse_report.get("strategy_validation"),
                zone_report=clean_result.zone_report,
            )
            markdown_text = clean_result.cleaned_markdown
            if extra_metadata.get("large_pdf_split"):
                markdown_text = restore_large_pdf_chapter_headings(markdown_text)

            stage_started = time.perf_counter()
            final_subject, final_material_type, metadata_selection, metadata_error = self._resolve_metadata_selection(
                selected_subject=subject,
                selected_material_type=material_type,
                current_subject=manifest.subject,
                current_material_type=manifest.material_type,
                metadata_profile=clean_result.metadata_profile,
                allow_metadata_mismatch=bool(extra_metadata.get("allow_metadata_mismatch")),
                use_llm_cleanup=bool(use_llm_cleanup and not extra_metadata.get("large_pdf_split")),
            )
            if metadata_error is not None:
                pipeline_logger.log(
                    "metadata_classify",
                    "failed",
                    duration_ms=monotonic_ms(stage_started),
                    error=metadata_error,
                    metadata_selection=metadata_selection,
                )
                manifest.parse_status = ParseStatus.FAILED
                manifest.quality_status = "failed"
                manifest.error = metadata_error
                manifest.metadata = {**extra_metadata, "metadata_profile": clean_result.metadata_profile}
                if metadata_selection:
                    manifest.metadata[metadata_error] = metadata_selection
                self.storage.save_manifest(safe_user_id, material_id, manifest)
                try:
                    self.storage.delete_material(safe_user_id, material_id)
                except FileNotFoundError:
                    pass
                return self._failure_result(
                    material_id,
                    safe_user_id,
                    metadata_error,
                    manifest_path,
                    metadata={
                        metadata_error: metadata_selection or {},
                        "metadata_profile": clean_result.metadata_profile,
                        "metadata_retry_overrides": {
                            "cleaning_strategy": clean_result.strategy,
                            "document_zones": clean_result.document_zones,
                            "metadata_profile": clean_result.metadata_profile,
                        },
                    },
                )

            if metadata_selection:
                extra_metadata["metadata_profile"] = metadata_selection["metadata_profile"]
                if metadata_selection.get("metadata_conflict"):
                    extra_metadata["metadata_conflict"] = metadata_selection["metadata_conflict"]

            if final_subject is not None and final_material_type is not None:
                previous_subject = manifest.subject
                manifest.subject = final_subject
                manifest.material_type = final_material_type
                if final_subject != previous_subject:
                    old_material_dir = material_dir
                    material_dir = self.storage.move_material_to_subject(safe_user_id, material_id, final_subject)
                    manifest_path = material_dir / "manifest.json"
                    pipeline_log_path = material_dir / "parsed" / "pipeline_events.jsonl"
                    pipeline_logger.bind_material_log(pipeline_log_path)
                    markdown_path = material_dir / (manifest.paths["markdown"] or "parsed/content.md")
                    extra_metadata["metadata_directory_move"] = {
                        "from": str(old_material_dir),
                        "to": str(material_dir),
                        "subject": final_subject.value,
                    }

            pipeline_logger.log(
                "metadata_classify",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                selected_subject=subject,
                selected_material_type=material_type,
                final_subject=manifest.subject.value,
                final_material_type=manifest.material_type.value,
                metadata_profile=clean_result.metadata_profile,
                metadata_conflict=extra_metadata.get("metadata_conflict"),
            )

            if layout_context and not extra_metadata.get("large_pdf_tables_replaced"):
                stage_started = time.perf_counter()
                markdown_text, table_warnings = replace_html_tables_with_layout_markdown(
                    markdown_text,
                    list(layout_context.get("tables", [])),
                )
                postprocess_warnings.extend(table_warnings)
                pipeline_logger.log(
                    "table_markdown_replace",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    table_count=len(layout_context.get("tables", [])),
                    warnings=table_warnings,
                    output_chars=len(markdown_text),
                )
            elif layout_context:
                pipeline_logger.log(
                    "table_markdown_replace",
                    "skipped",
                    reason="large_pdf_tables_already_replaced",
                    table_count=len(layout_context.get("tables", [])),
                )
            postprocess_warnings.extend(clean_result.warnings)
            extra_metadata["raw_markdown_cleaning"] = {
                "strategy_source": clean_result.strategy.get("strategy_source"),
                "converted_headings": clean_result.parse_report.get("stats", {}).get("converted_headings", 0),
                "warnings": clean_result.warnings,
            }

            llm_cleaning_report: dict[str, Any] = {
                "requested": llm_formula_cleanup_requested,
                "enabled": False,
                "report": {
                    "formula_repair": {
                        "candidate_count": 0,
                        "applied_count": 0,
                        "skipped_count": 0,
                        "skipped": [],
                        "applied": [],
                    },
                    "heading_review": {
                        "enabled": False,
                        "context": {
                            "heading_tree": [],
                            "heading_events": [],
                            "heading_count": 0,
                        },
                    },
                },
                "patches": [],
                "warnings": [],
            }
            stage_started = time.perf_counter()
            if llm_formula_cleanup_requested:
                formula_repair_client = build_qwen_formula_repair_client_from_env()
                llm_result = clean_markdown_with_llm_patches(
                    markdown_text,
                    formula_repair_client=formula_repair_client,
                    heading_review_client=formula_repair_client,
                    min_confidence=llm_formula_min_confidence,
                )
                markdown_text = llm_result.cleaned_markdown
                llm_cleaning_report = {
                    "requested": True,
                    **llm_result.to_dict(),
                }
                postprocess_warnings.extend(llm_result.warnings)
                pipeline_logger.log(
                    "llm_clean",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    requested=True,
                    enabled=llm_cleaning_report.get("enabled", False),
                    formula_candidates=llm_result.report.get("formula_repair", {}).get("candidate_count", 0),
                    applied_count=llm_result.report.get("formula_repair", {}).get("applied_count", 0),
                    skipped_count=llm_result.report.get("formula_repair", {}).get("skipped_count", 0),
                    warnings=llm_result.warnings,
                )
            else:
                pipeline_logger.log(
                    "llm_clean",
                    "skipped",
                    duration_ms=monotonic_ms(stage_started),
                    requested=False,
                    reason="disabled",
                )
            extra_metadata["llm_cleaning"] = llm_cleaning_report

            stage_started = time.perf_counter()
            markdown_path.write_text(markdown_text, encoding="utf-8")
            parsed_dir = material_dir / "parsed"
            format_probe_path = parsed_dir / "format_probe.json"
            cleaning_strategy_path = parsed_dir / "cleaning_strategy.json"
            document_zones_path = parsed_dir / "document_zones.json"
            metadata_profile_path = parsed_dir / "metadata_profile.json"
            zone_report_path = parsed_dir / "zone_report.json"
            llm_cleaning_report_path = parsed_dir / "llm_cleaning_report.json"
            format_probe_path.write_text(
                json.dumps(clean_result.format_probe, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            cleaning_strategy_path.write_text(
                json.dumps(clean_result.strategy, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            document_zones_path.write_text(
                json.dumps(clean_result.document_zones, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            metadata_profile_path.write_text(
                json.dumps(clean_result.metadata_profile, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            zone_report_path.write_text(
                json.dumps(clean_result.zone_report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            llm_cleaning_report_path.write_text(
                json.dumps(llm_cleaning_report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            manifest.paths["format_probe"] = _safe_relative(format_probe_path, material_dir)
            manifest.paths["cleaning_strategy"] = _safe_relative(cleaning_strategy_path, material_dir)
            manifest.paths["document_zones"] = _safe_relative(document_zones_path, material_dir)
            manifest.paths["metadata_profile"] = _safe_relative(metadata_profile_path, material_dir)
            manifest.paths["zone_report"] = _safe_relative(zone_report_path, material_dir)
            manifest.paths["llm_cleaning_report"] = _safe_relative(llm_cleaning_report_path, material_dir)
            pipeline_logger.log(
                "write_clean_artifacts",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                markdown_path=manifest.paths["markdown"],
                format_probe_path=manifest.paths["format_probe"],
                cleaning_strategy_path=manifest.paths["cleaning_strategy"],
                document_zones_path=manifest.paths["document_zones"],
                metadata_profile_path=manifest.paths["metadata_profile"],
                zone_report_path=manifest.paths["zone_report"],
                llm_cleaning_report_path=manifest.paths["llm_cleaning_report"],
                markdown_chars=len(markdown_text),
            )

            stage_started = time.perf_counter()
            title = extract_title_from_markdown(markdown_text)
            if title:
                extra_metadata.setdefault("title", title)
            if manifest.subject == Subject.UNKNOWN:
                manifest.subject = infer_subject_from_markdown(markdown_text)
            if manifest.material_type == MaterialType.UNKNOWN:
                manifest.material_type = infer_material_type_from_markdown(markdown_text)
            if manifest.material_type == MaterialType.UNKNOWN:
                manifest.material_type = MaterialType.LECTURE
            structure_profile = infer_material_structure_profile(
                manifest.original_filename,
                markdown_text,
                manifest.material_type,
            )
            if structure_profile:
                extra_metadata["structure_profile"] = structure_profile
            pipeline_logger.log(
                "metadata_infer",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                title=extra_metadata.get("title"),
                subject=manifest.subject.value,
                material_type=manifest.material_type.value,
                structure_profile=structure_profile,
            )

            exercise_structure_report: dict[str, Any] | None = None
            exercise_structure_repair_report: dict[str, Any] | None = None
            problem_groups: list[dict[str, Any]] | None = None
            if manifest.material_type == MaterialType.EXERCISE:
                stage_started = time.perf_counter()
                exercise_structure_report = analyze_exercise_structure(
                    markdown_text,
                    material_type=manifest.material_type.value,
                )
                problem_groups = list(exercise_structure_report.get("problem_groups") or [])
                extra_metadata["exercise_structure"] = {
                    key: value
                    for key, value in exercise_structure_report.items()
                    if key != "problem_groups"
                }
                pipeline_logger.log(
                    "exercise_structure",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    exercise_structure_status=exercise_structure_report.get("status"),
                    problem_count=exercise_structure_report.get("problem_count"),
                    solution_label_count=exercise_structure_report.get("solution_label_count"),
                    warning_count=len(exercise_structure_report.get("warnings") or []),
                )
                stage_started = time.perf_counter()
                has_repair_candidates = bool(
                    exercise_structure_report.get("missing_problem_indices")
                    or exercise_structure_report.get("sequence_gap_candidates")
                    or exercise_structure_report.get("tail_problem_candidate")
                )
                repair_client = (
                    build_deepseek_structure_repair_client_from_env()
                    if has_repair_candidates
                    else None
                )
                repair_result = repair_exercise_structure(
                    markdown_text,
                    exercise_structure_report,
                    llm_client=repair_client,
                )
                problem_groups = list(repair_result.get("problem_groups") or problem_groups or [])
                exercise_structure_repair_report = dict(repair_result.get("report") or {})
                exercise_structure_report = _refresh_exercise_structure_summary(
                    exercise_structure_report,
                    problem_groups,
                    exercise_structure_repair_report,
                )
                extra_metadata["exercise_structure"] = {
                    key: value
                    for key, value in exercise_structure_report.items()
                    if key != "problem_groups"
                }
                extra_metadata["exercise_structure_repair"] = exercise_structure_repair_report
                repair_report_path = parsed_dir / "exercise_structure_repair.json"
                repair_report_path.write_text(
                    json.dumps(exercise_structure_repair_report, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                manifest.paths["exercise_structure_repair"] = _safe_relative(repair_report_path, material_dir)
                pipeline_logger.log(
                    "exercise_structure_repair",
                    "completed",
                    duration_ms=monotonic_ms(stage_started),
                    enabled=exercise_structure_repair_report.get("enabled"),
                    model=exercise_structure_repair_report.get("model"),
                    candidate_count=exercise_structure_repair_report.get("candidate_count"),
                    applied_count=exercise_structure_repair_report.get("applied_count"),
                    skipped_count=exercise_structure_repair_report.get("skipped_count"),
                    warnings=exercise_structure_repair_report.get("warnings"),
                )

            stage_started = time.perf_counter()
            pipeline_logger.log("chunk", "started")
            chunks = chunk_markdown_file(
                markdown_path,
                material_id,
                safe_user_id,
                document_zones=clean_result.document_zones,
                problem_groups=problem_groups,
            )
            text_chunk_count = len(chunks)
            if layout_context:
                chunks.extend(
                    build_table_chunks(
                        list(layout_context.get("tables", [])),
                        material_id=material_id,
                        user_id=safe_user_id,
                        start_index=len(chunks),
                    )
                )
            pipeline_logger.log(
                "chunk",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                text_chunk_count=text_chunk_count,
                table_chunk_count=len(chunks) - text_chunk_count,
                total_chunk_count=len(chunks),
                unique_heading_path_count=len({tuple(chunk.heading_path) for chunk in chunks if chunk.heading_path}),
            )
            for chunk in chunks:
                chunk.metadata = {
                    **chunk.metadata,
                    "subject": manifest.subject.value,
                    "material_type": manifest.material_type.value,
                    "original_filename": manifest.original_filename,
                    "title": extra_metadata.get("title"),
                    "source_format": extra_metadata.get("source_format"),
                }

            stage_started = time.perf_counter()
            chunks_path = self.storage.save_chunks_jsonl(safe_user_id, material_id, chunks)
            self.storage.save_chunks_debug(safe_user_id, material_id, chunks)
            pipeline_logger.log(
                "save_chunks",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                chunks_path=_safe_relative(chunks_path, material_dir),
                chunk_count=len(chunks),
            )
            stage_started = time.perf_counter()
            pipeline_logger.log("index", "started")
            index_path = self.storage.save_search_index(
                safe_user_id,
                material_id,
                build_search_index(chunks),
            )
            pipeline_logger.log(
                "index",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                index_path=_safe_relative(index_path, material_dir),
                chunk_count=len(chunks),
            )

            stage_started = time.perf_counter()
            pipeline_logger.log("vector_index", "started")
            vector_index_result = build_material_vector_index(
                chunks,
                manifest,
                enabled=enable_vector_index,
            )
            extra_metadata["vector_index"] = vector_index_result.to_dict()
            pipeline_logger.log(
                "vector_index",
                vector_index_result.status,
                duration_ms=monotonic_ms(stage_started),
                enabled=vector_index_result.enabled,
                provider=vector_index_result.provider,
                collection=vector_index_result.collection,
                model=vector_index_result.model,
                dimension=vector_index_result.dimension,
                chunk_count=vector_index_result.chunk_count,
                warnings=vector_index_result.warnings,
                error=vector_index_result.error,
                usage=vector_index_result.usage,
            )

            stage_started = time.perf_counter()
            parse_report = build_quality_report(
                markdown_text,
                material_dir=material_dir,
                chunks=chunks,
                parser_warnings=parse_result.warnings,
                postprocess_warnings=postprocess_warnings,
            )
            parse_report.metrics["formula_cleaning"] = formula_cleaning_report
            parse_report.metrics["llm_cleaning"] = llm_cleaning_report
            parse_report.metrics["raw_markdown_cleaning"] = clean_result.parse_report
            if exercise_structure_report is not None:
                parse_report.metrics["exercise_structure"] = exercise_structure_report
                parse_report.warnings = sorted(
                    set(parse_report.warnings + list(exercise_structure_report.get("warnings") or []))
                )
            if exercise_structure_repair_report is not None:
                parse_report.metrics["exercise_structure_repair"] = exercise_structure_repair_report
                parse_report.warnings = sorted(
                    set(parse_report.warnings + list(exercise_structure_repair_report.get("warnings") or []))
                )
            if layout_context:
                parse_report.metrics["layout_sidecar"] = {
                    "source": layout_context.get("summary", {}).get("source", "mineru_layout"),
                    "table_count": len(layout_context.get("tables", [])),
                    "structured_table_rows": sum(
                        int(table.get("row_count", 0)) for table in layout_context.get("tables", [])
                    ),
                    "block_counts": layout_context.get("summary", {}).get("block_counts", {}),
                }
            parse_report.warnings = sorted(set(parse_report.warnings + clean_result.warnings))
            parse_report_path = save_quality_report(parse_report, material_dir / "parsed" / "parse_report.json")
            pipeline_logger.log(
                "quality_report",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                parse_report_path=_safe_relative(parse_report_path, material_dir),
                quality_status=parse_report.quality_status.value,
                overall_confidence=parse_report.overall_confidence,
                warnings=parse_report.warnings,
                metrics_summary={
                    "assets": parse_report.metrics.get("assets"),
                    "chunks": parse_report.metrics.get("chunks"),
                    "layout_sidecar": parse_report.metrics.get("layout_sidecar"),
                },
            )

            manifest.paths["chunks"] = _safe_relative(chunks_path, material_dir)
            manifest.paths["search_index"] = _safe_relative(index_path, material_dir)
            manifest.paths["parse_report"] = _safe_relative(parse_report_path, material_dir)
            manifest.chunk_count = len(chunks)
            manifest.asset_count = len(saved_images)
            manifest.parse_status = ParseStatus.READY
            manifest.quality_status = parse_report.quality_status.value
            manifest.overall_confidence = parse_report.overall_confidence
            manifest.warnings = parse_report.warnings
            manifest.metadata = extra_metadata
            manifest.error = None
            stage_started = time.perf_counter()
            self.storage.save_manifest(safe_user_id, material_id, manifest)
            pipeline_logger.log(
                "save_manifest",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                phase="final",
                manifest_path=str(manifest_path),
            )
            pipeline_logger.log(
                "ingest",
                "completed",
                duration_ms=monotonic_ms(ingest_started),
                parse_status=ParseStatus.READY.value,
                chunk_count=len(chunks),
                asset_count=len(saved_images),
                quality_status=parse_report.quality_status.value,
                overall_confidence=parse_report.overall_confidence,
                warnings=parse_report.warnings,
            )

            return MaterialIngestionResult(
                material_id=material_id,
                user_id=safe_user_id,
                parse_status=ParseStatus.READY,
                manifest_path=str(manifest_path),
                markdown_path=str(markdown_path),
                parse_report_path=str(parse_report_path),
                chunk_count=len(chunks),
                asset_count=len(saved_images),
                quality_status=parse_report.quality_status.value,
                overall_confidence=parse_report.overall_confidence,
                warnings=parse_report.warnings,
                metadata=extra_metadata,
            )
        except Exception as exc:
            pipeline_logger.log(
                "ingest",
                "failed",
                duration_ms=monotonic_ms(ingest_started),
                error_type=exc.__class__.__name__,
                error_message=str(exc),
            )
            if manifest_path and manifest_path.parent.exists():
                existing_manifest = self.storage.load_manifest(safe_user_id, material_id)
                if existing_manifest is None and file_path.exists():
                    detected = detect_file(file_path)
                    existing_manifest = MaterialManifest(
                        material_id=material_id,
                        user_id=safe_user_id,
                        original_filename=detected.original_filename,
                        file_ext=detected.file_ext,
                        mime_type=detected.mime_type,
                        sha256=detected.sha256,
                    )
                if existing_manifest is not None:
                    existing_manifest.parse_status = ParseStatus.FAILED
                    existing_manifest.quality_status = "failed"
                    existing_manifest.error = str(exc)
                    self.storage.save_manifest(safe_user_id, material_id, existing_manifest)

            return self._failure_result(material_id, safe_user_id, str(exc), manifest_path)

    def list_materials(
        self,
        user_id: str = "tester",
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        filters = filters or {}
        manifests = self.storage.list_user_manifests(safe_user_id)
        items: list[dict[str, Any]] = []

        for manifest in manifests:
            if filters.get("subject") and manifest.subject.value != filters["subject"]:
                continue
            if filters.get("material_type") and manifest.material_type.value != filters["material_type"]:
                continue

            items.append(
                {
                    "material_id": manifest.material_id,
                    "user_id": manifest.user_id,
                    "original_filename": manifest.original_filename,
                    "subject": manifest.subject.value,
                    "material_type": manifest.material_type.value,
                    "parse_status": manifest.parse_status.value,
                    "quality_status": manifest.quality_status,
                    "overall_confidence": manifest.overall_confidence,
                    "chunk_count": manifest.chunk_count,
                    "asset_count": manifest.asset_count,
                    "created_at": manifest.created_at,
                    "updated_at": manifest.updated_at,
                    "error": manifest.error,
                    "warnings": manifest.warnings,
                }
            )

        return items

    def delete_material(self, user_id: str, material_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_material_id = resolve_material_id(material_id)
        vector_delete = delete_material_vector_index(safe_user_id, safe_material_id, enabled=True)
        if vector_delete.status == "failed":
            raise RuntimeError(f"Failed to delete material vector index: {vector_delete.error or 'unknown error'}")
        self.storage.delete_material(safe_user_id, safe_material_id)
        return {
            "ok": True,
            "deleted": True,
            "user_id": safe_user_id,
            "material_id": safe_material_id,
            "vector_index": vector_delete.to_dict(),
        }
