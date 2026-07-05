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
        choices=["textbook", "lecture", "exercise", "unknown", "auto"],
        help="Material type, default: unknown",
    )
    parser.add_argument(
        "--no-llm-cleanup",
        action="store_true",
        help="Disable Qwen strategy generation and use local/default cleaning strategy only.",
    )
    parser.add_argument(
        "--no-formula-cleanup",
        action="store_true",
        help="Disable local formula rendering cleanup.",
    )
    parser.add_argument(
        "--formula-cleanup-level",
        type=str,
        default="safe",
        choices=["safe", "experimental"],
        help="Formula cleanup level, default: safe.",
    )
    parser.add_argument(
        "--use-llm-formula-cleanup",
        action="store_true",
        help="Enable LLM repair proposals for residual formula render errors.",
    )
    parser.add_argument(
        "--llm-formula-min-confidence",
        type=float,
        default=0.8,
        help="Minimum confidence for applying an LLM formula repair patch, default: 0.8.",
    )
    parser.add_argument(
        "--pdf-mode",
        type=str,
        default="auto",
        choices=["auto", "normal", "split"],
        help=(
            "PDF route mode: auto uses the large-PDF threshold, normal keeps the current MinerU path, "
            "split forces the large-PDF split route."
        ),
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
    print(f"formula_clean: {not args.no_formula_cleanup} ({args.formula_cleanup_level})")
    print(f"llm_formula  : {args.use_llm_formula_cleanup} (min_conf={args.llm_formula_min_confidence})")
    print("-" * 50)

    result = MaterialIngestionService().ingest_file(
        file_path=file_path,
        user_id=args.user_id,
        subject=args.subject,
        material_type=args.material_type,
        metadata={
            "pdf_mode": args.pdf_mode,
            "use_llm_formula_cleanup": args.use_llm_formula_cleanup,
            "llm_formula_min_confidence": args.llm_formula_min_confidence,
        },
        use_llm_cleanup=not args.no_llm_cleanup,
        use_formula_cleanup=not args.no_formula_cleanup,
        formula_cleanup_level=args.formula_cleanup_level,
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
