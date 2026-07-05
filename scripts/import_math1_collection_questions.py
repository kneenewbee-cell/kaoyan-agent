from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
DEFAULT_SOURCE = Path(r"D:\百度网盘\高数资料\【01】1987-2022年数学一真题（PDF）\【合集打印】1987-2009年考研数学一真题【 72页 】.pdf")

YEAR_RE = re.compile(r"((?:19|20)\s*\d\s*\d)\s*年")
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$")
ITEM_RE = re.compile(r"^\s*[（(]\s*(\d{1,2}|I|l)\s*[)）]\s*(.*)$")
SECTION_RE = re.compile(r"^\s*([-+－一二三四五六七八九十]+)、\s*(.*)$")
FULL_WIDTH_SPACES_RE = re.compile(r"[ \t]{2,}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class PageText:
    page_number: int
    year: int
    text: str


@dataclass
class ImportedQuestion:
    number: int
    question_type: str
    score: int | None
    pdf_pages: list[int]
    body: str


def _extract_pdf_pages(pdf_path: Path) -> list[str]:
    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(str(pdf_path)) as doc:
            return [page.extract_text(x_tolerance=1, y_tolerance=3) or "" for page in doc.pages]
    except Exception:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        return [page.extract_text() or "" for page in reader.pages]


def _normalize_year(raw: str) -> int:
    return int(re.sub(r"\s+", "", raw))


def _header_year(text: str) -> int | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:8]:
        if not any(token in line for token in ("真题", "全国", "研究生", "试题")):
            continue
        match = YEAR_RE.search(line)
        if not match:
            continue
        year = _normalize_year(match.group(1))
        if 1987 <= year <= 2009:
            return year
    return None


def assign_pages_to_years(page_texts: list[str]) -> dict[int, list[PageText]]:
    current_year: int | None = None
    grouped: dict[int, list[PageText]] = {}
    for index, text in enumerate(page_texts, start=1):
        detected = _header_year(text)
        if detected is not None:
            current_year = detected
        if current_year is None:
            continue
        if 1987 <= current_year <= 2009:
            grouped.setdefault(current_year, []).append(PageText(index, current_year, text))
    return grouped


def _clean_line(line: str) -> str:
    line = line.strip()
    line = line.replace("\u3000", " ")
    line = line.replace("（ ", "（").replace(" ）", "）")
    return FULL_WIDTH_SPACES_RE.sub(" ", line)


def _is_item_start(line: str) -> bool:
    match = ITEM_RE.match(line)
    if not match:
        return False
    rest = match.group(2).strip()
    return not rest or bool(CJK_RE.search(rest))


def _clean_page_text(page: PageText, year: int) -> list[str]:
    lines: list[str] = []
    for raw_line in page.text.splitlines():
        line = _clean_line(raw_line)
        if not line:
            continue
        if PAGE_FOOTER_RE.match(line):
            continue
        if "历年考研数学真题解析及复习思路" in line:
            continue
        if f"{year}年真题" in line.replace(" ", ""):
            continue
        if f"{year}年全国硕士研究生招生考试试题" in line.replace(" ", ""):
            continue
        if line in {"（试卷I)", "（试卷 I)", "（试卷I）", "（试卷 I）"}:
            continue
        lines.append(line)
    return lines


def _question_type_from_section(title: str) -> str:
    if "选择" in title:
        return "选择题"
    if "填空" in title:
        return "填空题"
    return "解答题"


def _score_from_text(text: str, *, per_item: bool) -> int | None:
    pattern = r"每小题\s*(\d+)\s*分" if per_item else r"满分\s*(\d+)\s*分"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None


def split_questions(pages: list[PageText], year: int) -> list[ImportedQuestion]:
    entries: list[tuple[int, str, int | None, str]] = []
    current_type = "解答题"
    current_score: int | None = None
    current_pages: list[int] = []
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines, current_pages
        body = "\n".join(current_lines).strip()
        if body:
            pages_text = ",".join(str(page) for page in sorted(set(current_pages)))
            entries.append((int(pages_text.split(",")[0]), current_type, current_score, body))
        current_lines = []
        current_pages = []

    for page in pages:
        for line in _clean_page_text(page, year):
            section_match = SECTION_RE.match(line)
            if section_match and ("题" in line or "本题" in line):
                heading_text = line
                # Major headings that announce a group should not become question bodies.
                if "共" in heading_text and "小题" in heading_text:
                    flush()
                    current_type = _question_type_from_section(heading_text)
                    current_score = _score_from_text(heading_text, per_item=True)
                    continue
                flush()
                current_type = _question_type_from_section(heading_text)
                current_score = _score_from_text(heading_text, per_item=False)
                current_lines = [heading_text]
                current_pages = [page.page_number]
                continue

            item_match = ITEM_RE.match(line)
            if item_match:
                flush()
                current_lines = [line]
                current_pages = [page.page_number]
                continue

            if current_lines:
                current_lines.append(line)
                current_pages.append(page.page_number)

    flush()

    questions: list[ImportedQuestion] = []
    for number, (_, question_type, score, body) in enumerate(entries, start=1):
        page_numbers = sorted(
            {
                int(match.group(1))
                for match in re.finditer(r"\[PDF_PAGE:(\d+)\]", body)
            }
        )
        clean_body = re.sub(r"\[PDF_PAGE:\d+\]", "", body).strip()
        if not page_numbers:
            # Preserve the first-page ordering from entries; the exact page is less important than review visibility.
            page_numbers = []
        questions.append(
            ImportedQuestion(
                number=number,
                question_type=question_type,
                score=score,
                pdf_pages=page_numbers,
                body=clean_body,
            )
        )
    return questions


