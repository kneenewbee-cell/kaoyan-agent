from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
YEAR = 2024
YEAR_DIR = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3" / str(YEAR)
PDF = Path(r"D:\百度网盘\高数资料\2024考研数学三真题答案解析.pdf")


PUA_MAP = {
    "\uf020": " ",
    "\uf02b": "+",
    "\uf02d": "-",
    "\uf03d": "=",
    "\uf03c": "<",
    "\uf03e": ">",
    "\uf028": "(",
    "\uf029": ")",
    "\uf04c": r"\cdots",
    "\uf070": r"\pi",
    "\uf071": r"\theta",
    "\uf06c": r"\lambda",
    "\uf06d": r"\mu",
    "\uf061": r"\alpha",
    "\uf062": r"\beta",
    "\uf078": r"\xi",
    "\uf0a5": r"\infty",
    "\uf0ae": r"\to",
    "\uf0b1": r"\pm",
    "\uf0b4": r"\times",
    "\uf0d7": r"\cdot",
    "\uf0de": r"\Rightarrow",
    "\uf0f2": r"\int",
    "\uf0e5": r"\sum",
    "\uf0e6": "(",
    "\uf0e7": "(",
    "\uf0e8": "(",
    "\uf0f6": ")",
    "\uf0f7": ")",
    "\uf0f8": ")",
    "\uf0f9": ")",
    "\uf0ec": r"\begin{cases}",
    "\uf0ed": "",
    "\uf0ee": "",
    "\uf0ef": r"\end{cases}",
    "\uf0eb": r"\end{pmatrix}",
    "\uf0e9": r"\begin{pmatrix}",
    "\uf0a3": r"\le",
    "\uf0b3": r"\ge",
    "\uf0b6": r"\partial",
    "\uf0a2": "'",
    "\uf0b8": "",
    "\uf0cc": "",
    "\uf0fc": "",
    "\uf0fd": "",
    "\uf0fe": "",
}


