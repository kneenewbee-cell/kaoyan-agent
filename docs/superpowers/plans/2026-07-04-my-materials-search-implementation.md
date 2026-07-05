# My Materials Search UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved “我的资料搜索增强版” in the existing app: scoped search, fast/AI mode, result explanations, material health cards, and on-demand detail drawer.

**Architecture:** Keep the current single-page `web/index.html` + `web/app.js` + `web/styles.css` structure. Reuse the existing `/api/materials/search` and `/api/materials/{material_id}` endpoints, with one API adjustment so “全部我的资料” can omit `subject`.

**Tech Stack:** FastAPI, vanilla HTML/CSS/JS, Python `unittest`.

---

### Task 1: Add Failing Coverage For Search Scope And Frontend Shell

**Files:**
- Modify: `tests/test_materials_mvp.py`
- Create: `tests/test_user_materials_frontend.py`

- [ ] **Step 1: Add API test for all-material search**

Add a test that calls `/api/materials/search` without `subject` and asserts the service receives no subject filter:

```python
def test_api_search_can_omit_subject_for_all_my_materials(self) -> None:
    with patch("materials.api.search_user_materials_tool", return_value=[]) as search_tool:
        response = self.client.get(
            "/api/materials/search",
            params={"query": "方差公式", "mode": "hybrid"},
        )

    self.assertEqual(response.status_code, 200)
    self.assertNotIn("subject", search_tool.call_args.kwargs["filters"])
```

- [ ] **Step 2: Add frontend structure test**

Create `tests/test_user_materials_frontend.py`:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "web" / "app.js"
INDEX_HTML = ROOT / "web" / "index.html"
STYLES_CSS = ROOT / "web" / "styles.css"


class UserMaterialsFrontendTests(unittest.TestCase):
    def test_search_workbench_exposes_scope_mode_limit_and_drawer(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="materialsSearchScope"', html)
        self.assertIn('id="materialsSearchMode"', html)
        self.assertIn('id="materialsSearchLimit"', html)
        self.assertIn('id="materialDetailDrawer"', html)
        self.assertIn("function setMaterialSearchScope", source)
        self.assertIn("function openMaterialDetailDrawer", source)
        self.assertIn("function buildMaterialsSearchUrl", source)
        self.assertIn(".material-detail-drawer", styles)
        self.assertIn(".materials-search-controls", styles)

    def test_search_results_render_llm_reason_and_concept_coverage(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderConceptCoverage", source)
        self.assertIn("function resultDecisionLabel", source)
        self.assertIn("result.llm_rerank", source)
        self.assertIn("retrieval_plan", source)
        self.assertIn("强匹配", source)
        self.assertIn("相关参考", source)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests and verify they fail**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_api_search_can_omit_subject_for_all_my_materials tests.test_user_materials_frontend
```

Expected: FAIL because the API currently requires `subject` and the frontend controls do not exist.

### Task 2: Allow All-My-Materials Search Scope

**Files:**
- Modify: `materials/api.py`
- Test: `tests/test_materials_mvp.py`

- [ ] **Step 1: Make `subject` optional for search**

Change the `/api/materials/search` endpoint so `subject` is optional:

```python
subject: str | None = Query(None, pattern="^(math|politics|english|408|other)$"),
```

Keep the filter construction unchanged so `None` is omitted.

- [ ] **Step 2: Run API test**

Run:

```bash
python -m unittest tests.test_materials_mvp.MaterialsMvpTest.test_api_search_can_omit_subject_for_all_my_materials
```

Expected: PASS.

### Task 3: Implement Search Workbench Controls

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_user_materials_frontend.py`

- [ ] **Step 1: Add controls and drawer shell to HTML**

Add:

- `#materialsSearchScope`
- `#materialsSearchMode`
- `#materialsSearchLimit`
- `#materialsSearchSummary`
- `#materialDetailDrawer`
- `#materialDetailBackdrop`

Keep the existing upload and subject tabs.

- [ ] **Step 2: Wire search URL construction**

Implement `buildMaterialsSearchUrl(query)` in `web/app.js` so:

- scope `subject` sends `subject=<activeMaterialsSubject()>`
- scope `all` omits `subject`
- scope `material:<id>` sends both `subject=<item.subject>` and `material_id=<id>`
- mode sends `mode=<materialsSearchMode.value>`
- limit sends `top_k=<materialsSearchLimit.value>`

- [ ] **Step 3: Wire material card actions**

Add:

- `setMaterialSearchScope(item)` for “在本资料搜索”
- `openMaterialDetailDrawer(item)` for “详情”
- visual selected state on the active material card

- [ ] **Step 4: Run frontend structure test**

Run:

```bash
python -m unittest tests.test_user_materials_frontend
```

Expected: PASS after implementation.

### Task 4: Render Result Explanations And Coverage

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Test: `tests/test_user_materials_frontend.py`

- [ ] **Step 1: Add result helpers**

Add helpers:

- `resultDecisionLabel(result)`
- `resultDecisionClass(result)`
- `resultReason(result)`
- `renderConceptCoverage(results, query)`

- [ ] **Step 2: Update `renderSearchResults`**

Display:

- coverage chips for multi-term query
- strong matches before related references
- material name, heading path, chunk id, matched_by, score kind
- AI reason from `llm_rerank.reason`
- retrieval plan summary when present

- [ ] **Step 3: Run frontend structure test**

Run:

```bash
python -m unittest tests.test_user_materials_frontend
```

Expected: PASS.

### Task 5: Verification

**Files:**
- Verify only.

- [ ] **Step 1: Compile touched Python**

Run:

```bash
python -m compileall materials tests
```

Expected: exit code 0.

- [ ] **Step 2: Run targeted tests**

Run:

```bash
python -m unittest tests.test_materials_mvp tests.test_user_materials_frontend
```

Expected: PASS.

- [ ] **Step 3: Run prescribed materials smoke tests if time permits**

Run:

```bash
python -m unittest tests.test_materials_vector_index
```

Expected: PASS or report existing failures with evidence.
