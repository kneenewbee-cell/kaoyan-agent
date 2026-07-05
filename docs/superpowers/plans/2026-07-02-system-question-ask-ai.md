# System Question Ask AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the system question drawer's "Ask AI" placeholder into a working chat handoff.

**Architecture:** Keep this as a frontend bridge. The system question detail already contains question, answer, explanation, topics, and safe asset URLs; the frontend builds a teaching prompt, switches to the chat page, and submits through the existing `/api/chat/stream` path. Image assets referenced by the system question are fetched as blobs and attached like uploaded images when available.

**Tech Stack:** Plain JavaScript in `web/app.js`, existing FastAPI chat stream endpoint, static frontend tests in `tests/test_system_library_frontend.py`.

---

### Task 1: Add Failing Frontend Tests

**Files:**
- Modify: `tests/test_system_library_frontend.py`

- [ ] **Step 1: Write the failing test for the drawer action**

Add a test that requires:

```python
def test_system_question_ask_ai_hands_context_to_chat(self) -> None:
    source = APP_JS.read_text(encoding="utf-8")

    self.assertIn("function systemQuestionChatPrompt(question)", source)
    self.assertIn("function askAiForSystemQuestion(question)", source)
    self.assertIn("data-system-ask-ai", source)
    self.assertIn('setActivePage("chat")', source)
    self.assertIn("submitChatMessage(prompt, imageFiles)", source)
    self.assertIn("function systemQuestionImageUrls(question)", source)
    self.assertIn("function fetchSystemQuestionImageFiles(question)", source)
```

- [ ] **Step 2: Write the failing test for shared chat submission**

Add a test that requires:

```python
def test_chat_submit_uses_reusable_submit_function(self) -> None:
    source = APP_JS.read_text(encoding="utf-8")

    self.assertIn("async function submitChatMessage(message, files = [])", source)
    self.assertIn("await submitChatMessage(message, files)", source)
    self.assertIn('form.addEventListener("submit"', source)
```

- [ ] **Step 3: Verify RED**

Run:

```powershell
python -m unittest tests.test_system_library_frontend.SystemLibraryFrontendTests.test_system_question_ask_ai_hands_context_to_chat tests.test_system_library_frontend.SystemLibraryFrontendTests.test_chat_submit_uses_reusable_submit_function
```

Expected: FAIL because the helper functions and `data-system-ask-ai` do not exist yet.

### Task 2: Implement Chat Handoff

**Files:**
- Modify: `web/app.js`
- Modify: `web/index.html`

- [ ] **Step 1: Extract reusable chat submission**

Move the existing chat form body into:

```javascript
async function submitChatMessage(message, files = []) {
  if (!message) return;
  const attachments = getSelectedAttachments(files);
  addMessage("user", message, attachments);
  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "思考中";

  const formData = new FormData();
  formData.append("message", message);
  formData.append("session", activeSessionId());
  formData.append("output_format", "ui");
  formData.append("debug", debugInput.checked ? "true" : "false");
  files.forEach((file) => formData.append("images", file));

  try {
    const assistantBubble = addMessage("assistant", "");
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop() || "";
      events.forEach((entry) => {
        const lines = entry.split("\n");
        const eventLine = lines.find((line) => line.startsWith("event: "));
        const dataLine = lines.find((line) => line.startsWith("data: "));
        if (!dataLine) return;
        const eventName = eventLine ? eventLine.slice(7).trim() : "message";
        const payload = dataLine.slice(6);
        if (payload === "{}") return;
        if (eventName === "progress") {
          updateAssistantProgress(assistantBubble, JSON.parse(payload));
        } else {
          appendAssistantChunk(assistantBubble, JSON.parse(payload));
        }
      });
    }

    imageInput.value = "";
    selectedFiles = [];
    renderImagePreview();
    await loadSessions();
  } catch (error) {
    addMessage("assistant", `请求失败：${error.message}`);
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "发送";
  }
}
```

The form submit handler becomes:

```javascript
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const files = [...selectedFiles];
  let message = input.value.trim();
  if (!message && files.length > 0) {
    message = "这道题怎么做？";
  }
  await submitChatMessage(message, files);
});
```

- [ ] **Step 2: Add system question prompt helpers**

