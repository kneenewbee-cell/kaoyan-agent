from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .postprocess.asset_rewriter import IMAGE_RE


CHAPTER_PLAN_FILENAME = "chapter_plan.json"
TOP_LEVEL_TITLE_RE = re.compile(r"^(?:第\s*[一二三四五六七八九十百千万\d]+\s*章\b|附录\b)")
SAFE_ID_RE = re.compile(r"[^a-zA-Z0-9_-]+")
MARKDOWN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
LARGE_PDF_CHAPTER_MARKER_RE = re.compile(r"^\s*<!--\s+large_pdf_chapter\b")


@dataclass(frozen=True)
class ChapterSegment:
    index: int
    title: str
    start_pdf_index: int
    end_pdf_index: int
    source: str = "pdf_outline"

    @property
    def page_count(self) -> int:
        return self.end_pdf_index - self.start_pdf_index

    @property
    def filename(self) -> str:
        return f"chapter_{self.index:03d}.pdf"

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter_index": self.index,
            "title": self.title,
            "filename": self.filename,
            "start_pdf_index": self.start_pdf_index,
            "end_pdf_index": self.end_pdf_index,
            "start_physical_page": self.start_pdf_index + 1,
            "end_physical_page": self.end_pdf_index,
            "page_count": self.page_count,
            "source": self.source,
        }


def _walk_outline_items(items: list[Any], *, depth: int = 0) -> list[tuple[Any, int]]:
    flattened: list[tuple[Any, int]] = []
    for item in items:
        if isinstance(item, list):
            flattened.extend(_walk_outline_items(item, depth=depth + 1))
        else:
            flattened.append((item, depth))
    return flattened


def _is_top_level_chapter_title(title: str) -> bool:
    normalized = re.sub(r"\s+", " ", title).strip()
    return bool(TOP_LEVEL_TITLE_RE.match(normalized))


def extract_outline_chapter_segments(source_pdf: Path) -> list[ChapterSegment]:
    from pypdf import PdfReader

    reader = PdfReader(str(source_pdf))
    total_pages = len(reader.pages)
    outline = getattr(reader, "outline", []) or []
    starts: list[tuple[str, int]] = []
    for item, depth in _walk_outline_items(outline if isinstance(outline, list) else []):
        if depth != 0:
            continue
        title = str(getattr(item, "title", item)).strip()
        if not _is_top_level_chapter_title(title):
            continue
        try:
            page_index = int(reader.get_destination_page_number(item))
        except Exception:
            continue
        if 0 <= page_index < total_pages:
            starts.append((title, page_index))

    deduped: list[tuple[str, int]] = []
    seen_pages: set[int] = set()
    for title, page_index in sorted(starts, key=lambda pair: pair[1]):
        if page_index in seen_pages:
            continue
        deduped.append((title, page_index))
        seen_pages.add(page_index)

    segments: list[ChapterSegment] = []
    for index, (title, start_page) in enumerate(deduped, start=1):
        end_page = deduped[index][1] if index < len(deduped) else total_pages
        if end_page <= start_page:
            continue
        segments.append(
            ChapterSegment(
                index=index,
                title=title,
                start_pdf_index=start_page,
                end_pdf_index=end_page,
            )
        )
    return segments


def build_fixed_chunk_segments(total_pages: int, *, max_pages: int = 160) -> list[ChapterSegment]:
    if total_pages <= 0:
        raise ValueError("total_pages must be positive")
    if max_pages <= 0:
        raise ValueError("max_pages must be positive")
    segments: list[ChapterSegment] = []
    start = 0
    while start < total_pages:
        end = min(start + max_pages, total_pages)
        index = len(segments) + 1
        segments.append(
            ChapterSegment(
                index=index,
                title=f"PDF 分段 {index}",
                start_pdf_index=start,
                end_pdf_index=end,
                source="fixed_page_chunks",
            )
        )
        start = end
    return segments


