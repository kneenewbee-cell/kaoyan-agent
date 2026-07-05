from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers" / "math3"
TEX_ROOT = ROOT / "tmp" / "kysx" / "year"
GRAPHICS_ROOT = ROOT / "tmp" / "kysx" / "graphics"
ANSWER_ROOT = Path(r"D:\百度网盘\高数资料\【02】1987-2022考研数学三答案解析（PDF）")
QUESTION_PDF = Path(
    r"D:\百度网盘\高数资料\【01】1987-2022考研数学三真题（PDF）\【合集打印】1987-1996考研数学三真题【43页】.pdf"
)

YEARS = range(1987, 1997)
LEGACY_IMAGE_FALLBACK_YEARS = {1987, 1988, 1989}

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
    "\uf0bb": r"\approx",
    "\uf07e": r"\sim",
    "\uf039": r"\sim",
    "\uf022": r"\forall",
    "\uf0c6": r"\varnothing",
    "\uf057": r"\Omega",
    "\uf0cf": r"\in",
    "\uf0c8": r"\cap",
    "\uf079": r"\psi",
    "\uf02c": ",",
}

QUESTION_PAGE_RANGES = {
    1987: (2, 5),
    1988: (6, 8),
    1989: (9, 11),
    1990: (13, 16),
    1991: (17, 20),
    1992: (22, 25),
    1993: (27, 30),
    1994: (31, 34),
    1995: (35, 38),
    1996: (39, 41),
}

CHINESE_NUMERALS = "一二三四五六七八九十"
CHINESE_SECTION_RE = re.compile(rf"(?m)^\s*([{CHINESE_NUMERALS}]{{1,3}})[、.．]\s*(.*)$")
ITEM_NUMBER_RE = re.compile(r"(?m)^\s*[（(]\s*(\d{1,2})\s*[）)]")
ANSWER_RE = re.compile(r"【答案】\s*([\s\S]*?)(?=【解析】|【详解】|【分析】|$)")
EXPLANATION_RE = re.compile(r"(?:【解析】|【详解】|【分析】)\s*([\s\S]*)")
IMAGE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")


@dataclass
class ProblemInfo:
    number: int
    local_number: int
    section: int
    part_title: str
    part_note: str
    points: int | None
    stem: str
    assets: list[str]


@dataclass
class AnswerBlock:
    answer: str
    explanation: str
    raw: str
    assets: list[str]


