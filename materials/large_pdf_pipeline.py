from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .large_pdf_chapters import (
    build_fixed_chunk_segments,
    combine_chapter_markdown,
    extract_outline_chapter_segments,
    split_pdf_by_segments,
)
from .large_pdf_samples import create_large_pdf_samples
from .postprocess.layout_sidecar import (
    build_layout_context,
    render_table_markdown,
    replace_html_tables_with_layout_markdown,
)
from .postprocess.raw_markdown_cleaner import clean_raw_markdown
from .schemas import ParseResult, ParseStatus


@dataclass
class LargePdfPipelineResult:
    parse_result: ParseResult
    sample_pages_path: Path | None = None
    chapter_plan_path: Path | None = None
    layout_context: dict[str, Any] | None = None
    sample_artifacts: dict[str, Path] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def _relative(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _sample_pdf_paths(sample_pages_path: Path) -> list[Path]:
    sample_dir = sample_pages_path.parent
    payload = _load_json(sample_pages_path)
    paths: list[Path] = []
    for window in payload.get("windows", []) or []:
        if not isinstance(window, dict):
            continue
        filename = window.get("filename")
        if filename:
            paths.append(sample_dir / str(filename))
    return paths


def _parse_pdf_parts(
    *,
    parser: Any,
    pdf_paths: list[Path],
    output_root: Path,
    context_prefix: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    parsed_parts: list[dict[str, Any]] = []
    warnings: list[str] = []
    for index, pdf_path in enumerate(pdf_paths, start=1):
        output_dir = output_root / pdf_path.stem
        result = parser.parse(
            input_path=pdf_path,
            output_dir=output_dir,
            context={"large_pdf_part": f"{context_prefix}_{index}", "source_pdf": pdf_path.name},
        )
        warnings.extend(result.warnings)
        if result.status != ParseStatus.READY or not result.markdown_path:
            raise RuntimeError(result.error or f"MinerU failed to parse {pdf_path.name}")
        parsed_parts.append(
            {
                "index": index,
                "pdf_path": pdf_path,
                "markdown_path": result.markdown_path,
                "layout_path": result.layout_path,
                "source_dir": Path(result.metadata.get("source_dir") or result.markdown_path.parent),
                "metadata": result.metadata,
                "warnings": result.warnings,
            }
        )
    return parsed_parts, warnings


def _write_combined_sample_markdown(sample_parts: list[dict[str, Any]], target: Path) -> Path:
    pieces: list[str] = []
    for part in sample_parts:
        pdf_path = Path(part["pdf_path"])
        markdown = Path(part["markdown_path"]).read_text(encoding="utf-8")
        pieces.extend(
            [
                f"<!-- large_pdf_sample name={pdf_path.stem} -->",
                markdown.strip(),
                "",
            ]
        )
    target.write_text("\n".join(pieces).strip() + "\n", encoding="utf-8")
    return target


def _write_sample_strategy_artifacts(sample_dir: Path, clean_result: Any) -> dict[str, Path]:
    artifacts = {
        "sample_format_probe": sample_dir / "sample_format_probe.json",
        "sample_cleaning_strategy": sample_dir / "sample_cleaning_strategy.json",
        "sample_document_zones": sample_dir / "sample_document_zones.json",
        "sample_metadata_profile": sample_dir / "sample_metadata_profile.json",
        "sample_zone_report": sample_dir / "sample_zone_report.json",
    }
    payloads = {
        "sample_format_probe": clean_result.format_probe,
        "sample_cleaning_strategy": clean_result.strategy,
        "sample_document_zones": clean_result.document_zones,
        "sample_metadata_profile": clean_result.metadata_profile,
        "sample_zone_report": clean_result.zone_report,
    }
    for key, path in artifacts.items():
        _write_json(path, payloads[key])
    return artifacts


def _chapter_pdf_paths(chapter_plan_path: Path) -> list[Path]:
    chapter_dir = chapter_plan_path.parent
    plan = _load_json(chapter_plan_path)
    return [chapter_dir / chapter["filename"] for chapter in plan.get("chapters", []) if isinstance(chapter, dict)]


def _update_chapter_plan_with_parse_results(
    chapter_plan_path: Path,
    chapter_parts: list[dict[str, Any]],
    *,
    material_dir: Path,
) -> list[dict[str, Any]]:
    plan = _load_json(chapter_plan_path)
    chapters = list(plan.get("chapters", []) or [])
    enriched: list[dict[str, Any]] = []
    for chapter, parsed in zip(chapters, chapter_parts):
        item = dict(chapter)
        item["markdown_path"] = _relative(Path(parsed["markdown_path"]), material_dir)
        item["source_dir"] = _relative(Path(parsed["source_dir"]), material_dir)
        if parsed.get("layout_path"):
            item["layout_path"] = _relative(Path(parsed["layout_path"]), material_dir)
        enriched.append(item)
    plan["chapters"] = enriched
    plan["status"] = "parsed"
    _write_json(chapter_plan_path, plan)
    return [
        {
            **chapter,
            "markdown_path": material_dir / chapter["markdown_path"],
            "source_dir": material_dir / chapter["source_dir"],
            "layout_path": material_dir / chapter["layout_path"] if chapter.get("layout_path") else None,
        }
        for chapter in enriched
    ]


def _table_samples(tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for table in tables[:12]:
        columns = [str(column) for column in table.get("columns", [])]
        rows = [row for row in table.get("rows", []) if isinstance(row, dict)]
        samples.append(
            {
                "table_id": table.get("table_id"),
                "page": table.get("page"),
                "chapter_index": table.get("chapter_index"),
                "chapter_title": table.get("chapter_title"),
                "bbox": table.get("bbox"),
                "rows": table.get("row_count"),
                "columns": columns[:6],
                "first_rows": [
                    [str(row.get(column, ""))[:100] for column in columns[:6]]
                    for row in rows[:2]
                ],
                "kind_guess": table.get("kind_guess"),
            }
        )
    return samples


def _offset_page(value: Any, start_physical_page: int) -> int | None:
    try:
        local_page = int(value)
    except (TypeError, ValueError):
        return None
    if local_page < 1:
        return None
    return start_physical_page + local_page - 1


def _prepare_chapter_table_sidecars(
    chapters: list[dict[str, Any]],
    *,
    material_dir: Path,
) -> tuple[dict[str, Any] | None, list[str]]:
    tables: list[dict[str, Any]] = []
    warnings: list[str] = []
    block_counts: dict[str, int] = {}
    title_samples: list[dict[str, Any]] = []
    page_sequence_samples: list[dict[str, Any]] = []
    table_index = 1

    for chapter in chapters:
        layout_path = chapter.get("layout_path")
        if not layout_path:
            continue
        layout_path = Path(layout_path)
        if not layout_path.exists() or not layout_path.is_file():
            warnings.append(f"large_pdf_chapter_layout_missing:{chapter.get('chapter_index')}")
            continue

        try:
            context = build_layout_context(layout_path)
        except Exception as exc:
            warnings.append(f"large_pdf_chapter_layout_unavailable:{chapter.get('chapter_index')}:{exc.__class__.__name__}")
            continue

        summary = context.get("summary", {})
        for key, value in (summary.get("block_counts") or {}).items():
            block_counts[str(key)] = block_counts.get(str(key), 0) + int(value or 0)

        start_physical_page = int(chapter.get("start_physical_page") or 1)
        chapter_index = int(chapter.get("chapter_index") or 0)
        chapter_title = str(chapter.get("title") or "").strip()
        for sample in summary.get("title_samples", []) or []:
            if not isinstance(sample, dict):
                continue
            sample_copy = dict(sample)
            sample_copy["local_page"] = sample_copy.get("page")
            sample_copy["page"] = _offset_page(sample_copy.get("page"), start_physical_page)
            sample_copy["chapter_index"] = chapter_index
            sample_copy["chapter_title"] = chapter_title
            if len(title_samples) < 90:
                title_samples.append(sample_copy)

        for sequence in summary.get("page_sequence_samples", []) or []:
            if not isinstance(sequence, dict):
                continue
            sequence_copy = dict(sequence)
            sequence_copy["local_page"] = sequence_copy.get("page")
            sequence_copy["page"] = _offset_page(sequence_copy.get("page"), start_physical_page)
            sequence_copy["chapter_index"] = chapter_index
            if len(page_sequence_samples) < 20:
                page_sequence_samples.append(sequence_copy)

        chapter_tables: list[dict[str, Any]] = []
        for table in context.get("tables", []) or []:
            if not isinstance(table, dict):
                continue
            table_copy = dict(table)
            local_table_id = str(table_copy.get("table_id") or f"table_{len(chapter_tables) + 1:03d}")
            local_page = table_copy.get("page")
            global_table_id = f"table_{table_index:03d}"
            table_copy["table_id"] = global_table_id
            table_copy["source_table_id"] = local_table_id
            table_copy["chapter_index"] = chapter_index
            table_copy["chapter_title"] = chapter_title
            table_copy["local_page"] = local_page
            table_copy["page"] = _offset_page(local_page, start_physical_page)
            table_copy["source_layout_path"] = _relative(layout_path, material_dir)
            table_copy["markdown"] = render_table_markdown(table_copy)
            chapter_tables.append(table_copy)
            tables.append(table_copy)
            table_index += 1

        if chapter_tables:
            markdown_path = Path(chapter["markdown_path"])
            markdown = markdown_path.read_text(encoding="utf-8")
            replaced, table_warnings = replace_html_tables_with_layout_markdown(markdown, chapter_tables)
            warnings.extend(f"chapter_{chapter_index}:{warning}" for warning in table_warnings)
            table_markdown_path = markdown_path.with_name(f"{markdown_path.stem}.tables{markdown_path.suffix}")
            table_markdown_path.write_text(replaced, encoding="utf-8")
            chapter["markdown_path"] = table_markdown_path
            chapter["table_markdown_path"] = _relative(table_markdown_path, material_dir)
            chapter["table_count"] = len(chapter_tables)

    if not tables:
        return None, warnings

    summary = {
        "source": "large_pdf_chapter_layouts",
        "page_count": sum(int(chapter.get("page_count") or 0) for chapter in chapters),
        "chapter_count": len(chapters),
        "block_counts": block_counts,
        "title_samples": title_samples,
        "table_samples": _table_samples(tables),
        "page_sequence_samples": page_sequence_samples,
    }
    return {"summary": summary, "tables": tables}, warnings


def run_large_pdf_split_pipeline(
    *,
    source_pdf: Path,
    material_dir: Path,
    parser: Any,
    source_name: str,
    use_llm_cleanup: bool,
    user_hints: dict[str, Any] | None = None,
) -> LargePdfPipelineResult:
    parsed_dir = material_dir / "parsed"
    sample_dir = parsed_dir / "large_pdf_samples"
    chapter_dir = parsed_dir / "large_pdf_chapters"
    metadata: dict[str, Any] = {"large_pdf_split": True}
    warnings: list[str] = []

    sample_pages_path = create_large_pdf_samples(source_pdf, sample_dir)
    sample_pdf_paths = _sample_pdf_paths(sample_pages_path)
    sample_parts, sample_warnings = _parse_pdf_parts(
        parser=parser,
        pdf_paths=sample_pdf_paths,
        output_root=sample_dir / "parsed_samples",
        context_prefix="sample",
    )
    warnings.extend(sample_warnings)
    sample_combined_path = _write_combined_sample_markdown(sample_parts, sample_dir / "sample_combined.md")

    sample_clean_result = clean_raw_markdown(
        sample_combined_path.read_text(encoding="utf-8"),
        source_name=f"{source_name} samples",
        use_llm_profile=use_llm_cleanup,
        user_hints=user_hints,
    )
    sample_artifacts = _write_sample_strategy_artifacts(sample_dir, sample_clean_result)
    metadata["cleaning_strategy_override"] = sample_clean_result.strategy
    metadata["document_zones_override"] = {
        "front_matter_zones": [],
        "body_start_line": None,
        "confidence": 0.0,
    }
    metadata["metadata_profile_override"] = sample_clean_result.metadata_profile
    metadata["large_pdf_sample_strategy"] = {
        "strategy_source": sample_clean_result.strategy.get("strategy_source"),
        "warnings": sample_clean_result.warnings,
        "artifacts": {key: _relative(path, material_dir) for key, path in sample_artifacts.items()},
    }
    warnings.extend(f"sample_strategy:{warning}" for warning in sample_clean_result.warnings)

    segments = extract_outline_chapter_segments(source_pdf)
    chapter_plan_source = "pdf_outline"
    if not segments:
        from pypdf import PdfReader

        segments = build_fixed_chunk_segments(len(PdfReader(str(source_pdf)).pages))
        chapter_plan_source = "fixed_page_chunks"
        warnings.append("large_pdf_chapter_plan_fallback_fixed_chunks")
    chapter_plan_path = split_pdf_by_segments(source_pdf, chapter_dir, segments)
    chapter_pdf_paths = _chapter_pdf_paths(chapter_plan_path)
    chapter_parts, chapter_warnings = _parse_pdf_parts(
        parser=parser,
        pdf_paths=chapter_pdf_paths,
        output_root=chapter_dir / "parsed_chapters",
        context_prefix="chapter",
    )
    warnings.extend(chapter_warnings)
    chapters = _update_chapter_plan_with_parse_results(
        chapter_plan_path,
        chapter_parts,
        material_dir=material_dir,
    )
    layout_context, layout_warnings = _prepare_chapter_table_sidecars(chapters, material_dir=material_dir)
    warnings.extend(layout_warnings)
    combined_markdown_path = parsed_dir / "content.md"
    combine_chapter_markdown(
        book_title=Path(source_name).stem,
        chapters=chapters,
        combined_markdown_path=combined_markdown_path,
    )

    metadata["source_format"] = "pdf"
    metadata["parser_backend"] = "large_pdf_split"
    metadata["source_dir"] = str(parsed_dir)
    metadata["large_pdf_samples"] = {
        "status": "ready",
        "sample_pages_path": _relative(sample_pages_path, material_dir),
        "sample_count": len(sample_pdf_paths),
    }
    metadata["large_pdf_chapter_plan"] = {
        "status": "ready",
        "source": chapter_plan_source,
        "chapter_plan_path": _relative(chapter_plan_path, material_dir),
        "chapter_count": len(chapters),
    }
    if layout_context:
        metadata["large_pdf_table_sidecar"] = {
            "status": "ready",
            "source": "chapter_layouts",
            "table_count": len(layout_context.get("tables", [])),
            "warning_count": len(layout_warnings),
        }
        metadata["large_pdf_tables_replaced"] = True
    else:
        metadata["large_pdf_table_sidecar"] = {
            "status": "missing",
            "source": "chapter_layouts",
            "table_count": 0,
            "warning_count": len(layout_warnings),
        }

    return LargePdfPipelineResult(
        parse_result=ParseResult(
            status=ParseStatus.READY,
            markdown_path=combined_markdown_path,
            metadata=metadata,
            warnings=warnings,
        ),
        sample_pages_path=sample_pages_path,
        chapter_plan_path=chapter_plan_path,
        layout_context=layout_context,
        sample_artifacts=sample_artifacts,
        metadata=metadata,
        warnings=warnings,
    )
