# AI Review Plan Load Formula Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic load-aware AI review planning so question type, user state, difficulty, and oversized practice sheets shape daily planning before the AI prompt.

**Architecture:** Introduce a focused `materials.system_review_plan_load` utility for load calculation and practice-sheet segmentation. Enrich planning candidates in `SystemPracticeReviewStore.build_ai_planning_context`, then make `system_ai_planner.py` prompt, normalize, dedupe, and rebalance from local candidate load instead of model guesses.

**Tech Stack:** Python 3 standard library, existing `unittest` suite, existing FastAPI endpoints, no new dependencies.

## Global Constraints

- Do not refactor `qa/`.
- Keep practice sheets whole at the source-data layer.
- Create planning segments that point back to parent practice sheets.
- Balance by `load_units` and `estimated_minutes`, not raw item count.
- AI receives compact candidates, not full question text, answers, or explanations.
- AI must not invent IDs, split sheets itself, or override local timing.
- New fields must be additive to preserve existing API compatibility.

---

### Task 1: Load Formula Utility

**Files:**
- Create: `materials/system_review_plan_load.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Produces: `calculate_question_load_units(question: dict[str, Any], state: str | None = None) -> float`
- Produces: `calculate_candidate_load(candidate: dict[str, Any], candidate_type: str | None = None) -> dict[str, Any]`
- Produces: `estimate_minutes_from_load(load_units: float) -> int`

- [ ] **Step 1: Write failing tests**

Add tests importing the new functions:

```python
from materials.system_review_plan_load import (
    calculate_candidate_load,
    calculate_question_load_units,
    estimate_minutes_from_load,
)

def test_ai_review_plan_question_load_uses_type_state_and_difficulty(self) -> None:
    easy_choice = {"question_type": "single_choice", "difficulty": "easy"}
    hard_wrong_proof = {"question_type": "proof", "difficulty": "hard", "state": "wrong"}

    self.assertAlmostEqual(calculate_question_load_units(easy_choice, "unstarted"), 0.85)
    self.assertAlmostEqual(calculate_question_load_units(hard_wrong_proof), 2.8)
    self.assertEqual(estimate_minutes_from_load(8.1), 58)

def test_ai_review_plan_candidate_load_sums_question_details(self) -> None:
    candidate = {
        "candidate_type": "draft_attempts",
        "question_ids": ["q1", "q2", "q3"],
        "questions": [
            {"question_id": "q1", "question_type": "single_choice", "difficulty": "medium"},
            {"question_id": "q2", "question_type": "fill_blank", "difficulty": "unknown"},
            {"question_id": "q3", "question_type": "solution", "difficulty": "hard"},
        ],
        "state": "draft_unanswered",
    }

    load = calculate_candidate_load(candidate)

    self.assertEqual(load["question_count"], 3)
    self.assertEqual(load["question_type_mix"], {"single_choice": 1, "fill_blank": 1, "solution": 1})
    self.assertGreater(load["load_units"], 5.0)
    self.assertEqual(load["estimated_minutes"], estimate_minutes_from_load(load["load_units"]))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_review_plan_question_load_uses_type_state_and_difficulty tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_review_plan_candidate_load_sums_question_details`

Expected: FAIL or ERROR because `materials.system_review_plan_load` does not exist.

- [ ] **Step 3: Implement minimal utility**

Create constants for type, state, difficulty, clamp limits, and minutes per load unit. Implement load calculation from `questions`, `question_details`, or scalar `question_type`/`difficulty` fields, with neutral defaults for unknowns.

- [ ] **Step 4: Run tests to verify they pass**

Run the same two tests. Expected: PASS.

---

### Task 2: Practice-Sheet Segmentation

**Files:**
- Modify: `materials/system_review_plan_load.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Produces: `split_candidate_into_plan_segments(candidate: dict[str, Any], *, daily_minutes: int, days: int, candidate_type: str | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]`

- [ ] **Step 1: Write failing tests**

Add tests:

