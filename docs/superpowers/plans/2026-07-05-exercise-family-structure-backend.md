# Exercise Family Structure Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve uploaded `exercise` materials by recognizing problem/example structure through the existing `heading_families + relation_hints` system, producing problem-level diagnostics and chunk metadata without adding hard sub-type routing or frontend changes.

**Architecture:** Keep `material_type=exercise` as the only user-facing type. Strengthen exercise-oriented family guidance and local validation, then add a backend-only `exercise_structure` analysis pass after markdown cleaning and before chunking. Chunking remains generic but can prefer validated problem groups when provided.

**Tech Stack:** Python standard library, existing `materials.postprocess` strategy system, existing dataclass schemas, `unittest`, current CLI/API ingestion pipeline.

---

## Scope

In scope:

- Backend only.
- No new user-facing material type.
- No hard routing by `exam_paper`, `worked_examples`, `problem_set`, or `wrong_book_like`.
- Add exercise family guidance to the LLM strategy prompt.
- Add local exercise structure analysis and quality metrics.
- Add optional problem-group-aware chunking metadata.
- Keep existing `quality_status` semantics unchanged.

Out of scope:

- Frontend UI changes.
- PDF/MinerU parser rewrite.
- OCR/VLM expansion.
- Real database/vector-store migration.
- QA module changes.

---

## File Structure

- Create `materials/postprocess/exercise_structure.py`
  - Owns problem/example group extraction from cleaned markdown.
  - Produces a serializable report with `status`, `confidence`, `problem_groups`, label counts, suspicious marker counts, and warnings.
  - Does not rewrite markdown.

- Modify `materials/postprocess/qwen_strategy_client.py`
  - Adds exercise/problem-family prompt guidance.
  - Reinforces that solution labels stay local labels, not heading families.
  - Reinforces option/formula-marker exclusions.

- Modify `materials/chunking/chunker.py`
  - Accepts optional `problem_groups`.
  - Uses problem-group line ranges as preferred sections when there are enough validated groups.
  - Adds `problem_id`, `problem_index`, `problem_title`, `problem_kind`, and `problem_part_index` to chunk metadata.

- Modify `materials/service.py`
  - Runs exercise structure analysis after postprocess and before chunking for `material_type=exercise`.
  - Passes groups to chunker.
  - Writes `exercise_structure` to `parse_report.metrics`, `manifest.metadata`, and `pipeline_events.jsonl`.

- Modify `materials/quality/report.py` only if needed
  - Prefer not changing generic quality scoring.
  - If adding a helper is cleaner, keep it optional and do not alter `overall_confidence`.

- Modify tests:
  - `tests/test_raw_markdown_cleaning.py`
  - Create `tests/test_exercise_structure.py`
  - Add focused service/chunk assertions to `tests/test_materials_mvp.py`

---

### Task 1: Add Exercise Structure Analyzer

**Files:**
- Create: `materials/postprocess/exercise_structure.py`
- Test: `tests/test_exercise_structure.py`

- [ ] **Step 1: Write failing tests for problem group extraction**

Create `tests/test_exercise_structure.py`:

```python
from __future__ import annotations

import unittest

from materials.postprocess.exercise_structure import analyze_exercise_structure


class ExerciseStructureTest(unittest.TestCase):
    def test_extracts_problem_groups_and_solution_labels(self) -> None:
        markdown = """# 2023 math paper

## 一、选择题

### (1) 设函数 f(x) 连续，求极限

A. 0
B. 1

**解析：** 先化简再代入。

### (2) 已知矩阵 A，求行列式

**答案：** 2
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["status"], "high")
        self.assertEqual(report["problem_count"], 2)
        self.assertEqual(report["solution_label_count"], 2)
        self.assertEqual(report["problem_groups"][0]["problem_id"], "problem_001")
        self.assertEqual(report["problem_groups"][0]["problem_index"], 1)
        self.assertEqual(report["problem_groups"][0]["problem_kind"], "question")
        self.assertEqual(report["problem_groups"][0]["title"], "(1) 设函数 f(x) 连续，求极限")
        self.assertLess(report["problem_groups"][0]["start_line"], report["problem_groups"][0]["end_line"])

    def test_ignores_non_exercise_materials(self) -> None:
        report = analyze_exercise_structure("## 1. 极限定义\n\n正文", material_type="lecture")

        self.assertEqual(report["status"], "skipped")
        self.assertEqual(report["problem_count"], 0)
        self.assertEqual(report["problem_groups"], [])

    def test_does_not_treat_options_as_problem_groups(self) -> None:
        markdown = """# exercise

## 第 1 题

A. 正确选项
B. 干扰项
C. 干扰项
D. 干扰项

**答案：** A
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 1)
        self.assertEqual(report["suspicious_option_marker_count"], 4)
        self.assertEqual(report["problem_groups"][0]["problem_id"], "problem_001")

    def test_reports_low_when_no_problem_groups_are_found(self) -> None:
        markdown = "# 习题资料\n\n这是一段没有题号的普通正文。\n\n**解析：** 只有解析没有题目。"

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["status"], "low")
        self.assertEqual(report["problem_count"], 0)
        self.assertEqual(report["solution_label_count"], 1)
        self.assertIn("exercise_no_problem_groups", report["warnings"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m unittest tests.test_exercise_structure
```

