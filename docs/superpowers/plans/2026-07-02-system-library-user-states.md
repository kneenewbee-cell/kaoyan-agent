# System Library User States Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist each user's personal state for system-library questions under `data/users/{user_id}/system_library/question_states.jsonl`.

**Architecture:** Keep public system question content in `data/raw/...`; add a small user-state repository that reads and writes only personal overlays. API list/detail responses merge `personal_state`, and a PATCH endpoint updates the overlay. The frontend stops treating system question state as browser-only memory and saves changes through the API.

**Tech Stack:** Python stdlib JSONL storage, FastAPI routes in `materials/api.py`, vanilla JS frontend in `web/app.js`, unittest coverage.

---

### Task 1: User State Repository

**Files:**
- Create: `materials/user_state.py`
- Test: `tests/test_user_system_state.py`

- [ ] Write failing tests for default state, update persistence, and path location under `data/users/{user_id}/system_library/question_states.jsonl`.
- [ ] Implement `UserSystemQuestionStateStore` with safe `user_id` and `question_id`, default state, JSONL read/write, and partial patch normalization.
- [ ] Run `python -m unittest tests.test_user_system_state`.

### Task 2: API Merge And Patch

**Files:**
- Modify: `materials/api.py`
- Test: `tests/test_system_library.py`

- [ ] Write failing tests for `PATCH /api/materials/system/questions/{question_id}/state` and for list/detail responses containing `personal_state`.
- [ ] Implement API merge helpers and PATCH route. Keep `user_id` from query/header; do not alter system question content.
- [ ] Run `python -m unittest tests.test_system_library tests.test_user_system_state`.

### Task 3: Frontend Persistence

**Files:**
- Modify: `web/app.js`
- Modify: `web/index.html`
- Test: `tests/test_system_library_frontend.py`

- [ ] Write failing frontend source tests for `saveSystemQuestionState`, `personal_state` hydration, and `user_id` propagation in system library fetches.
- [ ] Replace local-only state toggles with optimistic PATCH saves and hydrate `systemState.userState` from API `personal_state`.
- [ ] Bump static asset query string.
- [ ] Run `python -m unittest tests.test_system_library_frontend` and `node --check web/app.js`.

### Task 4: Verification

**Files:**
- No new files.

- [ ] Run `python -m compileall materials scripts tests`.
- [ ] Run `python -m unittest tests.test_user_system_state tests.test_system_library tests.test_system_library_frontend`.
- [ ] Confirm no `qa/` files were edited by this feature.
