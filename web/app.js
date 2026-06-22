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

const pages = {
  chat: document.querySelector("#chatPage"),
  materials: document.querySelector("#materialsPage"),
  plan: document.querySelector("#planPage"),
  school: document.querySelector("#schoolPage"),
};

const navButtons = [...document.querySelectorAll(".nav-button")];
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

const materialsUserIdInput = document.querySelector("#materialsUserId");
const materialsUploadForm = document.querySelector("#materialsUploadForm");
const materialsFileInput = document.querySelector("#materialsFileInput");
const materialsSubject = document.querySelector("#materialsSubject");
const materialsType = document.querySelector("#materialsType");
const materialsStatus = document.querySelector("#materialsStatus");
const materialsError = document.querySelector("#materialsError");
const materialsRefreshButton = document.querySelector("#materialsRefreshButton");
const materialsList = document.querySelector("#materialsList");
const materialsSearchForm = document.querySelector("#materialsSearchForm");
const materialsSearchInput = document.querySelector("#materialsSearchInput");
const materialsSearchResults = document.querySelector("#materialsSearchResults");

const welcomeMessage = "试试：`2021 年数学一第 9 题怎么做`\n\n也可以上传数学题图片后输入：`这道题怎么做`";
const deleteConfirmMessage = "确定要删除这份资料吗？此操作会删除该资料的原文件副本、解析结果、chunks 和索引。";

let selectedFiles = [];
let selectedImageUrls = [];
let currentMaterials = [];
let currentSearchResults = [];

function setActivePage(pageId) {
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.page === pageId);
  });
  Object.entries(pages).forEach(([key, element]) => {
    element.classList.toggle("active", key === pageId);
  });
  if (pageId === "materials") {
    void refreshMaterialsList();
  }
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => setActivePage(button.dataset.page));
});

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
    attachments.forEach((attachment) => {
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
    });
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
  items.forEach((item) => addMessage(item.role, item.content || ""));
}

function clearSelectedImageUrls() {
  selectedImageUrls.forEach((url) => URL.revokeObjectURL(url));
  selectedImageUrls = [];
}

function getSelectedAttachments(files) {
  clearSelectedImageUrls();
  return files.map((file) => {
    const url = URL.createObjectURL(file);
    selectedImageUrls.push(url);
    return { name: file.name, url };
  });
}

function syncImageInputFiles() {
  if (selectedFiles.length === 0) {
    imageInput.value = "";
    return;
  }
  try {
    const transfer = new DataTransfer();
    selectedFiles.forEach((file) => transfer.items.add(file));
    imageInput.files = transfer.files;
  } catch (error) {
    // Ignore browsers that disallow programmatic FileList assignment.
  }
}

function removeSelectedFile(index) {
  selectedFiles = selectedFiles.filter((_, fileIndex) => fileIndex !== index);
  syncImageInputFiles();
  renderImagePreview();
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
    removeButton.addEventListener("click", () => removeSelectedFile(index));

    item.appendChild(name);
    item.appendChild(removeButton);
    list.appendChild(item);
  });

  imagePreview.appendChild(list);
}

function activeSessionId() {
  return sessionInput.value.trim() || "default";
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  const payload = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(payload.detail || text || "Request failed");
  }
  return payload;
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

