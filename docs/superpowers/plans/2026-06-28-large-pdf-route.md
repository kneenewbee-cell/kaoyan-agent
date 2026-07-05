# Large PDF Route Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a pre-MinerU PDF size routing gate so small PDFs keep the current ingestion path and large PDFs are intercepted for the future split workflow.

**Architecture:** The existing `MinerUParser` and small-PDF path remain unchanged. `MaterialIngestionService` will call a new focused routing helper after file detection and before parsing; large PDFs write a route-plan artifact and fail clearly until the split workflow is implemented.

**Tech Stack:** Python dataclasses, existing `MaterialStorage`, `MaterialManifest`, and unittest mocks.

---

### Task 1: Routing Decision Helper

**Files:**
- Create: `materials/pdf_routing.py`
- Test: `tests/test_large_pdf_routing.py`

- [ ] Add tests for auto/normal/split PDF route decisions.
- [ ] Implement `decide_pdf_route()` with env/metadata threshold support.
- [ ] Verify tests pass with `python -m unittest tests.test_large_pdf_routing`.

### Task 2: Service Precheck Gate

**Files:**
- Modify: `materials/service.py`
- Test: `tests/test_large_pdf_routing.py`

- [ ] Add a failing test proving a large PDF does not call the parser.
- [ ] Add a failing test proving a small PDF still calls the current parser path.
- [ ] Insert the large-PDF decision after `detect_file()` and before `parser.parse()`.
- [ ] Write `parsed/large_pdf_route_plan.json` for large PDFs.
- [ ] Verify focused tests pass.

### Task 3: CLI Configuration

**Files:**
- Modify: `scripts/ingest_material.py`
- Modify: `.env.example`

- [ ] Add `--pdf-mode auto|normal|split` and pass it through metadata.
- [ ] Document threshold environment variables.
- [ ] Run compile and the required materials tests.
