from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"

EXAM_LABELS = {
    "math1": "数学一",
    "math2": "数学二",
    "math3": "数学三",
}

QUESTION_TYPE_MAP = {
    "选择题": "single_choice",
    "填空题": "fill_blank",
    "解答题": "solution",
    "证明题": "solution",
    "计算题": "solution",
}

QUESTION_METADATA_KEYS = {
    "题型",
    "题号",
    "分值",
    "模块",
    "考点",
    "校对状态",
    "PDF 页码",
    "来源页",
}

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
QUESTION_HEADING_RE = re.compile(r"^第\s*(\d+)\s*题\s*$")
METADATA_RE = re.compile(r"^\s*[-*]\s*([^：:]+)[：:]\s*(.*?)\s*$")
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
TOP_METADATA_RE = re.compile(r"^\s*([^：:]+)[：:]\s*(.*?)\s*$")
INCOMPLETE_ANSWER_RE = re.compile(r"待|暂未|未录入|补全|待校对|待视觉|待从")
EXPLANATION_SECTION_TITLES = {"详细解析", "答案解析", "解析", "详解"}
ANSWER_SECTION_TITLES = {"选择题", "填空题", "解答题"}
ANSWER_LINE_RE = re.compile(r"^\s*[-*]?\s*(?:答案|标准答案|解)\s*[：:].*$")


@dataclass
class ImageRef:
    alt: str
    target: str


@dataclass
class QuestionBlock:
    number: int
    heading: str
    metadata: dict[str, str]
    body: str
    group_images: list[ImageRef]
    direct_images: list[ImageRef]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def _exam_id(exam_type: str, year: int) -> str:
    return f"kaoyan_{exam_type}_{year}"


def _question_id(exam_type: str, year: int, number: int) -> str:
    return f"{_exam_id(exam_type, year)}_q{number:03d}"


def _question_file_name(number: int) -> str:
    return f"q{number:03d}.md"


def _normalize_question_type(raw: str | None) -> str:
    return QUESTION_TYPE_MAP.get((raw or "").strip(), "unknown")


def _normalize_review_status(raw: str | None) -> str:
    value = (raw or "").strip()
    if not value:
        return "unknown"
    if any(token in value for token in ("已校对", "用户确认", "确认无误")):
        return "confirmed"
    if any(token in value for token in ("待", "需", "根据截图整理", "人工视觉识别")):
        return "needs_review"
    return "unknown"


def _answer_status(answer: str | None, answer_review_status: str | None) -> str:
    if not answer:
        return "missing"
    if INCOMPLETE_ANSWER_RE.search(answer):
        return "incomplete"
    return _normalize_review_status(answer_review_status) if answer_review_status else "available"


def _explanation_status(explanation: str | None) -> str:
    if not explanation:
        return "missing"
    if INCOMPLETE_ANSWER_RE.search(explanation):
        return "incomplete"
    return "available"


def _split_topics(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in re.split(r"[、，,;；]", raw) if part.strip()]


def _parse_int(raw: str | None) -> int | None:
    if raw is None:
        return None
    match = re.search(r"\d+", raw)
    return int(match.group(0)) if match else None


def _extract_image_refs(text: str) -> list[ImageRef]:
    return [ImageRef(match.group(1).strip(), match.group(2).strip()) for match in IMAGE_RE.finditer(text)]


def _unique_images(images: list[ImageRef]) -> list[ImageRef]:
    seen: set[str] = set()
    result: list[ImageRef] = []
    for image in images:
        key = image.target
        if key in seen:
            continue
        seen.add(key)
        result.append(image)
    return result


def _card_link_target(target: str) -> str:
    if target.startswith(("http://", "https://", "data:", "/", "../")):
        return target
    return f"../{target}"