Expected:

```text
ModuleNotFoundError: No module named 'materials.postprocess.exercise_structure'
```

- [ ] **Step 3: Implement analyzer**

Create `materials/postprocess/exercise_structure.py`:

```python
from __future__ import annotations

import re
from typing import Any


HEADING_RE = re.compile(r"^(?P<marker>#{1,6})\s+(?P<title>.+?)\s*$")
QUESTION_HEADING_RE = re.compile(
    r"^(?:"
    r"第\s*(?P<q1>\d{1,3}|[一二三四五六七八九十百千万两]+)\s*题"
    r"|[（(]\s*(?P<q2>\d{1,3})\s*[）)]"
    r"|(?P<q3>\d{1,3})[.．、]\s*"
    r")\S*"
)
EXAMPLE_HEADING_RE = re.compile(
    r"^(?:"
    r"例\s*(?P<e1>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|例题\s*(?P<e2>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|典型例题\s*(?P<e3>\d{1,3}|[一二三四五六七八九十百千万两]+)"
    r"|【\s*例题\s*】"
    r")"
)
SOLUTION_LABEL_RE = re.compile(
    r"^\*\*(?:解|答|答案|解析|分析|证明|评注|点评|点拨|提示|说明|变式|注意)[:：]\*\*"
)
OPTION_MARKER_RE = re.compile(r"^[A-D][.．、]\s*\S+")
FORMULA_NUMBER_RE = re.compile(r"^[（(]\s*\d+(?:[.．]\d+)+\s*[）)]\s*$")


def _status(problem_count: int, solution_count: int, warnings: list[str]) -> tuple[str, float]:
    if problem_count >= 2:
        return "high", 0.9
    if problem_count == 1:
        return "medium", 0.72
    if solution_count:
        warnings.append("exercise_no_problem_groups")
        return "low", 0.45
    warnings.append("exercise_no_problem_signal")
    return "failed", 0.2


def _problem_kind(title: str) -> str | None:
    if FORMULA_NUMBER_RE.match(title.strip()):
        return None
    if EXAMPLE_HEADING_RE.match(title.strip()):
        return "example"
    if QUESTION_HEADING_RE.match(title.strip()):
        return "question"
    return None


def _heading_path_for_line(headings: list[dict[str, Any]], line_no: int) -> list[str]:
    stack: list[dict[str, Any]] = []
    for heading in headings:
        if heading["line_no"] > line_no:
            break
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        stack.append(heading)
    return [item["title"] for item in stack]


def analyze_exercise_structure(markdown: str, *, material_type: str) -> dict[str, Any]:
    if material_type != "exercise":
        return {
            "status": "skipped",
            "confidence": 0.0,
            "problem_count": 0,
            "solution_label_count": 0,
            "suspicious_option_marker_count": 0,
            "problem_groups": [],
            "warnings": [],
        }

    lines = markdown.splitlines()
    headings: list[dict[str, Any]] = []
    problem_starts: list[dict[str, Any]] = []
    solution_label_count = 0
    option_marker_count = 0
    warnings: list[str] = []

    for index, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            title = heading_match.group("title").strip()
            level = len(heading_match.group("marker"))
            heading = {"line_no": index, "level": level, "title": title}
            headings.append(heading)
            kind = _problem_kind(title)
            if kind is not None:
                problem_starts.append({**heading, "problem_kind": kind})
        if SOLUTION_LABEL_RE.match(stripped):
            solution_label_count += 1
        if OPTION_MARKER_RE.match(stripped):
            option_marker_count += 1

    problem_groups: list[dict[str, Any]] = []
    for group_index, start in enumerate(problem_starts, start=1):
        next_start_line = (
            problem_starts[group_index]["line_no"]
            if group_index < len(problem_starts)
            else len(lines) + 1
        )
        end_line = max(start["line_no"], next_start_line - 1)
        problem_groups.append(
            {
                "problem_id": f"problem_{group_index:03d}",
                "problem_index": group_index,
                "problem_kind": start["problem_kind"],
                "title": start["title"],
                "start_line": start["line_no"],
                "end_line": end_line,
                "heading_path": _heading_path_for_line(headings, start["line_no"]),
            }
        )

    status, confidence = _status(len(problem_groups), solution_label_count, warnings)
    return {
        "status": status,
        "confidence": confidence,
        "problem_count": len(problem_groups),
        "solution_label_count": solution_label_count,
        "suspicious_option_marker_count": option_marker_count,
        "problem_groups": problem_groups,
        "warnings": sorted(set(warnings)),
    }
```

