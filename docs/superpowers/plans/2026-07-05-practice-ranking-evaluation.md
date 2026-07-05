# Practice Ranking Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add backend tests and a small ranking evaluator so similar-practice generation can compare weight formulas and keep the best default explainable.

**Architecture:** Keep the existing practice-set API shape. Extract ranking math into focused helpers inside `materials/system_practice_review.py` so tests can evaluate weight presets without touching raw question data. Preserve the two-step behavior: candidate selection by relevance, practice-set display by paper order.

**Tech Stack:** Python `unittest`, current `SystemPracticeReviewStore`, local fixture question JSONL under temporary directories.

---

### Task 1: Add Weight Comparison Tests

**Files:**
- Modify: `tests/test_system_practice_review.py`

- [ ] **Step 1: Write failing tests for ranking diagnostics**

Add tests that call a new evaluator on fixture questions:

```python
def test_practice_ranking_evaluates_weight_presets_with_diverse_samples(self) -> None:
    ...
```

The test must assert:
- default preset beats type-heavy preset on multi-topic relevance.
- every result includes `score_breakdown`.
- selected default preset is `topic_first_v2`.

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_system_practice_review.SystemPracticeReviewTest.test_practice_ranking_evaluates_weight_presets_with_diverse_samples
```

Expected: fail because evaluator does not exist.

### Task 2: Implement Ranking Evaluator

**Files:**
- Modify: `materials/system_practice_review.py`

- [ ] **Step 1: Add scoring presets and breakdown helper**

Add weight presets:

```python
PRACTICE_RANKING_PRESETS = {
    "legacy_linear": {"topic": 100, "type": 20, "library": 10},
    "type_heavy": {"topic": 60, "type": 70, "library": 10},
    "topic_first_v2": {"topic": 100, "all_topic_bonus": 35, "partial_topic_penalty": 15, "type": 18, "library": 8},
}
```

The new default remains knowledge-first, but distinguishes full topic coverage from partial overlap.

- [ ] **Step 2: Add evaluator method**

Add `evaluate_practice_ranking_presets(...)` returning per-preset ordered ids, per-item score breakdown, and aggregate metrics.

- [ ] **Step 3: Wire ranking to topic_first_v2**

Update `_rank_similar_questions` to use the same helper with `topic_first_v2` while preserving filtering and display order.

- [ ] **Step 4: Run targeted tests**

Run:

```bash
python -m unittest tests.test_system_practice_review
```

Expected: all tests pass.

### Task 3: Verify Stability

**Files:**
- No additional production files.

- [ ] **Step 1: Compile changed Python**

Run:

```bash
python -m compileall materials tests
```

Expected: exit code 0.

- [ ] **Step 2: Run focused regression suite**

Run:

```bash
python -m unittest tests.test_system_practice_review tests.test_system_library
```

Expected: all tests pass.

