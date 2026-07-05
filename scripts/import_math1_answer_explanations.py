from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATH1_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers" / "math1"
DEFAULT_SOURCE_DIR = Path(r"D:\百度网盘\高数资料\【02】1987-2022年数学一真题详解答案（PDF）")
DEFAULT_2023_PDF = Path(r"D:\百度网盘\高数资料\2023考研数学一答案解析（一二三合集）.pdf")
DEFAULT_2024_PDF = Path(r"D:\百度网盘\高数资料\2024考研数学一真题答案解析.pdf")

DETAIL_TITLES = {"详细解析", "答案解析", "解析", "详解"}
ANSWER_TABLE_TITLES = {"选择题", "填空题", "解答题"}
NO_DETAIL_YEARS = {
    2021: "源文件名标明“目前暂无详细解析”，只能核对答案，不能补充源内不存在的详解。",
    2023: "用户指定的 2023 PDF 是数一/数二/数三答案速查合集，未提供逐题详细解析。",
}
PLACEHOLDER_RE = re.compile(r"待从|视觉清洗|暂无详细解析|未提供详细解析|源文件缺失")
ANSWER_MARKER_RE = re.compile(r"【\s*答案\s*】")
EXPLANATION_MARKER_RE = re.compile(r"【\s*(解析|详解|分析|解法|评注)\s*】")


@dataclass
class ExtractedQuestion:
    number: int
    answer: str = ""
    explanation: str = ""
    source_mode: str = ""
    source_pages: list[int] = field(default_factory=list)
    confidence: str = "medium"
    notes: list[str] = field(default_factory=list)


@dataclass
class YearReport:
    year: int
    question_count: int
    source_pdf: str | None
    extraction_mode: str
    extracted_count: int
    written_count: int
    warnings: list[str] = field(default_factory=list)
    low_confidence_questions: list[int] = field(default_factory=list)


def _runtime_base() -> Path | None:
    marker = Path(sys.executable).resolve()
    for parent in [marker.parent, *marker.parents]:
        if parent.name == "codex-primary-runtime":
            dependencies = parent / "dependencies"
            return dependencies if dependencies.exists() else parent
    candidate = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies"
    return candidate if candidate.exists() else None


def _add_runtime_dll_paths() -> None:
    deps = _runtime_base()
    if not deps:
        return
    paths = [
        deps / "python",
        deps / "python" / "DLLs",
        deps / "python" / "Lib" / "site-packages" / "onnxruntime" / "capi",
        deps / "native" / "poppler" / "Library" / "bin",
    ]
    for path in paths:
        if not path.exists():
            continue
        os.environ["PATH"] = str(path) + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(str(path))
            except OSError:
                pass


