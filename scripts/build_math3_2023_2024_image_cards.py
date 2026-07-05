from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3"


SOURCE_PAGE_MAP = {
    2023: {
        range(1, 6): "page-1.png",
        range(6, 11): "page-2.png",
        range(11, 18): "page-3.png",
        range(18, 23): "page-4.png",
    },
    2024: {
        range(1, 12): "page-1.png",
        range(12, 21): "page-2.png",
        range(21, 23): "page-3.png",
    },
}


def source_page_name(year: int, number: int) -> str:
    for numbers, page in SOURCE_PAGE_MAP[year].items():
        if number in numbers:
            return page
    raise ValueError(f"no source page mapping for {year} q{number}")


def qtype(number: int) -> str:
    if number <= 10:
        return "single_choice"
    if number <= 16:
        return "fill_blank"
    return "solution"


def score_for(number: int) -> int:
    if number <= 16:
        return 5
    if number == 17:
        return 10
    return 12


def module_for(number: int) -> str:
    if number in {6, 7, 8, 9, 10, 14, 20, 21}:
        return "线性代数"
    if number in {11, 15, 16, 22}:
        return "概率统计"
    return "高等数学"


def question_id(year: int, number: int) -> str:
    return f"kaoyan_math3_{year}_q{number:03d}"


def answer_page_links(year_dir: Path, from_card: bool) -> str:
    prefix = "../" if from_card else ""
    pages = sorted((year_dir / "images" / "answer_pages").glob("page-*.png"))
    if not pages:
        return "暂无答案解析页图。"
    lines = []
    for p in pages:
        rel = f"{prefix}images/answer_pages/{p.name}"
        lines.append(f"- [{p.stem}]({rel})")
    return "\n".join(lines)


def card_text(year: int, number: int, year_dir: Path) -> str:
    qid = question_id(year, number)
    source_page = source_page_name(year, number)
    answer_links = answer_page_links(year_dir, from_card=True)
    return f"""---
question_id: {qid}
exam_id: kaoyan_math3_{year}
exam_type: math3
year: {year}
question_number: {number}
question_type: {qtype(number)}
score: {score_for(number)}
module: {module_for(number)}
topics:
  - 待文本精修
difficulty: unknown
review_status: needs_text_refinement
answer_status: source_image_available
explanation_status: source_image_available
source_file: math3_{year}_questions.md
answer_source_file: math3_{year}_answers.md
---

# {year} 数学三第 {number} 题

## 题目

![{year} 数学三第 {number} 题所在原卷页](../images/source_pages/{source_page})

> 注：当前使用完整原卷页，避免自动裁切遗漏题干；后续可继续逐题文本化。

## 标准答案

见答案解析来源页图；本题待文本精修。

## 解析

本题当前按 PDF 页面视觉方式录入，未使用 PDF 乱码文本层。答案和解析来源为同年答案解析 PDF 页面图，后续需要继续清洗为纯文本 LaTeX 解析。

答案解析页图：

{answer_links}

## 来源

- 题目来源：{year} 年考研数学三真题 PDF
- 答案解析来源：{year} 年考研数学三答案解析 PDF
"""


def build_year(year: int) -> None:
    year_dir = EXAM_ROOT / str(year)
    (year_dir / "questions").mkdir(parents=True, exist_ok=True)
    rows = []
    questions_md = [f"# {year} 年考研数学三真题\n\n> 当前版本为 PDF 视觉落库版，后续需逐题文本精修。\n"]
    answers_md = [f"# {year} 年考研数学三答案与解析\n\n> 当前版本保留答案解析 PDF 页面图，后续需逐题文本精修。\n"]
    year_answer_links = answer_page_links(year_dir, from_card=False)

    for number in range(1, 23):
        qid = question_id(year, number)
        source_page = source_page_name(year, number)
        stem = f"![{year} 数学三第 {number} 题所在原卷页](images/source_pages/{source_page})"
        answer = "见答案解析来源页图；本题待文本精修。"
        explanation = "本题当前保留原卷页和答案解析页图，后续需要继续清洗为纯文本 LaTeX 解析。"

        (year_dir / "questions" / f"q{number:03d}.md").write_text(
            card_text(year, number, year_dir),
            encoding="utf-8",
            newline="\n",
        )
        questions_md.append(f"## 第 {number} 题\n\n{stem}\n")
        answers_md.append(
            f"## 第 {number} 题\n\n### 标准答案\n\n{answer}\n\n### 解析\n\n{explanation}\n\n"
            f"答案解析页图：\n\n{year_answer_links}\n"
        )
        rows.append(
            {
                "question_id": qid,
                "exam_id": f"kaoyan_math3_{year}",
                "exam_type": "math3",
                "year": year,
                "question_number": number,
                "question_type": qtype(number),
                "score": score_for(number),
                "module": module_for(number),
                "topics": ["待文本精修"],
                "difficulty": "unknown",
                "review_status": "needs_text_refinement",
                "answer_status": "source_image_available",
                "explanation_status": "source_image_available",
                "source_file": f"math3_{year}_questions.md",
                "answer_source_file": f"math3_{year}_answers.md",
                "card_path": f"questions/q{number:03d}.md",
                "stem": stem,
                "answer": answer,
                "explanation": explanation,
            }
        )

    (year_dir / f"math3_{year}_questions.md").write_text("\n".join(questions_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (year_dir / f"math3_{year}_answers.md").write_text("\n".join(answers_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (year_dir / "questions.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "exam_id": f"kaoyan_math3_{year}",
        "exam_type": "math3",
        "year": year,
        "question_count": 22,
        "source_files": [f"math3_{year}_questions.md", f"math3_{year}_answers.md"],
        "questions_jsonl": "questions.jsonl",
        "questions_dir": "questions",
        "status": "needs_text_refinement",
        "notes": [
            "当前为 PDF 视觉落库版，避免使用乱码文本层。",
            "题目以完整原卷页方式保留，答案解析页图已渲染入 images/answer_pages。",
            "后续应逐题转写为纯文本 LaTeX 题干、答案和解析。",
        ],
    }
    (year_dir / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"year": year, "question_count": 22}, ensure_ascii=False))


def main() -> None:
    for year in (2023, 2024):
        build_year(year)


if __name__ == "__main__":
    main()
