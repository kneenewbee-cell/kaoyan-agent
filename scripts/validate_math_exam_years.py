from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"


REQUIRED_CARD_SECTIONS = ("## 题目", "## 标准答案", "## 解析", "## 来源")


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


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
    return rows


def validate_year(root: Path, exam_type: str, year: int) -> list[str]:
    errors: list[str] = []
    year_dir = root / exam_type / str(year)
    if not year_dir.exists():
        return [f"{exam_type}/{year}: missing year directory"]

    expected_files = [
        year_dir / f"{exam_type}_{year}_questions.md",
        year_dir / f"{exam_type}_{year}_answers.md",
        year_dir / "questions.jsonl",
        year_dir / "paper_manifest.json",
    ]
    for path in expected_files:
        if not path.exists():
            errors.append(f"{exam_type}/{year}: missing {path.name}")

    jsonl_path = year_dir / "questions.jsonl"
    manifest_path = year_dir / "paper_manifest.json"
    if not jsonl_path.exists():
        return errors

    try:
        rows = load_jsonl(jsonl_path)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    if not rows:
        errors.append(f"{exam_type}/{year}: questions.jsonl is empty")

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            expected_count = manifest.get("question_count")
            if expected_count != len(rows):
                errors.append(
                    f"{exam_type}/{year}: manifest question_count={expected_count}, jsonl lines={len(rows)}"
                )
        except json.JSONDecodeError as exc:
            errors.append(f"{exam_type}/{year}: invalid paper_manifest.json: {exc}")

    seen_numbers: set[int] = set()
    for row in rows:
        number = row.get("question_number")
        qid = row.get("question_id")
        card_rel = row.get("card_path")
        answer = str(row.get("answer", "")).strip()
        explanation = str(row.get("explanation", "")).strip()

        if not isinstance(number, int):
            errors.append(f"{exam_type}/{year}: row {qid or '?'} has invalid question_number")
            continue
        if number in seen_numbers:
            errors.append(f"{exam_type}/{year}: duplicated question_number {number}")
        seen_numbers.add(number)

        if not answer:
            errors.append(f"{exam_type}/{year} q{number:03d}: empty answer")
        if not explanation:
            errors.append(f"{exam_type}/{year} q{number:03d}: empty explanation")

        if not card_rel:
            errors.append(f"{exam_type}/{year} q{number:03d}: missing card_path")
            continue
        card_path = year_dir / card_rel
        if not card_path.exists():
            errors.append(f"{exam_type}/{year} q{number:03d}: missing card {card_rel}")
            continue
        card_text = card_path.read_text(encoding="utf-8")
        for section in REQUIRED_CARD_SECTIONS:
            if section not in card_text:
                errors.append(f"{exam_type}/{year} q{number:03d}: missing section {section}")
        if "```text" in card_text:
            errors.append(f"{exam_type}/{year} q{number:03d}: contains ```text formula block")

    if seen_numbers:
        expected_numbers = set(range(1, max(seen_numbers) + 1))
        missing = sorted(expected_numbers - seen_numbers)
        if missing:
            errors.append(f"{exam_type}/{year}: missing question numbers {missing}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated math exam year files.")
    parser.add_argument("--exam-type", default="math3")
    parser.add_argument("--years", required=True, help="Comma-separated years or ranges, e.g. 2022-2010")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    args = parser.parse_args()

    failures: list[str] = []
    for year in parse_years(args.years):
        failures.extend(validate_year(args.root, args.exam_type, year))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print(f"OK: {args.exam_type} years {args.years}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
