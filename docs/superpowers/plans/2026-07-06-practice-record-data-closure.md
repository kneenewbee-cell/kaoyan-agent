# Practice Record Data Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing practice attempt prototype into a reliable data layer that records per-question attempts, updates question/topic statistics, and keeps AI grading corrections consistent.

**Architecture:** Keep the existing `SystemPracticeReviewStore` and JSONL user-layer storage. Add per-item and stats records beside `practice_attempts.jsonl`, then make submit and AI grading update those records idempotently while preserving legacy attempt compatibility. Frontend changes are limited to reading the richer attempt payload and showing real save/submit/grade states; no system question raw data or `qa/` code is changed.

**Tech Stack:** Python stdlib JSONL storage, FastAPI router, existing `materials.system_practice_review` store, `unittest`, existing browser/frontend files under `web/`.

---

## Current State

Already implemented:

- `practice_attempts.jsonl` exists and stores draft/submitted attempts.
- `create_practice_attempt`, `update_practice_attempt_answers`, `submit_practice_attempt`, `list_practice_attempts`, `apply_practice_item_grade`, and `request_practice_item_ai_grade` exist.
- Choice and blank local grading exist.
- Solution questions default to `pending_review`.
- AI grading endpoint and frontend `AI 判分` button exist.

Still missing:

- `practice_attempt_items.jsonl` as a first-class per-question record file.
- `user_question_stats.jsonl` and `user_topic_stats.jsonl`.
- Idempotent submit behavior using an attempt-level submit token or existing submitted state.
- Explicit submit failure recovery contract.
- AI grading updates to per-item records and stats, not only nested `attempt.results`.
- API response contract that exposes `attempt`, `items`, `summary`, and stats deltas.

## File Structure

Modify:

- `materials/system_practice_review.py`
  - Owns JSONL filenames, attempt creation/update/submit, item record creation, stats updates, AI grading reconciliation, and legacy backfill.
- `materials/system_practice_review_api.py`
  - Exposes richer attempt submit/get/grade responses.
- `tests/test_system_practice_review.py`
  - Adds data-layer tests for item records, stats, idempotent submit, AI correction, and API payloads.
- `web/app.js`
  - Uses richer attempt payload if present; keeps legacy `practice_attempt.results` fallback.
- `web/index.html`
  - Only update static asset version when `web/app.js` changes.

Do not modify:

- `qa/`
- `data/raw/`
- public system question markdown
- materials ingestion pipeline

Create no new production Python module in the first pass. Keep this vertical slice inside `SystemPracticeReviewStore` because the existing store already owns practice sets, attempts, review tasks, and the user JSONL folder. If the file becomes too large after this slice, split repository helpers in a later refactor.

## Data Files

User-layer files under `data/users/{user_id}/system_library/`:

```text
practice_attempts.jsonl
practice_attempt_items.jsonl
user_question_stats.jsonl
user_topic_stats.jsonl
```

`practice_attempt_items.jsonl` record shape:

```json
{
  "attempt_item_id": "pai_...",
  "attempt_id": "pa_...",
  "practice_set_id": "ps_...",
  "user_id": "tester",
  "question_id": "kaoyan_math1_2024_q011",
  "question_title": "2024 数一 Q11",
  "question_type": "fill_blank",
  "answer_type": "blank",
  "topics": ["极限", "导数"],
  "source_meta": {
    "subject": "math",
    "exam_type": "math1",
    "library_name": "数一历年真题",
    "year": 2024,
    "question_number": 11
  },
  "user_answer": "1",
  "standard_answer": "a = 6",
  "local_status": "incorrect",
  "ai_status": "not_used",
  "final_status": "incorrect",
  "judge_method": "local",
  "judge_confidence": 1.0,
  "judge_reason": "填空题先按参考答案本地判分；如表达等价可再请求 AI 判分。",
  "ai_feedback": "",
  "manual_override": false,
  "submitted_at": "2026-07-06T00:00:00+00:00",
  "graded_at": null,
  "grading_version": "local_v1"
}
```

`user_question_stats.jsonl` record shape:

```json
{
  "stat_id": "kaoyan_math1_2024_q011",
  "user_id": "tester",
  "question_id": "kaoyan_math1_2024_q011",
  "attempt_count": 2,
  "correct_count": 1,
  "incorrect_count": 1,
  "partial_count": 0,
  "pending_review_count": 0,
  "unanswered_count": 0,
  "latest_attempt_id": "pa_...",
  "latest_status": "correct",
  "latest_answer": "a=6",
  "latest_practiced_at": "2026-07-06T00:00:00+00:00",
  "wrong_streak": 0,
  "last_wrong_at": "2026-07-05T00:00:00+00:00",
  "topics": ["极限", "导数"]
}
```

`user_topic_stats.jsonl` record shape:

```json
{
  "stat_id": "math::极限",
  "user_id": "tester",
  "subject": "math",
  "topic": "极限",
  "attempt_count": 8,
  "correct_count": 5,
  "incorrect_count": 2,
  "partial_count": 0,
  "pending_review_count": 1,
  "unanswered_count": 0,
  "latest_attempt_id": "pa_...",
  "latest_practiced_at": "2026-07-06T00:00:00+00:00",
  "representative_wrong_question_ids": ["kaoyan_math1_2024_q011"]
}
```

## Task 1: Add Failing Data-Layer Tests

**Files:**

- Modify: `tests/test_system_practice_review.py`

- [ ] **Step 1: Add imports if missing**

Ensure `json` and `Path` are already available at the top of `tests/test_system_practice_review.py`. They currently are imported, so do not duplicate them.

- [ ] **Step 2: Add a test that submit writes attempt items and stats**

Add this method inside `SystemPracticeReviewTest` after `test_practice_attempt_create_save_submit_and_lock_answers`:

```python
    def test_practice_attempt_submit_writes_item_and_stats_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {
                    "kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"},
                    "kaoyan_math1_2099_q006": {"answer_type": "blank", "value": "43"},
                },
            )

            submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])
            items = store.list_practice_attempt_items("tester", attempt_id=attempt["attempt_id"])
            question_stats = store.list_user_question_stats("tester")
            topic_stats = store.list_user_topic_stats("tester")

            self.assertEqual(submitted["status"], "submitted")
            self.assertEqual(len(items), 5)
            item_by_question = {item["question_id"]: item for item in items}
            self.assertEqual(item_by_question["kaoyan_math1_2099_q002"]["final_status"], "correct")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["final_status"], "incorrect")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["standard_answer"], "42")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["judge_method"], "local")
            self.assertTrue((users_root / "tester" / "system_library" / "practice_attempt_items.jsonl").exists())
            self.assertTrue((users_root / "tester" / "system_library" / "user_question_stats.jsonl").exists())
            self.assertTrue((users_root / "tester" / "system_library" / "user_topic_stats.jsonl").exists())
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["attempt_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["correct_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["incorrect_count"], 1)
            self.assertTrue(any(stat["topic"] == "极限" for stat in topic_stats.values()))
```

- [ ] **Step 3: Run the new test and verify it fails**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_writes_item_and_stats_records
```

Expected: FAIL with `AttributeError: 'SystemPracticeReviewStore' object has no attribute 'list_practice_attempt_items'`.

## Task 2: Add Item and Stats Storage Helpers

**Files:**

- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Add constants near existing attempt constants**

In `materials/system_practice_review.py`, near `PRACTICE_ATTEMPT_FILENAME`, add:

```python
PRACTICE_ATTEMPT_ITEM_FILENAME = "practice_attempt_items.jsonl"
USER_QUESTION_STATS_FILENAME = "user_question_stats.jsonl"
USER_TOPIC_STATS_FILENAME = "user_topic_stats.jsonl"
```

- [ ] **Step 2: Add public list helpers after `get_practice_attempt`**

Add:

```python
    def list_practice_attempt_items(
        self,
        user_id: str,
        *,
        attempt_id: str | None = None,
        question_id: str | None = None,
    ) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id") if attempt_id else None
        safe_question_id = validate_safe_id(question_id, "question_id") if question_id else None
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        if safe_attempt_id:
            records = [record for record in records if record.get("attempt_id") == safe_attempt_id]
        if safe_question_id:
            records = [record for record in records if record.get("question_id") == safe_question_id]
        return sorted(records, key=lambda record: str(record.get("submitted_at") or ""))

    def list_user_question_stats(self, user_id: str) -> dict[str, dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, USER_QUESTION_STATS_FILENAME, "stat_id")
        return {str(record.get("question_id") or record.get("stat_id")): dict(record) for record in records}

    def list_user_topic_stats(self, user_id: str) -> dict[str, dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, USER_TOPIC_STATS_FILENAME, "stat_id")
        return {str(record.get("stat_id")): dict(record) for record in records}