- [ ] **Step 4: Run analyzer tests**

Run:

```bash
python -m unittest tests.test_exercise_structure
```

Expected:

```text
OK
```

---

### Task 2: Strengthen Exercise Family Strategy Guidance

**Files:**
- Modify: `materials/postprocess/qwen_strategy_client.py`
- Test: `tests/test_raw_markdown_cleaning.py`

- [ ] **Step 1: Add tests for exercise heading behavior**

Append to `tests/test_raw_markdown_cleaning.py`:

```python
    def test_exercise_family_promotes_questions_but_not_solution_labels_or_options(self) -> None:
        payload = family_strategy(
            {
                "id": "exam_section",
                "kind": "major_section",
                "anchors": [],
                "ordinal_styles": ["chinese"],
                "ordinal_required": True,
                "separators": ["、"],
                "examples": ["一、选择题", "二、填空题"],
                "min_repeats": 1,
            },
            {
                "id": "question_item",
                "kind": "item",
                "anchors": [],
                "ordinal_styles": ["paren_arabic"],
                "ordinal_required": True,
                "examples": ["(1) 设函数 f(x) 连续", "(2) 已知矩阵 A"],
                "parent_hints": ["exam_section"],
                "min_repeats": 2,
            },
        )
        payload["document_profile"]["document_type"] = "exercise_notes"
        payload["relation_hints"] = [
            {
                "relation_type": "direct_parent",
                "parent": "exam_section",
                "child": "question_item",
                "score": 90,
                "certainty": "strong",
                "scope": "body",
            }
        ]
        markdown = """# 试题

一、选择题

(1) 设函数 f(x) 连续，求极限
A. 0
B. 1
解：先化简。

(2) 已知矩阵 A，求行列式
答案：2
"""

        result = clean_with_strategy(markdown, payload)

        self.assertIn("## 一、选择题", result.cleaned_markdown)
        self.assertIn("### (1) 设函数 f(x) 连续，求极限", result.cleaned_markdown)
        self.assertIn("### (2) 已知矩阵 A，求行列式", result.cleaned_markdown)
        self.assertNotIn("### A. 0", result.cleaned_markdown)
        self.assertIn("**解：** 先化简。", result.cleaned_markdown)
        self.assertIn("**答案：** 2", result.cleaned_markdown)
```

- [ ] **Step 2: Run the focused test**

Run:

```bash
python -m unittest tests.test_raw_markdown_cleaning.RawMarkdownCleaningTest.test_exercise_family_promotes_questions_but_not_solution_labels_or_options
```

Expected:

```text
FAIL
```

The exact failure may differ depending on current cleaner behavior. If it already passes, keep the test as regression coverage and continue with prompt guidance.

- [ ] **Step 3: Add exercise prompt guidance**

In `materials/postprocess/qwen_strategy_client.py`, add this prompt block after the local solution label constraints:

```python
SYSTEM_PROMPT += """
Exercise/problem-family guidance:
- For exercise materials, keep the same heading_families mechanism; do not infer hard subtypes such as exam_paper,
  worked_examples, problem_set, or wrong_book_like as routing fields.
- Use reusable family ids such as exam_section, problem_group, question_item, example_item, and variant_item when the
  document has repeated evidence.
- True problem/example boundaries may look like "第1题", "(1) 题干", "1. 题干", "例1", "例题2", "典型例题3".
- Section boundaries may look like "一、选择题", "二、填空题", "三、解答题"; express them as ordinary heading_families
  with relation_hints to child question/example families when evidence is strong.
- Never make answer/solution labels into heading_families: 解, 答, 答案, 解析, 分析, 证明, 评注, 点评, 点拨,
  提示, 说明, 注意, 变式. These are local labels inside the nearest problem/example group.
- Never treat options A/B/C/D, formula numbers such as (1.1), page numbers, or isolated metadata badges as question
  headings.
- If a problem marker appears only once, leave it out of heading_families unless the surrounding context clearly shows
  it is the only problem in a short document.
"""
```

- [ ] **Step 4: If the focused cleaner test failed, make minimal local cleaner fix**

If options or solution labels were promoted, update `materials/postprocess/strategy_cleaner.py` with focused guards:

```python
OPTION_LINE_RE = re.compile(r"^[A-D][.．、]\s*\S+")
FORMULA_NUMBER_ONLY_RE = re.compile(r"^[（(]\s*\d+(?:[.．]\d+)+\s*[）)]\s*$")


def _is_exercise_non_heading_line(title: str) -> bool:
    stripped = title.strip()
    return bool(OPTION_LINE_RE.match(stripped) or FORMULA_NUMBER_ONLY_RE.match(stripped))
```

Then call it before `_match_heading_family(...)` for plain lines and existing markdown headings:

```python
if document_type == "exercise_notes" and _is_exercise_non_heading_line(match_title):
    local_label_matches.append(
        {
            "line_no": line_no,
            "raw": raw,
            "converted": stripped,
            "rule": "exercise_non_heading_marker_preserved",
            "confidence": 0.9,
        }
    )
    output.append(stripped)
    continue
```

Use the existing local variable names in each branch. Do not add a broad rewrite.

- [ ] **Step 5: Run raw cleaner tests**

Run:

```bash
python -m unittest tests.test_raw_markdown_cleaning
```

Expected:

```text
OK
```

---

### Task 3: Make Chunker Problem-Group Aware

**Files:**
- Modify: `materials/chunking/chunker.py`
- Test: `tests/test_exercise_structure.py`

- [ ] **Step 1: Add failing chunk metadata test**

Append to `tests/test_exercise_structure.py`:

```python
from materials.chunking.chunker import chunk_markdown


class ExerciseProblemChunkingTest(unittest.TestCase):
    def test_chunker_prefers_problem_groups_and_adds_problem_metadata(self) -> None:
        markdown = """# 试题

## 一、选择题

### (1) 第一题

题干一。

### (2) 第二题

题干二。
"""
        exercise_report = analyze_exercise_structure(markdown, material_type="exercise")

        chunks = chunk_markdown(
            markdown,
            "mat_exercise",
            "tester",
            problem_groups=exercise_report["problem_groups"],
        )

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["problem_id"], "problem_001")
        self.assertEqual(chunks[0].metadata["problem_index"], 1)
        self.assertEqual(chunks[0].metadata["problem_kind"], "question")
        self.assertEqual(chunks[1].metadata["problem_id"], "problem_002")
        self.assertEqual(chunks[1].metadata["problem_part_index"], 1)
```

- [ ] **Step 2: Run focused test to verify it fails**

Run:

```bash
python -m unittest tests.test_exercise_structure.ExerciseProblemChunkingTest.test_chunker_prefers_problem_groups_and_adds_problem_metadata
```

Expected:

```text
TypeError: chunk_markdown() got an unexpected keyword argument 'problem_groups'
```

- [ ] **Step 3: Add optional problem group sections**

Modify `materials/chunking/chunker.py`:

