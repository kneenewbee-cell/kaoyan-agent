# AI Plan Execution Feedback v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make accepted AI review-plan tasks explainable, executable, and traceable from the review workbench.

**Architecture:** Keep AI planning draft generation unchanged. Extend the explicit commit path so tasks created from an AI plan carry plan metadata, source labels, and reasons. Update the review workbench rendering to show those fields, keep one unified start action, and make future tasks easier to scan by due date.

**Tech Stack:** Python standard library, FastAPI router in `materials/system_practice_review_api.py`, JSONL user records in `materials/system_practice_review.py`, vanilla JS/CSS frontend, unittest tests.

## Global Constraints

- Do not refactor unrelated materials ingestion, raw data, or QA code.
- AI planning remains draft-only until the user explicitly commits selected tasks.
- System questions remain readonly; only user-layer review task records are written.
- Existing review task actions must keep working: start, complete, postpone, cancel, restore, delete.

---

### Task 1: Persist AI Plan Metadata on Accepted Review Tasks

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: existing `SystemPracticeReviewStore.create_review_tasks_from_ai_plan(...)`.
- Produces: review tasks with `created_from="ai_plan"`, `plan_id`, `plan_mode`, `plan_model`, `plan_source`, `plan_batch_title`, `plan_reason`, and `source_label`.

Steps:
- [ ] Add a failing unit test committing an AI plan item with `plan_id`, `mode`, and `draft.model`, then assert the created task carries AI plan metadata.
- [ ] Run the targeted test and confirm it fails because metadata is absent or incomplete.
- [ ] Extend `create_review_tasks_from_ai_plan` to copy commit-level plan metadata and item reason into every created task.
- [ ] Run the targeted test and confirm it passes.

### Task 2: Render AI Plan Provenance and Unified Start

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: review task metadata from Task 1.
- Produces: task cards that show AI plan source, mode, batch id, reason, and one `开始复习` action for pending tasks.

Steps:
- [ ] Add failing frontend static assertions for `来自 AI 规划`, `plan_mode`, `plan_reason`, and the unified start label.
- [ ] Run the frontend test and confirm it fails if copy/rendering is missing.
- [ ] Update review task rendering helpers to show a compact provenance row and keep one start action.
- [ ] Add CSS for the provenance row and plan chips.
- [ ] Run the frontend test and confirm it passes.

### Task 3: Future Task Scanability

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: existing future date grouping.
- Produces: future date groups with clearer date headers, counts, nearest-three expansion, and a stronger focus pulse after shortcut jumps.

Steps:
- [ ] Add failing frontend static assertions for clearer date grouping and stronger focus class.
- [ ] Update future-group rendering to show date, weekday, count, and nearest-date hint.
- [ ] Strengthen focus pulse CSS without changing page structure.
- [ ] Run frontend tests.

### Task 4: Verification

Steps:
- [ ] Run targeted backend tests for AI plan commit.
- [ ] Run frontend static tests.
- [ ] Run `node --check web/app.js`.
- [ ] Report remaining gaps, especially whether product-design visual audit was run.
