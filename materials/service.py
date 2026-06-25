from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from .chunking.chunker import chunk_markdown_file
from .detector import detect_file
from .indexing.material_indexer import build_search_index
from .postprocess.asset_rewriter import save_and_rewrite_images
from .postprocess.formula_cleaner import clean_formulas
from .postprocess.layout_sidecar import (
    build_layout_context,
    build_table_chunks,
    replace_html_tables_with_layout_markdown,
    save_layout_artifacts,
)
from .postprocess.metadata_extractor import (
    extract_title_from_markdown,
    infer_material_type_from_markdown,
    infer_subject_from_markdown,
    guess_material_type_from_filename,
    guess_subject_from_filename,
)
from .postprocess.raw_markdown_cleaner import clean_raw_markdown
from .quality.report import build_quality_report, save_quality_report
from .pipeline_logger import MaterialPipelineLogger, monotonic_ms
from .resolver import resolve_upload_path
from .router import get_parser
from .schemas import (
    MaterialIngestionResult,
    MaterialManifest,
    MaterialType,
    ParseStatus,
    ParserName,
    Subject,
)
from .security import resolve_material_id, resolve_user_id
from .storage import MaterialStorage


def _generate_material_id() -> str:
    return f"mat_{uuid.uuid4().hex[:16]}"


