# System Review Backend V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make system review tasks support the planning page workflow: inherited subject metadata, duplicate prevention, filtering, summary counts, and full task actions.

**Architecture:** Extend the existing JSONL-backed `SystemPracticeReviewStore` rather than introducing a database. Review tasks remain user-layer records under `data/users/{user_id}/system_library/`, while public system questions stay read-only.

**Tech Stack:** Python, FastAPI, unittest, local JSONL persistence.

---

### Task 1: Review Task Metadata And Duplicate Rule

**Files:**
- Modify: `tests/test_system_practice_review.py`
- Modify: `materials/system_practice_review.py`

- [x] Add a failing test that creates the same question review task twice for the same date and asserts the same task is returned once.
- [x] Add a failing test that verifies a question review task inherits `subject`, `exam_type`, `library_name`, and `source_title`.
- [x] Implement metadata inheritance for question and practice-set targets.
- [x] Implement duplicate detection by `target_type + target_id + due_at`.
- [x] Run `python -m unittest tests.test_system_practice_review`.

### Task 2: Review Task Filtering And Summary

**Files:**
- Modify: `tests/test_system_practice_review.py`
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`

- [x] Add failing tests for `subject`, `target_type`, `date_group`, and keyword filtering.
- [x] Add failing API test for `/review-tasks/summary`.
- [x] Implement filters in `list_review_tasks`.
- [x] Implement `review_task_summary`.
- [x] Add API query parameters and summary endpoint.
- [x] Run `python -m unittest tests.test_system_practice_review`.

### Task 3: Task Actions

**Files:**
- Modify: `tests/test_system_practice_review.py`
- Modify: `materials/system_practice_review.py`

- [x] Add failing tests for cancel, restore, postpone, complete, and delete behavior through `update_review_task` and `delete_review_task`.
- [x] Implement `cancelled_at`, `completed_at`, and `updated_at` fields consistently.
- [x] Keep `DELETE` as physical deletion.
- [x] Run `python -m unittest tests.test_system_practice_review`.