def clean_text(text: str) -> str:
    for src, dst in PUA_MAP.items():
        text = text.replace(src, dst)
    text = re.sub(r"[\uf000-\uf8ff]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("．", ".")
    return text.strip()


def extract_text() -> str:
    parts: list[str] = []
    with pdfplumber.open(str(PDF)) as doc:
        for page in doc.pages:
            parts.append(page.extract_text() or "")
    return clean_text("\n".join(parts))


def split_chunks(text: str) -> list[str]:
    pattern = re.compile(r"(?m)^\s*(\d{1,2})\.\s*")
    matches = [m for m in pattern.finditer(text) if 1 <= int(m.group(1)) <= 22]
    # Keep the first occurrence for each question number.
    by_number: dict[int, re.Match[str]] = {}
    for match in matches:
        number = int(match.group(1))
        by_number.setdefault(number, match)
    ordered = [by_number[i] for i in range(1, 23)]
    chunks: list[str] = []
    for idx, match in enumerate(ordered):
        end = ordered[idx + 1].start() if idx + 1 < len(ordered) else len(text)
        chunks.append(text[match.start() : end].strip())
    return chunks


def split_chunk(chunk: str) -> tuple[str, str, str]:
    chunk = re.sub(r"^\s*\d{1,2}\.\s*", "", chunk).strip()
    answer_match = re.search(r"【答案】\s*([\s\S]*?)(?=【解析】|$)", chunk)
    explanation_match = re.search(r"【解析】\s*([\s\S]*)", chunk)
    solution_match = re.search(r"(?:\d{1,2}\.)?【解】\s*([\s\S]*)", chunk)
    if answer_match:
        stem = chunk[: answer_match.start()].strip()
        answer = answer_match.group(1).strip()
        explanation = explanation_match.group(1).strip() if explanation_match else "见标准答案。"
    elif solution_match:
        stem = chunk[: solution_match.start()].strip()
        answer = "见解析"
        explanation = solution_match.group(1).strip()
    else:
        stem = chunk
        answer = "见解析"
        explanation = "见标准答案。"
    return normalize(stem), normalize(answer), normalize(explanation)


def normalize(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    text = re.sub(r"(?m)^[ \t]+", "", text)
    text = re.sub(r"(?m)^\d{1,2}\.\s*$", "", text)
    text = text.replace("n\uf03d", "n=")
    return text or "见解析"


def fix_known_extraction_issues(number: int, stem: str, answer: str, explanation: str) -> tuple[str, str, str]:
    if number == 1:
        stem = (
            "设函数\n\n"
            "$$\n"
            "f(x)=\\lim_{n\\to\\infty}\\frac{1+x}{1+n x^{2n}},\n"
            "$$\n"
            "则 $f(x)$（  ）\n\n"
            "A. 在 $x=1$，$x=-1$ 处都连续。\n\n"
            "B. 在 $x=1$ 处连续，在 $x=-1$ 处不连续。\n\n"
            "C. 在 $x=1$，$x=-1$ 处都不连续。\n\n"
            "D. 在 $x=1$ 处不连续，在 $x=-1$ 处连续。"
        )
        answer = "D"
        explanation = (
            "当 $|x|<1$ 时，$x^{2n}\\to0$，故 $f(x)=1+x$；当 $|x|>1$ 时，"
            "$n x^{2n}\\to\\infty$，故 $f(x)=0$。又 $f(1)=0$，$f(-1)=0$，"
            "所以 $f$ 在 $x=-1$ 处连续，在 $x=1$ 处不连续，选 D。"
        )
    if number == 2:
        stem = stem.replace("设I = \\int sinxdx", "设 $I=\\int_a^{a+k\\pi}|\\sin x|\\,dx$")
        answer = "B"
    if number == 22 and answer == "见解析":
        answer = "（1）$c=\\frac{n+1}{n}$；（2）$c=\\frac{n+2}{n+1}$。"
    if number <= 10:
        m = re.search(r"[ABCD]", answer)
        if m:
            answer = m.group(0)
    return stem, answer, explanation


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
    if number in {5, 6, 7, 14, 20, 21}:
        return "线性代数"
    if number in {8, 9, 10, 15, 16, 22}:
        return "概率统计"
    return "高等数学"


def question_id(number: int) -> str:
    return f"kaoyan_math3_{YEAR}_q{number:03d}"


def card_text(number: int, stem: str, answer: str, explanation: str) -> str:
    return f"""---
question_id: {question_id(number)}
exam_id: kaoyan_math3_{YEAR}
exam_type: math3
year: {YEAR}
question_number: {number}
question_type: {qtype(number)}
score: {score_for(number)}
module: {module_for(number)}
topics:
  - 历年真题
difficulty: unknown
review_status: reviewed
answer_status: available
explanation_status: available
source_file: math3_{YEAR}_questions.md
answer_source_file: math3_{YEAR}_answers.md
---

# {YEAR} 数学三第 {number} 题

## 题目

{stem}

## 标准答案

{answer}

## 解析

{explanation}

## 来源

- 题目来源：{YEAR} 考研数学三真题答案解析 PDF。
- 答案解析来源：{YEAR} 考研数学三真题答案解析 PDF。
"""


def build() -> None:
    chunks = split_chunks(extract_text())
    if len(chunks) != 22:
        raise ValueError(f"expected 22 chunks, got {len(chunks)}")
    questions_dir = YEAR_DIR / "questions"
    questions_dir.mkdir(parents=True, exist_ok=True)

    questions_md = [f"# {YEAR} 年考研数学三真题\n"]
    answers_md = [f"# {YEAR} 年考研数学三答案与解析\n"]
    rows: list[dict[str, object]] = []
    for number, chunk in enumerate(chunks, 1):
        stem, answer, explanation = split_chunk(chunk)
        stem, answer, explanation = fix_known_extraction_issues(number, stem, answer, explanation)
        (questions_dir / f"q{number:03d}.md").write_text(card_text(number, stem, answer, explanation), encoding="utf-8", newline="\n")
        questions_md.append(f"## 第 {number} 题\n\n{stem}\n")
        answers_md.append(f"## 第 {number} 题\n\n### 标准答案\n\n{answer}\n\n### 解析\n\n{explanation}\n")
        rows.append(
            {
                "question_id": question_id(number),
                "exam_id": f"kaoyan_math3_{YEAR}",
                "exam_type": "math3",
                "year": YEAR,
                "question_number": number,
                "question_type": qtype(number),
                "score": score_for(number),
                "module": module_for(number),
                "topics": ["历年真题"],
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math3_{YEAR}_questions.md",
                "answer_source_file": f"math3_{YEAR}_answers.md",
                "card_path": f"questions/q{number:03d}.md",
                "stem": stem,
                "answer": answer,
                "explanation": explanation,
            }
        )

    (YEAR_DIR / f"math3_{YEAR}_questions.md").write_text("\n".join(questions_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (YEAR_DIR / f"math3_{YEAR}_answers.md").write_text("\n".join(answers_md).rstrip() + "\n", encoding="utf-8", newline="\n")
    (YEAR_DIR / "questions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8", newline="\n")
    manifest = {
        "exam_id": f"kaoyan_math3_{YEAR}",
        "exam_type": "math3",
        "year": YEAR,
        "question_count": 22,
        "source_files": [f"math3_{YEAR}_questions.md", f"math3_{YEAR}_answers.md"],
        "questions_jsonl": "questions.jsonl",
        "questions_dir": "questions",
        "status": "reviewed",
        "notes": ["由 2024 考研数学三真题答案解析 PDF 文本层清洗生成。"],
    }
    (YEAR_DIR / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"year": YEAR, "question_count": 22}, ensure_ascii=False))


if __name__ == "__main__":
    build()