def _rewrite_image_links_for_card(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        target = match.group(2)
        return f"![{alt}]({_card_link_target(target)})"

    return IMAGE_RE.sub(replace, text)


def _clean_question_body(block_lines: list[str]) -> str:
    kept: list[str] = []
    for index, line in enumerate(block_lines):
        if index == 0 and line.strip().startswith("###"):
            continue
        metadata_match = METADATA_RE.match(line)
        if metadata_match and metadata_match.group(1).strip() in QUESTION_METADATA_KEYS:
            continue
        kept.append(line.rstrip())

    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    return _rewrite_image_links_for_card("\n".join(kept).strip())


def _parse_question_metadata(block_lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in block_lines:
        match = METADATA_RE.match(line)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip()
        metadata[key] = value
    return metadata


def extract_top_metadata(markdown: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in markdown.splitlines():
        if line.startswith("## "):
            break
        match = TOP_METADATA_RE.match(line)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip()
        if key and value:
            metadata[key] = value
    return metadata


def extract_question_blocks(markdown: str) -> list[QuestionBlock]:
    lines = markdown.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))

    questions: list[QuestionBlock] = []
    for position, (start, level, title) in enumerate(headings):
        if level != 3:
            continue
        question_match = QUESTION_HEADING_RE.match(title)
        if not question_match:
            continue

        end = len(lines)
        for next_start, next_level, _ in headings[position + 1 :]:
            if next_level <= 3:
                end = next_start
                break

        group_start = None
        for previous_start, previous_level, _ in reversed(headings[:position]):
            if previous_level == 2:
                group_start = previous_start
                break
        group_text = ""
        if group_start is not None:
            group_end = start
            for next_start, next_level, _ in headings:
                if next_start <= group_start:
                    continue
                if next_level <= 3:
                    group_end = next_start
                    break
            group_text = "\n".join(lines[group_start:group_end])
        block_lines = lines[start:end]
        block_text = "\n".join(block_lines)

        questions.append(
            QuestionBlock(
                number=int(question_match.group(1)),
                heading=title,
                metadata=_parse_question_metadata(block_lines),
                body=_clean_question_body(block_lines),
                group_images=_extract_image_refs(group_text),
                direct_images=_extract_image_refs(block_text),
            )
        )

    questions.sort(key=lambda item: item.number)
    return questions


def extract_answers(markdown: str) -> dict[int, str]:
    answers: dict[int, str] = {}
    in_answer_section = False
    for line in markdown.splitlines():
        heading = HEADING_RE.match(line)
        if heading and len(heading.group(1)) == 2:
            in_answer_section = heading.group(2).strip() in ANSWER_SECTION_TITLES
            continue
        if not in_answer_section or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0].isdigit():
            continue
        answers.setdefault(int(cells[0]), cells[1])
    return answers


def _clean_explanation_lines(lines: list[str]) -> str:
    kept = [line.rstrip() for line in lines]
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and ANSWER_LINE_RE.match(kept[0]):
        kept.pop(0)
        while kept and not kept[0].strip():
            kept.pop(0)
    while kept and kept[0].strip() in {"解析：", "解析:"}:
        kept.pop(0)
        while kept and not kept[0].strip():
            kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept).strip()


def extract_explanations(markdown: str) -> dict[int, str]:
    explanations: dict[int, str] = {}
    in_explanation_section = False
    current_number: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_lines
        if current_number is None:
            return
        cleaned = _clean_explanation_lines(current_lines)
        if cleaned:
            explanations[current_number] = cleaned
        current_number = None
        current_lines = []

    for line in markdown.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if level == 2:
                flush()
                in_explanation_section = title in EXPLANATION_SECTION_TITLES
                continue
            if in_explanation_section and level == 3:
                question_match = QUESTION_HEADING_RE.match(title)
                if question_match:
                    flush()
                    current_number = int(question_match.group(1))
                    continue
        if in_explanation_section and current_number is not None:
            current_lines.append(line)

    flush()
    return explanations


def _frontmatter_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    lines = [f"{key}:"]
    lines.extend(f"  - {value}" for value in values)
    return lines


def _render_related_images(images: list[ImageRef]) -> str:
    if not images:
        return ""
    lines = ["## 相关图片", ""]
    for image in images:
        alt = image.alt or Path(image.target).name
        lines.append(f"![{alt}]({_card_link_target(image.target)})")
        lines.append("")
    return "\n".join(lines).strip()


