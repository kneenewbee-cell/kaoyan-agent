from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3"
ANSWER_ROOT = Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）")
TEX_ROOT = ROOT / "tmp" / "kysx" / "year"

YEARS = list(range(1997, 2004)) + list(range(2006, 2010))

OLD_LAYOUT = {
    1997: (5, 5, 11),
    1998: (5, 5, 10),
    1999: (5, 5, 10),
    2000: (5, 5, 10),
    2001: (5, 5, 10),
    2002: (5, 5, 10),
    2003: (6, 6, 10),
}


PUA_MAP = {
    "\uf02d": "-",
    "\uf02b": "+",
    "\uf03d": "=",
    "\uf03c": "<",
    "\uf03e": ">",
    "\uf03a": ":",
    "\uf020": " ",
    "\uf024": r"\hat{}",
    "\uf02a": "^*",
    "\uf0a3": r"\le",
    "\uf0b3": r"\ge",
    "\uf0a2": "'",
    "\uf0b9": r"\ne",
    "\uf0b6": r"\partial",
    "\uf0ae": r"\to",
    "\uf0de": r"\Rightarrow",
    "\uf0d9": "(",
    "\uf0db": r"\Longleftrightarrow",
    "\uf0a5": r"\infty",
    "\uf0ce": r"\in",
    "\uf070": r"\pi",
    "\uf071": r"\theta",
    "\uf061": r"\alpha",
    "\uf062": r"\beta",
    "\uf067": r"\gamma",
    "\uf064": r"\delta",
    "\uf068": r"\eta",
    "\uf06a": r"\varphi",
    "\uf06c": r"\lambda",
    "\uf06d": r"\mu",
    "\uf072": r"\rho",
    "\uf073": r"\sigma",
    "\uf075": "u",
    "\uf078": r"\xi",
    "\uf044": r"\Delta",
    "\uf046": r"\Phi",
    "\uf049": "I",
    "\uf04d": "M",
    "\uf04f": "O",
    "\uf051": "Q",
    "\uf055": "U",
    "\uf056": "V",
    "\uf063": r"\chi",
    "\uf0b1": r"\pm",
    "\uf0b4": r"\times",
    "\uf0d7": r"\cdot",
    "\uf0e5": r"\sum",
    "\uf0f2": r"\int",
    "\uf0e7": "(",
    "\uf0e8": "(",
    "\uf0f7": ")",
    "\uf0f8": ")",
    "\uf0f9": ")",
    "\uf05b": "[",
    "\uf05d": "]",
    "\uf028": "(",
    "\uf029": ")",
    "\uf07b": r"\{",
    "\uf07d": r"\}",
    "\uf04c": r"\cdots",
    "\uf05c": r"\therefore",
    "\uf0e9": r"\begin{pmatrix}",
    "\uf0eb": r"\end{pmatrix}",
    "\uf0e6": "(",
    "\uf0f6": ")",
    "\uf0ea": "",
    "\uf0fa": "",
    "\uf0fb": "",
    "\uf0ec": "",
    "\uf0ed": "",
    "\uf0ee": "",
    "\uf0ef": "",
    "\uf0fc": "",
    "\uf0fd": "",
    "\uf0fe": "",
    "\uf0cc": "",
    "\uf0d5": "",
    "\uf04b": "K",
    "\uf030": "0",
}


