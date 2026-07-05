# Adaptive LLM Material Rerank Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an optional recall-first material search path that builds an adaptive candidate set and lets an LLM judge choose primary, related, and hidden results.

**Architecture:** Keep the existing fast hybrid search as the default. Add a high-recall candidate builder that sizes retrieval budgets from the current searchable chunk count, then add an optional Qwen-compatible LLM reranker that consumes compressed candidates and returns structured decisions. Fall back to deterministic hybrid search whenever the LLM mode is disabled, unavailable, or invalid.

**Tech Stack:** Python stdlib, existing `materials.search` APIs, existing OpenAI-compatible Qwen client conventions, `unittest`.

---

### File Structure

- Create `materials/search_planning.py`: adaptive chunk counting, recall/LLM budgets, query-profile flags, and source quotas.
- Create `materials/llm_reranker.py`: candidate compression, Qwen-compatible JSON call, response validation, and application of decisions to `MaterialSearchResult`.
- Modify `materials/search.py`: add optional `mode="llm"` / `mode="hybrid_llm"` path, high-recall retrieval, candidate builder wiring, and safe fallback.
- Modify `tests/test_materials_vector_index.py`: tests for adaptive budgets and high-recall retrieval counts near existing search tests.
- Create `tests/test_materials_llm_reranker.py`: tests for candidate compression, LLM decision application, invalid JSON fallback, and API client payload.
- Optionally update `scripts/evaluate_material_retrieval.py`: allow `--mode llm` once the search mode exists.

### Task 1: Adaptive Retrieval Planning

**Files:**
- Create: `materials/search_planning.py`
- Test: `tests/test_materials_vector_index.py`

- [ ] **Step 1: Write failing tests**

Add tests that expect:

```python
from materials.search_planning import build_retrieval_plan

def test_adaptive_plan_for_small_scope_caps_llm_candidates(self):
    plan = build_retrieval_plan(chunk_count=60, query="方差公式", scope="material")
    self.assertEqual(plan.recall_limit, 12)
    self.assertEqual(plan.llm_candidate_limit, 6)
    self.assertEqual(plan.keyword_top_k, 6)
    self.assertEqual(plan.vector_top_k, 6)

def test_adaptive_plan_for_large_subject_caps_absolute_budget(self):
    plan = build_retrieval_plan(chunk_count=2500, query="指数分布 均匀分布 正态分布", scope="subject")
    self.assertEqual(plan.recall_limit, 80)
    self.assertEqual(plan.llm_candidate_limit, 32)
    self.assertTrue(plan.is_multi_intent)
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m unittest tests.test_materials_vector_index.MaterialsVectorIndexTest.test_adaptive_plan_for_small_scope_caps_llm_candidates tests.test_materials_vector_index.MaterialsVectorIndexTest.test_adaptive_plan_for_large_subject_caps_absolute_budget
```

Expected: import failure for `materials.search_planning`.

- [ ] **Step 3: Implement minimal planning module**

Create a frozen dataclass with fields:

```python
RetrievalPlan(
    chunk_count: int,
    recall_limit: int,
    llm_candidate_limit: int,
    keyword_top_k: int,
    vector_top_k: int,
    heading_top_k: int,
    formula_top_k: int,
    per_intent_top_k: int,
    is_multi_intent: bool,
    is_formula_query: bool,
)
```

Use these first-version rules:

```text
recall_limit = clamp(round(N * ratio), min=12, max=80)
llm_candidate_limit = clamp(round(N * llm_ratio), min=6, max=32)
material scope max: recall 40, llm 16
multi-intent ratio: recall 0.10, llm 0.05
formula ratio: recall 0.08, llm 0.04
default ratio: recall 0.08, llm 0.03
keyword_top_k and vector_top_k split recall budget roughly half/half
heading_top_k and formula_top_k are small additive paths capped by plan
```

- [ ] **Step 4: Run tests and verify GREEN**

Run the same two tests. Expected: both pass.

### Task 2: Candidate Compression and Decision Application

**Files:**
- Create: `materials/llm_reranker.py`
- Test: `tests/test_materials_llm_reranker.py`

- [ ] **Step 1: Write failing tests**

Add tests that expect:

```python
from materials.llm_reranker import build_candidate_payload, apply_llm_decisions

def test_candidate_payload_truncates_text_and_preserves_scores(self):
    result = MaterialSearchResult(... text="x" * 2000, metadata={"matched_by": ["keyword"]})
    payload = build_candidate_payload("方差公式", [result], max_text_chars=500)
    self.assertLessEqual(len(payload["candidates"][0]["text"]), 520)
    self.assertEqual(payload["candidates"][0]["chunk_id"], result.chunk_id)

def test_apply_llm_decisions_outputs_primary_then_related_and_hides_noise(self):
    results = [...]
    decisions = {"results": [
        {"chunk_id": "good", "decision": "primary", "rank": 1, "confidence": 0.9, "reason": "直接回答"},
        {"chunk_id": "related", "decision": "related", "rank": 2, "confidence": 0.7, "reason": "相关扩展"},
        {"chunk_id": "noise", "decision": "hide", "rank": 3, "confidence": 0.8, "reason": "不回答"}
    ]}
    ranked = apply_llm_decisions(results, decisions, top_k=5)
    self.assertEqual([item.chunk_id for item in ranked], ["good", "related"])
    self.assertEqual(ranked[0].metadata["llm_rerank"]["decision"], "primary")
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m unittest tests.test_materials_llm_reranker
```