def render_question_card(
    *,
    exam_type: str,
    year: int,
    question: QuestionBlock,
    answer: str | None,
    explanation: str | None,
    answer_review_status: str | None,
    source_file: str,
    answer_source_file: str,
) -> tuple[str, dict[str, Any]]:
    metadata = question.metadata
    question_type = _normalize_question_type(metadata.get("题型"))
    topics = _split_topics(metadata.get("考点"))
    score = _parse_int(metadata.get("分值"))
    review_status = _normalize_review_status(metadata.get("校对状态"))
    answer_status = _answer_status(answer, answer_review_status)
    explanation_status = _explanation_status(explanation)
    all_images = _unique_images([*question.group_images, *question.direct_images])
    direct_targets = {image.target for image in question.direct_images}
    context_images = [image for image in question.group_images if image.target not in direct_targets]
    qid = _question_id(exam_type, year, question.number)
    exam_id = _exam_id(exam_type, year)
    assets = [image.target for image in all_images]

    frontmatter: list[str] = [
        "---",
        f"question_id: {qid}",
        f"exam_id: {exam_id}",
        f"exam_type: {exam_type}",
        f"year: {year}",
        f"question_number: {question.number}",
        f"question_type: {question_type}",
        f"score: {score if score is not None else 'unknown'}",
        f"module: {metadata.get('模块') or 'unknown'}",
        *_frontmatter_list("topics", topics),
        "difficulty: unknown",
        f"review_status: {review_status}",
        f"answer_status: {answer_status}",
        f"explanation_status: {explanation_status}",
        f"source_file: {source_file}",
        f"answer_source_file: {answer_source_file}",
        *_frontmatter_list("assets", assets),
        "---",
    ]

    sections = [
        f"# {year} {EXAM_LABELS.get(exam_type, exam_type)}第 {question.number} 题",
        _render_related_images(context_images),
        "## 题目\n\n" + (question.body or "（题面暂未录入）"),
        "## 标准答案\n\n" + (answer or "暂未录入"),
        "## 解析\n\n" + (explanation or "暂未录入"),
        (
            "## 来源\n\n"
            f"- 题目来源：`{source_file}`\n"
            f"- 答案来源：`{answer_source_file}`"
        ),
    ]
    text = "\n\n".join(section for section in sections if section).strip() + "\n"
    index_row = {
        "question_id": qid,
        "exam_id": exam_id,
        "exam_type": exam_type,
        "year": year,
        "question_number": question.number,
        "question_type": question_type,
        "score": score,
        "module": metadata.get("模块") or "unknown",
        "topics": topics,
        "difficulty": "unknown",
        "review_status": review_status,
        "answer_status": answer_status,
        "explanation_status": explanation_status,
        "source_file": source_file,
        "answer_source_file": answer_source_file,
        "card_path": f"questions/{_question_file_name(question.number)}",
        "assets": assets,
        "answer": answer,
        "explanation": explanation,
    }
    return "\n".join(frontmatter) + "\n\n" + text, index_row


def build_question_cards(root: Path, exam_type: str, year: int) -> dict[str, Any]:
    year_dir = root / exam_type / str(year)
    question_path = year_dir / f"{exam_type}_{year}_questions.md"
    answer_path = year_dir / f"{exam_type}_{year}_answers.md"
    if not question_path.exists():
        raise FileNotFoundError(f"Question file not found: {question_path}")
    if not answer_path.exists():
        raise FileNotFoundError(f"Answer file not found: {answer_path}")

    question_markdown = _read_text(question_path)
    answer_markdown = _read_text(answer_path)
    answer_metadata = extract_top_metadata(answer_markdown)
    questions = extract_question_blocks(question_markdown)
    answers = extract_answers(answer_markdown)
    explanations = extract_explanations(answer_markdown)
    if not questions:
        raise RuntimeError(f"No questions found in {question_path}")

    card_dir = year_dir / "questions"
    card_dir.mkdir(parents=True, exist_ok=True)
    expected_card_names = {_question_file_name(question.number) for question in questions}
    for stale_card in card_dir.glob("q*.md"):
        if stale_card.name not in expected_card_names:
            stale_card.unlink()

    rows: list[dict[str, Any]] = []
    for question in questions:
        card_text, row = render_question_card(
            exam_type=exam_type,
            year=year,
            question=question,
            answer=answers.get(question.number),
            explanation=explanations.get(question.number),
            answer_review_status=answer_metadata.get("校对状态"),
            source_file=question_path.name,
            answer_source_file=answer_path.name,
        )
        (card_dir / _question_file_name(question.number)).write_text(card_text, encoding="utf-8")
        rows.append(row)

    index_path = year_dir / "questions.jsonl"
    with index_path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": _exam_id(exam_type, year),
        "exam_type": exam_type,
        "exam_label": EXAM_LABELS.get(exam_type, exam_type),
        "year": year,
        "source_files": {
            "questions": question_path.name,
            "answers": answer_path.name,
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(rows),
        "explanation_count": sum(1 for row in rows if row["explanation_status"] == "available"),
        "question_ids": [row["question_id"] for row in rows],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path = year_dir / "paper_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "year_dir": str(year_dir),
        "card_dir": str(card_dir),
        "index_path": str(index_path),
        "manifest_path": str(manifest_path),
        "question_count": len(rows),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build per-question Markdown cards for math exam papers.")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT, help="Root directory of exam_papers")
    parser.add_argument("--exam-type", default="math1", choices=sorted(EXAM_LABELS), help="Exam type")
    parser.add_argument("--year", type=int, required=True, help="Exam year")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_question_cards(args.root, args.exam_type, args.year)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