def split_pdf_by_segments(source_pdf: Path, output_dir: Path, segments: list[ChapterSegment]) -> Path:
    from pypdf import PdfReader, PdfWriter

    if not segments:
        raise ValueError("chapter segments are required")

    output_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(source_pdf))
    total_pages = len(reader.pages)
    chapters_payload: list[dict[str, Any]] = []
    for segment in segments:
        if segment.start_pdf_index < 0 or segment.end_pdf_index > total_pages or segment.end_pdf_index <= segment.start_pdf_index:
            raise ValueError(f"invalid chapter segment range: {segment}")
        writer = PdfWriter()
        for page_index in range(segment.start_pdf_index, segment.end_pdf_index):
            writer.add_page(reader.pages[page_index])
        target = output_dir / segment.filename
        with target.open("wb") as file:
            writer.write(file)
        chapters_payload.append(segment.to_dict())

    source = segments[0].source if len({segment.source for segment in segments}) == 1 else "mixed"
    plan = {
        "version": "0.1",
        "source": source,
        "source_pdf": Path(source_pdf).name,
        "total_pages": total_pages,
        "chapters": chapters_payload,
    }
    plan_path = output_dir / CHAPTER_PLAN_FILENAME
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return plan_path


def _rewrite_image_refs_to_combined_source(markdown: str, *, chapter_source_dir: Path, combined_source_dir: Path) -> str:
    def rewrite(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        source_url = match.group(2)
        if source_url.startswith(("http://", "https://", "data:")):
            return match.group(0)
        source_path = Path(source_url)
        if not source_path.is_absolute():
            source_path = (chapter_source_dir / source_path).resolve()
        if not source_path.exists():
            return match.group(0)
        try:
            rewritten = source_path.relative_to(combined_source_dir.resolve())
        except ValueError:
            return match.group(0)
        return f"![{alt_text}]({str(rewritten).replace('\\', '/')})"

    return IMAGE_RE.sub(rewrite, markdown)


def _normalize_title_for_compare(title: str) -> str:
    return re.sub(r"[\s#：:、，,。；;（）()\[\]【】《》<>-]+", "", title).lower()


def _strip_leading_duplicate_heading(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    first_content_index = next((index for index, line in enumerate(lines) if line.strip()), None)
    if first_content_index is None:
        return markdown

    match = MARKDOWN_HEADING_RE.match(lines[first_content_index])
    if not match:
        return markdown

    heading_title = match.group(1).strip()
    normalized_heading = _normalize_title_for_compare(heading_title)
    normalized_title = _normalize_title_for_compare(title)
    if not normalized_heading or normalized_heading != normalized_title:
        return markdown

    end_index = first_content_index + 1
    while end_index < len(lines) and not lines[end_index].strip():
        end_index += 1
    return "\n".join(lines[:first_content_index] + lines[end_index:]).strip()


def combine_chapter_markdown(
    *,
    book_title: str,
    chapters: list[dict[str, Any]],
    combined_markdown_path: Path,
) -> Path:
    combined_source_dir = combined_markdown_path.parent
    parts: list[str] = [f"# {book_title}", ""]
    for chapter in chapters:
        title = str(chapter["title"]).strip()
        markdown_path = Path(chapter["markdown_path"])
        source_dir = Path(chapter.get("source_dir") or markdown_path.parent)
        markdown = markdown_path.read_text(encoding="utf-8")
        markdown = _strip_leading_duplicate_heading(markdown, title)
        markdown = _rewrite_image_refs_to_combined_source(
            markdown,
            chapter_source_dir=source_dir,
            combined_source_dir=combined_source_dir,
        )
        parts.extend(
            [
                f"<!-- large_pdf_chapter index={chapter['chapter_index']} "
                f"physical_pages={chapter['start_physical_page']}-{chapter['end_physical_page']} -->",
                f"## {title}",
                "",
                markdown.strip(),
                "",
            ]
        )
    combined_markdown_path.parent.mkdir(parents=True, exist_ok=True)
    combined_markdown_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    return combined_markdown_path


def restore_large_pdf_chapter_headings(markdown: str) -> str:
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        if not LARGE_PDF_CHAPTER_MARKER_RE.match(lines[index]):
            index += 1
            continue
        next_index = index + 1
        while next_index < len(lines) and not lines[next_index].strip():
            next_index += 1
        if next_index >= len(lines):
            break
        stripped = lines[next_index].strip()
        match = MARKDOWN_HEADING_RE.match(stripped)
        if match:
            lines[next_index] = f"## {match.group(1).strip()}"
        elif stripped:
            lines[next_index] = f"## {stripped}"
        index = next_index + 1
    return "\n".join(lines).strip() + "\n"