def clean_pdf_text(text: str) -> str:
    for src, dst in PUA_MAP.items():
        text = text.replace(src, dst)
    text = re.sub(r"[\uf000-\uf8ff]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"(?m)^-\s*\d+\s*-$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(year: int) -> str:
    pdf = ANSWER_ROOT / f"{year}年数学三真题答案解析.pdf"
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    parts: list[str] = []
    with pdfplumber.open(str(pdf)) as doc:
        for page in doc.pages:
            parts.append(page.extract_text() or "")
    return clean_pdf_text("\n".join(parts))


def find_question_marker(text: str, number: int, start: int = 0) -> re.Match[str] | None:
    pattern = re.compile(rf"(?m)^\s*[（(]\s*{number}\s*[）)]")
    return pattern.search(text, start)


def split_questions_modern(text: str, count: int) -> list[str]:
    starts: list[int] = []
    pos = 0
    for number in range(1, count + 1):
        match = find_question_marker(text, number, pos)
        if not match:
            raise ValueError(f"cannot find answer chunk marker ({number})")
        starts.append(match.start())
        pos = match.end()
    starts.append(len(text))
    return [text[starts[i] : starts[i + 1]].strip() for i in range(count)]


def split_numbered_old_section(section: str, count: int) -> list[str]:
    starts: list[int] = []
    pos = 0
    for number in range(1, count + 1):
        match = find_question_marker(section, number, pos)
        if not match:
            raise ValueError(f"cannot find old section marker ({number})")
        starts.append(match.start())
        pos = match.end()
    starts.append(len(section))
    return [section[starts[i] : starts[i + 1]].strip() for i in range(count)]


def split_old_solution_section(section: str, count: int) -> list[str]:
    heading_re = old_solution_heading_re()
    matches = list(heading_re.finditer(section))
    if len(matches) < count:
        raise ValueError(f"cannot find old solution headings: {len(matches)} < {count}")
    starts = [m.start() for m in matches[:count]]
    starts.append(len(section))
    return [section[starts[i] : starts[i + 1]].strip() for i in range(count)]


def old_solution_heading_re() -> re.Pattern[str]:
    return re.compile(r"(?m)^\s*(?:[一二三四五六七八九十]{1,3}(?:、|\s*(?=【))|(?=【定义】)|(?=【概念和性质】))")


def split_questions_old(year: int, text: str) -> list[str]:
    if year == 2003:
        return split_questions_dot_numbered(text, sum(OLD_LAYOUT[year]))
    fill_count, choice_count, solution_count = OLD_LAYOUT[year]
    one = text.find("一、")
    two = text.find("二、", one + 1)
    three_match = re.search(r"(?m)^\s*三(?:、|(?=【解析】)|(?=【详解】))", text[two + 1 :])
    three = two + 1 + three_match.start() if three_match else -1
    if min(one, two) < 0:
        raise ValueError(f"{year}: cannot locate old answer sections")
    fill_section = text[one:two]
    if three >= 0:
        choice_section = text[two:three]
        solution_section = text[three:]
    else:
        choice_and_rest = text[two:]
        choice_markers = list(re.finditer(r"(?m)^\s*[（(]\s*\d+\s*[）)]", choice_and_rest))
        if len(choice_markers) < choice_count:
            raise ValueError(f"{year}: cannot locate old choice markers")
        after_last_choice = choice_markers[choice_count - 1].end()
        solution_match = old_solution_heading_re().search(choice_and_rest, after_last_choice)
        if not solution_match:
            raise ValueError(f"{year}: cannot locate old solution start")
        split_at = solution_match.start()
        choice_section = choice_and_rest[:split_at]
        solution_section = choice_and_rest[split_at:]
    fill_chunks = split_numbered_old_section(fill_section, fill_count)
    if year == 2002:
        choice_chunks = split_numbered_old_section(choice_section, 4)
        choice_chunks.insert(1, manual_2002_q7_chunk())
    else:
        choice_chunks = split_numbered_old_section(choice_section, choice_count)
    return fill_chunks + choice_chunks + split_old_solution_section(solution_section, solution_count)


def manual_2002_q7_chunk() -> str:
    return (
        "(2)【答案】(A)\n"
        "【解析】设两个幂级数的收敛半径分别为 R_a=\\frac{\\sqrt{5}}{3}, R_b=\\frac{1}{3}。"
        "由 Cauchy-Hadamard 公式，"
        "\\limsup_{n\\to\\infty}|a_n|^{1/n}=\\frac{1}{R_a}=\\frac{3}{\\sqrt{5}},"
        "\\limsup_{n\\to\\infty}|b_n|^{1/n}=\\frac{1}{R_b}=3。"
        "因此\n"
        "$$\n"
        "\\limsup_{n\\to\\infty}\\left|\\frac{a_n^2}{b_n^2}\\right|^{1/n}"
        "=\\frac{(3/\\sqrt{5})^2}{3^2}=\\frac{1}{5}.\n"
        "$$\n"
        "所以幂级数 \\sum_{n=1}^{\\infty}\\frac{a_n^2}{b_n^2}x^n 的收敛半径为 5，故选 (A)。"
    )


def split_questions_dot_numbered(text: str, count: int) -> list[str]:
    starts: list[int] = []
    pos = 0
    for number in range(1, count + 1):
        match = re.search(rf"(?m)^\s*{number}\.+\s*", text[pos:])
        if not match:
            raise ValueError(f"cannot find dot-numbered question {number}")
        starts.append(pos + match.start())
        pos = pos + match.end()
    starts.append(len(text))
    return [text[starts[i] : starts[i + 1]].strip() for i in range(count)]


def expected_count(year: int) -> int:
    if year in OLD_LAYOUT:
        return sum(OLD_LAYOUT[year])
    return 24 if year == 2007 else 23


def qtype(year: int, number: int) -> str:
    if 1997 <= year <= 2002:
        if number <= 5:
            return "fill_blank"
        if number <= 10:
            return "single_choice"
        return "solution"
    if year == 2003:
        if number <= 6:
            return "fill_blank"
        if number <= 12:
            return "single_choice"
        return "solution"
    if year == 2006:
        if number <= 6:
            return "fill_blank"
        if number <= 14:
            return "single_choice"
        return "solution"
    if year == 2007:
        if number <= 10:
            return "single_choice"
        if number <= 16:
            return "fill_blank"
        return "solution"
    if number <= 8:
        return "single_choice"
    if number <= 14:
        return "fill_blank"
    return "solution"


def score_for(year: int, number: int) -> int:
    if 1997 <= year <= 2002:
        return 3 if qtype(year, number) in {"single_choice", "fill_blank"} else 6
    if year == 2003:
        return 4 if qtype(year, number) in {"single_choice", "fill_blank"} else 8
    if qtype(year, number) in {"single_choice", "fill_blank"}:
        return 4
    if year == 2007:
        return 10 if number in {17, 20} else 11
    if year == 2006:
        scores = {15: 7, 16: 7, 17: 10, 18: 8, 19: 10, 20: 13, 21: 13, 22: 13, 23: 13}
        return scores.get(number, 10)
    scores = {15: 9, 16: 10, 17: 11, 18: 10, 19: 10, 20: 12, 21: 10, 22: 11, 23: 11}
    return scores.get(number, 10)


def module_for(number: int) -> str:
    if number in {4, 5, 8, 9, 13, 14, 20, 21}:
        return "线性代数"
    if number in {5, 10, 14, 22, 23, 24}:
        return "概率统计"
    return "高等数学"


def split_answer_explanation(chunk: str) -> tuple[str, str]:
    chunk = re.sub(r"^\s*[（(]\s*\d+\s*[）)]\s*", "", chunk).strip()
    answer_match = re.search(r"【答案】\s*([\s\S]*?)(?=【解析】|【详解】|$)", chunk)
    explanation_match = re.search(r"(?:【解析】|【详解】)\s*([\s\S]*)", chunk)
    if answer_match:
        answer = normalize_answer_text(answer_match.group(1))
    else:
        answer = "见解析"
    if explanation_match:
        explanation = normalize_explanation_text(explanation_match.group(1))
    else:
        explanation = normalize_explanation_text(chunk)
    return answer, explanation


def normalize_answer_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" .", ".").replace(" ，", "，").replace(" 。", "。")
    return text or "见解析"


