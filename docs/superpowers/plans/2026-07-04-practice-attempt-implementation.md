# Practice Attempt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-version practice attempt flow so a generated practice set can be answered, submitted, checked, and saved as an immutable user practice record.

**Architecture:** Extend the existing `materials/system_practice_review.py` store instead of creating a new subsystem. Add a `practice_attempts.jsonl` user-layer file beside existing `practice_sets.jsonl` and `review_tasks.jsonl`, expose attempt APIs through `materials/system_practice_review_api.py`, then add a frontend practice overlay inside the current system-library workflow UI. Do not touch `qa/` or `data/raw/`.

**Tech Stack:** Python stdlib JSONL storage, FastAPI router, existing `SystemQuestionLibrary`, existing vanilla `web/app.js` UI, `unittest`, `node --check`.

---

## File Structure

- Modify `materials/system_practice_review.py`
  - Add attempt constants, answer normalization, draft creation, answer saving, submit-and-check, immutable record guard, list/get helpers.
- Modify `materials/system_practice_review_api.py`
  - Add REST endpoints for creating attempts, updating draft answers, submitting attempts, and listing attempt history.
- Modify `web/app.js`
  - Add “开始练习” entry from practice-set detail.
  - Render practice attempt overlay with paper view, right answer card, submit confirmation, result view, and disabled/placeholder “再次练习”.
- Modify `web/styles.css`
  - Add focused styles for practice attempt paper, answer card, submit confirm, and result table.
- Modify `tests/test_system_practice_review.py`
  - Add backend and API tests for attempt creation, answer save, submit immutability, choice checking, blank conservative checking, solution pending grading.
- Modify `tests/test_system_library_frontend.py`
  - Add static frontend tests for expected UI hooks and no OCR/retry implementation.

## Data Model

Practice attempts live in:

```text
{users_dir}/{user_id}/system_library/practice_attempts.jsonl
```

Attempt shape:

```json
{
  "attempt_id": "pa_abc123",
  "user_id": "tester",
  "practice_set_id": "ps_abc123",
  "status": "draft",
  "started_at": "2026-07-04T12:00:00+00:00",
  "submitted_at": null,
  "duration_seconds": null,
  "answers": {
    "kaoyan_math1_2099_q001": {
      "answer_type": "choice",
      "value": "B",
      "updated_at": "2026-07-04T12:01:00+00:00"
    }
  },
  "results": {},
  "summary": {
    "total": 0,
    "correct": 0,
    "incorrect": 0,
    "unanswered": 0,
    "needs_review": 0,
    "needs_grading": 0
  }
}
```

## Task 1: Backend Attempt Store

**Files:**
- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing tests for draft creation and answer saving**

Append these tests to `SystemPracticeReviewTest` before `_store`:

```python
    def test_practice_attempt_create_and_save_answers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=2,
                same_type_only=False,
                exclude_mastered=False,
            )

            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            updated = store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q003": {"answer_type": "blank", "value": " 1 / 2 "},
                },
            )

            self.assertEqual(updated["status"], "draft")
            self.assertEqual(updated["practice_set_id"], practice_set["set_id"])
            self.assertEqual(updated["answers"]["kaoyan_math1_2099_q002"]["value"], "B")
            self.assertEqual(updated["answers"]["kaoyan_math1_2099_q003"]["value"], "1 / 2")
```

