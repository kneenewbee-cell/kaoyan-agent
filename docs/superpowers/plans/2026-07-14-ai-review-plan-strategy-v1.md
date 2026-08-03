# AI Review Plan Strategy v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the five AI review planning modes use distinct backend candidate policies, and add an evaluation harness with many user personas before broad AI tuning.

**Architecture:** Add a small policy layer that turns `mode + include_types + learning context` into a constrained candidate pool. Keep AI generation side-effect free; AI receives a mode-aware compressed context, and fallback planning uses the same policy. Add deterministic policy/evaluator tests first so the backend can be tuned without repeatedly calling the model.

**Tech Stack:** Python 3 standard library, FastAPI router already in `materials/system_practice_review_api.py`, existing JSONL user-state repository in `materials/system_practice_review.py`, unittest test suite.

## Global Constraints

- Do not refactor `qa/`.
- Do not introduce a large database migration for this feature.
- System-layer question content remains readonly; user planning state writes only to user-layer records.
- AI planning must remain draft-only until the user explicitly commits selected tasks.
- Default AI planning model remains `deepseek-v4-flash`.
- Real AI calls are sampled later; first implementation must be verifiable without network calls.
- Frontend can continue using the existing AI planning modal; first backend slice should not require a new page.

---

### Task 1: Mode Policy and Candidate Filtering

**Files:**
- Create: `materials/system_review_plan_policy.py`
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Test: `tests/test_system_practice_review.py`

**Interfaces:**
- Produces: `build_mode_policy(mode: str, include_types: Iterable[str] | None = None) -> dict`
- Produces: `apply_mode_policy(candidates: dict[str, list[dict]], policy: dict) -> dict[str, list[dict]]`
- Consumes: existing `SystemPracticeReviewStore.build_ai_planning_context(...)`.

- [ ] **Step 1: Write failing policy tests**

Add tests proving:

```python
def test_ai_planning_context_wrong_mode_excludes_unstarted_candidates(self):
    ...
    response = client.get(
        "/api/materials/system/ai-planning-context",
        params={"user_id": "tester", "subject": "math", "mode": "wrong", "include_types": "unstarted_questions"},
    )
    context = response.json()["context"]
    self.assertEqual(context["constraints"]["mode"], "wrong")
    self.assertIn("unstarted_questions", context["policy"]["disabled_types"])
    self.assertEqual(context["ai_candidates"].get("unstarted_questions", []), [])
```

```python
def test_ai_planning_context_startup_mode_allows_unstarted_candidates(self):
    ...
    context = response.json()["context"]
    self.assertEqual(context["constraints"]["mode"], "startup")
    self.assertIn("unstarted_questions", context["policy"]["enabled_types"])
    self.assertIn("startup_candidates", context["ai_candidates"])
```

- [ ] **Step 2: Run tests and verify red**

Run:

```powershell
E:\python_project\.venv_mineru\Scripts\python.exe -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_planning_context_wrong_mode_excludes_unstarted_candidates tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_planning_context_startup_mode_allows_unstarted_candidates
```

Expected: fail because `mode`, `policy`, and unstarted candidate pools are not implemented.

- [ ] **Step 3: Implement minimal policy module**

Create `materials/system_review_plan_policy.py` with:

```python
MODE_POLICIES = {
    "balanced": {...},
    "weak": {...},
    "wrong": {...},
    "startup": {...},
    "sprint": {...},
}
```

Each policy returns:

```python
{
    "mode": "wrong",
    "label": "错题回收",
    "enabled_types": [...],
    "disabled_types": [...],
    "quotas": {...},
    "hard_rules": [...]
}
```

`include_types` can narrow enabled types but cannot re-enable disabled types unless `manual_override=True`, which is not exposed in this first slice.

- [ ] **Step 4: Wire policy into context**

Update `SystemPracticeReviewStore.build_ai_planning_context` signature:

```python
def build_ai_planning_context(..., mode: str = "balanced", include_types: list[str] | None = None) -> dict[str, Any]:
```

Add `constraints.mode`, `constraints.include_types`, `policy`, and filtered `ai_candidates`.

- [ ] **Step 5: Wire API params and draft body**

Update `/ai-planning-context` to accept `mode` and repeated or comma-separated `include_types`.

Update `/ai-review-plan/draft` to pass `mode` and `include_types` from the request body.

- [ ] **Step 6: Run targeted tests**

Run the same two tests. Expected: PASS.

---

### Task 2: Startup Candidate Pool

**Files:**
- Modify: `materials/system_practice_review.py`
- Test: `tests/test_system_practice_review.py`

**Interfaces:**
- Produces: `_ai_planning_startup_candidates(user_id: str, subject: str, limit: int) -> list[dict[str, Any]]`

- [ ] **Step 1: Write failing cold-start test**

Add:

```python
def test_ai_planning_context_cold_start_uses_startup_candidates_not_weak_topics(self):
    ...
    context = response.json()["context"]
    self.assertEqual(context["constraints"]["mode"], "startup")
    self.assertEqual(context["ai_candidates"]["weak_topics"], [])
    self.assertTrue(context["ai_candidates"]["startup_candidates"])
    self.assertEqual(context["ai_candidates"]["startup_candidates"][0]["candidate_type"], "startup_question")
```