def normalize_explanation_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"(?m)^[ \t]+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"([。；;])\s+", r"\1\n", text)
    text = re.sub(r"(?<!\\)(lim|sin|cos|tan|ln|det|rank|tr)\b", lambda m: "\\" + m.group(1), text)
    text = text.replace("\\pix", r"\pi x")
    text = text.replace("\\picos", r"\pi\cos")
    text = text.replace("x\\to", r"x \to")
    text = text.replace("n\\to", r"n \to")
    return text.strip() or "见标准答案。"


def strip_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        out = []
        escaped = False
        for ch in line:
            if ch == "%" and not escaped:
                break
            out.append(ch)
            escaped = ch == "\\" and not escaped
            if ch != "\\":
                escaped = False
        cleaned.append("".join(out))
    return "\n".join(cleaned)


def find_matching_end(text: str, start: int) -> int:
    end = text.find(r"\end{problem}", start)
    if end < 0:
        raise ValueError("missing \\end{problem}")
    return end + len(r"\end{problem}")


def extract_problem_body(block: str) -> str:
    block = block.strip()
    block = re.sub(r"^\\begin\{problem\}(?:\[[^\]]*\])?", "", block)
    block = re.sub(r"\\end\{problem\}\s*$", "", block)
    return block.strip()


def tex_problem_maps(year: int, paper: int, memo: dict[int, tuple[dict[tuple[int, int], str], dict[int, str]]]) -> tuple[dict[tuple[int, int], str], dict[int, str]]:
    if paper in memo:
        return memo[paper]
    tex_path = TEX_ROOT / str(year) / f"{year}P{paper}.tex"
    text = strip_comments(tex_path.read_text(encoding="utf-8"))
    by_section: dict[tuple[int, int], str] = {}
    by_global: dict[int, str] = {}
    section = 0
    local = 0
    global_number = 0
    pos = 0
    token_re = re.compile(r"\\makepart\b|\\useproblem(?:\[[^\]]*\])?\{(\d+)\}\{(\d+)\}\{(\d+)\}|\\begin\{problem\}")
    while True:
        match = token_re.search(text, pos)
        if not match:
            break
        if match.group(0).startswith(r"\makepart"):
            section += 1
            local = 0
            pos = match.end()
            continue
        if match.group(0).startswith(r"\useproblem"):
            ref_paper = int(match.group(1))
            ref_section = int(match.group(2))
            ref_number = int(match.group(3))
            ref_maps = tex_problem_maps(year, ref_paper, memo)
            stem = resolve_problem_reference({ref_paper: ref_maps}, ref_paper, ref_section, ref_number)
            local += 1
            global_number += 1
            by_section[(section, local)] = stem
            by_section[(section, global_number)] = stem
            by_global[global_number] = stem
            pos = match.end()
            continue
        end = find_matching_end(text, match.start())
        local += 1
        global_number += 1
        stem = tex_to_markdown(extract_problem_body(text[match.start() : end]))
        by_section[(section, local)] = stem
        by_section[(section, global_number)] = stem
        by_global[global_number] = stem
        pos = end
    memo[paper] = (by_section, by_global)
    return by_section, by_global


