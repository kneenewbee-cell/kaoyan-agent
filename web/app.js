const md = window.markdownit({
  html: false,
  linkify: true,
  breaks: true,
}).use(window.texmath, {
  engine: window.katex,
  delimiters: "dollars",
  katexOptions: {
    throwOnError: false,
  },
});

const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const imageInput = document.querySelector("#imageInput");
const imagePreview = document.querySelector("#imagePreview");
const messages = document.querySelector("#messages");
const sendButton = document.querySelector("#sendButton");
const sessionInput = document.querySelector("#sessionInput");
const sessionList = document.querySelector("#sessionList");
const newSessionButton = document.querySelector("#newSessionButton");
const deleteSessionButton = document.querySelector("#deleteSessionButton");
const debugInput = document.querySelector("#debugInput");

const welcomeMessage = "试试：`2021 年数学一第 9 题怎么做`\n\n也可以上传数学题图片后输入：`这道题怎么做`";

let selectedFiles = [];
let selectedImageUrls = [];

function addMessage(role, content, attachments = []) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.dataset.rawContent = content || "";
  bubble.innerHTML = role === "assistant"
    ? md.render(normalizeMathMarkdown(content || ""))
    : escapeHtml(content || "").replace(/\n/g, "<br>");

  if (attachments.length > 0) {
    const attachmentList = document.createElement("div");
    attachmentList.className = "message-attachments";

    for (const attachment of attachments) {
      const item = document.createElement("figure");
      item.className = "message-attachment";

      const img = document.createElement("img");
      img.src = attachment.url;
      img.alt = attachment.name;

      const caption = document.createElement("figcaption");
      caption.textContent = attachment.name;

      item.appendChild(img);
      item.appendChild(caption);
      attachmentList.appendChild(item);
    }

    bubble.appendChild(attachmentList);
  }

  article.appendChild(bubble);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}

function renderMessages(items) {
  messages.innerHTML = "";
  if (!items || items.length === 0) {
    addMessage("assistant", welcomeMessage);
    return;
  }
  for (const item of items) {
    addMessage(item.role, item.content || "");
  }
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]);
}

function normalizeMathMarkdown(value) {
  return value
    .replace(/\\\[((?:.|\n)*?)\\\]/g, (_, body) => `$$\n${body.trim()}\n$$`)
    .replace(/\\\(((?:.|\n)*?)\\\)/g, (_, body) => `$${body.trim()}$`)
    .replace(/\$([^$\n]+?)\$/g, (_, body) => {
      const formula = body.trim();
      return formula ? `$${formula}$` : "$$";
    });
}

function clearSelectedImageUrls() {
  for (const url of selectedImageUrls) {
    URL.revokeObjectURL(url);
  }
  selectedImageUrls = [];
}

function getSelectedAttachments(files) {
  clearSelectedImageUrls();
  return files.map((file) => {
    const url = URL.createObjectURL(file);
    selectedImageUrls.push(url);
    return {
      name: file.name,
      url,
    };
  });
}

function renderImagePreview() {
  imagePreview.innerHTML = "";
  if (selectedFiles.length === 0) {
    imagePreview.hidden = true;
    return;
  }

  imagePreview.hidden = false;
  const title = document.createElement("div");
  title.className = "image-preview-title";
  title.textContent = `已选择 ${selectedFiles.length} 张图片，会和本次问题一起发送`;
  imagePreview.appendChild(title);

  const list = document.createElement("div");
  list.className = "image-preview-list";

  selectedFiles.forEach((file, index) => {
    const item = document.createElement("div");
    item.className = "image-preview-item";

    const name = document.createElement("span");
    name.className = "image-preview-name";
    name.textContent = file.name;

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "image-preview-remove";
    removeButton.textContent = "×";
    removeButton.setAttribute("aria-label", `移除 ${file.name}`);
    removeButton.title = "移除";
    removeButton.addEventListener("click", () => removeSelectedFile(index));

    item.appendChild(name);
    item.appendChild(removeButton);
    list.appendChild(item);
  });

  imagePreview.appendChild(list);
}

function syncImageInputFiles() {
  if (selectedFiles.length === 0) {
    imageInput.value = "";
    return;
  }
  try {
    const transfer = new DataTransfer();
    for (const file of selectedFiles) {
      transfer.items.add(file);
    }
    imageInput.files = transfer.files;
  } catch (error) {
    // Some browsers do not allow programmatic FileList updates; submission uses selectedFiles.
  }
}

function removeSelectedFile(index) {
  selectedFiles = selectedFiles.filter((_, fileIndex) => fileIndex !== index);
  syncImageInputFiles();
  renderImagePreview();
}

