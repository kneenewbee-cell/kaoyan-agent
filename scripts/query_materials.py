#!/usr/bin/env python3
"""CLI for searching one user's materials library."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from materials.search import search_user_materials


def configure_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(
        description="Search the current user's material library.",
    )
    parser.add_argument(
        "--user-id",
        type=str,
        default="tester",
        help="Business user id, default: tester",
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Search query",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return, default: 5",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="hybrid",
        choices=["keyword", "vector", "hybrid"],
        help="Search mode, default: hybrid",
    )
    parser.add_argument(
        "--material-id",
        type=str,
        default=None,
        help="Optional material id filter",
    )
    parser.add_argument(
        "--subject",
        type=str,
        default=None,
        choices=["math", "politics", "408", "english", "unknown"],
        help="Optional subject filter",
    )
    parser.add_argument(
        "--material-type",
        type=str,
        default=None,
        choices=["lecture", "note", "exam", "wrong_book", "school_info", "unknown"],
        help="Optional material type filter",
    )

    args = parser.parse_args()

    print(f"query : {args.query}")
    print(f"user  : {args.user_id}")
    print(f"mode  : {args.mode}")
    print("-" * 50)

    filters: dict[str, str] = {}
    if args.material_id:
        filters["material_id"] = args.material_id
    if args.subject:
        filters["subject"] = args.subject
    if args.material_type:
        filters["material_type"] = args.material_type

    results = search_user_materials(
        user_id=args.user_id,
        query=args.query,
        top_k=args.top_k,
        filters=filters if filters else None,
        mode=args.mode,
    )

    if not results:
        print("No matching materials found.")
        return

    for result in results:
        print(f"--- rank {result.rank} (score: {result.score:.4f}) ---")
        print(f"  material_id  : {result.material_id}")
        print(f"  chunk_id     : {result.chunk_id}")
        print(f"  section      : {result.section_title or '(no section)'}")
        print(f"  heading_path : {' > '.join(result.heading_path) if result.heading_path else '(none)'}")
        print(f"  asset_paths  : {result.asset_paths}")
        print(f"  source_file  : {result.metadata.get('original_filename', '?')}")
        print(f"  subject      : {result.metadata.get('subject', '?')}")
        print(f"  matched_by   : {result.metadata.get('matched_by') or result.metadata.get('search_mode', args.mode)}")
        print(f"  text_preview : {result.text[:200]}...")
        print()


if __name__ == "__main__":
    main()
