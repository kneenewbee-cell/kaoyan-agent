# System Library MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable system library vertical slice inside the existing `资料库` page.

**Architecture:** Add a small read-only backend service for local math question cards, expose it through FastAPI, and render it in the existing vanilla JS frontend. Keep user materials unchanged and keep system-library personal state in browser memory for the first slice.

**Tech Stack:** Python, FastAPI, unittest, vanilla HTML/CSS/JavaScript, existing local `data/raw/math/exam_papers/math1` question cards.

---

## File Structure

- Create `materials/system_library.py`
  - Reads existing `data/raw/math/exam_papers/math1/{year}/questions.jsonl`.
  - Loads question markdown cards for detail display.
  - Normalizes labels, image URLs, answer, explanation, topics, type, year, and pagination.
  - Does not write system data.

- Modify `materials/api.py`
  - Adds read-only routes under `/api/materials/system/questions`.
  - Adds a safe static asset route under `/api/materials/system/assets/{exam_type}/{year}/{asset_path}`.

- Modify `web/index.html`
  - Rename left navigation entry to `资料库`.
  - Add `我的资料` / `系统资料` switch inside the materials page.
  - Add system library DOM containers without removing existing user-materials DOM.

- Modify `web/app.js`
  - Add system library state, API calls, filters, pagination, drawer open/close, answer/analysis folds, and in-memory personal state.
  - Keep existing upload/list/search behavior active when `我的资料` is selected.

- Modify `web/styles.css`
  - Add fixed-shell styles for system library.
  - Add scroll-contained main list and right drawer.
  - Keep existing user material styles intact.

- Create `tests/test_system_library.py`
  - Tests backend service and API behavior using a temporary question-card fixture.

## Task 1: Backend System Library Service

**Files:**
- Create: `materials/system_library.py`
- Test: `tests/test_system_library.py`

- [ ] **Step 1: Write the failing service test**

Add this test to `tests/test_system_library.py`:

```python
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from materials.system_library import SystemQuestionLibrary


class SystemQuestionLibraryTest(unittest.TestCase):
    def make_fixture(self, root: Path) -> Path:
        base = root / "math" / "exam_papers" / "math1" / "2099"
        (base / "questions").mkdir(parents=True)
        (base / "images").mkdir()
        (base / "images" / "q001.png").write_bytes(b"image")
        row = {
            "question_id": "kaoyan_math1_2099_q001",
            "exam_id": "kaoyan_math1_2099",
            "exam_type": "math1",
            "year": 2099,
            "question_number": 1,
            "question_type": "single_choice",
            "module": "高数",
            "topics": ["极限", "导数"],
            "difficulty": "unknown",
            "card_path": "questions/q001.md",
            "assets": ["images/q001.png"],
            "answer": "A",
            "explanation": "由定义可得。",
        }
        (base / "questions.jsonl").write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
        (base / "questions" / "q001.md").write_text(
            "\n".join([
                "---",
                "question_id: kaoyan_math1_2099_q001",
                "---",
                "",
                "# 2099 数学一第 1 题",
                "",
                "## 题目",
                "",
                "设函数 `f(x)` 连续，则（ ）。",
                "",
                "## 标准答案",
                "",
                "A",
                "",
                "## 解析",
                "",
                "由定义可得。",
            ]),
            encoding="utf-8",
        )
        return root

    def test_list_questions_filters_and_paginates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            library = SystemQuestionLibrary(raw_root=self.make_fixture(Path(tmp)))
            result = library.list_questions(subject="math", exam_type="math1", query="连续", page=1, page_size=10)

        self.assertEqual(result["total"], 1)
        self.assertEqual(result["page"], 1)
        self.assertEqual(result["page_size"], 10)
        self.assertEqual(result["items"][0]["question_id"], "kaoyan_math1_2099_q001")
        self.assertEqual(result["items"][0]["library_name"], "数一历年真题")
        self.assertEqual(result["items"][0]["preview"], "设函数 `f(x)` 连续，则（ ）。")
        self.assertEqual(result["items"][0]["asset_urls"], ["/api/materials/system/assets/math1/2099/images/q001.png"])

    def test_get_question_returns_detail_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            library = SystemQuestionLibrary(raw_root=self.make_fixture(Path(tmp)))
            detail = library.get_question("kaoyan_math1_2099_q001")

        self.assertEqual(detail["answer"], "A")
        self.assertEqual(detail["explanation"], "由定义可得。")
        self.assertEqual(detail["question_markdown"], "设函数 `f(x)` 连续，则（ ）。")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: fail with `ModuleNotFoundError: No module named 'materials.system_library'`.

- [ ] **Step 3: Implement `materials/system_library.py`**

Create a focused service with:

```python
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_ROOT = ROOT / "data" / "raw"

