# Practice Grading Data Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a durable practice submission and grading data layer so local grading, on-demand AI grading, user correction, result pages, and later AI planning share one source of truth.

**Architecture:** Extend the existing `SystemPracticeReviewStore` JSONL-backed repository with richer attempt item results. Keep storage behind service methods so the same shape can later move to MySQL without changing frontend calls. Add API endpoints for AI/manual grading overrides, then update the practice result UI to read `final_status`.

**Tech Stack:** Python `unittest`, FastAPI routers, existing `materials/system_practice_review.py`, browser frontend in `web/app.js` and `web/styles.css`.

---

### Task 1: Persist Three-Layer Grading Status

**Files:**
- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] Add tests that submitted attempts store `local_status`, `ai_status`, `final_status`, `judge_method`, `judge_confidence`, and `judge_reason` per question.
- [ ] Update `_grade_practice_attempt` so choice questions are locally `correct/incorrect`, blank questions are locally `correct/incorrect`, and solution questions are `pending_review` with `judge_method=manual`.
- [ ] Keep legacy `status` equal to `final_status` so current frontend calls do not break.
- [ ] Update summary counts to include `partial` and `pending_review`, while keeping `needs_review` and `needs_grading` as compatibility aliases where existing tests need them.

### Task 2: Add AI And Manual Grading Overrides

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Test: `tests/test_system_practice_review.py`

- [ ] Add a store method to apply a grading override for one submitted attempt item.
- [ ] Support `judge_method=ai` and `judge_method=manual`.
- [ ] For fill blanks, AI can turn a local `incorrect` into final `correct`.
- [ ] For solutions, AI can set `partial/correct/incorrect/pending_review` and attach feedback.
- [ ] Add FastAPI endpoint `POST /api/materials/system/practice-attempts/{attempt_id}/items/{question_id}/grade`.

### Task 3: Update Result Page Behavior

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_library_frontend.py` if existing static assertions fit; otherwise verify with browser audit.

- [ ] Render result badges from `final_status`.
- [ ] Show `AI 判分` for blank and solution items.
- [ ] After AI grading succeeds, update the result row in place.
- [ ] Never render `[object Object]`; all answer values pass through a formatter.

### Task 4: Verification And Product Audit

**Files:**
- Use: `tests/test_system_practice_review.py`
- Use: `tests/test_system_library_frontend.py`
- Output screenshots/notes: `E:\temp`

- [ ] Run focused backend tests.
- [ ] Run frontend/static tests.
- [ ] Run broader material/system tests.
- [ ] Use product-design:audit on the practice flow after implementation and save screenshots to `E:\temp`.
