#!/usr/bin/env python3
"""CLI for ingesting one material into the per-user materials library."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from materials.service import MaterialIngestionService


def configure_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(
        description="Ingest a material file into the user materials library.",
    )
    parser.add_argument(
        "--user-id",
        type=str,
        default="tester",
        help="Business user id, default: tester",
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the material file",
    )
    parser.add_argument(
        "--subject",
        type=str,
        default="unknown",
        choices=["math", "politics", "408", "english", "unknown"],
        help="Subject, default: unknown",
    )
    parser.add_argument(
        "--material-type",
        type=str,
        default="unknown",
        choices=["lecture", "note", "exam", "wrong_book", "school_info", "unknown"],
        help="Material type, default: unknown",
    )
    parser.add_argument(
        "--no-llm-cleanup",
        action="store_true",
        help="Disable Qwen strategy generation and use local/default cleaning strategy only.",
    )
    vector_group = parser.add_mutually_exclusive_group()
    vector_group.add_argument(
        "--enable-vector-index",
        dest="enable_vector_index",
        action="store_true",
        default=True,
        help="Build a Chroma vector index with text-embedding-v4 after chunking, default: enabled.",
    )
    vector_group.add_argument(
        "--no-vector-index",
        dest="enable_vector_index",
        action="store_false",
        help="Disable Chroma vector indexing for this ingest run.",
    )

    args = parser.parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    print(f"file         : {file_path.name}")
    print(f"user_id      : {args.user_id}")
    print(f"subject      : {args.subject}")
    print(f"material_type: {args.material_type}")
    print("-" * 50)

    result = MaterialIngestionService().ingest_file(
        file_path=file_path,
        user_id=args.user_id,
        subject=args.subject,
        material_type=args.material_type,
        use_llm_cleanup=not args.no_llm_cleanup,
        enable_vector_index=args.enable_vector_index,
    )

    print(f"material_id   : {result.material_id}")
    print(f"user_id       : {result.user_id}")
    print(f"parse_status  : {result.parse_status.value}")
    print(f"manifest_path : {result.manifest_path}")
    print(f"markdown_path : {result.markdown_path}")
    print(f"chunk_count   : {result.chunk_count}")
    print(f"asset_count   : {result.asset_count}")

    if result.error:
        print(f"error         : {result.error}")
        sys.exit(1)

    print("status        : ok")


if __name__ == "__main__":
    main()