def _safe_relative(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


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
        if subject and subject != "unknown":
            try:
                return Subject(subject)
            except ValueError:
                pass
        return guess_subject_from_filename(filename)

    @staticmethod
    def _normalize_material_type(material_type: str, filename: str) -> MaterialType:
        if material_type and material_type != "unknown":
            try:
                return MaterialType(material_type)
            except ValueError:
                pass
        return guess_material_type_from_filename(filename)

    @staticmethod
    def _failure_result(
        material_id: str,
        user_id: str,
        error: str,
        manifest_path: Path | None = None,
    ) -> MaterialIngestionResult:
        return MaterialIngestionResult(
            material_id=material_id,
            user_id=user_id,
            parse_status=ParseStatus.FAILED,
            manifest_path=str(manifest_path) if manifest_path else None,
            quality_status="failed",
            error=error,
        )

    def ingest_file(
        self,
        file_path: Path | str,
        user_id: str = "tester",
        subject: str = "unknown",
        material_type: str = "unknown",
        metadata: dict[str, Any] | None = None,
        use_llm_cleanup: bool = True,
    ) -> MaterialIngestionResult:
        """入库一个资料文件。

        use_llm_cleanup 表示是否允许 Qwen 读取 format_probe.json 生成 cleaning_strategy.json。
        即使启用，全文清洗仍由本地规则执行。
        """
        file_path = Path(file_path)
        safe_user_id = resolve_user_id(user_id)
        extra_metadata = dict(metadata or {})
        extra_metadata["use_llm_cleanup"] = bool(use_llm_cleanup)
        material_id = _generate_material_id()
        manifest_path: Path | None = None
        pipeline_logger = MaterialPipelineLogger(
            material_id=material_id,
            user_id=safe_user_id,
            source_name=file_path.name,
        )
        ingest_started = time.perf_counter()
        pipeline_logger.log(
            "ingest",
            "started",
            input_path=str(file_path),
            subject=subject,
            material_type=material_type,
            use_llm_cleanup=bool(use_llm_cleanup),
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
                sha256=detected.sha256,
            )
            stage_started = time.perf_counter()
            material_dir = self.storage.create_material_dir(safe_user_id, material_id)
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
            parser = get_parser(detected.file_ext)

            manifest = MaterialManifest(
                material_id=material_id,
                user_id=safe_user_id,
                original_filename=detected.original_filename,
                file_ext=detected.file_ext,
                mime_type=detected.mime_type,
                sha256=detected.sha256,
                subject=self._normalize_subject(subject, detected.original_filename),
                material_type=self._normalize_material_type(material_type, detected.original_filename),
                parser_name=(
                    ParserName(parser.parser_name)
                    if parser.parser_name in ParserName._value2member_map_
                    else ParserName.UNSUPPORTED
                ),
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
                    "zone_report": None,
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

            stage_started = time.perf_counter()
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
            markdown_text = clean_formulas(markdown_text)
            pipeline_logger.log(
                "formula_clean",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                input_chars=original_markdown_chars,
                output_chars=len(markdown_text),
            )

            source_dir_raw = parse_result.metadata.get("source_dir")
            source_dir = Path(source_dir_raw) if source_dir_raw else file_path.parent
            layout_context: dict[str, Any] | None = None
            layout_path = Path(parse_result.layout_path) if parse_result.layout_path else source_dir / "layout.json"
            if layout_path.exists() and layout_path.is_file():
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
            clean_result = clean_raw_markdown(
                markdown_text,
                source_name=detected.original_filename,
                use_llm_profile=use_llm_cleanup,
                user_hints={
                    "subject": manifest.subject.value,
                    "material_type": manifest.material_type.value,
                },
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
                strategy_validation=clean_result.parse_report.get("strategy_validation"),
                zone_report=clean_result.zone_report,
            )
            markdown_text = clean_result.cleaned_markdown
            if layout_context:
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
            postprocess_warnings.extend(clean_result.warnings)
            extra_metadata["raw_markdown_cleaning"] = {
                "strategy_source": clean_result.strategy.get("strategy_source"),
                "converted_headings": clean_result.parse_report.get("stats", {}).get("converted_headings", 0),
                "warnings": clean_result.warnings,
            }

            stage_started = time.perf_counter()
            markdown_path.write_text(markdown_text, encoding="utf-8")
            parsed_dir = material_dir / "parsed"
            format_probe_path = parsed_dir / "format_probe.json"
            cleaning_strategy_path = parsed_dir / "cleaning_strategy.json"
            document_zones_path = parsed_dir / "document_zones.json"
            zone_report_path = parsed_dir / "zone_report.json"
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
            zone_report_path.write_text(
                json.dumps(clean_result.zone_report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            manifest.paths["format_probe"] = _safe_relative(format_probe_path, material_dir)
            manifest.paths["cleaning_strategy"] = _safe_relative(cleaning_strategy_path, material_dir)
            manifest.paths["document_zones"] = _safe_relative(document_zones_path, material_dir)
            manifest.paths["zone_report"] = _safe_relative(zone_report_path, material_dir)
            pipeline_logger.log(
                "write_clean_artifacts",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                markdown_path=manifest.paths["markdown"],
                format_probe_path=manifest.paths["format_probe"],
                cleaning_strategy_path=manifest.paths["cleaning_strategy"],
                document_zones_path=manifest.paths["document_zones"],
                zone_report_path=manifest.paths["zone_report"],
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
            pipeline_logger.log(
                "metadata_infer",
                "completed",
                duration_ms=monotonic_ms(stage_started),
                title=extra_metadata.get("title"),
                subject=manifest.subject.value,
                material_type=manifest.material_type.value,
            )

            stage_started = time.perf_counter()
            chunks = chunk_markdown_file(
                markdown_path,
                material_id,
                safe_user_id,
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
            parse_report = build_quality_report(
                markdown_text,
                material_dir=material_dir,
                chunks=chunks,
                parser_warnings=parse_result.warnings,
                postprocess_warnings=postprocess_warnings,
            )
            parse_report.metrics["raw_markdown_cleaning"] = clean_result.parse_report
            if layout_context:
                parse_report.metrics["layout_sidecar"] = {
                    "source": "mineru_layout",
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
        self.storage.delete_material(safe_user_id, safe_material_id)
        return {
            "ok": True,
            "deleted": True,
            "user_id": safe_user_id,
            "material_id": safe_material_id,
        }
