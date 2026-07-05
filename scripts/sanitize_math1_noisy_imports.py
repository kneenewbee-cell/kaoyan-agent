from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_math_question_cards import DEFAULT_EXAM_ROOT, extract_answers
from import_math1_collection_questions import (
    DEFAULT_SOURCE,
    _extract_pdf_pages,
    assign_pages_to_years,
    split_questions_with_pages,
)
from import_math_answer_solutions import DEFAULT_SOURCE_DIR, find_pdf_for_year


DETAIL_HEADING = "## 详细解析"


def _question_count(question_path: Path) -> int:
    if not question_path.exists():
        return 0
    return question_path.read_text(encoding="utf-8").count("### 第")


def _without_detail(markdown: str) -> str:
    marker = f"\n{DETAIL_HEADING}"
    index = markdown.find(marker)
    if index < 0:
        return markdown.rstrip()
    return markdown[:index].rstrip()


def _page_image_name(page: int) -> str:
    return f"page_{page:03d}.png"


def _copy_page_images(render_dir: Path, year_dir: Path, pages: list[int]) -> None:
    image_dir = year_dir / "images" / "source_pages"
    image_dir.mkdir(parents=True, exist_ok=True)
    for page in sorted(set(pages)):
        candidates = [
            render_dir / f"page-{page}.png",
            render_dir / f"page-{page:02d}.png",
            render_dir / f"page-{page:03d}.png",
        ]
        source = next((candidate for candidate in candidates if candidate.exists()), None)
        if source is None:
            continue
        shutil.copyfile(source, image_dir / _page_image_name(page))


def _render_page_links(year: int, pages: list[int]) -> str:
    lines: list[str] = []
    for page in sorted(set(pages)):
        lines.append(f"![{year} 数一原卷 PDF 第 {page} 页](images/source_pages/{_page_image_name(page)})")
    return "\n\n".join(lines)


