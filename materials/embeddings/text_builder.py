from __future__ import annotations

from ..schemas import Chunk


def _clean_value(value: object) -> str:
    return str(value or "").strip()


def build_chunk_embedding_text(chunk: Chunk) -> str:
    """Build the semantic text sent to the embedding model for one chunk."""
    metadata = chunk.metadata or {}
    lines: list[str] = []

    heading_path = [item.strip() for item in chunk.heading_path if item and item.strip()]
    if heading_path:
        lines.append("标题路径：" + " > ".join(heading_path))

    title = _clean_value(metadata.get("title"))
    if title and (not heading_path or title != heading_path[0]):
        lines.append("资料标题：" + title)

    subject = _clean_value(metadata.get("subject"))
    if subject and subject != "unknown":
        lines.append("学科：" + subject)

    material_type = _clean_value(metadata.get("material_type"))
    if material_type and material_type != "unknown":
        lines.append("资料类型：" + material_type)

    section_title = _clean_value(chunk.section_title)
    if section_title and section_title not in heading_path:
        lines.append("当前小节：" + section_title)

    body = chunk.text.strip()
    if lines:
        lines.append("正文：")
    lines.append(body)
    return "\n".join(line for line in lines if line).strip()
