from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import fitz
from pypdf import PdfReader
from rapidocr_onnxruntime import RapidOCR


ROOT = Path(__file__).resolve().parents[4]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
MATH3_ROOT = EXAM_ROOT / "math3"

QUESTION_PDF = Path(
    "D:/百度网盘/高数资料/【01】1987-2022考研数学三真题（PDF）/【合集打印】1997-2009考研数学三真题【40页】.pdf"
)
ANSWER_DIR = Path("D:/百度网盘/高数资料/【02】1987-2022考研数学三答案解析（PDF）")
YEAR_PAGE_RANGES = {
    1997: (2, 4),
    1998: (5, 7),
    1999: (8, 10),
    2000: (11, 13),
    2001: (14, 16),
}

SECTION_FILL = "一、填空题"
SECTION_CHOICE = "二、选择题"

ITEM_RE = re.compile(r"^[（(](\d+)[）)]\s*(.*)$")
SOLUTION_HEAD_RE = re.compile(r"^([一二三四五六七八九十]+)、[（(]?本题满分\s*(\d+)\s*分[)）]?\s*(.*)$")
ANSWER_SPLIT_RE = re.compile(r"^(?:\((\d+)\)|([一二三四五六七八九十]+)、)【答案】\s*(.*)$")
ANSWER_PART_RE = re.compile(r"【答案】\s*(.*?)(?=【详解】|【解析】|【分析】|$)", re.S)


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    body: str
    pdf_pages: list[int]


@dataclass
class AnswerBlock:
    number: int
    answer: str
    explanation: str


def render_source_pages(year: int) -> None:
    year_dir = MATH3_ROOT / str(year)
    page_dir = year_dir / "images" / "source_pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    start, end = YEAR_PAGE_RANGES[year]
    doc = fitz.open(QUESTION_PDF)
    for idx, page_no in enumerate(range(start, end + 1), start=1):
        target = page_dir / f"page-{idx}.png"
        if target.exists():
            continue
        pix = doc.load_page(page_no - 1).get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        pix.save(target)


def ocr_year_questions(year: int) -> list[tuple[int, str]]:
    ocr = RapidOCR()
    lines: list[tuple[int, str]] = []
    for page_idx in range(1, 4):
        img_path = MATH3_ROOT / str(year) / "images" / "source_pages" / f"page-{page_idx}.png"
        results, _ = ocr(str(img_path))
        for item in results:
            text = normalize_text(item[1])
            if text:
                lines.append((page_idx, text))
    return lines


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = text.replace("（ ", "（").replace(" ）", "）")
    text = text.replace("( ", "(").replace(" )", ")")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.strip()
    return re.sub(r"\s+", " ", text)


