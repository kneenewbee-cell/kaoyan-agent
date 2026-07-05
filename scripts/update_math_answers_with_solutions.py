from __future__ import annotations

import argparse
from pathlib import Path

from import_math_answer_solutions import (  # type: ignore
    DEFAULT_SOURCE_DIR,
    SolutionBlock,
    _extract_pdf_text,
    _placeholder_blocks,
    find_pdf_for_year,
    split_solution_blocks,
)
from build_math_question_cards import DEFAULT_EXAM_ROOT, extract_answers


DETAIL_HEADING = "## 详细解析"


def _question_count(year_dir: Path, exam_type: str, year: int) -> int:
    question_path = year_dir / f"{exam_type}_{year}_questions.md"
    if not question_path.exists():
        return 0
    return question_path.read_text(encoding="utf-8").count("### 第")


def _without_detail_section(markdown: str) -> str:
    marker = f"\n{DETAIL_HEADING}"
    index = markdown.find(marker)
    if index < 0:
        return markdown.rstrip()
    return markdown[:index].rstrip()


def _answer_for_block(existing_answers: dict[int, str], block: SolutionBlock) -> str:
    if block.answer in {"见解析", "待从答案解析 PDF 视觉清洗"}:
        return existing_answers.get(block.number, block.answer)
    return block.answer


def _render_detail_section(blocks: list[SolutionBlock], existing_answers: dict[int, str], source_note: str) -> str:
    lines = [
        DETAIL_HEADING,
        "",
        f"解析来源：{source_note}  ",
        "校对状态：自动整理，待复核  ",
        "",
    ]
    for block in blocks:
        answer = _answer_for_block(existing_answers, block)
        lines.extend(
            [
                f"### 第 {block.number} 题",
                "",
                f"- 答案：{answer}",
                "",
                block.explanation or "待复核",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def update_year(root: Path, source_dir: Path, exam_type: str, year: int, overwrite_detail: bool = False) -> tuple[int, str, int]:
    year_dir = root / exam_type / str(year)
    answer_path = year_dir / f"{exam_type}_{year}_answers.md"
    if not answer_path.exists():
        return year, "missing_answer_file", 0
    markdown = answer_path.read_text(encoding="utf-8")
    if DETAIL_HEADING in markdown and not overwrite_detail:
        return year, "has_detail", 0

    question_count = _question_count(year_dir, exam_type, year)
    if question_count <= 0:
        return year, "missing_questions", 0

    pdf_path = find_pdf_for_year(source_dir, year)
    source_note: str
    if pdf_path is None:
        blocks = _placeholder_blocks(question_count)
        source_note = "未找到对应答案解析 PDF，待补源文件"
        real_count = 0
    elif any(token in pdf_path.name for token in ("暂无详细解析", "速查版", "答案速查")):
        blocks = _placeholder_blocks(question_count)
        source_note = f"`{pdf_path}`（源文件为速查版或暂无详细解析，待补详细解析源）"
        real_count = 0
    else:
        text = _extract_pdf_text(pdf_path)
        blocks = split_solution_blocks(text, max_blocks=question_count)
        real_count = len(blocks)
        if len(blocks) < question_count:
            blocks.extend(_placeholder_blocks(question_count - len(blocks), start=len(blocks) + 1))
        source_note = f"`{pdf_path}`"

    existing_answers = extract_answers(markdown)
    updated = _without_detail_section(markdown) + "\n\n" + _render_detail_section(blocks, existing_answers, source_note) + "\n"
    answer_path.write_text(updated, encoding="utf-8")
    if real_count == 0:
        return year, "needs_visual", 0
    if real_count < question_count:
        return year, "partial", real_count
    return year, "ok", real_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append/replace detailed solutions in existing math answer markdown files.")
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--exam-type", default="math1")
    parser.add_argument("--from-year", type=int, required=True)
    parser.add_argument("--to-year", type=int, required=True)
    parser.add_argument("--overwrite-detail", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for year in range(args.from_year, args.to_year + 1):
        result = update_year(args.root, args.source_dir, args.exam_type, year, args.overwrite_detail)
        print(f"{result[0]}: {result[1]} ({result[2]} real blocks)")


if __name__ == "__main__":
    main()
