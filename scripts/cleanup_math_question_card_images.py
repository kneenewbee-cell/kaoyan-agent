from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"

CARD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SHARED_IMAGE_NAME_RE = re.compile(r"q\d{2,3}-q\d{2,3}\.png$", re.IGNORECASE)
QUESTION_NUMBER_RE = re.compile(r"q(\d{3})\.md$", re.IGNORECASE)


def _is_banned_asset(target: str) -> bool:
    normalized = target.replace("\\", "/")
    name = normalized.rsplit("/", 1)[-1]
    return "source_pages/" in normalized or bool(SHARED_IMAGE_NAME_RE.search(name))


def _parse_frontmatter(text: str) -> tuple[list[str] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    frontmatter = text[4:end].splitlines()
    body = text[end + 5 :]
    return frontmatter, body


def _serialize_frontmatter(lines: list[str] | None) -> str:
    if lines is None:
        return ""
    return "---\n" + "\n".join(lines).rstrip() + "\n---\n"


def _clean_frontmatter(lines: list[str] | None) -> tuple[list[str] | None, list[str]]:
    if lines is None:
        return None, []

    cleaned: list[str] = []
    removed: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() != "assets:":
            cleaned.append(line)
            index += 1
            continue

        index += 1
        kept_assets: list[str] = []
        while index < len(lines):
            asset_line = lines[index]
            if not asset_line.startswith("  - "):
                break
            asset = asset_line[4:].strip()
            if _is_banned_asset(asset):
                removed.append(asset)
            else:
                kept_assets.append(asset)
            index += 1

        if kept_assets:
            cleaned.append(line)
            for asset in kept_assets:
                cleaned.append(f"  - {asset}")

    return cleaned, removed


def _strip_banned_images(body: str) -> tuple[str, list[str]]:
    removed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if _is_banned_asset(target):
            removed.append(target)
            return ""
        return match.group(0)

    updated = CARD_IMAGE_RE.sub(replace, body)
    lines = updated.splitlines()
    cleaned_lines: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped == "## 相关图片":
            lookahead = index + 1
            has_kept_content = False
            while lookahead < len(lines):
                candidate = lines[lookahead].strip()
                if candidate.startswith("## "):
                    break
                if candidate:
                    has_kept_content = True
                    break
                lookahead += 1
            if not has_kept_content:
                index = lookahead
                continue
        if stripped or (cleaned_lines and cleaned_lines[-1].strip()):
            cleaned_lines.append(line.rstrip())
        index += 1

    cleaned_text = "\n".join(cleaned_lines).strip() + "\n"
    return cleaned_text, removed


def _question_number_from_card(path: Path) -> int | None:
    match = QUESTION_NUMBER_RE.search(path.name)
    return int(match.group(1)) if match else None


def clean_year(year_dir: Path) -> dict[str, object] | None:
    question_dir = year_dir / "questions"
    index_path = year_dir / "questions.jsonl"
    if not question_dir.exists() or not index_path.exists():
        return None

    card_updates: dict[str, list[str]] = {}
    for card_path in sorted(question_dir.glob("q*.md")):
        original = card_path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        frontmatter, body = _parse_frontmatter(original)
        cleaned_frontmatter, removed_frontmatter = _clean_frontmatter(frontmatter)
        cleaned_body, removed_body = _strip_banned_images(body)
        updated = _serialize_frontmatter(cleaned_frontmatter) + cleaned_body
        removed = list(dict.fromkeys(removed_frontmatter + removed_body))
        if updated != original:
            card_path.write_text(updated, encoding="utf-8")
            card_updates[card_path.name] = removed

    jsonl_updates: list[int] = []
    rows: list[str] = []
    for raw_line in index_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        row = json.loads(raw_line)
        assets = row.get("assets", [])
        filtered_assets = [asset for asset in assets if not _is_banned_asset(asset)]
        if filtered_assets != assets:
            row["assets"] = filtered_assets
            number = row.get("question_number")
            if isinstance(number, int):
                jsonl_updates.append(number)
        rows.append(json.dumps(row, ensure_ascii=False))

    if jsonl_updates:
        index_path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    if not card_updates and not jsonl_updates:
        return None

    modified_numbers = sorted(
        {
            number
            for number in (
                [_question_number_from_card(question_dir / name) for name in card_updates]
                + jsonl_updates
            )
            if number is not None
        }
    )
    return {
        "year": int(year_dir.name),
        "modified_questions": modified_numbers,
        "modified_cards": len(card_updates),
        "modified_jsonl_rows": len(set(jsonl_updates)),
        "removed_assets_by_card": card_updates,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove full-page/shared image references from per-question markdown cards."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT / "math1")
    parser.add_argument("--from-year", type=int, default=1987)
    parser.add_argument("--to-year", type=int, default=2025)
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_EXAM_ROOT / "math1" / "math1_question_image_cleanup_report.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports: list[dict[str, object]] = []
    for year in range(args.from_year, args.to_year + 1):
        year_dir = args.root / str(year)
        if not year_dir.exists():
            continue
        report = clean_year(year_dir)
        if report:
            reports.append(report)

    summary = {
        "from_year": args.from_year,
        "to_year": args.to_year,
        "year_count": len(reports),
        "question_count": sum(len(item["modified_questions"]) for item in reports),
        "years": reports,
    }
    args.report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