Add helpers near the system drawer functions:

```javascript
function clipSystemChatText(value, maxLength = 5000) {
  const text = String(value || "").trim();
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength).trim()}\n\n[内容过长，已截断]`;
}

function systemQuestionImageUrls(question) {
  const urls = new Set(Array.isArray(question?.asset_urls) ? question.asset_urls : []);
  const markdown = question?.question_markdown || "";
  for (const match of markdown.matchAll(/!\[[^\]\n]*]\((\/api\/materials\/system\/assets\/[^)\s]+)[^)]*\)/g)) {
    urls.add(match[1]);
  }
  return [...urls].filter((url) => url.startsWith("/api/materials/system/assets/")).slice(0, 8);
}

async function fetchSystemQuestionImageFiles(question) {
  const urls = systemQuestionImageUrls(question);
  const files = [];
  for (const [index, url] of urls.entries()) {
    const response = await fetch(url);
    if (!response.ok) continue;
    const blob = await response.blob();
    const extension = url.split(".").pop()?.split("?")[0] || "png";
    files.push(new File([blob], `system-question-${index + 1}.${extension}`, { type: blob.type || "image/png" }));
  }
  return files;
}

function systemQuestionChatPrompt(question) {
  const personal = systemUserState(question.question_id);
  const sections = [
    "请用考研辅导老师的方式讲解这道系统题。",
    "要求：先判断考点和解题入口，再分步骤推导，最后总结易错点；如果题目图片信息不足，请明确指出需要看哪张图。",
    `题目：${systemQuestionTitle(question)}`,
    `来源：${question.library_name || "系统题库"}`,
    `题型：${question.question_type_label || question.question_type || "题型未知"}`,
    `知识点：${(question.topics || []).join(" / ") || "未标注"}`,
    `题干：\n${clipSystemChatText(question.question_markdown || question.preview || "")}`,
  ];
  if (question.answer_markdown || question.answer) {
    sections.push(`系统答案：\n${clipSystemChatText(question.answer_markdown || question.answer, 2000)}`);
  }
  if (question.explanation_markdown || question.explanation) {
    sections.push(`系统解析：\n${clipSystemChatText(question.explanation_markdown || question.explanation, 3000)}`);
  }
  if (personal.personal_note) {
    sections.push(`我的备注：\n${clipSystemChatText(personal.personal_note, 1000)}`);
  }
  return sections.join("\n\n");
}
```

- [ ] **Step 3: Wire the drawer button**

Replace the Ask AI placeholder button with:

```javascript
<button type="button" class="small-button dark-button" data-system-ask-ai>问 AI 讲题</button>
```

Add:

```javascript
async function askAiForSystemQuestion(question) {
  const prompt = systemQuestionChatPrompt(question);
  const imageFiles = await fetchSystemQuestionImageFiles(question);
  setActivePage("chat");
  await submitChatMessage(prompt, imageFiles);
}
```

Bind it in `renderSystemQuestionDrawer`:

```javascript
systemQuestionDrawer.querySelector("[data-system-ask-ai]")?.addEventListener("click", () => {
  void askAiForSystemQuestion(question);
});
```

Keep the other placeholder buttons as placeholders.

- [ ] **Step 4: Update cache version**

Change the app script query string in `web/index.html` to:

```html
<script src="/static/app.js?v=20260702-system-ask-ai"></script>
```

### Task 3: Verify

**Files:**
- Test: `tests/test_system_library_frontend.py`
- Test: `web/app.js`

- [ ] **Step 1: Verify GREEN**

Run:

```powershell
python -m unittest tests.test_system_library_frontend
node --check web\app.js
```

Expected: frontend tests pass and JS syntax check exits 0.

- [ ] **Step 2: Run focused regressions**

Run:

```powershell
python -m unittest tests.test_system_library tests.test_system_library_frontend
python -m compileall materials scripts tests
```

Expected: all pass.

- [ ] **Step 3: Smoke test in browser**

Use the running local app:

1. Open `http://127.0.0.1:49212/`.
2. Go to `资料库 -> 系统资料`.
3. Open a system question detail.
4. Click `问 AI 讲题`.
5. Confirm the app switches to the chat page and a user message containing the system question appears.
