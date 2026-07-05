from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
QUESTION_SOURCE_MAP = {
    range(1987, 1997): Path(
        r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\【合集打印】1987-1996考研数学三真题【43页】.pdf"
    ),
    range(1997, 2010): Path(
        r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\【合集打印】1997-2009考研数学三真题【40页】.pdf"
    ),
}
ANSWER_SOURCE_DIR = Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）")

YEAR_RE = re.compile(r"((?:19|20)\s*\d\s*\d)\s*年")
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$")
ITEM_RE = re.compile(r"^\s*[（(]\s*(\d{1,2}|I|l)\s*[)）]\s*(.*)$")
SECTION_RE = re.compile(r"^\s*([一二三四五六七八九十]+)[、.．]\s*(.*)$")
QUESTION_HEADING_RE = re.compile(r"^###\s*第\s*(\d+)\s*题\s*$")
ANSWER_HEADING_RE = re.compile(r"^###\s*第\s*(\d+)\s*题\s*$")
ANSWER_RE = re.compile(r"【答案】\s*(.*?)(?=【解析】|【详解】|【分析】|解[:：]|$)")


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


@dataclass
class SolutionBlock:
    number: int
    answer: str
    explanation: str


def _question_pdf_for_year(year: int) -> Path:
    for years, path in QUESTION_SOURCE_MAP.items():
        if year in years:
            return path
    raise ValueError(f"Unsupported year: {year}")


def _extract_question_pages(pdf_path: Path) -> list[str]:
    import pdfplumber  # type: ignore

    with pdfplumber.open(str(pdf_path)) as doc:
        return [page.extract_text(x_tolerance=1, y_tolerance=3) or "" for page in doc.pages]