def split_questions_with_pages(pages: list[PageText], year: int) -> list[ImportedQuestion]:
    lines_by_page: list[tuple[int, str]] = []
    for page in pages:
        lines_by_page.extend((page.page_number, line) for line in _clean_page_text(page, year))

    questions: list[ImportedQuestion] = []
    current_type = "解答题"
    current_score: int | None = None
    current_lines: list[str] = []
    current_pages: list[int] = []

    def flush() -> None:
        nonlocal current_lines, current_pages
        body = "\n".join(current_lines).strip()
        is_lonely_section_heading = len(current_lines) == 1 and SECTION_RE.match(current_lines[0])
        if body and not is_lonely_section_heading:
            questions.append(
                ImportedQuestion(
                    number=len(questions) + 1,
                    question_type=current_type,
                    score=current_score,
                    pdf_pages=sorted(set(current_pages)),
                    body=body,
                )
            )
        current_lines = []
        current_pages = []

    for page_number, line in lines_by_page:
        section_match = SECTION_RE.match(line)
        if section_match and ("题" in line or "本题" in line):
            if "共" in line and "小题" in line:
                flush()
                current_type = _question_type_from_section(line)
                current_score = _score_from_text(line, per_item=True)
                continue
            flush()
            current_type = _question_type_from_section(line)
            current_score = _score_from_text(line, per_item=False)
            current_lines = [line]
            current_pages = [page_number]
            continue

        if _is_item_start(line):
            flush()
            current_lines = [line]
            current_pages = [page_number]
            continue

        if current_lines:
            current_lines.append(line)
            current_pages.append(page_number)

    flush()
    return questions


def render_questions_markdown(year: int, questions: list[ImportedQuestion], source_pdf: Path) -> str:
    lines = [
        f"# Math 1 {year} Exam Questions",
        "",
        "资料类型：考研数学一历年真题  ",
        f"年份：{year}  ",
        "科目：数学一  ",
        f"来源 PDF：`{source_pdf}`  ",
        "整理状态：PDF文本层自动整理，待复核  ",
        "",
        "说明：本文件由 1987-2009 数学一真题合集 PDF 的文本层自动拆分生成；早年 PDF 公式和表格可能存在识别噪声，后续应对照原 PDF/截图复核。",
        "",
        f"## {year} 数一原卷题目",
        "",
    ]
    for question in questions:
        lines.extend(
            [
                f"### 第 {question.number} 题",
                "",
                f"- 题型：{question.question_type}",
                f"- 题号：{question.number}",
                f"- 分值：{question.score if question.score is not None else '待复核'}",
                "- 模块：待标注",
                "- 考点：待标注",
                f"- PDF 页码：{', '.join(str(page) for page in question.pdf_pages) or '待复核'}",
                "- 校对状态：PDF文本层自动整理，待复核",
                "",
                "题干：",
                "",
                question.body,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def import_questions(source_pdf: Path, root: Path, years: list[int], overwrite: bool = False) -> dict[int, int]:
    pages = _extract_pdf_pages(source_pdf)
    grouped = assign_pages_to_years(pages)
    counts: dict[int, int] = {}
    for year in years:
        year_pages = grouped.get(year, [])
        if not year_pages:
            raise RuntimeError(f"No pages found for {year} in {source_pdf}")
        year_dir = root / "math1" / str(year)
        target = year_dir / f"math1_{year}_questions.md"
        if target.exists() and not overwrite:
            continue
        questions = split_questions_with_pages(year_pages, year)
        if not questions:
            raise RuntimeError(f"No questions split for {year}")
        year_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(render_questions_markdown(year, questions, source_pdf), encoding="utf-8")
        counts[year] = len(questions)
    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import missing Math 1 questions from the 1987-2009 collection PDF.")
    parser.add_argument("--source-pdf", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    parser.add_argument("--from-year", type=int, default=1987)
    parser.add_argument("--to-year", type=int, default=2008)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    years = list(range(args.from_year, args.to_year + 1))
    counts = import_questions(args.source_pdf, args.root, years, args.overwrite)
    for year, count in counts.items():
        print(f"{year}: {count} questions")


if __name__ == "__main__":
    main()