```python
def _problem_group_sections(markdown: str, problem_groups: list[dict[str, Any]] | None) -> list[_MainSection]:
    if not problem_groups or len(problem_groups) < 2:
        return []
    lines = markdown.splitlines()
    sections: list[_MainSection] = []
    for group in problem_groups:
        try:
            start = max(int(group["start_line"]) - 1, 0)
            end = min(int(group["end_line"]) - 1, len(lines) - 1)
        except (KeyError, TypeError, ValueError):
            continue
        if start < 0 or end < start or start >= len(lines):
            continue
        content = "\n".join(lines[start : end + 1]).strip()
        if not content:
            continue
        title = str(group.get("title") or "").strip() or None
        heading_path = list(group.get("heading_path") or ([title] if title else []))
        section = _MainSection(
            title=title,
            heading_path=heading_path,
            content=content,
            start_line=start,
            end_line=end,
            level=3,
            split_reason="problem_group",
        )
        section.problem_group = group
        sections.append(section)
    return sections
```

Because `_MainSection` is currently a dataclass without `problem_group`, add the field:

```python
@dataclass
class _MainSection:
    title: str | None
    heading_path: list[str]
    content: str
    start_line: int
    end_line: int
    level: int = 0
    split_reason: str = "section"
    problem_group: dict[str, Any] | None = None
```

Update signatures:

```python
def chunk_markdown(
    markdown: str,
    material_id: str,
    user_id: str,
    max_tokens: int = MAX_CHUNK_TOKENS,
    *,
    strategy: dict | None = None,
    document_zones: Any | None = None,
    problem_groups: list[dict[str, Any]] | None = None,
) -> list[Chunk]:
```

Inside `chunk_markdown`, replace initial section assignment:

```python
sections = _problem_group_sections(markdown, problem_groups)
if not sections:
    sections = _split_main_sections(markdown, main_level, document_zones=document_zones)
```

Add problem metadata when creating chunks:

```python
problem_metadata: dict[str, Any] = {}
if section.problem_group:
    problem_metadata = {
        "problem_id": section.problem_group.get("problem_id"),
        "problem_index": section.problem_group.get("problem_index"),
        "problem_title": section.problem_group.get("title"),
        "problem_kind": section.problem_group.get("problem_kind"),
        "problem_part_index": part_index,
    }
```

Merge it into chunk metadata:

```python
metadata={
    "start_line": section.start_line,
    "end_line": section.end_line,
    "level": section.level or 1,
    "effective_main_level": effective_main_level,
    "part_index": part_index,
    "split_reason": split_reason,
    **problem_metadata,
},
```

Update `chunk_markdown_file` signature and call:

```python
def chunk_markdown_file(..., problem_groups: list[dict[str, Any]] | None = None) -> list[Chunk]:
    return chunk_markdown(..., problem_groups=problem_groups)
```

- [ ] **Step 4: Run chunking tests**

Run:

```bash
python -m unittest tests.test_exercise_structure
python -m unittest tests.test_raw_markdown_cleaning
```

Expected:

```text
OK
```

---

### Task 4: Integrate Exercise Structure Into Ingestion Service

**Files:**
- Modify: `materials/service.py`
- Test: `tests/test_materials_mvp.py`

- [ ] **Step 1: Add failing service integration test**

Append to `tests/test_materials_mvp.py`:

```python
    def test_exercise_ingest_writes_structure_report_and_problem_chunk_metadata(self) -> None:
        source = self.base_dir / "exercise_examples.md"
        source.write_text(
            "# 例题资料\n\n"
            "## 一、选择题\n\n"
            "### (1) 设函数 f(x) 连续，求极限\n\n"
            "A. 0\nB. 1\n\n"
            "**解析：** 先化简再代入。\n\n"
            "### (2) 已知矩阵 A，求行列式\n\n"
            "**答案：** 2\n",
            encoding="utf-8",
        )

        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="exercise",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertIsNone(result.error)
        material_dir = MaterialStorage(self.base_dir).material_dir("tester", result.material_id)
        report = json.loads((material_dir / "parsed" / "parse_report.json").read_text(encoding="utf-8"))
        manifest = json.loads((material_dir / "manifest.json").read_text(encoding="utf-8"))
        chunks = [
            json.loads(line)
            for line in (material_dir / "chunks" / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        self.assertEqual(report["metrics"]["exercise_structure"]["problem_count"], 2)
        self.assertEqual(report["metrics"]["exercise_structure"]["status"], "high")
        self.assertEqual(manifest["metadata"]["exercise_structure"]["problem_count"], 2)
        self.assertTrue(any(chunk["metadata"].get("problem_id") == "problem_001" for chunk in chunks))
```

