from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from .chunking.chunker import chunk_markdown_file
from .detector import detect_file
from .indexing.material_indexer import build_search_index
from .postprocess.asset_rewriter import save_and_rewrite_images
from .postprocess.formula_cleaner import clean_formulas
from .postprocess.metadata_extractor import (
    extract_title_from_markdown,
    infer_material_type_from_markdown,
    infer_subject_from_markdown,
    guess_material_type_from_filename,
    guess_subject_from_filename,
)
from .postprocess.raw_markdown_cleaner import clean_raw_markdown
from .quality.report import build_quality_report, save_quality_report
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

        try:
            resolved_items = resolve_upload_path(file_path)
            item = resolved_items[0]
            if not item.is_supported:
                return self._failure_result(material_id, safe_user_id, item.error or "Unsupported file type")

            detected = detect_file(file_path)
            material_dir = self.storage.create_material_dir(safe_user_id, material_id)
            manifest_path = material_dir / "manifest.json"
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
                    "chunks": None,
                    "search_index": None,
                    "parse_report": None,
                    "format_probe": None,
                    "cleaning_strategy": None,
                },
                metadata=extra_metadata.copy(),
            )
            self.storage.save_manifest(safe_user_id, material_id, manifest)
            self.storage.save_original(safe_user_id, material_id, file_path)

            parse_result = parser.parse(
                input_path=file_path,
                output_dir=material_dir / "parsed",
                context={"user_id": safe_user_id, "material_id": material_id},
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
            markdown_text = markdown_path.read_text(encoding="utf-8")
            markdown_text = clean_formulas(markdown_text)

            source_dir_raw = parse_result.metadata.get("source_dir")
            source_dir = Path(source_dir_raw) if source_dir_raw else file_path.parent
            markdown_text, saved_images = save_and_rewrite_images(
                markdown_text,
                source_dir,
                material_dir / "assets" / "images",
            )

            clean_result = clean_raw_markdown(
                markdown_text,
                source_name=detected.original_filename,
                use_llm_profile=use_llm_cleanup,
                user_hints={
                    "subject": manifest.subject.value,
                    "material_type": manifest.material_type.value,
                },
            )
            markdown_text = clean_result.cleaned_markdown
            postprocess_warnings.extend(clean_result.warnings)
            extra_metadata["raw_markdown_cleaning"] = {
                "strategy_source": clean_result.strategy.get("strategy_source"),
                "converted_headings": clean_result.parse_report.get("stats", {}).get("converted_headings", 0),
                "warnings": clean_result.warnings,
            }

            markdown_path.write_text(markdown_text, encoding="utf-8")
            parsed_dir = material_dir / "parsed"
            format_probe_path = parsed_dir / "format_probe.json"
            cleaning_strategy_path = parsed_dir / "cleaning_strategy.json"
            format_probe_path.write_text(
                json.dumps(clean_result.format_probe, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            cleaning_strategy_path.write_text(
                json.dumps(clean_result.strategy, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            manifest.paths["format_probe"] = _safe_relative(format_probe_path, material_dir)
            manifest.paths["cleaning_strategy"] = _safe_relative(cleaning_strategy_path, material_dir)

            title = extract_title_from_markdown(markdown_text)
            if title:
                extra_metadata.setdefault("title", title)
            if manifest.subject == Subject.UNKNOWN:
                manifest.subject = infer_subject_from_markdown(markdown_text)
            if manifest.material_type == MaterialType.UNKNOWN:
                manifest.material_type = infer_material_type_from_markdown(markdown_text)

            chunks = chunk_markdown_file(
                markdown_path,
                material_id,
                safe_user_id,
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

            chunks_path = self.storage.save_chunks_jsonl(safe_user_id, material_id, chunks)
            self.storage.save_chunks_debug(safe_user_id, material_id, chunks)
            index_path = self.storage.save_search_index(
                safe_user_id,
                material_id,
                build_search_index(chunks),
            )

            parse_report = build_quality_report(
                markdown_text,
                material_dir=material_dir,
                chunks=chunks,
                parser_warnings=parse_result.warnings,
                postprocess_warnings=postprocess_warnings,
            )
            parse_report.metrics["raw_markdown_cleaning"] = clean_result.parse_report
            parse_report.warnings = sorted(set(parse_report.warnings + clean_result.warnings))
            parse_report_path = save_quality_report(parse_report, material_dir / "parsed" / "parse_report.json")

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
            self.storage.save_manifest(safe_user_id, material_id, manifest)

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