function appendAssistantChunk(bubble, chunk) {
  bubble.dataset.rawContent = (bubble.dataset.rawContent || "") + chunk;
  bubble.dataset.progressText = "";
  renderAssistantBubble(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function stepLabel(name) {
  const labels = {
    subject_classifier: "判断问题类型",
    llm_tool_selection: "选择工具",
    llm_final: "整理最终回答",
    "tool:solve_exam_question": "运行真题解题流程",
    "tool:solve_general_math": "解答普通数学题",
    "tool:ocr_math_image": "识别上传图片",
    "tool:explain_math_step": "解释局部步骤",
  };
  return labels[name] || name || "处理中";
}

function formatProgress(payload) {
  if (payload.label) return payload.label;
  const step = payload.step || {};
  const name = step.name || payload.name || "";
  const seconds = typeof step.latency_ms === "number"
    ? `，用时 ${(step.latency_ms / 1000).toFixed(2)} 秒`
    : "";
  return `${stepLabel(name)}完成${seconds}`;
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
  sessions.forEach((session) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = `session-item${session.id === current ? " active" : ""}`;

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
  });
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

function currentMaterialsUserId() {
  return (materialsUserIdInput.value || "").trim() || "tester";
}

function setBanner(element, message) {
  element.hidden = !message;
  element.textContent = message || "";
}

function clearMaterialsFeedback() {
  setBanner(materialsStatus, "");
  setBanner(materialsError, "");
}

const MATERIAL_SUBJECT_LABELS = {
  unknown: "未分类",
  math: "数学",
  politics: "政治",
  408: "计算机 408",
  cs408: "计算机 408",
  english: "英语",
  other: "其他",
};

const MATERIAL_TYPE_LABELS = {
  unknown: "未分类",
  lecture: "课程讲义",
  note: "学习笔记",
  exam: "试卷真题",
  wrong_book: "错题本",
  school_info: "院校信息",
  other: "其他",
};

const MATERIAL_STATUS_LABELS = {
  unknown: "未知",
  pending: "等待处理",
  processing: "处理中",
  ready: "已就绪",
  failed: "处理失败",
};

function materialLabel(labels, value) {
  return labels[value] || value || "未知";
}

function formatMaterialDate(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  const pad = (part) => String(part).padStart(2, "0");
  return `${date.getFullYear()}年${pad(date.getMonth() + 1)}月${pad(date.getDate())}日 ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function materialMetaLine(item) {
  return [
    `学科：${materialLabel(MATERIAL_SUBJECT_LABELS, item.subject)}`,
    `资料类型：${materialLabel(MATERIAL_TYPE_LABELS, item.material_type)}`,
    `状态：${materialLabel(MATERIAL_STATUS_LABELS, item.parse_status)}`,
    `分块数：${item.chunk_count ?? 0}`,
  ].join(" · ");
}

function renderMaterialsList(items) {
  currentMaterials = items;
  materialsList.innerHTML = "";
  if (!items || items.length === 0) {
    materialsList.className = "materials-list empty-state";
    materialsList.textContent = "还没有资料，先上传一份 `.md` 或 `.txt` 吧。";
    return;
  }

  materialsList.className = "materials-list";
  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "material-card";

    const header = document.createElement("div");
    header.className = "material-card-header";

    const titleBlock = document.createElement("div");
    const title = document.createElement("h4");
    title.textContent = item.original_filename || "未命名资料";
    const meta = document.createElement("p");
    meta.className = "material-meta";
    meta.textContent = materialMetaLine(item);
    titleBlock.appendChild(title);
    titleBlock.appendChild(meta);

    const actions = document.createElement("div");
    actions.className = "material-actions";
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "danger-button inline-danger";
    deleteButton.textContent = "删除";
    deleteButton.addEventListener("click", () => void deleteMaterial(item.material_id));
    actions.appendChild(deleteButton);

    header.appendChild(titleBlock);
    header.appendChild(actions);
    card.appendChild(header);

    const footer = document.createElement("p");
    footer.className = "material-footer";
    footer.textContent = `创建时间：${formatMaterialDate(item.created_at)} · 更新时间：${formatMaterialDate(item.updated_at)}${item.error ? ` · 错误：${item.error}` : ""}`;
    card.appendChild(footer);
    materialsList.appendChild(card);
  });
}

function renderSearchResults(results) {
  currentSearchResults = results;
  materialsSearchResults.innerHTML = "";
  if (!results || results.length === 0) {
    materialsSearchResults.className = "search-results empty-state";
    materialsSearchResults.textContent = "当前用户资料库中没有找到相关内容";
    return;
  }

  materialsSearchResults.className = "search-results";
  results.forEach((result) => {
    const card = document.createElement("article");
    card.className = "search-card";

    const title = document.createElement("h4");
    title.textContent = `${result.original_filename || "未命名资料"} · 相关度 ${Number(result.score).toFixed(4)}`;
    const meta = document.createElement("p");
    meta.className = "material-meta";
    meta.textContent = `分块：${result.chunk_id}`;
    const preview = document.createElement("pre");
    preview.className = "search-preview";
    preview.textContent = result.text_preview || result.text || "";
    const assets = document.createElement("p");
    assets.className = "material-path";
    assets.textContent = `asset_paths: ${Array.isArray(result.asset_paths) && result.asset_paths.length ? result.asset_paths.join(", ") : "(none)"}`;

    card.appendChild(title);
    card.appendChild(meta);
    card.appendChild(preview);
    card.appendChild(assets);
    materialsSearchResults.appendChild(card);
  });
}

async function refreshMaterialsList() {
  clearMaterialsFeedback();
  try {
    const userId = currentMaterialsUserId();
    const data = await fetchJson(`/api/materials/list?user_id=${encodeURIComponent(userId)}`);
    renderMaterialsList(data.items || []);
  } catch (error) {
    renderMaterialsList([]);
    setBanner(materialsError, `资料列表加载失败：${error.message}`);
  }
}

async function deleteMaterial(materialId) {
  if (!window.confirm(deleteConfirmMessage)) {
    return;
  }
  clearMaterialsFeedback();
  try {
    const userId = currentMaterialsUserId();
    await fetchJson(`/api/materials/${encodeURIComponent(materialId)}?user_id=${encodeURIComponent(userId)}`, {
      method: "DELETE",
    });
    setBanner(materialsStatus, "资料已删除");
    await refreshMaterialsList();
    currentSearchResults = currentSearchResults.filter((result) => result.material_id !== materialId);
    if (currentSearchResults.length === 0) {
      materialsSearchInput.value = "";
      renderSearchResults([]);
      materialsSearchResults.textContent = "输入关键词后开始搜索。";
    } else {
      renderSearchResults(currentSearchResults);
    }
  } catch (error) {
    setBanner(materialsError, `删除失败：${error.message}`);
  }
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
});

materialsUploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMaterialsFeedback();

  const file = materialsFileInput.files[0];
  if (!file) {
    setBanner(materialsError, "请选择要上传的 .md 或 .txt 文件");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", currentMaterialsUserId());
  formData.append("subject", materialsSubject.value);
  formData.append("material_type", materialsType.value);
  formData.append("use_llm_cleanup", "true");

  try {
    materialsUploadButton.disabled = true;
    materialsUploadButton.textContent = "AI 整理中...";
    setBanner(materialsStatus, "正在上传并调用 Qwen 生成清洗策略，请稍等。");
    const data = await fetchJson("/api/materials/upload", {
      method: "POST",
      body: formData,
    });
    const cleaning = data.metadata?.raw_markdown_cleaning;
    const source = cleaning?.strategy_source ? `，策略来源：${cleaning.strategy_source}` : "";
    setBanner(materialsStatus, `资料已入库，生成 ${data.chunk_count} 个 chunks${source}`);
    materialsUploadForm.reset();
    materialsUserIdInput.value = currentMaterialsUserId();
    materialsSubject.value = "unknown";
    materialsType.value = "unknown";
    await refreshMaterialsList();
  } catch (error) {
    setBanner(materialsError, `上传失败：${error.message}`);
  } finally {
    materialsUploadButton.disabled = false;
    materialsUploadButton.textContent = "上传资料";
  }
});

materialsRefreshButton.addEventListener("click", () => {
  void refreshMaterialsList();
});

materialsSearchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMaterialsFeedback();
  const query = materialsSearchInput.value.trim();
  if (!query) {
    setBanner(materialsError, "请输入搜索关键词");
    return;
  }

  try {
    const userId = currentMaterialsUserId();
    const data = await fetchJson(`/api/materials/search?user_id=${encodeURIComponent(userId)}&query=${encodeURIComponent(query)}`);
    renderSearchResults(data.results || []);
    if (!data.results || data.results.length === 0) {
      setBanner(materialsStatus, "当前用户资料库中没有找到相关内容");
    }
  } catch (error) {
    renderSearchResults([]);
    setBanner(materialsError, `搜索失败：${error.message}`);
  }
});

switchSession(activeSessionId()).catch(() => {
  renderMessages([]);
  loadSessions().catch(() => {});
});

renderSearchResults([]);
setActivePage("chat");
