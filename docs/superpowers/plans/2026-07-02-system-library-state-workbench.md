# System Library State Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reliable personal-state workbench for system-library questions so users can see counts, filter by state, and receive save feedback.

**Architecture:** Keep system question content readonly in `data/raw/...` and personal overlays in `materials.user_state`. Add a small summary endpoint that counts merged personal states for the current system filters, then surface those counts as frontend filter chips. Keep frontend saves optimistic, with a visible pending/saved/error indicator.

**Tech Stack:** FastAPI in `materials/api.py`, JSONL user-state store in `materials/user_state.py`, vanilla JS in `web/app.js`, HTML/CSS in `web/index.html` and `web/styles.css`, unittest source/API coverage.

---

### Task 1: API State Summary

**Files:**
- Modify: `materials/api.py`
- Test: `tests/test_system_library.py`

- [ ] Add a failing API test that patches one question as favorite/learning/noted and verifies `GET /api/materials/system/questions/state-summary` returns counts for `all`, mastery states, `favorite`, `wrong_book`, and `noted` across the current non-status filters.
- [ ] Implement shared collection helpers in `materials/api.py` so the list route and summary route can both scan matching system questions without duplicating pagination loops.
- [ ] Run `python -m unittest tests.test_system_library`.

### Task 2: Frontend Summary Chips

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_library_frontend.py`

- [ ] Add failing source tests that expect `#systemStatusSummary`, `loadSystemStatusSummary`, `data-system-status-chip`, and `.system-status-summary` to exist.
- [ ] Render status chips for all states, load counts from the new API, and make chip clicks set `systemStatusFilter` plus reload page 1.
- [ ] Run `python -m unittest tests.test_system_library_frontend` and `node --check web/app.js`.

### Task 3: Save Feedback

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_library_frontend.py`

- [ ] Add failing source tests that expect `#systemSaveStatus`, `setSystemSaveStatus`, and `system-save-status` classes.
- [ ] Show `saving`, `saved`, and `error` feedback for system state PATCH calls without replacing the existing rollback behavior.
- [ ] Run `python -m unittest tests.test_system_library_frontend` and `node --check web/app.js`.

### Task 4: Verification

**Files:**
- No new production files.

- [ ] Run `python -m compileall materials scripts tests`.
- [ ] Run focused tests for system library state and frontend source checks.
- [ ] Run the project-required materials tests and `.md/.txt` ingest smoke commands.
- [ ] Confirm `qa/` was not modified by this feature.
