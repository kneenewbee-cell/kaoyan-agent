from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"

FORBIDDEN = (
    "待文本精修",
    "needs_text_refinement",
    "source_image_available",
    "见答案解析来源页图",
    "见解析来源页图",
    "所在原卷页",
    "当前使用完整原卷页",
    "PDF 视觉落库版",
    "PDF 页面视觉方式录入",
    "???",
    "????",
    "OCR",
    "A/B/C/D",
    "占位",
    "框架",
    "待补",
    "归档化转写",
)


def parse_years(value: str) -> list[int]:
    years: list[int] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            step = 1 if start <= end else -1
            years.extend(range(start, end + step, step))
        else:
            years.append(int(part))
    return years


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject image-placeholder math exam cards.")
    parser.add_argument("--exam-type", default="math3")
    parser.add_argument("--years", required=True)
    args = parser.parse_args()

    failures: list[str] = []
    for year in parse_years(args.years):
        year_dir = EXAM_ROOT / args.exam_type / str(year)
        if not year_dir.exists():
            failures.append(f"{args.exam_type}/{year}: missing year directory")
            continue
        files = (
            list(year_dir.glob("*.md"))
            + list((year_dir / "questions").glob("q*.md"))
            + [year_dir / "questions.jsonl", year_dir / "paper_manifest.json"]
        )
        for path in files:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in FORBIDDEN:
                if token in text:
                    failures.append(f"{path}: contains forbidden placeholder token {token!r}")
                    break

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print(f"OK: {args.exam_type} years {args.years} contain no image-placeholder tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
