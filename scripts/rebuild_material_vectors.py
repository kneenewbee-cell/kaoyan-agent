#!/usr/bin/env python3
"""Rebuild Chroma vectors for existing ingested materials."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from materials.indexing.vector_indexer import build_material_vector_index
from materials.schemas import Chunk
from materials.security import resolve_material_id, resolve_user_id
from materials.storage import MaterialStorage
from materials.vectorstores.chroma_store import ChromaVectorStore


def configure_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def load_chunks(path: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                chunks.append(Chunk.from_dict(json.loads(line)))
    return chunks


def cleanup_stale_vectors(user_id: str, active_material_ids: set[str]) -> int:
    store = ChromaVectorStore()
    collection = store.collection()
    payload = collection.get(where={"user_id": user_id}, include=["metadatas"])
    stale_ids: list[str] = []
    for record_id, metadata in zip(payload.get("ids") or [], payload.get("metadatas") or []):
        if (metadata or {}).get("material_id") not in active_material_ids:
            stale_ids.append(record_id)
    if stale_ids:
        collection.delete(ids=stale_ids)
    return len(stale_ids)


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Rebuild material chunk vectors in Chroma.")
    parser.add_argument("--user-id", type=str, default="tester", help="Business user id, default: tester")
    parser.add_argument("--material-id", type=str, default=None, help="Optional material id to rebuild")
    parser.add_argument("--cleanup-stale", action="store_true", help="Delete Chroma records for materials no longer present")
    parser.add_argument("--dry-run", action="store_true", help="Print candidates without calling embedding or Chroma")
    args = parser.parse_args()

    user_id = resolve_user_id(args.user_id)
    material_id = resolve_material_id(args.material_id) if args.material_id else None
    storage = MaterialStorage()
    manifests = storage.list_user_manifests(user_id)
    manifests = [manifest for manifest in manifests if manifest.parse_status.value == "ready"]
    if material_id:
        manifests = [manifest for manifest in manifests if manifest.material_id == material_id]

    active_ids = {manifest.material_id for manifest in storage.list_user_manifests(user_id) if manifest.parse_status.value == "ready"}
    if args.cleanup_stale and not args.dry_run:
        deleted = cleanup_stale_vectors(user_id, active_ids)
        print(f"cleanup_stale_deleted: {deleted}")

    if not manifests:
        print("No ready materials found.")
        return

    for manifest in manifests:
        chunks_path = manifest.paths.get("chunks") or "chunks/chunks.jsonl"
        chunks_file = storage.material_dir(user_id, manifest.material_id) / chunks_path
        if not chunks_file.exists():
            print(f"{manifest.material_id}: missing chunks file: {chunks_file}")
            continue
        chunks = load_chunks(chunks_file)
        token_total = sum(chunk.token_count for chunk in chunks)
        print(
            f"{manifest.material_id}: {manifest.original_filename} "
            f"chunks={len(chunks)} estimated_tokens={token_total}"
        )
        if args.dry_run:
            continue
        result = build_material_vector_index(chunks, manifest, enabled=True)
        manifest.metadata["vector_index"] = result.to_dict()
        storage.save_manifest(user_id, manifest.material_id, manifest)
        print(
            f"  vector_status={result.status} indexed={result.chunk_count} "
            f"model={result.model} tokens={result.usage.get('prompt_tokens', 0)} "
            f"error={result.error or ''}"
        )


if __name__ == "__main__":
    main()
