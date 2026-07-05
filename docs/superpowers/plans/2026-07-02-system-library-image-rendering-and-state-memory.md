# System Library Image Rendering And State Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix system-library question reading so markdown images render in their original positions, with suitable preview/drawer sizing, and persist system-library filters/page/selected question across reloads.

**Architecture:** Keep the current public system library plus per-user state model. Backend detail responses should return question markdown with safe local image links rewritten to `/api/materials/system/assets/...`; frontend should render that markdown directly and use `asset_urls` only as a fallback. Frontend view persistence should extend the existing `localStorage` page/mode memory with a compact JSON object for system-library filters, page, and selected question id.

**Tech Stack:** Python `unittest`, FastAPI `TestClient`, `materials.system_library.SystemQuestionLibrary`, browser frontend in `web/app.js`, CSS in `web/styles.css`, static contract tests in `tests/test_system_library_frontend.py`.

---

## Constraints

- Do not change formal app behavior while recording this plan.
- Keep formal question list page size at the current `10`; do not change it to `5`.
- Do not move images to the end of a question by default.
- `asset_urls` is a safety/fallback list, not the primary display order.
- Preview modal shows only question markdown and original-position images.
- Drawer shows question markdown and original-position images, then answer/analysis folds and personal actions.
- Do not touch `qa/`.
- Do not commit automatically; the worktree may contain parallel changes from another window.

## File Structure

- Modify `materials/system_library.py`: preserve question-body image lines for detail responses and rewrite markdown image URLs safely.
- Modify `web/app.js`: render question markdown with embedded images in preview and drawer; persist system library view JSON.
- Modify `web/styles.css`: constrain question images differently in preview and drawer.
- Modify `tests/test_system_library.py`: backend tests for image-link preservation and URL rewriting.
- Modify `tests/test_system_library_frontend.py`: frontend contract tests for embedded-image rendering, no end-stacked asset strip, and system view persistence.

---

### Task 1: Preserve Markdown Image Positions In Question Detail

**Files:**
- Modify: `materials/system_library.py`
- Modify: `tests/test_system_library.py`

- [ ] **Step 1: Write the failing backend test**

Add this test to `SystemQuestionLibraryTest` in `tests/test_system_library.py`:

```python
    def test_detail_question_markdown_preserves_and_rewrites_image_positions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            images_dir = year_dir / "images"
            questions_dir = year_dir / "questions"
            (images_dir / "q001_option_a.png").write_bytes(b"option-a")
            (questions_dir / "q001.md").write_text(
                "\r\n".join(
                    [
                        "---",
                        "question_id: kaoyan_math1_2099_q001",
                        "year: 2099",
                        "---",
                        "",
                        "## 棰樼洰",
                        "",
                        "原函数图像：",
                        "",
                        "![主图](../images/q001.png)",
                        "",
                        "题干文字。",
                        "",
                        "A.",
                        "",
                        "![A选项](../images/q001_option_a.png)",
                        "",
                        "## 鏍囧噯绛旀",
                        "",
                        "B",
                        "",
                        "## 瑙ｆ瀽",
                        "",
                        "解析文字。",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            detail = library.get_question("kaoyan_math1_2099_q001")

            self.assertIn("原函数图像：", detail["question_markdown"])
            self.assertIn(
                "![主图](/api/materials/system/assets/math1/2099/images/q001.png)",
                detail["question_markdown"],
            )
            self.assertLess(
                detail["question_markdown"].index("![主图]"),
                detail["question_markdown"].index("题干文字。"),
            )
            self.assertIn(
                "![A选项](/api/materials/system/assets/math1/2099/images/q001_option_a.png)",
                detail["question_markdown"],
            )
            self.assertNotIn("../images/", detail["question_markdown"])
```

- [ ] **Step 2: Run the backend test to verify it fails**

Run:

```bash
python -m unittest tests.test_system_library.SystemQuestionLibraryTest.test_detail_question_markdown_preserves_and_rewrites_image_positions
```

Expected: `FAIL` because current `_question_body()` strips markdown image lines.

- [ ] **Step 3: Implement safe markdown image rewriting**