def clean_pdf_text(text: str, *, keep_page_markers: bool = False) -> str:
    for src, dst in PUA_MAP.items():
        text = text.replace(src, dst)
    text = re.sub(r"[\uf000-\uf8ff]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not keep_page_markers:
        text = re.sub(r"(?m)^--- page \d+ ---$", "", text)
    text = re.sub(r"(?m)^-\s*\d+\s*-$", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def find_answer_pdf(year: int) -> Path:
    matches = sorted(path for path in ANSWER_ROOT.glob("*.pdf") if str(year) in path.name)
    if not matches:
        raise FileNotFoundError(f"cannot find answer PDF for {year} in {ANSWER_ROOT}")
    return matches[0]


def extract_answer_text(year: int, *, keep_page_markers: bool = False) -> str:
    pdf_path = find_answer_pdf(year)
    parts: list[str] = []
    with pdfplumber.open(str(pdf_path)) as doc:
        for index, page in enumerate(doc.pages, start=1):
            if keep_page_markers:
                parts.append(f"--- page {index} ---")
            parts.append(page.extract_text() or "")
    return clean_pdf_text("\n".join(parts), keep_page_markers=keep_page_markers)


def strip_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        out: list[str] = []
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


def parse_full_score(note: str) -> int | None:
    match = re.search(r"满分\s*(\d+)\s*分", note)
    return int(match.group(1)) if match else None


def parse_per_item_score(note: str) -> int | None:
    match = re.search(r"每小题\s*(\d+)\s*分", note)
    return int(match.group(1)) if match else None


def source_image_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not Path(name).suffix:
        name = f"{name}.png"
    return Path(name).name


def copy_graphics_asset(raw_name: str, year_dir: Path) -> str:
    image_name = source_image_name(raw_name)
    src = GRAPHICS_ROOT / image_name
    if not src.exists():
        raise FileNotFoundError(src)
    dst = year_dir / "images" / image_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"images/{image_name}"


def normalize_tex_spacing(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r" *\n *", "\n", body)
    return body.strip()


def format_abcd(match: re.Match[str]) -> str:
    content = match.group(1)
    parts = re.split(r"\\item\s*", content)
    labels = ["A", "B", "C", "D", "E", "F"]
    lines: list[str] = []
    for index, part in enumerate(parts[1:]):
        text = part.strip()
        if not text:
            continue
        lines.append(f"{labels[index]}. {text}")
    return "\n\n" + "\n\n".join(lines) + "\n"


def format_enumerate(match: re.Match[str]) -> str:
    content = match.group(1)
    parts = re.split(r"\\item\s*", content)
    lines: list[str] = []
    for index, part in enumerate(parts[1:], start=1):
        text = part.strip()
        if text:
            lines.append(f"{index}. {text}")
    return "\n\n" + "\n".join(lines) + "\n"


def tex_to_markdown(body: str, year_dir: Path, *, for_card: bool) -> tuple[str, list[str]]:
    body = body.strip()
    assets: list[str] = []

    def replace_image(match: re.Match[str]) -> str:
        asset = copy_graphics_asset(match.group(1), year_dir)
        if asset not in assets:
            assets.append(asset)
        target = f"../{asset}" if for_card else asset
        return f"\n\n![题图]({target})\n\n"

    body = re.sub(r"\\centerline\{([^{}]*\\includegraphics(?:\[[^\]]*\])?\{[^}]+\}[^{}]*)\}", r"\1", body)
    body = IMAGE_RE.sub(replace_image, body)
    body = re.sub(r"\\begin\{abcd\}([\s\S]*?)\\end\{abcd\}", format_abcd, body)
    body = re.sub(r"\\begin\{enumerate\*?\}([\s\S]*?)\\end\{enumerate\*?\}", format_enumerate, body)
    replacements = {
        r"\fillin{}": "____",
        r"\pickout{}": "（ ）",
        r"\pickin{}": "（ ）",
        r"\tickout{}": "（ ）",
        r"\dx": r"\,\mathrm{d}x",
        r"\dy": r"\,\mathrm{d}y",
        r"\dz": r"\,\mathrm{d}z",
        r"\dt": r"\,\mathrm{d}t",
        r"\du": r"\,\mathrm{d}u",
        r"\dv": r"\,\mathrm{d}v",
        r"\dr": r"\,\mathrm{d}r",
        r"\d ": r"\mathrm{d} ",
        r"\pd": r"\partial",
        r"\pdx": r"\partial x",
        r"\pdy": r"\partial y",
        r"\pdu": r"\partial u",
        r"\pdv": r"\partial v",
        r"\text{-}": "-",
    }
    for src, dst in replacements.items():
        body = body.replace(src, dst)
    body = re.sub(r"\\e(?![A-Za-z])", r"\\mathrm{e}", body)
    body = body.replace(r"\par", "\n\n")
    body = body.replace(r"\noindent", "")
    body = body.replace(r"\qquad", " ")
    body = body.replace(r"\quad", " ")
    body = re.sub(r"\\hspace\*\{[^}]+\}", " ", body)
    body = re.sub(r"\\text\{([^{}]+)\}", r"\1", body)
    return normalize_tex_spacing(body), assets


def tex_problem_maps(
    year: int,
    paper: int,
    year_dir: Path,
    memo: dict[int, tuple[dict[tuple[int, int], tuple[str, list[str]]], dict[int, tuple[str, list[str]]]]],
) -> tuple[dict[tuple[int, int], tuple[str, list[str]]], dict[int, tuple[str, list[str]]]]:
    if paper in memo:
        return memo[paper]
    tex_path = TEX_ROOT / str(year) / f"{year}P{paper}.tex"
    text = strip_comments(tex_path.read_text(encoding="utf-8"))
    by_section: dict[tuple[int, int], tuple[str, list[str]]] = {}
    by_global: dict[int, tuple[str, list[str]]] = {}
    section = 0
    local = 0
    global_number = 0
    pos = 0
    token_re = re.compile(
        r"\\makepart(?:\[[^\]]*\])?\{([^}]*)\}(?:\{([^}]*)\})?|"
        r"\\useproblem(?:\[[^\]]*\])?\{(\d+)\}\{(\d+)\}\{(\d+)\}|"
        r"\\begin\{problem\}"
    )
    while True:
        match = token_re.search(text, pos)
        if not match:
            break
        token = match.group(0)
        if token.startswith(r"\makepart"):
            section += 1
            local = 0
            pos = match.end()
            continue
        if token.startswith(r"\useproblem"):
            ref_paper = int(match.group(3))
            ref_section = int(match.group(4))
            ref_number = int(match.group(5))
            ref_maps = tex_problem_maps(year, ref_paper, year_dir, memo)
            stem_assets = resolve_problem_reference({ref_paper: ref_maps}, ref_paper, ref_section, ref_number)
            local += 1
            global_number += 1
            by_section[(section, local)] = stem_assets
            by_section[(section, global_number)] = stem_assets
            by_global[global_number] = stem_assets
            pos = match.end()
            continue
        end = find_matching_end(text, match.start())
        local += 1
        global_number += 1
        stem_assets = tex_to_markdown(extract_problem_body(text[match.start() : end]), year_dir, for_card=True)
        by_section[(section, local)] = stem_assets
        by_section[(section, global_number)] = stem_assets
        by_global[global_number] = stem_assets
        pos = end
    memo[paper] = (by_section, by_global)
    return by_section, by_global


def resolve_problem_reference(
    maps: dict[int, tuple[dict[tuple[int, int], tuple[str, list[str]]], dict[int, tuple[str, list[str]]]]],
    paper: int,
    section: int,
    number: int,
) -> tuple[str, list[str]]:
    by_section, by_global = maps[paper]
    if number == 0:
        stem_assets = by_global.get(section)
        if stem_assets is not None:
            return stem_assets
    stem_assets = by_section.get((section, number)) or by_global.get(number)
    if stem_assets is None:
        raise KeyError((paper, section, number))
    return stem_assets


def parse_problems_from_tex(year: int, year_dir: Path) -> list[ProblemInfo]:
    tex_path = TEX_ROOT / str(year) / f"{year}P4.tex"
    text = strip_comments(tex_path.read_text(encoding="utf-8"))
    memo: dict[int, tuple[dict[tuple[int, int], tuple[str, list[str]]], dict[int, tuple[str, list[str]]]]] = {}
    maps: dict[int, tuple[dict[tuple[int, int], tuple[str, list[str]]], dict[int, tuple[str, list[str]]]]] = {}
    for paper in range(1, 6):
        path = TEX_ROOT / str(year) / f"{year}P{paper}.tex"
        if path.exists():
            maps[paper] = tex_problem_maps(year, paper, year_dir, memo)

    problems: list[ProblemInfo] = []
    section = 0
    local = 0
    part_title = ""
    part_note = ""
    pos = 0
    token_re = re.compile(
        r"\\makepart(?:\[[^\]]*\])?\{([^}]*)\}(?:\{([^}]*)\})?|"
        r"\\useproblem(?:\[[^\]]*\])?\{(\d+)\}\{(\d+)\}\{(\d+)\}|"
        r"\\begin\{problem\}"
    )
    while True:
        match = token_re.search(text, pos)
        if not match:
            break
        token = match.group(0)
        if token.startswith(r"\makepart"):
            section += 1
            local = 0
            part_title = (match.group(1) or "").strip()
            part_note = (match.group(2) or "").strip()
            pos = match.end()
            continue
        if token.startswith(r"\useproblem"):
            paper = int(match.group(3))
            ref_section = int(match.group(4))
            ref_number = int(match.group(5))
            stem, assets = resolve_problem_reference(maps, paper, ref_section, ref_number)
            local += 1
            problems.append(
                ProblemInfo(
                    number=len(problems) + 1,
                    local_number=local,
                    section=section,
                    part_title=part_title,
                    part_note=part_note,
                    points=None,
                    stem=stem,
                    assets=assets,
                )
            )
            pos = match.end()
            continue
        end = find_matching_end(text, match.start())
        stem, assets = tex_to_markdown(extract_problem_body(text[match.start() : end]), year_dir, for_card=True)
        local += 1
        problems.append(
            ProblemInfo(
                number=len(problems) + 1,
                local_number=local,
                section=section,
                part_title=part_title,
                part_note=part_note,
                points=None,
                stem=stem,
                assets=assets,
            )
        )
        pos = end
    apply_section_scores(problems)
    return problems


def apply_section_scores(problems: list[ProblemInfo]) -> None:
    by_section: dict[int, list[ProblemInfo]] = {}
    for problem in problems:
        by_section.setdefault(problem.section, []).append(problem)

    for section_problems in by_section.values():
        note = section_problems[0].part_note
        per_item = parse_per_item_score(note)
        if per_item is not None:
            for problem in section_problems:
                problem.points = per_item
            continue

        if "每空" in note:
            for problem in section_problems:
                problem.points = None
            continue

        full_score = parse_full_score(note)
        if full_score is None:
            continue
        if len(section_problems) == 1:
            section_problems[0].points = full_score
        elif full_score % len(section_problems) == 0:
            per_problem = full_score // len(section_problems)
            for problem in section_problems:
                problem.points = per_problem


PAGE_MARKER_RE = re.compile(r"(?m)^--- page (\d+) ---$")


def split_answer_sections(text: str) -> list[str]:
    matches = list(CHINESE_SECTION_RE.finditer(text))
    if not matches:
        return [text]
    page_markers = list(PAGE_MARKER_RE.finditer(text))
    sections: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        previous_boundary = matches[index - 1].start() if index > 0 else 0
        for marker in reversed(page_markers):
            if previous_boundary <= marker.start() <= start:
                start = marker.start()
                break
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[start:end].strip())
    return sections


def chinese_number(index: int) -> str:
    values = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
        10: "十",
        11: "十一",
        12: "十二",
        13: "十三",
        14: "十四",
        15: "十五",
    }
    return values[index]