```

- [ ] **Step 3: Add status counting helper near `_summarize_practice_results`**

Add:

```python
    def _status_count_key(self, status: Any) -> str:
        normalized = str(status or "pending_review")
        if normalized in {"needs_review", "needs_grading", "pending"}:
            normalized = "pending_review"
        if normalized not in {"correct", "incorrect", "partial", "pending_review", "unanswered"}:
            normalized = "pending_review"
        return f"{normalized}_count"
```

- [ ] **Step 4: Run the new test and verify the failure moves forward**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_writes_item_and_stats_records
```

Expected: FAIL because `practice_attempt_items.jsonl` is not written yet, not because list methods are missing.

## Task 3: Write Attempt Items on Submit

**Files:**

- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Add `_attempt_item_from_result` helper after `_grade_practice_attempt`**

Add:

```python
    def _attempt_item_from_result(
        self,
        *,
        safe_user_id: str,
        attempt: dict[str, Any],
        practice_set: dict[str, Any],
        question_id: str,
        result: dict[str, Any],
        submitted_at: str,
    ) -> dict[str, Any]:
        question = self.library.get_question(question_id)
        source_meta = {
            "subject": str(question.get("module") or question.get("subject") or "math"),
            "exam_type": str(question.get("exam_type") or ""),
            "library_name": str(question.get("library_name") or ""),
            "year": question.get("year"),
            "question_number": question.get("question_number"),
        }
        return {
            "attempt_item_id": f"{attempt.get('attempt_id')}::{question_id}",
            "attempt_id": str(attempt.get("attempt_id") or ""),
            "practice_set_id": str(practice_set.get("set_id") or attempt.get("practice_set_id") or ""),
            "user_id": safe_user_id,
            "question_id": question_id,
            "question_title": self._question_title(question),
            "question_type": str(question.get("question_type") or ""),
            "answer_type": str(result.get("answer_type") or self._question_answer_type(question)),
            "topics": list(question.get("topics") or []),
            "source_meta": source_meta,
            "user_answer": self._clean_answer_value(result.get("user_answer")),
            "standard_answer": self._clean_answer_value(result.get("standard_answer")),
            "local_status": str(result.get("local_status") or result.get("status") or "pending_review"),
            "ai_status": str(result.get("ai_status") or "not_used"),
            "final_status": str(result.get("final_status") or result.get("status") or "pending_review"),
            "status": str(result.get("final_status") or result.get("status") or "pending_review"),
            "judge_method": str(result.get("judge_method") or "local"),
            "judge_confidence": self._normalize_confidence(result.get("judge_confidence")),
            "judge_reason": self._clean_string(result.get("judge_reason")),
            "ai_feedback": self._clean_string(result.get("ai_feedback")),
            "manual_override": bool(result.get("manual_override", False)),
            "submitted_at": submitted_at,
            "graded_at": result.get("graded_at"),
            "grading_version": str(result.get("grading_version") or "local_v1"),
        }
```

- [ ] **Step 2: Add `_write_attempt_items_for_attempt` helper**

Add:

```python
    def _write_attempt_items_for_attempt(
        self,
        safe_user_id: str,
        attempt: dict[str, Any],
        practice_set: dict[str, Any],
    ) -> list[dict[str, Any]]:
        results = attempt.get("results") if isinstance(attempt.get("results"), dict) else {}
        submitted_at = str(attempt.get("submitted_at") or self._utc_now())
        next_items: list[dict[str, Any]] = []
        for question_id, result in results.items():
            if not isinstance(result, dict):
                continue
            safe_question_id = validate_safe_id(str(question_id), "question_id")
            next_items.append(
                self._attempt_item_from_result(
                    safe_user_id=safe_user_id,
                    attempt=attempt,
                    practice_set=practice_set,
                    question_id=safe_question_id,
                    result=result,
                    submitted_at=submitted_at,
                )
            )
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        replacing_ids = {item["attempt_item_id"] for item in next_items}
        kept = [record for record in records if record.get("attempt_item_id") not in replacing_ids]
        kept.extend(next_items)
        self._write_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, kept)
        return next_items
```

- [ ] **Step 3: Call item writer inside `submit_practice_attempt`**

In `submit_practice_attempt`, after `records[index] = updated` and before `_write_records`, insert:

```python
            self._write_attempt_items_for_attempt(safe_user_id, updated, practice_set)
```

