# System Question Lightweight Tutor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete single-system-question "Ask AI" loop that uses a lightweight tutor runtime instead of the full QA agent loop.

**Architecture:** Keep system question content and user state in `materials`, but place the direct LLM tutor logic under `qa/tutors/system_question/`. `qa/tutors/system_question/api.py` exposes a QA-owned tutor stream endpoint that loads the question, state, history, and local assets, then delegates to the tutor service. `materials/api.py` remains responsible for system-library list/detail/state/assets only. `web/app.js` switches the question drawer into a temporary tutor mode, streams answers, keeps history in memory only, and can append selected assistant text into the question note.

**Tech Stack:** FastAPI form + SSE streaming, existing OpenAI-compatible Qwen client helpers, plain JavaScript frontend, unittest string/API tests.

---

### Task 1: Backend Tutor Runtime

**Files:**
- Create: `qa/tutors/system_question/service.py`
- Create: `qa/tutors/system_question/api.py`
- Modify: `scripts/web_server.py`
- Test: `tests/test_system_question_tutor.py`
- Test: `tests/test_system_question_tutor_api.py`

- [x] **Step 1: Write failing tests**

Test prompt construction locks the scope boundary: current subject, current question, related topics, and cross-subject refusal rules must be present. API streaming test patches the tutor stream and confirms the new route returns SSE chunks without calling the full QA runtime.

- [x] **Step 2: Implement the tutor module**

Add functions to normalize temporary history, build a compact system prompt, attach image data URLs when present, and stream model chunks directly through the OpenAI-compatible client. Do not import or call `run_standard_message_loop`.

- [x] **Step 3: Add API route**

Add `POST /api/qa/system-questions/{question_id}/tutor/stream`. The route resolves user id, loads question detail and personal state, parses temporary history, resolves safe system asset paths, and streams tutor chunks.

### Task 2: Frontend Temporary Tutor Mode

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `web/index.html`
- Test: `tests/test_system_library_frontend.py`

- [x] **Step 1: Write failing frontend tests**

Tests should assert that `askAiForSystemQuestion` calls the tutor stream endpoint, does not call `submitChatMessage`, does not switch to the ordinary chat session, and includes in-memory tutor history plus selected-text-to-note behavior.

- [x] **Step 2: Implement tutor UI state**

Add `systemTutor` state for active question, message history, streaming status, collapsed context, and selected assistant text. The mode should be temporary and reset when the user returns.

- [x] **Step 3: Wire the drawer and actions**

The existing drawer remains the context rail. Its close button becomes a return button in tutor mode. The Ask AI button starts tutor mode and sends the initial "讲解这道题" request through the new endpoint. Follow-up input streams through the same endpoint with temporary history.

### Task 3: Verification

**Files:**
- No new files.

- [x] **Step 1: Run focused backend tests**

`python -m unittest tests.test_system_question_tutor tests.test_system_question_tutor_api tests.test_system_library`

- [x] **Step 2: Run frontend static tests and syntax check**

`python -m unittest tests.test_system_library_frontend`

`node --check web/app.js`

- [x] **Step 3: Compile changed Python packages**

`python -m compileall qa scripts tests`