def item_marker_re(number: int, *, chinese: bool) -> re.Pattern[str]:
    marker = chinese_number(number) if chinese else str(number)
    return re.compile(rf"(?m)^\s*[（(]\s*{re.escape(marker)}\s*[）)]")


def split_numbered_section(section: str, count: int) -> list[str]:
    if count <= 1:
        return [section.strip()]

    def starts_for(chinese: bool) -> list[int] | None:
        starts: list[int] = []
        pos = 0
        for number in range(1, count + 1):
            match = item_marker_re(number, chinese=chinese).search(section, pos)
            if not match:
                return None
            starts.append(match.start())
            pos = match.end()
        return starts

    starts = starts_for(chinese=True)
    if starts is None:
        starts = starts_for(chinese=False)
    if starts is None:
        return [section.strip()] + [""] * (count - 1)
    starts.append(len(section))
    first_prefix = section[: starts[0]]
    first_markers = "\n".join(match.group(0) for match in PAGE_MARKER_RE.finditer(first_prefix))
    chunks: list[str] = []
    for index in range(count):
        chunk = section[starts[index] : starts[index + 1]].strip()
        if index == 0 and first_markers:
            chunk = f"{first_markers}\n{chunk}".strip()
        chunks.append(chunk)
    return chunks


def split_answers_by_tex_parts(year: int, text: str, problems: list[ProblemInfo]) -> list[str]:
    by_section: list[tuple[int, list[ProblemInfo]]] = []
    for problem in problems:
        if not by_section or by_section[-1][0] != problem.section:
            by_section.append((problem.section, []))
        by_section[-1][1].append(problem)
    answer_sections = split_answer_sections(text)
    if len(answer_sections) < len(by_section):
        raise ValueError(f"{year}: answer sections {len(answer_sections)} < tex sections {len(by_section)}")

    chunks: list[str] = []
    for index, (_, section_problems) in enumerate(by_section):
        section_text = answer_sections[index]
        chunks.extend(split_numbered_section(section_text, len(section_problems)))
    if len(chunks) != len(problems):
        raise ValueError(f"{year}: answer chunks {len(chunks)} != problems {len(problems)}")
    return chunks