- [ ] **Step 2: Run and verify red**

Expected: fail because startup candidates are absent.

- [ ] **Step 3: Implement startup candidates**

Read system questions through existing system library APIs. Pick by:

1. subject/exam_type match.
2. basic topic preference if available.
3. recent years first.
4. question order within year.

Return compact items:

```python
{
    "candidate_type": "startup_question",
    "question_id": "...",
    "title": "...",
    "topics": [...],
    "question_type": "...",
    "reason": "起步候选：匹配当前考试范围和基础知识点",
}
```

- [ ] **Step 4: Run targeted test**

Expected: PASS.

---

### Task 3: Mode-Aware Prompt and Fallback

**Files:**
- Modify: `materials/system_ai_planner.py`
- Test: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: `context["policy"]`.
- Produces: fallback items that respect policy enabled/disabled types.

- [ ] **Step 1: Write failing prompt test**

Extend `test_ai_review_plan_prompt_is_readable_chinese` or add a new test:

```python
def test_ai_review_plan_prompt_includes_mode_policy(self):
    prompt = _planning_prompt({"constraints": {"mode": "wrong", "days": 3}, "policy": {"label": "错题回收", "disabled_types": ["unstarted_questions"]}, "ai_candidates": {}})
    self.assertIn("错题回收", prompt)
    self.assertIn("unstarted_questions", prompt)
```

- [ ] **Step 2: Run and verify red**

Expected: fail until prompt includes policy in readable text.

- [ ] **Step 3: Update prompt**

Use clear Chinese text and JSON schema. Do not keep mojibake strings in newly added prompt text.

- [ ] **Step 4: Update fallback**

Fallback should choose from candidate groups allowed by policy. In wrong mode, it should not generate startup/new-task fallback items.

- [ ] **Step 5: Run prompt/fallback tests**

Expected: PASS.

---

### Task 4: Evaluation Personas and Deterministic Harness

**Files:**
- Create: `materials/system_review_plan_evaluator.py`
- Test: `tests/test_system_practice_review.py`

**Interfaces:**
- Produces: `build_persona_catalog() -> list[dict[str, Any]]`
- Produces: `evaluate_mode_policy_for_personas(personas: list[dict[str, Any]], modes: list[str] | None = None) -> dict[str, Any]`

- [ ] **Step 1: Write failing evaluator tests**

Add:

```python
def test_ai_plan_persona_catalog_has_at_least_sixty_fixed_personas(self):
    personas = build_persona_catalog()
    self.assertGreaterEqual(len(personas), 60)
    self.assertTrue(any(p["category"] == "cold_start" for p in personas))
    self.assertTrue(any(p["category"] == "heavy_wrong" for p in personas))
```

```python
def test_ai_plan_policy_evaluator_runs_all_five_modes(self):
    report = evaluate_mode_policy_for_personas(build_persona_catalog()[:3])
    self.assertEqual(set(report["modes"]), {"balanced", "weak", "wrong", "startup", "sprint"})
    self.assertEqual(report["case_count"], 15)
```

- [ ] **Step 2: Run and verify red**

Expected: fail because evaluator does not exist.

- [ ] **Step 3: Implement evaluator catalog**

Hard-code the first 60 fixed personas from the design doc with concise fields:

```python
{
    "persona_id": "cold_001",
    "category": "cold_start",
    "practice_volume": 0,
    "wrong_level": "none",
    ...
}
```

- [ ] **Step 4: Implement deterministic policy evaluation**

The evaluator does not call AI. It checks:

- case count.
- disabled type violations.
- cold start suitability.
- mode consistency.
- candidate coverage fields are present.

- [ ] **Step 5: Run evaluator tests**

Expected: PASS.

---

### Task 5: Frontend Copy and Policy Visibility

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: `context.policy`, `context.limits`, and `context.ai_candidates`.

- [ ] **Step 1: Write failing frontend static tests**

Add assertions that frontend references:

```python
self.assertIn("policy.disabled_types", source)
self.assertIn("本模式默认不纳入", source)
self.assertIn("页面显示 Top", source)
```

- [ ] **Step 2: Run and verify red**

Expected: fail until copy is added.

- [ ] **Step 3: Add policy visibility copy**

In AI planning settings step, show:

- current mode label.
- enabled candidate groups.
- disabled candidate groups.
- UI Top-K vs AI Top-K note.

- [ ] **Step 4: Run frontend test**

Expected: PASS.

---

### Task 6: Verification

**Files:**
- No new files.

- [ ] **Step 1: Run Python compile**

```powershell
E:\python_project\.venv_mineru\Scripts\python.exe -m compileall materials tests
```

- [ ] **Step 2: Run targeted backend tests**

```powershell
E:\python_project\.venv_mineru\Scripts\python.exe -m unittest tests.test_system_practice_review
```

- [ ] **Step 3: Run frontend static tests**

```powershell
E:\python_project\.venv_mineru\Scripts\python.exe -m unittest tests.test_system_library_frontend
```

- [ ] **Step 4: Run JS syntax check**

```powershell
node --check web\app.js
```

- [ ] **Step 5: Report remaining gaps**

Report whether real AI sampling has been run. If not, state that the current slice validates policy and evaluator only, and that real `deepseek-v4-flash` sampling is the next tuning phase.