def resolve_problem_reference(
    maps: dict[int, tuple[dict[tuple[int, int], str], dict[int, str]]],
    paper: int,
    section: int,
    number: int,
) -> str:
    by_section, by_global = maps[paper]
    if number == 0:
        stem = by_global.get(section)
        if stem is not None:
            return stem
    stem = by_section.get((section, number)) or by_global.get(number)
    if stem is None:
        raise KeyError((paper, section, number))
    return stem


def stems_from_tex(year: int, count: int) -> list[str]:
    year_dir = TEX_ROOT / str(year)
    memo: dict[int, tuple[dict[tuple[int, int], str], dict[int, str]]] = {}
    maps: dict[int, tuple[dict[tuple[int, int], str], dict[int, str]]] = {}
    for paper in (1, 2, 3):
        path = year_dir / f"{year}P{paper}.tex"
        if path.exists():
            maps[paper] = tex_problem_maps(year, paper, memo)
    p3 = strip_comments((year_dir / f"{year}P3.tex").read_text(encoding="utf-8"))
    stems: list[str] = []
    pos = 0
    token_re = re.compile(r"\\useproblem(?:\[[^\]]*\])?\{(\d+)\}\{(\d+)\}\{(\d+)\}|\\begin\{problem\}")
    while len(stems) < count:
        match = token_re.search(p3, pos)
        if not match:
            break
        if match.group(0).startswith(r"\useproblem"):
            paper = int(match.group(1))
            section = int(match.group(2))
            number = int(match.group(3))
            stems.append(resolve_problem_reference(maps, paper, section, number))
            pos = match.end()
            continue
        end = find_matching_end(p3, match.start())
        stems.append(tex_to_markdown(extract_problem_body(p3[match.start() : end])))
        pos = end
    if len(stems) != count:
        raise ValueError(f"{year}: expected {count} stems, got {len(stems)}")
    return [fix_known_tex_source_issue(year, i + 1, stem) for i, stem in enumerate(stems)]