In `materials/system_library.py`, change detail question markdown construction so detail responses preserve image lines:

```python
            raw_question_markdown = sections.get("棰樼洰") or self._row_question_fallback(row)
            question_markdown = self._detail_question_body(raw_question_markdown, exam_type, year)
```

Add these helpers near `_question_body()`:

```python
    def _detail_question_body(self, markdown: str, exam_type: str, year: int) -> str:
        lines = []
        for line in markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            lines.append(self._rewrite_markdown_image_urls(stripped, exam_type, year))
        return "\n".join(lines).strip()

    def _rewrite_markdown_image_urls(self, markdown: str, exam_type: str, year: int) -> str:
        def replace(match: re.Match[str]) -> str:
            alt_text = match.group("alt")
            raw_url = match.group("url").strip()
            normalized = raw_url.replace("\\", "/")
            if normalized.startswith("../"):
                normalized = normalized[3:]
            if normalized.startswith("./"):
                normalized = normalized[2:]
            try:
                rewritten = self._asset_url(exam_type, year, normalized)
            except (FileNotFoundError, OSError, ValueError):
                return f"[图片不可用：{alt_text}]"
            return f"![{alt_text}]({rewritten})"

        return re.sub(
            r"!\[(?P<alt>[^\]]*)\]\((?P<url>[^)]+)\)",
            replace,
            markdown,
        )
```

Keep `_preview()` image stripping unchanged so list cards remain lightweight.

- [ ] **Step 4: Run backend tests**

Run:

```bash
python -m unittest tests.test_system_library
```

Expected: all tests pass, including existing asset endpoint tests.

---

### Task 2: Render Embedded Markdown Images Instead Of End-Stacked Asset Strip

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write frontend contract tests**

Add these tests to `SystemLibraryFrontendTests` in `tests/test_system_library_frontend.py`:

```python
    def test_preview_and_drawer_render_markdown_images_in_place(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderSystemQuestionMarkdown(question)", source)
        self.assertIn("renderSystemQuestionMarkdown(question)", source)
        self.assertIn("const markdownHasImages", source)
        self.assertIn("renderSystemAssetFallback(question)", source)
        self.assertNotIn("${renderSystemAssetStrip(question.asset_urls)}", source)

    def test_system_question_images_have_preview_and_drawer_size_rules(self) -> None:
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn(".system-markdown img", styles)
        self.assertIn(".system-preview-dialog-body .system-markdown img", styles)
        self.assertIn("#systemQuestionDrawer .system-markdown img", styles)
        self.assertIn("max-width: 100%", styles)
        self.assertIn("object-fit: contain", styles)
```

- [ ] **Step 2: Run frontend tests to verify they fail**

Run:

```bash
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_preview_and_drawer_render_markdown_images_in_place tests.test_system_library_frontend.SystemLibraryFrontendTests.test_system_question_images_have_preview_and_drawer_size_rules
```

Expected: `FAIL` because the current drawer and preview append `renderSystemAssetStrip(question.asset_urls)` after markdown.

- [ ] **Step 3: Add markdown/fallback rendering helpers**

In `web/app.js`, replace the current direct pattern:

```js
<div class="system-markdown">${renderSystemMarkdown(questionMarkdown)}</div>
${renderSystemAssetStrip(question.asset_urls)}
```

with:

```js
${renderSystemQuestionMarkdown(question)}
```

Add helpers near `renderSystemAssetStrip()`:

```js
function systemMarkdownHasImages(markdown = "") {
  return /!\[[^\]]*]\([^)]+\)/.test(markdown || "");
}

function renderSystemAssetFallback(question) {
  const markdown = question?.question_markdown || question?.preview || "";
  const markdownHasImages = systemMarkdownHasImages(markdown);
  if (markdownHasImages) {
    return "";
  }
  return renderSystemAssetStrip(question?.asset_urls || []);
}

function renderSystemQuestionMarkdown(question) {
  const markdown = question?.question_markdown || question?.preview || "暂无题干";
  return `
    <div class="system-markdown">${renderSystemMarkdown(markdown)}</div>
    ${renderSystemAssetFallback(question)}
  `;
}
```