- [ ] **Step 2: Run the failing test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_create_and_save_answers
```

Expected: FAIL with `AttributeError: 'SystemPracticeReviewStore' object has no attribute 'create_practice_attempt'`.

- [ ] **Step 3: Add attempt constants and draft methods**

In `materials/system_practice_review.py`, add constants near the existing filenames:

```python
PRACTICE_ATTEMPT_FILENAME = "practice_attempts.jsonl"
PRACTICE_ATTEMPT_STATUSES = {"draft", "submitted", "abandoned"}
PRACTICE_ANSWER_TYPES = {"choice", "blank", "solution"}
```

Add these public methods to `SystemPracticeReviewStore` after `delete_practice_set`:

```python
    def create_practice_attempt(self, user_id: str, practice_set_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        practice_set = self.get_practice_set(safe_user_id, practice_set_id)
        now = self._utc_now()
        attempt = {
            "attempt_id": self._new_id("pa"),
            "user_id": safe_user_id,
            "practice_set_id": practice_set["set_id"],
            "status": "draft",
            "started_at": now,
            "submitted_at": None,
            "duration_seconds": None,
            "answers": {},
            "results": {},
            "summary": self._empty_attempt_summary(len(practice_set.get("question_ids") or [])),
            "source_meta": {
                "title": practice_set.get("title") or "",
                "subject": practice_set.get("subject") or "",
                "exam_type": practice_set.get("exam_type") or "",
                "library_name": practice_set.get("library_name") or "",
                "question_ids": list(practice_set.get("question_ids") or []),
                "matching_topics": list(practice_set.get("matching_topics") or []),
            },
        }
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        records.append(attempt)
        self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
        return dict(attempt)

    def update_practice_attempt_answers(
        self,
        user_id: str,
        attempt_id: str,
        answers: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(answers, dict):
            raise ValueError("answers must be a JSON object")
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        for index, record in enumerate(records):
            if record.get("attempt_id") != safe_attempt_id:
                continue
            if record.get("status") != "draft":
                raise ValueError("submitted practice attempts cannot be modified")
            practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
            allowed_ids = {str(question_id) for question_id in practice_set.get("question_ids") or []}
            next_answers = dict(record.get("answers") or {})
            for question_id, raw_answer in answers.items():
                safe_question_id = validate_safe_id(str(question_id), "question_id")
                if safe_question_id not in allowed_ids:
                    raise ValueError("answer question_id is not in this practice set")
                next_answers[safe_question_id] = self._normalize_attempt_answer(raw_answer)
            updated = {**record, "answers": next_answers}
            records[index] = updated
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")
```

Add helper methods near other private helpers:

```python
    def _normalize_attempt_answer(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("answer must be a JSON object")
        answer_type = str(value.get("answer_type") or "").strip()
        if answer_type not in PRACTICE_ANSWER_TYPES:
            raise ValueError("invalid answer_type")
        answer_value = self._clean_string(value.get("value"))
        return {
            "answer_type": answer_type,
            "value": answer_value,
            "updated_at": self._utc_now(),
        }

    def _empty_attempt_summary(self, total: int = 0) -> dict[str, int]:
        return {
            "total": int(total),
            "correct": 0,
            "incorrect": 0,
            "unanswered": int(total),
            "needs_review": 0,
            "needs_grading": 0,
        }
```

- [ ] **Step 4: Run the test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_create_and_save_answers
```

Expected: PASS.

## Task 2: Submit and Conservative Checking

**Files:**
- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing tests for submit, checking, and immutability**

Append:

```python
    def test_practice_attempt_submit_checks_supported_question_types_and_locks_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=3,
                same_type_only=False,
                exclude_mastered=False,
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"},
                    "kaoyan_math1_2099_q003": {"answer_type": "blank", "value": "1/2"},
                    "kaoyan_math1_2099_q004": {"answer_type": "solution", "value": "先分类讨论。"},
                },
            )

            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])

            self.assertEqual(submitted["status"], "submitted")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q002"]["status"], "correct")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q003"]["status"], "needs_review")
            self.assertEqual(submitted["results"]["kaoyan_math1_2099_q004"]["status"], "needs_grading")
            self.assertEqual(submitted["summary"]["total"], 3)
            self.assertEqual(submitted["summary"]["correct"], 1)
            self.assertEqual(submitted["summary"]["needs_review"], 1)
            self.assertEqual(submitted["summary"]["needs_grading"], 1)
            with self.assertRaises(ValueError):
                store.update_practice_attempt_answers(
                    "tester",
                    attempt["attempt_id"],
                    {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "C"}},
                )
```

- [ ] **Step 2: Run failing test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_checks_supported_question_types_and_locks_record
```

Expected: FAIL with missing `submit_practice_attempt`.

- [ ] **Step 3: Implement submit and checking helpers**

Add public methods after `update_practice_attempt_answers`:

```python
    def submit_practice_attempt(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        for index, record in enumerate(records):
            if record.get("attempt_id") != safe_attempt_id:
                continue
            if record.get("status") != "draft":
                raise ValueError("only draft practice attempts can be submitted")
            practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
            question_ids = [str(question_id) for question_id in practice_set.get("question_ids") or []]
            answers = record.get("answers") if isinstance(record.get("answers"), dict) else {}
            results = {
                question_id: self._check_attempt_question(question_id, answers.get(question_id))
                for question_id in question_ids
            }
            submitted_at = self._utc_now()
            updated = {
                **record,
                "status": "submitted",
                "submitted_at": submitted_at,
                "duration_seconds": self._attempt_duration_seconds(record.get("started_at"), submitted_at),
                "results": results,
                "summary": self._attempt_summary(results),
            }
            records[index] = updated
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def get_practice_attempt(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        for record in self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id"):
            if record.get("attempt_id") == safe_attempt_id:
                return dict(record)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def list_practice_attempts(self, user_id: str, practice_set_id: str | None = None) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        if practice_set_id is not None:
            safe_set_id = validate_safe_id(practice_set_id, "practice_set_id")
            records = [record for record in records if record.get("practice_set_id") == safe_set_id]
        return sorted(records, key=lambda record: str(record.get("started_at") or ""), reverse=True)
```

Add helpers:

```python
    def _check_attempt_question(self, question_id: str, answer: Any) -> dict[str, Any]:
        question = self.library.get_question(question_id)
        standard_answer = self._clean_string(question.get("answer") or question.get("answer_markdown"))
        if not isinstance(answer, dict) or not self._clean_string(answer.get("value")):
            return {
                "status": "unanswered",
                "standard_answer": standard_answer,
                "auto_checked": True,
                "ai_score": None,
                "ai_feedback": "",
            }
        answer_type = str(answer.get("answer_type") or "")
        value = self._clean_string(answer.get("value"))
        if answer_type == "choice":
            status = "correct" if self._normalize_choice_answer(value) == self._normalize_choice_answer(standard_answer) else "incorrect"
            auto_checked = True
        elif answer_type == "blank":
            status = "correct" if self._normalize_blank_answer(value) and self._normalize_blank_answer(value) == self._normalize_blank_answer(standard_answer) else "needs_review"
            auto_checked = status == "correct"
        else:
            status = "needs_grading"
            auto_checked = False
        return {
            "status": status,
            "standard_answer": standard_answer,
            "auto_checked": auto_checked,
            "ai_score": None,
            "ai_feedback": "",
        }

    def _attempt_summary(self, results: dict[str, dict[str, Any]]) -> dict[str, int]:
        summary = self._empty_attempt_summary(len(results))
        summary["unanswered"] = 0
        for result in results.values():
            status = str(result.get("status") or "")
            if status in summary:
                summary[status] += 1
        return summary

    def _normalize_choice_answer(self, value: Any) -> str:
        text = self._clean_string(value).upper()
        return text[:1] if text[:1] in {"A", "B", "C", "D"} else text

    def _normalize_blank_answer(self, value: Any) -> str:
        text = self._clean_string(value)
        return "".join(text.replace("，", ",").split()).lower()

    def _attempt_duration_seconds(self, started_at: Any, submitted_at: str) -> int | None:
        try:
            start = datetime.fromisoformat(str(started_at))
            end = datetime.fromisoformat(submitted_at)
        except ValueError:
            return None
        return max(0, int((end - start).total_seconds()))
```

- [ ] **Step 4: Run backend attempt tests**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_create_and_save_answers
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_checks_supported_question_types_and_locks_record
```

Expected: PASS.

## Task 3: Practice Attempt API

**Files:**
- Modify: `materials/system_practice_review_api.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing API test**

Append:

```python
    def test_practice_attempt_api_create_update_submit_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(system_practice_review_router)
            with patch(
                "materials.system_practice_review_api._store",
                return_value=self._store(raw_root, users_root),
            ):
                client = TestClient(app)
                practice_response = client.post(
                    "/api/materials/system/practice-sets",
                    params={"user_id": "tester"},
                    json={
                        "source_question_id": "kaoyan_math1_2099_q001",
                        "count": 2,
                        "same_type_only": False,
                        "exclude_mastered": False,
                    },
                )
                practice_set_id = practice_response.json()["practice_set"]["set_id"]
                create_response = client.post(
                    f"/api/materials/system/practice-sets/{practice_set_id}/attempts",
                    params={"user_id": "tester"},
                    json={},
                )
                attempt_id = create_response.json()["practice_attempt"]["attempt_id"]
                update_response = client.patch(
                    f"/api/materials/system/practice-attempts/{attempt_id}/answers",
                    params={"user_id": "tester"},
                    json={
                        "answers": {
                            "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "B"}
                        }
                    },
                )
                submit_response = client.post(
                    f"/api/materials/system/practice-attempts/{attempt_id}/submit",
                    params={"user_id": "tester"},
                    json={},
                )
                list_response = client.get(
                    "/api/materials/system/practice-attempts",
                    params={"user_id": "tester", "practice_set_id": practice_set_id},
                )

            self.assertEqual(create_response.status_code, 200)
            self.assertEqual(update_response.status_code, 200)
            self.assertEqual(submit_response.status_code, 200)
            self.assertEqual(submit_response.json()["practice_attempt"]["status"], "submitted")
            self.assertEqual(list_response.json()["total"], 1)
            self.assertEqual(list_response.json()["items"][0]["attempt_id"], attempt_id)
```

- [ ] **Step 2: Run failing test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_api_create_update_submit_and_list
```

Expected: FAIL with 404 for missing route.

- [ ] **Step 3: Add API routes**

In `materials/system_practice_review_api.py`, add routes before `/review-tasks`:

```python
@router.post("/practice-sets/{practice_set_id}/attempts")
async def create_practice_attempt(
    practice_set_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        attempt = _store().create_practice_attempt(uid, practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": attempt}


@router.get("/practice-attempts")
async def list_practice_attempts(
    request: Request,
    user_id: str | None = Query(None),
    practice_set_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        items = _store().list_practice_attempts(uid, practice_set_id=practice_set_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "total": len(items), "items": items}


@router.get("/practice-attempts/{attempt_id}")
async def get_practice_attempt(
    attempt_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        attempt = _store().get_practice_attempt(uid, attempt_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": attempt}


@router.patch("/practice-attempts/{attempt_id}/answers")
async def update_practice_attempt_answers(
    attempt_id: str,
    request: Request,
    payload: dict[str, Any],
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        attempt = _store().update_practice_attempt_answers(uid, attempt_id, payload.get("answers") or {})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": attempt}


@router.post("/practice-attempts/{attempt_id}/submit")
async def submit_practice_attempt(
    attempt_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        attempt = _store().submit_practice_attempt(uid, attempt_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "practice_attempt": attempt}
```

- [ ] **Step 4: Run API test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_api_create_update_submit_and_list
```

Expected: PASS.

## Task 4: Frontend Practice Attempt Flow

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Add failing static frontend test**

Append to `SystemLibraryFrontendTests`:

```python
    def test_practice_set_attempt_flow_has_answer_card_submit_and_placeholder_retry(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function openPracticeAttempt", source)
        self.assertIn("function renderPracticeAttemptDraft", source)
        self.assertIn("function renderPracticeAttemptResult", source)
        self.assertIn("data-practice-start-attempt", source)
        self.assertIn("data-practice-submit-attempt", source)
        self.assertIn("data-practice-answer-choice", source)
        self.assertIn("data-practice-answer-blank", source)
        self.assertIn("data-practice-answer-solution", source)
        self.assertIn("再次练习将在后续版本开放", source)
        self.assertNotIn("ocr", source[source.find("function openPracticeAttempt"):source.find("function renderSystemMaterialsSkeleton")])
        self.assertIn(".practice-attempt-layout", styles)
        self.assertIn(".practice-answer-card", styles)
        self.assertIn(".practice-result-table", styles)
```

- [ ] **Step 2: Run failing frontend test**

Run:

```bash
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_practice_set_attempt_flow_has_answer_card_submit_and_placeholder_retry
```

Expected: FAIL with missing `openPracticeAttempt`.

- [ ] **Step 3: Add Start Practice button to practice-set detail**

In `renderSystemPracticeSetDetail`, add this button in `.system-workflow-result-actions` before “加入复习规划”:

```javascript
<button type="button" class="small-button dark-button" data-practice-start-attempt>开始练习</button>
```

Add this listener after the existing add-review listener:

```javascript
  body.querySelector("[data-practice-start-attempt]")?.addEventListener("click", () => {
    void openPracticeAttempt(practiceSet, questions, { fallbackQuestions });
  });
```

- [ ] **Step 4: Add attempt helper functions**

Add these functions after `openSystemPracticeSetDetail`:

```javascript
function practiceAttemptId(attempt = {}) {
  return attempt.attempt_id || attempt.id || "";
}

function practiceAttemptQuestionAnswer(attempt = {}, questionId = "") {
  const answers = attempt.answers && typeof attempt.answers === "object" ? attempt.answers : {};
  return answers[questionId] || {};
}

function practiceAttemptAnswerType(question = {}) {
  const type = String(question.question_type || question.question_type_label || "").toLowerCase();
  if (type.includes("choice") || type.includes("选择")) return "choice";
  if (type.includes("blank") || type.includes("填空")) return "blank";
  return "solution";
}

function renderPracticeAnswerInput(question, attempt) {
  const questionId = question.question_id || "";
  const answer = practiceAttemptQuestionAnswer(attempt, questionId);
  const type = answer.answer_type || practiceAttemptAnswerType(question);
  const value = answer.value || "";
  if (type === "choice") {
    return `
      <div class="practice-answer-input">
        <strong>你的答案</strong>
        <div class="practice-choice-row">
          ${["A", "B", "C", "D"].map((choice) => `
            <button type="button" class="practice-choice ${value === choice ? "active" : ""}" data-practice-answer-choice="${escapeHtml(questionId)}" data-choice="${choice}">${choice}</button>
          `).join("")}
        </div>
      </div>
    `;
  }
  if (type === "blank") {
    return `
      <label class="practice-answer-input">
        <strong>你的答案</strong>
        <input type="text" value="${escapeHtml(value)}" data-practice-answer-blank="${escapeHtml(questionId)}" placeholder="输入填空答案">
      </label>
    `;
  }
  return `
    <label class="practice-answer-input">
      <strong>你的步骤</strong>
      <textarea data-practice-answer-solution="${escapeHtml(questionId)}" placeholder="第一版暂不做 OCR，请输入关键步骤">${escapeHtml(value)}</textarea>
    </label>
  `;
}
```

- [ ] **Step 5: Add draft renderer and answer save**

Add:

```javascript
function renderPracticeAttemptDraft(overlay, practiceSet, questions, attempt, options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const questionIds = practiceSetQuestionIds(practiceSet, options.fallbackQuestions || []);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const answeredCount = questionIds.filter((questionId) => practiceAttemptQuestionAnswer(attempt, questionId).value).length;
  body.innerHTML = `
    <section class="practice-attempt-layout">
      <main class="practice-attempt-paper">
        <div class="practice-attempt-head">
          <div>
            <h4>${escapeHtml(practiceSet.title || "练习单")}</h4>
            <p>${questionIds.length} 题 · 草稿自动保存 · 提交后不可修改</p>
          </div>
          <button type="button" class="small-button" data-practice-attempt-back>返回练习单</button>
        </div>
        ${questionIds.map((questionId, index) => {
          const question = questionMap.get(questionId) || { question_id: questionId };
          return `
            <article class="practice-attempt-question" id="practice-question-${index + 1}">
              <div class="practice-paper-question-head">
                <div>
                  <strong>第 ${index + 1} 题 · ${escapeHtml(systemQuestionTitle(question) || questionId)}</strong>
                  <p>${escapeHtml([question.question_type_label || question.question_type, question.library_name].filter(Boolean).join(" · "))}</p>
                </div>
              </div>
              <div class="practice-paper-question-body">${question.question_id ? renderSystemQuestionMarkdown(question) : `<p>${escapeHtml(questionId)}</p>`}</div>
              ${renderPracticeAnswerInput(question, attempt)}
            </article>
          `;
        }).join("")}
      </main>
      <aside class="practice-answer-card">
        <strong>答题卡</strong>
        <div class="practice-answer-grid">
          ${questionIds.map((questionId, index) => `<a href="#practice-question-${index + 1}" class="${practiceAttemptQuestionAnswer(attempt, questionId).value ? "answered" : ""}">${index + 1}</a>`).join("")}
        </div>
        <p>已答 ${answeredCount} / ${questionIds.length}</p>
        <button type="button" class="small-button dark-button" data-practice-submit-attempt="${escapeHtml(practiceAttemptId(attempt))}">提交练习</button>
        <button type="button" class="small-button" data-practice-attempt-back>暂存退出</button>
      </aside>
    </section>
  `;
  bindPracticeAttemptDraftEvents(overlay, practiceSet, questions, attempt, options);
}

function bindPracticeAttemptDraftEvents(overlay, practiceSet, questions, attempt, options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  body.querySelectorAll("[data-practice-attempt-back]").forEach((button) => {
    button.addEventListener("click", () => renderSystemPracticeSetDetail(overlay, practiceSet, questions, options));
  });
  body.querySelectorAll("[data-practice-answer-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      void savePracticeAttemptAnswers(overlay, practiceSet, questions, attempt, {
        [button.dataset.practiceAnswerChoice]: { answer_type: "choice", value: button.dataset.choice },
      }, options);
    });
  });
  body.querySelectorAll("[data-practice-answer-blank]").forEach((input) => {
    input.addEventListener("change", () => {
      void savePracticeAttemptAnswers(overlay, practiceSet, questions, attempt, {
        [input.dataset.practiceAnswerBlank]: { answer_type: "blank", value: input.value },
      }, options);
    });
  });
  body.querySelectorAll("[data-practice-answer-solution]").forEach((textarea) => {
    textarea.addEventListener("change", () => {
      void savePracticeAttemptAnswers(overlay, practiceSet, questions, attempt, {
        [textarea.dataset.practiceAnswerSolution]: { answer_type: "solution", value: textarea.value },
      }, options);
    });
  });
  body.querySelector("[data-practice-submit-attempt]")?.addEventListener("click", () => {
    if (!window.confirm("提交后本次练习记录不可修改，确认提交吗？")) return;
    void submitPracticeAttempt(overlay, practiceSet, questions, attempt, options);
  });
}
```

Add fetch methods:

```javascript
async function savePracticeAttemptAnswers(overlay, practiceSet, questions, attempt, answers, options = {}) {
  const attemptId = practiceAttemptId(attempt);
  const data = await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/answers?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  });
  const nextAttempt = data.practice_attempt || data;
  renderPracticeAttemptDraft(overlay, practiceSet, questions, nextAttempt, options);
}