- [ ] **Step 4: Run test and verify it fails on stats**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_writes_item_and_stats_records
```

Expected: FAIL because stats files are not written yet.

## Task 4: Add Question and Topic Stats Updates

**Files:**

- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Add `_rebuild_user_learning_stats` helper**

Add after `_write_attempt_items_for_attempt`:

```python
    def rebuild_user_learning_stats(self, user_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        items = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        question_stats: dict[str, dict[str, Any]] = {}
        topic_stats: dict[str, dict[str, Any]] = {}
        for item in sorted(items, key=lambda row: str(row.get("submitted_at") or "")):
            question_id = str(item.get("question_id") or "")
            if not question_id:
                continue
            status = str(item.get("final_status") or item.get("status") or "pending_review")
            count_key = self._status_count_key(status)
            question_stat = question_stats.setdefault(
                question_id,
                {
                    "stat_id": question_id,
                    "user_id": safe_user_id,
                    "question_id": question_id,
                    "attempt_count": 0,
                    "correct_count": 0,
                    "incorrect_count": 0,
                    "partial_count": 0,
                    "pending_review_count": 0,
                    "unanswered_count": 0,
                    "latest_attempt_id": "",
                    "latest_status": "",
                    "latest_answer": "",
                    "latest_practiced_at": "",
                    "wrong_streak": 0,
                    "last_wrong_at": "",
                    "topics": list(item.get("topics") or []),
                },
            )
            question_stat["attempt_count"] += 1
            question_stat[count_key] += 1
            question_stat["latest_attempt_id"] = str(item.get("attempt_id") or "")
            question_stat["latest_status"] = status
            question_stat["latest_answer"] = self._clean_answer_value(item.get("user_answer"))
            question_stat["latest_practiced_at"] = str(item.get("submitted_at") or "")
            question_stat["topics"] = list(item.get("topics") or [])
            if status == "incorrect":
                question_stat["wrong_streak"] += 1
                question_stat["last_wrong_at"] = str(item.get("submitted_at") or "")
            elif status == "correct":
                question_stat["wrong_streak"] = 0

            source_meta = item.get("source_meta") if isinstance(item.get("source_meta"), dict) else {}
            subject = str(source_meta.get("subject") or "math")
            for topic in [str(topic).strip() for topic in item.get("topics") or [] if str(topic).strip()]:
                stat_id = f"{subject}::{topic}"
                topic_stat = topic_stats.setdefault(
                    stat_id,
                    {
                        "stat_id": stat_id,
                        "user_id": safe_user_id,
                        "subject": subject,
                        "topic": topic,
                        "attempt_count": 0,
                        "correct_count": 0,
                        "incorrect_count": 0,
                        "partial_count": 0,
                        "pending_review_count": 0,
                        "unanswered_count": 0,
                        "latest_attempt_id": "",
                        "latest_practiced_at": "",
                        "representative_wrong_question_ids": [],
                    },
                )
                topic_stat["attempt_count"] += 1
                topic_stat[count_key] += 1
                topic_stat["latest_attempt_id"] = str(item.get("attempt_id") or "")
                topic_stat["latest_practiced_at"] = str(item.get("submitted_at") or "")
                if status == "incorrect" and question_id not in topic_stat["representative_wrong_question_ids"]:
                    topic_stat["representative_wrong_question_ids"].append(question_id)
                    topic_stat["representative_wrong_question_ids"] = topic_stat["representative_wrong_question_ids"][-5:]

        self._write_records(safe_user_id, USER_QUESTION_STATS_FILENAME, list(question_stats.values()))
        self._write_records(safe_user_id, USER_TOPIC_STATS_FILENAME, list(topic_stats.values()))
        return {"question_stats": question_stats, "topic_stats": topic_stats}
```

- [ ] **Step 2: Call stats rebuild after item write in `submit_practice_attempt`**

In `submit_practice_attempt`, after `_write_attempt_items_for_attempt(...)`, add:

```python
            self.rebuild_user_learning_stats(safe_user_id)
```

- [ ] **Step 3: Run the data-layer test**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_writes_item_and_stats_records
```

Expected: PASS.

- [ ] **Step 4: Run existing practice review tests**

Run:

```powershell
python -m unittest tests.test_system_practice_review
```

Expected: PASS.

## Task 5: Make Submit Idempotent and Recoverable

**Files:**

- Modify: `tests/test_system_practice_review.py`
- Modify: `materials/system_practice_review.py`

- [ ] **Step 1: Add idempotent submit test**

Add this method after the item/stats test:

```python
    def test_practice_attempt_submit_is_idempotent_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            store = self._store(raw_root, users_root)
            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )

            first = store.submit_practice_attempt("tester", attempt["attempt_id"])
            second = store.submit_practice_attempt("tester", attempt["attempt_id"])
            items = store.list_practice_attempt_items("tester", attempt_id=attempt["attempt_id"])
            question_stats = store.list_user_question_stats("tester")

            self.assertEqual(first["attempt_id"], second["attempt_id"])
            self.assertEqual(first["submitted_at"], second["submitted_at"])
            self.assertEqual(len(items), 5)
            self.assertEqual(question_stats["kaoyan_math1_2099_q002"]["attempt_count"], 1)
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_is_idempotent_after_success
```

Expected: FAIL with `ValueError: practice attempt is not submittable`.

- [ ] **Step 3: Update `submit_practice_attempt` submitted branch**

Inside `submit_practice_attempt`, replace:

```python
            if record.get("status") != "draft":
                raise ValueError("practice attempt is not submittable")
```

with:

```python
            if record.get("status") == "submitted":
                submitted = self._backfill_practice_attempt_result(record)
                practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
                self._write_attempt_items_for_attempt(safe_user_id, submitted, practice_set)
                self.rebuild_user_learning_stats(safe_user_id)
                return dict(submitted)
            if record.get("status") != "draft":
                raise ValueError("practice attempt is not submittable")
```

- [ ] **Step 4: Add failed status allowance**

Add `"submit_failed"` to `PRACTICE_ATTEMPT_STATUSES`, but do not persist it in the happy path yet:

```python
PRACTICE_ATTEMPT_STATUSES = {"draft", "submitted", "submit_failed", "abandoned"}
```

If a future submit exception is caught at API level, the frontend can still treat the attempt as draft because answers remain saved.

- [ ] **Step 5: Run idempotent submit test**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_submit_is_idempotent_after_success
```

Expected: PASS.

## Task 6: Make AI Grade Update Items and Stats

**Files:**

- Modify: `tests/test_system_practice_review.py`
- Modify: `materials/system_practice_review.py`

- [ ] **Step 1: Extend existing AI correction test**

In `test_ai_grade_override_can_correct_blank_result_and_updates_summary`, after the existing summary assertions, add:

```python
            items = store.list_practice_attempt_items("tester", attempt_id=submitted["attempt_id"])
            item_by_question = {item["question_id"]: item for item in items}
            question_stats = store.list_user_question_stats("tester")
            topic_stats = store.list_user_topic_stats("tester")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["final_status"], "correct")
            self.assertEqual(item_by_question["kaoyan_math1_2099_q006"]["judge_method"], "ai")
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["correct_count"], 1)
            self.assertEqual(question_stats["kaoyan_math1_2099_q006"]["incorrect_count"], 0)
            self.assertTrue(any(stat["correct_count"] >= 1 for stat in topic_stats.values()))
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_grade_override_can_correct_blank_result_and_updates_summary
```

Expected: FAIL because attempt item file/stat files are not updated after AI correction.

- [ ] **Step 3: Update `apply_practice_item_grade` to rewrite item/stats**

In `apply_practice_item_grade`, after:

```python
            updated["summary"] = self._summarize_practice_results(updated_results, len(updated_results))