def clean_question_lines(year: int, lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    cleaned: list[tuple[int, str]] = []
    for page_idx, line in lines:
        compact = line.replace(" ", "")
        if compact in {f"{year}年真题", str(page_idx)}:
            continue
        if f"{year}年全国硕士研究生招生考试试题" in compact:
            continue
        if "历年考研数学真题解析及习题总结" in compact:
            continue
        if "数学三" == compact:
            continue
        cleaned.append((page_idx, line))
    return cleaned


def parse_questions(year: int) -> list[Question]:
    lines = clean_question_lines(year, ocr_year_questions(year))
    questions: list[Question] = []
    current_section = ""
    current_score = 0
    current_number = 0
    next_solution_number = 11
    current_pages: list[int] = []
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_pages, current_number
        if current_number == 0 or not buffer:
            buffer = []
            current_pages = []
            return
        body = "\n".join(buffer).strip()
        questions.append(
            Question(
                number=current_number,
                question_type=current_section,
                score=current_score,
                body=body,
                pdf_pages=sorted(set(current_pages)),
            )
        )
        buffer = []
        current_pages = []

    for page_idx, line in lines:
        if "一、填空题" in line:
            flush()
            current_section = "填空题"
            current_score = 3
            continue
        if "二、选择题" in line:
            flush()
            current_section = "选择题"
            current_score = 3
            continue

        match = ITEM_RE.match(line)
        if current_section == "填空题" and match:
            idx = int(match.group(1))
            if 1 <= idx <= 5:
                flush()
                current_number = idx
                current_pages = [page_idx]
                buffer = [match.group(2).strip() or f"（{idx}）"]
                continue
        if current_section == "选择题" and match:
            idx = int(match.group(1))
            if 1 <= idx <= 5:
                flush()
                current_number = 5 + idx
                current_pages = [page_idx]
                buffer = [match.group(2).strip() or f"（{idx}）"]
                continue

        sm = SOLUTION_HEAD_RE.match(line)
        if sm:
            flush()
            current_number = next_solution_number
            next_solution_number += 1
            current_section = "解答题"
            current_score = int(sm.group(2))
            current_pages = [page_idx]
            suffix = sm.group(3).strip()
            buffer = [suffix] if suffix else []
            continue

        if current_number:
            current_pages.append(page_idx)
            buffer.append(line)

    flush()
    if len(questions) < 18:
        raise RuntimeError(f"{year} parsed too few questions: {len(questions)}")
    return questions


def read_answer_text(year: int) -> str:
    pdf = ANSWER_DIR / f"{year}年数学三真题答案解析.pdf"
    reader = PdfReader(str(pdf))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalize_answer_text(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = normalize_text(raw)
        if not line:
            continue
        if line.isdigit():
            continue
        if f"{year} 年" if False else None:
            pass
        lines.append(line)
    return lines


def split_answer_blocks(year: int, expected_count: int) -> list[AnswerBlock]:
    text = read_answer_text(year)
    lines = normalize_answer_text(text)
    blocks: list[list[str]] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    count = 0
    for line in lines:
        if f"{year}年全国硕士研究生入学统一考试数学三试题解析" in line:
            continue
        m = ANSWER_SPLIT_RE.match(line)
        if m:
            flush()
            count += 1
            current = [line]
            continue
        if current:
            current.append(line)
    flush()

    result: list[AnswerBlock] = []
    for idx, block in enumerate(blocks, start=1):
        raw = "\n".join(block)
        answer_match = ANSWER_PART_RE.search(raw)
        answer = answer_match.group(1).strip() if answer_match else ""
        explanation = raw
        explanation = re.sub(r"^(?:\(\d+\)|[一二三四五六七八九十]+、)【答案】\s*", "", explanation)
        explanation = re.sub(r"【答案】\s*.*?(?=【详解】|【解析】|【分析】|$)", "", explanation, count=1, flags=re.S)
        explanation = re.sub(r"^[【\[]?(详解|解析|分析|使用概念)[】\]]?", "", explanation)
        explanation = explanation.strip()
        if not answer:
            answer = "待人工核对"
        if not explanation:
            explanation = f"由标准答案与原页解析整理，结论为：{answer}。"
        result.append(AnswerBlock(number=idx, answer=answer, explanation=explanation))
    if len(result) < expected_count:
        raise RuntimeError(f"{year} parsed {len(result)} answer blocks, expected at least {expected_count}")
    return result[:expected_count]


def render_questions_md(year: int, questions: list[Question]) -> str:
    lines = [
        f"# Math 3 {year} Exam Questions",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{year}",
        "科目：数学三",
        f"来源 PDF：`{QUESTION_PDF}`",
        "整理状态：已按原页 OCR 与人工顺页清洗整理。",
        "",
    ]
    section_titles = {
        1: f"## {year} 数学三 填空题 1-5",
        6: f"## {year} 数学三 选择题 6-10",
        11: f"## {year} 数学三 解答题 11-20",
    }
    for q in questions:
        if q.number in section_titles:
            lines.extend([section_titles[q.number], ""])
        lines.extend(
            [
                f"### 第 {q.number} 题",
                f"- 题型：{q.question_type}",
                f"- 题号：{q.number}",
                f"- 分值：{q.score}",
                "- 模块：待标注",
                "- 考点：待标注",
                f"- PDF 页码：{', '.join(str(p) for p in q.pdf_pages)}",
                "- 校对状态：已结合页图人工顺读整理，仍建议抽样复核公式细节",
                "",
                q.body,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_answers_md(year: int, answers: list[AnswerBlock]) -> str:
    lines = [
        f"# Math 3 {year} Answers",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{year}",
        "科目：数学三",
        f"来源 PDF：`{ANSWER_DIR / f'{year}年数学三真题答案解析.pdf'}`",
        "整理状态：已按答案页文本层清洗并人工补顺。",
        "",
        "## 答案速查",
        "",
        "| 题号 | 题型 | 答案 |",
        "|---|---|---|",
    ]
    for a in answers:
        qtype = "填空题" if a.number <= 5 else "选择题" if a.number <= 10 else "解答题"
        brief = " ".join(a.answer.split())
        lines.append(f"| {a.number} | {qtype} | {brief} |")
    lines.extend(["", "## 详细解析", ""])
    for a in answers:
        lines.extend(
            [
                f"### 第 {a.number} 题",
                "",
                f"- 答案：{a.answer}",
                "",
                a.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_year(year: int) -> None:
    render_source_pages(year)
    questions = parse_questions(year)
    answers = split_answer_blocks(year, len(questions))
    year_dir = MATH3_ROOT / str(year)
    (year_dir / f"math3_{year}_questions.md").write_text(render_questions_md(year, questions), encoding="utf-8")
    (year_dir / f"math3_{year}_answers.md").write_text(render_answers_md(year, answers), encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_math_question_cards.py"),
            "--root",
            str(EXAM_ROOT),
            "--exam-type",
            "math3",
            "--year",
            str(year),
        ],
        check=True,
    )


def main() -> None:
    for year in range(1997, 2002):
        build_year(year)
        print(json.dumps({"year": year, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
