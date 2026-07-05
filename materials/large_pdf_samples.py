from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_FRONT_SAMPLE_PAGES = 30
DEFAULT_MIDDLE_SAMPLE_PAGES = 20
DEFAULT_TAIL_SAMPLE_PAGES = 20
SAMPLE_PAGES_FILENAME = "sample_pages.json"


@dataclass(frozen=True)
class PdfSampleWindow:
    name: str
    start_pdf_index: int
    end_pdf_index: int

    @property
    def page_count(self) -> int:
        return self.end_pdf_index - self.start_pdf_index

    def to_dict(self, *, filename: str) -> dict[str, Any]:
        return {
            "sample_name": self.name,
            "filename": filename,
            "start_pdf_index": self.start_pdf_index,
            "end_pdf_index": self.end_pdf_index,
            "start_physical_page": self.start_pdf_index + 1,
            "end_physical_page": self.end_pdf_index,
            "page_count": self.page_count,
        }


def build_sample_windows(
    total_pages: int,
    *,
    front_pages: int = DEFAULT_FRONT_SAMPLE_PAGES,
    middle_pages: int = DEFAULT_MIDDLE_SAMPLE_PAGES,
    tail_pages: int = DEFAULT_TAIL_SAMPLE_PAGES,
) -> list[PdfSampleWindow]:
    if total_pages <= 0:
        raise ValueError("total_pages must be positive")
    if front_pages <= 0 or middle_pages <= 0 or tail_pages <= 0:
        raise ValueError("sample page counts must be positive")

    if total_pages <= front_pages + middle_pages + tail_pages:
        return [PdfSampleWindow("full", 0, total_pages)]

    front_end = min(front_pages, total_pages)
    tail_start = max(total_pages - tail_pages, 0)
    middle_width = min(middle_pages, max(tail_start - front_end, 0))
    middle_start = max(0, (total_pages - middle_width) // 2)
    middle_end = middle_start + middle_width

    if middle_start < front_end:
        middle_start = front_end
        middle_end = middle_start + middle_width
    if middle_end > tail_start:
        middle_end = tail_start
        middle_start = max(front_end, middle_end - middle_width)

    windows = [PdfSampleWindow("front", 0, front_end)]
    if middle_start < middle_end:
        windows.append(PdfSampleWindow("middle", middle_start, middle_end))
    windows.append(PdfSampleWindow("tail", tail_start, total_pages))
    return windows


def create_large_pdf_samples(
    source_pdf: Path,
    output_dir: Path,
    *,
    front_pages: int = DEFAULT_FRONT_SAMPLE_PAGES,
    middle_pages: int = DEFAULT_MIDDLE_SAMPLE_PAGES,
    tail_pages: int = DEFAULT_TAIL_SAMPLE_PAGES,
) -> Path:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("pypdf is required to create large PDF samples") from exc

    source_pdf = Path(source_pdf)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(source_pdf))
    total_pages = len(reader.pages)
    windows = build_sample_windows(
        total_pages,
        front_pages=front_pages,
        middle_pages=middle_pages,
        tail_pages=tail_pages,
    )

    window_payloads: list[dict[str, Any]] = []
    page_payloads: list[dict[str, Any]] = []
    for window in windows:
        filename = f"{window.name}.pdf"
        sample_path = output_dir / filename
        writer = PdfWriter()
        for original_pdf_index in range(window.start_pdf_index, window.end_pdf_index):
            writer.add_page(reader.pages[original_pdf_index])
            page_payloads.append(
                {
                    "sample_name": window.name,
                    "sample_pdf_page_index": original_pdf_index - window.start_pdf_index,
                    "original_pdf_index": original_pdf_index,
                    "physical_page": original_pdf_index + 1,
                }
            )
        with sample_path.open("wb") as file:
            writer.write(file)
        window_payloads.append(window.to_dict(filename=filename))

    sample_pages_path = output_dir / SAMPLE_PAGES_FILENAME
    payload = {
        "version": "0.1",
        "source_pdf": source_pdf.name,
        "total_pages": total_pages,
        "config": {
            "front_pages": front_pages,
            "middle_pages": middle_pages,
            "tail_pages": tail_pages,
        },
        "windows": window_payloads,
        "pages": page_payloads,
    }
    sample_pages_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return sample_pages_path