```

add:

```python
            practice_set = self.get_practice_set(safe_user_id, str(updated.get("practice_set_id") or ""))
            self._write_attempt_items_for_attempt(safe_user_id, updated, practice_set)
            self.rebuild_user_learning_stats(safe_user_id)
```

- [ ] **Step 4: Run AI correction test**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_grade_override_can_correct_blank_result_and_updates_summary
```

Expected: PASS.

- [ ] **Step 5: Run all practice review tests**

Run:

```powershell
python -m unittest tests.test_system_practice_review
```

Expected: PASS.

## Task 7: Add API Response Contract for Attempt Details

**Files:**

- Modify: `materials/system_practice_review_api.py`
- Modify: `tests/test_system_practice_review.py`

- [ ] **Step 1: Add GET attempt endpoint test**

In the API test method or as a new method, add:

```python
    def test_practice_attempt_api_returns_attempt_items_and_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_blank=True)
            users_root = base / "users"
            app = FastAPI()
            library = SystemQuestionLibrary(raw_root=raw_root)
            state_store = UserSystemQuestionStateStore(users_dir=users_root)
            store = SystemPracticeReviewStore(library=library, state_store=state_store, users_dir=users_root)
            app.include_router(system_practice_review_router)
            app.state.system_practice_review_store = store
            client = TestClient(app)

            practice_set = store.create_practice_set(
                "tester",
                source_question_id="kaoyan_math1_2099_q001",
                count=5,
                same_type_only=False,
                exclude_mastered=False,
                source_scope="same_year",
            )
            attempt = store.create_practice_attempt("tester", practice_set["set_id"])
            store.update_practice_attempt_answers(
                "tester",
                attempt["attempt_id"],
                {"kaoyan_math1_2099_q002": {"answer_type": "choice", "value": "A"}},
            )
            store.submit_practice_attempt("tester", attempt["attempt_id"])

            response = client.get(f"/api/materials/system/practice-attempts/{attempt['attempt_id']}?user_id=tester")

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["practice_attempt"]["attempt_id"], attempt["attempt_id"])
            self.assertEqual(len(payload["items"]), 5)
            self.assertIn("question_stats", payload)
            self.assertIn("topic_stats", payload)
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_api_returns_attempt_items_and_stats
```

Expected: FAIL with 404 because the GET endpoint does not exist.

- [ ] **Step 3: Add GET endpoint before list endpoint**

In `materials/system_practice_review_api.py`, add before `@router.get("/practice-attempts")`:

```python
@router.get("/practice-attempts/{attempt_id}")
async def get_practice_attempt(
    attempt_id: str,
    request: Request,
    user_id: str | None = Query(None),
) -> dict[str, Any]:
    uid = _resolve_request_user_id(request, user_id)
    try:
        store = _store()
        practice_attempt = store.get_practice_attempt(uid, attempt_id)
        items = store.list_practice_attempt_items(uid, attempt_id=attempt_id)
        return {
            "ok": True,
            "user_id": uid,
            "practice_attempt": practice_attempt,
            "items": items,
            "summary": practice_attempt.get("summary") or {},
            "question_stats": store.list_user_question_stats(uid),
            "topic_stats": store.list_user_topic_stats(uid),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
```

