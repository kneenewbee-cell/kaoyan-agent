from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Callable

from ..embeddings.qwen_embedding import (
    EmbeddingSettings,
    embed_texts,
    embedding_api_available,
    load_embedding_settings,
)
from ..embeddings.text_builder import build_chunk_embedding_text
from ..schemas import Chunk, MaterialManifest
from ..vectorstores.chroma_store import (
    ChromaUnavailableError,
    ChromaVectorStore,
    DEFAULT_COLLECTION_NAME,
    VectorRecord,
)


Embedder = Callable[[list[str]], list[list[float]]]


@dataclass
class VectorIndexResult:
    status: str
    enabled: bool
    provider: str = "chroma"
    collection: str = DEFAULT_COLLECTION_NAME
    model: str = "text-embedding-v4"
    dimension: int = 1024
    chunk_count: int = 0
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "enabled": self.enabled,
            "provider": self.provider,
            "collection": self.collection,
            "model": self.model,
            "dimension": self.dimension,
            "chunk_count": self.chunk_count,
            "warnings": self.warnings,
            "error": self.error,
            "usage": self.usage,
        }


def _env_flag(name: str) -> str:
    return (os.getenv(name) or "").strip().lower()


def vector_index_requested(explicit: bool | None = None, settings: EmbeddingSettings | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    flag = _env_flag("MATERIALS_VECTOR_INDEX_ENABLED")
    if flag in {"0", "false", "no", "off", "disabled"}:
        return False
    if flag in {"1", "true", "yes", "on", "enabled"}:
        return True
    return True


def vector_record_id(chunk: Chunk) -> str:
    return f"{chunk.user_id}:{chunk.material_id}:{chunk.chunk_id}"


def chunk_vector_metadata(chunk: Chunk, *, settings: EmbeddingSettings, manifest: MaterialManifest) -> dict[str, Any]:
    metadata = dict(chunk.metadata or {})
    return {
        "user_id": chunk.user_id,
        "material_id": chunk.material_id,
        "chunk_id": chunk.chunk_id,
        "chunk_index": chunk.chunk_index,
        "section_title": chunk.section_title or "",
        "heading_path_text": " > ".join(chunk.heading_path),
        "subject": metadata.get("subject") or manifest.subject.value,
        "material_type": metadata.get("material_type") or manifest.material_type.value,
        "original_filename": metadata.get("original_filename") or manifest.original_filename,
        "title": metadata.get("title") or "",
        "source_type": metadata.get("source_type") or "",
        "table_id": metadata.get("table_id") or "",
        "table_row_index": metadata.get("table_row_index") or "",
        "page": metadata.get("page") or "",
        "kind_guess": metadata.get("kind_guess") or "",
        "source_markdown_path": manifest.paths.get("markdown") or "",
        "embedding_model": settings.model,
        "embedding_dimension": settings.dimensions,
    }


def build_material_vector_index(
    chunks: list[Chunk],
    manifest: MaterialManifest,
    *,
    enabled: bool | None = None,
    store: ChromaVectorStore | None = None,
    embedder: Embedder | None = None,
) -> VectorIndexResult:
    settings = load_embedding_settings()
    collection = (store.collection_name if store else DEFAULT_COLLECTION_NAME)
    result = VectorIndexResult(
        status="skipped",
        enabled=False,
        collection=collection,
        model=settings.model,
        dimension=settings.dimensions,
    )

    requested = vector_index_requested(enabled, settings)
    result.enabled = requested
    if not requested:
        result.warnings.append("vector_index_disabled")
        return result
    if not chunks:
        result.warnings.append("vector_index_no_chunks")
        return result
    if embedder is None and not settings.api_key:
        result.warnings.append("vector_index_missing_api_key")
        result.error = "DashScope embedding API key is not configured"
        return result

    usage: dict[str, Any] = {}
    try:
        target_store = store or ChromaVectorStore(collection_name=collection)
        texts = [build_chunk_embedding_text(chunk) for chunk in chunks]
        embeddings = embedder(texts) if embedder else embed_texts(texts, settings=settings, usage_metrics=usage)
        records = [
            VectorRecord(
                record_id=vector_record_id(chunk),
                embedding=embedding,
                document=chunk.text,
                metadata=chunk_vector_metadata(chunk, settings=settings, manifest=manifest),
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        if len(records) != len(chunks):
            raise RuntimeError("Embedding count does not match chunk count")
        target_store.delete_material(manifest.user_id, manifest.material_id)
        result.chunk_count = target_store.upsert_records(records)
        result.status = "ready"
        result.usage = usage
        return result
    except ChromaUnavailableError as exc:
        result.status = "skipped"
        result.error = str(exc)
        result.warnings.append("vector_index_chroma_unavailable")
        return result
    except Exception as exc:
        result.status = "failed"
        result.error = str(exc)
        result.warnings.append(f"vector_index_failed:{exc.__class__.__name__}")
        return result


def delete_material_vector_index(
    user_id: str,
    material_id: str,
    *,
    enabled: bool | None = None,
    store: ChromaVectorStore | None = None,
) -> VectorIndexResult:
    settings = load_embedding_settings()
    collection = (store.collection_name if store else DEFAULT_COLLECTION_NAME)
    result = VectorIndexResult(
        status="skipped",
        enabled=False,
        collection=collection,
        model=settings.model,
        dimension=settings.dimensions,
    )
    requested = True if enabled is None else bool(enabled)
    result.enabled = requested
    if not requested:
        result.warnings.append("vector_index_disabled")
        return result
    try:
        target_store = store or ChromaVectorStore(collection_name=collection)
        target_store.delete_material(user_id, material_id)
        result.status = "ready"
        return result
    except ChromaUnavailableError as exc:
        result.status = "skipped"
        result.error = str(exc)
        result.warnings.append("vector_index_chroma_unavailable")
        return result
    except Exception as exc:
        result.status = "failed"
        result.error = str(exc)
        result.warnings.append(f"vector_index_delete_failed:{exc.__class__.__name__}")
        return result
