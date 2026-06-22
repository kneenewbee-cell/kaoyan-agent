"""materials/quality/validators.py — Markdown/asset/chunk 质量检查规则。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..schemas import Chunk

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
BROKEN_CHARS = ("�", "□", "�", "Ã", "ä¸", "å")


def text_metrics(markdown: str) -> dict[str, Any]:
    stripped = markdown.strip()
    char_count = len(stripped)
    lines = stripped.splitlines() if stripped else []
    non_empty_lines = [line for line in lines if line.strip()]
    broken_count = sum(stripped.count(ch) for ch in BROKEN_CHARS)
    repeat_ratio = 0.0
    if non_empty_lines:
        repeat_ratio = 1 - (len(set(non_empty_lines)) / len(non_empty_lines))
    return {
        "char_count": char_count,
        "line_count": len(lines),
        "non_empty_line_count": len(non_empty_lines),
        "broken_char_count": broken_count,
        "broken_char_ratio": broken_count / max(char_count, 1),
        "repeat_line_ratio": repeat_ratio,
    }


def heading_metrics(markdown: str) -> dict[str, Any]:
    headings = [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(markdown)]
    short_headings = [title for _, title in headings if len(title) <= 1]
    duplicate_titles = len(headings) - len({title for _, title in headings}) if headings else 0
    level_jumps = 0
    last_level = 0
    for level, _ in headings:
        if last_level and level - last_level > 1:
            level_jumps += 1
        last_level = level
    return {
        "heading_count": len(headings),
        "short_heading_count": len(short_headings),
        "duplicate_heading_count": duplicate_titles,
        "heading_level_jump_count": level_jumps,
        "first_heading": headings[0][1] if headings else None,
    }


def asset_metrics(markdown: str, material_dir: Path | None = None) -> dict[str, Any]:
    refs = [m.group(2) for m in IMAGE_RE.finditer(markdown)]
    missing: list[str] = []
    if material_dir is not None:
        for ref in refs:
            if ref.startswith(("http://", "https://", "data:")):
                continue
            ref_path = Path(ref)
            candidate = ref_path if ref_path.is_absolute() else (material_dir / ref_path).resolve()
            if not candidate.exists():
                missing.append(ref)
    return {
        "image_ref_count": len(refs),
        "missing_image_count": len(missing),
        "missing_image_refs": missing[:20],
    }


def chunk_metrics(chunks: list[Chunk] | None = None) -> dict[str, Any]:
    chunks = chunks or []
    if not chunks:
        return {
            "chunk_count": 0,
            "empty_chunk_count": 0,
            "short_chunk_count": 0,
            "long_chunk_count": 0,
            "duplicate_chunk_count": 0,
            "missing_heading_path_count": 0,
        }
    texts = [chunk.text.strip() for chunk in chunks]
    return {
        "chunk_count": len(chunks),
        "empty_chunk_count": sum(1 for text in texts if not text),
        "short_chunk_count": sum(1 for chunk in chunks if 0 < chunk.token_count < 20),
        "long_chunk_count": sum(1 for chunk in chunks if chunk.token_count > 1200),
        "duplicate_chunk_count": len(texts) - len(set(texts)),
        "missing_heading_path_count": sum(1 for chunk in chunks if not chunk.heading_path),
    }