- [ ] **Step 4: Run endpoint test**

Run:

```powershell
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_attempt_api_returns_attempt_items_and_stats
```

Expected: PASS.

## Task 8: Frontend Compatibility Only

**Files:**

- Modify: `web/app.js`
- Modify: `web/index.html`
- Test: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Add a frontend source assertion**

In `tests/test_system_library_frontend.py`, add a small assertion to the existing practice attempt frontend test:

```python
        self.assertIn("/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}", source)
```

- [ ] **Step 2: Run frontend source test and verify it fails**

Run:

```powershell
python -m unittest tests.test_system_library_frontend
```

Expected: FAIL because the frontend does not fetch the new attempt detail endpoint yet.

- [ ] **Step 3: Add fetch helper in `web/app.js`**

Near existing practice attempt helpers, add:

```javascript
async function fetchPracticeAttemptDetail(attemptId) {
  return fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
}
```

- [ ] **Step 4: Use detail fetch after submit and AI grade**

After successful submit and after successful AI grading, fetch the detail endpoint and pass its `practice_attempt` into the existing renderer while preserving `items` for future use:

```javascript
const detail = await fetchPracticeAttemptDetail(submittedAttempt.attempt_id);
renderPracticeAttemptResult(overlay, practiceSet, questions, mergePracticeAttempt(submittedAttempt, detail.practice_attempt || submittedAttempt), options);
```

For AI grade:

```javascript
const detail = await fetchPracticeAttemptDetail(attemptId);
renderPracticeAttemptResult(overlay, practiceSet, questions, mergePracticeAttempt(gradedAttempt, detail.practice_attempt || gradedAttempt), {
  preserveScrollTop: currentScrollTop
});
```

- [ ] **Step 5: Update asset version in `web/index.html`**

Change both static versions to a new suffix:

```html
?v=20260706-practice-record-data
```

- [ ] **Step 6: Run frontend tests**

Run:

```powershell
python -m unittest tests.test_system_library_frontend
```

Expected: PASS.

## Task 9: Verification Sweep

**Files:**

- No new files unless tests reveal a necessary correction.

- [ ] **Step 1: Run focused backend tests**

Run:

```powershell
python -m unittest tests.test_system_practice_review
```

Expected: PASS.

- [ ] **Step 2: Run focused frontend source tests**

Run:

```powershell
python -m unittest tests.test_system_library_frontend
```

Expected: PASS.

- [ ] **Step 3: Run compile check for touched modules**

Run:

```powershell
python -m compileall materials web tests
```

Expected: PASS with no syntax errors.

- [ ] **Step 4: Manually inspect generated user files in a temp test run**

Use a temporary users directory in tests only. Do not write to `data/raw`. Confirm these files are created:

```text
practice_attempts.jsonl
practice_attempt_items.jsonl
user_question_stats.jsonl
user_topic_stats.jsonl
```

- [ ] **Step 5: Commit**

Stage only touched code and tests:

```powershell
git add materials/system_practice_review.py materials/system_practice_review_api.py tests/test_system_practice_review.py tests/test_system_library_frontend.py web/app.js web/index.html
git commit -m "feat: 完善练习记录数据闭环"
```

Do not stage unrelated `data/raw` changes, logs, temp screenshots, or other worktree edits.

## Self-Review

Spec coverage:

- Per-question records: Task 1-3.
- Question/topic stats: Task 4.
- Idempotent submit and recoverability: Task 5.
- AI grading consistency: Task 6.
- Result read contract: Task 7-8.
- Verification: Task 9.

Scope check:

- This plan intentionally does not build `learning_profile_snapshots`; it creates the stats foundation required for that later feature.
- This plan intentionally does not migrate to MySQL/SQLite; JSONL remains the storage implementation.
- This plan intentionally does not redesign the practice attempt UI; frontend changes are compatibility-only.

Risk controls:

- Legacy `practice_attempts.jsonl` remains readable.
- `practice_attempt.results` remains in API payloads during transition.
- New files live only in the user-layer `system_library` directory.
- No system question public content is changed.