Expected: import failure for `materials.llm_reranker`.

- [ ] **Step 3: Implement deterministic reranker helpers**

Implement:

```python
build_candidate_payload(query, results, max_text_chars=900) -> dict
validate_llm_decisions(payload, allowed_chunk_ids) -> dict
apply_llm_decisions(results, decision_payload, top_k) -> list[MaterialSearchResult]
```

Rules:

```text
Unknown chunk IDs are ignored.
Invalid decisions are ignored.
Only primary and related are returned.
Sort by decision group, then LLM rank, then confidence.
Attach metadata["llm_rerank"] with decision, reason, confidence.
If no valid visible decisions exist, return [].
```

- [ ] **Step 4: Run tests and verify GREEN**

Run `python -m unittest tests.test_materials_llm_reranker`. Expected: all pass.

### Task 3: Qwen-Compatible LLM Judge Client

**Files:**
- Modify: `materials/llm_reranker.py`
- Test: `tests/test_materials_llm_reranker.py`

- [ ] **Step 1: Write failing tests**

Add a fake OpenAI client test that verifies the payload uses:

```text
response_format={"type": "json_object"}
temperature=0
extra_body={"enable_thinking": False}
```

Also test that `build_material_search_rerank_client_from_env()` returns `None` when no API key exists.

- [ ] **Step 2: Run tests and verify RED**

Expected: missing client functions.

- [ ] **Step 3: Implement client**

Implement:

```python
MaterialSearchRerankClient.rerank(payload) -> dict
build_material_search_rerank_client_from_env(env_path=None, timeout_seconds=60)
generate_material_search_rerank_with_qwen(payload, ...)
```

Use `QWEN_API_KEY` / `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL`, and `MATERIALS_SEARCH_RERANK_MODEL`, falling back to `QWEN_CLEANING_STRATEGY_MODEL`.

- [ ] **Step 4: Run tests and verify GREEN**

Run `python -m unittest tests.test_materials_llm_reranker`. Expected: all pass.

### Task 4: Search Integration

**Files:**
- Modify: `materials/search.py`
- Test: `tests/test_materials_vector_index.py`

- [ ] **Step 1: Write failing integration tests**

Add tests that patch keyword/vector retrieval and a fake reranker:

```python
def test_llm_mode_uses_adaptive_high_recall_before_judging(self):
    with patch("materials.search.search_user_materials_keyword") as keyword, ...
        results = search_user_materials("tester", "方差公式", top_k=5, mode="llm", rerank_client=fake_client)
    self.assertGreater(keyword.call_args.kwargs["top_k"], 5)
    self.assertGreater(vector.call_args.kwargs["top_k"], 5)
    self.assertEqual(results[0].metadata["llm_rerank"]["decision"], "primary")

def test_llm_mode_falls_back_to_hybrid_when_client_missing(self):
    ...
```

- [ ] **Step 2: Run tests and verify RED**

Expected: `mode="llm"` not supported or `rerank_client` not accepted.

- [ ] **Step 3: Implement search wiring**

Add `llm` and `hybrid_llm` to `_normalize_search_mode`. Add optional keyword-only `rerank_client=None` to `search_user_materials`. For LLM mode:

```text
count scope chunks from ready manifests
build adaptive plan
retrieve keyword/vector with plan budgets
merge using hybrid scoring without final display filter by requesting recall_limit
compress candidates to llm_candidate_limit with source diversity
call rerank client
apply decisions
expand split context
fallback to deterministic hybrid if client missing or errors
```

- [ ] **Step 4: Run tests and verify GREEN**

Run `python -m unittest tests.test_materials_vector_index tests.test_materials_llm_reranker`.

### Task 5: Evaluation Script Mode

**Files:**
- Modify: `scripts/evaluate_material_retrieval.py`

- [ ] **Step 1: Add `llm` to the mode choices**

Allow:

```text
--mode keyword|vector|hybrid|llm
```

The evaluation script can use deterministic fallback if no real client is present.

- [ ] **Step 2: Compile**

Run:

```bash
python -m py_compile scripts/evaluate_material_retrieval.py
```

Expected: exit 0.

### Task 6: Verification

**Files:** no new files

- [ ] Run:

```bash
python -m compileall materials scripts tests
python -m unittest tests.test_materials_llm_reranker
python -m unittest tests.test_materials_vector_index
python -m unittest tests.test_materials_mvp
python -m unittest tests.test_agent_runtime
```

Expected: all pass, preserving the existing skipped test in `tests.test_agent_runtime`.

- [ ] Run the current retrieval eval:

```bash
python scripts/evaluate_material_retrieval.py --config balanced_v3_gate_exact --output data/runtime/evals/material_retrieval_balanced_v3_after_llm_wiring.json
```

Expected: deterministic hybrid baseline remains stable.

---

### Self-Review

- Spec coverage: adaptive budgets, bounded LLM candidates, recall-first retrieval, structured LLM decisions, fallback behavior, and tests are covered.
- Placeholder scan: no implementation step relies on "later" behavior; concrete functions and commands are named.
- Type consistency: `RetrievalPlan`, `MaterialSearchRerankClient`, `build_candidate_payload`, and `apply_llm_decisions` are consistently referenced.