```python
def test_ai_review_plan_splits_oversized_practice_sheet_without_mutating_parent(self) -> None:
    candidate = {
        "candidate_type": "draft_attempts",
        "attempt_id": "pa_big",
        "practice_set_id": "ps_big",
        "title": "Large sheet",
        "question_ids": [f"q{i}" for i in range(1, 21)],
        "questions": [
            {"question_id": f"q{i}", "question_type": "solution", "difficulty": "hard"}
            for i in range(1, 21)
        ],
        "state": "draft_unanswered",
    }
    original_ids = list(candidate["question_ids"])

    segments, pending = split_candidate_into_plan_segments(candidate, daily_minutes=60, days=3)

    self.assertGreater(len(segments), 1)
    self.assertTrue(pending)
    self.assertEqual(candidate["question_ids"], original_ids)
    self.assertEqual(segments[0]["parent_practice_set_id"], "ps_big")
    self.assertEqual(segments[0]["part_index"], 1)
    self.assertEqual(segments[0]["part_count"], len(segments) + len(pending))
    self.assertLessEqual(segments[0]["estimated_minutes"], 69)

def test_ai_review_plan_keeps_small_practice_sheet_whole(self) -> None:
    candidate = {
        "candidate_type": "unstarted_questions",
        "source_id": "sheet_small",
        "question_ids": ["q1", "q2"],
        "questions": [
            {"question_id": "q1", "question_type": "single_choice", "difficulty": "medium"},
            {"question_id": "q2", "question_type": "fill_blank", "difficulty": "unknown"},
        ],
        "state": "unstarted",
    }

    segments, pending = split_candidate_into_plan_segments(candidate, daily_minutes=60, days=7)

    self.assertEqual(len(segments), 1)
    self.assertEqual(pending, [])
    self.assertNotIn("part_index", segments[0])
```

- [ ] **Step 2: Run tests to verify they fail**

Run both new tests. Expected: ERROR because the split helper is missing.

- [ ] **Step 3: Implement segmentation**

Split only when load exceeds `daily_target_units * 1.15` and question detail exists. Keep the parent candidate unchanged. Use deterministic segment IDs such as `{parent_id}:seg:{index}`. Mark overflow beyond `days * daily_minutes` as `later_pending`.

- [ ] **Step 4: Run tests to verify they pass**

Run both new tests. Expected: PASS.

---

### Task 3: Enrich AI Planning Context

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: `calculate_candidate_load`, `split_candidate_into_plan_segments`
- Produces: AI candidates with `load_units`, `estimated_minutes`, `question_type_mix`, `state_mix`, `difficulty_mix`, and segment metadata.

- [ ] **Step 1: Write failing tests**

Add tests around `build_ai_planning_context`:

```python
def test_ai_planning_context_enriches_candidates_with_load_fields(self) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        raw_root = self._make_raw_root(base / "raw", include_blank=True)
        users_root = base / "users"
        store = self._store(raw_root, users_root)
        context = store.build_ai_planning_context("tester", subject="math", mode="startup", days=7, daily_minutes=60)

        candidate = context["ai_candidates"]["unstarted_questions"][0]

        self.assertIn("load_units", candidate)
        self.assertIn("estimated_minutes", candidate)
        self.assertIn("question_type_mix", candidate)
        self.assertIn("splittable", candidate)
        self.assertNotIn("explanation", candidate)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_ai_planning_context_enriches_candidates_with_load_fields`

Expected: FAIL because existing candidates do not all include load fields.

- [ ] **Step 3: Implement enrichment**

Add a private store helper that attaches question details from `SystemQuestionLibrary` when possible, computes load, drops heavy text fields from AI candidate payloads, and expands oversized practice/draft candidates into segment candidates.

- [ ] **Step 4: Run the test to verify it passes**

Run the same test. Expected: PASS.

---

### Task 4: Prompt And Normalization

**Files:**
- Modify: `materials/system_ai_planner.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: enriched candidate fields.
- Produces: normalized items that carry `load_units`, `parent_practice_set_id`, `part_index`, and `part_count`.

- [ ] **Step 1: Write failing tests**

Add tests:

```python
def test_ai_review_plan_prompt_uses_precomputed_load_and_segments(self) -> None:
    prompt = _planning_prompt(
        {
            "constraints": {"days": 2, "daily_minutes": 60, "mode": "balanced"},
            "policy": {"type_priority": ["draft_attempts"]},
            "ai_candidates": {"draft_attempts": [{"source_id": "pa:seg:1", "load_units": 8.1, "estimated_minutes": 58}]},
        }
    )

    self.assertIn("load_units", prompt)
    self.assertIn("estimated_minutes", prompt)
    self.assertIn("Do not split practice sheets yourself", prompt)
    self.assertNotIn("璇峰", prompt)

