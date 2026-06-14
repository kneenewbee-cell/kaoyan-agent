from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF_GLOB = "2025*高数*主册*.pdf"
DEFAULT_DOWNLOAD_DIR = Path("d:/download")
OUTPUT_DIR = ROOT / "data" / "raw" / "math" / "gaoshu" / "by_year"

YEAR_MARK_RE = re.compile(r"[\[【](?P<year>(?:19|20)\d{2})\s*[，,][^\]】\n]{0,30}[\]】]")
KAODIAN_RE = re.compile(r"考点\s*\d+\s+([^\n]+)")


@dataclass
class Question:
    year: str
    source_label: str
    topic: str
    page: int
    content: str


def main() -> None:
    pdf_path = find_pdf()
    questions = extract_questions(pdf_path)
    write_by_year(questions, pdf_path)
    print(f"PDF: {pdf_path}")
    print(f"Extracted questions: {len(questions)}")
    print(f"Output dir: {OUTPUT_DIR}")
    for year, count in sorted(count_by_year(questions).items()):
        print(f"{year}: {count}")


def find_pdf() -> Path:
    matches = sorted(DEFAULT_DOWNLOAD_DIR.glob(DEFAULT_PDF_GLOB))
    if not matches:
        raise SystemExit(f"No PDF matched {DEFAULT_DOWNLOAD_DIR / DEFAULT_PDF_GLOB}")
    return matches[0]


def extract_questions(pdf_path: Path) -> list[Question]:
    reader = PdfReader(str(pdf_path))
    current_topic = "未识别考点"
    pages: list[tuple[int, str, str]] = []

    for page_index, page in enumerate(reader.pages, start=1):
        text = safe_text(page.extract_text() or "")
        topic_match = KAODIAN_RE.search(text)
        if topic_match:
            current_topic = normalize_space(topic_match.group(1))
        pages.append((page_index, current_topic, text))

    questions: list[Question] = []
    for page, topic, text in pages:
        matches = list(YEAR_MARK_RE.finditer(text))
        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            raw = text[start:end]
            content = cleanup_question(raw)
            if is_noise(content):
                continue
            questions.append(
                Question(
                    year=match.group("year"),
                    source_label=normalize_space(match.group(0).strip("[]【】")),
                    topic=topic,
                    page=page,
                    content=content,
                )
            )
    return dedupe_questions(questions)


def cleanup_question(text: str) -> str:
    text = safe_text(text)
    lines = []
    for line in text.splitlines():
        line = normalize_space(line)
        if not line:
            continue
        if line.startswith("B 站："):
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if line.startswith("考点 ") or line.startswith("第一部分") or line.startswith("第二部分") or line.startswith("第三部分"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def is_noise(content: str) -> bool:
    if len(content) < 20:
        return True
    if "考频" in content and "总合计" in content:
        return True
    return False


def dedupe_questions(questions: list[Question]) -> list[Question]:
    seen: set[tuple[str, str]] = set()
    result: list[Question] = []
    for question in questions:
        key = (question.year, normalize_space(question.content[:220]))
        if key in seen:
            continue
        seen.add(key)
        result.append(question)
    return result


def write_by_year(questions: list[Question], pdf_path: Path) -> None:
    grouped: dict[str, list[Question]] = defaultdict(list)
    for question in questions:
        grouped[question.year].append(question)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for year, items in sorted(grouped.items()):
        lines = [
            f"# 数学-高数-{year}年真题整理",
            "",
            "资料来源：用户提供的《2025高数上册（主册）》PDF，经脚本按年份标记自动抽取。",
            "",
            "校对提醒：PDF 文本层会导致部分公式、图形和选项排版失真，入库前建议人工对照原 PDF 校对。",
            "",
        ]
        for number, item in enumerate(items, start=1):
            lines.extend(
                [
                    f"## {year} 真题 {number}",
                    "",
                    f"- 科目：数学",
                    f"- 模块：高数",
                    f"- 年份：{year}",
                    f"- 试卷标签：{item.source_label}",
                    f"- 所属考点：{item.topic}",
                    f"- PDF 页码：{item.page}",
                    "",
                    "题目：",
                    "",
                    item.content,
                    "",
                ]
            )
        (OUTPUT_DIR / f"{year}.md").write_text("\n".join(lines), encoding="utf-8")


def count_by_year(questions: list[Question]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for question in questions:
        counts[question.year] += 1
    return counts


def safe_text(text: str) -> str:
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    main()
