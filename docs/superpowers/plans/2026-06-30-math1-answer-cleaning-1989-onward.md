# Math1 Answer Cleaning 1989 Onward Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean and complete Math 1 answer explanations from 1989 onward with the same standard used for the repaired 1988 files.

**Architecture:** Process one year at a time. For each year, use the question text as the anchor, use answer-page images as the source when available, and write clean Markdown explanations; if the source answer lacks an explanation, derive one from the question and record the reasoning directly in the explanation rather than leaving placeholders.

**Tech Stack:** Markdown data files, JSONL question index, local rendered PDF page images, PowerShell/Python verification scripts.

---

### Task 1: Per-Year Source Audit

**Files:**
- Read: `E:\python_project\data\raw\math\exam_papers\math1\<year>\math1_<year>_questions.md`
- Read: `E:\python_project\data\raw\math\exam_papers\math1\<year>\math1_<year>_answers.md`
- Read: `E:\python_project\data\raw\math\exam_papers\math1\<year>\questions.jsonl`
- Read: `E:\python_project\data\raw\math\exam_papers\math1\<year>\images\answer_pages\*.png`

- [ ] **Step 1: Count expected questions**

Run a JSONL count and confirm question numbers are continuous after removing Math 1 paper-II-only items.

- [ ] **Step 2: Inspect source answer pages**

Open the answer-page images for the year and identify whether each question has a printed answer, explanation, or only a short final answer.

- [ ] **Step 3: Mark source conflicts**

When a printed answer conflicts with the question and mathematical derivation, write the corrected answer and include the derivation that explains why the printed source is not used.

### Task 2: Clean Year Answer Markdown

**Files:**
- Modify: `E:\python_project\data\raw\math\exam_papers\math1\<year>\math1_<year>_answers.md`

- [ ] **Step 1: Rewrite answer quick table**

Use confirmed answer values, not `见解析` when a short answer is available.

- [ ] **Step 2: Rewrite detailed explanations**

Each section must contain exactly one question's solution, with readable LaTeX and no OCR fragments, confidence notes, or cross-question leakage.

- [ ] **Step 3: Normalize formula style**

Use `\frac{a}{b}`, `\begin{pmatrix}`, `\begin{cases}`, and aligned display equations where useful. Avoid compact forms like `\frac12` or `\frac32` in final cleaned Markdown.

### Task 3: Sync Single-Question Cards And JSONL

**Files:**
- Modify: `E:\python_project\data\raw\math\exam_papers\math1\<year>\questions\q*.md`
- Modify: `E:\python_project\data\raw\math\exam_papers\math1\<year>\questions.jsonl`
- Modify: `E:\python_project\data\raw\math\exam_papers\math1\<year>\paper_manifest.json`

- [ ] **Step 1: Update card answers**

For each card, set `answer_status: available` and `explanation_status: available` when the cleaned answer has been written.

- [ ] **Step 2: Update card explanation**

Replace OCR fragments with the same cleaned explanation used in the total answer file.

- [ ] **Step 3: Update JSONL**

Mirror the answer and explanation fields from the cards. Write JSON with UTF-8 and `ensure_ascii=False`.

- [ ] **Step 4: Update manifest**

Keep `question_count`, `explanation_count`, and `question_ids` consistent with `questions.jsonl` and card files.

### Task 4: Verification

**Files:**
- Verify: `E:\python_project\data\raw\math\exam_papers\math1\<year>\`

- [ ] **Step 1: Count consistency**

Confirm `questions.jsonl` rows, `paper_manifest.json` count, and `questions/q*.md` count match.

- [ ] **Step 2: Residual noise scan**

Search for `置信度：low`, `OCR 漏识别`, `旧卷按大题`, `待核对`, `待人工确认`, `\frac12`, `\frac32`, and obvious `???` encoding damage.

- [ ] **Step 3: Spot-check high-risk formulas**

Inspect any source-answer conflicts, probability transformations, series endpoint tests, and matrix computations before moving to the next year.
