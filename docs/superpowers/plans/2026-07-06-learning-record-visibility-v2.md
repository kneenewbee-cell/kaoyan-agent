# Learning Record Visibility V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the practice database visible to the user as learning feedback: after submitting and grading a practice set, the result page, question drawer, and review plan should show what was recorded and why it matters.

**Architecture:** Keep the current local user-data repository under `data/users/{user_id}/system_library/` and add read-model methods that summarize existing attempt items, question stats, and topic stats. The frontend should consume these summaries instead of exposing raw database files. This plan does not migrate to MySQL and does not rebuild the whole system library UI.

**Tech Stack:** Python `unittest`, FastAPI router in `materials/system_practice_review_api.py`, file-backed store in `materials/system_practice_review.py`, vanilla frontend in `web/app.js`, CSS in `web/styles.css`.

---

## Scope

This plan implements a product-facing loop:

```text
练习提交
→ 后端保存 attempt / attempt_items / question_stats / topic_stats
→ 结果页显示“记录已沉淀 + 本次薄弱点 + 下一步建议”
→ 单题抽屉显示这道题的历史练习摘要
→ 复习规划任务显示推荐原因
```

Out of scope:

```text
MySQL migration
large AI learning planner
OCR or handwritten answer recognition
new knowledge-point page
raw database admin table
```

## File Structure

- Modify: `materials/system_practice_review.py`
  - Add read-model methods for practice insights, question learning snapshots, and review recommendation reasons.
  - Keep storage writes idempotent; these methods only summarize existing records.

- Modify: `materials/system_practice_review_api.py`
  - Return insights from the practice-attempt detail endpoint.
  - Add a question learning snapshot endpoint for the drawer.
  - Add learning reason fields to review task list responses if needed.

- Modify: `web/app.js`
  - Render result insight panel after submit/AI grading.
  - Fetch and render single-question practice history inside the right drawer.
  - Render review task reason chips on the review page.

- Modify: `web/styles.css`
  - Add non-transparent, compact styles for insight panels, history rows, and reason chips.

- Modify: `web/index.html`
  - Bump cache version after frontend changes.

- Modify: `tests/test_system_practice_review.py`
  - Add backend tests for insight summaries and question snapshots.

- Modify: `tests/test_system_library_frontend.py`
  - Add source-level frontend tests for visible learning record surfaces.

---

### Task 1: Backend Practice Insight Read Model

**Files:**
- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing backend test for practice insights**

Add this test near the existing practice attempt record tests:

```python
def test_practice_attempt_insights_explain_recorded_learning_data(self) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        users_root = Path(temp_dir) / "users"
        raw_root = Path(temp_dir) / "raw"
        write_test_questions(raw_root)
        store = SystemPracticeReviewStore(users_dir=users_root, raw_root=raw_root)

        practice_set = store.create_practice_set(
            "tester",
            "kaoyan_math1_2099_q001",
            {"limit": 5, "topic_ids": ["limits", "derivatives"]},
        )
        attempt = store.create_practice_attempt("tester", practice_set["set_id"])
        store.update_practice_attempt_answers(
            "tester",
            attempt["attempt_id"],
            {
                "kaoyan_math1_2099_q002": {"value": "B"},
                "kaoyan_math1_2099_q003": {"value": "6"},
                "kaoyan_math1_2099_q006": {"value": "43"},
            },
        )
        submitted = store.submit_practice_attempt("tester", attempt["attempt_id"])

        insights = store.build_practice_attempt_insights("tester", submitted["attempt_id"])

        self.assertEqual(insights["attempt_id"], submitted["attempt_id"])
        self.assertEqual(insights["record_status"], "recorded")
        self.assertGreaterEqual(insights["summary"]["total"], 5)
        self.assertIn("薄弱知识点", insights["headline"])
        self.assertTrue(insights["topic_impacts"])
        self.assertTrue(insights["next_actions"])
        self.assertIn("question_stats_updated", insights["recorded_fields"])
        self.assertIn("topic_stats_updated", insights["recorded_fields"])
```