def normalize_answer_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" 。；;")
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
    return text.strip()


def objective_answer_from_raw(raw: str) -> str | None:
    answer_marker = re.search(r"【\s*答案\s*】\s*[（(]?\s*([ABCD])\s*[）)]?", raw, re.IGNORECASE)
    if answer_marker:
        return answer_marker.group(1).upper()
    marker = re.search(r"[（(]\s*([ABCD])\s*[）)]", raw, re.IGNORECASE)
    if marker:
        return marker.group(1).upper()
    if re.search(r"[（(]\s*(?:√|对|正确)\s*[）)]", raw):
        return "√"
    if re.search(r"[（(]\s*(?:×|错|错误|\\times)\s*[）)]", raw):
        return "×"
    return None


def strip_legacy_marker(raw: str) -> str:
    text = CHINESE_SECTION_RE.sub("", raw, count=1).strip()
    text = PAGE_MARKER_RE.sub("", text).strip()
    text = re.sub(r"^\s*[（(]\s*(?:\d{1,2}|[一二三四五六七八九十]{1,3})\s*[）)]\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def page_numbers_from_chunk(chunk: str) -> list[int]:
    return [int(value) for value in PAGE_MARKER_RE.findall(chunk)]


def answer_assets_for_pages(pages: list[int]) -> list[str]:
    return [f"images/answer_pages/page_{page:03d}.png" for page in pages]


def image_fallback_explanation(problem: ProblemInfo, answer: str | None = None) -> str:
    if answer and answer not in {"见解析", "见答案解析页图"}:
        return f"答案为 {answer}。解析见下方答案解析页图；PDF 文本层公式不稳定，未直接转写为 LaTeX。"
    if question_type_for(problem) == "fill_blank":
        return "该题答案见下方答案解析页图；PDF 文本层顺序和公式不稳定，未直接转写为标准 LaTeX 文本。"
    return "解析见下方答案解析页图；PDF 文本层公式不稳定，未直接转写为 LaTeX。"


def is_safe_direct_answer(answer: str, qtype: str) -> bool:
    answer = answer.strip()
    if not answer or answer in {"见解析", "见答案解析页图"}:
        return False
    if qtype == "single_choice":
        return bool(re.fullmatch(r"[ABCD]", answer.strip("()（） ").upper()))
    if qtype == "true_false":
        return answer in {"√", "×"}
    if len(answer) > 32 or "\n" in answer:
        return False
    if any(token in answer for token in ("\\begin", "\\end", " ", "dx", "dy", "ln", "sin", "cos", "tan")):
        return False
    if re.search(r"[A-Za-z]", answer):
        return False
    return True


def split_answer_explanation(chunk: str, problem: ProblemInfo, *, year: int, assets: list[str]) -> AnswerBlock:
    raw = chunk.strip()
    answer_match = ANSWER_RE.search(raw)

    if year in LEGACY_IMAGE_FALLBACK_YEARS:
        qtype = question_type_for(problem)
        objective_answer = objective_answer_from_raw(raw) if qtype in {"true_false", "single_choice"} else None
        if objective_answer is not None:
            return AnswerBlock(
                answer=objective_answer,
                explanation=image_fallback_explanation(problem, objective_answer),
                raw=raw,
                assets=assets,
            )
        if qtype == "fill_blank":
            return AnswerBlock(
                answer="见答案解析页图",
                explanation=image_fallback_explanation(problem),
                raw=raw,
                assets=assets,
            )
        return AnswerBlock(
            answer="见答案解析页图",
            explanation=image_fallback_explanation(problem),
            raw=raw,
            assets=assets,
        )

    qtype = question_type_for(problem)
    if qtype in {"single_choice", "true_false"}:
        answer = objective_answer_from_raw(raw) or "见答案解析页图"
    elif answer_match:
        answer = normalize_answer_text(answer_match.group(1))
    else:
        answer = objective_answer_from_raw(raw) or "见答案解析页图"
    if not is_safe_direct_answer(answer, qtype):
        answer = "见答案解析页图"
    return AnswerBlock(
        answer=answer,
        explanation=image_fallback_explanation(problem, answer),
        raw=raw,
        assets=assets,
    )


def question_type_for(problem: ProblemInfo) -> str:
    if "选择" in problem.part_title:
        return "single_choice"
    if "填空" in problem.part_title:
        return "fill_blank"
    if "判断" in problem.part_title:
        return "true_false"
    return "solution"


def module_for(problem: ProblemInfo) -> str:
    text = problem.stem
    probability_tokens = [
        "随机变量",
        "概率",
        "分布函数",
        "概率密度",
        "数学期望",
        "方差",
        "正态分布",
        "置信区间",
        "假设检验",
        "样本",
        "二项分布",
        "均匀分布",
    ]
    linear_tokens = [
        "矩阵",
        "行列式",
        "线性方程组",
        "向量组",
        "特征值",
        "特征向量",
        "伴随矩阵",
        "二次型",
        "线性无关",
        "线性相关",
        "秩",
        "基础解系",
    ]
    if any(token in text for token in probability_tokens):
        return "概率统计"
    if any(token in text for token in linear_tokens):
        return "线性代数"
    return "高等数学"


TOPIC_RULES = [
    ("无穷小比较", ["无穷小", "等价无穷小", "同阶", "高阶"]),
    ("极限", ["极限", r"\lim"]),
    ("连续性", ["连续"]),
    ("可导性", ["可导", "导函数"]),
    ("导数", ["导数", r"f'", "切线", "边际", "弹性"]),
    ("偏导数", ["偏导", r"\partial"]),
    ("全微分", ["全微分", r"\mathrm{d}z"]),
    ("极值与最值", ["极值", "最大", "最小", "最优", "单调"]),
    ("凹凸性与拐点", ["凹凸", "拐点"]),
    ("渐近线", ["渐近线"]),
    ("不定积分", ["不定积分", r"\int", "+ C"]),
    ("定积分", ["定积分", "旋转体", "面积", "体积"]),
    ("二重积分", ["二重积分", r"\iint"]),
    ("级数", ["级数"]),
    ("幂级数", ["幂级数", "收敛区间", "收敛域"]),
    ("敛散性", ["敛散", "收敛", "发散"]),
    ("微分方程", ["微分方程", "通解"]),
    ("中值定理", ["罗尔定理", "拉格朗日中值定理", "中值定理"]),
    ("函数方程", ["函数方程"]),
    ("需求函数与弹性", ["需求", "供给", "弹性", "销售", "收益", "价格"]),
    ("矩阵", ["矩阵"]),
    ("行列式", ["行列式"]),
    ("矩阵的秩", ["秩"]),
    ("伴随矩阵", ["伴随矩阵", "A^*"]),
    ("特征值与特征向量", ["特征值", "特征向量", "特征方程"]),
    ("线性方程组", ["线性方程组", "基础解系"]),
    ("向量组线性相关性", ["向量组", "线性相关", "线性无关"]),
    ("概率", ["概率", "古典概型", "条件概率", "全概率", "贝叶斯"]),
    ("随机变量分布", ["随机变量", "分布函数", "概率密度", "联合分布"]),
    ("数学期望", ["数学期望", "期望"]),
    ("方差", ["方差"]),
    ("正态分布", ["正态分布", "标准正态"]),
    ("置信区间", ["置信区间", "置信度"]),
    ("假设检验", ["假设检验"]),
]

METHOD_RULES = [
    ("洛必达法则", ["洛必达", "罗必塔"]),
    ("泰勒展开", ["泰勒"]),
    ("分部积分", ["分部积分"]),
    ("换元积分", ["换元", "变量代换", "令 "]),
    ("有理化", ["有理化"]),
    ("积分区域交换", ["交换积分次序", "改换积分次序"]),
    ("极坐标变换", ["极坐标"]),
    ("比值判别法", ["比值判别法"]),
    ("比较判别法", ["比较判别法"]),
    ("莱布尼茨判别法", ["莱布尼茨判别法"]),
    ("初等变换", ["初等行变换", "初等列变换"]),
    ("待定系数法", ["待定系数"]),
    ("特征方程法", ["特征方程"]),
    ("反证法", ["反证法"]),
    ("全概率公式", ["全概率公式"]),
    ("贝叶斯公式", ["贝叶斯公式"]),
    ("标准化", ["标准化"]),
]


def labels_from_rules(text: str, rules: list[tuple[str, list[str]]]) -> list[str]:
    labels: list[str] = []
    for label, patterns in rules:
        if any(pattern in text for pattern in patterns):
            labels.append(label)
    return labels


def classify(problem: ProblemInfo, block: AnswerBlock) -> tuple[list[str], list[str]]:
    text = f"{problem.stem}\n{block.raw}\n{block.explanation}"
    topics = labels_from_rules(text, TOPIC_RULES)
    methods = labels_from_rules(text, METHOD_RULES)
    module = module_for(problem)
    if not topics:
        if module == "线性代数":
            topics = ["矩阵"]
        elif module == "概率统计":
            topics = ["概率"]
        else:
            topics = ["函数"]
    return dedupe(topics), dedupe(methods)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def yaml_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:"] + [f"  - {value}" for value in values]


def answer_page_assets(year_dir: Path) -> list[str]:
    answer_dir = year_dir / "images" / "answer_pages"
    if not answer_dir.exists():
        return []
    return [f"images/answer_pages/{path.name}" for path in sorted(answer_dir.glob("*.png"))]


def question_source_assets(year: int, year_dir: Path) -> list[str]:
    source_dir = year_dir / "images" / "source_pages"
    if not source_dir.exists():
        return []
    first_last = QUESTION_PAGE_RANGES.get(year)
    if not first_last:
        return [f"images/source_pages/{path.name}" for path in sorted(source_dir.glob("*.png"))]
    first, last = first_last
    assets = []
    for page in range(first, last + 1):
        name = f"page_{page:03d}.png"
        if (source_dir / name).exists():
            assets.append(f"images/source_pages/{name}")
    return assets


def render_source_pages(year_dir: Path, *, pdftoppm: Path | None) -> None:
    if pdftoppm is None or not QUESTION_PDF.exists():
        return
    year = int(year_dir.name)
    first_last = QUESTION_PAGE_RANGES.get(year)
    if not first_last:
        return
    first, last = first_last
    expected_names = {f"page_{page:03d}.png" for page in range(first, last + 1)}
    source_dir = year_dir / "images" / "source_pages"
    source_dir.mkdir(parents=True, exist_ok=True)
    tmp_pdf = ROOT / "tmp" / "math3_1987_1996_questions_ascii.pdf"
    if not tmp_pdf.exists():
        shutil.copy2(QUESTION_PDF, tmp_pdf)
    prefix = source_dir / "page"
    existing_names = {path.name for path in source_dir.glob("page_*.png")}
    if list(source_dir.glob("page-*.png")) or existing_names != expected_names:
        for path in list(source_dir.glob("page-*.png")) + list(source_dir.glob("page_*.png")):
            path.unlink()
    elif existing_names == expected_names:
        return
    subprocess.run(
        [str(pdftoppm), "-png", "-r", "160", "-f", str(first), "-l", str(last), str(tmp_pdf), str(prefix)],
        check=True,
    )
    for path in source_dir.glob("page-*.png"):
        match = re.search(r"page-(\d+)\.png$", path.name)
        if match:
            path.rename(source_dir / f"page_{int(match.group(1)):03d}.png")


def render_answer_pages(year: int, year_dir: Path, *, pdftoppm: Path | None) -> None:
    if pdftoppm is None:
        return
    answer_pdf = find_answer_pdf(year)
    answer_dir = year_dir / "images" / "answer_pages"
    answer_dir.mkdir(parents=True, exist_ok=True)
    if list(answer_dir.glob("page-*.png")):
        for path in list(answer_dir.glob("page-*.png")) + list(answer_dir.glob("page_*.png")):
            path.unlink()
    elif list(answer_dir.glob("page_*.png")):
        return
    tmp_pdf = ROOT / "tmp" / f"math3_{year}_answer_ascii.pdf"
    shutil.copy2(answer_pdf, tmp_pdf)
    prefix = answer_dir / "page"
    subprocess.run([str(pdftoppm), "-png", "-r", "160", str(tmp_pdf), str(prefix)], check=True)
    for path in answer_dir.glob("page-*.png"):
        match = re.search(r"page-(\d+)\.png$", path.name)
        if match:
            path.rename(answer_dir / f"page_{int(match.group(1)):03d}.png")


def question_id(year: int, number: int) -> str:
    return f"kaoyan_math3_{year}_q{number:03d}"


def card_text(
    *,
    year: int,
    problem: ProblemInfo,
    block: AnswerBlock,
    topics: list[str],
    methods: list[str],
    source_assets: list[str],
    answer_assets: list[str],
) -> str:
    qid = question_id(year, problem.number)
    qtype = question_type_for(problem)
    module = module_for(problem)
    assets = dedupe([*problem.assets, *source_assets, *answer_assets])
    frontmatter = [
        "---",
        f"question_id: {qid}",
        f"exam_id: kaoyan_math3_{year}",
        "exam_type: math3",
        f"year: {year}",
        f"question_number: {problem.number}",
        f"question_type: {qtype}",
        f"score: {problem.points if problem.points is not None else 'unknown'}",
        f"module: {module}",
        *yaml_list("topics", topics),
        *yaml_list("methods", methods),
        "difficulty: unknown",
        "review_status: reviewed",
        "answer_status: available",
        "explanation_status: available",
        f"source_file: math3_{year}_questions.md",
        f"answer_source_file: math3_{year}_answers.md",
        *yaml_list("assets", assets),
        "---",
    ]
    related = ""
    if answer_assets:
        related = "\n".join(
            [
                "## 答案解析页图",
                "",
                *[
                    f"![答案解析页 {index}](../{asset})"
                    for index, asset in enumerate(answer_assets, start=1)
                ],
                "",
            ]
        ).strip()
    source = (
        "## 来源\n\n"
        f"- 题目来源：{year} 年数学三 TeX 试卷源（试卷四）。\n"
        f"- 答案解析来源：{find_answer_pdf(year).name}。\n"
        "- 页面图只作为原卷/解析复核依据；题干正文已按 TeX 源整理为 LaTeX。"
    )
    sections = [
        f"# {year} 数学三第 {problem.number} 题",
        "## 题目\n\n" + problem.stem,
        "## 标准答案\n\n" + block.answer,
        "## 解析\n\n" + block.explanation,
        related,
        source,
    ]
    return "\n".join(frontmatter) + "\n\n" + "\n\n".join(section for section in sections if section).strip() + "\n"


def question_markdown_for_year(year: int, problems: list[ProblemInfo], year_dir: Path) -> str:
    lines = [
        f"# {year} 年考研数学三真题",
        "",
        "资料类型：考研数学三历年真题",
        f"年份：{year}",
        "科目：数学三",
        "整理状态：TeX 题干源整理，答案解析 PDF 文本层拆分",
        "",
    ]
    source_assets = question_source_assets(year, year_dir)
    if source_assets:
        lines.extend(["## 原卷页图", ""])
        for asset in source_assets:
            page_match = re.search(r"page_(\d+)\.png$", asset)
            page_label = page_match.group(1) if page_match else Path(asset).stem
            lines.extend([f"![{year} 数学三原卷页 {page_label}]({asset})", ""])

    current_section = None
    for problem in problems:
        if problem.section != current_section:
            current_section = problem.section
            title = problem.part_title or f"第 {problem.section} 部分"
            note = f"（{problem.part_note}）" if problem.part_note else ""
            lines.extend([f"## {title}{note}", ""])
        qtype_label = {"single_choice": "选择题", "fill_blank": "填空题", "true_false": "判断题"}.get(
            question_type_for(problem),
            "解答题",
        )
        lines.extend(
            [
                f"### 第 {problem.number} 题",
                "",
                f"- 题型：{qtype_label}",
                f"- 题号：{problem.number}",
                f"- 分值：{problem.points if problem.points is not None else '待复核'}",
                f"- 模块：{module_for(problem)}",
                "- 校对状态：已按 TeX 源整理",
                "",
                problem.stem.replace("../images/", "images/"),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def answers_markdown_for_year(year: int, blocks: list[AnswerBlock]) -> str:
    lines = [
        f"# {year} 年考研数学三答案与解析",
        "",
        "资料类型：考研数学三答案解析",
        f"年份：{year}",
        "科目：数学三",
        "校对状态：按答案解析 PDF 文本层拆分",
        "",
        "## 答案速查",
        "",
        "| 题号 | 答案 |",
        "|---|---|",
    ]
    for index, block in enumerate(blocks, start=1):
        answer = normalize_answer_text(block.answer)
        brief = " ".join(answer.split())
        if len(brief) > 48:
            brief = "见详细解析"
        lines.append(f"| {index} | {brief} |")
    lines.extend(["", "## 详细解析", ""])
    for index, block in enumerate(blocks, start=1):
        lines.extend(
            [
                f"### 第 {index} 题",
                "",
                f"- 答案：{block.answer}",
                "",
                block.explanation,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def row_for(
    *,
    year: int,
    problem: ProblemInfo,
    block: AnswerBlock,
    topics: list[str],
    methods: list[str],
    source_assets: list[str],
    answer_assets: list[str],
) -> dict[str, Any]:
    return {
        "question_id": question_id(year, problem.number),
        "exam_id": f"kaoyan_math3_{year}",
        "exam_type": "math3",
        "year": year,
        "question_number": problem.number,
        "question_type": question_type_for(problem),
        "score": problem.points,
        "module": module_for(problem),
        "topics": topics,
        "methods": methods,
        "difficulty": "unknown",
        "review_status": "reviewed",
        "answer_status": "available",
        "explanation_status": "available",
        "source_file": f"math3_{year}_questions.md",
        "answer_source_file": f"math3_{year}_answers.md",
        "card_path": f"questions/q{problem.number:03d}.md",
        "assets": dedupe([*problem.assets, *source_assets, *answer_assets]),
        "stem": problem.stem,
        "answer": block.answer,
        "explanation": block.explanation,
    }


def build_year(year: int, *, pdftoppm: Path | None, render_pages: bool) -> dict[str, Any]:
    year_dir = EXAM_ROOT / str(year)
    questions_dir = year_dir / "questions"
    questions_dir.mkdir(parents=True, exist_ok=True)
    (year_dir / "images").mkdir(parents=True, exist_ok=True)

    if render_pages:
        render_source_pages(year_dir, pdftoppm=pdftoppm)
        render_answer_pages(year, year_dir, pdftoppm=pdftoppm)

    problems = parse_problems_from_tex(year, year_dir)
    answer_text = extract_answer_text(year, keep_page_markers=True)
    answer_chunks = split_answers_by_tex_parts(year, answer_text, problems)
    blocks: list[AnswerBlock] = []
    current_pages: list[int] = []
    for chunk, problem in zip(answer_chunks, problems):
        pages = page_numbers_from_chunk(chunk)
        if pages:
            current_pages = pages
        blocks.append(
            split_answer_explanation(
                chunk,
                problem,
                year=year,
                assets=answer_assets_for_pages(current_pages),
            )
        )
    source_assets = question_source_assets(year, year_dir)
    answer_assets = answer_page_assets(year_dir)

    rows: list[dict[str, Any]] = []
    for problem, block in zip(problems, blocks):
        topics, methods = classify(problem, block)
        text = card_text(
            year=year,
            problem=problem,
            block=block,
            topics=topics,
            methods=methods,
            source_assets=[],
            answer_assets=block.assets,
        )
        (questions_dir / f"q{problem.number:03d}.md").write_text(text, encoding="utf-8", newline="\n")
        rows.append(
            row_for(
                year=year,
                problem=problem,
                block=block,
                topics=topics,
                methods=methods,
                source_assets=[],
                answer_assets=block.assets,
            )
        )

    (year_dir / f"math3_{year}_questions.md").write_text(
        question_markdown_for_year(year, problems, year_dir),
        encoding="utf-8",
        newline="\n",
    )
    (year_dir / f"math3_{year}_answers.md").write_text(
        answers_markdown_for_year(year, blocks),
        encoding="utf-8",
        newline="\n",
    )
    (year_dir / "questions.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "exam_id": f"kaoyan_math3_{year}",
        "exam_type": "math3",
        "exam_label": "数学三",
        "year": year,
        "source_files": {
            "questions": f"math3_{year}_questions.md",
            "answers": f"math3_{year}_answers.md",
        },
        "card_dir": "questions",
        "index_file": "questions.jsonl",
        "question_count": len(rows),
        "explanation_count": len(rows),
        "question_ids": [row["question_id"] for row in rows],
        "source_page_assets": source_assets,
        "answer_page_assets": answer_assets,
        "status": "reviewed",
        "notes": [
            "题干使用 TeX 源按数学三试卷四顺序还原。",
            "答案解析使用同年数学三答案解析 PDF 文本层按 TeX 题目结构拆分。",
            "PDF 页面图渲染为复核辅助资产，不替代题干正文。",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (year_dir / "paper_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {"year": year, "question_count": len(rows), "answer_chunks": len(blocks)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build math3 1987-1996 question cards from TeX and answer PDFs.")
    parser.add_argument("--from-year", type=int, default=1987)
    parser.add_argument("--to-year", type=int, default=1996)
    parser.add_argument("--pdftoppm", type=Path, default=None)
    parser.add_argument("--no-render-pages", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = []
    for year in range(args.from_year, args.to_year + 1):
        results.append(build_year(year, pdftoppm=args.pdftoppm, render_pages=not args.no_render_pages))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