async function submitPracticeAttempt(overlay, practiceSet, questions, attempt, options = {}) {
  const attemptId = practiceAttemptId(attempt);
  const data = await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/submit?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  renderPracticeAttemptResult(overlay, practiceSet, questions, data.practice_attempt || data, options);
}
```

- [ ] **Step 6: Add result renderer and start function**

Add:

```javascript
function practiceResultStatusLabel(status) {
  if (status === "correct") return "正确";
  if (status === "incorrect") return "错误";
  if (status === "unanswered") return "未答";
  if (status === "needs_review") return "待核对";
  if (status === "needs_grading") return "待评分";
  return "未知";
}

function renderPracticeAttemptResult(overlay, practiceSet, questions, attempt, options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const questionIds = practiceSetQuestionIds(practiceSet, options.fallbackQuestions || []);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const results = attempt.results && typeof attempt.results === "object" ? attempt.results : {};
  const summary = attempt.summary || {};
  body.innerHTML = `
    <section class="practice-attempt-result">
      <div class="practice-attempt-head">
        <div>
          <h4>练习结果</h4>
          <p>本次记录已锁定 · ${escapeHtml(attempt.submitted_at || "")}</p>
        </div>
        <button type="button" class="small-button" data-practice-result-back>返回练习单</button>
      </div>
      <div class="practice-result-summary">
        <span>正确 ${Number(summary.correct || 0)}</span>
        <span>错误 ${Number(summary.incorrect || 0)}</span>
        <span>待核对 ${Number(summary.needs_review || 0)}</span>
        <span>待评分 ${Number(summary.needs_grading || 0)}</span>
      </div>
      <table class="practice-result-table">
        <thead><tr><th>题号</th><th>你的答案</th><th>标准答案</th><th>结果</th><th>动作</th></tr></thead>
        <tbody>
          ${questionIds.map((questionId, index) => {
            const answer = practiceAttemptQuestionAnswer(attempt, questionId);
            const result = results[questionId] || {};
            return `
              <tr>
                <td>第 ${index + 1} 题</td>
                <td>${escapeHtml(answer.value || "未答")}</td>
                <td>${escapeHtml(result.standard_answer || "")}</td>
                <td>${escapeHtml(practiceResultStatusLabel(result.status))}</td>
                <td>
                  <button type="button" class="small-button" data-practice-result-detail="${escapeHtml(questionId)}">查看详情</button>
                  <button type="button" class="small-button" data-practice-result-wrong="${escapeHtml(questionId)}">加入错题</button>
                  ${result.status === "needs_grading" ? `<button type="button" class="small-button" data-practice-ai-grade="${escapeHtml(questionId)}">问 AI 评分</button>` : ""}
                </td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
      <div class="system-workflow-actions">
        <button type="button" class="small-button" data-practice-retry-placeholder>再次练习</button>
        <button type="button" class="small-button dark-button" data-practice-add-review>把错题加入复习规划</button>
      </div>
    </section>
  `;
  body.querySelector("[data-practice-result-back]")?.addEventListener("click", () => renderSystemPracticeSetDetail(overlay, practiceSet, questions, options));
  body.querySelector("[data-practice-retry-placeholder]")?.addEventListener("click", () => window.alert("再次练习将在后续版本开放"));
  body.querySelectorAll("[data-practice-result-detail]").forEach((button) => {
    button.addEventListener("click", () => {
      closeSystemWorkflowModal();
      setActivePage("materials");
      setMaterialsMode(MATERIALS_MODE_SYSTEM, { skipRefreshWhenCurrent: true });
      void openSystemQuestionDrawer(button.dataset.practiceResultDetail);
    });
  });
  body.querySelectorAll("[data-practice-result-wrong]").forEach((button) => {
    button.addEventListener("click", () => toggleSystemWrongBook(button.dataset.practiceResultWrong));
  });
  body.querySelectorAll("[data-practice-ai-grade]").forEach((button) => {
    button.addEventListener("click", () => window.alert("AI 评分入口将在后续接入；第一版先显示标准答案与解析。"));
  });
}

async function openPracticeAttempt(practiceSet, questions = [], options = {}) {
  const practiceSetId = systemPracticeSetId(practiceSet);
  if (!practiceSetId) return;
  const overlay = document.querySelector(".system-workflow-overlay");
  const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}/attempts?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  renderPracticeAttemptDraft(overlay, practiceSet, questions, data.practice_attempt || data, options);
}
```

- [ ] **Step 7: Add styles**

Append to `web/styles.css`:

```css
.practice-attempt-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 16px;
  align-items: start;
}

.practice-attempt-paper,
.practice-answer-card,
.practice-attempt-result {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
}

.practice-attempt-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 12px;
  margin-bottom: 14px;
}

.practice-attempt-head h4 {
  margin: 0;
  color: #111827;
}

.practice-attempt-head p {
  margin: 4px 0 0;
  color: #64748b;
}

.practice-attempt-question {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 14px;
}

.practice-answer-input {
  display: grid;
  gap: 8px;
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #dbe3ef;
  border-radius: 10px;
  background: #f8fafc;
}

.practice-answer-input input,
.practice-answer-input textarea {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px;
  font: inherit;
}

.practice-answer-input textarea {
  min-height: 96px;
  resize: vertical;
}

.practice-choice-row {
  display: flex;
  gap: 8px;
}

.practice-choice {
  width: 38px;
  height: 34px;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  background: #fff;
  font-weight: 800;
}

.practice-choice.active {
  background: #17785f;
  border-color: #17785f;
  color: #fff;
}

.practice-answer-card {
  position: sticky;
  top: 12px;
}

.practice-answer-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin: 12px 0;
}

.practice-answer-grid a {
  display: grid;
  place-items: center;
  height: 34px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  color: #111827;
  text-decoration: none;
  font-weight: 800;
}

.practice-answer-grid a.answered {
  background: #dcfce7;
  border-color: #86efac;
  color: #166534;
}

.practice-result-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}

.practice-result-summary span {
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f8fafc;
  font-weight: 800;
}

.practice-result-table {
  width: 100%;
  border-collapse: collapse;
}

.practice-result-table th,
.practice-result-table td {
  border: 1px solid #e5e7eb;
  padding: 10px;
  text-align: left;
  vertical-align: top;
}

.practice-result-table th {
  background: #f8fafc;
}
```

- [ ] **Step 8: Run frontend static test**

Run:

```bash
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_practice_set_attempt_flow_has_answer_card_submit_and_placeholder_retry
```

Expected: PASS.

## Task 5: Full Verification and Manual Smoke

**Files:**
- No new implementation files.

- [ ] **Step 1: Run targeted test suite**

Run:

```bash
python -m unittest tests.test_system_practice_review
python -m unittest tests.test_system_library_frontend
node --check web/app.js
python -m compileall materials scripts tests
```

Expected:

- `tests.test_system_practice_review`: OK
- `tests.test_system_library_frontend`: OK
- `node --check web/app.js`: no output, exit 0
- compileall: exit 0

- [ ] **Step 2: Restart local server**

Run:

```powershell
$conns = Get-NetTCPConnection -LocalPort 49214 -State Listen -ErrorAction SilentlyContinue
foreach ($pidValue in ($conns | Select-Object -ExpandProperty OwningProcess -Unique)) {
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$pidValue"
  if ($proc.CommandLine -like '*scripts.web_server:app*') {
    Stop-Process -Id $pidValue -Force
  }
}
Start-Sleep -Milliseconds 800
Start-Process -WindowStyle Hidden -FilePath python -ArgumentList @('-m','uvicorn','scripts.web_server:app','--host','127.0.0.1','--port','49214') -WorkingDirectory 'E:\python_project'
Start-Sleep -Seconds 2
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:49214/
```

Expected: HTTP 200.

- [ ] **Step 3: Manual browser smoke**

Open:

```text
http://127.0.0.1:49214/
```

Manual path:

1. Go to `资料库`.
2. Switch to `系统资料`.
3. Open any question drawer.
4. Click `生成同类训练`.
5. Generate a practice set.
6. Click `打开练习单`.
7. Click `开始练习`.
8. Answer one choice question, one blank question, one solution question if present.
9. Click `提交练习`.
10. Confirm result page appears.
11. Click `再次练习`.

Expected:

- Answers update the right answer card.
- Submit confirmation warns that the record cannot be modified.
- Result page shows summary and per-question rows.
- `再次练习` shows the placeholder message only.

## Self-Review

Spec coverage:

- Practice set remains separate from user attempt records: Task 1.
- Submitted attempt immutable: Task 2.
- Choice/blank/solution type handling: Task 2 and Task 4.
- API endpoints: Task 3.
- Whole-paper view with right answer card: Task 4.
- Result page and placeholder retry: Task 4.
- No OCR in first version: Task 4 frontend assertion and spec boundary.
- Review planning data foundation through stored attempts: Task 1 and Task 2.

No placeholders:

- The plan intentionally uses “placeholder” only for the user-visible `再次练习` product behavior required by the spec.
- No `TODO` or `TBD` implementation placeholders should remain in code snippets.

Type consistency:

- Backend uses `practice_attempt`, `practice_attempts`, `attempt_id`, `practice_set_id`.
- API response key is `practice_attempt`.
- Frontend helper names use `PracticeAttempt`.