- [ ] **Step 2: Run the failing test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewStoreTests.test_practice_attempt_insights_explain_recorded_learning_data
```

Expected:

```text
AttributeError: 'SystemPracticeReviewStore' object has no attribute 'build_practice_attempt_insights'
```

- [ ] **Step 3: Implement `build_practice_attempt_insights`**

Add this public method after `list_user_topic_stats`:

```python
    def build_practice_attempt_insights(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = validate_safe_id(user_id, "user_id")
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        attempt = self.get_practice_attempt(safe_user_id, safe_attempt_id)
        items = self.list_practice_attempt_items(safe_user_id, attempt_id=safe_attempt_id)
        question_stats = self.list_user_question_stats(safe_user_id)
        topic_stats = self.list_user_topic_stats(safe_user_id)

        summary = dict(attempt.get("summary") or {})
        weak_topics = self._practice_attempt_weak_topics(items, topic_stats)
        question_impacts = self._practice_attempt_question_impacts(items, question_stats)
        next_actions = self._practice_attempt_next_actions(summary, weak_topics)

        return {
            "attempt_id": safe_attempt_id,
            "practice_set_id": attempt.get("practice_set_id"),
            "record_status": "recorded" if items else "missing_items",
            "headline": self._practice_attempt_insight_headline(summary, weak_topics),
            "summary": summary,
            "topic_impacts": weak_topics,
            "question_impacts": question_impacts,
            "next_actions": next_actions,
            "recorded_fields": [
                "practice_attempt",
                "practice_attempt_items",
                "question_stats_updated",
                "topic_stats_updated",
            ],
        }
```

Add these helper methods near the stats helpers:

```python
    def _practice_attempt_weak_topics(
        self,
        items: list[dict[str, Any]],
        topic_stats: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        by_topic: dict[str, dict[str, Any]] = {}
        for item in items:
            status = str(item.get("final_status") or item.get("status") or "pending_review")
            for topic in item.get("topics") or []:
                label = str(topic)
                entry = by_topic.setdefault(label, {"topic": label, "attempt_count": 0, "wrong_count": 0})
                entry["attempt_count"] += 1
                if status in {"incorrect", "partial", "pending_review"}:
                    entry["wrong_count"] += 1

        for entry in by_topic.values():
            stat = next((value for value in topic_stats.values() if value.get("topic") == entry["topic"]), {})
            entry["lifetime_attempt_count"] = int(stat.get("attempt_count") or 0)
            entry["lifetime_wrong_count"] = int(stat.get("incorrect_count") or 0) + int(stat.get("partial_count") or 0)
            entry["wrong_rate"] = (
                entry["wrong_count"] / entry["attempt_count"]
                if entry["attempt_count"]
                else 0
            )

        return sorted(
            by_topic.values(),
            key=lambda item: (-float(item.get("wrong_rate") or 0), -int(item.get("wrong_count") or 0), item["topic"]),
        )[:3]

    def _practice_attempt_question_impacts(
        self,
        items: list[dict[str, Any]],
        question_stats: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        impacts: list[dict[str, Any]] = []
        for item in items:
            question_id = str(item.get("question_id") or "")
            stat = question_stats.get(question_id, {})
            impacts.append(
                {
                    "question_id": question_id,
                    "title": item.get("question_title") or question_id,
                    "final_status": item.get("final_status") or item.get("status") or "pending_review",
                    "judge_method": item.get("judge_method") or "local",
                    "attempt_count": int(stat.get("attempt_count") or 0),
                    "wrong_count": int(stat.get("incorrect_count") or 0),
                    "last_practiced_at": stat.get("latest_practiced_at"),
                }
            )
        return impacts

    def _practice_attempt_next_actions(
        self,
        summary: dict[str, Any],
        weak_topics: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        wrong_total = int(summary.get("incorrect") or 0) + int(summary.get("partial") or 0)
        pending_total = int(summary.get("pending_review") or 0)
        if wrong_total:
            actions.append({"type": "review_wrong", "label": f"复习 {wrong_total} 道错题"})
        if pending_total:
            actions.append({"type": "confirm_grading", "label": f"确认 {pending_total} 道待核对题"})
        if weak_topics:
            actions.append({"type": "topic_review", "label": f"优先复习 {weak_topics[0]['topic']}"})
        if not actions:
            actions.append({"type": "keep_practicing", "label": "本次表现稳定，可继续同类训练"})
        return actions

    def _practice_attempt_insight_headline(
        self,
        summary: dict[str, Any],
        weak_topics: list[dict[str, Any]],
    ) -> str:
        if weak_topics:
            return f"薄弱知识点：{weak_topics[0]['topic']}"
        if int(summary.get("incorrect") or 0) == 0 and int(summary.get("pending_review") or 0) == 0:
            return "本次练习记录已保存，暂无明显薄弱点"
        return "本次练习记录已保存，建议处理错题和待核对题"
```

- [ ] **Step 4: Run the backend test again**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewStoreTests.test_practice_attempt_insights_explain_recorded_learning_data
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit**

Only commit if the working tree is intentionally ready for this task:

```bash
git add materials/system_practice_review.py tests/test_system_practice_review.py
git commit -m "feat: 显化练习提交后的学习记录摘要"
```

---

### Task 2: Practice Attempt Detail API Returns Insights

**Files:**
- Modify: `materials/system_practice_review_api.py`
- Test: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing API test**

Extend `test_practice_attempt_api_returns_attempt_items_and_stats` with:

```python
self.assertEqual(payload["insights"]["record_status"], "recorded")
self.assertIn("next_actions", payload["insights"])
self.assertIn("topic_impacts", payload["insights"])
```

- [ ] **Step 2: Run the failing test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewStoreTests.test_practice_attempt_api_returns_attempt_items_and_stats
```

Expected:

```text
KeyError: 'insights'
```

- [ ] **Step 3: Add insights to the detail endpoint**

Change `get_practice_attempt` in `materials/system_practice_review_api.py`:

```python
        insights = store.build_practice_attempt_insights(uid, attempt_id)
        return {
            "ok": True,
            "user_id": uid,
            "practice_attempt": practice_attempt,
            "items": items,
            "summary": practice_attempt.get("summary") or {},
            "question_stats": store.list_user_question_stats(uid),
            "topic_stats": store.list_user_topic_stats(uid),
            "insights": insights,
        }
```

- [ ] **Step 4: Run the API test**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewStoreTests.test_practice_attempt_api_returns_attempt_items_and_stats
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit**

```bash
git add materials/system_practice_review_api.py tests/test_system_practice_review.py
git commit -m "feat: 返回练习记录可视化摘要"
```

---

### Task 3: Result Page Shows Recorded Learning Feedback

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `web/index.html`
- Test: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write failing frontend source test**

Add a test in `tests/test_system_library_frontend.py`:

```python
def test_practice_result_renders_learning_record_insights(self) -> None:
    source = APP_JS.read_text(encoding="utf-8")
    styles = STYLES_CSS.read_text(encoding="utf-8")

    self.assertIn("function renderPracticeAttemptInsights", source)
    self.assertIn("data-practice-record-insights", source)
    self.assertIn("本次练习已写入学习记录", source)
    self.assertIn(".practice-record-insights", styles)
```

- [ ] **Step 2: Run the failing frontend test**

Run:

```bash
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_practice_result_renders_learning_record_insights
```

Expected:

```text
AssertionError: 'function renderPracticeAttemptInsights' not found
```

- [ ] **Step 3: Add result insight renderer**

Add this helper near result rendering helpers in `web/app.js`:

```javascript
function renderPracticeAttemptInsights(practiceAttempt = {}) {
  const insights = practiceAttempt.insights || practiceAttempt.learning_insights || {};
  const summary = insights.summary || practiceAttempt.summary || {};
  const topicImpacts = Array.isArray(insights.topic_impacts) ? insights.topic_impacts : [];
  const nextActions = Array.isArray(insights.next_actions) ? insights.next_actions : [];
  const headline = insights.headline || "本次练习已写入学习记录";
  return `
    <section class="practice-record-insights" data-practice-record-insights>
      <div>
        <span class="eyebrow">LEARNING RECORD</span>
        <h4>本次练习已写入学习记录</h4>
        <p>${escapeHtml(headline)}</p>
      </div>
      <div class="practice-record-metrics">
        <span>正确 ${escapeHtml(String(summary.correct || 0))}</span>
        <span>错误 ${escapeHtml(String(summary.incorrect || 0))}</span>
        <span>待核对 ${escapeHtml(String(summary.pending_review || 0))}</span>
      </div>
      ${topicImpacts.length ? `
        <div class="practice-record-topic-list">
          ${topicImpacts.map((topic) => `
            <span>${escapeHtml(topic.topic || "")} · 本次错 ${escapeHtml(String(topic.wrong_count || 0))}/${escapeHtml(String(topic.attempt_count || 0))}</span>
          `).join("")}
        </div>
      ` : ""}
      ${nextActions.length ? `
        <div class="practice-record-actions">
          ${nextActions.map((action) => `<span>${escapeHtml(action.label || "")}</span>`).join("")}
        </div>
      ` : ""}
    </section>
  `;
}
```

In `renderPracticeAttemptResult`, place it directly under the result header:

```javascript
${renderPracticeAttemptInsights(practiceAttempt)}
```

- [ ] **Step 4: Preserve insights after fetching attempt detail**

In both submit and AI grade flows, after `fetchPracticeAttemptDetail`, merge:

```javascript
const detailAttempt = {
  ...(detail.practice_attempt || data.practice_attempt || practiceAttempt || {}),
  insights: detail.insights || {},
};
```

- [ ] **Step 5: Add CSS**

Add to `web/styles.css`:

```css
.practice-record-insights {
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid rgba(15, 118, 110, 0.2);
  border-left: 4px solid #0f766e;
  border-radius: 8px;
  background: #f7fffc;
}

.practice-record-insights h4 {
  margin: 2px 0 4px;
  color: #172033;
}

.practice-record-insights p {
  margin: 0;
  color: #526078;
}

.practice-record-metrics,
.practice-record-topic-list,
.practice-record-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.practice-record-metrics span,
.practice-record-topic-list span,
.practice-record-actions span {
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid #d6e4df;
  background: #ffffff;
  color: #172033;
  font-size: 13px;
  font-weight: 700;
}
```

- [ ] **Step 6: Bump cache version**

In `web/index.html`, change both query strings to:

```html
?v=20260706-learning-record-visibility-v2
```

Update the existing cache-bust test expectations in `tests/test_system_library_frontend.py`.

- [ ] **Step 7: Run frontend tests**

Run:

```bash
python -m unittest tests.test_system_library_frontend
```

Expected:

```text
OK
```

- [ ] **Step 8: Commit**

```bash
git add web/app.js web/styles.css web/index.html tests/test_system_library_frontend.py
git commit -m "feat: 练习结果页显化学习记录"
```

---

### Task 4: Question Drawer Shows Single-Question History

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_practice_review.py`
- Test: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write backend test for question learning snapshot**

Add:

```python
def test_question_learning_snapshot_returns_history_and_stats(self) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        users_root = Path(temp_dir) / "users"
        raw_root = Path(temp_dir) / "raw"
        write_test_questions(raw_root)
        store = SystemPracticeReviewStore(users_dir=users_root, raw_root=raw_root)
        practice_set = store.create_practice_set("tester", "kaoyan_math1_2099_q001", {"limit": 5})
        attempt = store.create_practice_attempt("tester", practice_set["set_id"])
        store.update_practice_attempt_answers(
            "tester",
            attempt["attempt_id"],
            {"kaoyan_math1_2099_q002": {"value": "A"}},
        )
        store.submit_practice_attempt("tester", attempt["attempt_id"])

        snapshot = store.build_question_learning_snapshot("tester", "kaoyan_math1_2099_q002")

        self.assertEqual(snapshot["question_id"], "kaoyan_math1_2099_q002")
        self.assertEqual(snapshot["attempt_count"], 1)
        self.assertEqual(len(snapshot["recent_attempts"]), 1)
        self.assertIn(snapshot["latest_status"], {"correct", "incorrect", "pending_review"})
```

- [ ] **Step 2: Implement store method**

Add:

```python
    def build_question_learning_snapshot(self, user_id: str, question_id: str) -> dict[str, Any]:
        safe_user_id = validate_safe_id(user_id, "user_id")
        safe_question_id = validate_safe_id(question_id, "question_id")
        stats = self.list_user_question_stats(safe_user_id).get(safe_question_id, {})
        items = self.list_practice_attempt_items(safe_user_id, question_id=safe_question_id)
        recent_items = sorted(
            items,
            key=lambda item: str(item.get("submitted_at") or item.get("graded_at") or ""),
            reverse=True,
        )[:5]
        return {
            "question_id": safe_question_id,
            "attempt_count": int(stats.get("attempt_count") or 0),
            "correct_count": int(stats.get("correct_count") or 0),
            "incorrect_count": int(stats.get("incorrect_count") or 0),
            "latest_status": stats.get("latest_status") or "",
            "latest_answer": stats.get("latest_answer"),
            "latest_practiced_at": stats.get("latest_practiced_at"),
            "wrong_streak": int(stats.get("wrong_streak") or 0),
            "recent_attempts": [
                {
                    "attempt_id": item.get("attempt_id"),
                    "practice_set_id": item.get("practice_set_id"),
                    "status": item.get("final_status") or item.get("status"),
                    "judge_method": item.get("judge_method"),
                    "submitted_at": item.get("submitted_at"),
                    "user_answer": item.get("user_answer"),
                }
                for item in recent_items
            ],
        }
```

- [ ] **Step 3: Add API endpoint**

In `materials/system_practice_review_api.py`:

```python
@router.get("/questions/{question_id}/learning-snapshot")
async def question_learning_snapshot(question_id: str, user_id: str = Query(default="tester")):
    uid = _safe_user_id(user_id)
    try:
        snapshot = _store().build_question_learning_snapshot(uid, question_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "user_id": uid, "snapshot": snapshot}
```

- [ ] **Step 4: Write frontend source test**

Add:

```python
def test_question_drawer_exposes_learning_history_snapshot(self) -> None:
    source = APP_JS.read_text(encoding="utf-8")
    styles = STYLES_CSS.read_text(encoding="utf-8")

    self.assertIn("function loadSystemQuestionLearningSnapshot", source)
    self.assertIn("function renderSystemQuestionLearningSnapshot", source)
    self.assertIn("learning-snapshot", source)
    self.assertIn(".system-learning-history", styles)
```

- [ ] **Step 5: Add frontend drawer fetch/render**

Add:

```javascript
async function loadSystemQuestionLearningSnapshot(questionId) {
  if (!questionId) return null;
  const data = await fetchJson(`/api/materials/system/questions/${encodeURIComponent(questionId)}/learning-snapshot?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
  return data.snapshot || null;
}

function renderSystemQuestionLearningSnapshot(snapshot = {}) {
  if (!snapshot || !snapshot.question_id) {
    return `<section class="system-drawer-section system-learning-history"><h4>练习记录</h4><p>暂无练习记录。</p></section>`;
  }
  const recent = Array.isArray(snapshot.recent_attempts) ? snapshot.recent_attempts : [];
  return `
    <section class="system-drawer-section system-learning-history">
      <h4>练习记录</h4>
      <div class="system-learning-history-metrics">
        <span>做过 ${escapeHtml(String(snapshot.attempt_count || 0))} 次</span>
        <span>错 ${escapeHtml(String(snapshot.incorrect_count || 0))} 次</span>
        <span>连续错 ${escapeHtml(String(snapshot.wrong_streak || 0))} 次</span>
      </div>
      ${recent.length ? `
        <ul>
          ${recent.map((item) => `
            <li>${escapeHtml(item.submitted_at || "未记录时间")} · ${escapeHtml(practiceResultStatusLabel(item.status || ""))} · ${escapeHtml(item.judge_method || "local")}</li>
          `).join("")}
        </ul>
      ` : `<p>暂无提交历史。</p>`}
    </section>
  `;
}
```

In `renderSystemQuestionDrawer`, include a placeholder:

```html
<div data-system-learning-history>${renderSystemQuestionLearningSnapshot(question.learning_snapshot || {})}</div>
```

After rendering the drawer:

```javascript
loadSystemQuestionLearningSnapshot(question.question_id)
  .then((snapshot) => {
    const target = systemQuestionDrawer.querySelector("[data-system-learning-history]");
    if (target) target.innerHTML = renderSystemQuestionLearningSnapshot(snapshot || {});
  })
  .catch(() => {
    const target = systemQuestionDrawer.querySelector("[data-system-learning-history]");
    if (target) target.innerHTML = renderSystemQuestionLearningSnapshot({});
  });
```

- [ ] **Step 6: Add CSS**

```css
.system-learning-history {
  display: grid;
  gap: 10px;
}

.system-learning-history-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.system-learning-history-metrics span {
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f7f5;
  border: 1px solid #d9e3df;
  color: #172033;
  font-weight: 700;
  font-size: 13px;
}

.system-learning-history ul {
  margin: 0;
  padding-left: 18px;
  color: #526078;
}
```

- [ ] **Step 7: Run backend and frontend tests**

Run:

```bash
python -m unittest tests.test_system_practice_review tests.test_system_library_frontend
```

Expected:

```text
OK
```

- [ ] **Step 8: Commit**

```bash
git add materials/system_practice_review.py materials/system_practice_review_api.py web/app.js web/styles.css tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "feat: 单题抽屉显示练习历史"
```

---

### Task 5: Review Plan Shows Recommendation Reasons

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_practice_review.py`
- Test: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write backend test for review task reasons**

Add to the review task tests:

```python
def test_review_tasks_include_learning_reason_from_stats(self) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        users_root = Path(temp_dir) / "users"
        raw_root = Path(temp_dir) / "raw"
        write_test_questions(raw_root)
        store = SystemPracticeReviewStore(users_dir=users_root, raw_root=raw_root)

        practice_set = store.create_practice_set("tester", "kaoyan_math1_2099_q001", {"limit": 5})
        attempt = store.create_practice_attempt("tester", practice_set["set_id"])
        store.update_practice_attempt_answers(
            "tester",
            attempt["attempt_id"],
            {"kaoyan_math1_2099_q002": {"value": "A"}},
        )
        store.submit_practice_attempt("tester", attempt["attempt_id"])

        task = store.create_review_task(
            "tester",
            target_type="question",
            target_id="kaoyan_math1_2099_q002",
            due_at="2099-01-01",
        )
        listed = store.list_review_tasks("tester")

        self.assertEqual(listed[0]["task_id"], task["task_id"])
        self.assertTrue(listed[0]["learning_reasons"])
```

- [ ] **Step 2: Implement reason enrichment**

Add:

```python
    def _review_task_learning_reasons(self, safe_user_id: str, task: dict[str, Any]) -> list[dict[str, str]]:
        target_type = str(task.get("target_type") or "")
        target_id = str(task.get("target_id") or "")
        reasons: list[dict[str, str]] = []
        if target_type == "question" and target_id:
            snapshot = self.build_question_learning_snapshot(safe_user_id, target_id)
            if snapshot.get("incorrect_count"):
                reasons.append({"type": "wrong_history", "label": f"历史错 {snapshot['incorrect_count']} 次"})
            if snapshot.get("wrong_streak"):
                reasons.append({"type": "wrong_streak", "label": f"连续错 {snapshot['wrong_streak']} 次"})
            if snapshot.get("latest_status") == "pending_review":
                reasons.append({"type": "pending_review", "label": "最近一次待核对"})
        if target_type == "practice_set":
            reasons.append({"type": "practice_set", "label": "来自同类训练练习单"})
        return reasons[:3]
```

In `list_review_tasks`, before returning records, enrich each record:

```python
records = [
    {**record, "learning_reasons": self._review_task_learning_reasons(safe_user_id, record)}
    for record in records
]
```

- [ ] **Step 3: Write frontend source test**

Add:

```python
def test_review_tasks_render_learning_reasons(self) -> None:
    source = APP_JS.read_text(encoding="utf-8")
    styles = STYLES_CSS.read_text(encoding="utf-8")

    self.assertIn("learning_reasons", source)
    self.assertIn("review-task-reasons", source)
    self.assertIn(".review-task-reasons", styles)
```

- [ ] **Step 4: Render reason chips**

In `renderReviewTaskCard`, add:

```javascript
const learningReasons = Array.isArray(task.learning_reasons) ? task.learning_reasons : [];
```

Inside the card body:

```javascript
${learningReasons.length ? `
  <div class="review-task-reasons">
    ${learningReasons.map((reason) => `<span>${escapeHtml(reason.label || "")}</span>`).join("")}
  </div>
` : ""}
```

- [ ] **Step 5: Add CSS**

```css
.review-task-reasons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.review-task-reasons span {
  padding: 5px 9px;
  border-radius: 999px;
  background: #fff7ed;
  border: 1px solid #fed7aa;
  color: #9a3412;
  font-size: 12px;
  font-weight: 700;
}
```

- [ ] **Step 6: Run review-related tests**

Run:

```bash
python -m unittest tests.test_system_practice_review tests.test_system_library_frontend
```

Expected:

```text
OK
```

- [ ] **Step 7: Commit**

```bash
git add materials/system_practice_review.py web/app.js web/styles.css tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "feat: 复习规划显示推荐原因"
```

---

### Task 6: Product Design Audit And Regression Verification

**Files:**
- No required source edits unless the audit finds a concrete issue.
- Capture screenshots to `E:/temp/learning-record-visibility-v2/`.

- [ ] **Step 1: Start or reuse local server**

Run the project server using the repo's normal command. If an existing server is running, reuse it.

Expected:

```text
Local URL available, for example http://127.0.0.1:<port>/
```

- [ ] **Step 2: Browser smoke path**

Use the in-app browser or Playwright-compatible browser control to verify:

```text
资料库 → 系统资料 → 生成同类训练 → 开始练习 → 填答案 → 提交练习 → 结果页
```

Required visible checks:

```text
结果页显示“本次练习已写入学习记录”
结果页显示正确/错误/待核对统计
结果页显示薄弱知识点或下一步建议
单题抽屉显示练习记录
复习规划卡片显示推荐原因
按钮均可见，不透明
```

- [ ] **Step 3: Save screenshots**

Save screenshots:

```text
E:/temp/learning-record-visibility-v2/practice-result-insights.png
E:/temp/learning-record-visibility-v2/question-drawer-history.png
E:/temp/learning-record-visibility-v2/review-task-reasons.png
```

- [ ] **Step 4: Run automated tests**

Run:

```bash
python -m compileall materials scripts tests
python -m unittest tests.test_system_practice_review
python -m unittest tests.test_system_library_frontend
python -m unittest tests.test_materials_mvp tests.test_agent_runtime
```

Expected:

```text
All commands exit 0. Existing deprecation warnings are acceptable if tests pass.
```

- [ ] **Step 5: Commit if changes were needed after audit**

If audit fixes were made:

```bash
git add materials/system_practice_review.py materials/system_practice_review_api.py web/app.js web/styles.css web/index.html tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "fix: 打磨学习记录显化体验"
```

---

## Self-Review

- Spec coverage: The plan covers result-page visibility, single-question history, and review-plan recommendation reasons. It intentionally excludes MySQL migration and full AI planner.
- Placeholder scan: No `TBD` or unbounded “add tests” steps remain; each task names files, tests, and expected results.
- Type consistency: Backend names are stable across tasks: `build_practice_attempt_insights`, `build_question_learning_snapshot`, `learning_reasons`, `insights`.
- Risk: `web/app.js` is already large. This plan limits changes to helpers near existing practice/review render functions instead of restructuring the frontend.