def _extract_answer_text(pdf_path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


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
        grouped.setdefault(current_year, []).append(PageText(index, current_year, text))
    return grouped


def _clean_line(line: str) -> str:
    line = line.strip()
    line = line.replace("\u3000", " ")
    line = line.replace("•", "·")
    return re.sub(r"[ \t]{2,}", " ", line)


def _is_question_noise(line: str, year: int) -> bool:
    compact = line.replace(" ", "")
    if not line:
        return True
    if PAGE_FOOTER_RE.match(line):
        return True
    if "更多考研精品资料" in line or "光速考研工作室" in line:
        return True
    if f"{year}年真题" in compact:
        return True
    if f"{year}年全国硕士研究生招生考试试题" in compact:
        return True
    if compact in {"（试卷IV）", "（试卷V）", "（试卷N)", "（试卷N）"}:
        return True
    return False


def _clean_question_page(page: PageText, year: int) -> list[str]:
    return [
        line
        for raw_line in page.text.splitlines()
        if not _is_question_noise((line := _clean_line(raw_line)), year)
    ]


def _question_type_from_section(title: str) -> str:
    if "选择" in title:
        return "选择题"
    if "填空" in title:
        return "填空题"
    if "判断" in title:
        return "判断题"
    return "解答题"


def _score_from_text(text: str, *, per_item: bool) -> int | None:
    pattern = r"每小题\s*(\d+)\s*分" if per_item else r"满分\s*(\d+)\s*分"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None


def _is_item_start(line: str) -> bool:
    match = ITEM_RE.match(line)
    if not match:
        return False
    rest = match.group(2).strip()
    return not rest or any("\u4e00" <= ch <= "\u9fff" for ch in rest)


def split_questions_with_pages(pages: list[PageText], year: int) -> list[ImportedQuestion]:
    lines_by_page: list[tuple[int, str]] = []
    for page in pages:
        lines_by_page.extend((page.page_number, line) for line in _clean_question_page(page, year))

    questions: list[ImportedQuestion] = []
    current_type = "解答题"
    current_score: int | None = None
    current_lines: list[str] = []
    current_pages: list[int] = []

    def flush() -> None:
        nonlocal current_lines, current_pages
        body = "\n".join(current_lines).strip()
        is_lonely_heading = len(current_lines) == 1 and SECTION_RE.match(current_lines[0])
        if body and not is_lonely_heading:
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


def find_answer_pdf(year: int) -> Path | None:
    matches = sorted(path for path in ANSWER_SOURCE_DIR.glob("*.pdf") if str(year) in path.name)
    return matches[0] if matches else None


def _answer_region(text: str) -> str:
    markers = ["参考解答及评分标准", "答案解析", "试题解析"]
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    return text[min(positions) :] if positions else text


def _is_answer_noise(line: str) -> bool:
    if not line or PAGE_FOOTER_RE.match(line):
        return True
    return "更多考研精品资料" in line or "光速考研工作室" in line


def _looks_like_section_heading(line: str) -> bool:
    match = SECTION_RE.match(line)
    if not match:
        return False
    title = match.group(2)
    return any(token in title for token in ("填空", "选择", "判断", "解答", "本题"))


def _is_group_section(line: str) -> bool:
    return "共" in line or "每小题" in line or "填空" in line or "选择" in line or "判断" in line


def _is_problem_section(line: str) -> bool:
    return bool(_looks_like_section_heading(line) and not _is_group_section(line))


def split_solution_blocks(text: str, question_count: int | None = None) -> list[SolutionBlock]:
    lines = [_clean_line(line) for line in _answer_region(text).splitlines()]
    blocks: list[list[str]] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    for line in lines:
        if _is_answer_noise(line):
            continue
        if _is_group_section(line) and _looks_like_section_heading(line):
            continue
        if _is_problem_section(line):
            flush()
            current = [line]
            continue
        if _is_item_start(line):
            flush()
            current = [line]
            continue
        if current:
            current.append(line)

    flush()

    result: list[SolutionBlock] = []
    for block_lines in blocks:
        raw = "\n".join(block_lines).strip()
        if not raw:
            continue
        result.append(
            SolutionBlock(
                number=len(result) + 1,
                answer=_extract_answer(raw),
                explanation=_clean_explanation(raw),
            )
        )
        if question_count and len(result) >= question_count:
            break
    return result


def _extract_answer(raw: str) -> str:
    one_line = re.sub(r"\s+", " ", raw)
    match = ANSWER_RE.search(one_line)
    if match:
        answer = match.group(1).strip(" 。；;")
        if answer:
            return answer
    first_line = raw.splitlines()[0]
    first_line = ITEM_RE.sub("", first_line).strip()
    if "【答案】" in first_line:
        return first_line.split("【答案】", 1)[1].strip() or "见解析"
    if "答案" in first_line and len(first_line) <= 80:
        return first_line
    return "见解析"


def _clean_explanation(raw: str) -> str:
    lines = [_clean_line(line) for line in raw.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    if lines:
        lines[0] = ITEM_RE.sub("", lines[0]).strip()
    return "\n".join(line for line in lines if line).strip()


def _render_questions_markdown(year: int, questions: list[ImportedQuestion], source_pdf: Path) -> str:
    lines = [
        f"# {year} 年数学三真题",
        "",
        "资料类型：考研数学三历年真题  ",
        f"年份：{year}  ",
        "科目：数学三  ",
        f"来源 PDF：`{source_pdf}`  ",
        "整理状态：按 PDF 文本骨架清洗并转为正式题卡格式，待抽样复核  ",
        "",
    ]
    for question in questions:
        lines.extend(
            [
                f"### 第{question.number}题",
                f"- 题型：{question.question_type}",
                f"- 题号：{question.number}",
                f"- 分值：{question.score if question.score is not None else '待复核'}",
                "- 模块：待标注",
                "- 考点：待标注",
                f"- PDF 页码：{', '.join(str(page) for page in question.pdf_pages) or '待复核'}",
                "- 校对状态：初整理，待抽样复核",
                "",
                question.body,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_answers_markdown(year: int, blocks: list[SolutionBlock], source_pdf: Path) -> str:
    lines = [
        f"# {year} 年数学三答案解析",
        "",
        "资料类型：考研数学三答案解析  ",
        f"年份：{year}  ",
        "科目：数学三  ",
        f"来源 PDF：`{source_pdf}`  ",
        "整理状态：按答案 PDF 文本骨架清洗并转为正式题卡格式，待抽样复核  ",
        "",
        "## 答案速查",
        "",
        "| 题号 | 答案 |",
        "|---|---|",
    ]
    for block in blocks:
        brief = " ".join(block.answer.split())
        if len(brief) > 48:
            brief = "见详细解析"
        lines.append(f"| {block.number} | {brief} |")
    lines.extend(["", "## 详细解析", ""])
    for block in blocks:
        lines.extend(
            [
                f"### 第{block.number}题",
                "",
                f"- 答案：{block.answer}",
                "",
                block.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def import_year(root: Path, year: int, overwrite: bool = False, build_cards: bool = False) -> tuple[int, int]:
    question_pdf = _question_pdf_for_year(year)
    question_pages = assign_pages_to_years(_extract_question_pages(question_pdf)).get(year, [])
    if not question_pages:
        raise RuntimeError(f"No question pages found for {year}")

    questions = split_questions_with_pages(question_pages, year)
    if not questions:
        raise RuntimeError(f"No questions extracted for {year}")

    answer_pdf = find_answer_pdf(year)
    if answer_pdf is None:
        raise FileNotFoundError(f"No answer PDF found for {year}")
    blocks = split_solution_blocks(_extract_answer_text(answer_pdf), question_count=len(questions))
    while len(blocks) < len(questions):
        number = len(blocks) + 1
        blocks.append(SolutionBlock(number, "见解析", "待补录"))

    year_dir = root / "math3" / str(year)
    question_md = year_dir / f"math3_{year}_questions.md"
    answer_md = year_dir / f"math3_{year}_answers.md"
    if year_dir.exists() and not overwrite and question_md.exists() and answer_md.exists():
        return year, len(questions)

    year_dir.mkdir(parents=True, exist_ok=True)
    question_md.write_text(_render_questions_markdown(year, questions, question_pdf), encoding="utf-8")
    answer_md.write_text(_render_answers_markdown(year, blocks, answer_pdf), encoding="utf-8")

    if build_cards:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_math_question_cards.py"),
                "--root",
                str(root),
                "--exam-type",
                "math3",
                "--year",
                str(year),
            ],
            check=True,
        )
    return year, len(questions)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import math3 1987-2005 legacy exam papers.")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    parser.add_argument("--from-year", type=int, default=1987)
    parser.add_argument("--to-year", type=int, default=2005)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--build-cards", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for year in range(args.from_year, args.to_year + 1):
        imported_year, count = import_year(args.root, year, overwrite=args.overwrite, build_cards=args.build_cards)
        print(f"{imported_year}: {count} questions")


if __name__ == "__main__":
    main()