function activeSessionId() {
  return sessionInput.value.trim() || "default";
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

function appendAssistantChunk(bubble, chunk) {
  const next = (bubble.dataset.rawContent || "") + chunk;
  bubble.dataset.rawContent = next;
  bubble.dataset.progressText = "";
  renderAssistantBubble(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function renderAssistantBubble(bubble) {
  const content = bubble.dataset.rawContent || "";
  const progressText = bubble.dataset.progressText || "";
  let html = content ? md.render(normalizeMathMarkdown(content)) : "";
  if (progressText) {
    html += `<div class="progress-line">${escapeHtml(progressText)}</div>`;
  }
  bubble.innerHTML = html || '<div class="progress-line">处理中...</div>';
}

function stepLabel(name) {
  const labels = {
    subject_classifier: "判断问题类型",
    llm_tool_selection: "选择工具",
    llm_final: "整理最终回复",
    "tool:solve_exam_question": "运行真题解题流程",
    "tool:solve_general_math": "解答普通数学题",
    "tool:ocr_math_image": "识别上传图片",
    "tool:explain_math_step": "解释局部步骤",
    "tool:show_math_exam_question": "读取本地题面",
    "tool:show_math_exam_answer": "读取本地答案",
    "skill:solve_exam_question:search_math_exam": "查找本地真题",
    "skill:solve_exam_question:collect_images": "收集题库图片",
    "skill:solve_exam_question:ocr_math_image": "识别题图",
    "skill:solve_exam_question:solve_math_exam": "数学模型解题",
    "skill:solve_exam_question:judge_math_answer": "核对标准答案",
    "skill:solve_exam_question:fallback_explanation": "按标准答案纠偏",
  };
  return labels[name] || name || "处理步骤";
}

function formatProgress(payload) {
  if (payload.label) return payload.label;
  const step = payload.step || {};
  const name = step.name || payload.name || "";
  const seconds = typeof step.latency_ms === "number"
    ? `，用时 ${(step.latency_ms / 1000).toFixed(2)} 秒`
    : "";
  const extra = [];
  if (typeof step.total_tokens === "number") extra.push(`${step.total_tokens} tokens`);
  if (typeof step.ocr_images === "number") extra.push(`${step.ocr_images} 张图`);
  if (typeof step.image_count === "number") extra.push(`${step.image_count} 张图`);
  if (typeof step.attempt === "number") extra.push(`第 ${step.attempt} 次`);
  const suffix = extra.length ? `（${extra.join("，")}）` : "";
  return `${stepLabel(name)}完成${seconds}${suffix}`;
}

function updateAssistantProgress(bubble, payload) {
  if (bubble.dataset.rawContent) return;
  bubble.dataset.progressText = formatProgress(payload);
  renderAssistantBubble(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function renderSessionList(sessions) {
  sessionList.innerHTML = "";
  const current = activeSessionId();

  for (const session of sessions) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = `session-item${session.id === current ? " active" : ""}`;
    item.dataset.sessionId = session.id;

    const title = document.createElement("span");
    title.className = "session-title";
    title.textContent = session.id;

    const meta = document.createElement("span");
    meta.className = "session-meta";
    meta.textContent = `${session.turn_count || 0} 轮${session.title ? ` · ${session.title}` : ""}`;

    item.appendChild(title);
    item.appendChild(meta);
    item.addEventListener("click", () => switchSession(session.id));
    sessionList.appendChild(item);
  }
}

async function loadSessions() {
  const data = await fetchJson("/api/sessions");
  renderSessionList(data.sessions || []);
}

async function switchSession(sessionId) {
  sessionInput.value = sessionId || "default";
  const data = await fetchJson(`/api/sessions/${encodeURIComponent(activeSessionId())}`);
  renderMessages(data.messages || []);
  await loadSessions();
}

async function createSession() {
  const defaultName = `session_${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "")}`;
  const rawName = window.prompt("新会话名称", defaultName);
  const name = (rawName || "").trim();
  if (!name) return;

  const formData = new FormData();
  formData.append("session", name);
  const data = await fetchJson("/api/sessions", {
    method: "POST",
    body: formData,
  });
  await loadSessions();
  await switchSession(data.session.id);
}

async function deleteCurrentSession() {
  const sessionId = activeSessionId();
  const message = sessionId === "default"
    ? "default 会话不能删除，但可以清空记录。确定清空吗？"
    : `确定删除会话 ${sessionId} 吗？`;
  if (!window.confirm(message)) return;

  await fetchJson(`/api/sessions/${encodeURIComponent(sessionId)}`, { method: "DELETE" });
  await loadSessions();
  await switchSession("default");
}

imageInput.addEventListener("change", () => {
  selectedFiles = Array.from(imageInput.files);
  renderImagePreview();
});

newSessionButton.addEventListener("click", async () => {
  try {
    await createSession();
  } catch (error) {
    addMessage("assistant", `新建会话失败：${error.message}`);
  }
});

deleteSessionButton.addEventListener("click", async () => {
  try {
    await deleteCurrentSession();
  } catch (error) {
    addMessage("assistant", `删除会话失败：${error.message}`);
  }
});

sessionInput.addEventListener("change", async () => {
  try {
    await switchSession(activeSessionId());
  } catch (error) {
    addMessage("assistant", `切换会话失败：${error.message}`);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const files = [...selectedFiles];
  let message = input.value.trim();
  if (!message && files.length > 0) {
    message = "这道题怎么做？";
  }
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
  for (const file of files) {
    formData.append("images", file);
  }

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
      for (const event of events) {
        const lines = event.split("\n");
        const eventLine = lines.find((item) => item.startsWith("event: "));
        const dataLine = lines.find((item) => item.startsWith("data: "));
        if (!dataLine) continue;
        const eventName = eventLine ? eventLine.slice(7).trim() : "message";
        const payload = dataLine.slice(6);
        if (payload === "{}") continue;
        if (eventName === "progress") {
          updateAssistantProgress(assistantBubble, JSON.parse(payload));
        } else {
          appendAssistantChunk(assistantBubble, JSON.parse(payload));
        }
      }
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
});

switchSession(activeSessionId()).catch(() => {
  renderMessages([]);
  loadSessions().catch(() => {});
});
