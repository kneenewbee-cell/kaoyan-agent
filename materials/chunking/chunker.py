from __future__ import annotations

import hashlib
import re
from pathlib import Path

from ..schemas import Chunk
from .section_splitter import split_by_headings
from .token_counter import estimate_tokens

MAX_CHUNK_TOKENS = 1024
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def _extract_asset_paths_from_text(text: str) -> list[str]:
    return [match.group(2) for match in IMAGE_RE.finditer(text)]


def _make_chunk_id(material_id: str, chunk_index: int) -> str:
    raw = f"{material_id}:{chunk_index}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _split_long_sentence(text: str, max_tokens: int) -> list[str]:
    sentences = re.split(r"(?<=[。！？!?])|\n", text)
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        candidate = f"{current}\n{sentence}".strip() if current else sentence
        if current and estimate_tokens(candidate) > max_tokens:
            chunks.append(current.strip())
            current = sentence
        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())

    return chunks or [text]


def _split_long_text(text: str, max_tokens: int = MAX_CHUNK_TOKENS) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and estimate_tokens(candidate) > max_tokens:
            chunks.append(current.strip())
            if estimate_tokens(paragraph) > max_tokens:
                chunks.extend(_split_long_sentence(paragraph, max_tokens))
                current = ""
            else:
                current = paragraph
        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())

    return chunks or [text]


def chunk_markdown(
    markdown: str,
    material_id: str,
    user_id: str,
    max_tokens: int = MAX_CHUNK_TOKENS,
) -> list[Chunk]:
    sections = split_by_headings(markdown)
    chunks: list[Chunk] = []
    chunk_index = 0

    for section in sections:
        section_text = section.content.strip()
        if not section_text:
            continue

        section_parts = [section_text]
        if estimate_tokens(section_text) > max_tokens:
            section_parts = _split_long_text(section_text, max_tokens)

        for part in section_parts:
            text = part.strip()
            if not text:
                continue

            chunks.append(
                Chunk(
                    chunk_id=_make_chunk_id(material_id, chunk_index),
                    material_id=material_id,
                    user_id=user_id,
                    chunk_index=chunk_index,
                    text=text,
                    section_title=section.title,
                    heading_path=section.heading_path,
                    asset_paths=_extract_asset_paths_from_text(text),
                    token_count=estimate_tokens(text),
                    metadata={
                        "start_line": section.start_line,
                        "end_line": section.end_line,
                        "level": section.level,
                    },
                )
            )
            chunk_index += 1

    return chunks


def chunk_markdown_file(
    markdown_path: Path,
    material_id: str,
    user_id: str,
    max_tokens: int = MAX_CHUNK_TOKENS,
) -> list[Chunk]:
    content = markdown_path.read_text(encoding="utf-8")
    return chunk_markdown(content, material_id, user_id, max_tokens)