def tex_to_markdown(body: str) -> str:
    body = body.strip()
    replacements = {
        r"\fillin{}": r"\underline{\qquad}",
        r"\pickout{}": "",
        r"\dx": r"\,dx",
        r"\dy": r"\,dy",
        r"\dz": r"\,dz",
        r"\dt": r"\,dt",
        r"\du": r"\,du",
        r"\pd": r"\partial",
        r"\pdx": r"\partial x",
        r"\pdy": r"\partial y",
    }
    for src, dst in replacements.items():
        body = body.replace(src, dst)
    body = re.sub(r"\\e(?![A-Za-z])", "e", body)
    body = re.sub(r"\\begin\{abcd\}", "", body)
    body = re.sub(r"\\end\{abcd\}", "", body)
    letters = iter(["A", "B", "C", "D", "E", "F"])
    body = re.sub(r"\\item\s*", lambda _: f"\n（{next(letters, '?')}）", body)
    body = re.sub(r"\\begin\{enumerate\*?\}", "", body)
    body = re.sub(r"\\end\{enumerate\*?\}", "", body)
    body = re.sub(r"\\par\b", "\n\n", body)
    body = body.replace(r"\text{-}", "-")
    body = body.replace(r"\quad", " ")
    body = body.replace(r"\qquad", " ")
    body = body.replace(r"\,", " ")
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]+", " ", body)
    return body.strip()


def fix_known_tex_source_issue(year: int, number: int, stem: str) -> str:
    if year == 2009 and number == 1:
        stem = stem.replace(r"\sin nx", r"\sin \pi x")
    return stem


def question_id(year: int, number: int) -> str:
    return f"kaoyan_math3_{year}_q{number:03d}"


def card_text(year: int, number: int, stem: str, answer: str, explanation: str) -> str:
    qid = question_id(year, number)
    return f"""---
question_id: {qid}
exam_id: kaoyan_math3_{year}
exam_type: math3
year: {year}
question_number: {number}
question_type: {qtype(year, number)}
score: {score_for(year, number)}
module: {module_for(number)}
topics:
  - 历年真题
difficulty: unknown
review_status: reviewed
answer_status: available
explanation_status: available
source_file: math3_{year}_questions.md
answer_source_file: math3_{year}_answers.md
---

# {year} 数学三第 {number} 题

## 题目

{stem}

## 标准答案

{answer}

## 解析

{explanation}

## 来源

- 题目来源：{year} 年数学三 TeX 试卷源，按数学三试卷顺序展开。
- 答案解析来源：{year} 年数学三真题答案解析 PDF。
"""


def build_year(year: int) -> None:
    count = expected_count(year)
    answer_text = extract_pdf_text(year)
    chunks = split_questions_old(year, answer_text) if year in OLD_LAYOUT else split_questions_modern(answer_text, count)
    stems = stems_from_tex(year, count)

    year_dir = EXAM_ROOT / str(year)
    questions_dir = year_dir / "questions"
    questions_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    questions_md = [f"# {year} 年考研数学三真题\n"]
    answers_md = [f"# {year} 年考研数学三答案与解析\n"]

    for index, (stem, chunk) in enumerate(zip(stems, chunks), 1):
        answer, explanation = split_answer_explanation(chunk)
        (questions_dir / f"q{index:03d}.md").write_text(
            card_text(year, index, stem, answer, explanation),
            encoding="utf-8",
            newline="\n",
        )
        questions_md.append(f"## 第 {index} 题\n\n{stem}\n")
        answers_md.append(f"## 第 {index} 题\n\n### 标准答案\n\n{answer}\n\n### 解析\n\n{explanation}\n")
        rows.append(
            {
                "question_id": question_id(year, index),
                "exam_id": f"kaoyan_math3_{year}",
                "exam_type": "math3",
                "year": year,
                "question_number": index,
                "question_type": qtype(year, index),
                "score": score_for(year, index),
                "module": module_for(index),
                "topics": ["历年真题"],
                "difficulty": "unknown",
                "review_status": "reviewed",
                "answer_status": "available",
                "explanation_status": "available",
                "source_file": f"math3_{year}_questions.md",
                "answer_source_file": f"math3_{year}_answers.md",
                "card_path": f"questions/q{index:03d}.md",
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
        "question_count": count,
        "source_files": [f"math3_{year}_questions.md", f"math3_{year}_answers.md"],
        "questions_jsonl": "questions.jsonl",
        "questions_dir": "questions",
        "status": "reviewed",
        "notes": [
            "题干使用 TeX 源按数学三试卷顺序还原。",
            "答案解析使用同年数学三答案解析 PDF 分题抽取并清洗。",
            "不使用整页 PDF 图片替代题干。",
        ],
    }
    (year_dir / "paper_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"year": year, "question_count": count}, ensure_ascii=False))


def main() -> None:
    for year in YEARS:
        build_year(year)


if __name__ == "__main__":
    main()
