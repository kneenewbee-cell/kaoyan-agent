# Exercise Structure LLM Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local-window LLM repair stage for uploaded exercise materials so missing problem numbers swallowed by the previous problem can be split into problem-level chunks.

**Architecture:** Keep `exercise_structure` as the primary deterministic analyzer. Add a focused `exercise_structure_repair` stage that builds candidate windows only for missing indices, asks DeepSeek V4 Flash to judge the local boundary, then applies the result only after local validation. The stage updates `problem_groups` and reports repair evidence without rewriting `parsed/content.md`.

**Tech Stack:** Python standard library, OpenAI-compatible DeepSeek client, existing materials ingestion service, `unittest`.

---

## File Structure

- Create `materials/postprocess/deepseek_structure_client.py`
  - Reads `MATERIALS_STRUCTURE_REPAIR_*` or `DEEPSEEK_*` environment variables.
  - Uses default model `deepseek-v4-flash`.
  - Calls chat completions with JSON response, temperature 0, and `extra_body={"thinking": {"type": "disabled"}}`.

- Create `materials/postprocess/exercise_structure_repair.py`
  - Builds `previous_problem_absorption` candidates from `missing_problem_indices`.
  - Sends only the previous problem range plus a short next-problem reference to an optional client.
  - Validates LLM `start_line/end_line/confidence` before applying.
  - Returns final `problem_groups` and a serializable repair report.

- Modify `materials/service.py`
  - After `analyze_exercise_structure`, build the DeepSeek repair client.
  - Run repair for exercise materials.
  - Pass repaired groups into chunking.
  - Write `parsed/exercise_structure_repair.json`, `manifest.metadata["exercise_structure_repair"]`, and `parse_report.metrics["exercise_structure_repair"]`.

- Add tests:
  - `tests/test_exercise_structure_repair.py`
  - `tests/test_deepseek_structure_client.py`
  - Extend `tests/test_materials_mvp.py`

---

### Task 1: RED tests for local repair behavior

- [ ] Add tests proving a missing problem swallowed by the previous group is split only when a fake LLM returns a validated boundary.
- [ ] Add tests proving option lines and low-confidence judgements are rejected.
- [ ] Run `python -m unittest tests.test_exercise_structure_repair` and verify it fails because the module does not exist.

### Task 2: Implement repair module

- [ ] Create `exercise_structure_repair.py` with candidate generation, judgement normalization, validation, and group application.
- [ ] Run `python -m unittest tests.test_exercise_structure_repair` and verify it passes.

### Task 3: RED tests for DeepSeek client

- [ ] Add a fake OpenAI client test proving the request uses `deepseek-v4-flash`, JSON mode, temperature 0, and disabled thinking.
- [ ] Run `python -m unittest tests.test_deepseek_structure_client` and verify it fails because the module does not exist.

### Task 4: Implement DeepSeek client

- [ ] Create `deepseek_structure_client.py` using OpenAI-compatible calls and env fallback.
- [ ] Run `python -m unittest tests.test_deepseek_structure_client` and verify it passes.

### Task 5: Integrate ingestion service

- [ ] Add a service-level test that patches the DeepSeek repair client and verifies final chunks include the repaired problem id.
- [ ] Run the focused service test and verify it fails before integration.
- [ ] Modify `materials/service.py` to run repair after initial `exercise_structure` and before chunking.
- [ ] Run the focused service test and verify it passes.

### Task 6: Verification

- [ ] Run `python -m compileall materials scripts tests`.
- [ ] Run `python -m unittest tests.test_exercise_structure tests.test_exercise_structure_repair tests.test_deepseek_structure_client tests.test_materials_mvp`.
- [ ] Run AGENTS-required formula and runtime tests.
- [ ] Re-ingest `data/demo/test.md`, `data/demo/test.txt`, and the 2023 math2 PDF sample.
- [ ] Confirm repaired PDF chunks include problem 16 and 20 when DeepSeek is available; if the API is unavailable, confirm the repair report records a skipped/disabled client rather than silently claiming success.
