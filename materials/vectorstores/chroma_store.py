from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHROMA_DIR = ROOT / "data" / "vectorstores" / "chroma"
DEFAULT_COLLECTION_NAME = "materials_text_embedding_v4_1024"


class ChromaUnavailableError(RuntimeError):
    pass


@dataclass(frozen=True)
class VectorRecord:
    record_id: str
    embedding: list[float]
    document: str
    metadata: dict[str, Any]


def _metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, list | tuple):
        return " > ".join(str(item) for item in value if item is not None)
    return str(value)


def sanitize_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    return {key: _metadata_value(value) for key, value in metadata.items()}


def build_where_filter(filters: dict[str, Any]) -> dict[str, Any] | None:
    clauses: list[dict[str, Any]] = []
    for key, value in filters.items():
        if value is None or value == "":
            continue
        clauses.append({key: _metadata_value(value)})
    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


class ChromaVectorStore:
    def __init__(
        self,
        *,
        persist_dir: Path | str | None = None,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        distance: str = "cosine",
    ) -> None:
        self.persist_dir = Path(persist_dir) if persist_dir else DEFAULT_CHROMA_DIR
        self.collection_name = collection_name
        self.distance = distance
        self._client: Any | None = None
        self._collection: Any | None = None

    def _load_chroma(self) -> Any:
        try:
            import chromadb
        except Exception as exc:  # pragma: no cover - exercised when optional dependency is absent
            raise ChromaUnavailableError("chromadb is not installed") from exc
        return chromadb

    def collection(self) -> Any:
        if self._collection is not None:
            return self._collection
        chromadb = self._load_chroma()
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": self.distance},
        )
        return self._collection

    def upsert_records(self, records: list[VectorRecord]) -> int:
        if not records:
            return 0
        collection = self.collection()
        ids = [record.record_id for record in records]
        embeddings = [record.embedding for record in records]
        documents = [record.document for record in records]
        metadatas = [sanitize_metadata(record.metadata) for record in records]
        if hasattr(collection, "upsert"):
            collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
        else:  # pragma: no cover - compatibility with old Chroma releases
            collection.delete(ids=ids)
            collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
        return len(records)

    def delete_material(self, user_id: str, material_id: str) -> None:
        where = build_where_filter({"user_id": user_id, "material_id": material_id})
        if where is None:
            return
        self.collection().delete(where=where)

    def query(
        self,
        query_embedding: list[float],
        *,
        top_k: int,
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        where = build_where_filter(filters)
        kwargs: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        return self.collection().query(**kwargs)