def _find_pdftoppm() -> str:
    exe = shutil.which("pdftoppm")
    if exe:
        return exe
    deps = _runtime_base()
    if deps:
        candidate = deps / "native" / "poppler" / "Library" / "bin" / "pdftoppm.exe"
        if candidate.exists():
            return str(candidate)
    raise RuntimeError("Cannot find pdftoppm executable.")


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _render_pdf_pages(pdf_path: Path, target_dir: Path, dpi: int) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    for old in target_dir.glob("page-*.png"):
        old.unlink()
    prefix = target_dir / "page"
    command = [
        _find_pdftoppm(),
        "-png",
        "-r",
        str(dpi),
        str(pdf_path),
        str(prefix),
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return sorted(target_dir.glob("page-*.png"))


def _ocr_pdf(pdf_path: Path, target_dir: Path, dpi: int) -> tuple[str, list[dict[str, Any]]]:
    _add_runtime_dll_paths()
    from rapidocr_onnxruntime import RapidOCR

    cache_path = target_dir / "ocr_text.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        return cached.get("text", ""), cached.get("page_reports", [])

    image_paths = _render_pdf_pages(pdf_path, target_dir, dpi)
    ocr = RapidOCR()
    parts: list[str] = []
    page_reports: list[dict[str, Any]] = []
    for page_no, image_path in enumerate(image_paths, start=1):
        result, elapsed = ocr(str(image_path))
        lines: list[str] = []
        scores: list[float] = []
        if result:
            for item in result:
                text = str(item[1]).strip()
                if not text:
                    continue
                lines.append(text)
                try:
                    scores.append(float(item[2]))
                except (TypeError, ValueError):
                    pass
        avg_score = round(sum(scores) / len(scores), 4) if scores else 0.0
        page_reports.append(
            {
                "page": page_no,
                "image": str(image_path.relative_to(target_dir.parents[1])),
                "line_count": len(lines),
                "avg_score": avg_score,
                "elapsed": elapsed,
            }
        )
        parts.append(f"\n\n[[page:{page_no}]]\n" + "\n".join(lines))
    text = _normalize_text("\n".join(parts))
    cache_path.write_text(
        json.dumps({"text": text, "page_reports": page_reports}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return text, page_reports


def _source_for_year(year: int, source_dir: Path, pdf_2023: Path, pdf_2024: Path) -> Path | None:
    if year == 2023:
        return pdf_2023 if pdf_2023.exists() else None
    if year == 2024:
        return pdf_2024 if pdf_2024.exists() else None
    matches = sorted(source_dir.glob(f"*{year}*.pdf"))
    return matches[0] if matches else None


def _question_count(year_dir: Path) -> int:
    jsonl = year_dir / "questions.jsonl"
    if jsonl.exists():
        return sum(1 for line in jsonl.read_text(encoding="utf-8").splitlines() if line.strip())
    question_md = next(year_dir.glob("*_questions.md"), None)
    if question_md and question_md.exists():
        text = question_md.read_text(encoding="utf-8")
        return len(re.findall(r"^###\s+第\s+\d+\s+题\s*$", text, re.MULTILINE))
    return 0


def _extract_answers_from_text(text: str) -> dict[int, str]:
    answers: dict[int, str] = {}
    in_answer_table = False
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            title = heading.group(1).strip()
            in_answer_table = title in ANSWER_TABLE_TITLES
            continue
        if not in_answer_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].isdigit() and cells[1]:
            answers[int(cells[0])] = cells[1]
    return answers


def _git_head_text(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    completed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout if completed.returncode == 0 else None


def _extract_existing_answers(answer_md: Path) -> dict[int, str]:
    current_answers: dict[int, str] = {}
    if answer_md.exists():
        current_answers = _extract_answers_from_text(answer_md.read_text(encoding="utf-8"))

    baseline_text = _git_head_text(answer_md)
    if not baseline_text:
        return current_answers

    baseline_answers = _extract_answers_from_text(baseline_text)
    merged = dict(current_answers)
    for number, answer in baseline_answers.items():
        if answer and not PLACEHOLDER_RE.search(answer):
            merged[number] = answer
    return merged


def _extract_top_metadata(answer_md: Path, year: int) -> dict[str, str]:
    metadata = {
        "资料类型": "考研数学一答案解析",
        "年份": str(year),
        "科目": "数学一",
        "校对状态": "OCR/文本层批量整理，待抽样复核",
    }
    if not answer_md.exists():
        return metadata
    for line in answer_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        match = re.match(r"^\s*([^：:]+)[：:]\s*(.*?)\s*$", line)
        if match and match.group(1).strip() and match.group(2).strip():
            metadata[match.group(1).strip()] = match.group(2).strip()
    metadata["资料类型"] = "考研数学一答案解析"
    metadata["校对状态"] = "OCR/文本层批量整理，待抽样复核"
    return metadata


def _solution_start(text: str) -> str:
    candidates = [
        "试题解析",
        "参考解答",
        "答案解析",
        "真题解析",
    ]
    positions = [text.rfind(candidate) for candidate in candidates if candidate in text]
    positions = [pos for pos in positions if pos >= 0]
    if not positions:
        return text
    start = min(pos for pos in positions if pos >= max(0, max(positions) - 2000)) if positions else 0
    return text[start:]


def _page_for_offset(text: str, offset: int) -> int | None:
    current: int | None = None
    for match in re.finditer(r"\[\[page:(\d+)]]", text):
        if match.start() > offset:
            break
        current = int(match.group(1))
    return current


def _boundary_matches(text: str) -> list[re.Match[str]]:
    strong_patterns = [
        r"(?m)^\s*(\d{1,2})[．.]\s*【\s*答案\s*】",
        r"(?m)^\s*[（(](\d{1,2})[）)]\s*【\s*答案\s*】",
        r"(?m)^\s*[（(](\d{1,2})[）)]\s*(?=.{0,80}(?:【\s*答案\s*】|【\s*解析\s*】|【\s*详解\s*】|解[:：]))",
        r"(?m)^\s*(\d{1,2})[．.、]\s*(?=.{0,80}(?:【\s*答案\s*】|【\s*解析\s*】|【\s*详解\s*】|解[:：]))",
    ]
    strong_matches: list[re.Match[str]] = []
    for pattern in strong_patterns:
        strong_matches.extend(re.finditer(pattern, text))
    strong_numbers = {int(match.group(1)) for match in strong_matches if match.lastindex}

    general_matches = [
        match
        for match in re.finditer(r"(?m)^\s*(\d{1,2})[．.。]\s*(?=\S)", text)
        if match.lastindex and int(match.group(1)) not in strong_numbers
    ]
    matches = strong_matches + general_matches
    deduped: list[re.Match[str]] = []
    seen: set[int] = set()
    for match in matches:
        if match.start() in seen:
            continue
        seen.add(match.start())
        deduped.append(match)
    return sorted(deduped, key=lambda item: item.start())


def _general_boundary_matches(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"(?m)^\s*(\d{1,2})[．.。]\s*(?=\S)", text))


def _split_segments(text: str, expected_count: int) -> list[tuple[int | None, str, int]]:
    solution = _solution_start(text)
    matches = _boundary_matches(solution)
    if len(matches) < max(3, expected_count // 3):
        return []
    end_offsets = sorted({match.start() for match in matches} | {match.start() for match in _general_boundary_matches(solution)})
    segments: list[tuple[int | None, str, int]] = []
    for index, match in enumerate(matches):
        end = len(solution)
        for offset in end_offsets:
            if offset > match.start():
                end = offset
                break
        number = int(match.group(1)) if match.lastindex else None
        segment = solution[match.start() : end].strip()
        if segment:
            segments.append((number, segment, match.start()))
    return segments


def _extract_answer_from_segment(segment: str) -> tuple[str, str]:
    answer = ""
    explanation = segment
    answer_match = ANSWER_MARKER_RE.search(segment)
    if answer_match:
        after_answer = segment[answer_match.end() :].strip()
        marker = EXPLANATION_MARKER_RE.search(after_answer)
        if marker:
            answer = after_answer[: marker.start()].strip()
            explanation = after_answer[marker.start() :].strip()
        else:
            first_line, _, rest = after_answer.partition("\n")
            answer = first_line.strip()
            explanation = rest.strip() or after_answer
    else:
        for token in ("解：", "解:", "解析：", "解析:"):
            pos = segment.find(token)
            if pos >= 0:
                explanation = segment[pos:].strip()
                break

    answer = re.sub(r"\s+", " ", answer).strip(" ：:；;，,")
    explanation = _clean_explanation(explanation)
    return answer, explanation


def _clean_explanation(text: str) -> str:
    text = re.sub(r"\[\[page:\d+]]", "", text)
    text = re.sub(r"^\s*[（(]?\d{1,2}[）)]?[．.、]?\s*", "", text.strip())
    text = text.replace("【详解】", "详解：").replace("【解析】", "解析：").replace("【分析】", "分析：")
    cleaned_lines = []
    for line in text.splitlines():
        if any(token in line for token in ("后续更新关注公众号", "永久联系微信", "发普")):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _trim_cross_question_tail(text: str, number: int, expected_count: int) -> str:
    cut_positions: list[int] = []
    section_match = re.search(r"\s+[一二三四五六七八九十]、\s*(?:选择题|填空题|解答题)", text)
    if section_match and section_match.start() > 40:
        cut_positions.append(section_match.start())
    for next_number in range(number + 1, expected_count + 1):
        pattern = rf"(?<!\d)\s+{next_number}[．.。]\s*(?=\S)"
        match = re.search(pattern, text)
        if match and match.start() > 40:
            cut_positions.append(match.start())
            break
    if not cut_positions:
        return text.strip()
    return text[: min(cut_positions)].strip()


def _segments_to_questions(text: str, expected_count: int) -> tuple[dict[int, ExtractedQuestion], list[str]]:
    warnings: list[str] = []
    segments = _split_segments(text, expected_count)
    extracted: dict[int, ExtractedQuestion] = {}
    if not segments:
        warnings.append("未能按题号切分来源文本。")
        return extracted, warnings

    captured_numbers = [number for number, _, _ in segments if number is not None]
    unique_captured = sorted(set(captured_numbers))
    use_captured_number = (
        len(unique_captured) >= min(expected_count, 10)
        and max(unique_captured, default=0) >= min(expected_count, 10)
        and len(captured_numbers) <= expected_count + 5
    )

    assigned = 0
    for sequence, (captured, segment, offset) in enumerate(segments, start=1):
        number = captured if use_captured_number and captured is not None else sequence
        if not number or number < 1 or number > expected_count:
            continue
        if number in extracted:
            continue
        answer, explanation = _extract_answer_from_segment(segment)
        explanation = _trim_cross_question_tail(explanation, number, expected_count)
        if not explanation:
            continue
        page = _page_for_offset(text, offset)
        extracted[number] = ExtractedQuestion(
            number=number,
            answer=answer,
            explanation=explanation,
            source_mode="text_or_ocr",
            source_pages=[page] if page else [],
            confidence="medium" if answer or "解析" in explanation or "详解" in explanation else "low",
        )
        assigned += 1
        if assigned >= expected_count:
            break

    if len(extracted) < expected_count:
        warnings.append(f"按题号切分得到 {len(extracted)}/{expected_count} 题。")
    return extracted, warnings


def _legacy_sequential_questions(text: str, expected_count: int) -> dict[int, ExtractedQuestion]:
    section_re = re.compile(r"(?m)^\s*([一二三四五六七八九十]{1,3})[、．.]\s*")
    sub_re = re.compile(r"(?m)^\s*[（(](\d{1,2})[）)]")
    headings = list(section_re.finditer(text))
    if not headings:
        return {}

    units: list[tuple[int | None, int | None, list[str]]] = []
    split_sub_sections = {"一", "二", "三", "十"}
    for index, heading in enumerate(headings):
        section_start = heading.start()
        section_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section_text = text[section_start:section_end]
        section_name = heading.group(1)
        sub_matches = [(int(match.group(1)), section_start + match.start()) for match in sub_re.finditer(section_text)]
        if section_name in split_sub_sections:
            by_label: dict[int, int] = {}
            for label, start in sub_matches:
                by_label.setdefault(label, start)
            max_label = max(by_label) if by_label else 0
            for label in range(1, max_label + 1):
                start = by_label.get(label)
                if start is None:
                    units.append((None, None, [f"旧卷第{section_name}大题第 {label} 小题在 OCR 文本中缺少稳定题号。"]))
                    continue
                later_starts = [candidate for candidate_label, candidate in by_label.items() if candidate_label > label]
                end = min(later_starts) if later_starts else section_end
                units.append((start, end, []))
        else:
            units.append((section_start, section_end, []))

    if len(units) < max(3, expected_count // 2):
        return {}

    extracted: dict[int, ExtractedQuestion] = {}
    for sequence, (start, end, unit_notes) in enumerate(units[:expected_count], start=1):
        if start is None or end is None:
            extracted[sequence] = ExtractedQuestion(
                number=sequence,
                answer="待核对",
                explanation="源页 OCR 漏识别该小题编号或正文，需人工核对。",
                source_mode="legacy_page_order",
                confidence="low",
                notes=unit_notes or ["旧卷 OCR 顺序切分缺失该题。"],
            )
            continue
        segment = text[start:end].strip()
        if not segment:
            continue
        answer, explanation = _extract_answer_from_segment(segment)
        explanation = _trim_cross_question_tail(explanation, sequence, expected_count)
        page = _page_for_offset(text, start)
        extracted[sequence] = ExtractedQuestion(
            number=sequence,
            answer=answer or "见解析",
            explanation=explanation,
            source_mode="legacy_page_order",
            source_pages=[page] if page else [],
            confidence="low",
            notes=["旧卷按大题/小题出现顺序映射，建议抽样核对。"],
        )
    return extracted


def _fallback_sequential_chunks(text: str, expected_count: int) -> dict[int, ExtractedQuestion]:
    cleaned = _clean_explanation(_solution_start(text))
    if not cleaned:
        return {}
    paragraphs = [part.strip() for part in re.split(r"\n{2,}", cleaned) if part.strip()]
    if len(paragraphs) < expected_count:
        return {}
    chunks: dict[int, ExtractedQuestion] = {}
    for number in range(1, expected_count + 1):
        index = min(number - 1, len(paragraphs) - 1)
        chunks[number] = ExtractedQuestion(
            number=number,
            explanation=paragraphs[index],
            source_mode="fallback_paragraph",
            confidence="low",
            notes=["未识别到稳定题号，按段落顺序兜底分配，需人工核对。"],
        )
    return chunks


def _page_chunks(text: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"\[\[page:(\d+)]]", text))
    chunks: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        page_text = _clean_explanation(text[match.end() : end])
        if page_text:
            chunks.append((int(match.group(1)), page_text))
    return chunks


def _fallback_missing_from_pages(text: str, missing_numbers: list[int], expected_count: int) -> dict[int, ExtractedQuestion]:
    chunks = _page_chunks(text)
    if not chunks:
        return {}
    fallback: dict[int, ExtractedQuestion] = {}
    page_count = len(chunks)
    for number in missing_numbers:
        if expected_count <= 1:
            page_index = 0
        else:
            page_index = round((number - 1) * (page_count - 1) / (expected_count - 1))
        page, page_text = chunks[max(0, min(page_index, page_count - 1))]
        fallback[number] = ExtractedQuestion(
            number=number,
            answer="见解析",
            explanation=page_text,
            source_mode="page_position_fallback",
            source_pages=[page],
            confidence="low",
            notes=["未能稳定切出本题解析，按题号位置映射到来源页 OCR 文本，必须人工核对。"],
        )
    return fallback

def _answer_tables(answers: dict[int, str], question_count: int) -> str:
    choice_end = min(10, question_count)
    blank_end = min(16, question_count)
    groups = [
        ("选择题", range(1, min(choice_end, question_count) + 1), "答案"),
        ("填空题", range(choice_end + 1, min(blank_end, question_count) + 1), "答案"),
        ("解答题", range(blank_end + 1, question_count + 1), "答案速查"),
    ]
    lines: list[str] = []
    for title, numbers, answer_header in groups:
        nums = list(numbers)
        if not nums:
            continue
        lines.extend([f"## {title}", "", f"| 题号 | {answer_header} |", "|---|---|"])
        for number in nums:
            lines.append(f"| {number} | {answers.get(number, '待核对')} |")
        lines.append("")
    return "\n".join(lines).strip()


def _render_answer_md(
    *,
    year: int,
    metadata: dict[str, str],
    source_pdf: Path | None,
    question_count: int,
    answers: dict[int, str],
    extracted: dict[int, ExtractedQuestion],
    extraction_mode: str,
    year_warning: str | None,
) -> str:
    lines = [f"# Math 1 {year} Answers", ""]
    for key in ("资料类型", "年份", "科目", "来源", "校对状态"):
        if key == "来源":
            value = str(source_pdf) if source_pdf else "未找到用户指定来源 PDF"
        else:
            value = metadata.get(key)
        if value:
            lines.append(f"{key}：{value}  ")
    lines.append("")
    lines.append(_answer_tables(answers, question_count))
    lines.extend(["", "## 详细解析", ""])
    lines.append(f"解析来源：`{source_pdf}`  " if source_pdf else "解析来源：未找到用户指定来源 PDF  ")
    lines.append(f"抽取方式：{extraction_mode}  ")
    if year_warning:
        lines.append(f"说明：{year_warning}  ")
    lines.append("")

    for number in range(1, question_count + 1):
        item = extracted.get(number)
        answer = (item.answer if item and item.answer else answers.get(number, "待核对")).strip()
        lines.extend([f"### 第 {number} 题", "", f"- 答案：{answer}", ""])
        if item and item.explanation:
            if item.source_pages:
                page_text = "、".join(str(page) for page in item.source_pages)
                lines.append(f"> 来源页：{page_text}；置信度：{item.confidence}")
                lines.append("")
            for note in item.notes:
                lines.append(f"> 注意：{note}")
                lines.append("")
            lines.append(item.explanation.strip())
        else:
            if year_warning:
                lines.append(year_warning)
            else:
                lines.append("未能从来源 PDF 中稳定切出本题解析，需人工核对来源页。")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _build_cards(math_root: Path, year: int) -> None:
    script = ROOT / "scripts" / "build_math_question_cards.py"
    command = [
        sys.executable,
        str(script),
        "--root",
        str(math_root.parent),
        "--exam-type",
        "math1",
        "--year",
        str(year),
    ]
    completed = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())


def process_year(
    *,
    year: int,
    math1_root: Path,
    source_dir: Path,
    pdf_2023: Path,
    pdf_2024: Path,
    dpi: int,
    use_ocr: bool,
    rebuild_cards: bool,
) -> YearReport:
    year_dir = math1_root / str(year)
    answer_md = year_dir / f"math1_{year}_answers.md"
    question_count = _question_count(year_dir)
    if question_count == 0:
        return YearReport(year, 0, None, "missing_questions", 0, 0, ["未找到题目数据。"])

    existing_answers = _extract_existing_answers(answer_md)
    metadata = _extract_top_metadata(answer_md, year)
    source_pdf = _source_for_year(year, source_dir, pdf_2023, pdf_2024)
    extracted: dict[int, ExtractedQuestion] = {}
    warnings: list[str] = []
    extraction_mode = "missing_source"
    year_warning: str | None = None
    image_text = ""

    if source_pdf is None:
        year_warning = "未在用户指定来源目录中找到本年份答案解析 PDF，暂无法补充可靠详细解析。"
        warnings.append(year_warning)
    elif year in NO_DETAIL_YEARS:
        extraction_mode = "source_has_answers_only"
        year_warning = NO_DETAIL_YEARS[year]
        warnings.append(year_warning)
    else:
        if use_ocr:
            ocr_dir = year_dir / "images" / "answer_pages"
            image_text, page_reports = _ocr_pdf(source_pdf, ocr_dir, dpi)
            extracted, segment_warnings = _segments_to_questions(image_text, question_count)
            extraction_mode = "rapidocr_page_images"
            warnings.extend(segment_warnings)
            low_pages = [item["page"] for item in page_reports if item["avg_score"] < 0.82]
            if low_pages:
                warnings.append(f"OCR 平均置信度偏低页：{low_pages}")
        else:
            extraction_mode = "page_images_disabled"
            warnings.append("已禁用页面图像 OCR，未抽取解析。")
        if len(extracted) < question_count:
            legacy = _legacy_sequential_questions(image_text, question_count)
            if len(legacy) > len(extracted):
                extracted = legacy
                extraction_mode = "legacy_page_order"
                warnings.append("使用旧卷大题/小题顺序切分。")
        if len(extracted) < question_count:
            fallback = _fallback_sequential_chunks(image_text, question_count)
            for number, item in fallback.items():
                extracted.setdefault(number, item)
            if fallback:
                warnings.append("部分题目使用按段落顺序兜底切分。")
        missing_after_order_fallback = [number for number in range(1, question_count + 1) if number not in extracted]
        if image_text and missing_after_order_fallback:
            page_missing = missing_after_order_fallback
            if year == 1988:
                page_missing = [number for number in page_missing if number <= 22]
            page_fallback = _fallback_missing_from_pages(image_text, page_missing, question_count)
            for number, item in page_fallback.items():
                extracted.setdefault(number, item)
            if page_fallback:
                warnings.append("部分题目使用来源页位置 OCR 低置信兜底。")

    final_answers = dict(existing_answers)
    for number in range(1, question_count + 1):
        item = extracted.get(number)
        existing_answer = existing_answers.get(number, "")
        if item and existing_answer and not PLACEHOLDER_RE.search(existing_answer):
            item.answer = existing_answer
        elif item and (not item.answer or PLACEHOLDER_RE.search(item.answer)):
            item.answer = existing_answer if existing_answer and not PLACEHOLDER_RE.search(existing_answer) else "见解析"
        if item and (not final_answers.get(number) or PLACEHOLDER_RE.search(final_answers.get(number, ""))):
            final_answers[number] = item.answer or "见解析"
        elif not item and year_warning:
            missing_source_answer = existing_answer if existing_answer and not PLACEHOLDER_RE.search(existing_answer) else "源文件缺失，待补源"
            extracted[number] = ExtractedQuestion(
                number=number,
                answer=missing_source_answer,
                explanation=year_warning,
                source_mode=extraction_mode,
                confidence="low",
                notes=["源文件无法提供本题详细解析。"],
            )
            final_answers[number] = missing_source_answer

    rendered = _render_answer_md(
        year=year,
        metadata=metadata,
        source_pdf=source_pdf,
        question_count=question_count,
        answers=final_answers,
        extracted=extracted,
        extraction_mode=extraction_mode,
        year_warning=year_warning,
    )
    answer_md.write_text(rendered, encoding="utf-8")

    if rebuild_cards:
        _build_cards(math1_root, year)

    low_confidence = [
        number
        for number, item in sorted(extracted.items())
        if item.confidence == "low" or any("兜底" in note for note in item.notes)
    ]
    missing = [number for number in range(1, question_count + 1) if number not in extracted]
    if missing:
        warnings.append(f"仍未写入解析的题号：{missing}")

    return YearReport(
        year=year,
        question_count=question_count,
        source_pdf=str(source_pdf) if source_pdf else None,
        extraction_mode=extraction_mode,
        extracted_count=len(extracted),
        written_count=question_count,
        warnings=warnings,
        low_confidence_questions=low_confidence,
    )


def _question_hits_by_notice(math1_root: Path, notice: str, end_year: int) -> dict[int, list[int]]:
    hits: dict[int, list[int]] = {}
    for answer_path in sorted(math1_root.glob("*/math1_*_answers.md")):
        year_dir = answer_path.parent.name
        if not year_dir.isdigit():
            continue
        year = int(year_dir)
        if year > end_year:
            continue
        text = answer_path.read_text(encoding="utf-8")
        if notice not in text:
            continue
        for block in text.split("### 第 ")[1:]:
            heading, _, body = block.partition(" 题")
            if not heading.isdigit() or notice not in body:
                continue
            hits.setdefault(year, []).append(int(heading))
    return hits


def _compact_numbers(numbers: list[int]) -> str:
    if not numbers:
        return ""
    values = sorted(set(numbers))
    ranges: list[str] = []
    start = prev = values[0]
    for value in values[1:]:
        if value == prev + 1:
            prev = value
            continue
        ranges.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = value
    ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return "、".join(ranges)


def _append_hit_section(lines: list[str], title: str, hits: dict[int, list[int]], note: str | None = None) -> None:
    lines.append(f"## {title}")
    if note:
        lines.append(note)
        lines.append("")
    if not hits:
        lines.append("无")
    else:
        for year in sorted(hits):
            lines.append(f"- {year}：第 {_compact_numbers(hits[year])} 题")
    lines.append("")


def write_uncertainty_markdown(math1_root: Path, output_path: Path, end_year: int) -> None:
    source_missing = _question_hits_by_notice(
        math1_root,
        "未在用户指定来源目录中找到本年份答案解析 PDF",
        end_year,
    )
    no_detail = _question_hits_by_notice(math1_root, "源文件名标明", end_year)
    for year, nums in _question_hits_by_notice(math1_root, "未提供逐题详细解析", end_year).items():
        no_detail.setdefault(year, []).extend(nums)
    not_covered = _question_hits_by_notice(math1_root, "未能从来源 PDF 中稳定切出本题解析", end_year)
    page_fallback = _question_hits_by_notice(math1_root, "按题号位置映射到来源页 OCR 文本", end_year)
    ocr_missing = _question_hits_by_notice(math1_root, "源页 OCR 漏识别该小题编号或正文", end_year)

    lines = [
        "# 数一答案解析人工复核清单",
        "",
        "这份清单只列需要人工看一眼的地方；`answers.md` 和单题卡里已经写入了对应说明。",
        "",
    ]
    _append_hit_section(
        lines,
        "A. 源文件缺失",
        source_missing,
        "这些年份/题号在用户指定的答案解析来源中没有找到对应 PDF。",
    )
    _append_hit_section(
        lines,
        "B. 源文件本身没有逐题详解",
        no_detail,
        "这些来源只能确认答案速查，不能从源文件补出真正的详细解析。",
    )
    _append_hit_section(
        lines,
        "C. 来源 PDF 未覆盖或无法稳定切出",
        not_covered,
        "这些题在当前来源 PDF 中未稳定切出解析，建议补源或看原卷。",
    )
    _append_hit_section(
        lines,
        "D. 按来源页位置低置信兜底",
        page_fallback,
        "这些题已放入相邻来源页 OCR 文本，但题号对应需要人工核对。",
    )
    _append_hit_section(
        lines,
        "E. OCR 漏识别小题编号或正文",
        ocr_missing,
        "这些题所在大题结构被保留，但 OCR 没稳定识别到小题编号或正文。",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Math 1 answer explanations from source PDFs.")
    parser.add_argument("--math1-root", type=Path, default=DEFAULT_MATH1_ROOT)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--pdf-2023", type=Path, default=DEFAULT_2023_PDF)
    parser.add_argument("--pdf-2024", type=Path, default=DEFAULT_2024_PDF)
    parser.add_argument("--start-year", type=int, default=1987)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--years", nargs="*", type=int)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--no-ocr", action="store_true")
    parser.add_argument("--no-rebuild-cards", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_MATH1_ROOT / "math1_answer_explanation_import_report.json")
    parser.add_argument(
        "--uncertainty-report",
        type=Path,
        default=DEFAULT_MATH1_ROOT / "math1_answer_explanation_uncertainties.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _add_runtime_dll_paths()
    years = args.years if args.years else list(range(args.start_year, args.end_year + 1))
    reports: list[YearReport] = []
    for year in years:
        report = process_year(
            year=year,
            math1_root=args.math1_root,
            source_dir=args.source_dir,
            pdf_2023=args.pdf_2023,
            pdf_2024=args.pdf_2024,
            dpi=args.dpi,
            use_ocr=not args.no_ocr,
            rebuild_cards=not args.no_rebuild_cards,
        )
        reports.append(report)
        print(
            f"{year}: mode={report.extraction_mode} "
            f"extracted={report.extracted_count}/{report.question_count} "
            f"warnings={len(report.warnings)}"
        )

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps([report.__dict__ for report in reports], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_uncertainty_markdown(args.math1_root, args.uncertainty_report, args.end_year)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