Use `renderSystemQuestionMarkdown(question)` in both `renderSystemQuestionDrawer(question)` and `openSystemQuestionPreview(questionId)`.

- [ ] **Step 4: Keep preview limited to question content**

In `openSystemQuestionPreview(questionId)`, keep the successful body content to title/meta plus `renderSystemQuestionMarkdown(question)`. Do not include answer or explanation in the preview modal.

The success body should follow this shape:

```js
body.innerHTML = `
  <p class="system-preview-meta">${escapeHtml(systemQuestionTitle(question))}</p>
  ${renderSystemQuestionMarkdown(question)}
`;
```

- [ ] **Step 5: Add image sizing CSS**

In `web/styles.css`, add or adjust these rules:

```css
.system-markdown img {
  display: block;
  max-width: 100%;
  height: auto;
  object-fit: contain;
  margin: 10px 0;
  border: 1px solid #e3e8ef;
  border-radius: 8px;
  background: #fff;
}

.system-preview-dialog-body .system-markdown img {
  max-height: min(56vh, 560px);
}

#systemQuestionDrawer .system-markdown img {
  max-height: 360px;
}
```

These rules keep multi-image option questions readable in preview and prevent large scans from dominating the drawer.

- [ ] **Step 6: Run frontend checks**

Run:

```bash
python -m unittest tests.test_system_library_frontend
node --check web/app.js
```

Expected: tests pass and `node --check` exits with code `0`.

---

### Task 3: Persist System Library Filters, Page, And Selected Question

**Files:**
- Modify: `web/app.js`
- Modify: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write frontend state persistence contract test**

Add this test to `SystemLibraryFrontendTests` in `tests/test_system_library_frontend.py`:

```python
    def test_system_library_filters_page_and_selection_survive_reload(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("const SYSTEM_LIBRARY_VIEW_STORAGE_KEY", source)
        self.assertIn("function restoreSystemLibraryViewFromStorage()", source)
        self.assertIn("function rememberSystemLibraryView()", source)
        self.assertIn("function applyRestoredSystemLibraryView()", source)
        self.assertIn("subject: systemState.subject", source)
        self.assertIn("contentType: systemState.contentType", source)
        self.assertIn("examType: systemState.examType", source)
        self.assertIn("page: systemState.page", source)
        self.assertIn("selectedQuestionId: systemState.selectedQuestionId", source)
        self.assertIn("rememberSystemLibraryView();", source)
        self.assertIn("applyRestoredSystemLibraryView();", source)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_system_library_filters_page_and_selection_survive_reload
```

Expected: `FAIL` because only active page and materials mode currently persist.

- [ ] **Step 3: Add storage key and restore/save functions**

In `web/app.js`, add:

```js
const SYSTEM_LIBRARY_VIEW_STORAGE_KEY = "kaoyan_agent_system_library_view";
```

Add helpers near existing localStorage helpers:

```js
function restoreSystemLibraryViewFromStorage() {
  try {
    const raw = window.localStorage.getItem(SYSTEM_LIBRARY_VIEW_STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function rememberSystemLibraryView() {
  try {
    const payload = {
      subject: systemState.subject,
      contentType: systemState.contentType,
      examType: systemState.examType,
      year: systemState.year,
      questionType: systemState.questionType,
      topic: systemState.topic,
      status: systemState.status,
      query: systemState.query,
      page: systemState.page,
      selectedQuestionId: systemState.selectedQuestionId,
    };
    window.localStorage.setItem(SYSTEM_LIBRARY_VIEW_STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // The system library should remain usable when localStorage is unavailable.
  }
}

function applyRestoredSystemLibraryView() {
  const restored = restoreSystemLibraryViewFromStorage();
  systemState.subject = restored.subject || systemState.subject;
  systemState.contentType = restored.contentType || systemState.contentType;
  systemState.examType = restored.examType || systemState.examType;
  systemState.year = restored.year || "";
  systemState.questionType = restored.questionType || "";
  systemState.topic = restored.topic || "";
  systemState.status = restored.status || "";
  systemState.query = restored.query || "";
  systemState.page = Math.max(1, Number(restored.page || 1));
  systemState.selectedQuestionId = restored.selectedQuestionId || "";

  systemLibraryNameFilter.value = systemState.examType;
  systemYearFilter.value = systemState.year;
  systemQuestionTypeFilter.value = systemState.questionType;
  systemStatusFilter.value = systemState.status;
  systemSearchInput.value = systemState.query;
}
```