- [ ] **Step 2: Run focused test to verify it fails**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_exercise_ingest_writes_structure_report_and_problem_chunk_metadata
```

Expected:

```text
FAIL: 'exercise_structure' not found
```

- [ ] **Step 3: Integrate analyzer in service**

In `materials/service.py`, import:

```python
from .postprocess.exercise_structure import analyze_exercise_structure
```

Before chunking, after final `markdown_text` is settled and after `structure_profile` handling, add:

```python
            exercise_structure_report: dict[str, Any] | None = None
            problem_groups: list[dict[str, Any]] | None = None
            if manifest.material_type == MaterialType.EXERCISE:
                exercise_structure_report = analyze_exercise_structure(
                    markdown_text,
                    material_type=manifest.material_type.value,
                )
                problem_groups = list(exercise_structure_report.get("problem_groups") or [])
                extra_metadata["exercise_structure"] = {
                    key: value
                    for key, value in exercise_structure_report.items()
                    if key != "problem_groups"
                }
                pipeline_logger.log(
                    "exercise_structure",
                    "completed",
                    status=exercise_structure_report.get("status"),
                    problem_count=exercise_structure_report.get("problem_count"),
                    solution_label_count=exercise_structure_report.get("solution_label_count"),
                    warning_count=len(exercise_structure_report.get("warnings") or []),
                )
```

When calling `chunk_markdown_file`, pass:

```python
                problem_groups=problem_groups,
```

After `parse_report = build_quality_report(...)`, add:

```python
            if exercise_structure_report is not None:
                parse_report.metrics["exercise_structure"] = exercise_structure_report
                parse_report.warnings = sorted(
                    set(parse_report.warnings + list(exercise_structure_report.get("warnings") or []))
                )
```

Keep `parse_report.quality_status` and `overall_confidence` unchanged.

- [ ] **Step 4: Run integration test**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_exercise_ingest_writes_structure_report_and_problem_chunk_metadata
```

Expected:

```text
OK
```

---

### Task 5: Add Regression Tests For Realistic Exercise Edge Cases

**Files:**
- Modify: `tests/test_exercise_structure.py`
- Modify: `tests/test_raw_markdown_cleaning.py`

- [ ] **Step 1: Add edge-case tests**

Append to `tests/test_exercise_structure.py`:

```python
class ExerciseStructureEdgeCaseTest(unittest.TestCase):
    def test_example_items_are_problem_groups(self) -> None:
        markdown = """# 例题讲义

## 二项分布

### 例1 二项分布的期望

题干。

**解：** 使用公式。

### 例题2 泊松分布近似

题干。

**评注：** 注意条件。
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 2)
        self.assertEqual([group["problem_kind"] for group in report["problem_groups"]], ["example", "example"])
        self.assertEqual(report["solution_label_count"], 2)

    def test_formula_numbers_are_not_problem_groups(self) -> None:
        markdown = """# 公式

## 二项分布

### (1.1)

$E(X)=np$

### (1) 设 X 服从二项分布，求期望

**答案：** np
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 1)
        self.assertEqual(report["problem_groups"][0]["title"], "(1) 设 X 服从二项分布，求期望")
```

- [ ] **Step 2: Run edge-case tests**

Run:

```bash
python -m unittest tests.test_exercise_structure
```

Expected:

```text
OK
```

- [ ] **Step 3: Add q20-style regression test**

Add a raw cleaner regression test that represents a visible `(20)` marker in markdown, not a MinerU-omitted marker:

```python
    def test_exercise_paren_arabic_family_can_promote_question_20_when_present(self) -> None:
        payload = family_strategy(
            {
                "id": "question_item",
                "kind": "item",
                "anchors": [],
                "ordinal_styles": ["paren_arabic"],
                "ordinal_required": True,
                "examples": ["(19) 求曲线积分", "(20) 求二重积分"],
                "min_repeats": 2,
            },
        )
        payload["document_profile"]["document_type"] = "exercise_notes"
        markdown = """# 试题

(19) 求曲线积分

解析：略。

(20) 求二重积分

解析：略。
"""

        result = clean_with_strategy(markdown, payload)

        self.assertIn("## (19) 求曲线积分", result.cleaned_markdown)
        self.assertIn("## (20) 求二重积分", result.cleaned_markdown)
```

- [ ] **Step 4: Run raw cleaner regression**

Run:

```bash
python -m unittest tests.test_raw_markdown_cleaning.RawMarkdownCleaningTest.test_exercise_paren_arabic_family_can_promote_question_20_when_present
```