def test_ai_plan_normalization_recomputes_minutes_and_preserves_segment_metadata(self) -> None:
    context = {
        "constraints": {"days": 1, "daily_minutes": 60},
        "policy": {"enabled_types": ["draft_attempts"]},
        "ai_candidates": {
            "draft_attempts": [
                {
                    "source_id": "pa_big:seg:1",
                    "candidate_type": "draft_attempts",
                    "title": "Large sheet - Part 1/3",
                    "load_units": 8.1,
                    "estimated_minutes": 58,
                    "parent_practice_set_id": "ps_big",
                    "part_index": 1,
                    "part_count": 3,
                }
            ]
        },
    }

    payload = _normalize_ai_plan_payload(
        {
            "days": [
                {
                    "date": "2099-01-02",
                    "items": [
                        {
                            "type": "continue_draft",
                            "title": "Bad estimate",
                            "estimated_minutes": 5,
                            "source_ids": ["pa_big:seg:1"],
                        }
                    ],
                }
            ]
        },
        context=context,
        model="deepseek-v4-flash",
    )

    item = payload["days"][0]["items"][0]
    self.assertEqual(item["estimated_minutes"], 58)
    self.assertEqual(item["load_units"], 8.1)
    self.assertEqual(item["parent_practice_set_id"], "ps_big")
    self.assertEqual(item["part_index"], 1)
    self.assertEqual(item["part_count"], 3)
```

- [ ] **Step 2: Run tests to verify they fail**

Run the two tests. Expected: FAIL because prompt and normalizer do not yet carry segment load fields.

- [ ] **Step 3: Implement prompt and normalization changes**

Rewrite prompt text in readable Chinese plus explicit load/segment constraints. Extend `_normalize_plan_item` to overlay trusted candidate metadata from lookup. Update `_plan_item_load_minutes` to prefer candidate `estimated_minutes`.

- [ ] **Step 4: Run tests to verify they pass**

Run both tests. Expected: PASS.

---

### Task 5: Dedupe And Evaluation

**Files:**
- Modify: `materials/system_ai_planner.py`
- Modify: `materials/system_review_plan_evaluator.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: segment IDs.
- Produces: dedupe by segment ID, while allowing multiple segments from one parent practice sheet.

- [ ] **Step 1: Write failing tests**

Add a test where two items share `parent_practice_set_id` but have different segment IDs and both survive normalization.

- [ ] **Step 2: Run test to verify it fails**

Run the new test. Expected: FAIL if dedupe collapses by parent or metadata is lost.

- [ ] **Step 3: Implement dedupe/evaluator updates**

Ensure source IDs include `candidate_id` and `plan_segment_id`. Add evaluator synthetic candidates with question type, difficulty, and segment load metrics.

- [ ] **Step 4: Run targeted tests**

Run: `python -m unittest tests.test_system_practice_review`

Expected: PASS.

---

### Task 6: Frontend Display Hooks

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: item `load_units`, `part_index`, `part_count`, `parent_practice_set_id`.
- Produces: visible daily load and practice-sheet part labels without changing practice-sheet identity.

- [ ] **Step 1: Write failing frontend string tests**

Add assertions that `app.js` contains helpers for formatting load and plan part labels.

- [ ] **Step 2: Run frontend tests to verify failure**

Run: `python -m unittest tests.test_system_library_frontend`

Expected: FAIL because helpers are missing.

- [ ] **Step 3: Implement minimal frontend helpers**

Render load metadata where AI plan items are displayed. Keep UI additive and avoid layout rewrites.

- [ ] **Step 4: Run frontend tests**

Run: `python -m unittest tests.test_system_library_frontend`

Expected: PASS.

---

### Task 7: Final Verification

**Files:**
- No new files.

**Interfaces:**
- Verifies all changed surfaces.

- [ ] **Step 1: Compile Python**

Run: `python -m compileall materials scripts tests`

Expected: exit 0.

- [ ] **Step 2: Run focused review planning tests**

Run: `python -m unittest tests.test_system_practice_review tests.test_system_library_frontend`

Expected: PASS.

- [ ] **Step 3: Run JavaScript syntax check**

Run: `node --check web/app.js`

Expected: exit 0.

- [ ] **Step 4: Inspect diff**

Run: `git diff -- materials/system_review_plan_load.py materials/system_ai_planner.py materials/system_practice_review.py materials/system_review_plan_evaluator.py tests/test_system_practice_review.py web/app.js web/styles.css tests/test_system_library_frontend.py docs/superpowers/plans/2026-08-02-ai-review-plan-load-formula.md`

Expected: Diff only includes planned changes.