QUESTION_TYPE_LABELS = {
    "single_choice": "选择题",
    "fill_blank": "填空题",
    "solution": "解答题",
}

EXAM_LABELS = {
    "math1": "数一",
}

LIBRARY_NAMES = {
    "math1": "数一历年真题",
}


@dataclass(frozen=True)
class QuestionLocation:
    exam_type: str
    year: int
    row: dict[str, Any]
    year_dir: Path


class SystemQuestionLibrary:
    def __init__(self, raw_root: Path | None = None) -> None:
        self.raw_root = raw_root or DEFAULT_RAW_ROOT

    def list_questions(
        self,
        *,
        subject: str = "math",
        exam_type: str = "math1",
        library_name: str | None = None,
        year: int | None = None,
        question_type: str | None = None,
        topic: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        rows = [
            self._summary(location)
            for location in self._iter_locations(subject=subject, exam_type=exam_type, year=year)
        ]
        if library_name:
            rows = [row for row in rows if row["library_name"] == library_name]
        if question_type:
            rows = [row for row in rows if row["question_type"] == question_type]
        if topic:
            rows = [row for row in rows if topic in row["topics"]]
        if query:
            needle = query.lower()
            rows = [
                row for row in rows
                if needle in " ".join([
                    row["preview"],
                    row["library_name"],
                    row["question_type_label"],
                    " ".join(row["topics"]),
                    str(row["year"]),
                ]).lower()
            ]
        rows.sort(key=lambda item: (item["year"], item["question_number"]), reverse=True)
        total = len(rows)
        safe_page_size = max(1, min(page_size, 50))
        safe_page = max(1, page)
        start = (safe_page - 1) * safe_page_size
        end = start + safe_page_size
        return {
            "ok": True,
            "subject": subject,
            "exam_type": exam_type,
            "total": total,
            "page": safe_page,
            "page_size": safe_page_size,
            "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            "items": rows[start:end],
        }

    def get_question(self, question_id: str) -> dict[str, Any]:
        for location in self._iter_locations(subject="math", exam_type="math1"):
            if location.row.get("question_id") == question_id:
                summary = self._summary(location)
                sections = self._read_card_sections(location)
                return {
                    **summary,
                    "question_markdown": sections.get("题目", summary["preview"]),
                    "answer": sections.get("标准答案", location.row.get("answer") or ""),
                    "explanation": sections.get("解析", location.row.get("explanation") or ""),
                }
        raise FileNotFoundError(question_id)

    def asset_path(self, exam_type: str, year: int, asset_path: str) -> Path:
        safe_parts = [part for part in Path(asset_path).parts if part not in {"", ".", ".."}]
        if not safe_parts:
            raise ValueError("Invalid asset path")
        path = self.raw_root / "math" / "exam_papers" / exam_type / str(year) / Path(*safe_parts)
        resolved = path.resolve()
        year_dir = (self.raw_root / "math" / "exam_papers" / exam_type / str(year)).resolve()
        if year_dir not in resolved.parents and resolved != year_dir:
            raise ValueError("Asset path escapes question directory")
        if not resolved.exists() or not resolved.is_file():
            raise FileNotFoundError(asset_path)
        return resolved

    def _iter_locations(self, *, subject: str, exam_type: str, year: int | None = None) -> list[QuestionLocation]:
        if subject != "math" or exam_type != "math1":
            return []
        base = self.raw_root / "math" / "exam_papers" / exam_type
        if not base.exists():
            return []
        year_dirs = [base / str(year)] if year else [path for path in base.iterdir() if path.is_dir() and path.name.isdigit()]
        locations: list[QuestionLocation] = []
        for year_dir in year_dirs:
            questions_path = year_dir / "questions.jsonl"
            if not questions_path.exists():
                continue
            for line in questions_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                locations.append(QuestionLocation(exam_type=exam_type, year=int(year_dir.name), row=row, year_dir=year_dir))
        return locations

    def _summary(self, location: QuestionLocation) -> dict[str, Any]:
        row = location.row
        question_markdown = self._read_card_sections(location).get("题目", "")
        preview = self._preview(question_markdown)
        assets = [str(asset) for asset in row.get("assets") or []]
        return {
            "question_id": row.get("question_id"),
            "exam_id": row.get("exam_id"),
            "subject": "math",
            "exam_type": location.exam_type,
            "exam_label": EXAM_LABELS.get(location.exam_type, location.exam_type),
            "library_name": LIBRARY_NAMES.get(location.exam_type, location.exam_type),
            "year": int(row.get("year") or location.year),
            "question_number": int(row.get("question_number") or 0),
            "question_type": row.get("question_type") or "unknown",
            "question_type_label": QUESTION_TYPE_LABELS.get(row.get("question_type"), row.get("question_type") or "未知"),
            "score": row.get("score"),
            "module": row.get("module") or "",
            "topics": list(row.get("topics") or []),
            "difficulty": row.get("difficulty") or "unknown",
            "review_status": row.get("review_status") or "unknown",
            "answer_status": row.get("answer_status") or "unknown",
            "explanation_status": row.get("explanation_status") or "unknown",
            "preview": preview,
            "assets": assets,
            "asset_urls": [f"/api/materials/system/assets/{location.exam_type}/{location.year}/{asset}" for asset in assets],
        }

    def _read_card_sections(self, location: QuestionLocation) -> dict[str, str]:
        card_path = location.year_dir / str(location.row.get("card_path") or "")
        if not card_path.exists():
            return {}
        text = card_path.read_text(encoding="utf-8")
        text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
        sections: dict[str, list[str]] = {}
        current: str | None = None
        for line in text.splitlines():
            if line.startswith("## "):
                current = line[3:].strip()
                sections.setdefault(current, [])
                continue
            if current:
                sections[current].append(line)
        return {key: "\n".join(value).strip() for key, value in sections.items()}

    def _preview(self, markdown: str) -> str:
        lines = []
        for line in markdown.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("!"):
                continue
            lines.append(stripped)
        return " ".join(lines)[:180]
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: `OK`.

## Task 2: Backend API Routes

**Files:**
- Modify: `materials/api.py`
- Test: `tests/test_system_library.py`

- [ ] **Step 1: Write failing API tests**

Append tests that create a FastAPI app with the materials router and call:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from materials.api import router as materials_router


class SystemQuestionApiTest(unittest.TestCase):
    def test_api_lists_system_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = SystemQuestionLibraryTest().make_fixture(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                response = TestClient(app).get("/api/materials/system/questions", params={"subject": "math", "exam_type": "math1", "query": "连续"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["question_id"], "kaoyan_math1_2099_q001")

    def test_api_returns_question_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = SystemQuestionLibraryTest().make_fixture(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                response = TestClient(app).get("/api/materials/system/questions/kaoyan_math1_2099_q001")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["question_markdown"], "设函数 `f(x)` 连续，则（ ）。")
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: route tests fail with `404`.

- [ ] **Step 3: Add API routes**

Modify `materials/api.py`:

```python
from fastapi.responses import FileResponse
from .system_library import SystemQuestionLibrary
```

Add routes before `@router.delete("/{material_id}")`:

```python
@router.get("/system/questions")
async def list_system_questions(
    subject: str = Query("math", pattern="^(math|politics|english|408|other)$"),
    exam_type: str = Query("math1"),
    library_name: str | None = Query(None),
    year: int | None = Query(None),
    question_type: str | None = Query(None),
    topic: str | None = Query(None),
    query: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
) -> dict[str, Any]:
    return SystemQuestionLibrary().list_questions(
        subject=subject,
        exam_type=exam_type,
        library_name=library_name,
        year=year,
        question_type=question_type,
        topic=topic,
        query=query,
        page=page,
        page_size=page_size,
    )


@router.get("/system/questions/{question_id}")
async def get_system_question(question_id: str) -> dict[str, Any]:
    try:
        return SystemQuestionLibrary().get_question(question_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="System question not found") from exc


@router.get("/system/assets/{exam_type}/{year}/{asset_path:path}")
async def get_system_question_asset(exam_type: str, year: int, asset_path: str) -> FileResponse:
    try:
        return FileResponse(SystemQuestionLibrary().asset_path(exam_type, year, asset_path))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="System asset not found") from exc
```

- [ ] **Step 4: Run tests to verify pass**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: `OK`.

## Task 3: Frontend System Library Skeleton

**Files:**
- Modify: `web/index.html`
- Modify: `web/styles.css`
- Modify: `web/app.js`

- [ ] **Step 1: Add static DOM containers**

Change the sidebar nav text from `我的资料库` to `资料库`.

Inside `materialsPage`, add:

```html
<div class="materials-mode-tabs" role="tablist" aria-label="资料库类型">
  <button type="button" class="materials-mode-tab active" data-materials-mode="user">我的资料</button>
  <button type="button" class="materials-mode-tab" data-materials-mode="system">系统资料</button>
</div>
```

Wrap the existing user-material upload/list/search sections in:

```html
<div id="userMaterialsView" class="materials-mode-view active"></div>
```

Add:

```html
<div id="systemMaterialsView" class="materials-mode-view">
  <div class="system-library-shell">
    ...
  </div>
</div>
```

Use the v8 mockup structure for the initial shell.

- [ ] **Step 2: Add CSS for fixed shell and drawer**

Add classes:

```css
.materials-mode-tabs {}
.materials-mode-tab {}
.materials-mode-view {}
.materials-mode-view.active {}
.system-library-shell {}
.system-library-main {}
.system-question-list {}
.system-question-drawer {}
```

Keep existing user material classes unchanged.

- [ ] **Step 3: Add JS mode switching**

In `web/app.js`, add:

```javascript
const materialsModeTabs = [...document.querySelectorAll("[data-materials-mode]")];
const userMaterialsView = document.querySelector("#userMaterialsView");
const systemMaterialsView = document.querySelector("#systemMaterialsView");

let activeMaterialsMode = "user";

function setMaterialsMode(mode) {
  activeMaterialsMode = mode === "system" ? "system" : "user";
  materialsModeTabs.forEach((button) => {
    const active = button.dataset.materialsMode === activeMaterialsMode;
    button.classList.toggle("active", active);
  });
  userMaterialsView.classList.toggle("active", activeMaterialsMode === "user");
  systemMaterialsView.classList.toggle("active", activeMaterialsMode === "system");
  if (activeMaterialsMode === "system") {
    void loadSystemQuestions();
  } else {
    void refreshMaterialsList();
  }
}
```

## Task 4: Frontend Data Loading, Filters, Pagination, Drawer

**Files:**
- Modify: `web/app.js`
- Modify: `web/index.html`
- Modify: `web/styles.css`

- [ ] **Step 1: Add system library state**

Add:

```javascript
const systemState = {
  subject: "math",
  contentType: "questions",
  examType: "math1",
  page: 1,
  pageSize: 10,
  query: "",
  year: "",
  topic: "",
  questionType: "",
  items: [],
  selectedQuestion: null,
  userState: new Map(),
};
```

- [ ] **Step 2: Implement `loadSystemQuestions`**

Fetch `/api/materials/system/questions` with current filters and render cards.

- [ ] **Step 3: Implement `openSystemQuestionDrawer`**

Fetch `/api/materials/system/questions/{question_id}` and render drawer with:

- mastery status
- personal marks
- question markdown
- assets
- `details` for answer and explanation
- note
- actions

- [ ] **Step 4: Implement personal-state toggles in memory**

Store state by `question_id`:

```javascript
{
  mastery_status: "learning",
  is_favorite: true,
  in_wrong_book: false,
  personal_note: ""
}
```

## Task 5: Verification

**Files:**
- No new files.

- [ ] **Step 1: Run focused backend tests**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: `OK`.

- [ ] **Step 2: Run existing materials MVP tests**

Run:

```bash
python -m unittest tests.test_materials_mvp
```

Expected: existing tests pass or report unrelated existing failures explicitly.

- [ ] **Step 3: Run compile check**

Run:

```bash
python -m compileall materials scripts tests
```

Expected: no compile errors.

- [ ] **Step 4: Run the local web server**

Run:

```bash
python scripts/web_server.py
```

Open the served URL. Verify:

- `资料库` left nav opens the materials page.
- `我的资料` still shows existing upload/list/search.
- `系统资料` shows math question cards.
- Filters and pagination update cards.
- `查看` opens right drawer.
- `答案` and `解析` folds expand in drawer.
- Status/favorite/wrong-book/note update in UI without changing system content.

## Self-Review

- Spec coverage: the plan covers backend read-only system questions, frontend mode switch, filters, pagination, right drawer, answer/explanation folds, and in-memory user state.
- Scope check: persistence for user state, knowledge-point pages, database migration, and AI question answering are intentionally out of scope.
- Placeholder scan: no implementation step uses `TBD` or `TODO`; task steps contain specific paths and commands.