Expected:

```text
OK
```

If this fails because the cleaner requires a parent section and produces `###`, accept either H2 or H3 by changing assertions to regex:

```python
self.assertRegex(result.cleaned_markdown, r"#{2,3} \(20\) 求二重积分")
```

---

### Task 6: Verify Search Metadata Surfaces Problem Context

**Files:**
- Modify: `tests/test_materials_mvp.py`

- [ ] **Step 1: Add search metadata regression**

Add to `tests/test_materials_mvp.py`:

```python
    def test_exercise_search_result_keeps_problem_metadata(self) -> None:
        source = self.base_dir / "exercise_search.md"
        source.write_text(
            "# 题集\n\n"
            "## 一、选择题\n\n"
            "### (1) 二项分布期望公式\n\n"
            "题干：求 E(X)。\n\n"
            "**答案：** np\n\n"
            "### (2) 泊松分布方差公式\n\n"
            "题干：求 D(X)。\n\n"
            "**答案：** lambda\n",
            encoding="utf-8",
        )
        result = self.service.ingest_file(
            source,
            user_id="tester",
            subject="math",
            material_type="exercise",
            use_llm_cleanup=False,
            enable_vector_index=False,
        )

        self.assertIsNone(result.error)
        search_result = search_user_materials(
            "tester",
            "泊松分布方差公式",
            top_k=3,
            filters={"material_id": result.material_id},
        )

        self.assertGreaterEqual(len(search_result), 1)
        self.assertEqual(search_result[0].metadata.get("problem_id"), "problem_002")
        self.assertEqual(search_result[0].metadata.get("problem_index"), 2)
```

Ensure `search_user_materials` is imported in the test file if not already available:

```python
from materials.search import search_user_materials
```

- [ ] **Step 2: Run focused test**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_exercise_search_result_keeps_problem_metadata
```

Expected:

```text
OK
```

---

### Task 7: Full Verification

**Files:**
- No new files.

- [ ] **Step 1: Run compileall**

Run:

```bash
python -m compileall materials scripts tests
```

Expected:

```text
0 failures
```

- [ ] **Step 2: Run focused materials tests**

Run:

```bash
python -m unittest tests.test_exercise_structure
python -m unittest tests.test_raw_markdown_cleaning
python -m unittest tests.test_materials_mvp
python -m unittest tests.test_materials_vector_index
```

Expected:

```text
OK
```

- [ ] **Step 3: Run AGENTS-required tests**

Run:

```bash
python -m unittest tests.test_formula_cleaner
python -m unittest tests.test_formula_extractor
python -m unittest tests.test_llm_cleaner
python -m unittest tests.test_qwen_formula_client
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"
python -m unittest tests.test_agent_runtime
```

Expected:

```text
All tests OK.
Both ingest commands produce parsed/content.md, parsed/parse_report.json, chunks/chunks.jsonl, and index/search_index.json.
The query command returns relevant chunks.
```

- [ ] **Step 4: Run real exercise smoke tests**

Use one markdown or PDF-derived exercise file that is already available in the workspace. If using the user-provided PDF path, run with explicit `exercise` type:

```bash
python scripts/ingest_material.py --user-id tester --file "D:\百度网盘\高数资料\2023考研数学二真题.pdf" --subject math --material-type exercise
```

Expected:

```text
parse_status: ready
manifest metadata contains exercise_structure
parse_report metrics contains exercise_structure
chunks metadata contains problem_id for problem-group chunks when problem headings are present in cleaned markdown
```

If MinerU omits a problem marker from `content.md`, record it as parser/source loss, not an exercise family failure.

---

## Self-Review Notes

- Spec coverage: The plan implements the selected first approach only: unified family enhancement plus problem group diagnostics. It does not add hard internal routing.
- Frontend: No frontend files are modified. Existing pages continue to work because new information is added to manifest, parse_report, and chunk metadata.
- Quality status: Existing `quality_status` is preserved. Exercise-specific structure quality lives under `metrics.exercise_structure.status`.
- Risk: Problem-group chunking should only activate when at least two groups are detected. Single-problem or uncertain documents fall back to existing heading chunking.
- Parser limitation: If the PDF/MinerU parser drops a question marker before markdown cleaning, this backend structure pass cannot recover it from missing text.

