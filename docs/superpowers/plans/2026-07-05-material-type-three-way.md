# Material Type Three-Way Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse user material top-level types to `textbook`, `lecture`, and `exercise`, while preserving legacy input compatibility and storing exam-like nuance in metadata.

**Architecture:** Keep `MaterialType.UNKNOWN` as an internal detection state, but remove legacy enum members from the formal type set. Normalize all legacy inputs at service and manifest-read boundaries, and add a lightweight `structure_profile.exercise_kind` metadata value for exam papers, problem sets, worked examples, and wrong-book-like material.

**Tech Stack:** Python dataclasses/enums, FastAPI query/form handling, unittest, vanilla frontend JavaScript.

---

### Task 1: Type Contract Tests

**Files:**
- Modify: `tests/test_materials_mvp.py`

- [ ] **Step 1: Write failing tests**

Add tests that assert only the three active material types are exposed, legacy manifest values read as modern types, and service normalization maps legacy inputs to the modern values.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_material_type_contract_uses_three_active_types tests.test_materials_mvp.MaterialsMvpTest.test_legacy_material_type_values_are_mapped_on_manifest_read tests.test_materials_mvp.MaterialsMvpTest.test_service_normalizes_legacy_material_type_inputs
```

Expected: FAIL because legacy enum values still exist or the helper/behavior is missing.

### Task 2: Normalize Schema And Service

**Files:**
- Modify: `materials/schemas.py`
- Modify: `materials/service.py`
- Modify: `materials/postprocess/metadata_extractor.py`

- [ ] **Step 1: Remove legacy enum members**

Keep `TEXTBOOK`, `LECTURE`, `EXERCISE`, and `UNKNOWN`; add a helper that maps `note`, `exam`, `wrong_book`, `school_info`, and `other` to modern types.

- [ ] **Step 2: Use helper at manifest load and service normalization**

`MaterialManifest.from_dict()` should tolerate old manifests. `MaterialIngestionService._normalize_material_type()` should accept old CLI/API inputs but store only modern types.

- [ ] **Step 3: Add lightweight structure profile inference**

Add metadata like:

```json
{"structure_profile": {"exercise_kind": "exam_paper"}}
```

for filenames/markdown that indicate real exams, papers, wrong books, worked examples, or generic problem sets.

- [ ] **Step 4: Run tests**

Run the Task 1 tests and then `python -m unittest tests.test_materials_mvp`.

### Task 3: Public Option Cleanup

**Files:**
- Modify: `scripts/ingest_material.py`
- Modify: `scripts/query_materials.py`
- Modify: `materials/api.py`
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `tests/test_user_materials_frontend.py`

- [ ] **Step 1: Update tests for frontend labels/options**

Assert that visible material type labels only include three active options and legacy labels are not present in the user-materials labels.

- [ ] **Step 2: Restrict CLI/API/frontend choices**

Upload/search/list should use only `textbook`, `lecture`, `exercise` plus `unknown` where needed for upload auto-detection.

- [ ] **Step 3: Verify frontend and backend**

Run:

```bash
python -m unittest tests.test_user_materials_frontend tests.test_materials_mvp
node --check web\app.js
python -m compileall materials scripts tests
```

---

Self-review:

- Scope is limited to material type contract and lightweight structure metadata.
- No `qa` changes.
- No PDF/MinerU reconstruction or single-question chunking in this plan; those build on the new `exercise_kind` later.