def sanitize_questions(source_pdf: Path, render_dir: Path, root: Path, from_year: int, to_year: int) -> dict[int, int]:
    pages = _extract_pdf_pages(source_pdf)
    grouped = assign_pages_to_years(pages)
    results: dict[int, int] = {}

    for year in range(from_year, to_year + 1):
        year_pages = grouped.get(year, [])
        if not year_pages:
            continue
        questions = split_questions_with_pages(year_pages, year)
        all_pages = sorted({page for question in questions for page in question.pdf_pages})
        year_dir = root / "math1" / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        _copy_page_images(render_dir, year_dir, all_pages)

        lines = [
            f"# Math 1 {year} Exam Questions",
            "",
            "资料类型：考研数学一历年真题  ",
            f"年份：{year}  ",
            "科目：数学一  ",
            f"来源 PDF：`{source_pdf}`  ",
            "整理状态：已移除乱码文本层，保留原 PDF 页图，待视觉清洗  ",
            "",
            "说明：此前 PDF 文本层抽取存在乱码和公式错位；本文件已撤掉不可靠文本，只保留稳定题号槽位和原 PDF 页图，后续逐题视觉转写时再替换题干正文。",
            "",
            f"## {year} 数一原卷题目",
            "",
        ]
        for question in questions:
            page_text = ", ".join(str(page) for page in question.pdf_pages) or "待复核"
            page_links = _render_page_links(year, question.pdf_pages)
            lines.extend(
                [
                    f"### 第 {question.number} 题",
                    "",
                    f"- 题型：{question.question_type}",
                    f"- 题号：{question.number}",
                    f"- 分值：{question.score if question.score is not None else '待复核'}",
                    "- 模块：待标注",
                    "- 考点：待标注",
                    f"- PDF 页码：{page_text}",
                    "- 校对状态：已移除乱码文本层，待视觉清洗",
                    "",
                    "题干：",
                    "",
                    "本题题面待视觉清洗；为避免污染题库，已移除 PDF 文本层乱码。请以原 PDF 页图为准：",
                    "",
                    page_links or "（原 PDF 页图待生成）",
                    "",
                ]
            )
        (year_dir / f"math1_{year}_questions.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        results[year] = len(questions)
    return results


def _render_placeholder_detail(question_count: int, existing_answers: dict[int, str], source_note: str) -> str:
    lines = [
        DETAIL_HEADING,
        "",
        f"解析来源：{source_note}  ",
        "校对状态：已移除乱码文本层，待视觉清洗  ",
        "",
    ]
    for number in range(1, question_count + 1):
        answer = existing_answers.get(number, "待从答案解析 PDF 视觉清洗")
        lines.extend(
            [
                f"### 第 {number} 题",
                "",
                f"- 答案：{answer}",
                "",
                "待从答案解析 PDF 视觉清洗。",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def reset_answer_file(year_dir: Path, year: int, source_note: str, question_count: int) -> None:
    lines = [
        f"# Math 1 {year} Answers",
        "",
        "资料类型：考研数学一答案解析  ",
        f"年份：{year}  ",
        "科目：数学一  ",
        f"来源 PDF：{source_note}  ",
        "校对状态：已移除乱码文本层，待视觉清洗  ",
        "",
        "## 解答题",
        "",
        "| 题号 | 答案 |",
        "|---|---|",
    ]
    for number in range(1, question_count + 1):
        lines.append(f"| {number} | 待从答案解析 PDF 视觉清洗 |")
    lines.extend(["", _render_placeholder_detail(question_count, {}, source_note), ""])
    (year_dir / f"math1_{year}_answers.md").write_text("\n".join(lines), encoding="utf-8")


def sanitize_answers(root: Path, source_dir: Path, reset_from_year: int, reset_to_year: int, detail_from_year: int, detail_to_year: int) -> None:
    for year in range(reset_from_year, reset_to_year + 1):
        year_dir = root / "math1" / str(year)
        question_count = _question_count(year_dir / f"math1_{year}_questions.md")
        if question_count <= 0:
            continue
        pdf = find_pdf_for_year(source_dir, year)
        source_note = f"`{pdf}`" if pdf else "未找到对应答案解析 PDF"
        reset_answer_file(year_dir, year, source_note, question_count)

    for year in range(detail_from_year, detail_to_year + 1):
        if year == 2011:
            continue
        year_dir = root / "math1" / str(year)
        answer_path = year_dir / f"math1_{year}_answers.md"
        question_count = _question_count(year_dir / f"math1_{year}_questions.md")
        if not answer_path.exists() or question_count <= 0:
            continue
        markdown = answer_path.read_text(encoding="utf-8")
        existing_answers = extract_answers(markdown)
        pdf = find_pdf_for_year(source_dir, year)
        source_note = f"`{pdf}`" if pdf else "未找到对应答案解析 PDF"
        updated = _without_detail(markdown) + "\n\n" + _render_placeholder_detail(question_count, existing_answers, source_note) + "\n"
        answer_path.write_text(updated, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove noisy PDF text-layer imports from Math 1 generated files.")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    parser.add_argument("--question-source-pdf", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--answer-source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--render-dir", type=Path, required=True)
    parser.add_argument("--question-from-year", type=int, default=1987)
    parser.add_argument("--question-to-year", type=int, default=2008)
    parser.add_argument("--reset-answer-from-year", type=int, default=1987)
    parser.add_argument("--reset-answer-to-year", type=int, default=2008)
    parser.add_argument("--sanitize-detail-from-year", type=int, default=2009)
    parser.add_argument("--sanitize-detail-to-year", type=int, default=2022)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    counts = sanitize_questions(
        args.question_source_pdf,
        args.render_dir,
        args.root,
        args.question_from_year,
        args.question_to_year,
    )
    sanitize_answers(
        args.root,
        args.answer_source_dir,
        args.reset_answer_from_year,
        args.reset_answer_to_year,
        args.sanitize_detail_from_year,
        args.sanitize_detail_to_year,
    )
    for year, count in counts.items():
        print(f"{year}: sanitized {count} question slots")


if __name__ == "__main__":
    main()