- [ ] **Step 4: Save state from existing flow points**

Call `rememberSystemLibraryView();` after existing state updates:

```js
function syncSystemFiltersFromInputs() {
  systemState.examType = systemLibraryNameFilter?.value || "math1";
  systemState.year = systemYearFilter?.value || "";
  systemState.questionType = systemQuestionTypeFilter?.value || "";
  systemState.topic = (systemTopicFilter?.value || "").trim();
  systemState.status = systemStatusFilter?.value || "";
  systemState.query = (systemSearchInput?.value || "").trim();
  rememberSystemLibraryView();
}
```

In pagination button handlers, after changing `systemState.page`, call `rememberSystemLibraryView();` before `loadSystemQuestions()`.

In `openSystemQuestionDrawer(questionId)`, after setting `systemState.selectedQuestionId = questionId`, call `rememberSystemLibraryView();`.

In `closeSystemQuestionDrawer()`, after clearing `selectedQuestionId`, call `rememberSystemLibraryView();`.

- [ ] **Step 5: Restore tabs and selected drawer safely**

During startup, after `restoreMaterialsUserIdFromStorage();` and before first system library load, call:

```js
applyRestoredSystemLibraryView();
```

After `loadSystemQuestions()` receives items, restore drawer only if the selected question is on the current page:

```js
const selectedStillVisible = systemState.items.some((item) => item.question_id === systemState.selectedQuestionId);
if (selectedStillVisible) {
  void openSystemQuestionDrawer(systemState.selectedQuestionId);
} else if (systemState.selectedQuestionId) {
  systemState.selectedQuestionId = "";
  systemState.selectedQuestion = null;
  rememberSystemLibraryView();
  renderSystemDrawerEmpty();
}
```

Use a guard such as `options.restoreSelection` or a local boolean to avoid recursively reopening the drawer after every manual load.

- [ ] **Step 6: Run frontend tests**

Run:

```bash
python -m unittest tests.test_system_library_frontend
node --check web/app.js
```

Expected: tests pass and JavaScript syntax check exits with code `0`.

---

### Task 4: Verify The Combined User Flow

**Files:**
- No code files beyond Tasks 1-3.

- [ ] **Step 1: Run focused automated checks**

Run:

```bash
python -m unittest tests.test_system_library tests.test_system_library_frontend
node --check web/app.js
```

Expected: all tests pass.

- [ ] **Step 2: Run broader project checks**

Run:

```bash
python -m compileall materials scripts tests
python -m unittest tests.test_user_system_state tests.test_system_library tests.test_system_library_frontend
```

Expected: all tests pass.

- [ ] **Step 3: Manual browser verification**

Open:

```text
http://127.0.0.1:49212/
```

Verify:

- `2009 数一 Q3` or an equivalent multi-image question displays the main graph before the question text and A/B/C/D images next to their option labels.
- Preview modal displays question markdown and images only.
- Drawer displays question markdown and images, then answer and analysis folds.
- Drawer images fit within the drawer width and do not overflow horizontally.
- Preview images fit within the modal and do not make the close button unreachable.
- System library remains at 10 questions per page.
- After setting filters/page/selected question and refreshing, the page returns to the same system library view.
- If the selected question is not on the restored page or filter result, drawer shows the empty state.

## Self-Review

- Spec coverage: image original-position rendering is covered by Tasks 1-2; preview/drawer image sizing by Task 2; filter/page/selection reload persistence by Task 3; verification by Task 4.
- Placeholder scan: no deferred blanks are present; each task names files, tests, commands, and expected outcomes.
- Type consistency: storage names, state fields, and helper names are consistent across tests and implementation steps.
