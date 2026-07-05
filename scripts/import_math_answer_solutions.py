from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
DEFAULT_SOURCE_DIR = Path(r"D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）")

YEAR_RE = re.compile(r"(19\d{2}|20\d{2})")
ITEM_LINE_RE = re.compile(r"^\s*[（(]\s*(\d{1,2}|I|l)\s*[)）]\s*(.*)$")
ANSWER_RE = re.compile(r"【答案】\s*(.*?)(?=【解析】|【详解】|【分析】|解[:：]|$)")
SECTION_HEADING_RE = re.compile(r"^\s*[一二三四五六七八九十]+[、.．]\s*(.*)$")
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class SolutionBlock:
    number: int
    answer: str
    explanation: str


def _extract_pdf_text(pdf_path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _clean_line(line: str) -> str:
    line = line.strip().replace("\u3000", " ")
    return re.sub(r"[ \t]{2,}", " ", line)


def _solution_region(text: str) -> str:
    markers = ["试题解析", "参考解答及评分标准", "答案解析"]
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    if positions:
        return text[min(positions) :]
    return text


def _is_noise_line(line: str) -> bool:
    if not line:
        return True
    if PAGE_FOOTER_RE.match(line):
        return True
    if "历年考研数学真题解析及复习思路" in line:
        return True
    return False


def _looks_like_section_heading(line: str) -> bool:
    match = SECTION_HEADING_RE.match(line)
    if not match:
        return False
    title = match.group(1)
    return any(token in title for token in ("填空", "选择", "解答", "本题"))


def _is_group_section(line: str) -> bool:
    return "共" in line or "每小题" in line or "填空" in line or "选择" in line


def _is_problem_section(line: str) -> bool:
    return bool(_looks_like_section_heading(line) and not _is_group_section(line))


def _is_item_start(line: str) -> bool:
    match = ITEM_LINE_RE.match(line)
    if not match:
        return False
    rest = match.group(2).strip()
    if not rest:
        return True
    if rest.startswith("【"):
        return True
    return bool(CJK_RE.search(rest))


def split_solution_blocks(text: str, max_blocks: int | None = None) -> list[SolutionBlock]:
    lines = [_clean_line(line) for line in _solution_region(text).splitlines()]
    blocks: list[list[str]] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    for line in lines:
        if _is_noise_line(line):
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
        answer = _extract_answer(raw)
        explanation = _clean_explanation(raw)
        result.append(SolutionBlock(len(result) + 1, answer, explanation))
        if max_blocks and len(result) >= max_blocks:
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
    first_line = ITEM_LINE_RE.sub("", first_line).strip()
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
        lines[0] = ITEM_LINE_RE.sub("", lines[0]).strip()
    return "\n".join(line for line in lines if line).strip()


def _question_count(answer_path: Path) -> int | None:
    year_dir = answer_path.parent
    match = YEAR_RE.search(answer_path.name)
    if not match:
        return None
    year = int(match.group(1))
    question_path = year_dir / f"math1_{year}_questions.md"
    if not question_path.exists():
        return None
    return question_path.read_text(encoding="utf-8").count("### 第")


def render_answers_markdown(year: int, blocks: list[SolutionBlock], source_pdf: Path, text_layer_chars: int) -> str:
    missing_count = sum(1 for block in blocks if block.explanation.startswith("待从"))
    if not blocks:
        status = "未抽取到可用文本层，需视觉清洗"
    elif missing_count:
        status = f"部分解析待视觉清洗，已抽取 {len(blocks) - missing_count}/{len(blocks)} 题"
    else:
        status = "PDF文本层自动整理，待复核"
    lines = [
        f"# Math 1 {year} Answers",
        "",
        "资料类型：考研数学一答案解析  ",
        f"年份：{year}  ",
        "科目：数学一  ",
        f"来源 PDF：`{source_pdf}`  ",
        f"文本层字符数：{text_layer_chars}  ",
        f"校对状态：{status}  ",
        "",
        "## 解答题",
        "",
        "| 题号 | 答案速查 |",
        "|---|---|",
    ]
    if blocks:
        for block in blocks:
            lines.append(f"| {block.number} | {block.answer} |")
    else:
        lines.append("| 1 | 待从答案解析 PDF 视觉清洗 |")
    lines.extend(["", "## 详细解析", ""])
    if blocks:
        for block in blocks:
            lines.extend(
                [
                    f"### 第 {block.number} 题",
                    "",
                    f"- 答案：{block.answer}",
                    "",
                    block.explanation or "待复核",
                    "",
                ]
            )
    else:
        lines.extend(
            [
                "### 第 1 题",
                "",
                "- 答案：待从答案解析 PDF 视觉清洗",
                "",
                "待从答案解析 PDF 视觉清洗。",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def find_pdf_for_year(source_dir: Path, year: int) -> Path | None:
    matches = sorted(path for path in source_dir.glob("*.pdf") if str(year) in path.name)
    return matches[0] if matches else None


def import_year(source_dir: Path, root: Path, year: int, overwrite: bool = False) -> tuple[int, int, str]:
    pdf_path = find_pdf_for_year(source_dir, year)
    year_dir = root / "math1" / str(year)
    answer_path = year_dir / f"math1_{year}_answers.md"
    if answer_path.exists() and not overwrite:
        return year, 0, "exists"
    count = _question_count(answer_path)
    if pdf_path is None:
        blocks = _placeholder_blocks(count or 1)
        year_dir.mkdir(parents=True, exist_ok=True)
        answer_path.write_text(
            render_answers_markdown(year, blocks, Path("未找到对应答案解析 PDF"), 0),
            encoding="utf-8",
        )
        return year, 0, "missing_pdf"
    text = _extract_pdf_text(pdf_path)
    text_chars = len(text.strip())
    blocks = split_solution_blocks(text, max_blocks=count)
    if count and len(blocks) < count:
        blocks.extend(_placeholder_blocks(count - len(blocks), start=len(blocks) + 1))
    year_dir.mkdir(parents=True, exist_ok=True)
    answer_path.write_text(render_answers_markdown(year, blocks, pdf_path, text_chars), encoding="utf-8")
    real_blocks = sum(1 for block in blocks if not block.explanation.startswith("待从"))
    if real_blocks == 0:
        return year, 0, "needs_visual"
    if count and real_blocks < count:
        return year, real_blocks, "partial"
    return year, real_blocks, "ok"


def _placeholder_blocks(count: int, start: int = 1) -> list[SolutionBlock]:
    return [
        SolutionBlock(number, "待从答案解析 PDF 视觉清洗", "待从答案解析 PDF 视觉清洗。")
        for number in range(start, start + count)
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Math 1 answer solutions from per-year PDF text layers.")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--root", type=Path, default=DEFAULT_EXAM_ROOT)
    parser.add_argument("--from-year", type=int, default=1988)
    parser.add_argument("--to-year", type=int, default=2022)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for year in range(args.from_year, args.to_year + 1):
        result = import_year(args.source_dir, args.root, year, args.overwrite)
        print(f"{result[0]}: {result[1]} blocks ({result[2]})")


if __name__ == "__main__":
    main()
