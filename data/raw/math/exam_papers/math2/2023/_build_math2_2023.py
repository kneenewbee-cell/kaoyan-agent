from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
YEAR = 2023
RAW_FILE = ROOT / "_raw_questions_2023.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def qtype_label(qtype: str) -> str:
    return {
        "single_choice": "选择题",
        "fill_blank": "填空题",
        "solution": "解答题",
        "proof": "证明题",
    }[qtype]


def answer_for_table(answer: str) -> str:
    brief = " ".join(answer.replace("\n", " ").split())
    if len(brief) > 48 or "\\begin{" in brief:
        return "见详细解析"
    return brief


def question_page(number: int) -> int:
    if number <= 7:
        return 1
    if number <= 17:
        return 2
    return 3


def answer_page(number: int) -> int:
    if number <= 16:
        return 3
    return 4


@dataclass
class Question:
    number: int
    question_type: str
    score: int
    module: str
    topics: list[str]
    stem: str
    answer: str
    explanation: str
    assets: list[str]


def load_questions() -> list[Question]:
    raw_items = json.loads(RAW_FILE.read_text(encoding="utf-8"))
    questions: list[Question] = []
    for item in raw_items:
        number = item["question_number"]
        questions.append(
            Question(
                number=number,
                question_type=item["question_type"],
                score=item["score"],
                module=item["module"],
                topics=item["topics"],
                stem=item["question_text"].strip(),
                answer=item["answer"].strip(),
                explanation=item["explanation"].strip(),
                assets=[
                    f"images/source_pages/page-{question_page(number)}.png",
                    f"images/answer_pages/page-{answer_page(number)}.png",
                ],
            )
        )
    return questions


def build_card(q: Question) -> str:
    qid = f"kaoyan_math2_{YEAR}_q{q.number:03d}"
    lines = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math2_{YEAR}",
        "exam_type: math2",
        f"year: {YEAR}",
        f"question_number: {q.number}",
        f"question_type: {q.question_type}",
        f"score: {q.score}",
        f"module: {q.module}",
        "topics:",
        *[f"  - {topic}" for topic in q.topics],
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math2_{YEAR}_questions.md",
        f"answer_source_file: math2_{YEAR}_answers.md",
        "assets:",
        *[f"  - {asset}" for asset in q.assets],
        "---",
        "",
        f"# {YEAR} 数学二第 {q.number} 题",
        "",
        "## 题目",
        "",
        q.stem,
        "",
    ]
    for asset in q.assets:
        lines.append(f"![题图](../{asset})")
    lines.extend(
        [
            "",
            "## 标准答案",
            "",
            q.answer,
            "",
            "## 解析",
            "",
            q.explanation,
            "",
            "## 来源",
            "",
            f"- 题目来源：`math2_{YEAR}_questions.md`",
            f"- 答案来源：`math2_{YEAR}_answers.md`",
            "",
        ]
    )
    return "\n".join(lines)


def annual_questions_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二真题",
        "",
        "资料类型：考研数学二历年真题",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：按题面 PDF 页图人工转写，并清理无关水印文字。",
        "",
    ]
    for page in range(1, 4):
        lines.extend(
            [
                f"**题面页图 {page}**",
                "",
                f"![{YEAR} 数学二题面页 {page}](images/source_pages/page-{page}.png)",
                "",
            ]
        )
    for q in questions:
        lines.extend(
            [
                f"## 第 {q.number} 题",
                f"- 题型：{qtype_label(q.question_type)}",
                f"- 分值：{q.score}",
                f"- 模块：{q.module}",
                f"- 考点：{'、'.join(q.topics)}",
                "",
                q.stem,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def annual_answers_md(questions: list[Question]) -> str:
    lines = [
        f"# {YEAR} 年数学二答案解析",
        "",
        "资料类型：考研数学二答案解析",
        f"年份：{YEAR}",
        "科目：数学二",
        "整理状态：仅保留答案合集中的数学二页面（第 3、4 页），并结合题面补全简洁解析。",
        "",
    ]
    for page in (3, 4):
        lines.extend(
            [
                f"**答案页图 {page}**",
                "",
                f"![{YEAR} 数学二答案页 {page}](images/answer_pages/page-{page}.png)",
                "",
            ]
        )
    lines.extend(
        [
            "## 答案速查",
            "",
            "| 题号 | 题型 | 答案 |",
            "|---|---|---|",
        ]
    )
    for q in questions:
        lines.append(f"| {q.number} | {qtype_label(q.question_type)} | {answer_for_table(q.answer)} |")
    lines.extend(["", "## 详细解析", ""])
    for q in questions:
        lines.extend(
            [
                f"### 第 {q.number} 题",
                "",
                f"- 答案：{q.answer}",
                "",
                q.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def card_record(q: Question) -> dict:
    return {
        "question_id": f"kaoyan_math2_{YEAR}_q{q.number:03d}",
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "year": YEAR,
        "question_number": q.number,
        "question_type": q.question_type,
        "score": q.score,
        "module": q.module,
        "topics": q.topics,
        "difficulty": "unknown",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
        "source_file": f"math2_{YEAR}_questions.md",
        "answer_source_file": f"math2_{YEAR}_answers.md",
        "card_path": f"questions/q{q.number:03d}.md",
        "assets": q.assets,
        "answer": q.answer,
        "explanation": q.explanation,
    }


def write_outputs(questions: list[Question]) -> None:
    question_md = annual_questions_md(questions)
    answer_md = annual_answers_md(questions)
    (ROOT / f"math2_{YEAR}_questions.md").write_text(question_md, encoding="utf-8")
    (ROOT / f"math2_{YEAR}_answers.md").write_text(answer_md, encoding="utf-8")

    card_dir = ROOT / "questions"
    card_dir.mkdir(exist_ok=True)
    records = []
    for q in questions:
        card_path = card_dir / f"q{q.number:03d}.md"
        card_path.write_text(build_card(q), encoding="utf-8")
        records.append(card_record(q))

    with (ROOT / "questions.jsonl").open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "exam_id": f"kaoyan_math2_{YEAR}",
        "exam_type": "math2",
        "exam_label": "数学二",
        "year": YEAR,
        "source_files": {
            "questions": f"math2_{YEAR}_questions.md",
            "answers": f"math2_{YEAR}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(questions),
        "explanation_count": len(questions),
        "question_ids": [record["question_id"] for record in records],
        "generated_at": now_iso(),
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
    }
    (ROOT / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    questions = load_questions()
    if len(questions) != 22:
        raise SystemExit(f"Expected 22 questions, got {len(questions)}")
    write_outputs(questions)


if __name__ == "__main__":
    main()
