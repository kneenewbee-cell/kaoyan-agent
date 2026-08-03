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
const systemMarkdownRenderCache = new Map();
const SYSTEM_MARKDOWN_RENDER_CACHE_LIMIT = 240;

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
const materialsUploadButton = document.querySelector("#materialsUploadButton");
const materialsFileInput = document.querySelector("#materialsFileInput");
const materialsSubject = document.querySelector("#materialsSubject");
const materialsType = document.querySelector("#materialsType");
const materialsStatus = document.querySelector("#materialsStatus");
const materialsError = document.querySelector("#materialsError");
const materialsUploadProgress = document.querySelector("#materialsUploadProgress");
const materialsUploadStage = document.querySelector("#materialsUploadStage");
const materialsUploadPercent = document.querySelector("#materialsUploadPercent");
const materialsUploadBar = document.querySelector("#materialsUploadBar");
const materialsUploadMessage = document.querySelector("#materialsUploadMessage");
const materialsRefreshButton = document.querySelector("#materialsRefreshButton");
const materialsList = document.querySelector("#materialsList");
const materialsSearchForm = document.querySelector("#materialsSearchForm");
const materialsSearchInput = document.querySelector("#materialsSearchInput");
const materialsSearchScope = document.querySelector("#materialsSearchScope");
const materialsSearchMode = document.querySelector("#materialsSearchMode");
const materialsSearchLimit = document.querySelector("#materialsSearchLimit");
const materialsSearchModeStatus = document.querySelector("#materialsSearchModeStatus");
const materialsSearchSummary = document.querySelector("#materialsSearchSummary");
const materialsSearchResults = document.querySelector("#materialsSearchResults");
const materialDetailDrawer = document.querySelector("#materialDetailDrawer");
const materialDetailBackdrop = document.querySelector("#materialDetailBackdrop");
const materialDetailCloseButton = document.querySelector("#materialDetailCloseButton");
const materialDetailTitle = document.querySelector("#materialDetailTitle");
const materialDetailMeta = document.querySelector("#materialDetailMeta");
const materialDetailBody = document.querySelector("#materialDetailBody");
const materialsLibraryTabs = [...document.querySelectorAll("[data-materials-subject]")];
const materialsModeTabs = [...document.querySelectorAll("[data-materials-mode]")];
const userMaterialsView = document.querySelector("#userMaterialsView");
const systemMaterialsView = document.querySelector("#systemMaterialsView");
const systemSubjectTabs = [...document.querySelectorAll("[data-system-subject]")];
const systemContentTabs = [...document.querySelectorAll("[data-system-content]")];
const systemQuestionList = document.querySelector("#systemQuestionList");
const systemPagination = document.querySelector("#systemPagination");
const systemQuestionDrawer = document.querySelector("#systemQuestionDrawer");
const systemQuestionTutorPanel = document.querySelector("#systemQuestionTutorPanel");
const systemLibraryNameFilter = document.querySelector("#systemLibraryNameFilter");
const systemYearFilter = document.querySelector("#systemYearFilter");
const systemQuestionTypeFilter = document.querySelector("#systemQuestionTypeFilter");
const systemTopicFilter = document.querySelector("#systemTopicFilter");
const systemStatusFilter = document.querySelector("#systemStatusFilter");
const systemSearchInput = document.querySelector("#systemSearchInput");
const systemStatusSummary = document.querySelector("#systemStatusSummary");
const systemSaveStatus = document.querySelector("#systemSaveStatus");
const reviewTasksRefreshButton = document.querySelector("#reviewTasksRefreshButton");
const reviewAiPlanButton = document.querySelector("#reviewAiPlanButton");
const reviewTasksStatus = document.querySelector("#reviewTasksStatus");
const reviewLearningInsights = document.querySelector("#reviewLearningInsights");
const reviewTaskList = document.querySelector("#reviewTaskList");
const reviewSubjectFilter = document.querySelector("#reviewSubjectFilter");
const reviewTargetTypeFilter = document.querySelector("#reviewTargetTypeFilter");
const reviewDateGroupFilter = document.querySelector("#reviewDateGroupFilter");
const reviewKeywordFilter = document.querySelector("#reviewKeywordFilter");

const welcomeMessage = "试试：`2021 年数学一第 9 题怎么做`\n\n也可以上传数学题图片后输入：`这道题怎么做`";
const deleteConfirmMessage = "确定要删除这份资料吗？此操作会删除该资料的原文件副本、解析结果、chunks 和索引。";

let selectedFiles = [];
let selectedImageUrls = [];
let currentMaterials = [];
let currentSearchResults = [];
let activeMaterialSearchId = "";

const systemState = {
  userId: "",
  subject: "math",
  contentType: "questions",
  examType: "",
  page: 1,
  pageSize: 10,
  query: "",
  year: "",
  topic: "",
  questionType: "",
  status: "",
  items: [],
  total: 0,
  totalPages: 1,
  selectedQuestionId: "",
  selectedQuestion: null,
  loading: false,
  error: "",
  summaryLoading: false,
  summaryError: "",
  stateSummary: {},
  userState: new Map(),
  selectedIds: new Set(),
};

const SYSTEM_EXAM_TYPE_LABELS = {
  math1: "数学一",
  math2: "数学二",
  math3: "数学三",
};

const systemTutor = {
  active: false,
  questionId: "",
  question: null,
  messages: [],
  history: [],
  streaming: false,
  selectedText: "",
  contextCollapsed: false,
};

const reviewTasksState = {
  items: [],
  learningInsights: null,
  insightsLoading: false,
  insightsError: "",
  loading: false,
  error: "",
  filters: {
    subject: "",
    targetType: "",
    dateGroup: "",
    keyword: "",
  },
};

const REVIEW_TASK_SECTION_DEFAULT_COLLAPSED = Object.freeze({
  overdue: false,
  today: false,
  future: false,
  completed: true,
  cancelled: true,
});

const reviewTaskSectionCollapsed = {
  ...REVIEW_TASK_SECTION_DEFAULT_COLLAPSED,
};

let systemQuestionsRequestSeq = 0;
let systemStatusSummaryRequestSeq = 0;
let systemNoteSaveTimer = 0;
let systemSaveStatusTimer = 0;
let systemTutorMessageSeq = 0;

const MATERIALS_MODE_USER = "user";
const MATERIALS_MODE_SYSTEM = "system";
const DEFAULT_MATERIALS_SUBJECT = "math";
const ACTIVE_PAGE_STORAGE_KEY = "kaoyan_agent_active_page";
const MATERIALS_MODE_STORAGE_KEY = "kaoyan_agent_materials_mode";
const MATERIALS_USER_ID_STORAGE_KEY = "kaoyan_agent_materials_user_id";
const DEFAULT_AI_REVIEW_PLAN_MODEL = "deepseek-v4-flash";
const AI_REVIEW_PLAN_MODES = [
  {
    value: "balanced",
    label: "均衡推进",
    hint: "错题、薄弱点、到期任务和少量新题一起排，适合日常稳定推进。",
    candidateTitle: "均衡候选池",
    candidateCountLabel: "综合候选 Top 40",
  },
  {
    value: "weak",
    label: "补弱优先",
    hint: "围绕薄弱知识点、相关错题和待核对题安排，新题只作为少量补充。",
    candidateTitle: "薄弱候选池",
    candidateCountLabel: "薄弱 Top 30",
  },
  {
    value: "wrong",
    label: "错题回收",
    hint: "只处理已经暴露过问题的错题、待核对题和到期错题任务，不混入未开始题。",
    candidateTitle: "错题回收候选池",
    candidateCountLabel: "错题 Top 40",
  },
  {
    value: "startup",
    label: "新题启动",
    hint: "用于历史数据少或想开启新范围。这里不叫薄弱 Top-K，而叫起步候选。",
    candidateTitle: "起步候选池",
    candidateCountLabel: "起步候选 Top 30",
  },
  {
    value: "sprint",
    label: "考前冲刺",
    hint: "优先处理到期、错题、薄弱和收藏未掌握，限制新题比例，避免任务发散。",
    candidateTitle: "冲刺候选池",
    candidateCountLabel: "冲刺 Top 45",
  },
];
const AI_REVIEW_PLAN_INCLUDE_OPTIONS = [
  { value: "due_tasks", label: "到期/逾期任务", modes: ["balanced", "weak", "wrong", "sprint"], defaults: ["balanced", "wrong", "sprint"] },
  { value: "wrong_questions", label: "高频错题", modes: ["balanced", "weak", "wrong", "sprint"], defaults: ["balanced", "weak", "wrong", "sprint"] },
  { value: "pending_review", label: "待核对题", modes: ["balanced", "weak", "wrong", "sprint"], defaults: ["balanced", "weak", "wrong"] },
  { value: "weak_topics", label: "薄弱知识点", modes: ["balanced", "weak", "wrong", "startup", "sprint"], defaults: ["balanced", "weak", "sprint"] },
  { value: "unstarted", label: "未开始/未掌握题", modes: ["balanced", "weak", "startup", "sprint"], defaults: ["startup"] },
  { value: "draft_attempts", label: "未提交练习", modes: ["balanced", "weak", "sprint"], defaults: ["balanced"] },
  { value: "favorite_unmastered", label: "收藏但未掌握", modes: ["balanced", "weak", "startup", "sprint"], defaults: ["sprint"] },
];
const SYSTEM_MASTERY_VALUES = ["not_started", "learning", "mastered"];
const SYSTEM_DEFAULT_PERSONAL_STATE = Object.freeze({
  mastery_status: "not_started",
  is_favorite: false,
  in_wrong_book: false,
  personal_note: "",
  last_practiced_at: null,
  review_due_at: null,
});

let activeMaterialsMode = restoreMaterialsModeFromStorage();

function restoreMaterialsUserIdFromStorage() {
  if (!materialsUserIdInput) return;
  try {
    const savedUserId = window.localStorage.getItem(MATERIALS_USER_ID_STORAGE_KEY);
    if (savedUserId && savedUserId.trim()) {
      materialsUserIdInput.value = savedUserId.trim();
    }
  } catch {
    // localStorage may be unavailable in private or embedded browser contexts.
  }
}

function rememberMaterialsUserId() {
  if (!materialsUserIdInput) return;
  try {
    window.localStorage.setItem(MATERIALS_USER_ID_STORAGE_KEY, currentMaterialsUserId());
  } catch {
    // Keeping the current page working matters more than persisting this hint.
  }
}

function restoreActivePageFromStorage() {
  try {
    const savedPage = window.localStorage.getItem(ACTIVE_PAGE_STORAGE_KEY);
    if (savedPage && pages[savedPage]) {
      return savedPage;
    }
  } catch {
    // Falling back to chat keeps startup resilient when storage is unavailable.
  }
  return "chat";
}

function rememberActivePage(pageId) {
  if (!pages[pageId]) return;
  try {
    window.localStorage.setItem(ACTIVE_PAGE_STORAGE_KEY, pageId);
  } catch {
    // Page switching should still work if storage is blocked.
  }
}

function restoreMaterialsModeFromStorage() {
  try {
    const savedMode = window.localStorage.getItem(MATERIALS_MODE_STORAGE_KEY);
    if (savedMode === MATERIALS_MODE_SYSTEM) {
      return MATERIALS_MODE_SYSTEM;
    }
  } catch {
    // The user can still switch modes manually if persistence is unavailable.
  }
  return MATERIALS_MODE_USER;
}

function rememberMaterialsMode(mode) {
  const nextMode = mode === MATERIALS_MODE_SYSTEM ? MATERIALS_MODE_SYSTEM : MATERIALS_MODE_USER;
  try {
    window.localStorage.setItem(MATERIALS_MODE_STORAGE_KEY, nextMode);
  } catch {
    // Keep the in-page switch responsive even if persistence is unavailable.
  }
}

function syncSystemUserScope() {
  const currentUserId = currentMaterialsUserId();
  if (systemState.userId === currentUserId) {
    return false;
  }
  systemState.userId = currentUserId;
  systemState.page = 1;
  systemState.items = [];
  systemState.total = 0;
  systemState.totalPages = 1;
  systemState.selectedQuestionId = "";
  systemState.selectedQuestion = null;
  systemState.error = "";
  systemState.summaryError = "";
  systemState.stateSummary = {};
  window.clearTimeout(systemNoteSaveTimer);
  systemNoteSaveTimer = 0;
  systemState.userState.clear();
  systemState.selectedIds.clear();
  return true;
}

function activeMaterialsSubject() {
  return (
    materialsLibraryTabs.find((button) => button.classList.contains("active"))?.dataset.materialsSubject
    || materialsSubject.value
    || DEFAULT_MATERIALS_SUBJECT
  );
}

function setActiveMaterialsSubject(subject, options = {}) {
  const normalized = subject || DEFAULT_MATERIALS_SUBJECT;
  materialsLibraryTabs.forEach((button) => {
    const active = button.dataset.materialsSubject === normalized;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  if (!options.keepSearch) {
    activeMaterialSearchId = "";
    if (materialsSearchScope) {
      materialsSearchScope.value = "subject";
    }
    materialsSearchInput.value = "";
    renderSearchResults([]);
    materialsSearchResults.textContent = "输入关键词后开始搜索。";
    if (materialsSearchSummary) {
      materialsSearchSummary.hidden = true;
      materialsSearchSummary.textContent = "";
    }
  }
  if (!options.skipRefresh) {
    void refreshMaterialsList();
  }
}

function systemUserState(questionId) {
  if (!systemState.userState.has(questionId)) {
    systemState.userState.set(questionId, { ...SYSTEM_DEFAULT_PERSONAL_STATE });
  }
  return systemState.userState.get(questionId);
}

function normalizeSystemQuestionPersonalState(personalState = {}) {
  const source = personalState && typeof personalState === "object" ? personalState : {};
  const masteryStatus = SYSTEM_MASTERY_VALUES.includes(source.mastery_status)
    ? source.mastery_status
    : SYSTEM_DEFAULT_PERSONAL_STATE.mastery_status;
  return {
    ...SYSTEM_DEFAULT_PERSONAL_STATE,
    mastery_status: masteryStatus,
    is_favorite: Boolean(source.is_favorite),
    in_wrong_book: Boolean(source.in_wrong_book),
    personal_note: typeof source.personal_note === "string" ? source.personal_note : "",
    last_practiced_at: source.last_practiced_at || null,
    review_due_at: source.review_due_at || null,
  };
}

function hydrateSystemQuestionPersonalState(questionId, personalState) {
  const normalized = normalizeSystemQuestionPersonalState(personalState);
  if (questionId) {
    systemState.userState.set(questionId, normalized);
  }
  return normalized;
}

function updateSystemQuestionPersonalState(questionId, patch) {
  const current = systemUserState(questionId);
  const next = normalizeSystemQuestionPersonalState({ ...current, ...patch });
  systemState.userState.set(questionId, next);
  return next;
}

const SYSTEM_MASTERY_LABELS = {
  not_started: "未开始",
  learning: "学习中",
  mastered: "已掌握",
};
const SYSTEM_STATE_SUMMARY_DEFAULT = Object.freeze({
  all: 0,
  not_started: 0,
  learning: 0,
  mastered: 0,
  favorite: 0,
  wrong_book: 0,
  noted: 0,
});
const SYSTEM_STATUS_CHIPS = [
  { value: "", key: "all", label: "全部" },
  { value: "not_started", key: "not_started", label: "未开始" },
  { value: "learning", key: "learning", label: "学习中" },
  { value: "mastered", key: "mastered", label: "已掌握" },
  { value: "favorite", key: "favorite", label: "已收藏" },
  { value: "wrong_book", key: "wrong_book", label: "错题" },
  { value: "noted", key: "noted", label: "有备注" },
];

function systemQuestionTitle(item) {
  const year = item?.year || "";
  const exam = item?.exam_type_label || "数一";
  const number = item?.question_number ? `Q${item.question_number}` : "";
  return [year, exam, number].filter(Boolean).join(" ");
}

function systemExamTypeLabel(examType) {
  return SYSTEM_EXAM_TYPE_LABELS[examType] || "全部数学";
}

function systemStateMatchesStatus(questionId) {
  const status = systemState.status;
  if (!status) return true;
  const personal = systemUserState(questionId);
  if (["not_started", "learning", "mastered"].includes(status)) {
    return personal.mastery_status === status;
  }
  if (status === "favorite") return personal.is_favorite;
  if (status === "wrong_book") return personal.in_wrong_book;
  if (status === "noted") return Boolean((personal.personal_note || "").trim());
  return true;
}

function systemQuestionRequestParams(options = {}) {
  const params = new URLSearchParams({
    subject: systemState.subject,
    exam_type: systemState.examType,
  });
  params.set("user_id", currentMaterialsUserId());
  if (options.includePage !== false) {
    params.set("page", String(systemState.page));
    params.set("page_size", String(systemState.pageSize));
  }
  if (systemState.query) params.set("query", systemState.query);
  if (systemState.year) params.set("year", systemState.year);
  if (systemState.questionType) params.set("question_type", systemState.questionType);
  if (systemState.topic) params.set("topic", systemState.topic);
  if (options.includeStatus) {
    if (systemState.status) params.set("user_status", systemState.status);
  }
  return params;
}

function renderSystemStatusSummary() {
  if (!systemStatusSummary) return;
  if (systemState.subject !== "math" || systemState.contentType !== "questions") {
    systemStatusSummary.innerHTML = "";
    return;
  }
  const summary = { ...SYSTEM_STATE_SUMMARY_DEFAULT, ...(systemState.stateSummary || {}) };
  systemStatusSummary.innerHTML = "";
  SYSTEM_STATUS_CHIPS.forEach((chip) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `system-status-chip${systemState.status === chip.value ? " active" : ""}`;
    button.setAttribute("data-system-status-chip", chip.value);
    button.setAttribute("aria-pressed", systemState.status === chip.value ? "true" : "false");
    const count = Number(summary[chip.key] || 0);
    button.innerHTML = `<span>${escapeHtml(chip.label)}</span><strong>${count}</strong>`;
    button.addEventListener("click", () => {
      systemState.status = chip.value;
      if (systemStatusFilter) {
        systemStatusFilter.value = chip.value;
      }
      systemState.page = 1;
      void loadSystemQuestions();
    });
    systemStatusSummary.appendChild(button);
  });
}

async function loadSystemStatusSummary() {
  syncSystemUserScope();
  syncSystemFiltersFromInputs();
  if (systemState.subject !== "math" || systemState.contentType !== "questions") {
    systemState.stateSummary = {};
    renderSystemStatusSummary();
    return;
  }
  const requestId = ++systemStatusSummaryRequestSeq;
  systemState.summaryLoading = true;
  systemState.summaryError = "";
  renderSystemStatusSummary();
  try {
    const params = systemQuestionRequestParams({ includePage: false, includeStatus: false });
    const data = await fetchJson(`/api/materials/system/questions/state-summary?${params.toString()}`);
    if (requestId !== systemStatusSummaryRequestSeq) return;
    systemState.stateSummary = { ...SYSTEM_STATE_SUMMARY_DEFAULT, ...(data.state_summary || {}) };
  } catch (error) {
    if (requestId !== systemStatusSummaryRequestSeq) return;
    systemState.stateSummary = {};
    systemState.summaryError = error.message;
  } finally {
    if (requestId !== systemStatusSummaryRequestSeq) return;
    systemState.summaryLoading = false;
    renderSystemStatusSummary();
  }
}

function setSystemSaveStatus(status, message = "") {
  if (!systemSaveStatus) return;
  window.clearTimeout(systemSaveStatusTimer);
  if (!status) {
    systemSaveStatus.hidden = true;
    systemSaveStatus.textContent = "";
    systemSaveStatus.className = "system-save-status";
    return;
  }
  if (status === "saving") {
    systemSaveStatus.className = "system-save-status saving";
  } else if (status === "saved") {
    systemSaveStatus.className = "system-save-status saved";
  } else {
    systemSaveStatus.className = "system-save-status error";
  }
  systemSaveStatus.hidden = false;
  systemSaveStatus.textContent = message;
  if (status === "saved") {
    systemSaveStatusTimer = window.setTimeout(() => setSystemSaveStatus(""), 1400);
  }
}

function filteredSystemItems() {
  return systemState.items.filter((item) => systemStateMatchesStatus(item.question_id));
}

function renderSystemStateSurfaces(questionId, options = {}) {
  renderSystemQuestionList();
  if (options.renderDrawer === false) {
    return;
  }
  if (systemState.selectedQuestionId === questionId && systemState.selectedQuestion) {
    renderSystemQuestionDrawer(systemState.selectedQuestion);
  }
}

function handleSystemQuestionStateSaveError(questionId, error, previousState) {
  if (previousState) {
    hydrateSystemQuestionPersonalState(questionId, previousState);
  }
  renderSystemStateSurfaces(questionId);
  setSystemSaveStatus("error", `个人状态保存失败：${error.message}`);
  window.alert(`个人状态保存失败：${error.message}`);
}

function applyAndSaveSystemQuestionState(questionId, patch, options = {}) {
  if (syncSystemUserScope()) {
    renderSystemQuestionList();
    void loadSystemQuestions();
    return;
  }
  const userId = systemState.userId || currentMaterialsUserId();
  const previousState = { ...systemUserState(questionId) };
  updateSystemQuestionPersonalState(questionId, patch);
  if (options.render !== false) {
    renderSystemStateSurfaces(questionId);
  }
  void saveSystemQuestionState(questionId, patch, { ...options, userId })
    .catch((error) => {
      if (userId !== currentMaterialsUserId()) return;
      handleSystemQuestionStateSaveError(questionId, error, previousState);
    });
}

function systemQuestionDetailUrl(questionId) {
  return `/api/materials/system/questions/${encodeURIComponent(questionId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`;
}

async function askAiForSystemQuestion(question) {
  await startSystemQuestionTutor(question);
}

function systemQuestionTutorUrl(questionId) {
  return `/api/qa/system-questions/${encodeURIComponent(questionId)}/tutor/stream?user_id=${encodeURIComponent(currentMaterialsUserId())}`;
}

function renderSystemTutorMessageContent(content) {
  const text = content || "";
  if (!text.trim()) return '<div class="progress-line">正在讲解...</div>';
  return md.render(normalizeMathMarkdown(text));
}

function renderSystemTutorMessages() {
  if (!systemQuestionTutorPanel || !systemTutor.active) return;
  const list = systemQuestionTutorPanel.querySelector("#systemTutorMessages");
  if (!list) return;
  list.innerHTML = systemTutor.messages.map((message) => {
    const roleClass = message.role === "user" ? "user" : "assistant system-tutor-assistant";
    const content = message.role === "user"
      ? escapeHtml(message.content)
      : renderSystemTutorMessageContent(message.content);
    return `
      <article class="system-tutor-message ${roleClass}" data-system-tutor-message-id="${message.id}">
        <div class="system-tutor-bubble">${content}</div>
      </article>
    `;
  }).join("");
  list.scrollTop = list.scrollHeight;
  updateSystemTutorSelectionActions();
}

function renderSystemTutorPanel() {
  if (!systemQuestionTutorPanel) return;
  if (!systemTutor.active || !systemTutor.question) {
    systemQuestionTutorPanel.hidden = true;
    systemQuestionTutorPanel.innerHTML = "";
    return;
  }

  systemQuestionTutorPanel.hidden = false;
  systemQuestionTutorPanel.innerHTML = `
    <header class="system-tutor-header">
      <div>
        <p class="eyebrow">Temporary Tutor</p>
        <h3>${escapeHtml(systemQuestionTitle(systemTutor.question))} · AI 讲题</h3>
      </div>
      <span class="status-pill note">不进入会话列表</span>
    </header>
    <div class="system-tutor-context-banner">已带入题目上下文：题干、答案、解析、题图、个人备注。</div>
    <div id="systemTutorMessages" class="system-tutor-messages" aria-live="polite"></div>
    <div class="system-tutor-selection-actions" hidden>
      <button type="button" class="small-button dark-button" data-system-tutor-add-note>将选中文本加入备注</button>
      <button type="button" class="small-button" data-system-tutor-followup>追问这一步</button>
    </div>
    <form id="systemTutorForm" class="system-tutor-form">
      <textarea id="systemTutorInput" rows="3" placeholder="继续追问这道题，例如：为什么这里可以这样变形？"></textarea>
      <div class="system-tutor-form-footer">
        <span>上下文：${escapeHtml(systemQuestionTitle(systemTutor.question))} · 退出后清空</span>
        <button type="submit" class="small-button dark-button">发送</button>
      </div>
    </form>
  `;

  systemQuestionTutorPanel.querySelector("#systemTutorForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const inputNode = systemQuestionTutorPanel.querySelector("#systemTutorInput");
    const message = inputNode?.value.trim() || "";
    if (inputNode) inputNode.value = "";
    void sendSystemTutorMessage(message);
  });
  systemQuestionTutorPanel.querySelector("[data-system-tutor-add-note]")?.addEventListener("click", appendSelectedSystemTutorTextToNote);
  systemQuestionTutorPanel.querySelector("[data-system-tutor-followup]")?.addEventListener("click", followUpSelectedSystemTutorText);
  renderSystemTutorMessages();
}

async function startSystemQuestionTutor(question) {
  if (!question?.question_id) return;
  systemTutor.active = true;
  systemTutor.questionId = question.question_id;
  systemTutor.question = question;
  systemTutor.messages = [];
  systemTutor.history = [];
  systemTutor.streaming = false;
  systemTutor.selectedText = "";
  systemTutor.contextCollapsed = false;
  systemMaterialsView?.classList.add("system-tutor-active");
  systemMaterialsView?.classList.remove("system-tutor-context-collapsed");
  renderSystemTutorPanel();
  renderSystemQuestionDrawer(question);
  await sendSystemTutorMessage("请讲解这道题。", { showUser: false });
}

function exitSystemQuestionTutor() {
  systemTutor.active = false;
  systemTutor.questionId = "";
  systemTutor.question = null;
  systemTutor.messages = [];
  systemTutor.history = [];
  systemTutor.streaming = false;
  systemTutor.selectedText = "";
  systemTutor.contextCollapsed = false;
  systemMaterialsView?.classList.remove("system-tutor-active", "system-tutor-context-collapsed");
  renderSystemTutorPanel();
  if (systemState.selectedQuestion) {
    renderSystemQuestionDrawer(systemState.selectedQuestion);
  } else {
    renderSystemDrawerEmpty();
  }
}

function toggleSystemTutorContext() {
  if (!systemTutor.active) return;
  systemTutor.contextCollapsed = !systemTutor.contextCollapsed;
  systemMaterialsView?.classList.toggle("system-tutor-context-collapsed", systemTutor.contextCollapsed);
  if (systemState.selectedQuestion) {
    renderSystemQuestionDrawer(systemState.selectedQuestion);
  }
}

function appendSystemTutorAssistantChunk(messageId, chunk) {
  const message = systemTutor.messages.find((item) => item.id === messageId);
  if (!message) return;
  message.content += chunk;
  renderSystemTutorMessages();
}

async function sendSystemTutorMessage(message, options = {}) {
  const text = String(message || "").trim();
  if (!text || !systemTutor.active || !systemTutor.questionId || systemTutor.streaming) return;

  if (options.showUser !== false) {
    systemTutor.messages.push({ id: `user-${++systemTutorMessageSeq}`, role: "user", content: text });
  }
  const assistantMessage = { id: `assistant-${++systemTutorMessageSeq}`, role: "assistant", content: "" };
  systemTutor.messages.push(assistantMessage);
  systemTutor.streaming = true;
  renderSystemTutorMessages();

  const formData = new FormData();
  formData.append("message", text);
  formData.append("history", JSON.stringify(systemTutor.history));

  try {
    const response = await fetch(systemQuestionTutorUrl(systemTutor.questionId), {
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
        if (eventName === "error") {
          throw new Error(JSON.parse(payload));
        }
        appendSystemTutorAssistantChunk(assistantMessage.id, JSON.parse(payload));
      });
    }

    if (assistantMessage.content.trim()) {
      systemTutor.history.push({ role: "user", content: text });
      systemTutor.history.push({ role: "assistant", content: assistantMessage.content });
      systemTutor.history = systemTutor.history.slice(-8);
    }
  } catch (error) {
    appendSystemTutorAssistantChunk(assistantMessage.id, `\n\n请求失败：${error.message}`);
  } finally {
    systemTutor.streaming = false;
    renderSystemTutorMessages();
  }
}

function updateSystemTutorSelectionActions() {
  if (!systemQuestionTutorPanel || !systemTutor.active) return;
  const actions = systemQuestionTutorPanel.querySelector(".system-tutor-selection-actions");
  if (!actions) return;
  const selection = window.getSelection();
  const text = selection?.toString().trim() || "";
  const anchor = selection?.anchorNode?.nodeType === Node.TEXT_NODE
    ? selection.anchorNode.parentElement
    : selection?.anchorNode;
  const insideAssistant = Boolean(anchor?.closest?.(".system-tutor-assistant"));
  systemTutor.selectedText = text && insideAssistant ? text : "";
  const visible = Boolean(systemTutor.selectedText);
  actions.hidden = !visible;
  actions.classList.toggle("visible", visible);
}

function appendSelectedSystemTutorTextToNote() {
  const text = systemTutor.selectedText.trim();
  if (!text || !systemTutor.questionId) return;
  const current = systemUserState(systemTutor.questionId).personal_note || "";
  const addition = `来自 AI：${text}`;
  const note = current.trim() ? `${current.trim()}\n\n${addition}` : addition;
  updateSystemQuestionPersonalState(systemTutor.questionId, { personal_note: note });
  renderSystemQuestionList();
  if (systemState.selectedQuestion) {
    renderSystemQuestionDrawer(systemState.selectedQuestion);
  }
  void saveSystemQuestionState(systemTutor.questionId, { personal_note: note }, { renderDrawer: false });
  window.getSelection()?.removeAllRanges();
  systemTutor.selectedText = "";
  updateSystemTutorSelectionActions();
}

function followUpSelectedSystemTutorText() {
  if (!systemQuestionTutorPanel || !systemTutor.selectedText) return;
  const inputNode = systemQuestionTutorPanel.querySelector("#systemTutorInput");
  if (inputNode) {
    inputNode.value = `请解释这一步：${systemTutor.selectedText}`;
    inputNode.focus();
  }
}

async function saveSystemQuestionState(questionId, patch, options = {}) {
  const userId = options.userId || currentMaterialsUserId();
  setSystemSaveStatus("saving", "正在保存个人状态...");
  const data = await fetchJson(
    `/api/materials/system/questions/${encodeURIComponent(questionId)}/state?user_id=${encodeURIComponent(userId)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    }
  );
  if (data.personal_state && userId === currentMaterialsUserId()) {
    hydrateSystemQuestionPersonalState(data.question_id || questionId, data.personal_state);
    renderSystemStateSurfaces(data.question_id || questionId, options);
    setSystemSaveStatus("saved", "个人状态已保存");
    void loadSystemStatusSummary();
  }
  return data;
}

function refreshCurrentSystemDrawerIfNeeded(changedIds) {
  if (systemState.selectedQuestion && changedIds.has(systemState.selectedQuestionId)) {
    renderSystemQuestionDrawer(systemState.selectedQuestion);
  }
}

function renderSystemDrawerEmpty(message = "选择一道题查看详情") {
  if (!systemQuestionDrawer) return;
  systemQuestionDrawer.innerHTML = `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function renderSystemPlaceholder(message) {
  if (systemQuestionList) {
    systemQuestionList.className = "system-question-list empty-state";
    systemQuestionList.textContent = message;
  }
  renderSystemPagination();
  renderSystemDrawerEmpty();
}

function renderSystemPagination() {
  if (!systemPagination) return;
  systemPagination.innerHTML = "";
  const summary = document.createElement("span");
  summary.className = "system-pagination-summary";
  summary.textContent = `第 ${systemState.page} 页 / 共 ${systemState.totalPages} 页 · 共 ${systemState.total} 题${systemState.status ? " · 已按状态筛选" : ""}`;

  const actions = document.createElement("div");
  actions.className = "system-pagination-actions";
  const prev = document.createElement("button");
  prev.type = "button";
  prev.className = "small-button";
  prev.textContent = "上一页";
  prev.disabled = systemState.loading || systemState.page <= 1;
  prev.addEventListener("click", () => {
    if (systemState.page <= 1) return;
    systemState.page -= 1;
    void loadSystemQuestions();
  });

  const next = document.createElement("button");
  next.type = "button";
  next.className = "small-button";
  next.textContent = "下一页";
  next.disabled = systemState.loading || systemState.page >= systemState.totalPages;
  next.addEventListener("click", () => {
    if (systemState.page >= systemState.totalPages) return;
    systemState.page += 1;
    void loadSystemQuestions();
  });

  const current = document.createElement("span");
  current.className = "system-pagination-current";
  current.textContent = `${systemState.page} / ${systemState.totalPages}`;

  actions.appendChild(prev);
  actions.appendChild(current);
  actions.appendChild(next);
  systemPagination.appendChild(summary);
  systemPagination.appendChild(actions);
}

function renderSystemTopicOptions(topicOptions = []) {
  if (!systemTopicFilter) return;
  const selected = systemTopicFilter.value || systemState.topic || "";
  const options = [...new Set(
    (Array.isArray(topicOptions) ? topicOptions : [])
      .map((topic) => String(topic || "").trim())
      .filter(Boolean)
  )].sort((a, b) => a.localeCompare(b, "zh-Hans"));

  systemTopicFilter.innerHTML = "";
  const allOption = document.createElement("option");
  allOption.value = "";
  allOption.textContent = "全部";
  systemTopicFilter.appendChild(allOption);

  if (selected && !options.includes(selected)) {
    options.unshift(selected);
  }
  options.forEach((topic) => {
    const option = document.createElement("option");
    option.value = topic;
    option.textContent = topic;
    systemTopicFilter.appendChild(option);
  });
  systemTopicFilter.value = selected;
}

function renderSystemAssetStrip(assetUrls = []) {
  const urls = (Array.isArray(assetUrls) ? assetUrls : [])
    .filter((url) => typeof url === "string" && url.startsWith("/api/materials/system/assets/"));
  if (urls.length === 0) return "";
  return `
    <div class="system-asset-strip">
      <div class="system-asset-strip-title">题图</div>
      ${urls.map((url, index) => `
        <a href="${escapeHtml(url)}" target="_blank" rel="noreferrer">
          <img src="${escapeHtml(url)}" alt="题图 ${index + 1}">
        </a>
      `).join("")}
    </div>
  `;
}

function systemMarkdownHasImages(markdown = "") {
  return /!\[[^\]\n]*]\([^)]+\)/.test(markdown || "");
}

function systemChoiceMarker(line) {
  const match = String(line || "").match(/^\s*(?:[（(]?\s*)?([A-D])\s*(?:[.)．、）])\s*$/);
  return match ? match[1] : "";
}

function isSystemChoiceBoundary(line) {
  return /^\s*(?:[（(]?\s*)?[A-D]\s*(?:[.)．、）])\s*/.test(String(line || ""));
}

function isSystemChoiceSectionEnd(line) {
  return /^\s*(答案|解析|【答案】|【解析】|##|#{1,6}\s)/.test(String(line || ""));
}

function normalizeSystemChoiceOptionMarkdown(value) {
  const lines = String(value || "").split(/\r?\n/);
  const output = [];
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const optionMarker = systemChoiceMarker(line);
    if (!optionMarker) {
      output.push(line);
      continue;
    }
    const optionParts = [`${optionMarker}.`];
    let cursor = index + 1;
    while (cursor < lines.length) {
      const nextLine = lines[cursor];
      if (isSystemChoiceBoundary(nextLine) || isSystemChoiceSectionEnd(nextLine)) {
        break;
      }
      if (/^\s*[A-D]\.\s*/.test(nextLine) || /^\s*(答案|解析|##)\b/.test(nextLine)) {
        break;
      }
      if (!nextLine.trim()) {
        cursor += 1;
        continue;
      }
      optionParts.push(nextLine.trim());
      cursor += 1;
    }
    output.push(optionParts.join(" "));
    index = cursor - 1;
  }
  return output.join("\n");
}

function normalizeInlineSystemChoiceOptionMarkdown(value) {
  const source = String(value || "").replace(/\r\n?/g, "\n");
  const markers = orderedPracticeChoiceMarkers(findPracticeChoiceMarkers(source));
  if (markers.length < 2) {
    return source;
  }

  const firstMarkerStart = markers[0].markerStart;
  const optionEnd = practiceChoiceOptionEnd(source, markers[markers.length - 1].contentStart);
  const before = source.slice(0, firstMarkerStart).trimEnd();
  const after = source.slice(optionEnd).trimStart();
  const parts = [];
  if (before) {
    parts.push(before);
  }
  markers.forEach((marker, index) => {
    const end = index + 1 < markers.length ? markers[index + 1].markerStart : optionEnd;
    const body = source.slice(marker.contentStart, end).trim();
    parts.push(body ? `${marker.key}.\n${body}` : `${marker.key}.`);
  });
  if (after) {
    parts.push(after);
  }
  return parts.join("\n");
}

function normalizeSystemMathCodeExpression(value) {
  let expression = String(value || "").trim();
  expression = expression.replace(/∫/g, "\\int");
  expression = expression.replace(/\s+/g, " ");
  expression = expression.replace(/sqrt\(([^()]+)\)/g, (_, body) => {
    const sqrtMatch = String(body || "").trim();
    return `\\sqrt{${sqrtMatch}}`;
  });
  expression = expression.replace(/\b(sin|cos|tan|ln|lim|max|min)\b/g, "\\$1");
  return expression;
}

function normalizeSystemMathCodeSpans(value) {
  return String(value || "").replace(/`([^`\n]+)`/g, (match, body) => {
    const text = String(body || "").trim();
    if (!/[∫∑√∞_^]|sqrt\(|\\[a-zA-Z]+|[a-zA-Z]\([^)]*\)/.test(text)) {
      return match;
    }
    return `$${normalizeSystemMathCodeExpression(text)}$`;
  });
}

function renderSystemMarkdown(value) {
  const text = value || "";
  if (!text.trim()) return '<div class="empty-state">暂无内容</div>';
  const html = md.render(normalizeMathMarkdown(normalizeSystemMathCodeSpans(normalizeSystemChoiceOptionMarkdown(normalizeInlineSystemChoiceOptionMarkdown(text)))));
  const template = document.createElement("template");
  template.innerHTML = html;
  template.content.querySelectorAll("img").forEach((image) => {
    const src = image.getAttribute("src") || "";
    if (!src.startsWith("/api/materials/system/assets/")) {
      image.replaceWith(document.createTextNode(image.getAttribute("alt") || ""));
      return;
    }
    image.setAttribute("loading", "lazy");
    image.setAttribute("decoding", "async");
  });
  return template.innerHTML;
}

function renderCachedSystemMarkdown(value) {
  const key = String(value || "");
  if (!key.trim()) {
    return renderSystemMarkdown(key);
  }
  if (systemMarkdownRenderCache.has(key)) {
    return systemMarkdownRenderCache.get(key);
  }
  const html = renderSystemMarkdown(key);
  systemMarkdownRenderCache.set(key, html);
  if (systemMarkdownRenderCache.size > SYSTEM_MARKDOWN_RENDER_CACHE_LIMIT) {
    const oldestKey = systemMarkdownRenderCache.keys().next().value;
    systemMarkdownRenderCache.delete(oldestKey);
  }
  return html;
}

function compactSystemQuestionPreviewText(value, fallback = "暂无题干预览") {
  const text = String(value || "")
    .replace(/!\[[^\]]*]\([^)]+\)/g, "")
    .replace(/`([^`\n]+)`/g, "$1")
    .replace(/\${1,2}/g, "")
    .replace(/\\begin\{[^}]+}/g, "")
    .replace(/\\end\{[^}]+}/g, "")
    .replace(/\s+/g, " ")
    .trim();
  return text || fallback;
}

function renderScheduledSystemQuestionPreview(preview) {
  if (!preview || preview.dataset.rendered === "true") {
    return;
  }
  const markdown = preview.dataset.markdown || "";
  preview.innerHTML = renderCachedSystemMarkdown(markdown || "暂无题干预览");
  preview.dataset.rendered = "true";
  preview.removeAttribute("data-markdown");
}

function createSystemQuestionPreviewObserver() {
  if (typeof IntersectionObserver === "undefined") {
    return null;
  }
  return new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting && entry.intersectionRatio <= 0) {
        return;
      }
      renderScheduledSystemQuestionPreview(entry.target);
      observer.unobserve(entry.target);
    });
  }, {
    root: null,
    rootMargin: "420px 0px",
    threshold: 0.01,
  });
}

function scheduleSystemQuestionPreviewRender(preview, markdown) {
  if (!preview) {
    return;
  }
  preview.dataset.markdown = markdown || "暂无题干预览";
  preview.dataset.rendered = "false";
  if (!systemQuestionPreviewObserver) {
    window.requestAnimationFrame(() => renderScheduledSystemQuestionPreview(preview));
    return;
  }
  systemQuestionPreviewObserver.observe(preview);
}

function renderSystemAssetFallback(question) {
  const markdown = question?.question_markdown || question?.preview || "";
  if (systemMarkdownHasImages(markdown)) return "";
  return renderSystemAssetStrip(question?.asset_urls);
}

function renderSystemQuestionMarkdown(question) {
  const markdown = question?.question_markdown || question?.preview || "暂无题干";
  return `
    <div class="system-markdown">${renderSystemMarkdown(markdown)}</div>
    ${renderSystemAssetFallback(question)}
  `;
}

const systemQuestionPreviewObserver = createSystemQuestionPreviewObserver();

function stripPracticeChoiceLeadIn(value = "") {
  const lines = String(value || "").split("\n");
  while (lines.length > 0) {
    const tail = lines[lines.length - 1].trim();
    if (!tail) {
      lines.pop();
      continue;
    }
    if (/^(?:选项|选择项|备选项)\s*[:：]?\s*$/.test(tail)) {
      lines.pop();
      continue;
    }
    break;
  }
  return lines.join("\n").trimEnd();
}

function stripPracticeChoiceOptionsFromMarkdown(markdown = "") {
  const source = String(markdown || "").replace(/\r\n?/g, "\n");
  const markers = orderedPracticeChoiceMarkers(findPracticeChoiceMarkers(source));
  if (markers.length < 2) {
    return source;
  }
  const optionStart = markers[0].markerStart;
  const optionEnd = practiceChoiceOptionEnd(source, markers[markers.length - 1].contentStart);
  const before = stripPracticeChoiceLeadIn(source.slice(0, optionStart).trimEnd());
  const after = source.slice(optionEnd).trimStart();
  return [before, after].filter(Boolean).join("\n\n").trim() || before.trim() || source;
}

function practiceQuestionMarkdownForAttempt(question = {}) {
  const markdown = question?.question_markdown || question?.preview || "暂无题干";
  if (practiceQuestionAnswerType(question) !== "choice") {
    return markdown;
  }
  return stripPracticeChoiceOptionsFromMarkdown(markdown);
}

function renderPracticeQuestionMarkdown(question) {
  const strippedMarkdown = practiceQuestionMarkdownForAttempt(question);
  return renderSystemQuestionMarkdown({ ...question, question_markdown: strippedMarkdown });
}

function renderSystemQuestionList() {
  if (!systemQuestionList) return;
  if (systemState.subject !== "math") {
    renderSystemPlaceholder("该学科系统题库待补充");
    updateSystemBatchActionState();
    return;
  }
  if (systemState.contentType !== "questions") {
    renderSystemPlaceholder("知识点库待接入");
    updateSystemBatchActionState();
    return;
  }
  if (systemState.loading) {
    systemQuestionList.className = "system-question-list empty-state";
    systemQuestionList.textContent = "正在加载系统题库...";
    renderSystemPagination();
    updateSystemBatchActionState();
    return;
  }
  if (systemState.error) {
    systemQuestionList.className = "system-question-list empty-state";
    systemQuestionList.textContent = `系统题库加载失败：${systemState.error}`;
    renderSystemPagination();
    updateSystemBatchActionState();
    return;
  }

  const items = filteredSystemItems();
  systemQuestionList.innerHTML = "";
  if (items.length === 0) {
    systemQuestionList.className = "system-question-list empty-state";
    systemQuestionList.textContent = systemState.items.length === 0
      ? "没有找到符合条件的题目"
      : "当前页没有匹配个人状态的题目，可切换页码或清除状态筛选。";
    renderSystemPagination();
    updateSystemBatchActionState();
    return;
  }

  systemQuestionList.className = "system-question-list";
  const fragment = document.createDocumentFragment();
  items.forEach((item) => {
    const personal = systemUserState(item.question_id);
    const card = document.createElement("article");
    card.className = `system-question-card${item.question_id === systemState.selectedQuestionId ? " active" : ""}`;
    card.classList.toggle("favorite", personal.is_favorite);

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "system-question-check";
    checkbox.checked = systemState.selectedIds.has(item.question_id);
    checkbox.setAttribute("aria-label", `选择 ${systemQuestionTitle(item)}`);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        systemState.selectedIds.add(item.question_id);
      } else {
        systemState.selectedIds.delete(item.question_id);
      }
      renderSystemPagination();
      updateSystemBatchActionState();
    });

    const body = document.createElement("div");
    body.className = "system-question-card-body";

    const header = document.createElement("div");
    header.className = "system-question-card-header";
    const titleRow = document.createElement("div");
    titleRow.className = "system-question-title-row";
    const title = document.createElement("div");
    title.className = "system-question-card-title";
    title.textContent = systemQuestionTitle(item);
    const inlineMeta = document.createElement("div");
    inlineMeta.className = "system-question-inline-meta";
    inlineMeta.innerHTML = `
      <span class="status-pill type">${escapeHtml(item.question_type_label || item.question_type || "题型未知")}</span>
      <span class="status-pill ${escapeHtml(personal.mastery_status)}">${escapeHtml(SYSTEM_MASTERY_LABELS[personal.mastery_status] || "未开始")}</span>
      ${personal.is_favorite ? '<span class="status-pill favorite">已收藏</span>' : ""}
      ${personal.in_wrong_book ? '<span class="status-pill wrong">错题</span>' : ""}
      ${personal.personal_note ? '<span class="status-pill note">有备注</span>' : ""}
    `;
    titleRow.appendChild(title);
    titleRow.appendChild(inlineMeta);
    const library = document.createElement("span");
    library.className = "system-library-name";
    library.textContent = item.library_name || "系统题库";
    header.appendChild(titleRow);
    header.appendChild(library);

    const preview = document.createElement("p");
    preview.className = "system-question-preview";
    preview.dataset.rendered = "false";
    preview.textContent = compactSystemQuestionPreviewText(item.preview, "暂无题干预览");
    scheduleSystemQuestionPreviewRender(preview, item.preview || "暂无题干预览");

    const topics = document.createElement("div");
    topics.className = "system-topic-list";
    (item.topics || []).slice(0, 6).forEach((topic) => {
      const pill = document.createElement("span");
      pill.textContent = topic;
      topics.appendChild(pill);
    });

    const footer = document.createElement("div");
    footer.className = "system-question-footer";
    const actions = document.createElement("div");
    actions.className = "system-question-actions";
    const previewButton = document.createElement("button");
    previewButton.type = "button";
    previewButton.className = "small-button system-preview-button";
    previewButton.title = "预览完整题干";
    previewButton.setAttribute("aria-label", `预览完整题干：${systemQuestionTitle(item)}`);
    previewButton.innerHTML = '<span class="system-eye-icon" aria-hidden="true"></span><span class="sr-only">预览完整题干</span>';
    previewButton.addEventListener("click", () => void openSystemQuestionPreview(item.question_id));

    const viewButton = document.createElement("button");
    viewButton.type = "button";
    viewButton.className = "small-button dark-button";
    viewButton.textContent = "查看";
    viewButton.addEventListener("click", () => void openSystemQuestionDrawer(item.question_id));

    const favoriteButton = document.createElement("button");
    favoriteButton.type = "button";
    favoriteButton.className = `small-button ${personal.is_favorite ? "active" : ""}`;
    favoriteButton.setAttribute("aria-pressed", personal.is_favorite ? "true" : "false");
    favoriteButton.textContent = personal.is_favorite ? "取消收藏" : "收藏";
    favoriteButton.addEventListener("click", () => toggleSystemFavorite(item.question_id));

    const wrongButton = document.createElement("button");
    wrongButton.type = "button";
    wrongButton.className = "small-button";
    wrongButton.textContent = personal.in_wrong_book ? "移出错题" : "错题";
    wrongButton.addEventListener("click", () => toggleSystemWrongBook(item.question_id));

    actions.appendChild(previewButton);
    actions.appendChild(viewButton);
    actions.appendChild(favoriteButton);
    actions.appendChild(wrongButton);
    footer.appendChild(topics);
    footer.appendChild(actions);
    body.appendChild(header);
    body.appendChild(preview);
    body.appendChild(footer);
    card.appendChild(checkbox);
    card.appendChild(body);
    fragment.appendChild(card);
  });
  systemQuestionList.appendChild(fragment);
  renderSystemPagination();
  updateSystemBatchActionState();
}

function syncSystemFiltersFromInputs() {
  systemState.examType = systemLibraryNameFilter ? systemLibraryNameFilter.value : "math1";
  systemState.year = systemYearFilter?.value || "";
  systemState.questionType = systemQuestionTypeFilter?.value || "";
  systemState.topic = (systemTopicFilter?.value || "").trim();
  systemState.status = systemStatusFilter?.value || "";
  systemState.query = (systemSearchInput?.value || "").trim();
}

async function loadSystemQuestions() {
  syncSystemUserScope();
  syncSystemFiltersFromInputs();
  systemState.selectedQuestion = null;
  systemState.error = "";
  const requestId = ++systemQuestionsRequestSeq;

  if (systemState.subject !== "math" || systemState.contentType !== "questions") {
    systemState.loading = false;
    systemState.items = [];
    systemState.total = 0;
    systemState.totalPages = 1;
    renderSystemTopicOptions([]);
    systemState.stateSummary = {};
    renderSystemStatusSummary();
    renderSystemQuestionList();
    return;
  }

  systemState.loading = true;
  renderSystemQuestionList();
  void loadSystemStatusSummary();
  const params = systemQuestionRequestParams({ includePage: true, includeStatus: true });

  try {
    const data = await fetchJson(`/api/materials/system/questions?${params.toString()}`);
    if (requestId !== systemQuestionsRequestSeq) return;
    systemState.items = (data.items || []).map((item) => {
      hydrateSystemQuestionPersonalState(item.question_id, item.personal_state);
      return item;
    });
    systemState.total = Number(data.total || 0);
    systemState.totalPages = Math.max(1, Number(data.total_pages || 1));
    systemState.page = Number(data.page || systemState.page);
    renderSystemTopicOptions(data.topic_options || []);
  } catch (error) {
    if (requestId !== systemQuestionsRequestSeq) return;
    systemState.items = [];
    systemState.total = 0;
    systemState.totalPages = 1;
    systemState.error = error.message;
    renderSystemTopicOptions([]);
  } finally {
    if (requestId !== systemQuestionsRequestSeq) return;
    systemState.loading = false;
    renderSystemQuestionList();
  }
}

function setSystemMastery(questionId, masteryStatus) {
  if (!Object.prototype.hasOwnProperty.call(SYSTEM_MASTERY_LABELS, masteryStatus)) {
    return;
  }
  applyAndSaveSystemQuestionState(questionId, { mastery_status: masteryStatus });
}

function toggleSystemFavorite(questionId) {
  const personal = systemUserState(questionId);
  applyAndSaveSystemQuestionState(questionId, { is_favorite: !personal.is_favorite });
}

function toggleSystemWrongBook(questionId) {
  const personal = systemUserState(questionId);
  applyAndSaveSystemQuestionState(questionId, { in_wrong_book: !personal.in_wrong_book });
}

function updateSystemBatchActionState() {
  const selectedCount = systemState.selectedIds.size;
  document.querySelectorAll("[data-system-action]").forEach((button) => {
    if (!button.dataset.baseLabel) {
      button.dataset.baseLabel = button.textContent;
    }
    button.textContent = selectedCount > 0
      ? `${button.dataset.baseLabel}（已选 ${selectedCount}）`
      : button.dataset.baseLabel;
  });
}

function applySystemBatchAction(action) {
  const selectedIds = new Set(systemState.selectedIds);
  if (selectedIds.size === 0) {
    window.alert("请先选择题目。");
    return;
  }
  if (action === "mark-mastered") {
    selectedIds.forEach((questionId) => {
      applyAndSaveSystemQuestionState(questionId, { mastery_status: "mastered" }, { render: false });
    });
    renderSystemQuestionList();
    refreshCurrentSystemDrawerIfNeeded(selectedIds);
    return;
  }
  if (action === "add-wrong-book") {
    selectedIds.forEach((questionId) => {
      applyAndSaveSystemQuestionState(questionId, { in_wrong_book: true }, { render: false });
    });
    renderSystemQuestionList();
    refreshCurrentSystemDrawerIfNeeded(selectedIds);
    return;
  }
  if (action === "generate-practice") {
    const firstQuestion = systemState.items.find((item) => selectedIds.has(item.question_id));
    if (!firstQuestion) {
      window.alert("未找到已选择题目的当前页数据。");
      return;
    }
    openSystemPracticeModal(firstQuestion, { seedQuestionIds: [...selectedIds] });
  }
}

function closeSystemWorkflowModal() {
  document.querySelector(".system-workflow-overlay")?.remove();
}

function systemWorkflowKeydownHandler(overlay, close) {
  return (event) => {
    if (event.key === "Escape" && overlay.isConnected) {
      close();
    }
  };
}

function createSystemWorkflowOverlay(title, subtitle, options = {}) {
  closeSystemWorkflowModal();
  const headerActionLabel = options.headerActionLabel || "关闭";
  const overlay = document.createElement("div");
  overlay.className = "system-workflow-overlay";
  overlay.innerHTML = `
    <section class="system-workflow-dialog" role="dialog" aria-modal="true" aria-labelledby="systemWorkflowTitle">
      <header class="system-workflow-header">
        <div>
          <p class="eyebrow">System Library</p>
          <h3 id="systemWorkflowTitle">${escapeHtml(title)}</h3>
          ${subtitle ? `<p class="helper-text">${escapeHtml(subtitle)}</p>` : ""}
        </div>
        <button type="button" class="small-button" data-system-workflow-close>${escapeHtml(headerActionLabel)}</button>
      </header>
      <div class="system-workflow-body"></div>
    </section>
  `;
  const close = () => {
    document.removeEventListener("keydown", onKeyDown);
    overlay.remove();
  };
  const runHeaderAction = () => {
    if (typeof options.onHeaderAction === "function") {
      options.onHeaderAction({ overlay, close });
      return;
    }
    close();
  };
  const onKeyDown = systemWorkflowKeydownHandler(overlay, close);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) close();
  });
  overlay.querySelector("[data-system-workflow-close]")?.addEventListener("click", runHeaderAction);
  document.addEventListener("keydown", onKeyDown);
  document.body.appendChild(overlay);
  return { overlay, close };
}

function systemPracticeCandidateItems(question, config) {
  const count = Math.max(1, Math.min(50, Number(config.count || 5)));
  const seedIds = new Set(config.seedQuestionIds || []);
  const topicFilters = new Set(config.topicFilters || []);
  const pool = [...systemState.items];
  const candidates = pool.filter((item) => {
    if (!item?.question_id) return false;
    if (question?.question_id && item.question_id === question.question_id) return false;
    if (!systemPracticeItemMatchesSourceScope(item, question, config.sourceScope || "exam_type")) {
      return false;
    }
    if (config.sameType && question?.question_type && item.question_type !== question.question_type) {
      return seedIds.has(item.question_id);
    }
    if (config.excludeMastered && systemUserState(item.question_id).mastery_status === "mastered") {
      return seedIds.has(item.question_id);
    }
    if (topicFilters.size > 0) {
      const itemTopics = Array.isArray(item.topics) ? item.topics.map(String) : [];
      if (!itemTopics.some((topic) => topicFilters.has(topic))) {
        return seedIds.has(item.question_id);
      }
    }
    return true;
  });
  const ordered = [
    ...candidates.filter((item) => seedIds.has(item.question_id)),
    ...candidates.filter((item) => !seedIds.has(item.question_id)),
  ];
  const seen = new Set();
  return ordered.filter((item) => {
    if (seen.has(item.question_id)) return false;
    seen.add(item.question_id);
    return true;
  }).slice(0, count);
}

function systemPracticeItemMatchesSourceScope(item, question, sourceScope) {
  if (!question) return true;
  if (sourceScope === "same_year") {
    return String(item.year || "") === String(question.year || "");
  }
  if (sourceScope === "same_library") {
    return String(item.library_name || item.exam_type || "") === String(question.library_name || question.exam_type || "");
  }
  if (sourceScope === "subject") {
    return true;
  }
  return String(item.exam_type || "") === String(question.exam_type || systemState.examType || "");
}

function systemPracticeTopicOptions(question) {
  const sourceTopics = Array.isArray(question?.topics)
    ? question.topics.map((topic) => String(topic).trim()).filter(Boolean)
    : [];
  return [...new Set(sourceTopics)];
}

function systemPracticePreviewPayload(question, config) {
  return {
    source_question_id: question?.question_id || "",
    count: Math.max(1, Math.min(50, Number(config.count || 5))),
    same_type_only: Boolean(config.sameType),
    exclude_mastered: Boolean(config.excludeMastered),
    topic_filters: Array.isArray(config.topicFilters) ? config.topicFilters : [],
    source_scope: config.sourceScope || "exam_type",
    subject: systemState.subject,
    exam_type: systemState.examType,
  };
}

function currentSystemPracticeCandidates(question, config) {
  if (Array.isArray(config.previewCandidates) && (config.previewLoaded || config.previewCandidates.length)) {
    return config.previewCandidates;
  }
  return systemPracticeCandidateItems(question, config);
}

function systemPracticeCanCreate(candidates, config = {}) {
  return Boolean(candidates.length && !config.previewLoading && !config.creating);
}

function systemPracticeCreateButtonLabel(candidates, config = {}) {
  if (config.creating) return "生成中...";
  if (config.previewLoading) return "候选加载中...";
  if (!candidates.length) return "暂无可生成题目";
  return "生成练习单";
}

function reloadSystemPracticeCandidatePreview(question, config, overlay, patch = {}) {
  Object.assign(config, patch);
  config.createdPracticeSet = null;
  config.previewCandidates = [];
  config.previewTotal = 0;
  config.previewLoaded = false;
  config.previewError = "";
  void loadSystemPracticeCandidatePreview(question, config, overlay);
}

async function loadSystemPracticeCandidatePreview(question, config, overlay) {
  const requestSeq = Number(config.previewRequestSeq || 0) + 1;
  config.previewRequestSeq = requestSeq;
  config.previewLoading = true;
  config.previewLoaded = false;
  config.previewError = "";
  renderSystemPracticeModal(overlay, question, config);
  try {
    const data = await fetchJson(`/api/materials/system/practice-candidates?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(systemPracticePreviewPayload(question, config)),
    });
    if (config.previewRequestSeq !== requestSeq) return;
    config.previewCandidates = Array.isArray(data.items) ? data.items : [];
    config.previewTotal = Number(data.total || config.previewCandidates.length || 0);
    config.previewLoaded = true;
    config.previewError = "";
  } catch (error) {
    if (config.previewRequestSeq !== requestSeq) return;
    config.previewCandidates = [];
    config.previewTotal = 0;
    config.previewLoaded = false;
    config.previewError = error.message || "candidate preview failed";
  } finally {
    if (config.previewRequestSeq === requestSeq) {
      config.previewLoading = false;
      renderSystemPracticeModal(overlay, question, config);
    }
  }
}

function systemPracticeSetId(practiceSet = {}) {
  return practiceSet.practice_set_id || practiceSet.id || practiceSet.set_id || "";
}

function renderSystemPracticeEmptyRecoveryActions(config = {}) {
  const actions = [];
  if (Array.isArray(config.topicFilters) && config.topicFilters.length) {
    actions.push('<button type="button" class="small-button" data-system-practice-relax-topics>放宽知识点</button>');
  }
  if (config.sameType) {
    actions.push('<button type="button" class="small-button" data-system-practice-relax-type>取消同题型</button>');
  }
  if ((config.sourceScope || "exam_type") !== "subject") {
    actions.push('<button type="button" class="small-button" data-system-practice-expand-scope>扩大到全部数学题库</button>');
  }
  if (!actions.length) return "";
  return `<div class="system-practice-empty-actions">${actions.join("")}</div>`;
}

function renderSystemPracticeCandidatePreview(candidates, config = {}) {
  if (config.previewLoading) {
    return '<div class="empty-state">正在按当前范围刷新候选题，请稍等...</div>';
  }
  const errorHtml = config.previewError
    ? `<div class="empty-state">候选预览加载失败，暂用本页候选兜底：${escapeHtml(config.previewError)}</div>`
    : "";
  if (!candidates.length && errorHtml) {
    return `${errorHtml}<div class="empty-state">当前筛选下没有候选题。</div>${renderSystemPracticeEmptyRecoveryActions(config)}`;
  }
  if (!candidates.length) {
    return `<div class="empty-state">当前筛选下没有可预览的候选题。</div>${renderSystemPracticeEmptyRecoveryActions(config)}`;
  }
  const total = Number(config.previewTotal || candidates.length || 0);
  return `
    ${errorHtml}
    <p class="system-practice-candidate-summary">已匹配 ${candidates.length} 题${total > candidates.length ? ` / 共 ${total} 题` : ""}</p>
    <div class="system-practice-candidate-list" data-system-practice-candidates>
      ${candidates.map((item) => `
        <article class="system-practice-candidate">
          <strong>${escapeHtml(systemQuestionTitle(item))}</strong>
          <span>${escapeHtml(item.question_type_label || item.question_type || "题型未知")}</span>
          <p>${escapeHtml((item.topics || []).join(" / ") || item.library_name || "系统题库")}</p>
        </article>
      `).join("")}
    </div>
  `;
}

function renderSystemPracticeSetSummary(practiceSet, candidates) {
  const practiceSetId = systemPracticeSetId(practiceSet);
  const questionCount = Number(practiceSet.question_count || practiceSet.count || candidates.length || 0);
  return `
    <section class="system-workflow-result practice-result">
      <div>
        <strong>练习单已生成</strong>
        <p>${escapeHtml(practiceSet.title || practiceSet.name || "同类训练")} · ${questionCount} 题</p>
      </div>
      <div class="system-workflow-result-actions practice-result-actions">
        <button type="button" class="small-button dark-button" data-system-practice-start>开始练习</button>
        <button type="button" class="small-button" data-system-practice-view>查看练习单</button>
        <button type="button" class="small-button" data-system-practice-add-review>加入复习规划</button>
        <button type="button" class="small-button" data-system-practice-download-pdf>下载 PDF</button>
        <button type="button" class="small-button" data-system-practice-delete ${practiceSetId ? "" : "disabled"}" ${practiceSetId ? "" : "disabled"}>删除练习单</button>
      </div>
    </section>
  `;
}

function renderSystemPracticeModal(overlay, question, config) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const candidates = currentSystemPracticeCandidates(question, config);
  const canCreate = systemPracticeCanCreate(candidates, config);
  const topicOptions = systemPracticeTopicOptions(question);
  const created = config.createdPracticeSet;
  const currentExamLabel = systemExamTypeLabel(systemState.examType || question.exam_type);
  body.innerHTML = `
    <div class="workflow-form-grid">
      <label class="field">
        <span>题源</span>
        <input type="text" value="${escapeHtml(systemQuestionTitle(question))}" readonly>
      </label>
      <label class="field">
        <span>数量</span>
        <input type="number" min="1" max="50" value="${Number(config.count || 5)}" data-system-practice-count>
      </label>
      <label class="field">
        <span>找题范围</span>
        <select data-system-practice-source-scope>
          <option value="exam_type" ${config.sourceScope === "exam_type" ? "selected" : ""}>当前${currentExamLabel}题库</option>
          <option value="same_library" ${config.sourceScope === "same_library" ? "selected" : ""}>同一资料库</option>
          <option value="same_year" ${config.sourceScope === "same_year" ? "selected" : ""}>同一年真题</option>
          <option value="subject" ${config.sourceScope === "subject" ? "selected" : ""}>全部数学题库</option>
        </select>
      </label>
      <label class="check-row workflow-check-row">
        <input type="checkbox" data-system-practice-same-type ${config.sameType ? "checked" : ""}>
        同题型
      </label>
      <label class="check-row workflow-check-row">
        <input type="checkbox" data-system-practice-exclude-mastered ${config.excludeMastered ? "checked" : ""}>
        排除已掌握
      </label>
    </div>
    ${topicOptions.length ? `
      <section class="system-workflow-section">
        <h4>知识点筛选</h4>
        <div class="system-practice-topic-filter">
          ${topicOptions.map((topic) => `
            <label class="check-row workflow-check-row">
              <input type="checkbox" value="${escapeHtml(topic)}" data-system-practice-topic-filter ${config.topicFilters.includes(topic) ? "checked" : ""}>
              ${escapeHtml(topic)}
            </label>
          `).join("")}
        </div>
      </section>
    ` : ""}
    <section class="system-workflow-section">
      <h4>候选预览</h4>
      ${renderSystemPracticeCandidatePreview(candidates, config)}
    </section>
    ${created ? renderSystemPracticeSetSummary(created, candidates) : ""}
    <div class="system-workflow-actions">
      <button type="button" class="small-button dark-button" data-system-practice-create ${canCreate ? "" : "disabled"}>${systemPracticeCreateButtonLabel(candidates, config)}</button>
    </div>
  `;
  body.querySelector("[data-system-practice-count]")?.addEventListener("input", (event) => {
    config.count = event.target.value;
    reloadSystemPracticeCandidatePreview(question, config, overlay);
  });
  body.querySelector("[data-system-practice-source-scope]")?.addEventListener("change", (event) => {
    reloadSystemPracticeCandidatePreview(question, config, overlay, {
      sourceScope: event.target.value || "exam_type",
    });
  });
  body.querySelector("[data-system-practice-same-type]")?.addEventListener("change", (event) => {
    reloadSystemPracticeCandidatePreview(question, config, overlay, {
      sameType: event.target.checked,
    });
  });
  body.querySelector("[data-system-practice-exclude-mastered]")?.addEventListener("change", (event) => {
    reloadSystemPracticeCandidatePreview(question, config, overlay, {
      excludeMastered: event.target.checked,
    });
  });
  body.querySelectorAll("[data-system-practice-topic-filter]").forEach((input) => {
    input.addEventListener("change", () => {
      const topicFilters = [...body.querySelectorAll("[data-system-practice-topic-filter]:checked")]
        .map((item) => item.value)
        .filter(Boolean);
      reloadSystemPracticeCandidatePreview(question, config, overlay, { topicFilters });
    });
  });
  body.querySelector("[data-system-practice-relax-topics]")?.addEventListener("click", () => {
    config.topicFilters = [];
    reloadSystemPracticeCandidatePreview(question, config, overlay, { topicFilters: [] });
  });
  body.querySelector("[data-system-practice-relax-type]")?.addEventListener("click", () => {
    config.sameType = false;
    reloadSystemPracticeCandidatePreview(question, config, overlay, { sameType: false });
  });
  body.querySelector("[data-system-practice-expand-scope]")?.addEventListener("click", () => {
    config.sourceScope = "subject";
    reloadSystemPracticeCandidatePreview(question, config, overlay, { sourceScope: "subject" });
  });
  body.querySelector("[data-system-practice-create]")?.addEventListener("click", () => {
    void createSystemPracticeSet(question, config, overlay);
  });
  body.querySelector("[data-system-practice-add-review]")?.addEventListener("click", () => {
    openSystemReviewModal(question, {
      practiceSet: config.createdPracticeSet,
      questionIds: candidates.map((item) => item.question_id),
    });
  });
  body.querySelector("[data-system-practice-delete]")?.addEventListener("click", () => {
    void deleteSystemPracticeSet(config.createdPracticeSet, question, config, overlay);
  });
  body.querySelector("[data-system-practice-start]")?.addEventListener("click", () => {
    void openPracticeAttempt(config.createdPracticeSet, candidates, { fallbackQuestions: candidates });
  });
  body.querySelector("[data-system-practice-view]")?.addEventListener("click", () => {
    void openSystemPracticeSetDetail(config.createdPracticeSet, { fallbackQuestions: candidates });
  });
  body.querySelector("[data-system-practice-download-pdf]")?.addEventListener("click", () => {
    void openSystemPracticeSetPrintable(config.createdPracticeSet, { fallbackQuestions: candidates });
  });
}

function openSystemPracticeModal(question, options = {}) {
  const { overlay } = createSystemWorkflowOverlay("生成同类训练", "从当前题目或已选题目出发，生成可追踪的练习单。");
  const config = {
    count: Math.max(1, options.seedQuestionIds?.length || 5),
    sameType: true,
    excludeMastered: true,
    topicFilters: systemPracticeTopicOptions(question),
    sourceScope: "exam_type",
    seedQuestionIds: options.seedQuestionIds || [question.question_id],
    previewCandidates: [],
    previewTotal: 0,
    previewLoaded: false,
    previewLoading: false,
    previewError: "",
    previewRequestSeq: 0,
    creating: false,
    createdPracticeSet: null,
  };
  renderSystemPracticeModal(overlay, question, config);
  void loadSystemPracticeCandidatePreview(question, config, overlay);
}

async function createSystemPracticeSet(question, config, overlay) {
  const candidates = currentSystemPracticeCandidates(question, config);
  if (config.previewLoading) {
    setSystemSaveStatus("saving", "候选题还在加载，请稍后生成。");
    renderSystemPracticeModal(overlay, question, config);
    return;
  }
  if (!candidates.length) {
    setSystemSaveStatus("error", "当前筛选下没有可生成的候选题，请先放宽条件。");
    renderSystemPracticeModal(overlay, question, config);
    return;
  }
  config.creating = true;
  renderSystemPracticeModal(overlay, question, config);
  try {
    const questionIds = candidates.map((item) => item.question_id);
    const payload = {
      source_question_id: question.question_id,
      count: Math.max(1, Math.min(50, Number(config.count || 5))),
      same_type_only: Boolean(config.sameType),
      exclude_mastered: Boolean(config.excludeMastered),
      topic_filters: config.topicFilters,
      source_scope: config.sourceScope,
      subject: systemState.subject,
      exam_type: systemState.examType,
      title: `${systemQuestionTitle(question)} 同类训练`,
    };
    const data = await fetchJson(`/api/materials/system/practice-sets?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    config.createdPracticeSet = data.practice_set || data;
    if (!Array.isArray(config.createdPracticeSet.question_ids)) {
      config.createdPracticeSet.question_ids = questionIds;
    }
    setSystemSaveStatus("saved", "练习单已生成");
  } catch (error) {
    config.createdPracticeSet = null;
    setSystemSaveStatus("error", `练习单生成失败：${error.message}`);
  } finally {
    config.creating = false;
    renderSystemPracticeModal(overlay, question, config);
  }
}

async function deleteSystemPracticeSet(practiceSet, question, config, overlay) {
  const practiceSetId = systemPracticeSetId(practiceSet);
  if (!practiceSetId) return;
  try {
    await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "DELETE",
    });
    config.createdPracticeSet = null;
    setSystemSaveStatus("saved", "练习单已删除");
    renderSystemPracticeModal(overlay, question, config);
  } catch (error) {
    setSystemSaveStatus("error", `删除练习单失败：${error.message}`);
  }
}

function wrongPoolQuestionTypeLabel(value) {
  const labels = {
    single_choice: "选择题",
    multiple_choice: "选择题",
    choice: "选择题",
    fill_blank: "填空题",
    blank: "填空题",
    solution: "解答题",
  };
  return labels[value] || value || "题型";
}

function wrongPoolRiskTypeLabel(value) {
  const labels = {
    "": "全部风险",
    all: "全部风险",
    wrong: "错题",
    pending: "待核对",
    skipped: "多次未答",
    manual: "手动标记",
  };
  return labels[value] || value || "风险类型";
}

function wrongPoolRiskTypeOptions(config) {
  const rawOptions = Array.isArray(config.riskTypeOptions) ? config.riskTypeOptions : [];
  const seen = new Set();
  const options = [];
  [{ value: "", label: "全部风险" }, ...rawOptions].forEach((option) => {
    const value = String(option.value || "");
    if (seen.has(value)) return;
    seen.add(value);
    options.push({
      value,
      label: option.label || wrongPoolRiskTypeLabel(value),
      count: Number(option.count || 0),
    });
  });
  ["wrong", "pending", "skipped", "manual"].forEach((value) => {
    if (!seen.has(value)) {
      options.push({ value, label: wrongPoolRiskTypeLabel(value), count: 0 });
    }
  });
  return options;
}

function renderPriorityReasonTags(reasons = []) {
  const tags = Array.isArray(reasons)
    ? reasons.filter((reason) => reason && (reason.label || reason.type)).slice(0, 4)
    : [];
  if (!tags.length) return "";
  return `
    <div class="priority-reason-list">
      ${tags.map((reason) => `<span class="priority-reason-chip">${escapeHtml(reason.label || reason.type || "")}</span>`).join("")}
    </div>
  `;
}

function wrongPoolSelectedItems(config) {
  const selectedIds = config.selectedIds || new Set();
  return (config.items || []).filter((item) => selectedIds.has(item.question_id));
}

function renderWrongPoolItem(item, config) {
  const selected = config.selectedIds?.has(item.question_id);
  const riskText = `错题 ${Number(item.wrong_count || 0)} · 待核对 ${Number(item.pending_review_count || 0)} · 共练 ${Number(item.attempt_count || 0)} 次`;
  return `
    <article class="wrong-pool-item ${selected ? "selected" : ""}">
      <label class="wrong-pool-check">
        <input type="checkbox" value="${escapeHtml(item.question_id)}" data-wrong-pool-item ${selected ? "checked" : ""}>
      </label>
      <div class="wrong-pool-item-body">
        <div class="wrong-pool-item-head">
          <strong>${escapeHtml(item.title || item.question_id)}</strong>
          <span>${escapeHtml(item.library_name || systemExamTypeLabel(item.exam_type))}</span>
        </div>
        <p>${escapeHtml(item.preview || "暂无题干预览")}</p>
        <div class="wrong-pool-meta">
          <span>${escapeHtml(wrongPoolQuestionTypeLabel(item.question_type))}</span>
          <span>${escapeHtml((item.topics || []).join(" / ") || "未标注知识点")}</span>
          <span>${escapeHtml(riskText)}</span>
          <span>优先级 ${escapeHtml(String(item.priority_score || 0))}</span>
        </div>
        ${renderPriorityReasonTags(item.priority_reasons)}
      </div>
    </article>
  `;
}

function renderWrongQuestionPoolModal(overlay, config) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const selectedItems = wrongPoolSelectedItems(config);
  const created = config.createdPracticeSet;
  const topicOptions = Array.isArray(config.topicOptions) ? config.topicOptions : [];
  const typeOptions = Array.isArray(config.questionTypeOptions) ? config.questionTypeOptions : [];
  body.innerHTML = `
    <div class="workflow-form-grid wrong-pool-filters">
      <label class="field">
        <span>题库范围</span>
        <select data-wrong-pool-exam-type>
          <option value="" ${config.examType ? "" : "selected"}>全部数学题库</option>
          <option value="math1" ${config.examType === "math1" ? "selected" : ""}>数学一真题</option>
          <option value="math2" ${config.examType === "math2" ? "selected" : ""}>数学二真题</option>
          <option value="math3" ${config.examType === "math3" ? "selected" : ""}>数学三真题</option>
        </select>
      </label>
      <label class="field">
        <span>题型</span>
        <select data-wrong-pool-question-type>
          <option value="" ${config.questionType ? "" : "selected"}>全部题型</option>
          ${["single_choice", "fill_blank", "solution", ...typeOptions.filter((item) => !["single_choice", "fill_blank", "solution"].includes(item))]
            .map((type) => `<option value="${escapeHtml(type)}" ${config.questionType === type ? "selected" : ""}>${escapeHtml(wrongPoolQuestionTypeLabel(type))}</option>`)
            .join("")}
        </select>
      </label>
      <label class="field">
        <span>知识点</span>
        <select data-wrong-pool-topic>
          <option value="" ${config.topic ? "" : "selected"}>全部知识点</option>
          ${topicOptions.map((topic) => `<option value="${escapeHtml(topic)}" ${config.topic === topic ? "selected" : ""}>${escapeHtml(topic)}</option>`).join("")}
        </select>
      </label>
      <label class="field">
        <span>风险类型</span>
        <select data-wrong-pool-risk-type>
          ${wrongPoolRiskTypeOptions(config)
            .map((option) => `
              <option value="${escapeHtml(option.value)}" ${config.riskType === option.value ? "selected" : ""}>
                ${escapeHtml(option.label)}${option.count ? `（${escapeHtml(String(option.count))}）` : ""}
              </option>
            `)
            .join("")}
        </select>
      </label>
    </div>
    <section class="system-workflow-section">
      <div class="wrong-pool-summary">
        <div>
          <h4>错题池</h4>
          <p>${config.loading ? "正在读取错题..." : `共 ${Number(config.total || 0)} 道可复习错题，默认勾选优先级最高的 ${Math.min(5, Number(config.total || 0))} 道。`}</p>
        </div>
        <span class="status-pill learning">已选 ${selectedItems.length}</span>
      </div>
      ${config.error ? `<p class="helper-text error-text">${escapeHtml(config.error)}</p>` : ""}
      ${config.loading ? `
        <div class="empty-state">正在加载错题池...</div>
      ` : config.items.length ? `
        <div class="wrong-pool-list">
          ${config.items.map((item) => renderWrongPoolItem(item, config)).join("")}
        </div>
      ` : `
        <div class="empty-state">当前筛选下没有错题。可以换一个学科、题型或知识点。</div>
      `}
    </section>
    ${created ? renderSystemPracticeSetSummary(created, selectedItems) : ""}
    <div class="system-workflow-actions">
      <button type="button" class="small-button dark-button" data-wrong-pool-create ${selectedItems.length && !config.creating ? "" : "disabled"}>
        ${config.creating ? "生成中..." : "生成错题练习单"}
      </button>
    </div>
  `;
  body.querySelector("[data-wrong-pool-exam-type]")?.addEventListener("change", (event) => {
    config.examType = event.target.value || "";
    config.createdPracticeSet = null;
    void loadWrongQuestionPool(config, overlay);
  });
  body.querySelector("[data-wrong-pool-question-type]")?.addEventListener("change", (event) => {
    config.questionType = event.target.value || "";
    config.createdPracticeSet = null;
    void loadWrongQuestionPool(config, overlay);
  });
  body.querySelector("[data-wrong-pool-topic]")?.addEventListener("change", (event) => {
    config.topic = event.target.value || "";
    config.createdPracticeSet = null;
    void loadWrongQuestionPool(config, overlay);
  });
  body.querySelector("[data-wrong-pool-risk-type]")?.addEventListener("change", (event) => {
    config.riskType = event.target.value || "";
    config.createdPracticeSet = null;
    void loadWrongQuestionPool(config, overlay);
  });
  body.querySelectorAll("[data-wrong-pool-item]").forEach((input) => {
    input.addEventListener("change", () => {
      if (input.checked) {
        config.selectedIds.add(input.value);
      } else {
        config.selectedIds.delete(input.value);
      }
      config.createdPracticeSet = null;
      renderWrongQuestionPoolModal(overlay, config);
    });
  });
  body.querySelector("[data-wrong-pool-create]")?.addEventListener("click", () => {
    void createWrongPoolPracticeSet(config, overlay);
  });
  body.querySelector("[data-system-practice-start]")?.addEventListener("click", () => {
    void openPracticeAttempt(config.createdPracticeSet, selectedItems, { fallbackQuestions: selectedItems });
  });
  body.querySelector("[data-system-practice-view]")?.addEventListener("click", () => {
    void openSystemPracticeSetDetail(config.createdPracticeSet, { fallbackQuestions: selectedItems });
  });
  body.querySelector("[data-system-practice-add-review]")?.addEventListener("click", () => {
    openSystemReviewModal(selectedItems[0] || {}, {
      practiceSet: config.createdPracticeSet,
      questionIds: practiceSetQuestionIds(config.createdPracticeSet, selectedItems),
    });
  });
  body.querySelector("[data-system-practice-download-pdf]")?.addEventListener("click", () => {
    void openSystemPracticeSetPrintable(config.createdPracticeSet, { fallbackQuestions: selectedItems });
  });
  body.querySelector("[data-system-practice-delete]")?.addEventListener("click", () => {
    void deleteWrongPoolPracticeSet(config, overlay);
  });
}

async function loadWrongQuestionPool(config, overlay) {
  config.loading = true;
  config.error = "";
  renderWrongQuestionPoolModal(overlay, config);
  const params = new URLSearchParams({
    user_id: currentMaterialsUserId(),
    subject: config.subject || "math",
    exam_type: config.examType || "",
    limit: "50",
  });
  if (config.topic) params.set("topic", config.topic);
  if (config.questionType) params.set("question_type", config.questionType);
  if (config.riskType) params.set("risk_type", config.riskType);
  try {
    const data = await fetchJson(`/api/materials/system/wrong-question-pool?${params.toString()}`);
    const pool = data.pool || {};
    config.items = Array.isArray(pool.items) ? pool.items : [];
    config.total = Number(pool.total || config.items.length || 0);
    config.topicOptions = Array.isArray(pool.topic_options) ? pool.topic_options : [];
    config.questionTypeOptions = Array.isArray(pool.question_type_options) ? pool.question_type_options : [];
    config.riskTypeOptions = Array.isArray(pool.risk_type_options) ? pool.risk_type_options : [];
    config.selectedIds = new Set(pool.default_selected_question_ids || []);
  } catch (error) {
    config.items = [];
    config.total = 0;
    config.selectedIds = new Set();
    config.riskTypeOptions = [];
    config.error = error.message;
  } finally {
    config.loading = false;
    renderWrongQuestionPoolModal(overlay, config);
  }
}

function openWrongQuestionPoolModal(options = {}) {
  const workflowOptions = options.returnToTopic
    ? {
        headerActionLabel: "返回",
        onHeaderAction: ({ close }) => {
          const topic = options.returnToTopic;
          close();
          openLearningTopicPanel(topic);
        },
      }
    : {};
  const { overlay } = createSystemWorkflowOverlay("错题池", "筛选错题，默认选择优先级最高的 5 道，生成可追踪的错题练习单。", workflowOptions);
  const config = {
    subject: options.subject || reviewTasksState.filters.subject || systemState.subject || "math",
    examType: options.examType || systemState.examType || "",
    topic: options.topic || "",
    questionType: options.questionType || "",
    riskType: options.riskType || "",
    items: [],
    total: 0,
    topicOptions: [],
    questionTypeOptions: [],
    riskTypeOptions: [],
    selectedIds: new Set(),
    loading: false,
    error: "",
    creating: false,
    createdPracticeSet: null,
  };
  renderWrongQuestionPoolModal(overlay, config);
  void loadWrongQuestionPool(config, overlay);
}

async function createWrongPoolPracticeSet(config, overlay) {
  const selectedItems = wrongPoolSelectedItems(config);
  if (!selectedItems.length) {
    setSystemSaveStatus("error", "请先选择要复习的错题。");
    return;
  }
  config.creating = true;
  renderWrongQuestionPoolModal(overlay, config);
  try {
    const payload = {
      question_ids: selectedItems.map((item) => item.question_id),
      title: "错题复习",
      subject: config.subject || "math",
      exam_type: config.examType || "",
      filters: {
        topic: config.topic || "",
        question_type: config.questionType || "",
        risk_type: config.riskType || "",
      },
    };
    const data = await fetchJson(`/api/materials/system/practice-sets/from-wrong-pool?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    config.createdPracticeSet = data.practice_set || data;
    setSystemSaveStatus("saved", "错题练习单已生成");
  } catch (error) {
    config.createdPracticeSet = null;
    setSystemSaveStatus("error", `错题练习单生成失败：${error.message}`);
  } finally {
    config.creating = false;
    renderWrongQuestionPoolModal(overlay, config);
  }
}

async function deleteWrongPoolPracticeSet(config, overlay) {
  const practiceSetId = systemPracticeSetId(config.createdPracticeSet);
  if (!practiceSetId) return;
  try {
    await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "DELETE",
    });
    config.createdPracticeSet = null;
    setSystemSaveStatus("saved", "错题练习单已删除");
    renderWrongQuestionPoolModal(overlay, config);
  } catch (error) {
    setSystemSaveStatus("error", `删除错题练习单失败：${error.message}`);
  }
}

function learningTopicByName(topicName) {
  const weakTopics = Array.isArray(reviewTasksState.learningInsights?.weak_topics)
    ? reviewTasksState.learningInsights.weak_topics
    : [];
  return weakTopics.find((item) => String(item.topic || "") === String(topicName || "")) || null;
}

function scrollReviewTaskListIntoView() {
  if (!reviewTaskList) return false;
  reviewTaskList.scrollIntoView({ behavior: "smooth", block: "start" });
  return true;
}

function openLearningTopicPanel(topicName) {
  const topic = learningTopicByName(topicName) || { topic: topicName };
  const title = String(topic.topic || "未命名知识点");
  const { overlay, close } = createSystemWorkflowOverlay("知识点处理", "从学习概览进入，先看原因，再选择错题、待核对或复习任务。");
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  body.innerHTML = `
    <section class="learning-topic-panel">
      <header>
        <div>
          <p class="eyebrow">Learning Topic</p>
          <h4>${escapeHtml(title)}</h4>
          <p>系统知识点内容暂未接入。当前先展示你的练习记录、风险原因和可执行入口。</p>
        </div>
        <span class="status-pill learning">优先级：${escapeHtml(learningPriorityLabel(topic.priority_score))}</span>
      </header>
      <div class="learning-topic-panel-grid">
        <div>
          <strong>练习记录</strong>
          <p>共练 ${escapeHtml(String(topic.attempt_count || 0))} 次，错题 ${escapeHtml(String(topic.wrong_count || 0))} 次，待核对 ${escapeHtml(String(topic.pending_review_count || 0))} 次，未答 ${escapeHtml(String(topic.unanswered_count || 0))} 次。</p>
          <p>判断可信度：${escapeHtml(learningConfidenceLabel(topic.confidence))}</p>
        </div>
        <div>
          <strong>处理原因</strong>
          ${learningTopicReasonTags(topic) || "<p>暂无明确风险原因。</p>"}
        </div>
      </div>
      <div class="system-workflow-actions">
        <button type="button" class="small-button dark-button" data-topic-panel-wrong>复习相关错题</button>
        <button type="button" class="small-button" data-topic-panel-pending>核对相关题</button>
        <button type="button" class="small-button" data-topic-panel-filter>筛选下方复习任务</button>
      </div>
    </section>
  `;
  body.querySelector("[data-topic-panel-wrong]")?.addEventListener("click", () => {
    close();
    openWrongQuestionPoolModal({ topic: title, riskType: "wrong", returnToTopic: title });
  });
  body.querySelector("[data-topic-panel-pending]")?.addEventListener("click", () => {
    close();
    openPendingReviewModal({ topic: title });
  });
  body.querySelector("[data-topic-panel-filter]")?.addEventListener("click", () => {
    close();
    if (reviewKeywordFilter) reviewKeywordFilter.value = title;
    reviewTasksState.filters.keyword = title;
    void loadReviewTasks().then(() => {
      scrollReviewTaskListIntoView();
    });
    setReviewTasksStatus("saved", `已在下方复习任务列表筛选「${title}」`);
  });
}

function pendingReviewItemTitle(item = {}) {
  return item.question_title || item.title || item.question_id || "待核对题目";
}

function pendingReviewAnswerTypeLabel(value = "") {
  if (value === "blank") return "填空题";
  if (value === "solution") return "解答题";
  return value || "待核对";
}

function pendingReviewManualConflictSources(item = {}, finalStatus = "") {
  const sources = [];
  const localStatus = String(item.local_status || "");
  const aiStatus = String(item.ai_status || "not_used");
  if (["correct", "incorrect", "partial"].includes(localStatus) && localStatus !== finalStatus) {
    sources.push("local");
  }
  if (["correct", "incorrect", "partial"].includes(aiStatus) && aiStatus !== finalStatus) {
    sources.push("ai");
  }
  return sources;
}

function pendingReviewStatusLabel(status = "") {
  if (status === "correct") return "正确";
  if (status === "incorrect") return "错误";
  if (status === "partial") return "部分正确";
  if (status === "pending_review") return "待核对";
  if (status === "unanswered") return "未作答";
  if (status === "not_used") return "未使用";
  return status || "未知";
}

function confirmPendingReviewManualGrade(item = {}, finalStatus = "") {
  const conflictSources = pendingReviewManualConflictSources(item, finalStatus);
  if (!conflictSources.length) return true;
  const sourceLabels = conflictSources.map((source) => (source === "ai" ? "AI 判分" : "本地判分")).join("、");
  const localStatus = pendingReviewStatusLabel(item.local_status || "");
  const aiStatus = pendingReviewStatusLabel(item.ai_status || "not_used");
  const finalLabel = pendingReviewStatusLabel(finalStatus);
  return window.confirm(
    `${sourceLabels}与本次人工确认不一致。\n\n本地判分：${localStatus}\nAI 判分：${aiStatus}\n人工确认：${finalLabel}\n\n仍然按人工确认保存吗？`
  );
}

function pendingReviewCorrectActionHtml(item = {}, attemptId = "", questionId = "") {
  const aiStatus = String(item.ai_status || "not_used");
  const safeAttemptId = escapeHtml(attemptId);
  const safeQuestionId = escapeHtml(questionId);
  if (aiStatus === "correct") {
    return `<button type="button" class="small-button" data-pending-review-correct data-attempt-id="${safeAttemptId}" data-question-id="${safeQuestionId}">采纳AI判定为正确</button>`;
  }
  if (aiStatus === "incorrect" || aiStatus === "partial") {
    return `<button type="button" class="small-button" data-pending-review-correct-override data-attempt-id="${safeAttemptId}" data-question-id="${safeQuestionId}">仍认为正确</button>`;
  }
  return "";
}

function renderPendingReviewItem(item) {
  const attemptId = item.attempt_id || "";
  const questionId = item.question_id || "";
  const topics = Array.isArray(item.topics) ? item.topics : [];
  const conflictSources = Array.isArray(item.manual_conflict_sources) ? item.manual_conflict_sources : [];
  const evidence = item.manual_evidence && typeof item.manual_evidence === "object" ? item.manual_evidence : {};
  return `
    <article class="pending-review-item">
      <header>
        <div>
          <strong>${escapeHtml(pendingReviewItemTitle(item))}</strong>
          <p>${escapeHtml(pendingReviewAnswerTypeLabel(item.answer_type))} · ${escapeHtml(topics.join(" / ") || "未标注知识点")}</p>
        </div>
        <span class="practice-result-status needs_review">待核对</span>
      </header>
      <div class="pending-review-answer-grid">
        <div>
          <strong>你的答案</strong>
          <div class="system-markdown">${renderSystemMarkdown(item.user_answer || "未作答")}</div>
        </div>
        <div>
          <strong>参考答案</strong>
          <div class="system-markdown">${renderSystemMarkdown(item.standard_answer || "暂无参考答案")}</div>
        </div>
      </div>
      ${conflictSources.length ? `
        <p class="practice-result-focus-message">上次人工确认与 ${escapeHtml(conflictSources.join(" / "))} 判分不一致；证据：本地 ${escapeHtml(pendingReviewStatusLabel(evidence.local_status || item.local_status || ""))}，AI ${escapeHtml(pendingReviewStatusLabel(evidence.ai_status || item.ai_status || "not_used"))}。</p>
      ` : ""}
      ${item.judge_reason ? `<p class="practice-result-feedback">${escapeHtml(String(item.judge_reason))}</p>` : ""}
      <div class="pending-review-actions">
        <button type="button" class="small-button" data-pending-review-open="${escapeHtml(questionId)}">查看题目</button>
        <button type="button" class="small-button" data-pending-review-ai data-attempt-id="${escapeHtml(attemptId)}" data-question-id="${escapeHtml(questionId)}">AI 判分</button>
        ${pendingReviewCorrectActionHtml(item, attemptId, questionId)}
        <button type="button" class="small-button" data-pending-review-incorrect data-attempt-id="${escapeHtml(attemptId)}" data-question-id="${escapeHtml(questionId)}">确认错误</button>
      </div>
    </article>
  `;
}

function renderPendingReviewModal(overlay, config) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const topicOptions = Array.isArray(config.topicOptions) ? config.topicOptions : [];
  body.innerHTML = `
    <div class="workflow-form-grid">
      <label class="field">
        <span>题库范围</span>
        <select data-pending-review-exam-type>
          <option value="" ${config.examType ? "" : "selected"}>全部数学题库</option>
          <option value="math1" ${config.examType === "math1" ? "selected" : ""}>数学一真题</option>
          <option value="math2" ${config.examType === "math2" ? "selected" : ""}>数学二真题</option>
          <option value="math3" ${config.examType === "math3" ? "selected" : ""}>数学三真题</option>
        </select>
      </label>
      <label class="field">
        <span>知识点</span>
        <select data-pending-review-topic>
          <option value="" ${config.topic ? "" : "selected"}>全部知识点</option>
          ${topicOptions.map((topic) => `<option value="${escapeHtml(topic)}" ${config.topic === topic ? "selected" : ""}>${escapeHtml(topic)}</option>`).join("")}
        </select>
      </label>
    </div>
    <section class="system-workflow-section">
      <div class="wrong-pool-summary">
        <div>
          <h4>待核对名单</h4>
          <p>${config.loading ? "正在读取待核对题..." : `共 ${Number(config.total || 0)} 道需要核对的非选择题。`}</p>
        </div>
      </div>
      ${config.error ? `<p class="helper-text error-text">${escapeHtml(config.error)}</p>` : ""}
      ${config.loading ? `
        <div class="empty-state">正在加载待核对名单...</div>
      ` : config.items.length ? `
        <div class="pending-review-list">
          ${config.items.map(renderPendingReviewItem).join("")}
        </div>
      ` : `
        <div class="empty-state">当前筛选下没有待核对题。</div>
      `}
    </section>
  `;
  body.querySelector("[data-pending-review-exam-type]")?.addEventListener("change", (event) => {
    config.examType = event.target.value || "";
    void loadPendingReviewItems(config, overlay);
  });
  body.querySelector("[data-pending-review-topic]")?.addEventListener("change", (event) => {
    config.topic = event.target.value || "";
    void loadPendingReviewItems(config, overlay);
  });
  body.querySelectorAll("[data-pending-review-open]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.pendingReviewOpen || "";
      if (questionId) void openSystemQuestionDrawer(questionId);
    });
  });
  body.querySelectorAll("[data-pending-review-ai], [data-pending-review-correct], [data-pending-review-correct-override], [data-pending-review-incorrect]").forEach((button) => {
    button.addEventListener("click", () => {
      const method = button.dataset.pendingReviewAi !== undefined ? "ai" : "manual";
      const finalStatus = button.dataset.pendingReviewCorrect !== undefined || button.dataset.pendingReviewCorrectOverride !== undefined
        ? "correct"
        : (button.dataset.pendingReviewIncorrect !== undefined ? "incorrect" : "");
      const item = config.items.find((candidate) => (
        String(candidate.attempt_id || "") === String(button.dataset.attemptId || "")
        && String(candidate.question_id || "") === String(button.dataset.questionId || "")
      )) || {};
      if (button.dataset.pendingReviewCorrectOverride !== undefined) {
        const reason = window.prompt("AI/本地判分不支持正确，请写一句你认为正确的理由：", "");
        if (!reason || !reason.trim()) {
          return;
        }
        button.dataset.judgeReason = `人工仍认为正确：${reason.trim()}`;
      } else {
        delete button.dataset.judgeReason;
      }
      if (method === "manual" && !confirmPendingReviewManualGrade(item, finalStatus)) {
        return;
      }
      void gradePendingReviewItem(config, overlay, button, method, finalStatus);
    });
  });
}

async function loadPendingReviewItems(config, overlay) {
  config.loading = true;
  config.error = "";
  renderPendingReviewModal(overlay, config);
  const params = new URLSearchParams({
    user_id: currentMaterialsUserId(),
    subject: config.subject || "math",
    exam_type: config.examType || "",
    limit: "50",
  });
  if (config.topic) params.set("topic", config.topic);
  try {
    const data = await fetchJson(`/api/materials/system/pending-review-items?${params.toString()}`);
    const pendingReview = data.pending_review || {};
    config.items = Array.isArray(pendingReview.items) ? pendingReview.items : [];
    config.total = Number(pendingReview.total || config.items.length || 0);
    config.topicOptions = Array.isArray(pendingReview.topic_options) ? pendingReview.topic_options : [];
  } catch (error) {
    config.items = [];
    config.total = 0;
    config.topicOptions = [];
    config.error = error.message;
  } finally {
    config.loading = false;
    renderPendingReviewModal(overlay, config);
  }
}

function openPendingReviewModal(options = {}) {
  const { overlay } = createSystemWorkflowOverlay("待核对名单", "只列出需要人工或 AI 判分的非选择题。选择题按标准答案自动判分，不进入这里。");
  const config = {
    subject: options.subject || reviewTasksState.filters.subject || systemState.subject || "math",
    examType: options.examType || systemState.examType || "",
    topic: options.topic || "",
    items: [],
    total: 0,
    topicOptions: [],
    loading: false,
    error: "",
  };
  renderPendingReviewModal(overlay, config);
  void loadPendingReviewItems(config, overlay);
}

async function gradePendingReviewItem(config, overlay, button, judgeMethod, finalStatus) {
  const attemptId = button?.dataset.attemptId || "";
  const questionId = button?.dataset.questionId || "";
  if (!attemptId || !questionId || button.disabled) return;
  const judgeReason = button?.dataset.judgeReason
    || (finalStatus === "correct" ? "人工确认正确。" : "人工确认错误。");
  const originalText = button.textContent;
  button.disabled = true;
  button.classList.add("is-loading");
  button.setAttribute("aria-busy", "true");
  button.textContent = judgeMethod === "ai" ? "正在评分..." : "正在确认...";
  try {
    const payload = judgeMethod === "ai"
      ? { judge_method: "ai" }
      : {
          judge_method: "manual",
          final_status: finalStatus,
          judge_confidence: 1,
          judge_reason: judgeReason,
          manual_override: true,
        };
    await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/items/${encodeURIComponent(questionId)}/grade?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    setSystemSaveStatus("saved", "待核对结果已更新");
    await loadPendingReviewItems(config, overlay);
    await loadReviewLearningInsights({ silent: true });
    await loadReviewTasks({ silent: true });
  } catch (error) {
    button.disabled = false;
    button.classList.remove("is-loading");
    button.removeAttribute("aria-busy");
    button.textContent = originalText;
    setSystemSaveStatus("error", `待核对更新失败：${error.message}`);
  }
}

function practiceSetQuestionIds(practiceSet = {}, fallbackQuestions = []) {
  const ids = Array.isArray(practiceSet.question_ids) ? practiceSet.question_ids : [];
  const fallbackIds = Array.isArray(fallbackQuestions)
    ? fallbackQuestions.map((item) => item.question_id).filter(Boolean)
    : [];
  return [...new Set([...ids, ...fallbackIds].map((id) => String(id)).filter(Boolean))];
}

function practiceAttemptId(practiceAttempt = {}) {
  return practiceAttempt.practice_attempt_id || practiceAttempt.attempt_id || practiceAttempt.id || "";
}

function latestSubmittedPracticeAttempt(practiceAttempts = []) {
  const attempts = Array.isArray(practiceAttempts) ? practiceAttempts : [];
  return attempts
    .filter((attempt) => attempt && (attempt.status === "submitted" || attempt.submitted_at))
    .sort((left, right) => String(right.submitted_at || right.started_at || "").localeCompare(String(left.submitted_at || left.started_at || "")))[0] || null;
}

function practiceAttemptSummaryText(practiceAttempt = {}) {
  const summary = practiceAttempt.summary || {};
  const total = Number(summary.total || 0);
  const correct = Number(summary.correct || 0);
  const incorrect = Number(summary.incorrect || 0);
  const pending = Number(summary.pending_review || summary.needs_review || 0);
  if (!total) {
    return "暂无可汇总结果";
  }
  return `${total} 题 · 正确 ${correct} · 错误 ${incorrect} · 待核对 ${pending}`;
}

function practiceQuestionAnswerType(question = {}) {
  const type = String(question.question_type || question.question_type_label || "").toLowerCase();
  if (type.includes("choice") || type.includes("选择")) return "choice";
  if (type.includes("blank") || type.includes("fill") || type.includes("填空")) return "blank";
  return "solution";
}

function practiceAnswerTextValue(value = "") {
  if (value == null) {
    return "";
  }
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (typeof value === "object") {
    if (Object.prototype.hasOwnProperty.call(value, "value")) {
      return practiceAnswerTextValue(value.value);
    }
    if (Object.prototype.hasOwnProperty.call(value, "text")) {
      return practiceAnswerTextValue(value.text);
    }
    if (Object.prototype.hasOwnProperty.call(value, "content")) {
      return practiceAnswerTextValue(value.content);
    }
    if (Object.prototype.hasOwnProperty.call(value, "markdown")) {
      return practiceAnswerTextValue(value.markdown);
    }
    if (Object.prototype.hasOwnProperty.call(value, "answer")) {
      return practiceAnswerTextValue(value.answer);
    }
    return "";
  }
  return String(value);
}

function practiceAnswerValue(answer = {}) {
  if (answer && typeof answer === "object") {
    if (Object.prototype.hasOwnProperty.call(answer, "value")) {
      return practiceAnswerTextValue(answer.value);
    }
    if (Object.prototype.hasOwnProperty.call(answer, "text")) {
      return practiceAnswerTextValue(answer.text);
    }
    if (Object.prototype.hasOwnProperty.call(answer, "content")) {
      return practiceAnswerTextValue(answer.content);
    }
    if (Object.prototype.hasOwnProperty.call(answer, "markdown")) {
      return practiceAnswerTextValue(answer.markdown);
    }
    if (Object.prototype.hasOwnProperty.call(answer, "answer")) {
      return practiceAnswerTextValue(answer.answer);
    }
    return "";
  }
  return practiceAnswerTextValue(answer);
}

function practiceAttemptAnswers(practiceAttempt = {}) {
  return practiceAttempt.answers && typeof practiceAttempt.answers === "object" ? practiceAttempt.answers : {};
}

function mergePracticeAttempt(previousAttempt = {}, nextAttempt = {}) {
  const merged = { ...previousAttempt, ...nextAttempt };
  merged.answers = {
    ...practiceAttemptAnswers(previousAttempt),
    ...practiceAttemptAnswers(nextAttempt),
  };
  return merged;
}

function practiceAttemptResultForQuestion(practiceAttempt = {}, questionId) {
  const results = practiceAttempt.results || practiceAttempt.question_results || practiceAttempt.grading || {};
  if (Array.isArray(results)) {
    return results.find((item) => item.question_id === questionId) || {};
  }
  return results[questionId] || {};
}

function practiceAttemptFinalStatus(result = {}) {
  return result.final_status || result.result || result.status || result.correctness || "unknown";
}

function practiceAttemptResultLabel(result = {}) {
  const value = practiceAttemptFinalStatus(result);
  const labels = {
    correct: "正确",
    incorrect: "错误",
    partial: "部分正确",
    pending: "待批改",
    pending_review: "待核对",
    needs_review: "待核对",
    needs_grading: "待评分",
    unanswered: "未作答",
    unknown: "待批改",
  };
  return labels[value] || result.label || value || "待批改";
}

function practiceResultStatusClass(result = {}) {
  const value = practiceAttemptFinalStatus(result);
  const classes = {
    correct: "practice-result-status correct",
    incorrect: "practice-result-status incorrect",
    partial: "practice-result-status needs_review",
    pending: "practice-result-status needs_review",
    pending_review: "practice-result-status needs_review",
    needs_review: "practice-result-status needs_review",
    needs_grading: "practice-result-status needs_grading",
    unanswered: "practice-result-status unanswered",
    unknown: "practice-result-status unknown",
  };
  return classes[value] || "practice-result-status unknown";
}

function practiceQuestionStandardAnswer(question = {}, result = {}) {
  return (
    result.standard_answer
    || result.answer
    || question.answer_markdown
    || question.answer
    || question.standard_answer
    || question.correct_answer
    || ""
  );
}

function practiceResultCanUseAiGrade(question = {}, result = {}) {
  const answerType = result.answer_type || practiceQuestionAnswerType(question);
  const finalStatus = practiceAttemptFinalStatus(result);
  return ["blank", "solution"].includes(answerType) && finalStatus !== "unanswered";
}

function practiceResultFeedbackMarkdown(result = {}) {
  return [
    result.judge_reason,
    result.ai_feedback ? `AI 反馈：${result.ai_feedback}` : "",
  ].filter(Boolean).join("\n\n");
}

const PRACTICE_CHOICE_KEYS = ["A", "B", "C", "D"];

function normalizePracticeChoiceText(value = "") {
  return String(value || "")
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .join(" ")
    .replace(/\s+/g, " ")
    .replace(/\$\s+/g, "$")
    .replace(/\s+\$/g, "$")
    .trim();
}

function findPracticeChoiceMarkers(markdown = "") {
  const text = String(markdown || "").replace(/\r\n?/g, "\n");
  const markers = [];
  const pattern = /(^|[\s(（])([A-D])[\.\uFF0E、]\s*/g;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    const prefix = String(match[1] || "");
    const key = String(match[2] || "").toUpperCase();
    const markerStart = match.index + prefix.length;
    const contentStart = match.index + String(match[0] || "").length;
    markers.push({ key, markerStart, contentStart });
  }
  return markers;
}

function orderedPracticeChoiceMarkers(markers = []) {
  for (let startIndex = 0; startIndex < markers.length; startIndex += 1) {
    if (markers[startIndex].key !== "A") continue;
    const sequence = [markers[startIndex]];
    let expectedIndex = 1;
    for (let index = startIndex + 1; index < markers.length && expectedIndex < PRACTICE_CHOICE_KEYS.length; index += 1) {
      if (markers[index].key === PRACTICE_CHOICE_KEYS[expectedIndex]) {
        sequence.push(markers[index]);
        expectedIndex += 1;
      }
    }
    if (sequence.length >= 2) {
      return sequence;
    }
  }
  return [];
}

function practiceChoiceOptionEnd(text, fallbackEnd) {
  const source = String(text || "");
  const tail = source.slice(fallbackEnd);
  const sectionMatch = tail.match(/\n\s*(?:答案|解析|【答案】|【解析】|#{1,6}\s+)/);
  return sectionMatch ? fallbackEnd + sectionMatch.index : source.length;
}

function parsePracticeChoiceOptionsFromMarkdown(markdown = "") {
  const text = String(markdown || "").replace(/\r\n?/g, "\n");
  const markers = orderedPracticeChoiceMarkers(findPracticeChoiceMarkers(text));
  if (markers.length < 2) {
    return [];
  }
  return markers
    .map((marker, index) => {
      const end = index + 1 < markers.length
        ? markers[index + 1].markerStart
        : practiceChoiceOptionEnd(text, marker.contentStart);
      return {
        key: marker.key,
        text: normalizePracticeChoiceText(text.slice(marker.contentStart, end)),
      };
    })
    .filter((item) => item.key && item.text);
}

function practiceChoiceOptions(question = {}) {
  const explicitOptions = Array.isArray(question.choice_options) && question.choice_options.length
    ? question.choice_options
    : [];
  if (explicitOptions.length) {
    return explicitOptions.map((item, index) => {
      if (item && typeof item === "object") {
        const key = String(item.value || item.key || item.label || String.fromCharCode(65 + index)).slice(0, 1).toUpperCase();
        const text = normalizePracticeChoiceText(item.text || item.content || item.markdown || item.label || key);
        return { key, text };
      }
      const raw = String(item || "").trim();
      const match = raw.match(/^([A-D])[\.\uff0e、\s]*(.*)$/i);
      const key = (match?.[1] || String.fromCharCode(65 + index)).toUpperCase();
      return { key, text: normalizePracticeChoiceText(match?.[2] || raw || key) };
    });
  }

  const markdown = String(question.question_markdown || question.preview || "");
  const inlineParsed = parsePracticeChoiceOptionsFromMarkdown(markdown);
  if (inlineParsed.length >= 2) {
    return inlineParsed;
  }
  const matches = [...markdown.matchAll(/(?:^|\n)\s*([A-D])[\.\uff0e、]\s*([\s\S]*?)(?=\n\s*[A-D][\.\uff0e、]\s*|\n\s*##\s+|\s*$)/gi)];
  const parsed = matches
    .map((match) => ({
      key: String(match[1] || "").toUpperCase(),
      text: normalizePracticeChoiceText(match[2] || ""),
    }))
    .filter((item) => item.key && item.text);
  if (parsed.length >= 2) {
    return parsed;
  }
  return ["A", "B", "C", "D"].map((key) => ({ key, text: key }));
}

function renderPracticeAnswerInput(question = {}, savedAnswer = {}) {
  const questionId = question.question_id || "";
  const answerType = savedAnswer.answer_type || practiceQuestionAnswerType(question);
  const value = practiceAnswerValue(savedAnswer);
  const data = `data-practice-answer-input data-question-id="${escapeHtml(questionId)}" data-answer-type="${escapeHtml(answerType)}"`;
  if (answerType === "choice") {
    return `
      <div class="practice-choice-group" role="radiogroup" aria-label="选择题答案">
        ${practiceChoiceOptions(question).map((option) => `
          <label class="practice-choice-option ${value === option.key ? "selected" : ""}">
            <input type="radio" name="practice-answer-${escapeHtml(questionId)}" value="${escapeHtml(option.key)}" ${data} ${value === option.key ? "checked" : ""}>
            <span class="practice-choice-option-key">${escapeHtml(option.key)}</span>
            <span class="practice-choice-option-content system-markdown">${renderSystemMarkdown(option.text || option.key)}</span>
          </label>
        `).join("")}
      </div>
    `;
  }
  if (answerType === "blank") {
    return `<input type="text" class="practice-fill-input" value="${escapeHtml(value)}" placeholder="输入填空答案" ${data}>`;
  }
  return `<textarea class="practice-solution-input" rows="6" placeholder="写下解题步骤或关键思路" ${data}>${escapeHtml(value)}</textarea>`;
}

function practiceSetCurrentQuestionIndex(questionIds = [], options = {}) {
  if (!questionIds.length) return 0;
  const rawIndex = Number(options.currentQuestionIndex || 0);
  if (!Number.isFinite(rawIndex)) return 0;
  return Math.min(Math.max(Math.trunc(rawIndex), 0), questionIds.length - 1);
}

function isPracticeQuestionDetailReady(question = {}) {
  return Boolean(
    question?.question_markdown
    || question?.answer_markdown
    || question?.explanation_markdown
    || (Array.isArray(question?.asset_urls) && question.asset_urls.length)
  );
}

async function resolvePracticeAttemptQuestions(practiceSet, questions = [], options = {}) {
  const fallbackQuestions = options.fallbackQuestions || [];
  const questionIds = practiceSetQuestionIds(practiceSet, fallbackQuestions);
  const providedQuestions = new Map(
    [...fallbackQuestions, ...questions]
      .filter((question) => question?.question_id)
      .map((question) => [question.question_id, question])
  );

  return Promise.all(questionIds.map(async (questionId) => {
    const existing = providedQuestions.get(questionId) || { question_id: questionId };
    if (isPracticeQuestionDetailReady(existing)) {
      return existing;
    }
    try {
      const detail = await fetchJson(systemQuestionDetailUrl(questionId));
      return { ...existing, ...detail };
    } catch {
      return existing;
    }
  }));
}

function renderPracticeAttemptDraft(overlay, practiceSet, questions = [], practiceAttempt = {}, options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const fallbackQuestions = options.fallbackQuestions || [];
  const questionIds = practiceSetQuestionIds(practiceSet, fallbackQuestions);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const answers = practiceAttemptAnswers(practiceAttempt);
  const answeredCount = questionIds.filter((questionId) => practiceAnswerValue(answers[questionId]).trim()).length;
  const currentQuestionIndex = practiceSetCurrentQuestionIndex(questionIds, options);
  const currentQuestionId = questionIds[currentQuestionIndex] || "";
  const currentQuestion = questionMap.get(currentQuestionId)
    || fallbackQuestions.find((item) => item.question_id === currentQuestionId)
    || { question_id: currentQuestionId };
  const currentTopics = Array.isArray(currentQuestion.topics) ? currentQuestion.topics.join(" / ") : "";
  const title = practiceSet.title || practiceSet.name || "同类训练练习单";
  body.innerHTML = `
    <section class="system-workflow-result practice-attempt-head" data-practice-current-index="${currentQuestionIndex}">
      <div>
        <strong>${escapeHtml(title)}</strong>
        <p>第 ${questionIds.length ? currentQuestionIndex + 1 : 0}/${questionIds.length} 题 · ${answeredCount}/${questionIds.length} 已答 · 草稿会自动保存</p>
      </div>
    </section>
    <section class="practice-attempt-layout">
      <div class="practice-attempt-paper">
        ${questionIds.length ? `
          <article class="practice-paper-question current" id="practice-question-${escapeHtml(currentQuestionId)}">
            <div class="practice-paper-question-head">
              <div>
                <strong>${currentQuestionIndex + 1}. ${escapeHtml(systemQuestionTitle(currentQuestion) || currentQuestionId)}</strong>
                <p>${escapeHtml([currentQuestion.question_type_label || currentQuestion.question_type, currentQuestion.library_name, currentTopics].filter(Boolean).join(" · ") || currentQuestionId)}</p>
              </div>
            </div>
            <div class="practice-paper-question-body">
              ${currentQuestion.question_id ? renderPracticeQuestionMarkdown(currentQuestion) : `<p>${escapeHtml(currentQuestionId)}</p>`}
            </div>
            <div class="practice-answer-card">
              <h4>我的答案</h4>
              ${renderPracticeAnswerInput(currentQuestion, answers[currentQuestionId] || {})}
            </div>
          </article>
        ` : '<div class="empty-state">这张练习单暂时没有题目。</div>'}
      </div>
      <aside class="practice-answer-sheet" aria-label="答题卡">
        <div>
          <strong>答题卡</strong>
          <p>${answeredCount}/${questionIds.length} 已答</p>
        </div>
        <div class="practice-answer-nav">
          ${questionIds.map((questionId, index) => `
            <button type="button" class="practice-answer-nav-button ${practiceAnswerValue(answers[questionId]).trim() ? "answered" : ""} ${index === currentQuestionIndex ? "current" : ""}" data-practice-card-link="${index}" data-question-id="${escapeHtml(questionId)}">${index + 1}</button>
          `).join("")}
        </div>
      </aside>
    </section>
    <section class="system-workflow-result practice-attempt-submit-bar">
      <div>
        <strong>完成作答后提交</strong>
        <p>提交后会核对选择题和可判定填空题，解答题标记为待核对。</p>
      </div>
      <div class="practice-attempt-page-actions">
        <button type="button" class="small-button" data-practice-prev ${currentQuestionIndex <= 0 ? "disabled" : ""}>上一题</button>
        <button type="button" class="small-button" data-practice-next ${currentQuestionIndex >= questionIds.length - 1 ? "disabled" : ""}>下一题</button>
        <button type="button" class="small-button dark-button" data-practice-attempt-submit>提交练习</button>
      </div>
    </section>
  `;

  let saveTimer = 0;
  const collectAnswers = () => {
    const nextAnswers = { ...practiceAttemptAnswers(practiceAttempt) };
    body.querySelectorAll("[data-practice-answer-input]").forEach((input) => {
      if (input.type === "radio" && !input.checked) return;
      const questionId = input.dataset.questionId;
      if (!questionId) return;
      nextAnswers[questionId] = {
        answer_type: input.dataset.answerType || "solution",
        value: input.value || "",
      };
    });
    practiceAttempt.answers = nextAnswers;
    return nextAnswers;
  };
  const scheduleSave = () => {
    const nextAnswers = collectAnswers();
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(() => {
      void savePracticeAttemptAnswers(practiceAttempt, nextAnswers)
        .then((savedAttempt) => {
          if (savedAttempt) practiceAttempt = savedAttempt;
          renderPracticeAttemptDraft(overlay, practiceSet, questions, practiceAttempt, options);
        });
    }, 320);
  };
  body.querySelectorAll("[data-practice-answer-input]").forEach((input) => {
    input.addEventListener(input.type === "radio" ? "change" : "input", scheduleSave);
  });
  const saveAndRenderQuestion = (nextIndex) => {
    const clampedIndex = practiceSetCurrentQuestionIndex(questionIds, { currentQuestionIndex: nextIndex });
    const nextAnswers = collectAnswers();
    void savePracticeAttemptAnswers(practiceAttempt, nextAnswers)
      .then((savedAttempt) => {
        if (savedAttempt) practiceAttempt = savedAttempt;
        renderPracticeAttemptDraft(overlay, practiceSet, questions, practiceAttempt, { ...options, currentQuestionIndex: clampedIndex });
      });
  };
  body.querySelectorAll("[data-practice-card-link]").forEach((button) => {
    button.addEventListener("click", () => {
      saveAndRenderQuestion(Number(button.dataset.practiceCardLink || 0));
    });
  });
  body.querySelector("[data-practice-prev]")?.addEventListener("click", () => {
    saveAndRenderQuestion(currentQuestionIndex - 1);
  });
  body.querySelector("[data-practice-next]")?.addEventListener("click", () => {
    saveAndRenderQuestion(currentQuestionIndex + 1);
  });
  body.querySelector("[data-practice-attempt-submit]")?.addEventListener("click", () => {
    const nextAnswers = collectAnswers();
    const unansweredCount = questionIds.filter((questionId) => !practiceAnswerValue(nextAnswers[questionId]).trim()).length;
    if (unansweredCount > 0 && !window.confirm(`还有 ${unansweredCount} 题未作答，确认提交吗？`)) {
      return;
    }
    void savePracticeAttemptAnswers(practiceAttempt, nextAnswers)
      .then((savedAttempt) => submitPracticeAttempt(savedAttempt || practiceAttempt, overlay, practiceSet, questions, options));
  });
}

function renderPracticeAttemptResult(overlay, practiceSet, questions = [], practiceAttempt = {}, options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const fallbackQuestions = options.fallbackQuestions || [];
  const questionIds = practiceSetQuestionIds(practiceSet, fallbackQuestions);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const answers = practiceAttemptAnswers(practiceAttempt);
  const title = practiceSet.title || practiceSet.name || "同类训练练习单";
  body.innerHTML = `
    <section class="system-workflow-result practice-attempt-head">
      <div>
        <strong>${escapeHtml(title)} · 结果</strong>
        <p>本次练习已提交，记录不可修改。</p>
      </div>
      <div class="system-workflow-result-actions">
        <button type="button" class="small-button" data-practice-retry-placeholder>再次练习</button>
      </div>
    </section>
    ${renderPracticeAttemptInsights(practiceAttempt)}
    <div class="practice-result-focus-message" data-practice-result-focus-message hidden></div>
    <section class="practice-result-table" aria-label="练习结果">
      ${questionIds.map((questionId, index) => {
        const question = questionMap.get(questionId) || fallbackQuestions.find((item) => item.question_id === questionId) || { question_id: questionId };
        const result = practiceAttemptResultForQuestion(practiceAttempt, questionId);
        const userAnswer = practiceAnswerValue(answers[questionId]);
        const standardAnswer = practiceQuestionStandardAnswer(question, result);
        const feedback = practiceResultFeedbackMarkdown(result);
        const finalStatus = practiceAttemptFinalStatus(result);
        const topics = Array.isArray(question.topics) ? question.topics.map((topic) => String(topic || "")) : [];
        const personal = systemUserState(questionId);
        const nextMastery = personal.mastery_status === "mastered" ? "learning" : "mastered";
        return `
          <article
            class="practice-result-row"
            data-practice-result-row
            data-practice-result-question-id="${escapeHtml(questionId)}"
            data-practice-result-status="${escapeHtml(finalStatus)}"
            data-practice-result-topics="${escapeHtml(topics.join("||"))}"
          >
            <header>
              <strong>${index + 1}. ${escapeHtml(systemQuestionTitle(question) || questionId)}</strong>
              <div class="practice-result-row-head-actions">
                <span class="${escapeHtml(practiceResultStatusClass(result))}">${escapeHtml(practiceAttemptResultLabel(result))}</span>
                <details class="practice-question-menu practice-result-menu" data-practice-result-menu>
                  <summary aria-label="单题操作">...</summary>
                  <div class="practice-question-menu-panel">
                    <button type="button" class="small-button" data-practice-result-toggle-favorite="${escapeHtml(questionId)}">${personal.is_favorite ? "取消收藏" : "收藏"}</button>
                    <button type="button" class="small-button" data-practice-result-toggle-wrong="${escapeHtml(questionId)}">${personal.in_wrong_book ? "移出错题" : "加入错题"}</button>
                    <button type="button" class="small-button" data-practice-result-toggle-mastery="${escapeHtml(questionId)}" data-next-mastery="${escapeHtml(nextMastery)}">${personal.mastery_status === "mastered" ? "改为学习中" : "标记已掌握"}</button>
                    <button type="button" class="small-button" data-practice-result-add-review="${escapeHtml(questionId)}">加入复习规划</button>
                  </div>
                </details>
              </div>
            </header>
            <div class="practice-result-columns">
              <div>
                <h4>你的答案</h4>
                <div class="system-markdown">${renderSystemMarkdown(userAnswer || "未作答")}</div>
              </div>
              <div>
                <h4>标准答案</h4>
                <div class="system-markdown">${renderSystemMarkdown(standardAnswer || "暂无标准答案")}</div>
              </div>
            </div>
            ${feedback ? `<div class="practice-result-feedback system-markdown">${renderSystemMarkdown(feedback)}</div>` : ""}
            <div class="practice-result-actions">
              <button type="button" class="small-button" data-practice-result-question="${escapeHtml(questionId)}">查看题目详情</button>
              ${practiceResultCanUseAiGrade(question, result) ? `<button type="button" class="small-button" data-practice-ai-grade="${escapeHtml(questionId)}">AI 判分</button>` : ""}
            </div>
          </article>
        `;
      }).join("") || '<div class="empty-state">本次练习暂无结果。</div>'}
    </section>
  `;
  if (Number.isFinite(options.restoreScrollTop)) {
    restoreWorkflowBodyScroll(body, options.restoreScrollTop);
  } else {
    body.scrollTop = 0;
  }
  body.querySelector("[data-practice-retry-placeholder]")?.addEventListener("click", () => {
    window.alert("再次练习将在后续版本开放");
  });
  body.querySelectorAll("[data-practice-next-action]").forEach((button) => {
    button.addEventListener("click", () => {
      applyPracticeResultFocus(body, {
        type: button.dataset.practiceNextAction || "",
        status: button.dataset.practiceNextStatus || "",
        topic: button.dataset.practiceNextTopic || "",
      });
    });
  });
  body.querySelectorAll("[data-practice-result-question]").forEach((button) => {
    button.addEventListener("click", () => {
      closeSystemWorkflowModal();
      setActivePage("materials");
      setMaterialsMode(MATERIALS_MODE_SYSTEM, { skipRefreshWhenCurrent: true });
      void openSystemQuestionDrawer(button.dataset.practiceResultQuestion);
    });
  });
  body.querySelectorAll("[data-practice-ai-grade]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.practiceAiGrade;
      const question = questionMap.get(questionId)
        || fallbackQuestions.find((item) => item.question_id === questionId)
        || { question_id: questionId };
      void requestPracticeAiGrade(practiceAttempt, question, overlay, practiceSet, questions, options, button);
    });
  });
  body.querySelectorAll("[data-practice-result-toggle-favorite]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.practiceResultToggleFavorite || "";
      const personal = systemUserState(questionId);
      void savePracticeResultQuestionState(questionId, { is_favorite: !personal.is_favorite }, overlay, practiceSet, questions, practiceAttempt, options);
    });
  });
  body.querySelectorAll("[data-practice-result-toggle-wrong]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.practiceResultToggleWrong || "";
      const personal = systemUserState(questionId);
      void savePracticeResultQuestionState(questionId, { in_wrong_book: !personal.in_wrong_book }, overlay, practiceSet, questions, practiceAttempt, options);
    });
  });
  body.querySelectorAll("[data-practice-result-toggle-mastery]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.practiceResultToggleMastery || "";
      const masteryStatus = button.dataset.nextMastery || "mastered";
      void savePracticeResultQuestionState(questionId, { mastery_status: masteryStatus }, overlay, practiceSet, questions, practiceAttempt, options);
    });
  });
  body.querySelectorAll("[data-practice-result-add-review]").forEach((button) => {
    button.addEventListener("click", () => {
      const questionId = button.dataset.practiceResultAddReview || "";
      const question = questionMap.get(questionId)
        || fallbackQuestions.find((item) => item.question_id === questionId)
        || { question_id: questionId };
      openSystemReviewModal(question);
    });
  });
}

function applyPracticeResultFocus(body, action = {}) {
  if (!body) return;
  const rows = Array.from(body.querySelectorAll("[data-practice-result-row]"));
  const status = action.status || "";
  const topic = action.topic || "";
  let matched = rows;
  if (status) {
    const acceptedStatuses = status === "incorrect" ? ["incorrect", "partial"] : [status];
    matched = rows.filter((row) => acceptedStatuses.includes(row.dataset.practiceResultStatus || ""));
  }
  if (topic) {
    matched = rows.filter((row) => (row.dataset.practiceResultTopics || "").split("||").includes(topic));
  }
  rows.forEach((row) => {
    const isMatch = matched.includes(row);
    row.classList.toggle("is-emphasized", isMatch && matched.length > 0);
    row.classList.toggle("is-dimmed", !isMatch && matched.length > 0);
  });
  const message = body.querySelector("[data-practice-result-focus-message]");
  if (message) {
    message.hidden = false;
    message.textContent = matched.length
      ? `已定位 ${matched.length} 道相关题`
      : "当前结果里暂无匹配题目";
  }
  matched[0]?.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function savePracticeResultQuestionState(questionId, patch, overlay, practiceSet, questions = [], practiceAttempt = {}, options = {}) {
  if (!questionId) return;
  const body = overlay?.querySelector(".system-workflow-body");
  const currentScrollTop = body ? body.scrollTop : 0;
  const previousState = { ...systemUserState(questionId) };
  updateSystemQuestionPersonalState(questionId, patch);
  renderPracticeAttemptResult(overlay, practiceSet, questions, practiceAttempt, {
    ...options,
    restoreScrollTop: currentScrollTop,
  });
  try {
    await saveSystemQuestionState(questionId, patch, {
      renderDrawer: false,
      userId: currentMaterialsUserId(),
    });
  } catch (error) {
    hydrateSystemQuestionPersonalState(questionId, previousState);
    renderPracticeAttemptResult(overlay, practiceSet, questions, practiceAttempt, {
      ...options,
      restoreScrollTop: currentScrollTop,
    });
    handleSystemQuestionStateSaveError(questionId, error, previousState);
  }
}

function restoreWorkflowBodyScroll(body, scrollTop) {
  if (!body || !Number.isFinite(scrollTop)) return;
  window.requestAnimationFrame(() => {
    body.scrollTop = scrollTop;
  });
}

function setPracticeAiGradeButtonLoading(button, loading) {
  if (!button) return;
  if (loading) {
    button.dataset.originalLabel = button.textContent || "AI 判分";
    button.textContent = "正在评分...";
    button.disabled = true;
    button.classList.add("is-loading");
    button.setAttribute("aria-busy", "true");
    return;
  }
  button.textContent = button.dataset.originalLabel || "AI 判分";
  button.disabled = false;
  button.classList.remove("is-loading");
  button.removeAttribute("aria-busy");
}

function renderPracticeAttemptInsights(practiceAttempt = {}) {
  const insights = practiceAttempt.insights && typeof practiceAttempt.insights === "object"
    ? practiceAttempt.insights
    : {};
  const summary = insights.summary && typeof insights.summary === "object" ? insights.summary : {};
  const topicImpacts = Array.isArray(insights.topic_impacts) ? insights.topic_impacts : [];
  const questionImpacts = Array.isArray(insights.question_impacts) ? insights.question_impacts : [];
  const nextActions = Array.isArray(insights.next_actions) ? insights.next_actions : [];
  const hasRecord = insights.record_status || Object.keys(summary).length || topicImpacts.length || questionImpacts.length;
  const metrics = [
    ["正确", summary.correct],
    ["错误", summary.incorrect],
    ["部分正确", summary.partial],
    ["待核对", summary.pending_review],
    ["未作答", summary.unanswered],
  ].filter(([, value]) => Number(value || 0) > 0);
  return `
    <section class="practice-record-insights ${hasRecord ? "" : "muted"}" data-practice-record-insights>
      <header>
        <div>
          <strong>学习记录</strong>
          <p>${escapeHtml(insights.headline || "本次提交会沉淀到练习记录、单题状态和知识点统计。")}</p>
        </div>
        <span class="status-pill ${hasRecord ? "mastered" : "learning"}">${hasRecord ? "已记录" : "待记录"}</span>
      </header>
      <div class="practice-record-metrics">
        ${(metrics.length ? metrics : [["已提交", 1]]).map(([label, value]) => `
          <span>${escapeHtml(label)} <strong>${escapeHtml(String(value || ""))}</strong></span>
        `).join("")}
      </div>
      ${topicImpacts.length ? `
        <div class="practice-record-section">
          <h4>影响到的知识点</h4>
          <div class="practice-record-chip-list">
            ${topicImpacts.map((item) => `
              <span>${escapeHtml(item.topic || "未命名知识点")} · 本次错/待核对 ${escapeHtml(String(item.wrong_count || 0))}/${escapeHtml(String(item.attempt_count || 0))}</span>
            `).join("")}
          </div>
        </div>
      ` : ""}
      ${nextActions.length ? `
        <div class="practice-record-section">
          <h4>下一步</h4>
          <div class="practice-record-chip-list action">
            ${nextActions.map((item) => {
              const actionType = item.type || "";
              const actionStatus = item.status
                || (actionType === "review_wrong" ? "incorrect" : "")
                || (actionType === "confirm_grading" ? "pending_review" : "");
              const actionTopic = item.topic
                || (actionType === "topic_review" ? String(item.label || "").replace(/^优先复习\s*/, "") : "");
              return `
                <button
                  type="button"
                  class="practice-record-action-chip"
                  data-practice-next-action="${escapeHtml(actionType)}"
                  data-practice-next-status="${escapeHtml(actionStatus)}"
                  data-practice-next-topic="${escapeHtml(actionTopic)}"
                >
                  ${escapeHtml(item.label || "")}
                </button>
              `;
            }).join("")}
          </div>
        </div>
      ` : ""}
    </section>
  `;
}

async function requestPracticeAiGrade(practiceAttempt, question, overlay, practiceSet, questions = [], options = {}, button = null) {
  const attemptId = practiceAttemptId(practiceAttempt);
  const questionId = question?.question_id || "";
  if (!attemptId || !questionId) return;
  if (button?.disabled) return;
  const body = overlay?.querySelector(".system-workflow-body");
  const currentScrollTop = body ? body.scrollTop : 0;
  setPracticeAiGradeButtonLoading(button, true);
  setSystemSaveStatus("saving", "AI 判分中...");
  try {
    const data = await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/items/${encodeURIComponent(questionId)}/grade?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ judge_method: "ai" }),
    });
    const gradedAttempt = mergePracticeAttempt(practiceAttempt, data.practice_attempt || data);
    const detail = await fetchPracticeAttemptDetail(attemptId);
    const detailAttempt = {
      ...mergePracticeAttempt(gradedAttempt, detail?.practice_attempt || {}),
      insights: detail.insights || gradedAttempt.insights || {},
    };
    setSystemSaveStatus("saved", "AI 判分结果已更新");
    renderPracticeAttemptResult(overlay, practiceSet, questions, detailAttempt, {
      ...options,
      restoreScrollTop: currentScrollTop,
    });
  } catch (error) {
    setPracticeAiGradeButtonLoading(button, false);
    setSystemSaveStatus("error", `AI 判分失败：${error.message}`);
  }
}

async function savePracticeAttemptAnswers(practiceAttempt, answers) {
  const attemptId = practiceAttemptId(practiceAttempt);
  if (!attemptId) return practiceAttempt;
  setSystemSaveStatus("saving", "练习答案保存中...");
  try {
    const data = await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/answers?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers }),
    });
    setSystemSaveStatus("saved", "练习答案已保存");
    return mergePracticeAttempt(practiceAttempt, data.practice_attempt || data);
  } catch (error) {
    setSystemSaveStatus("error", `练习答案保存失败：${error.message}`);
    return practiceAttempt;
  }
}

async function fetchPracticeAttemptDetail(attemptId) {
  if (!attemptId) return null;
  return fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
}

async function openPracticeAttemptResultById(attemptId) {
  if (!attemptId) return;
  const detail = await fetchPracticeAttemptDetail(attemptId);
  const practiceAttempt = detail?.practice_attempt || {};
  const practiceSetId = practiceAttempt.practice_set_id || "";
  let practiceSet = { set_id: practiceSetId, title: "练习结果", question_ids: Object.keys(practiceAttempt.results || {}) };
  if (practiceSetId) {
    try {
      const setData = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
      practiceSet = setData.practice_set || setData || practiceSet;
    } catch {
      // The attempt record is still enough to show a result shell.
    }
  }
  const questionIds = practiceSetQuestionIds(practiceSet, []);
  const questions = await Promise.all(
    questionIds.map(async (questionId) => {
      try {
        return await fetchJson(systemQuestionDetailUrl(questionId));
      } catch {
        return { question_id: questionId };
      }
    })
  );
  const { overlay } = createSystemWorkflowOverlay("练习作答", "查看已提交练习的判分结果。");
  renderPracticeAttemptResult(
    overlay,
    practiceSet,
    questions,
    {
      ...practiceAttempt,
      insights: detail?.insights || practiceAttempt.insights || {},
    },
    { fallbackQuestions: questions },
  );
}

function practiceAttemptDraftTitle(attempt = {}) {
  const sourceMeta = attempt.source_meta && typeof attempt.source_meta === "object" ? attempt.source_meta : {};
  return (
    attempt.title
    || attempt.practice_set_title
    || sourceMeta.practice_set_title
    || sourceMeta.source_title
    || sourceMeta.title
    || attempt.practice_set_id
    || "未提交练习"
  );
}

function practiceAttemptDraftProgress(attempt = {}) {
  const answers = practiceAttemptAnswers(attempt);
  const answeredCount = Object.values(answers).filter((answer) => practiceAnswerValue(answer).trim()).length;
  const sourceMeta = attempt.source_meta && typeof attempt.source_meta === "object" ? attempt.source_meta : {};
  const total = Number(attempt.question_count || sourceMeta.question_count || 0);
  return total > 0 ? `${answeredCount}/${total} 已答` : `${answeredCount} 题已答`;
}

function practiceAttemptDraftUpdatedAt(attempt = {}) {
  const raw = attempt.last_saved_at || attempt.started_at || attempt.updated_at || "";
  return formatPracticeLocalDateTime(raw);
}

async function fetchPracticeSetForAttempt(attempt = {}) {
  const practiceSetId = String(attempt.practice_set_id || "");
  let practiceSet = {
    set_id: practiceSetId,
    title: practiceAttemptDraftTitle(attempt),
    question_ids: Object.keys(practiceAttemptAnswers(attempt)),
  };
  if (!practiceSetId) return practiceSet;
  try {
    const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
    practiceSet = { ...practiceSet, ...(data.practice_set || data || {}) };
  } catch {
    // The attempt itself still has enough data to show a recoverable shell.
  }
  return practiceSet;
}

async function continuePracticeDraftAttempt(overlay, draftAttempt) {
  const body = overlay.querySelector(".system-workflow-body");
  if (body) {
    body.innerHTML = '<div class="empty-state">正在恢复未提交练习...</div>';
  }
  const attemptId = practiceAttemptId(draftAttempt);
  const detail = attemptId ? await fetchPracticeAttemptDetail(attemptId) : null;
  const practiceAttempt = mergePracticeAttempt(draftAttempt, detail?.practice_attempt || {});
  const practiceSet = await fetchPracticeSetForAttempt(practiceAttempt);
  const questions = await resolvePracticeAttemptQuestions(practiceSet, [], {});
  overlay.classList.add("practice-attempt-overlay");
  overlay.querySelector(".system-workflow-dialog")?.classList.add("practice-attempt-dialog");
  renderPracticeAttemptDraft(overlay, practiceSet, questions, practiceAttempt, { fallbackQuestions: questions });
}

async function openPracticeDraftListModal() {
  const { overlay } = createSystemWorkflowOverlay("未提交练习", "这里显示已经开始但尚未提交的练习草稿。关闭作答不会丢失答案。");
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  body.innerHTML = '<div class="empty-state">正在读取未提交练习...</div>';
  try {
    const data = await fetchJson(`/api/materials/system/practice-attempts?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
    const attempts = Array.isArray(data.practice_attempts) ? data.practice_attempts : [];
    const drafts = attempts.filter((attempt) => String(attempt.status || "") === "draft");
    if (!drafts.length) {
      body.innerHTML = '<div class="empty-state">当前没有未提交练习。开始练习并关闭作答页后，会在这里继续。</div>';
      return;
    }
    body.innerHTML = `
      <section class="system-workflow-result">
        <div>
          <strong>未提交草稿</strong>
          <p>${escapeHtml(String(drafts.length))} 份练习尚未提交，可以继续作答或稍后处理。</p>
        </div>
      </section>
      <section class="practice-detail-question-list">
        ${drafts.map((attempt) => {
          const attemptId = practiceAttemptId(attempt);
          return `
            <article class="practice-paper-question">
              <div class="practice-paper-question-head">
                <div>
                  <strong>${escapeHtml(practiceAttemptDraftTitle(attempt))}</strong>
                  <p>${escapeHtml(practiceAttemptDraftProgress(attempt))} · 最后保存：${escapeHtml(practiceAttemptDraftUpdatedAt(attempt))}</p>
                </div>
                <button type="button" class="small-button dark-button" data-practice-draft-continue="${escapeHtml(attemptId)}">继续作答</button>
              </div>
            </article>
          `;
        }).join("")}
      </section>
    `;
    body.querySelectorAll("[data-practice-draft-continue]").forEach((button) => {
      button.addEventListener("click", async () => {
        const attemptId = button.dataset.practiceDraftContinue || "";
        const draft = drafts.find((attempt) => practiceAttemptId(attempt) === attemptId);
        if (!draft || button.disabled) return;
        button.disabled = true;
        button.textContent = "正在恢复...";
        try {
          await continuePracticeDraftAttempt(overlay, draft);
        } catch (error) {
          setSystemSaveStatus("error", `未提交练习恢复失败：${error.message}`);
          button.disabled = false;
          button.textContent = "继续作答";
        }
      });
    });
  } catch (error) {
    body.innerHTML = `<div class="empty-state">未提交练习读取失败：${escapeHtml(error.message)}</div>`;
  }
}

async function submitPracticeAttempt(practiceAttempt, overlay, practiceSet, questions = [], options = {}) {
  const attemptId = practiceAttemptId(practiceAttempt);
  if (!attemptId) return;
  if (!window.confirm("提交后本次练习记录不可修改")) return;
  setSystemSaveStatus("saving", "练习提交中...");
  try {
    const data = await fetchJson(`/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/submit?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
    });
    const submittedAttempt = mergePracticeAttempt(practiceAttempt, data.practice_attempt || data);
    const detail = await fetchPracticeAttemptDetail(attemptId);
    const detailAttempt = {
      ...mergePracticeAttempt(submittedAttempt, detail?.practice_attempt || {}),
      insights: detail.insights || submittedAttempt.insights || {},
    };
    setSystemSaveStatus("saved", "练习已提交");
    refreshPracticeRecordsAfterPracticeChange();
    renderPracticeAttemptResult(overlay, practiceSet, questions, detailAttempt, options);
  } catch (error) {
    setSystemSaveStatus("error", `练习提交失败：${error.message}`);
  }
}

async function openPracticeAttempt(practiceSet, questions = [], options = {}) {
  const practiceSetId = systemPracticeSetId(practiceSet);
  if (!practiceSetId) {
    window.alert("这张练习单暂时无法开始练习。");
    return;
  }
  const { overlay } = createSystemWorkflowOverlay("练习作答", "按整张练习卷作答，右侧答题卡会显示进度。");
  overlay.classList.add("practice-attempt-overlay");
  overlay.querySelector(".system-workflow-dialog")?.classList.add("practice-attempt-dialog");
  const body = overlay.querySelector(".system-workflow-body");
  if (body) {
    body.innerHTML = '<div class="empty-state">正在创建练习记录...</div>';
  }
  try {
    const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}/attempts?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
    });
    const practiceAttempt = data.practice_attempt || data;
    const detailQuestions = await resolvePracticeAttemptQuestions(practiceSet, questions, options);
    if (practiceAttempt.status === "submitted" || practiceAttempt.submitted_at) {
      renderPracticeAttemptResult(overlay, practiceSet, detailQuestions, practiceAttempt, { ...options, fallbackQuestions: detailQuestions });
      return;
    }
    setSystemSaveStatus("saved", "未提交草稿已保存，可在复习规划的学习概览里继续。");
    refreshPracticeRecordsAfterPracticeChange();
    renderPracticeAttemptDraft(overlay, practiceSet, detailQuestions, practiceAttempt, { ...options, fallbackQuestions: detailQuestions });
  } catch (error) {
    if (body) {
      body.innerHTML = `<div class="empty-state">练习记录创建失败：${escapeHtml(error.message)}</div>`;
    }
  }
}

function renderSystemPracticeSetDetail(overlay, practiceSet, questions = [], options = {}) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const fallbackQuestions = options.fallbackQuestions || [];
  const questionIds = practiceSetQuestionIds(practiceSet, fallbackQuestions);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const title = practiceSet.title || practiceSet.name || "同类训练练习单";
  const firstQuestion = questionMap.get(questionIds[0]) || fallbackQuestions.find((item) => item.question_id === questionIds[0]) || {};
  const latestAttempt = latestSubmittedPracticeAttempt(options.practiceAttempts);
  const latestAttemptId = practiceAttemptId(latestAttempt || {});
  const latestAttemptDate = latestAttempt?.submitted_at ? String(latestAttempt.submitted_at).slice(0, 10) : "";
  body.innerHTML = `
    <section class="system-workflow-result">
      <div>
        <strong>${escapeHtml(title)}</strong>
        <p>${questionIds.length} 题 · ${escapeHtml((practiceSet.matching_topics || []).join(" / ") || practiceSet.library_name || "系统题库")}</p>
      </div>
      <div class="system-workflow-result-actions">
        <button type="button" class="small-button" data-practice-detail-return>返回复习规划</button>
        <button type="button" class="small-button dark-button" data-practice-start-attempt>开始练习</button>
        <button type="button" class="small-button dark-button" data-practice-add-review>加入复习规划</button>
        <button type="button" class="small-button" data-practice-download-pdf>打印/另存 PDF</button>
        <button type="button" class="small-button" data-practice-delete>删除练习单</button>
        <button type="button" class="small-button" data-practice-detail-close>关闭</button>
      </div>
    </section>
    ${latestAttemptId ? `
      <section class="practice-latest-result" data-practice-latest-result>
        <div>
          <strong>最近练习结果</strong>
          <p>${escapeHtml(practiceAttemptSummaryText(latestAttempt))}${latestAttemptDate ? ` · ${escapeHtml(latestAttemptDate)}` : ""}</p>
        </div>
        <button type="button" class="small-button dark-button" data-practice-latest-result-open="${escapeHtml(latestAttemptId)}">查看最近结果</button>
      </section>
    ` : ""}
    <section class="practice-detail-paper" data-practice-detail-paper>
      <button type="button" class="small-button practice-detail-back-button" data-practice-detail-return>返回</button>
      <div class="practice-detail-paper-head">
        <div>
          <h4>练习题</h4>
          <p>连续练习卷视图。每题完整显示题干、公式和题图；单题操作收在右上角菜单。</p>
        </div>
      </div>
      <div class="practice-detail-question-list">
        ${questionIds.length ? questionIds.map((questionId, index) => {
          const question = questionMap.get(questionId) || fallbackQuestions.find((item) => item.question_id === questionId) || { question_id: questionId };
          const topics = Array.isArray(question.topics) ? question.topics.join(" / ") : "";
          const personal = systemUserState(questionId);
          return `
            <article class="practice-paper-question">
              <div class="practice-paper-question-head">
                <div>
                  <strong>${index + 1}. ${escapeHtml(question.question_id ? systemQuestionTitle(question) || question.question_id : questionId)}</strong>
                  <p>${escapeHtml([question.question_type_label || question.question_type, question.library_name, topics].filter(Boolean).join(" · ") || questionId)}</p>
                </div>
                <details class="practice-question-menu" data-practice-question-menu>
                  <summary aria-label="题目操作">···</summary>
                  <div class="practice-question-menu-panel">
                    <button type="button" class="small-button" data-practice-detail-question="${escapeHtml(questionId)}">查看详情</button>
                    <button type="button" class="small-button" data-practice-question-wrong="${escapeHtml(questionId)}">${personal.in_wrong_book ? "移出错题" : "加入错题"}</button>
                    <button type="button" class="small-button" data-practice-question-mastered="${escapeHtml(questionId)}">标记掌握</button>
                    <button type="button" class="small-button" data-practice-question-review="${escapeHtml(questionId)}">加入复习规划</button>
                  </div>
                </details>
              </div>
              <div class="practice-paper-question-body">
                ${question.question_id ? renderSystemQuestionMarkdown(question) : `<p>${escapeHtml(questionId)}</p>`}
              </div>
            </article>
          `;
        }).join("") : '<div class="empty-state">这张练习单暂时没有题目。</div>'}
      </div>
    </section>
  `;
  body.querySelector("[data-practice-detail-close]")?.addEventListener("click", closeSystemWorkflowModal);
  body.querySelector("[data-practice-start-attempt]")?.addEventListener("click", () => {
    void openPracticeAttempt(practiceSet, questions, { fallbackQuestions });
  });
  body.querySelector("[data-practice-latest-result-open]")?.addEventListener("click", async (event) => {
    const attemptId = event.currentTarget?.dataset?.practiceLatestResultOpen || latestAttemptId;
    if (!attemptId) return;
    try {
      const detail = await fetchPracticeAttemptDetail(attemptId);
      const detailAttempt = {
        ...mergePracticeAttempt(latestAttempt || {}, detail?.practice_attempt || {}),
        insights: detail?.insights || latestAttempt?.insights || {},
      };
      renderPracticeAttemptResult(overlay, practiceSet, questions, detailAttempt, { fallbackQuestions });
    } catch (error) {
      setSystemSaveStatus("error", `练习结果加载失败：${error.message}`);
    }
  });
  body.querySelectorAll("[data-practice-detail-return]").forEach((button) => {
    button.addEventListener("click", () => {
      closeSystemWorkflowModal();
      setActivePage("plan");
    });
  });
  body.querySelector("[data-practice-add-review]")?.addEventListener("click", () => {
    if (!firstQuestion.question_id) return;
    openSystemReviewModal(firstQuestion, {
      practiceSet,
      questionIds,
    });
  });
  body.querySelector("[data-practice-download-pdf]")?.addEventListener("click", () => {
    showPracticeSetPrintOverlay(practiceSet, questions, { fallbackQuestions });
  });
  body.querySelector("[data-practice-delete]")?.addEventListener("click", async () => {
    const practiceSetId = systemPracticeSetId(practiceSet);
    if (!practiceSetId) return;
    if (!window.confirm("确定删除这张练习单吗？")) return;
    try {
      await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
        method: "DELETE",
      });
      setSystemSaveStatus("saved", "练习单已删除");
      closeSystemWorkflowModal();
      if (pages.plan?.classList.contains("active")) {
        void loadReviewTasks({ silent: true });
      }
    } catch (error) {
      setSystemSaveStatus("error", `删除练习单失败：${error.message}`);
    }
  });
  body.querySelectorAll("[data-practice-detail-question]").forEach((button) => {
    button.addEventListener("click", () => {
      closeSystemWorkflowModal();
      setActivePage("materials");
      setMaterialsMode(MATERIALS_MODE_SYSTEM, { skipRefreshWhenCurrent: true });
      void openSystemQuestionDrawer(button.dataset.practiceDetailQuestion);
    });
  });
  body.querySelectorAll("[data-practice-question-wrong]").forEach((button) => {
    button.addEventListener("click", () => {
      toggleSystemWrongBook(button.dataset.practiceQuestionWrong);
      renderSystemPracticeSetDetail(overlay, practiceSet, questions, options);
    });
  });
  body.querySelectorAll("[data-practice-question-mastered]").forEach((button) => {
    button.addEventListener("click", () => {
      setSystemMastery(button.dataset.practiceQuestionMastered, "mastered");
      renderSystemPracticeSetDetail(overlay, practiceSet, questions, options);
    });
  });
  body.querySelectorAll("[data-practice-question-review]").forEach((button) => {
    button.addEventListener("click", () => {
      const question = questionMap.get(button.dataset.practiceQuestionReview) || fallbackQuestions.find((item) => item.question_id === button.dataset.practiceQuestionReview);
      if (question) {
        openSystemReviewModal(question);
      }
    });
  });
}

function practiceQuestionPrintableText(question = {}) {
  return (
    question.question_text
    || question.stem
    || question.preview
    || question.content
    || question.raw_markdown
    || question.question_id
    || ""
  );
}

function showPracticeSetPrintOverlay(practiceSet = {}, questions = [], options = {}) {
  const fallbackQuestions = options.fallbackQuestions || [];
  const questionIds = practiceSetQuestionIds(practiceSet, fallbackQuestions);
  const questionMap = new Map(questions.map((question) => [question.question_id, question]));
  const title = practiceSet.title || practiceSet.name || "同类训练练习单";
  const rows = questionIds.map((questionId, index) => {
    const question = questionMap.get(questionId) || fallbackQuestions.find((item) => item.question_id === questionId) || { question_id: questionId };
    const topics = Array.isArray(question.topics) ? question.topics.join(" / ") : "";
    const text = practiceQuestionPrintableText(question);
    return `
      <article class="print-question">
        <h2>${index + 1}. ${escapeHtml(systemQuestionTitle(question) || questionId)}</h2>
        <p class="meta">${escapeHtml([question.question_type_label || question.question_type, question.library_name, topics].filter(Boolean).join(" · "))}</p>
        <div>${md.render(normalizeMathMarkdown(normalizeSystemMathCodeSpans(normalizeSystemChoiceOptionMarkdown(text))))}</div>
      </article>
    `;
  }).join("");
  document.querySelector(".practice-print-overlay")?.remove();
  const overlay = document.createElement("div");
  overlay.className = "practice-print-overlay";
  overlay.innerHTML = `
    <section class="practice-print-sheet" role="dialog" aria-modal="true" aria-labelledby="practicePrintTitle">
      <div class="practice-print-actions">
        <button type="button" class="small-button dark-button" data-practice-print-now>打印/另存 PDF</button>
        <button type="button" class="small-button" data-practice-print-close>关闭</button>
      </div>
      <div class="practice-print-content">
        <h1>${escapeHtml(title)}</h1>
        <p class="meta">${questionIds.length} 题 · ${escapeHtml(practiceSet.library_name || "系统题库")}</p>
        ${rows || "<p>这张练习单暂时没有题目。</p>"}
      </div>
    </section>
  `;
  document.body.appendChild(overlay);

  const close = () => {
    document.body.classList.remove("practice-printing");
    overlay.remove();
  };
  overlay.querySelector("[data-practice-print-close]")?.addEventListener("click", close);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) close();
  });
  overlay.querySelector("[data-practice-print-now]")?.addEventListener("click", () => {
    document.body.classList.add("practice-printing");
    window.print();
    window.setTimeout(() => document.body.classList.remove("practice-printing"), 300);
  });
}

async function openSystemPracticeSetDetail(practiceSet, options = {}) {
  const practiceSetId = systemPracticeSetId(practiceSet);
  const { overlay } = createSystemWorkflowOverlay("练习单详情", "查看练习单中的题目，后续可下载为 PDF。");
  const fallbackQuestions = options.fallbackQuestions || [];
  const body = overlay.querySelector(".system-workflow-body");
  if (body) {
    body.innerHTML = '<div class="empty-state">正在加载练习单题目...</div>';
  }
  try {
    let detail = practiceSet || {};
    let practiceAttempts = [];
    if (practiceSetId) {
      const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
      detail = data.practice_set || data;
      const attemptData = await fetchJson(`/api/materials/system/practice-attempts?practice_set_id=${encodeURIComponent(practiceSetId)}&user_id=${encodeURIComponent(currentMaterialsUserId())}`);
      practiceAttempts = Array.isArray(attemptData.practice_attempts) ? attemptData.practice_attempts : [];
    }
    const ids = practiceSetQuestionIds(detail, fallbackQuestions);
    const questions = await Promise.all(
      ids.map(async (questionId) => {
        try {
          return await fetchJson(systemQuestionDetailUrl(questionId));
        } catch {
          return { question_id: questionId };
        }
      })
    );
    renderSystemPracticeSetDetail(overlay, detail, questions, { fallbackQuestions, practiceAttempts });
  } catch (error) {
    if (body) {
      body.innerHTML = `<div class="empty-state">练习单加载失败：${escapeHtml(error.message)}</div>`;
    }
  }
}

function defaultReviewDueDate(days = 1) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return localDateKey(date);
}

function localDateKey(value = new Date()) {
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const pad = (part) => String(part).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function formatPracticeLocalDateTime(value) {
  if (!value) return "未记录";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value).slice(0, 16).replace("T", " ");
  const pad = (part) => String(part).padStart(2, "0");
  return `${localDateKey(date)} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function reviewTaskId(task = {}) {
  return task.review_task_id || task.id || task.task_id || "";
}

function reviewTaskDueDate(task = {}) {
  return String(task.due_date || task.review_due_at || task.due_at || "").slice(0, 10);
}

function markQuestionReviewScheduled(question, dueDate) {
  if (!question?.question_id) return;
  updateSystemQuestionPersonalState(question.question_id, { review_due_at: dueDate || null });
  renderSystemStateSurfaces(question.question_id);
}

function renderSystemReviewModal(overlay, question, config) {
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const targetCount = Math.max(1, (config.questionIds || [question.question_id]).length);
  body.innerHTML = `
    <div class="workflow-form-grid">
      <label class="field">
        <span>目标题</span>
        <input type="text" value="${escapeHtml(targetCount > 1 ? `${targetCount} 道题` : systemQuestionTitle(question))}" readonly>
      </label>
      <label class="field">
        <span>到期日期</span>
        <input type="date" value="${escapeHtml(config.dueDate)}" data-system-review-due-date>
      </label>
      <label class="field">
        <span>优先级</span>
        <select data-system-review-priority>
          <option value="normal" ${config.priority === "normal" ? "selected" : ""}>普通</option>
          <option value="high" ${config.priority === "high" ? "selected" : ""}>高</option>
          <option value="low" ${config.priority === "low" ? "selected" : ""}>低</option>
        </select>
      </label>
      <div class="system-review-shortcuts" aria-label="到期时间快捷">
        <button type="button" class="small-button" data-system-review-due-shortcut="0">今天</button>
        <button type="button" class="small-button" data-system-review-due-shortcut="1">明天</button>
        <button type="button" class="small-button" data-system-review-due-shortcut="7">7 天后</button>
      </div>
    </div>
    <label class="field">
      <span>备注</span>
      <textarea rows="4" data-system-review-note placeholder="记录复习目的、易错点或练习单说明">${escapeHtml(config.note || "")}</textarea>
    </label>
    ${config.savedReviewTask ? `
      <section class="system-workflow-result">
        <div>
          <strong>已加入复习规划</strong>
          <p>${escapeHtml(reviewTaskDueDate(config.savedReviewTask) || config.dueDate)} · ${escapeHtml(config.priority)}</p>
        </div>
        <button type="button" class="small-button dark-button" data-system-review-open-plan>查看规划</button>
      </section>
    ` : ""}
    <div class="system-workflow-actions">
      <button type="button" class="small-button dark-button" data-system-review-save ${config.saving ? "disabled" : ""}>${config.saving ? "保存中..." : "保存到复习规划"}</button>
    </div>
  `;
  body.querySelector("[data-system-review-due-date]")?.addEventListener("input", (event) => {
    config.dueDate = event.target.value;
  });
  body.querySelector("[data-system-review-priority]")?.addEventListener("change", (event) => {
    config.priority = event.target.value;
  });
  body.querySelector("[data-system-review-note]")?.addEventListener("input", (event) => {
    config.note = event.target.value;
  });
  body.querySelectorAll("[data-system-review-due-shortcut]").forEach((button) => {
    button.addEventListener("click", () => {
      config.dueDate = defaultReviewDueDate(Number(button.dataset.systemReviewDueShortcut || 1));
      config.savedReviewTask = null;
      renderSystemReviewModal(overlay, question, config);
    });
  });
  body.querySelector("[data-system-review-save]")?.addEventListener("click", () => {
    void saveSystemReviewTask(question, config, overlay);
  });
  body.querySelector("[data-system-review-open-plan]")?.addEventListener("click", () => {
    closeSystemWorkflowModal();
    setActivePage("plan");
  });
}

function openSystemReviewModal(question, options = {}) {
  const { overlay } = createSystemWorkflowOverlay("加入复习规划", "设置到期时间、优先级和备注，保存为个人复习任务。");
  const config = {
    dueDate: defaultReviewDueDate(1),
    priority: "normal",
    note: options.practiceSet ? "来自同类训练练习单" : "",
    practiceSet: options.practiceSet || null,
    questionIds: options.questionIds || [question.question_id],
    saving: false,
    savedReviewTask: null,
  };
  renderSystemReviewModal(overlay, question, config);
}

async function saveSystemReviewTask(question, config, overlay) {
  config.saving = true;
  renderSystemReviewModal(overlay, question, config);
  try {
    const payload = {
      target_type: config.practiceSet ? "practice_set" : "question",
      target_id: config.practiceSet ? systemPracticeSetId(config.practiceSet) : question.question_id,
      title: config.practiceSet
        ? (config.practiceSet.title || "同类训练复习")
        : `${systemQuestionTitle(question)} 复习`,
      due_at: config.dueDate,
      priority: systemReviewPriorityValue(config.priority),
      note: config.note || "",
    };
    const data = await fetchJson(`/api/materials/system/review-tasks?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    config.savedReviewTask = data.review_task || data;
    markQuestionReviewScheduled(question, reviewTaskDueDate(config.savedReviewTask) || config.dueDate);
    setSystemSaveStatus("saved", "已加入复习规划");
    if (pages.plan?.classList.contains("active")) {
      void loadReviewTasks({ silent: true });
    }
  } catch (error) {
    setSystemSaveStatus("error", `复习规划保存失败：${error.message}`);
  } finally {
    config.saving = false;
    renderSystemReviewModal(overlay, question, config);
  }
}

async function loadSystemQuestionLearningSnapshot(questionId) {
  if (!questionId) return {};
  const data = await fetchJson(`/api/materials/system/questions/${encodeURIComponent(questionId)}/learning-snapshot?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
  return data.snapshot || {};
}

function renderSystemQuestionLearningSnapshot(snapshot = {}) {
  const attempts = Array.isArray(snapshot.recent_attempts) ? snapshot.recent_attempts : [];
  const attemptCount = Number(snapshot.attempt_count || 0);
  const latestStatus = snapshot.latest_status || "";
  const latestDate = snapshot.latest_practiced_at ? String(snapshot.latest_practiced_at).slice(0, 10) : "";
  return `
    <section class="system-learning-history" data-system-learning-history>
      <header>
        <h4>练习记录</h4>
        <span class="status-pill ${attemptCount ? "mastered" : "learning"}">${attemptCount ? `${attemptCount} 次` : "暂无"}</span>
      </header>
      <div class="system-learning-history-metrics">
        <span>正确 <strong>${escapeHtml(String(snapshot.correct_count || 0))}</strong></span>
        <span>错误 <strong>${escapeHtml(String(snapshot.incorrect_count || 0))}</strong></span>
        <span>待核对 <strong>${escapeHtml(String(snapshot.pending_review_count || 0))}</strong></span>
        ${snapshot.wrong_streak ? `<span>连续错 <strong>${escapeHtml(String(snapshot.wrong_streak))}</strong></span>` : ""}
      </div>
      ${latestStatus ? `<p>最近一次：${escapeHtml(practiceAttemptResultLabel({ final_status: latestStatus }))}${latestDate ? ` · ${escapeHtml(latestDate)}` : ""}</p>` : "<p>提交练习后，这里会显示单题历史、错题次数和最近状态。</p>"}
      ${attempts.length ? `
        <div class="system-learning-history-list">
          ${attempts.map((item) => `
            <span>${escapeHtml(String(item.submitted_at || "").slice(0, 10) || "未记录日期")} · ${escapeHtml(practiceAttemptResultLabel({ final_status: item.status }))}</span>
          `).join("")}
        </div>
      ` : ""}
    </section>
  `;
}

function renderSystemQuestionDrawer(question) {
  if (!systemQuestionDrawer) return;
  const personal = systemUserState(question.question_id);
  const tutorMode = systemTutor.active && systemTutor.questionId === question.question_id;
  const closeLabel = tutorMode ? "返回" : "关闭";
  const collapseLabel = systemTutor.contextCollapsed ? "展开题目上下文" : "折叠题目上下文";
  const collapseIcon = systemTutor.contextCollapsed ? "<" : ">";
  systemQuestionDrawer.innerHTML = `
    ${tutorMode ? `<button type="button" class="system-drawer-collapse-handle" data-system-tutor-toggle-context aria-label="${collapseLabel}" title="${collapseLabel}">${collapseIcon}</button>` : ""}
    <div class="system-drawer-header">
      <div>
        <p class="eyebrow">System Question</p>
        <h3>${escapeHtml(systemQuestionTitle(question))}</h3>
      </div>
      <button type="button" class="small-button" data-system-drawer-close>${closeLabel}</button>
    </div>
    <section class="system-drawer-section">
      <h4>掌握状态</h4>
      <div class="segmented-control" role="group" aria-label="掌握状态">
        ${Object.entries(SYSTEM_MASTERY_LABELS).map(([value, label]) => `
          <button type="button" class="${personal.mastery_status === value ? "active" : ""}" data-system-mastery="${value}">${label}</button>
        `).join("")}
      </div>
    </section>
    <section class="system-drawer-section">
      <h4>个人操作</h4>
      <div class="system-mark-actions">
        <button type="button" class="small-button ${personal.is_favorite ? "active" : ""}" data-system-toggle-favorite>${personal.is_favorite ? "取消收藏" : "收藏"}</button>
        <button type="button" class="small-button ${personal.in_wrong_book ? "active" : ""}" data-system-toggle-wrong>${personal.in_wrong_book ? "移出错题" : "加入错题"}</button>
        <span class="status-pill note" data-system-note-indicator>${personal.personal_note ? "有备注" : "无备注"}</span>
        ${personal.review_due_at ? `<span class="status-pill review">复习 ${escapeHtml(String(personal.review_due_at).slice(0, 10))}</span>` : ""}
      </div>
    </section>
    <div data-system-learning-history>
      ${renderSystemQuestionLearningSnapshot(question.learning_snapshot || {})}
    </div>
    <section class="system-drawer-section">
      <h4>题目详情</h4>
      <div class="system-detail-meta">
        <span>${escapeHtml(question.library_name || "系统题库")}</span>
        <span>${escapeHtml(question.question_type_label || question.question_type || "题型未知")}</span>
        <span>${escapeHtml((question.topics || []).join(" / ") || "知识点未标注")}</span>
      </div>
      ${renderSystemQuestionMarkdown(question)}
      <details class="system-fold">
        <summary>答案</summary>
        <div class="system-markdown">${renderSystemMarkdown(question.answer_markdown || question.answer || "")}</div>
      </details>
      <details class="system-fold">
        <summary>解析</summary>
        <div class="system-markdown">${renderSystemMarkdown(question.explanation_markdown || question.explanation || "")}</div>
      </details>
    </section>
    <section class="system-drawer-section">
      <h4>个人备注</h4>
      <textarea class="system-note-input" rows="5" placeholder="写下这道题的易错点、解题入口或复习提醒">${escapeHtml(personal.personal_note)}</textarea>
    </section>
    <section class="system-drawer-section">
      <h4>动作</h4>
      <div class="system-drawer-actions">
        <button type="button" class="small-button dark-button" data-system-ask-ai ${tutorMode ? "disabled" : ""}>${tutorMode ? "正在讲题" : "问 AI 讲题"}</button>
        <button type="button" class="small-button" data-system-open-practice>生成同类训练</button>
        <button type="button" class="small-button" data-system-open-review>${personal.review_due_at ? "调整复习规划" : "加入复习规划"}</button>
      </div>
    </section>
  `;

  systemQuestionDrawer.querySelector("[data-system-drawer-close]")?.addEventListener("click", () => {
    if (tutorMode) {
      exitSystemQuestionTutor();
      return;
    }
    closeSystemQuestionDrawer();
  });
  systemQuestionDrawer.querySelector("[data-system-tutor-toggle-context]")?.addEventListener("click", toggleSystemTutorContext);
  systemQuestionDrawer.querySelectorAll("[data-system-mastery]").forEach((button) => {
    button.addEventListener("click", () => setSystemMastery(question.question_id, button.dataset.systemMastery));
  });
  systemQuestionDrawer.querySelector("[data-system-toggle-favorite]")?.addEventListener("click", () => toggleSystemFavorite(question.question_id));
  systemQuestionDrawer.querySelector("[data-system-toggle-wrong]")?.addEventListener("click", () => toggleSystemWrongBook(question.question_id));
  systemQuestionDrawer.querySelector("[data-system-ask-ai]")?.addEventListener("click", (event) => {
    event.currentTarget.disabled = true;
    void askAiForSystemQuestion(question).finally(() => {
      event.currentTarget.disabled = false;
    });
  });
  systemQuestionDrawer.querySelector("[data-system-open-practice]")?.addEventListener("click", () => openSystemPracticeModal(question));
  systemQuestionDrawer.querySelector("[data-system-open-review]")?.addEventListener("click", () => openSystemReviewModal(question));
  systemQuestionDrawer.querySelector(".system-note-input")?.addEventListener("input", (event) => {
    const previousState = { ...systemUserState(question.question_id) };
    const noteUserId = systemState.userId || currentMaterialsUserId();
    updateSystemQuestionPersonalState(question.question_id, { personal_note: event.target.value });
    const noteIndicator = systemQuestionDrawer.querySelector("[data-system-note-indicator]");
    if (noteIndicator) {
      noteIndicator.textContent = systemUserState(question.question_id).personal_note ? "有备注" : "无备注";
    }
    renderSystemQuestionList();
    window.clearTimeout(systemNoteSaveTimer);
    systemNoteSaveTimer = window.setTimeout(() => {
      if (noteUserId !== currentMaterialsUserId()) return;
      const note = systemUserState(question.question_id).personal_note;
      void saveSystemQuestionState(question.question_id, { personal_note: note }, { renderDrawer: false, userId: noteUserId })
        .catch((error) => {
          if (noteUserId !== currentMaterialsUserId()) return;
          handleSystemQuestionStateSaveError(question.question_id, error, previousState);
        });
    }, 360);
  });
  void loadSystemQuestionLearningSnapshot(question.question_id)
    .then((snapshot) => {
      if (!systemQuestionDrawer || systemState.selectedQuestionId !== question.question_id) return;
      const target = systemQuestionDrawer.querySelector("[data-system-learning-history]");
      if (target) {
        target.innerHTML = renderSystemQuestionLearningSnapshot(snapshot);
      }
      if (systemState.selectedQuestion && systemState.selectedQuestion.question_id === question.question_id) {
        systemState.selectedQuestion.learning_snapshot = snapshot;
      }
    })
    .catch(() => {
      if (!systemQuestionDrawer || systemState.selectedQuestionId !== question.question_id) return;
      const target = systemQuestionDrawer.querySelector("[data-system-learning-history]");
      if (target) {
        target.innerHTML = `
          <section class="system-learning-history" data-system-learning-history>
            <header><h4>练习记录</h4><span class="status-pill learning">加载失败</span></header>
            <p>暂时无法读取这道题的练习记录。</p>
          </section>
        `;
      }
    });
}

async function openSystemQuestionDrawer(questionId) {
  systemState.selectedQuestionId = questionId;
  systemState.selectedQuestion = null;
  renderSystemQuestionList();
  if (systemQuestionDrawer) {
    systemQuestionDrawer.innerHTML = '<div class="empty-state">正在加载题目详情...</div>';
  }
  try {
    const detail = await fetchJson(systemQuestionDetailUrl(questionId));
    if (systemState.selectedQuestionId !== questionId) {
      return;
    }
    hydrateSystemQuestionPersonalState(detail.question_id, detail.personal_state);
    systemState.selectedQuestion = detail;
    renderSystemQuestionList();
    renderSystemQuestionDrawer(detail);
  } catch (error) {
    if (systemState.selectedQuestionId !== questionId) {
      return;
    }
    if (systemQuestionDrawer) {
      systemQuestionDrawer.innerHTML = `<div class="empty-state">题目详情加载失败：${escapeHtml(error.message)}</div>`;
    }
  }
}

async function openSystemQuestionPreview(questionId) {
  document.querySelector(".system-preview-overlay")?.remove();

  const overlay = document.createElement("div");
  overlay.className = "system-preview-overlay";
  overlay.innerHTML = `
    <section class="system-preview-dialog" role="dialog" aria-modal="true" aria-labelledby="systemPreviewTitle">
      <header class="system-preview-dialog-header">
        <div>
          <p class="eyebrow">Question Preview</p>
          <h3 id="systemPreviewTitle">题目预览</h3>
        </div>
        <button type="button" class="small-button" data-system-preview-close>关闭</button>
      </header>
      <div class="system-preview-dialog-body empty-state">正在加载完整题干...</div>
    </section>
  `;

  const close = () => {
    document.removeEventListener("keydown", onKeyDown);
    overlay.remove();
  };
  const onKeyDown = (event) => {
    if (event.key === "Escape") {
      close();
    }
  };

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) {
      close();
    }
  });
  overlay.querySelector("[data-system-preview-close]")?.addEventListener("click", close);
  document.addEventListener("keydown", onKeyDown);
  document.body.appendChild(overlay);

  try {
    const question = await fetchJson(systemQuestionDetailUrl(questionId));
    if (!overlay.isConnected) return;
    hydrateSystemQuestionPersonalState(question.question_id, question.personal_state);
    renderSystemQuestionList();

    const title = overlay.querySelector("#systemPreviewTitle");
    const body = overlay.querySelector(".system-preview-dialog-body");
    if (title) {
      title.textContent = systemQuestionTitle(question);
    }
    if (body) {
      const topics = Array.isArray(question.topics) && question.topics.length
        ? `<div class="system-topic-list">${question.topics.slice(0, 8).map((topic) => `<span>${escapeHtml(topic)}</span>`).join("")}</div>`
        : "";
      body.className = "system-preview-dialog-body";
      body.innerHTML = `
        <div class="system-detail-meta">
          <span class="status-pill type">${escapeHtml(question.question_type_label || question.question_type || "题型未知")}</span>
          <span>${escapeHtml(question.library_name || "系统题库")}</span>
        </div>
        ${topics}
        ${renderSystemQuestionMarkdown(question)}
      `;
    }
  } catch (error) {
    const body = overlay.querySelector(".system-preview-dialog-body");
    if (body) {
      body.className = "system-preview-dialog-body empty-state";
      body.textContent = `题目预览加载失败：${error.message}`;
    }
  }
}

function closeSystemQuestionDrawer() {
  systemState.selectedQuestionId = "";
  systemState.selectedQuestion = null;
  renderSystemQuestionList();
  renderSystemDrawerEmpty();
}

function setReviewTasksStatus(status, message = "") {
  if (!reviewTasksStatus) return;
  if (!status) {
    reviewTasksStatus.hidden = true;
    reviewTasksStatus.textContent = "";
    reviewTasksStatus.className = "system-save-status";
    return;
  }
  reviewTasksStatus.hidden = false;
  reviewTasksStatus.className = status === "error"
    ? "system-save-status error"
    : "system-save-status saved";
  reviewTasksStatus.textContent = message;
}

function normalizeReviewTasksPayload(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.items)) return data.items;
  if (Array.isArray(data.review_tasks)) return data.review_tasks;
  if (Array.isArray(data.tasks)) return data.tasks;
  return [];
}

function buildReviewTaskQuery() {
  const params = new URLSearchParams();
  params.set("user_id", currentMaterialsUserId());
  if (reviewTasksState.filters.subject) params.set("subject", reviewTasksState.filters.subject);
  if (reviewTasksState.filters.targetType) params.set("target_type", reviewTasksState.filters.targetType);
  if (reviewTasksState.filters.dateGroup) params.set("date_group", reviewTasksState.filters.dateGroup);
  if (reviewTasksState.filters.keyword) params.set("keyword", reviewTasksState.filters.keyword);
  return params.toString();
}

function buildReviewLearningInsightsQuery() {
  const params = new URLSearchParams();
  params.set("user_id", currentMaterialsUserId());
  params.set("limit", "5");
  if (reviewTasksState.filters.subject) {
    params.set("subject", reviewTasksState.filters.subject);
  }
  return params.toString();
}

async function loadReviewLearningInsights(options = {}) {
  if (!reviewLearningInsights) return;
  if (!options.silent) {
    reviewTasksState.insightsLoading = true;
    reviewTasksState.insightsError = "";
    renderReviewLearningInsights();
  }
  try {
    const data = await fetchJson(`/api/materials/system/learning-insights?${buildReviewLearningInsightsQuery()}`);
    reviewTasksState.learningInsights = data.insights || {};
    reviewTasksState.insightsError = "";
  } catch (error) {
    reviewTasksState.learningInsights = null;
    reviewTasksState.insightsError = error.message;
  } finally {
    reviewTasksState.insightsLoading = false;
    renderReviewLearningInsights();
  }
}

function refreshPracticeRecordsAfterPracticeChange() {
  if (!pages.plan?.classList.contains("active")) return;
  void loadReviewLearningInsights({ silent: true });
  void loadReviewTasks({ silent: true });
}

async function loadReviewTasks(options = {}) {
  if (!reviewTaskList) return;
  if (!options.silent) {
    reviewTasksState.loading = true;
    reviewTasksState.error = "";
    renderReviewTasks();
  }
  try {
    const data = await fetchJson(`/api/materials/system/review-tasks?${buildReviewTaskQuery()}`);
    reviewTasksState.items = normalizeReviewTasksPayload(data);
    reviewTasksState.error = "";
    setReviewTasksStatus("", "");
  } catch (error) {
    reviewTasksState.items = [];
    reviewTasksState.error = error.message;
    setReviewTasksStatus("error", `复习任务加载失败：${error.message}`);
  } finally {
    reviewTasksState.loading = false;
    renderReviewTasks();
  }
}

function reviewTaskStatus(task = {}) {
  return String(task.status || task.state || "pending");
}

function reviewTaskTitle(task = {}) {
  if (task.title) return task.title;
  if (task.question_title) return task.question_title;
  if (task.source_question_id) return `系统题 ${task.source_question_id}`;
  if (Array.isArray(task.question_ids) && task.question_ids.length) return `${task.question_ids.length} 道系统题`;
  return "复习任务";
}

function reviewTaskPriorityLabel(priority) {
  const value = String(priority);
  if (value === "high" || value === "4" || value === "5") return "高优先级";
  if (value === "low" || value === "1") return "低优先级";
  return "普通";
}

function reviewTaskTargetTypeLabel(targetType) {
  const value = String(targetType || "");
  if (value === "practice_set") return "练习单";
  if (value === "knowledge_point") return "知识点";
  return "单题";
}

function reviewTaskStatusLabel(status) {
  const value = String(status || "pending");
  if (value === "completed" || value === "done") return "已完成";
  if (value === "cancelled" || value === "canceled") return "已取消";
  return "待复习";
}

function systemReviewPriorityValue(priority) {
  if (priority === "high") return 4;
  if (priority === "low") return 1;
  return 2;
}

function reviewTaskDateGroup(task) {
  const status = reviewTaskStatus(task);
  if (status === "completed" || status === "done") {
    return "completed";
  }
  if (status === "cancelled" || status === "canceled") {
    return "cancelled";
  }
  const dueDate = reviewTaskDueDate(task);
  if (!dueDate) return "future";
  const today = localDateKey();
  if (dueDate < today) return "overdue";
  if (dueDate === today) return "today";
  return "future";
}

function reviewTaskDateTimestamp(dateKey) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(dateKey || ""))) return Number.MAX_SAFE_INTEGER;
  return new Date(`${dateKey}T00:00:00`).getTime();
}

function reviewTaskCompactDateLabel(dateKey) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(dateKey || ""))) return "未定";
  const date = new Date(`${dateKey}T00:00:00`);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
}

function reviewTaskDateGroupLabel(dateKey) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(dateKey || ""))) return "未设置日期";
  const date = new Date(`${dateKey}T00:00:00`);
  const weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
  return `${dateKey} ${weekdays[date.getDay()]}`;
}

function groupFutureReviewTasksByDate(tasks) {
  const grouped = new Map();
  [...tasks]
    .sort((left, right) => {
      const leftDate = reviewTaskDueDate(left) || "";
      const rightDate = reviewTaskDueDate(right) || "";
      const byDate = reviewTaskDateTimestamp(leftDate) - reviewTaskDateTimestamp(rightDate);
      if (byDate !== 0) return byDate;
      return reviewTaskTitle(left).localeCompare(reviewTaskTitle(right), "zh-Hans-CN");
    })
    .forEach((task) => {
      const dateKey = reviewTaskDueDate(task) || "unscheduled";
      if (!grouped.has(dateKey)) grouped.set(dateKey, []);
      grouped.get(dateKey).push(task);
    });
  return [...grouped.entries()].map(([dateKey, items]) => ({ dateKey, items }));
}

function reviewTaskEstimatedMinutes(task) {
  const parsed = Number(task?.estimated_minutes || task?.minutes || 0);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

function futureReviewDateGroupMinutes(items) {
  return items.reduce((sum, task) => sum + reviewTaskEstimatedMinutes(task), 0);
}

function groupedReviewTasks() {
  const groups = {
    overdue: [],
    today: [],
    future: [],
    completed: [],
    cancelled: [],
  };
  reviewTasksState.items.forEach((task) => {
    groups[reviewTaskDateGroup(task)].push(task);
  });
  return groups;
}

function reviewTaskPlanModeLabel(mode) {
  const normalized = String(mode || "").trim();
  const match = AI_REVIEW_PLAN_MODES.find((item) => item.value === normalized);
  return match?.label || normalized || "AI 规划";
}

function reviewTaskPlanSourceLabel(source) {
  const normalized = String(source || "").trim();
  if (normalized === "llm") return "AI 生成";
  if (normalized === "fallback") return "规则兜底";
  if (normalized === "blocked") return "未调用 AI";
  return normalized || "";
}

function reviewTaskPlanBatchLabel(task) {
  const title = String(task?.plan_batch_title || "").trim();
  if (title) return title;
  const planId = String(task?.plan_id || "").trim();
  if (!planId) return "";
  const shortId = planId.length > 10 ? planId.slice(-10) : planId;
  return `批次 ${shortId}`;
}

function renderReviewTaskPlanMeta(task) {
  const isAiPlanTask = String(task.created_from || "") === "ai_plan" || Boolean(task.plan_id);
  if (!isAiPlanTask) return "";
  const chips = ["来自 AI 规划"];
  const batchLabel = reviewTaskPlanBatchLabel(task);
  if (batchLabel) chips.push(`规划批次：${batchLabel}`);
  if (task.plan_mode) chips.push(`${reviewTaskPlanModeLabel(task.plan_mode)}模式`);
  if (task.plan_model) chips.push(String(task.plan_model));
  const sourceLabel = reviewTaskPlanSourceLabel(task.plan_source);
  if (sourceLabel) chips.push(sourceLabel);
  if (task.estimated_minutes) chips.push(`预计 ${task.estimated_minutes} 分钟`);
  const reason = String(task.plan_reason || "").trim();
  return `
    <div class="review-task-plan-meta" aria-label="AI 规划来源">
      ${chips.map((chip) => `<span${chip.startsWith("规划批次：") ? ' class="review-task-plan-batch"' : ""}>${escapeHtml(chip)}</span>`).join("")}
    </div>
    ${reason ? `<p class="review-task-plan-reason">安排理由：${escapeHtml(reason)}</p>` : ""}
  `;
}

function renderReviewTaskActions(id, status) {
  const completed = status === "completed" || status === "done";
  const cancelled = status === "cancelled" || status === "canceled";
  const inactive = completed || cancelled;
  return `
    <div class="review-task-actions">
      <button type="button" class="small-button dark-button" data-review-task-open="${escapeHtml(id)}">开始复习</button>
      ${inactive ? `<button type="button" class="small-button" data-review-task-restore="${escapeHtml(id)}">恢复</button>` : ""}
      ${inactive ? "" : `<button type="button" class="small-button dark-button" data-review-task-complete="${escapeHtml(id)}">完成</button>`}
      ${inactive ? "" : `<button type="button" class="small-button" data-review-task-postpone="${escapeHtml(id)}">推迟</button>`}
      ${inactive ? "" : `<button type="button" class="small-button" data-review-task-cancel="${escapeHtml(id)}">取消</button>`}
      <button type="button" class="small-button" data-review-task-delete="${escapeHtml(id)}">删除</button>
    </div>
  `;
}

function renderReviewTaskCard(task) {
  const id = reviewTaskId(task);
  const status = reviewTaskStatus(task);
  const dueDate = reviewTaskDueDate(task) || "未设置日期";
  const priority = task.priority || "normal";
  const note = task.note || task.personal_note || "";
  const completed = status === "completed" || status === "done";
  const targetType = String(task.target_type || "");
  const isAiPlanTask = String(task.created_from || "") === "ai_plan" || Boolean(task.plan_id);
  const sourceMeta = task.source_meta && typeof task.source_meta === "object" ? task.source_meta : {};
  const learningReasons = Array.isArray(task.learning_reasons) ? task.learning_reasons : [];
  const sourceText = [
    task.subject,
    task.library_name,
    sourceMeta.question_count ? `${sourceMeta.question_count} 题` : "",
  ].filter(Boolean).join(" · ");
  return `
    <article class="review-task-card">
      <div class="review-task-main">
        <div class="review-task-title-row">
          <strong>${escapeHtml(reviewTaskTitle(task))}</strong>
          ${reviewTaskDateGroup(task) === "future" && reviewTaskDueDate(task) ? `<span class="review-task-date-pill">${escapeHtml(reviewTaskCompactDateLabel(reviewTaskDueDate(task)))}</span>` : ""}
          <span class="status-pill ${completed ? "mastered" : "learning"}">${escapeHtml(reviewTaskStatusLabel(status))}</span>
          <span class="status-pill type">${escapeHtml(reviewTaskTargetTypeLabel(targetType))}</span>
        </div>
        <div class="system-detail-meta">
          <span>到期：${escapeHtml(dueDate)}</span>
          <span>${escapeHtml(reviewTaskPriorityLabel(priority))}</span>
          ${sourceText ? `<span>${escapeHtml(sourceText)}</span>` : ""}
        </div>
        ${!isAiPlanTask && note ? `<p>${escapeHtml(note)}</p>` : ""}
        ${renderReviewTaskPlanMeta(task)}
        ${learningReasons.length ? `
          <div class="review-task-reasons" aria-label="复习原因">
            ${learningReasons.map((reason) => `<span>${escapeHtml(reason.label || "")}</span>`).join("")}
          </div>
        ` : ""}
      </div>
      ${renderReviewTaskActions(id, status)}
    </article>
  `;
}

function isReviewTaskSectionCollapsed(group) {
  const key = String(group || "");
  if (!key) return false;
  if (!(key in reviewTaskSectionCollapsed)) {
    reviewTaskSectionCollapsed[key] = Boolean(REVIEW_TASK_SECTION_DEFAULT_COLLAPSED[key]);
  }
  return Boolean(reviewTaskSectionCollapsed[key]);
}

function reviewTaskSectionToggleLabel(collapsed) {
  return collapsed ? "展开" : "收起";
}

function renderReviewTaskSectionHeader(title, tasks, group, collapsed) {
  return `
      <header class="review-task-section-header">
        <h4>${escapeHtml(title)}</h4>
        <button
          type="button"
          class="review-task-section-toggle"
          data-review-task-section-toggle="${escapeHtml(group)}"
          aria-expanded="${escapeHtml(String(!collapsed))}"
        >
          <span class="review-task-section-count">${escapeHtml(String(tasks.length))}</span>
          <span data-review-task-section-toggle-label>${escapeHtml(reviewTaskSectionToggleLabel(collapsed))}</span>
        </button>
      </header>
  `;
}

function setReviewTaskSectionDomCollapsed(group, collapsed) {
  if (!reviewTaskList) return;
  const sections = [...reviewTaskList.querySelectorAll("[data-review-task-group]")];
  const section = sections.find((item) => item.dataset.reviewTaskGroup === group);
  if (!section) return;
  section.classList.toggle("is-collapsed", collapsed);
  const toggle = section.querySelector("[data-review-task-section-toggle]");
  if (toggle) {
    toggle.setAttribute("aria-expanded", String(!collapsed));
    const label = toggle.querySelector("[data-review-task-section-toggle-label]");
    if (label) label.textContent = reviewTaskSectionToggleLabel(collapsed);
  }
}

function toggleReviewTaskSection(group) {
  const key = String(group || "");
  if (!key) return;
  reviewTaskSectionCollapsed[key] = !isReviewTaskSectionCollapsed(key);
  setReviewTaskSectionDomCollapsed(key, reviewTaskSectionCollapsed[key]);
}

function expandReviewTaskSection(group) {
  const key = String(group || "");
  if (!key) return;
  reviewTaskSectionCollapsed[key] = false;
  setReviewTaskSectionDomCollapsed(key, false);
}

function renderFutureReviewTaskSection(title, tasks, group = "") {
  const dateGroups = groupFutureReviewTasksByDate(tasks);
  const collapsed = isReviewTaskSectionCollapsed(group);
  return `
    <section class="review-task-section review-task-section-future ${collapsed ? "is-collapsed" : ""}" data-review-task-group="${escapeHtml(group)}">
      ${renderReviewTaskSectionHeader(title, tasks, group, collapsed)}
      ${tasks.length ? dateGroups.map(({ dateKey, items }, index) => {
        const minutes = futureReviewDateGroupMinutes(items);
        return `
          <details class="review-future-date-group" ${index < 3 ? "open" : ""}>
            <summary>
              <span class="review-date-anchor">
                <strong>${escapeHtml(dateKey === "unscheduled" ? "未设置日期" : reviewTaskDateGroupLabel(dateKey))}</strong>
                <span class="review-date-count-pill">${escapeHtml(`${items.length} 个任务`)}</span>
                ${minutes ? `<span class="review-date-load-pill">${escapeHtml(`预计 ${minutes} 分钟`)}</span>` : ""}
              </span>
              <span class="review-date-toggle">展开/收起</span>
            </summary>
            <div class="review-future-date-list">
              ${items.map(renderReviewTaskCard).join("")}
            </div>
          </details>
        `;
      }).join("") : '<div class="empty-state">暂无任务</div>'}
    </section>
  `;
}

function renderReviewTaskSection(title, tasks, group = "") {
  const collapsed = isReviewTaskSectionCollapsed(group);
  return `
    <section class="review-task-section ${collapsed ? "is-collapsed" : ""}" data-review-task-group="${escapeHtml(group)}">
      ${renderReviewTaskSectionHeader(title, tasks, group, collapsed)}
      ${tasks.length ? tasks.map(renderReviewTaskCard).join("") : '<div class="empty-state">暂无任务</div>'}
    </section>
  `;
}

function scrollReviewTaskGroupIntoView(group) {
  expandReviewTaskSection(group);
  const sections = reviewTaskList ? [...reviewTaskList.querySelectorAll("[data-review-task-group]")] : [];
  const section = sections.find((item) => item.dataset.reviewTaskGroup === group);
  if (!section) return false;
  section.scrollIntoView({ behavior: "smooth", block: "start" });
  section.classList.add("is-focused");
  window.setTimeout(() => section.classList.remove("is-focused"), 2300);
  return true;
}

function learningTopicReasonTags(topic) {
  return renderPriorityReasonTags(topic?.priority_reasons || []);
}

function renderReviewLearningInsights() {
  if (!reviewLearningInsights) return;
  if (reviewTasksState.insightsLoading) {
    reviewLearningInsights.className = "review-learning-insights empty-state";
    reviewLearningInsights.textContent = "正在读取学习记录...";
    return;
  }
  if (reviewTasksState.insightsError) {
    reviewLearningInsights.className = "review-learning-insights empty-state";
    reviewLearningInsights.textContent = `学习洞察加载失败：${reviewTasksState.insightsError}`;
    return;
  }
  const insights = reviewTasksState.learningInsights || {};
  const summary = insights.summary && typeof insights.summary === "object" ? insights.summary : {};
  const reviewSummary = insights.review_summary && typeof insights.review_summary === "object" ? insights.review_summary : {};
  const weakTopics = Array.isArray(insights.weak_topics) ? insights.weak_topics : [];
  const nextActions = Array.isArray(insights.next_actions) ? insights.next_actions : [];
  const hasData = Number(summary.question_attempt_count || 0) > 0
    || Number(summary.draft_attempt_count || 0) > 0
    || weakTopics.length
    || Number(reviewSummary.total || 0) > 0;
  if (!hasData) {
    reviewLearningInsights.className = "review-learning-insights muted";
    reviewLearningInsights.innerHTML = `
      <header>
        <div>
          <h4>学习概览</h4>
          <p>还没有可分析的练习记录。完成一次练习后，这里会显示错题、待核对题和薄弱知识点。</p>
        </div>
        <span class="status-pill learning">待积累</span>
      </header>
    `;
    return;
  }
  const wrongRecordCount = Number(summary.incorrect_count || 0) + Number(summary.partial_count || 0);
  const uniqueWrongQuestionCount = Number(summary.unique_wrong_question_count || 0) || wrongRecordCount;
  const metrics = [
    ["练习", summary.practice_attempt_count || 0],
    ["草稿", summary.draft_attempt_count || 0],
    ["题次", summary.question_attempt_count || 0],
    ["正确", summary.correct_count || 0],
    ["错题", uniqueWrongQuestionCount],
    ["错误记录", wrongRecordCount],
    ["待核对题", summary.pending_review_question_count || summary.pending_review_count || 0],
    ["到期", reviewSummary.due_count || 0],
  ];
  reviewLearningInsights.className = "review-learning-insights";
  reviewLearningInsights.innerHTML = `
    <header>
      <div>
        <h4>学习概览</h4>
        <p>${escapeHtml(reviewTasksState.filters.subject ? "当前学科的练习记录与复习任务摘要。" : "全部学科的练习记录与复习任务摘要。")}</p>
      </div>
      <span class="status-pill mastered">已同步</span>
    </header>
    <div class="review-learning-header-actions">
      <button type="button" class="small-button" data-review-ai-plan>让 AI 排计划</button>
    </div>
    <div class="review-learning-metrics">
      ${metrics.map(([label, value]) => `<span>${escapeHtml(label)} <strong>${escapeHtml(String(value))}</strong></span>`).join("")}
    </div>
    ${weakTopics.length ? `
      <section class="review-learning-block">
        <h4>薄弱知识点 Top ${weakTopics.length}</h4>
        <div class="review-learning-topic-list">
          ${weakTopics.map((topic) => `
            <article
              class="review-learning-topic"
              tabindex="0"
              role="button"
              data-learning-topic-card
              data-learning-topic="${escapeHtml(topic.topic || "")}"
              aria-label="查看知识点处理：${escapeHtml(topic.topic || "未命名知识点")}"
            >
              <strong>${escapeHtml(topic.topic || "未命名知识点")}</strong>
              <span>优先级：${escapeHtml(learningPriorityLabel(topic.priority_score))}</span>
              <p>共练 ${escapeHtml(String(topic.attempt_count || 0))} 次：错题 ${escapeHtml(String(topic.wrong_count || 0))} 次，待核对 ${escapeHtml(String(topic.pending_review_count || 0))} 次，未答 ${escapeHtml(String(topic.unanswered_count || 0))} 次，判断可信度：${escapeHtml(learningConfidenceLabel(topic.confidence))}</p>
              ${learningTopicReasonTags(topic)}
              <span class="learning-topic-card-action">查看处理</span>
            </article>
          `).join("")}
        </div>
      </section>
    ` : ""}
    ${nextActions.length ? `
      <section class="review-learning-block">
        <h4>下一步建议</h4>
        <div class="review-learning-actions">
          ${nextActions.map((action) => `
            <button
              type="button"
              class="review-insight-action"
              data-review-insight-action="${escapeHtml(action.type || "")}"
              data-review-insight-status="${escapeHtml(action.status || "")}"
              data-review-insight-topic="${escapeHtml(action.topic || "")}"
            >
              ${escapeHtml(action.label || "")}
            </button>
          `).join("")}
        </div>
      </section>
    ` : ""}
  `;
}

function learningPriorityLabel(value) {
  const score = Number(value || 0);
  if (score >= 0.75) return "很高";
  if (score >= 0.55) return "高";
  if (score >= 0.35) return "中";
  return "低";
}

function learningConfidenceLabel(value) {
  const confidence = Number(value || 0);
  if (confidence >= 0.85) return "高";
  if (confidence >= 0.5) return "中";
  return "低";
}

function renderReviewTasksLegacy() {
  if (!reviewTaskList) return;
  if (reviewTasksState.loading) {
    reviewTaskList.className = "review-task-list empty-state";
    reviewTaskList.textContent = "正在加载复习任务...";
    return;
  }
  if (reviewTasksState.error) {
    reviewTaskList.className = "review-task-list empty-state";
    reviewTaskList.textContent = `复习任务加载失败：${reviewTasksState.error}`;
    return;
  }
  const groups = groupedReviewTasks();
  reviewTaskList.className = "review-task-list";
  reviewTaskList.innerHTML = [
    renderReviewTaskSection("逾期", groups.overdue, "overdue"),
    renderReviewTaskSection("今日", groups.today, "today"),
    renderReviewTaskSection("未来", groups.future, "future"),
    renderReviewTaskSection("已完成 / 已取消", groups.completed, "completed"),
    renderReviewTaskSection("已取消", groups.cancelled, "cancelled"),
  ].join("");
}

function renderReviewTasks() {
  if (!reviewTaskList) return;
  if (reviewTasksState.loading) {
    reviewTaskList.className = "review-task-list empty-state";
    reviewTaskList.textContent = "正在加载复习任务...";
    return;
  }
  if (reviewTasksState.error) {
    reviewTaskList.className = "review-task-list empty-state";
    reviewTaskList.textContent = `复习任务加载失败：${reviewTasksState.error}`;
    return;
  }
  const groups = groupedReviewTasks();
  reviewTaskList.className = "review-task-list";
  reviewTaskList.innerHTML = [
    renderReviewTaskSection("逾期", groups.overdue, "overdue"),
    renderReviewTaskSection("今日", groups.today, "today"),
    renderFutureReviewTaskSection("未来", groups.future, "future"),
    renderReviewTaskSection("已完成", groups.completed, "completed"),
    renderReviewTaskSection("已取消", groups.cancelled, "cancelled"),
  ].join("");
}

function nextReviewDateFromTask(task, days = 1) {
  const rawDate = reviewTaskDueDate(task);
  const base = rawDate ? new Date(`${rawDate}T00:00:00`) : new Date();
  base.setDate(base.getDate() + days);
  return base.toISOString().slice(0, 10);
}

async function patchReviewTask(taskId, patch, successMessage) {
  if (!taskId) return;
  try {
    await fetchJson(`/api/materials/system/review-tasks/${encodeURIComponent(taskId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    });
    setReviewTasksStatus("saved", successMessage);
    await loadReviewTasks({ silent: true });
    await loadReviewLearningInsights({ silent: true });
  } catch (error) {
    setReviewTasksStatus("error", `复习任务更新失败：${error.message}`);
  }
}

async function markReviewTaskStarted(task) {
  const taskId = reviewTaskId(task);
  if (!taskId) return null;
  try {
    const data = await fetchJson(`/api/materials/system/review-tasks/${encodeURIComponent(taskId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ feedback_action: "started" }),
    });
    return data.review_task || data;
  } catch (error) {
    setReviewTasksStatus("error", `复习开始记录失败：${error.message}`);
    return null;
  }
}

async function deleteReviewTask(taskId) {
  if (!taskId) return;
  if (!window.confirm("确定删除这个复习任务吗？删除后不可恢复。")) return;
  try {
    await fetchJson(`/api/materials/system/review-tasks/${encodeURIComponent(taskId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
      method: "DELETE",
    });
    setReviewTasksStatus("saved", "复习任务已删除");
    await loadReviewTasks({ silent: true });
    await loadReviewLearningInsights({ silent: true });
  } catch (error) {
    setReviewTasksStatus("error", `复习任务删除失败：${error.message}`);
  }
}

function openReviewTaskPostponeDialog(task) {
  const taskId = reviewTaskId(task);
  if (!taskId) return;
  const fallbackDate = nextReviewDateFromTask(task, 1);
  const { overlay, close } = createSystemWorkflowOverlay("推迟复习", "选择新的复习日期，保存后任务会移动到对应时间分组。");
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  body.innerHTML = `
    <div class="workflow-form-grid">
      <label class="field">
        <span>任务</span>
        <input type="text" value="${escapeHtml(reviewTaskTitle(task))}" readonly>
      </label>
      <label class="field">
        <span>新的复习日期</span>
        <input type="date" value="${escapeHtml(fallbackDate)}" data-review-postpone-date>
      </label>
    </div>
    <div class="system-workflow-actions">
      <button type="button" class="small-button" data-review-postpone-cancel>取消</button>
      <button type="button" class="small-button dark-button" data-review-postpone-save>保存</button>
    </div>
  `;
  body.querySelector("[data-review-postpone-cancel]")?.addEventListener("click", close);
  body.querySelector("[data-review-postpone-save]")?.addEventListener("click", () => {
    const input = body.querySelector("[data-review-postpone-date]");
    const dueAt = String(input?.value || "").trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dueAt)) {
      setReviewTasksStatus("error", "请选择有效的复习日期");
      return;
    }
    close();
    void patchReviewTask(taskId, { status: "pending", due_at: dueAt, feedback_action: "postponed" }, "复习任务已推迟");
  });
}

function handleReviewTaskAction(event) {
  const sectionToggle = event.target.closest("[data-review-task-section-toggle]");
  if (sectionToggle && reviewTaskList?.contains(sectionToggle)) {
    toggleReviewTaskSection(sectionToggle.dataset.reviewTaskSectionToggle);
    return;
  }
  const button = event.target.closest("[data-review-task-open], [data-review-task-complete], [data-review-task-postpone], [data-review-task-cancel], [data-review-task-restore], [data-review-task-delete]");
  if (!button) return;
  const taskId = button.dataset.reviewTaskOpen
    || button.dataset.reviewTaskComplete
    || button.dataset.reviewTaskPostpone
    || button.dataset.reviewTaskCancel
    || button.dataset.reviewTaskRestore
    || button.dataset.reviewTaskDelete;
  const task = reviewTasksState.items.find((item) => reviewTaskId(item) === taskId) || {};
  if (button.dataset.reviewTaskOpen) {
    void openReviewTaskSource(task);
    return;
  }
  if (button.dataset.reviewTaskComplete) {
    void patchReviewTask(taskId, { status: "completed", completed_at: new Date().toISOString(), feedback_action: "completed" }, "复习任务已完成");
    return;
  }
  if (button.dataset.reviewTaskPostpone) {
    openReviewTaskPostponeDialog(task);
    return;
  }
  if (button.dataset.reviewTaskCancel) {
    void patchReviewTask(taskId, { status: "cancelled", feedback_action: "cancelled" }, "复习任务已取消");
    return;
  }
  if (button.dataset.reviewTaskRestore) {
    void patchReviewTask(taskId, { status: "pending", feedback_action: "restored" }, "复习任务已恢复");
    return;
  }
  if (button.dataset.reviewTaskDelete) {
    void deleteReviewTask(taskId);
  }
}

function aiReviewPlanConstraints() {
  return {
    subject: reviewTasksState.filters.subject || "math",
    days: 7,
    daily_minutes: 60,
    goal: "补弱优先",
  };
}

function aiReviewPlanQuery(constraints) {
  return new URLSearchParams({
    user_id: currentMaterialsUserId(),
    subject: constraints.subject,
    days: String(constraints.days),
    daily_minutes: String(constraints.daily_minutes),
    goal: constraints.goal,
  });
}

function aiPlanCountBadge(label, value) {
  return `<span><strong>${escapeHtml(String(value || 0))}</strong>${escapeHtml(label)}</span>`;
}

function aiReviewPlanModeConfig(mode) {
  return AI_REVIEW_PLAN_MODES.find((item) => item.value === mode) || AI_REVIEW_PLAN_MODES[0];
}

function aiReviewPlanDefaultMode(context = {}) {
  const summary = context.summary || {};
  const wrongCount = Number(summary.unique_wrong_question_count || summary.incorrect_count || 0);
  const practiceCount = Number(summary.practice_attempt_count || 0);
  if (!practiceCount && !wrongCount) return "startup";
  if (wrongCount >= 5) return "wrong";
  return "balanced";
}

function aiReviewPlanDefaultIncludes(mode) {
  return AI_REVIEW_PLAN_INCLUDE_OPTIONS
    .filter((item) => item.modes.includes(mode) && item.defaults.includes(mode))
    .map((item) => item.value);
}

function aiReviewPlanIncludeLabels(values = []) {
  const selected = new Set(values);
  return AI_REVIEW_PLAN_INCLUDE_OPTIONS
    .filter((item) => selected.has(item.value))
    .map((item) => item.label);
}

const AI_REVIEW_PLAN_INCLUDE_CANDIDATE_GROUPS = {
  due_tasks: {
    candidateKeys: ["review_tasks"],
    limitKeys: ["ai_review_task_limit"],
  },
  wrong_questions: {
    candidateKeys: ["wrong_questions"],
    limitKeys: ["ai_wrong_question_limit"],
  },
  pending_review: {
    candidateKeys: ["pending_review_items"],
    limitKeys: ["ai_pending_review_limit"],
  },
  weak_topics: {
    candidateKeys: ["weak_topics"],
    limitKeys: ["ai_weak_topic_limit"],
  },
  unstarted: {
    candidateKeys: ["unstarted_questions", "startup_candidates"],
    limitKeys: ["ai_unstarted_question_limit", "ai_startup_candidate_limit"],
  },
  draft_attempts: {
    candidateKeys: ["draft_attempts"],
    limitKeys: ["ai_draft_attempt_limit"],
  },
  favorite_unmastered: {
    candidateKeys: ["favorite_unmastered"],
    limitKeys: ["ai_favorite_unmastered_limit"],
  },
};

function aiReviewPlanCandidateArrayCount(candidates, key) {
  const value = candidates?.[key];
  return Array.isArray(value) ? value.length : 0;
}

function aiReviewPlanCandidateLimitTotal(limits, keys = []) {
  return keys.reduce((sum, key) => {
    const value = Number(limits?.[key] || 0);
    return Number.isFinite(value) ? sum + value : sum;
  }, 0);
}

function aiReviewPlanCandidateAvailability(state, context = {}) {
  const selected = Array.isArray(state.includeTypes) ? state.includeTypes : [];
  const candidates = context.ai_candidates || {};
  const limits = context.limits || {};
  const policy = context.policy || {};
  const ignoredTypes = new Set(Array.isArray(policy.ignored_requested_types) ? policy.ignored_requested_types : []);
  return selected.map((value) => {
    const option = AI_REVIEW_PLAN_INCLUDE_OPTIONS.find((item) => item.value === value);
    const group = AI_REVIEW_PLAN_INCLUDE_CANDIDATE_GROUPS[value] || { candidateKeys: [], limitKeys: [] };
    const count = group.candidateKeys.reduce((sum, key) => sum + aiReviewPlanCandidateArrayCount(candidates, key), 0);
    const limit = aiReviewPlanCandidateLimitTotal(limits, group.limitKeys);
    const ignored = group.candidateKeys.some((key) => ignoredTypes.has(key));
    const enabled = option ? option.modes.includes(state.mode) : true;
    return {
      value,
      label: option?.label || value,
      count,
      limit,
      ignored,
      enabled,
    };
  });
}

function renderAiReviewPlanCandidateAvailability(state, context = {}) {
  const rows = aiReviewPlanCandidateAvailability(state, context);
  if (!rows.length) return "";
  const emptyRows = rows.filter((row) => row.enabled && !row.ignored && row.count <= 0);
  const rowMarkup = rows.map((row) => {
    const disabled = !row.enabled || row.ignored;
    const className = disabled ? "disabled" : row.count > 0 ? "ok" : "empty";
    const detail = disabled
      ? "当前模式未纳入"
      : `可用 ${row.count} / 送 AI 上限 ${row.limit || row.count}`;
    return `
      <span class="ai-plan-availability-chip ${className}">
        <strong>${escapeHtml(row.label)}</strong>
        <em>${escapeHtml(detail)}</em>
      </span>
    `;
  }).join("");
  return `
    <div class="ai-plan-availability">
      <div class="ai-plan-meta">
        <strong>本次可用候选</strong>
        <span>送 AI 上限只控制输入规模，最终题量按每日时长生成</span>
      </div>
      <div class="ai-plan-availability-list">${rowMarkup}</div>
      ${emptyRows.length ? `<p class="ai-plan-availability-empty">已勾选但暂无候选：${escapeHtml(emptyRows.map((row) => row.label).join("、"))}。这类内容不会出现在本次 AI 草案里。</p>` : ""}
    </div>
  `;
}

function formatPriorityScore(value) {
  const score = Number(value || 0);
  if (!Number.isFinite(score)) return "0";
  return score.toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function aiReviewPlanCandidateRows(mode, context = {}) {
  const candidates = context.ai_candidates || {};
  const weakTopics = Array.isArray(candidates.weak_topics) ? candidates.weak_topics : [];
  const wrongQuestions = Array.isArray(candidates.wrong_questions) ? candidates.wrong_questions : [];
  const pendingItems = Array.isArray(candidates.pending_review_items) ? candidates.pending_review_items : [];
  const reviewTasks = Array.isArray(candidates.review_tasks) ? candidates.review_tasks : [];
  const draftAttempts = Array.isArray(candidates.draft_attempts) ? candidates.draft_attempts : [];
  if (mode === "startup") {
    return [
      { type: "起步", title: "按考试范围预选基础题", reason: "历史数据不足时，后端按数一/数二/数三、题库顺序、基础知识点和题型配比抽样。" },
      { type: "起步", title: "未开始/未掌握题", reason: "只给 AI 压缩后的起步候选，不把全量未开始题塞进提示词。" },
      { type: "起步", title: "收藏但未掌握", reason: "用户手动标记会提高候选优先级。" },
    ];
  }
  const rows = [];
  weakTopics.slice(0, mode === "wrong" ? 1 : 3).forEach((topic) => {
    rows.push({
      type: "知识点",
      title: topic.topic || "薄弱知识点",
      reason: `优先级 ${formatPriorityScore(topic.priority_score)}，错题 ${Number(topic.wrong_count || topic.incorrect_count || 0)} 次，待核对 ${Number(topic.pending_review_count || 0)} 次。`,
    });
  });
  wrongQuestions.slice(0, 3).forEach((question) => {
    rows.push({
      type: "错题",
      title: question.title || systemQuestionTitle(question),
      reason: question.reason || `优先级 ${formatPriorityScore(question.priority_score)}，适合回收。`,
    });
  });
  pendingItems.slice(0, 2).forEach((item) => {
    rows.push({
      type: "待核对",
      title: item.title || item.question_title || "待核对题",
      reason: "本地无法确认等价表达，需要 AI 或人工确认。",
    });
  });
  reviewTasks.slice(0, 2).forEach((task) => {
    rows.push({
      type: "任务",
      title: task.title || task.task_title || "复习任务",
      reason: task.due_at ? `到期：${task.due_at}` : "已加入复习规划。",
    });
  });
  draftAttempts.slice(0, 1).forEach((draft) => {
    rows.push({
      type: "草稿",
      title: draft.title || draft.practice_set_title || "未提交练习",
      reason: "已有作答草稿，可继续完成或稍后处理。",
    });
  });
  if (!rows.length) {
    rows.push({ type: "候选", title: "暂无足够历史数据", reason: "可以切换到新题启动，使用起步候选生成计划。" });
  }
  return rows.slice(0, 6);
}

function aiReviewPlanCandidateExplain(mode) {
  if (mode === "wrong") {
    return "错题回收候选只来自错题、待核对题和到期错题任务；未开始题会被禁用，避免目标混杂。";
  }
  if (mode === "startup") {
    return "起步候选用于冷启动或新范围：后端按考试范围、题库结构顺序、基础知识点、题型配比和用户偏好预选候选。";
  }
  if (mode === "weak") {
    return "薄弱候选优先按知识点风险排序，再带上代表错题、待核对题和近期趋势。";
  }
  if (mode === "sprint") {
    return "冲刺候选限制新题比例，优先到期、错题、薄弱和收藏未掌握内容。";
  }
  return "均衡候选会压缩读取到期任务、错题、薄弱点、草稿和少量新题，避免把全量历史直接丢给 AI。";
}

function aiReviewPlanStateFromContext(constraints, context) {
  const mode = aiReviewPlanDefaultMode(context);
  return {
    ...constraints,
    mode,
    includeTypes: aiReviewPlanDefaultIncludes(mode),
    context,
  };
}

function renderAiReviewPlanStepper(step) {
  const steps = [
    ["settings", "设置范围"],
    ["draft", "生成草案"],
    ["result", "确认结果"],
  ];
  return `<div class="ai-plan-stepper">${steps.map(([value, label]) => `
    <span class="${value === step ? "active" : ""}">${escapeHtml(label)}</span>
  `).join("")}</div>`;
}

function renderAiReviewPlanSettings(body, state) {
  const context = state.context || {};
  const summary = context.summary || {};
  const reviewSummary = context.review_summary || {};
  const limits = context.limits || {};
  const candidates = context.ai_candidates || {};
  const weakTopics = Array.isArray(candidates.weak_topics) ? candidates.weak_topics : [];
  const wrongQuestions = Array.isArray(candidates.wrong_questions) ? candidates.wrong_questions : [];
  const pendingItems = Array.isArray(candidates.pending_review_items) ? candidates.pending_review_items : [];
  const reviewTasks = Array.isArray(candidates.review_tasks) ? candidates.review_tasks : [];
  const draftAttempts = Array.isArray(candidates.draft_attempts) ? candidates.draft_attempts : [];
  const readiness = context.readiness || {};
  const candidateSummary = context.candidate_summary || {};
  const readinessStatus = String(readiness.status || "unknown");
  const readinessLabel = {
    ready: "可生成",
    weak: "数据偏少",
    blocked: "暂不建议生成",
  }[readinessStatus] || "未评估";
  const readinessReason = readiness.reason || "后端会先检查当前模式是否有足够候选，再决定是否调用 AI。";
  const filteredTotal = Number(candidateSummary.filtered_total || 0);
  const rawTotal = Number(candidateSummary.raw_total || 0);
  const mode = aiReviewPlanModeConfig(state.mode);
  const includeSet = new Set(state.includeTypes || []);
  const includeOptionsMarkup = AI_REVIEW_PLAN_INCLUDE_OPTIONS.map((item) => {
    const enabled = item.modes.includes(state.mode);
    const checked = enabled && includeSet.has(item.value);
    return `
      <label class="ai-plan-include-card${enabled ? "" : " disabled"}">
        <input type="checkbox" data-ai-review-plan-include="${escapeHtml(item.value)}" ${checked ? "checked" : ""} ${enabled ? "" : "disabled"}>
        <span>${escapeHtml(item.label)}</span>
      </label>
    `;
  }).join("");
  const candidateRows = aiReviewPlanCandidateRows(state.mode, context);
  body.innerHTML = `
    <section class="ai-plan-context" data-ai-plan-step="settings">
      ${renderAiReviewPlanStepper("settings")}
      <div class="ai-plan-context-grid">
        ${aiPlanCountBadge("练习", summary.practice_attempt_count)}
        ${aiPlanCountBadge("题次", summary.question_attempt_count)}
        ${aiPlanCountBadge("错题", summary.unique_wrong_question_count || summary.incorrect_count)}
        ${aiPlanCountBadge("待核对", summary.pending_review_question_count || summary.pending_review_count)}
        ${aiPlanCountBadge("到期任务", reviewSummary.due_count)}
        ${aiPlanCountBadge("草稿", summary.draft_attempt_count)}
      </div>
      <div class="ai-plan-card ai-plan-readiness" data-ai-plan-readiness="${escapeHtml(readinessStatus)}">
        <div class="ai-plan-meta">
          <strong>生成可行性：${escapeHtml(readinessLabel)}</strong>
          <span>候选 ${escapeHtml(String(filteredTotal))}/${escapeHtml(String(rawTotal))} · 核心 ${escapeHtml(String(readiness.core_available || 0))}/${escapeHtml(String(readiness.core_required || 0))}</span>
        </div>
        <p>${escapeHtml(readinessReason)}</p>
      </div>
      <div class="ai-plan-card">
        <h4>规划依据范围</h4>
        <p>页面只展示少量 Top 项；AI 规划会读取更宽的候选池：薄弱知识点 Top ${escapeHtml(String(limits.ai_weak_topic_limit || weakTopics.length))}、错题 Top ${escapeHtml(String(limits.ai_wrong_question_limit || wrongQuestions.length))}、待核对 Top ${escapeHtml(String(limits.ai_pending_review_limit || pendingItems.length))}、任务 Top ${escapeHtml(String(limits.ai_review_task_limit || reviewTasks.length))}、未提交练习 Top ${escapeHtml(String(limits.ai_draft_attempt_limit || draftAttempts.length))}。</p>
      </div>
      <div class="ai-plan-card">
        <h4>规划模式</h4>
        <div class="ai-plan-mode-grid">
          ${AI_REVIEW_PLAN_MODES.map((item) => `
            <button type="button" class="ai-plan-mode-card${item.value === state.mode ? " active" : ""}" data-ai-review-plan-mode="${escapeHtml(item.value)}">
              <strong>${escapeHtml(item.label)}</strong>
              <span>${escapeHtml(item.hint)}</span>
            </button>
          `).join("")}
        </div>
      </div>
      <div class="ai-plan-card">
        <h4>纳入内容</h4>
        <p>${escapeHtml(mode.hint)}</p>
        <div class="ai-plan-include-grid">${includeOptionsMarkup}</div>
      </div>
      <div class="ai-plan-card">
        <div class="ai-plan-meta">
          <strong>${escapeHtml(mode.candidateTitle)}</strong>
          <span>${escapeHtml(mode.candidateCountLabel)}</span>
        </div>
        <p>${escapeHtml(aiReviewPlanCandidateExplain(state.mode))}</p>
        <div class="ai-plan-candidate-list">
          ${candidateRows.map((row) => `
            <article class="ai-plan-candidate">
              <span>${escapeHtml(row.type)}</span>
              <div>
                <strong>${escapeHtml(row.title)}</strong>
                <p>${escapeHtml(row.reason)}</p>
              </div>
            </article>
          `).join("")}
        </div>
      </div>
      <div class="ai-plan-card">
        <h4>计划约束</h4>
        <div class="ai-plan-form-grid">
          <label>规划天数
            <input type="number" min="1" max="21" value="${escapeHtml(String(state.days || 7))}" data-ai-review-plan-days>
          </label>
          <label>每天时长（分钟）
            <input type="number" min="10" max="240" step="5" value="${escapeHtml(String(state.daily_minutes || 60))}" data-ai-review-plan-minutes>
          </label>
        </div>
      </div>
      <div class="system-workflow-actions">
        <button type="button" class="small-button dark-button" data-ai-review-plan-draft>生成 AI 草案</button>
      </div>
    </section>
  `;
}

function aiReviewPlanDraftItems(payload) {
  const draft = payload?.draft || {};
  const days = Array.isArray(draft.days) ? draft.days : [];
  const items = [];
  days.forEach((day, dayIndex) => {
    const dayItems = Array.isArray(day.items) ? day.items : [];
    dayItems.forEach((item, itemIndex) => {
      if (!item || typeof item !== "object") return;
      const key = `${dayIndex}:${itemIndex}`;
      items.push({
        key,
        date: day.date || day.label || "",
        item: { ...item, date: item.date || day.date || day.label || "", _commit_key: key },
      });
    });
  });
  return items;
}

function selectedAiReviewPlanItems(body, payload) {
  const draftItems = aiReviewPlanDraftItems(payload);
  const byKey = new Map(draftItems.map((entry) => [entry.key, entry.item]));
  const selectedEntries = [...body.querySelectorAll("[data-ai-review-plan-item-checkbox]:checked")]
    .map((input) => {
      const key = input.dataset.aiReviewPlanItemCheckbox;
      const row = input.closest("[data-ai-review-plan-item]");
      if (!key || !row || row.dataset.aiReviewPlanRemoved === "true") return null;
      const baseItem = byKey.get(key);
      if (!baseItem) return null;
      const item = { ...baseItem, _commit_key: key };
      const dateValue = row.querySelector("[data-ai-review-plan-item-date]")?.value;
      if (dateValue) {
        item.date = dateValue;
        item.due_at = dateValue;
      }
      const minutesValue = Number(row.querySelector("[data-ai-review-plan-item-minutes]")?.value || item.estimated_minutes || item.minutes || 0);
      if (Number.isFinite(minutesValue) && minutesValue > 0) {
        item.estimated_minutes = Math.round(minutesValue);
      }
      return { key, item };
    })
    .filter(Boolean);
  const selectedKeys = selectedEntries.map((entry) => entry.key);
  return {
    selected_item_keys: selectedKeys,
    items: selectedEntries.map((entry) => entry.item),
  };
}

function aiReviewPlanEditableDate(value) {
  const text = String(value || "").slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(text) ? text : "";
}

function aiReviewPlanItemMinutes(item) {
  const minutes = Number(item?.estimated_minutes || item?.minutes || 0);
  if (!Number.isFinite(minutes) || minutes <= 0) return 30;
  return Math.max(5, Math.min(240, Math.round(minutes)));
}

function aiReviewPlanPracticePartLabel(item) {
  const partIndex = Number(item?.part_index || 0);
  const partCount = Number(item?.part_count || 0);
  if (!Number.isFinite(partIndex) || !Number.isFinite(partCount) || partIndex <= 0 || partCount <= 1) {
    return "";
  }
  return `Part ${Math.round(partIndex)}/${Math.round(partCount)}`;
}

function aiReviewPlanItemLoadMeta(item) {
  const parts = [];
  const loadUnits = Number(item?.load_units || 0);
  const questionCount = Number(item?.question_count || 0);
  const partLabel = aiReviewPlanPracticePartLabel(item);
  if (Number.isFinite(loadUnits) && loadUnits > 0) {
    parts.push(`load ${loadUnits.toFixed(1)}`);
  }
  if (Number.isFinite(questionCount) && questionCount > 0) {
    parts.push(`${Math.round(questionCount)} questions`);
  }
  if (partLabel) {
    parts.push(partLabel);
  }
  return parts.length ? `<span class="ai-plan-item-load">${escapeHtml(parts.join(" · "))}</span>` : "";
}

function aiReviewPlanCandidateLookup(context) {
  const candidates = context?.ai_candidates && typeof context.ai_candidates === "object" ? context.ai_candidates : {};
  const lookup = new Map();
  Object.values(candidates).forEach((items) => {
    if (!Array.isArray(items)) return;
    items.forEach((item) => {
      if (!item || typeof item !== "object") return;
      [
        "source_id",
        "candidate_id",
        "plan_segment_id",
        "question_id",
        "task_id",
        "attempt_id",
        "set_id",
        "practice_set_id",
        "topic",
      ].forEach((key) => {
        const value = String(item[key] || "").trim();
        if (value && !lookup.has(value)) {
          lookup.set(value, item);
        }
      });
    });
  });
  return lookup;
}

function aiReviewPlanItemSourceIds(item) {
  const values = [
    ...(Array.isArray(item?.source_ids) ? item.source_ids : []),
    ...(Array.isArray(item?.planned_question_ids) ? item.planned_question_ids : []),
  ];
  const seen = new Set();
  return values
    .map((value) => String(value || "").trim())
    .filter((value) => {
      if (!value || seen.has(value)) return false;
      seen.add(value);
      return true;
    });
}

function aiReviewPlanSourceTitle(sourceId, candidate) {
  const explicitTitle = String(candidate?.title || candidate?.question_title || candidate?.name || "").trim();
  if (explicitTitle) return explicitTitle;
  const questionTitle = candidate ? systemQuestionTitle(candidate) : "";
  return questionTitle || sourceId;
}

function aiReviewPlanSourceMeta(candidate) {
  if (!candidate || typeof candidate !== "object") return "";
  const topics = Array.isArray(candidate.topics)
    ? candidate.topics.slice(0, 3).join(" / ")
    : String(candidate.topic || "").trim();
  const examType = String(candidate.exam_type || "").trim();
  const parts = [
    candidate.question_type_label || candidate.question_type || "",
    candidate.library_name || (examType ? systemExamTypeLabel(examType) : ""),
    candidate.estimated_minutes ? `${candidate.estimated_minutes} 分钟` : "",
    topics,
  ].filter(Boolean);
  return parts.join(" · ");
}

function aiReviewPlanSourcePreviewRow({ title, meta, previewId, className = "" }) {
  return `
    <li class="${escapeHtml(className)}">
      <span>
        <strong>${escapeHtml(title)}</strong>
        ${meta ? `<small>${escapeHtml(meta)}</small>` : ""}
      </span>
      ${previewId ? `<button type="button" class="small-button" data-ai-review-plan-source-preview="${escapeHtml(previewId)}">预览</button>` : ""}
    </li>
  `;
}

function aiReviewPlanCandidateQuestionRows(sourceId, candidate) {
  const questions = Array.isArray(candidate?.questions) ? candidate.questions : [];
  if (!questions.length) return [];
  return questions
    .filter((question) => question && typeof question === "object")
    .map((question) => {
      const questionId = String(question.question_id || question.id || "").trim();
      const metaCandidate = {
        ...candidate,
        ...question,
        library_name: question.library_name || candidate.library_name,
        exam_type: question.exam_type || candidate.exam_type,
        estimated_minutes: question.estimated_minutes || "",
      };
      const answerState = question.answered === true ? "已答" : question.answered === false ? "未答" : "";
      const meta = [answerState, aiReviewPlanSourceMeta(metaCandidate)].filter(Boolean).join(" · ");
      return {
        title: aiReviewPlanSourceTitle(questionId || sourceId, question),
        meta,
        previewId: questionId.startsWith("kaoyan_") ? questionId : "",
        className: "is-child",
      };
    });
}

function aiReviewPlanSourcePreview(item, context) {
  const sourceIds = aiReviewPlanItemSourceIds(item);
  if (!sourceIds.length) return "";
  const lookup = aiReviewPlanCandidateLookup(context);
  let visibleCount = 0;
  const rows = sourceIds.map((sourceId) => {
    const candidate = lookup.get(sourceId);
    const questionRows = aiReviewPlanCandidateQuestionRows(sourceId, candidate);
    if (questionRows.length) {
      visibleCount += questionRows.length;
      const parentMeta = aiReviewPlanSourceMeta(candidate) || sourceId;
      const parentTitle = aiReviewPlanSourceTitle(sourceId, candidate);
      return `
        ${aiReviewPlanSourcePreviewRow({
          title: parentTitle,
          meta: parentMeta,
          previewId: "",
          className: "ai-plan-source-preview-parent",
        })}
        ${questionRows.map((row) => aiReviewPlanSourcePreviewRow(row)).join("")}
      `;
    }
    const previewId = String(candidate?.question_id || (sourceId.startsWith("kaoyan_") ? sourceId : "")).trim();
    const meta = aiReviewPlanSourceMeta(candidate);
    visibleCount += 1;
    return aiReviewPlanSourcePreviewRow({
      title: aiReviewPlanSourceTitle(sourceId, candidate),
      meta: meta || sourceId,
      previewId,
    });
  }).join("");
  return `
    <div class="ai-plan-source-preview">
      <strong>题目预览 · ${escapeHtml(String(visibleCount || sourceIds.length))} 项</strong>
      <ol class="ai-plan-source-preview-list">${rows}</ol>
    </div>
  `;
}

function renderAiReviewPlanValidation(body, validation) {
  const target = body.querySelector("[data-ai-review-plan-validation]");
  if (!target) return;
  const warnings = Array.isArray(validation?.warnings) ? validation.warnings : [];
  const rejected = Array.isArray(validation?.rejected) ? validation.rejected : [];
  const dailyLoad = Array.isArray(validation?.daily_load) ? validation.daily_load : [];
  const validCount = Number(validation?.valid_count || 0);
  const rejectedCount = Number(validation?.rejected_count || 0);
  target.hidden = false;
  target.classList.toggle("warn", Boolean(warnings.length || rejectedCount));
  target.classList.toggle("good", Boolean(validCount && !warnings.length && !rejectedCount));
  target.innerHTML = `
    <strong>提交前校验：可写入 ${escapeHtml(String(validCount))} 项，拦截 ${escapeHtml(String(rejectedCount))} 项</strong>
    ${warnings.length ? `<div>${warnings.map((item) => `<p>${escapeHtml(String(item))}</p>`).join("")}</div>` : "<p>所选任务都有可追踪来源，未发现单日超载。</p>"}
    ${rejected.length ? `<ul>${rejected.map((item) => `<li>${escapeHtml(item.title || "规划项")}：${escapeHtml(item.reason || "未通过校验")}</li>`).join("")}</ul>` : ""}
    ${dailyLoad.length ? `<div class="ai-plan-load-list">${dailyLoad.map((item) => `<span class="${item.over_limit ? "over" : ""}">${escapeHtml(item.date || "未定日期")} · ${escapeHtml(String(item.minutes || 0))}/${escapeHtml(String(item.limit || "不限"))} 分钟</span>`).join("")}</div>` : ""}
  `;
}

function renderAiReviewPlanDraft(body, state, payload) {
  const draft = payload?.draft || {};
  const draftContext = payload?.context || state.context || {};
  const warnings = Array.isArray(draft.warnings) ? draft.warnings : [];
  const days = Array.isArray(draft.days) ? draft.days : [];
  const isBlockedDraft = draft.source === "blocked";
  const sourceLabel = draft.source === "llm" ? "AI 生成" : isBlockedDraft ? "未调用 AI" : "规则兜底";
  const dayMarkup = days.length
    ? days.map((day, dayIndex) => {
      const items = Array.isArray(day.items) ? day.items : [];
      const itemMarkup = items.length
        ? items.map((item, itemIndex) => {
          const key = `${dayIndex}:${itemIndex}`;
          const minutes = aiReviewPlanItemMinutes(item);
          const dateValue = aiReviewPlanEditableDate(item.date || day.date || day.label);
          const sourcePreview = aiReviewPlanSourcePreview(item, draftContext);
          return `
            <div class="ai-plan-item" data-ai-review-plan-item="${escapeHtml(key)}">
              <label class="ai-plan-item-main">
                <input type="checkbox" data-ai-review-plan-item-checkbox="${escapeHtml(key)}" checked>
                <span class="ai-plan-item-content">
                  <strong>${escapeHtml(item.title || item.action || "复习任务")}</strong>
                  <p>${escapeHtml(item.reason || item.description || "根据当前薄弱项和复习任务生成。")}</p>
                  <em>${escapeHtml(String(minutes))} 分钟</em>
                  ${aiReviewPlanItemLoadMeta(item)}
                </span>
              </label>
              ${sourcePreview}
              <div class="ai-plan-item-controls">
                <label>日期
                  <input type="date" data-ai-review-plan-item-date="${escapeHtml(key)}" value="${escapeHtml(dateValue)}">
                </label>
                <label>预计分钟
                  <input type="number" min="5" max="240" step="5" data-ai-review-plan-item-minutes="${escapeHtml(key)}" value="${escapeHtml(String(minutes))}">
                </label>
                <button type="button" class="small-button danger-button ghost-danger" data-ai-review-plan-item-remove="${escapeHtml(key)}">删除</button>
              </div>
            </div>
          `;
        }).join("")
        : "<p>暂无具体任务。</p>";
      return `
        <article class="ai-plan-day">
          <h4>${escapeHtml(day.date || day.label || "计划日")}</h4>
          ${itemMarkup}
        </article>
      `;
    }).join("")
    : `<article class="ai-plan-day"><p>暂未生成具体日程。</p></article>`;
  const includeLabels = aiReviewPlanIncludeLabels(state.includeTypes || []);
  body.innerHTML = `
    <section class="ai-plan-draft" data-ai-plan-step="draft" data-ai-plan-draft-result>
      ${renderAiReviewPlanStepper("draft")}
      <div class="ai-plan-meta">
        <strong>草案结果</strong>
        <span>${escapeHtml(sourceLabel)} · ${escapeHtml(draft.model || DEFAULT_AI_REVIEW_PLAN_MODEL)} · 需勾选后写入</span>
      </div>
      <div class="ai-plan-card">
        <h4>${escapeHtml(aiReviewPlanModeConfig(state.mode).label)} · ${escapeHtml(String(state.days || 7))} 天</h4>
        <p>${isBlockedDraft ? "当前模式的数据不足，后端没有调用 AI，也不会写入复习规划。你可以返回设置切换模式、缩短天数或扩大范围。" : `纳入内容：${includeLabels.length ? escapeHtml(includeLabels.join(" / ")) : "未选择"}。默认全选，你可以取消不想加入复习规划的项目。`}</p>
      </div>
      ${renderAiReviewPlanCandidateAvailability(state, draftContext)}
      ${warnings.length ? `<div class="ai-plan-warning">${warnings.map((item) => `<p>${escapeHtml(String(item))}</p>`).join("")}</div>` : ""}
      <div class="ai-plan-warning" data-ai-review-plan-selection-warning hidden></div>
      <div class="ai-plan-days">${dayMarkup}</div>
      <div class="ai-plan-validation" data-ai-review-plan-validation hidden></div>
      <div class="system-workflow-actions">
        <button type="button" class="small-button" data-ai-review-plan-back-settings>返回设置</button>
        <button type="button" class="small-button" data-ai-review-plan-regenerate>重新生成</button>
        <button type="button" class="small-button dark-button" data-ai-review-plan-commit ${isBlockedDraft ? "disabled" : ""}>校验并加入复习规划</button>
      </div>
    </section>
  `;
}

function renderAiReviewPlanAccepted(body, state, payload, commitPayload = {}) {
  const draft = payload?.draft || {};
  const result = commitPayload?.result || {};
  const resultRows = Array.isArray(result.results) ? result.results : [];
  const createdCount = Number(result.created_count || 0);
  const skippedCount = Number(result.skipped_count || 0);
  const failedCount = Number(result.failed_count || 0);
  const rejectedCount = Number(result.rejected_count || 0);
  const warnings = Array.isArray(result.warnings) ? result.warnings : [];
  const dailyLoad = Array.isArray(result.daily_load) ? result.daily_load : [];
  body.innerHTML = `
    <section class="ai-plan-draft" data-ai-plan-step="result">
      ${renderAiReviewPlanStepper("result")}
      <div class="ai-plan-card">
        <h4>已加入复习规划</h4>
        <p>新增 ${escapeHtml(String(createdCount))} 项，跳过重复 ${escapeHtml(String(skippedCount))} 项，拦截 ${escapeHtml(String(rejectedCount))} 项，失败 ${escapeHtml(String(failedCount))} 项。重复项不会再次创建，缺少真实来源的任务不会写入。</p>
      </div>
      ${warnings.length || dailyLoad.length ? `
        <div class="ai-plan-validation ${warnings.length ? "warn" : "good"}">
          <strong>写入校验结果</strong>
          ${warnings.length ? warnings.map((item) => `<p>${escapeHtml(String(item))}</p>`).join("") : "<p>未发现单日超载或无来源任务。</p>"}
          ${dailyLoad.length ? `<div class="ai-plan-load-list">${dailyLoad.map((item) => `<span class="${item.over_limit ? "over" : ""}">${escapeHtml(item.date || "未定日期")} · ${escapeHtml(String(item.minutes || 0))}/${escapeHtml(String(item.limit || "不限"))} 分钟</span>`).join("")}</div>` : ""}
        </div>
      ` : ""}
      <div class="ai-plan-days">
        ${resultRows.length ? resultRows.map((item) => `
          <div class="ai-plan-item ai-plan-result-item">
            <span class="ai-plan-item-content">
              <strong>${escapeHtml(item.title || "复习任务")}</strong>
              <p>${escapeHtml(item.status === "created" ? "已创建任务" : item.status === "duplicate" ? "已有相同日期的任务，已跳过" : item.status === "rejected" ? item.reason || "提交前校验已拦截" : item.reason || "写入失败")}</p>
              ${item.due_at ? `<em>${escapeHtml(String(item.due_at).slice(0, 10))}</em>` : ""}
            </span>
          </div>
        `).join("") : "<p>没有写入任何复习任务。</p>"}
      </div>
      <div class="system-workflow-actions">
        <button type="button" class="small-button" data-ai-review-plan-back-draft>返回草案</button>
        <button type="button" class="small-button dark-button" data-ai-review-plan-back-settings>继续调整</button>
      </div>
    </section>
  `;
}

async function openAiReviewPlanModal() {
  const constraints = aiReviewPlanConstraints();
  let step = "loading";
  let state = { ...constraints, mode: "balanced", includeTypes: [] };
  let latestDraft = null;
  const { overlay, close } = createSystemWorkflowOverlay("AI 生成规划", "先选择规划模式，再生成不会自动写入任务的草案。", {
    onHeaderAction: () => {
      if (step === "settings" || step === "loading") {
        close();
        return;
      }
      if (step === "result" && latestDraft) {
        step = "draft";
        setHeaderAction("返回设置");
        renderAiReviewPlanDraft(body, state, latestDraft);
        bindDraftEvents();
        return;
      }
      renderSettingsStep();
    },
  });
  const body = overlay.querySelector(".system-workflow-body");
  if (!body) return;
  const headerButton = overlay.querySelector("[data-system-workflow-close]");
  const setHeaderAction = (label) => {
    if (headerButton) headerButton.textContent = label;
  };
  const bindSettingsEvents = () => {
    body.querySelectorAll("[data-ai-review-plan-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        const mode = button.dataset.aiReviewPlanMode || "balanced";
        state = {
          ...state,
          mode,
          includeTypes: aiReviewPlanDefaultIncludes(mode),
        };
        renderSettingsStep();
      });
    });
    body.querySelectorAll("[data-ai-review-plan-include]").forEach((input) => {
      input.addEventListener("change", () => {
        state.includeTypes = [...body.querySelectorAll("[data-ai-review-plan-include]:checked")]
          .map((item) => item.dataset.aiReviewPlanInclude)
          .filter(Boolean);
      });
    });
    body.querySelector("[data-ai-review-plan-days]")?.addEventListener("input", (event) => {
      state.days = Math.max(1, Math.min(21, Number(event.target.value || 7)));
    });
    body.querySelector("[data-ai-review-plan-minutes]")?.addEventListener("input", (event) => {
      state.daily_minutes = Math.max(10, Math.min(240, Number(event.target.value || 60)));
    });
    body.querySelector("[data-ai-review-plan-draft]")?.addEventListener("click", () => {
      void generateDraft();
    });
  };
  const renderSettingsStep = () => {
    step = "settings";
    setHeaderAction("关闭");
    renderAiReviewPlanSettings(body, state);
    bindSettingsEvents();
  };
  const bindResultEvents = () => {
    body.querySelector("[data-ai-review-plan-back-draft]")?.addEventListener("click", () => {
      step = "draft";
      setHeaderAction("返回设置");
      renderAiReviewPlanDraft(body, state, latestDraft);
      bindDraftEvents();
    });
    body.querySelector("[data-ai-review-plan-back-settings]")?.addEventListener("click", renderSettingsStep);
  };
  const commitDraft = async () => {
    if (!latestDraft) return;
    const selection = selectedAiReviewPlanItems(body, latestDraft);
    const warning = body.querySelector("[data-ai-review-plan-selection-warning]");
    if (!selection.items.length) {
      if (warning) {
        warning.hidden = false;
        warning.innerHTML = "<p>请至少勾选一个规划项，再加入复习规划。</p>";
      }
      return;
    }
    if (warning) {
      warning.hidden = true;
      warning.innerHTML = "";
    }
    const button = body.querySelector("[data-ai-review-plan-commit]");
    if (button) {
      button.disabled = true;
      button.textContent = "正在校验...";
    }
    const requestBody = {
      plan_id: latestDraft?.draft?.plan_id || "",
      subject: state.subject || "math",
      daily_minutes: state.daily_minutes,
      items: selection.items,
      selected_item_keys: selection.selected_item_keys,
      draft: latestDraft?.draft || null,
    };
    try {
      const validationPayload = await fetchJson(`/api/materials/system/ai-review-plan/validate?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      const validation = validationPayload?.validation || {};
      renderAiReviewPlanValidation(body, validation);
      if (!validation.can_commit) {
        if (warning) {
          warning.hidden = false;
          warning.innerHTML = "<p>所选规划项都没有可追踪的真实题目或练习单来源，暂不能加入复习规划。</p>";
        }
        if (button) {
          button.disabled = false;
          button.textContent = "校验并加入复习规划";
        }
        return;
      }
      if (button) {
        button.textContent = "正在加入...";
      }
      const commitPayload = await fetchJson(`/api/materials/system/ai-review-plan/commit?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      await loadReviewTasks({ silent: true });
      await loadReviewLearningInsights({ silent: true });
      step = "result";
      setHeaderAction("返回草案");
      renderAiReviewPlanAccepted(body, state, latestDraft, commitPayload);
      bindResultEvents();
    } catch (error) {
      if (warning) {
        warning.hidden = false;
        warning.innerHTML = `<p>加入复习规划失败：${escapeHtml(error.message)}</p>`;
      }
      if (button) {
        button.disabled = false;
        button.textContent = "校验并加入复习规划";
      }
    }
  };
  const bindDraftEvents = () => {
    body.querySelector("[data-ai-review-plan-back-settings]")?.addEventListener("click", renderSettingsStep);
    body.querySelector("[data-ai-review-plan-regenerate]")?.addEventListener("click", () => {
      void generateDraft();
    });
    body.querySelector("[data-ai-review-plan-commit]")?.addEventListener("click", () => {
      void commitDraft();
    });
    body.querySelectorAll("[data-ai-review-plan-source-preview]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const sourceId = button.dataset.aiReviewPlanSourcePreview || "";
        if (sourceId) {
          void openSystemQuestionPreview(sourceId);
        }
      });
    });
    body.querySelectorAll("[data-ai-review-plan-item-remove]").forEach((button) => {
      button.addEventListener("click", () => {
        const row = button.closest("[data-ai-review-plan-item]");
        if (!row) return;
        row.dataset.aiReviewPlanRemoved = "true";
        row.remove();
        const validation = body.querySelector("[data-ai-review-plan-validation]");
        if (validation) {
          validation.hidden = true;
          validation.innerHTML = "";
        }
      });
    });
    body.querySelectorAll("[data-ai-review-plan-item-checkbox], [data-ai-review-plan-item-date], [data-ai-review-plan-item-minutes]").forEach((control) => {
      control.addEventListener("change", () => {
        const validation = body.querySelector("[data-ai-review-plan-validation]");
        if (validation) {
          validation.hidden = true;
          validation.innerHTML = "";
        }
      });
    });
  };
  const generateDraft = async () => {
    step = "draft";
    setHeaderAction("返回设置");
    body.innerHTML = `<section class="system-workflow-section"><p>正在生成 AI 规划草案...</p></section>`;
    try {
      latestDraft = await fetchJson(`/api/materials/system/ai-review-plan/draft?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: state.subject,
          days: state.days,
          daily_minutes: state.daily_minutes,
          goal: aiReviewPlanModeConfig(state.mode).label,
          mode: state.mode,
          include_types: state.includeTypes,
          model: DEFAULT_AI_REVIEW_PLAN_MODEL,
        }),
      });
      if (latestDraft?.context) {
        state = { ...state, context: latestDraft.context };
      }
      renderAiReviewPlanDraft(body, state, latestDraft);
      bindDraftEvents();
    } catch (error) {
      body.innerHTML = `
        <section class="ai-plan-warning">
          <p>AI 规划生成失败：${escapeHtml(error.message)}</p>
        </section>
        <div class="system-workflow-actions">
          <button type="button" class="small-button" data-ai-review-plan-back-settings>返回设置</button>
          <button type="button" class="small-button dark-button" data-ai-review-plan-regenerate>重试生成</button>
        </div>
      `;
      body.querySelector("[data-ai-review-plan-back-settings]")?.addEventListener("click", renderSettingsStep);
      body.querySelector("[data-ai-review-plan-regenerate]")?.addEventListener("click", () => {
        void generateDraft();
      });
    }
  };
  body.innerHTML = `<section class="system-workflow-section"><p>正在整理学习画像和候选任务...</p></section>`;
  try {
    const query = aiReviewPlanQuery(constraints);
    const data = await fetchJson(`/api/materials/system/ai-planning-context?${query.toString()}`);
    const context = data.context || data;
    state = aiReviewPlanStateFromContext(constraints, context);
    renderSettingsStep();
  } catch (error) {
    body.innerHTML = `<section class="ai-plan-warning"><p>AI 规划依据加载失败：${escapeHtml(error.message)}</p></section>`;
  }
}

function handleReviewInsightAction(event) {
  const aiPlanButton = event.target.closest("[data-review-ai-plan]");
  if (aiPlanButton && reviewLearningInsights?.contains(aiPlanButton)) {
    void openAiReviewPlanModal();
    return;
  }
  const button = event.target.closest("[data-review-insight-action]");
  if (!button) {
    const topicCard = event.target.closest("[data-learning-topic-card]");
    if (topicCard && reviewLearningInsights?.contains(topicCard)) {
      openLearningTopicPanel(topicCard.dataset.learningTopic || "");
    }
    return;
  }
  const action = button.dataset.reviewInsightAction || "";
  if (action === "review_due") {
    const insights = reviewTasksState.learningInsights || {};
    const reviewSummary = insights.review_summary || {};
    const nextGroup = Number(reviewSummary.overdue_count || 0) > 0 ? "overdue" : "today";
    scrollReviewTaskGroupIntoView(nextGroup);
    setReviewTasksStatus("saved", "已定位到期复习任务");
    return;
  }
  if (action === "continue_draft") {
    void openPracticeDraftListModal();
    return;
  }
  if (action === "topic_review") {
    const topic = button.dataset.reviewInsightTopic || "";
    openLearningTopicPanel(topic);
    setReviewTasksStatus("saved", topic ? `已打开「${topic}」处理面板` : "已打开知识点处理面板");
    return;
  }
  if (action === "review_wrong") {
    openWrongQuestionPoolModal();
    return;
  }
  if (action === "confirm_grading") {
    openPendingReviewModal();
  }
}

function handleReviewInsightKeydown(event) {
  if (event.key !== "Enter" && event.key !== " ") return;
  const topicCard = event.target.closest("[data-learning-topic-card]");
  if (!topicCard || !reviewLearningInsights?.contains(topicCard)) return;
  event.preventDefault();
  openLearningTopicPanel(topicCard.dataset.learningTopic || "");
}

async function openSystemPracticeSetPrintable(practiceSet, options = {}) {
  const fallbackQuestions = options.fallbackQuestions || [];
  const practiceSetId = systemPracticeSetId(practiceSet);
  let detail = practiceSet || {};
  if (practiceSetId) {
    try {
      const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
      detail = data.practice_set || data;
    } catch {
      detail = practiceSet || {};
    }
  }
  const ids = practiceSetQuestionIds(detail, fallbackQuestions);
  const questions = await Promise.all(
    ids.map(async (questionId) => {
      try {
        return await fetchJson(systemQuestionDetailUrl(questionId));
      } catch {
        return fallbackQuestions.find((item) => item.question_id === questionId) || { question_id: questionId };
      }
    })
  );
  showPracticeSetPrintOverlay(detail, questions, { fallbackQuestions });
}

async function fetchPracticeSetWithQuestions(practiceSetId, fallbackTitle = "") {
  const data = await fetchJson(`/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
  const practiceSet = data.practice_set || data || {};
  const detail = { ...practiceSet };
  if (fallbackTitle && !detail.title && !detail.name) {
    detail.title = fallbackTitle;
  }
  const questionIds = practiceSetQuestionIds(detail, []);
  const questions = await Promise.all(
    questionIds.map(async (questionId) => {
      try {
        return await fetchJson(systemQuestionDetailUrl(questionId));
      } catch {
        return { question_id: questionId };
      }
    })
  );
  return { practiceSet: detail, questions };
}

async function openSingleQuestionReviewAttempt(task) {
  const questionId = String(task?.target_id || task?.source_question_id || "");
  if (!questionId) return;
  let question = { question_id: questionId };
  try {
    question = await fetchJson(systemQuestionDetailUrl(questionId));
  } catch {
    question = { question_id: questionId };
  }
  const baseTitle = reviewTaskTitle(task) || systemQuestionTitle(question) || questionId;
  const title = String(baseTitle).includes("单题复习") ? String(baseTitle) : `${baseTitle} 单题复习`;
  const payload = {
    question_ids: [questionId],
    title,
    subject: question.subject || task?.subject || systemState.subject || "math",
    exam_type: question.exam_type || task?.exam_type || systemState.examType || "",
    source_type: "review_question",
    filters: {
      source: "review_task",
      review_task_id: reviewTaskId(task),
      target_type: "question",
    },
  };
  const data = await fetchJson(`/api/materials/system/practice-sets/from-question-ids?user_id=${encodeURIComponent(currentMaterialsUserId())}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const practiceSet = data.practice_set || data || {};
  if (!Array.isArray(practiceSet.question_ids)) {
    practiceSet.question_ids = [questionId];
  }
  await openPracticeAttempt(practiceSet, [question], { fallbackQuestions: [question], reviewTask: task });
}

async function openReviewTaskSource(task) {
  const targetType = String(task?.target_type || "");
  const targetId = String(task?.target_id || "");
  if (!targetId) return;
  await markReviewTaskStarted(task);
  if (targetType === "question") {
    await openSingleQuestionReviewAttempt(task);
    return;
  }
  if (targetType === "practice_set") {
    const { practiceSet, questions } = await fetchPracticeSetWithQuestions(targetId, reviewTaskTitle(task));
    await openPracticeAttempt(practiceSet, questions, { fallbackQuestions: questions });
    return;
  }
  if (targetType === "knowledge_point") {
    openLearningTopicPanel(targetId);
    return;
  }
  setActivePage("materials");
  setMaterialsMode(MATERIALS_MODE_SYSTEM, { skipRefreshWhenCurrent: true });
  await openSystemQuestionDrawer(targetId);
}

function renderSystemMaterialsSkeleton() {
  renderSystemQuestionList();
  if (!systemState.loading && systemState.items.length === 0 && systemState.subject === "math" && systemState.contentType === "questions") {
    void loadSystemQuestions();
  }
}

function setMaterialsMode(mode, options = {}) {
  const nextMode = mode === MATERIALS_MODE_SYSTEM ? MATERIALS_MODE_SYSTEM : MATERIALS_MODE_USER;
  const modeChanged = nextMode !== activeMaterialsMode;

  activeMaterialsMode = nextMode;
  materialsModeTabs.forEach((button) => {
    const active = button.dataset.materialsMode === activeMaterialsMode;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  userMaterialsView?.classList.toggle("active", activeMaterialsMode === MATERIALS_MODE_USER);
  systemMaterialsView?.classList.toggle("active", activeMaterialsMode === MATERIALS_MODE_SYSTEM);
  rememberMaterialsMode(activeMaterialsMode);

  if (activeMaterialsMode === MATERIALS_MODE_SYSTEM) {
    if (!pages.materials?.classList.contains("active")) {
      return;
    }
    renderSystemMaterialsSkeleton();
    return;
  }
  if (!options.skipRefresh && pages.materials?.classList.contains("active") && (modeChanged || !options.skipRefreshWhenCurrent)) {
    void refreshMaterialsList();
  }
}

function setActivePage(pageId) {
  const nextPageId = pages[pageId] ? pageId : "chat";
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.page === nextPageId);
  });
  Object.entries(pages).forEach(([key, element]) => {
    element.classList.toggle("active", key === nextPageId);
  });
  rememberActivePage(nextPageId);
  if (nextPageId === "materials") {
    setMaterialsMode(activeMaterialsMode);
  }
  if (nextPageId === "plan") {
    void loadReviewLearningInsights();
    void loadReviewTasks();
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
    removeButton.textContent = "脳";
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

function setUploadProgress(jobOrState) {
  if (!jobOrState) {
    materialsUploadProgress.hidden = true;
    materialsUploadStage.textContent = "等待上传";
    materialsUploadPercent.textContent = "0%";
    materialsUploadBar.style.width = "0%";
    materialsUploadMessage.textContent = "等待上传文件。";
    return;
  }
  const progress = Math.max(0, Math.min(100, Number(jobOrState.progress ?? 0)));
  materialsUploadProgress.hidden = false;
  materialsUploadStage.textContent = jobOrState.stage_label || jobOrState.stage || "处理中";
  materialsUploadPercent.textContent = `${Math.round(progress)}%`;
  materialsUploadBar.style.width = `${progress}%`;
  materialsUploadMessage.textContent = jobOrState.message || "正在处理资料。";
}

function sleep(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

async function waitForUploadJob(jobId) {
  while (true) {
    const payload = await fetchJson(`/api/materials/upload-jobs/${encodeURIComponent(jobId)}`);
    const job = payload.job;
    setUploadProgress(job);
    if (job.status === "completed") {
      return job.result;
    }
    if (job.status === "failed") {
      if (job.result && ["metadata_conflict", "metadata_detection_required"].includes(job.result.error)) {
        return job.result;
      }
      throw new Error(job.error || job.message || "资料处理失败");
    }
    await sleep(1500);
  }
}

function clearMaterialsFeedback() {
  setBanner(materialsStatus, "");
  setBanner(materialsError, "");
  setUploadProgress(null);
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
  textbook: "教材",
  lecture: "讲义",
  exercise: "习题",
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

function formatSearchScore(result) {
  const score = Number(result.score || 0);
  if (result.score_kind === "llm_rerank" || result.search_mode === "llm" || result.search_mode === "hybrid_llm") {
    const rerank = result.llm_rerank || {};
    if (rerank.score !== undefined) {
      return `AI 置信 ${(Number(rerank.score || 0) * 100).toFixed(0)}%`;
    }
    return `AI 排序 #${result.rank || rerank.rank || "-"}`;
  }
  if (result.score_kind === "vector_similarity" || result.search_mode === "vector") {
    return `相似度 ${(score * 100).toFixed(1)}%`;
  }
  if (result.score_kind === "rank_fusion" || result.search_mode === "hybrid") {
    return `融合排序分 ${(score * 100).toFixed(2)}`;
  }
  return `关键词分 ${score.toFixed(4)}`;
}

function qualityStatusLabel(value) {
  if (value === "high") return "质量高";
  if (value === "medium") return "质量中";
  if (value === "low") return "质量低";
  if (value === "failed") return "入库失败";
  return value || "待评估";
}

function qualityStatusClass(value) {
  if (value === "high") return "good";
  if (value === "low" || value === "failed") return "wrong";
  return "learning";
}

function indexStatusLabel(item) {
  if (item.parse_status === "ready" && Number(item.chunk_count || 0) > 0) {
    return "索引已建立";
  }
  if (item.parse_status === "failed") return "索引不可用";
  return "等待索引";
}

function materialById(materialId) {
  return currentMaterials.find((item) => item.material_id === materialId) || null;
}

function syncMaterialsSearchScopeOptions() {
  if (!materialsSearchScope) return;
  const previousValue = materialsSearchScope.value || "subject";
  materialsSearchScope.innerHTML = "";
  [
    ["subject", `当前学科：${materialLabel(MATERIAL_SUBJECT_LABELS, activeMaterialsSubject())}`],
    ["all", "全部我的资料"],
  ].forEach(([value, label]) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    materialsSearchScope.appendChild(option);
  });
  currentMaterials.forEach((item) => {
    const option = document.createElement("option");
    option.value = `material:${item.material_id}`;
    option.textContent = `当前资料：${item.original_filename || item.material_id}`;
    materialsSearchScope.appendChild(option);
  });
  const hasPrevious = [...materialsSearchScope.options].some((option) => option.value === previousValue);
  materialsSearchScope.value = hasPrevious ? previousValue : "subject";
  activeMaterialSearchId = materialsSearchScope.value.startsWith("material:")
    ? materialsSearchScope.value.slice("material:".length)
    : "";
}

function updateMaterialsSearchModeStatus() {
  if (!materialsSearchModeStatus || !materialsSearchMode) return;
  materialsSearchModeStatus.textContent = materialsSearchMode.value === "llm" ? "AI 精排" : "快速检索";
  materialsSearchModeStatus.className = `status-pill ${materialsSearchMode.value === "llm" ? "mastered" : "type"}`;
}

function updateMaterialCardSelection() {
  materialsList.querySelectorAll("[data-material-id]").forEach((card) => {
    card.classList.toggle("active", Boolean(activeMaterialSearchId && card.dataset.materialId === activeMaterialSearchId));
  });
}

function setMaterialSearchScope(item) {
  if (!item || !materialsSearchScope) return;
  const scopeValue = `material:${item.material_id}`;
  const hasOption = [...materialsSearchScope.options].some((option) => option.value === scopeValue);
  if (!hasOption) {
    syncMaterialsSearchScopeOptions();
  }
  materialsSearchScope.value = scopeValue;
  activeMaterialSearchId = item.material_id;
  updateMaterialCardSelection();
  materialsSearchInput.focus();
  setBanner(materialsStatus, `已切换为在《${item.original_filename || "未命名资料"}》内搜索`);
}

function closeMaterialDetailDrawer() {
  if (!materialDetailDrawer || !materialDetailBackdrop) return;
  materialDetailDrawer.hidden = true;
  materialDetailBackdrop.hidden = true;
  materialDetailDrawer.setAttribute("aria-hidden", "true");
}

function materialDetailValue(value, fallback = "-") {
  if (value === null || value === undefined || value === "") return fallback;
  return String(value);
}

function renderMaterialDetailContent(detail) {
  if (!materialDetailBody) return;
  const metadata = detail.metadata && typeof detail.metadata === "object" ? detail.metadata : {};
  const formulaCleaning = metadata.formula_cleaning || {};
  const llmCleaning = metadata.llm_cleaning || {};
  const warnings = Array.isArray(detail.warnings) ? detail.warnings : [];
  materialDetailBody.className = "material-detail-body";
  materialDetailBody.innerHTML = `
    <section class="material-detail-section">
      <h4>概览</h4>
      <dl class="material-detail-grid">
        <div><dt>学科</dt><dd>${escapeHtml(materialLabel(MATERIAL_SUBJECT_LABELS, detail.subject))}</dd></div>
        <div><dt>资料类型</dt><dd>${escapeHtml(materialLabel(MATERIAL_TYPE_LABELS, detail.material_type))}</dd></div>
        <div><dt>解析状态</dt><dd>${escapeHtml(materialLabel(MATERIAL_STATUS_LABELS, detail.parse_status))}</dd></div>
        <div><dt>质量</dt><dd>${escapeHtml(qualityStatusLabel(detail.quality_status))}</dd></div>
        <div><dt>置信度</dt><dd>${escapeHtml(materialDetailValue(detail.overall_confidence))}</dd></div>
        <div><dt>chunks</dt><dd>${escapeHtml(materialDetailValue(detail.chunk_count, "0"))}</dd></div>
      </dl>
    </section>
    <section class="material-detail-section">
      <h4>搜索健康</h4>
      <p class="material-meta">${escapeHtml(indexStatusLabel(detail))} · 图片资源 ${escapeHtml(materialDetailValue(detail.asset_count, "0"))} 个 · 更新时间 ${escapeHtml(formatMaterialDate(detail.updated_at))}</p>
    </section>
    <section class="material-detail-section">
      <h4>高级诊断</h4>
      <dl class="material-detail-grid">
        <div><dt>formula_cleaning</dt><dd>${escapeHtml(materialDetailValue(formulaCleaning.status || formulaCleaning.enabled))}</dd></div>
        <div><dt>llm_cleaning</dt><dd>${escapeHtml(materialDetailValue(llmCleaning.status || llmCleaning.enabled || "未启用"))}</dd></div>
        <div><dt>warnings</dt><dd>${warnings.length}</dd></div>
      </dl>
      ${warnings.length ? `<p class="material-detail-warning">${escapeHtml(warnings.slice(0, 3).join("；"))}</p>` : ""}
    </section>
  `;
}

async function openMaterialDetailDrawer(item) {
  if (!item || !materialDetailDrawer || !materialDetailBackdrop) return;
  materialDetailDrawer.hidden = false;
  materialDetailBackdrop.hidden = false;
  materialDetailDrawer.setAttribute("aria-hidden", "false");
  if (materialDetailTitle) {
    materialDetailTitle.textContent = item.original_filename || "未命名资料";
  }
  if (materialDetailMeta) {
    materialDetailMeta.textContent = materialMetaLine(item);
  }
  renderMaterialDetailContent(item);
  try {
    const detail = await fetchJson(`/api/materials/${encodeURIComponent(item.material_id)}?user_id=${encodeURIComponent(currentMaterialsUserId())}`);
    if (materialDetailTitle) {
      materialDetailTitle.textContent = detail.original_filename || item.original_filename || "未命名资料";
    }
    if (materialDetailMeta) {
      materialDetailMeta.textContent = materialMetaLine(detail);
    }
    renderMaterialDetailContent(detail);
  } catch (error) {
    if (materialDetailBody) {
      materialDetailBody.insertAdjacentHTML(
        "beforeend",
        `<section class="material-detail-section material-detail-warning">详情加载失败：${escapeHtml(error.message)}</section>`
      );
    }
  }
}

function openSearchResultDrawer(result) {
  if (!result || !materialDetailDrawer || !materialDetailBackdrop) return;
  materialDetailDrawer.hidden = false;
  materialDetailBackdrop.hidden = false;
  materialDetailDrawer.setAttribute("aria-hidden", "false");
  if (materialDetailTitle) {
    materialDetailTitle.textContent = result.section_title || result.original_filename || "检索片段";
  }
  if (materialDetailMeta) {
    const headingPath = Array.isArray(result.heading_path) ? result.heading_path.join(" / ") : "";
    materialDetailMeta.textContent = [result.original_filename, headingPath, result.chunk_id].filter(Boolean).join(" · ");
  }
  if (materialDetailBody) {
    materialDetailBody.className = "material-detail-body";
    materialDetailBody.innerHTML = `
      <section class="material-detail-section">
        <h4>命中理由</h4>
        <p class="material-meta">${escapeHtml(resultReason(result))}</p>
      </section>
      <section class="material-detail-section">
        <h4>片段内容</h4>
        <pre class="search-preview">${escapeHtml(result.text || result.text_preview || "")}</pre>
      </section>
    `;
  }
}

function buildMaterialsSearchUrl(query) {
  const params = new URLSearchParams({
    user_id: currentMaterialsUserId(),
    query,
    mode: materialsSearchMode?.value || "hybrid",
    top_k: materialsSearchLimit?.value || "6",
  });
  const scopeValue = materialsSearchScope?.value || "subject";
  if (scopeValue === "subject") {
    params.set("subject", activeMaterialsSubject());
  } else if (scopeValue.startsWith("material:")) {
    const materialId = scopeValue.slice("material:".length);
    const material = materialById(materialId);
    params.set("material_id", materialId);
    params.set("subject", material?.subject || activeMaterialsSubject());
  }
  return `/api/materials/search?${params.toString()}`;
}

function resultDecisionLabel(result) {
  const rerank = result.llm_rerank || {};
  if (rerank.decision === "related") return "相关参考";
  if (rerank.decision === "rejected" || rerank.decision === "reject") return "已过滤";
  if (rerank.decision === "primary") return "强匹配";
  if (result.score_kind === "llm_rerank") return "AI 精排";
  return "强匹配";
}

function resultDecisionClass(result) {
  const label = resultDecisionLabel(result);
  if (label === "相关参考") return "warn";
  if (label === "已过滤") return "wrong";
  return "good";
}

function resultReason(result) {
  const rerank = result.llm_rerank || {};
  if (rerank.reason) return `AI 判定：${rerank.reason}`;
  if (Array.isArray(result.matched_by) && result.matched_by.length) {
    return `命中方式：${result.matched_by.join(" + ")}`;
  }
  return `排序依据：${formatSearchScore(result)}`;
}

function extractQueryConcepts(query) {
  return [...new Set(
    String(query || "")
      .split(/[\s,，、;；|/]+/)
      .map((term) => term.trim())
      .filter((term) => term.length >= 2)
  )].slice(0, 8);
}

function renderConceptCoverage(results, query) {
  const concepts = extractQueryConcepts(query);
  if (concepts.length < 2) return null;
  const combinedResultsText = (results || [])
    .map((result) => [
      result.section_title,
      Array.isArray(result.heading_path) ? result.heading_path.join(" ") : "",
      result.text,
      result.text_preview,
    ].filter(Boolean).join(" "))
    .join("\n");
  const covered = concepts.filter((concept) => combinedResultsText.includes(concept));
  const wrapper = document.createElement("section");
  wrapper.className = "materials-coverage";
  const title = document.createElement("div");
  title.className = "materials-coverage-title";
  title.innerHTML = `<strong>概念覆盖</strong><span>已覆盖 ${covered.length}/${concepts.length}</span>`;
  const chips = document.createElement("div");
  chips.className = "materials-coverage-chips";
  concepts.forEach((concept) => {
    const chip = document.createElement("span");
    const isCovered = covered.includes(concept);
    chip.className = `material-result-chip ${isCovered ? "hit" : "miss"}`;
    chip.textContent = `${isCovered ? "已覆盖" : "未覆盖"}：${concept}`;
    chips.appendChild(chip);
  });
  wrapper.appendChild(title);
  wrapper.appendChild(chips);
  return wrapper;
}

function renderMaterialsSearchSummary(data, query) {
  if (!materialsSearchSummary) return;
  const results = data?.results || [];
  const modeLabel = (data?.mode || materialsSearchMode?.value) === "llm" ? "AI 精排" : "快速检索";
  const fallback = (materialsSearchMode?.value === "llm" && results.length > 0 && !results.some((result) => result.llm_rerank && Object.keys(result.llm_rerank).length));
  materialsSearchSummary.hidden = false;
  materialsSearchSummary.textContent = `${modeLabel} · ${results.length} 条结果 · ${query}${fallback ? " · AI 不可用，已回退快速检索" : ""}`;
}

function renderMaterialsList(items) {
  currentMaterials = items || [];
  syncMaterialsSearchScopeOptions();
  materialsList.innerHTML = "";
  if (!currentMaterials.length) {
    materialsList.className = "materials-list empty-state";
    materialsList.textContent = "当前学科资料库还没有资料，先上传一份 `.md`、`.txt` 或 `.pdf` 吧。";
    return;
  }

  materialsList.className = "materials-list";
  currentMaterials.forEach((item) => {
    const card = document.createElement("article");
    card.className = "material-card";
    card.dataset.materialId = item.material_id;
    if (activeMaterialSearchId && activeMaterialSearchId === item.material_id) {
      card.classList.add("active");
    }

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

    const health = document.createElement("p");
    health.className = "material-meta";
    health.textContent = `${qualityStatusLabel(item.quality_status)} · ${indexStatusLabel(item)}${Array.isArray(item.warnings) && item.warnings.length ? ` · ${item.warnings.length} 条提醒` : ""}`;
    titleBlock.appendChild(health);

    const actions = document.createElement("div");
    actions.className = "material-actions";
    const scopeButton = document.createElement("button");
    scopeButton.type = "button";
    scopeButton.className = "small-button";
    scopeButton.textContent = "在本资料搜索";
    scopeButton.addEventListener("click", () => setMaterialSearchScope(item));
    const detailButton = document.createElement("button");
    detailButton.type = "button";
    detailButton.className = "small-button";
    detailButton.textContent = "详情";
    detailButton.addEventListener("click", () => void openMaterialDetailDrawer(item));
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "danger-button inline-danger";
    deleteButton.textContent = "删除";
    deleteButton.addEventListener("click", () => void deleteMaterial(item.material_id));
    actions.appendChild(scopeButton);
    actions.appendChild(detailButton);
    actions.appendChild(deleteButton);

    header.appendChild(titleBlock);
    header.appendChild(actions);
    card.appendChild(header);

    const statusRow = document.createElement("div");
    statusRow.className = "material-health-row";
    const quality = document.createElement("span");
    quality.className = `status-pill ${qualityStatusClass(item.quality_status)}`;
    quality.textContent = qualityStatusLabel(item.quality_status);
    const chunks = document.createElement("span");
    chunks.className = "status-pill type";
    chunks.textContent = `${item.chunk_count ?? 0} chunks`;
    const index = document.createElement("span");
    index.className = "status-pill mastered";
    index.textContent = indexStatusLabel(item);
    statusRow.appendChild(quality);
    statusRow.appendChild(chunks);
    statusRow.appendChild(index);
    card.appendChild(statusRow);

    const footer = document.createElement("p");
    footer.className = "material-footer";
    footer.textContent = `创建时间：${formatMaterialDate(item.created_at)} · 更新时间：${formatMaterialDate(item.updated_at)}${item.error ? ` · 错误：${item.error}` : ""}`;
    card.appendChild(footer);
    materialsList.appendChild(card);
  });
}

function appendSearchResultSection(title, results) {
  if (!results.length) return;
  const section = document.createElement("section");
  section.className = "search-result-section";
  const heading = document.createElement("h4");
  heading.textContent = title;
  section.appendChild(heading);
  results.forEach((result) => {
    const card = document.createElement("article");
    card.className = `search-card ${resultDecisionLabel(result) === "相关参考" ? "related" : ""}`;

    const titleRow = document.createElement("div");
    titleRow.className = "search-card-title-row";
    const titleBlock = document.createElement("div");
    const titleElement = document.createElement("h4");
    titleElement.textContent = `${result.section_title || result.original_filename || "未命名资料"} · ${formatSearchScore(result)}`;
    const badge = document.createElement("span");
    badge.className = `status-pill ${resultDecisionClass(result)}`;
    badge.textContent = resultDecisionLabel(result);
    titleBlock.appendChild(titleElement);
    titleRow.appendChild(titleBlock);
    titleRow.appendChild(badge);

    const headingPath = Array.isArray(result.heading_path) && result.heading_path.length
      ? ` · 标题：${result.heading_path.join(" / ")}`
      : "";
    const matchedBy = Array.isArray(result.matched_by) && result.matched_by.length
      ? ` · 命中：${result.matched_by.join("+")}`
      : "";
    const tableMeta = result.table_id ? ` · 表格：${result.table_id}` : "";
    const plan = result.retrieval_plan || {};
    const planMeta = Object.keys(plan).length
      ? ` · 候选：${plan.llm_candidate_limit || "-"} / 召回：${plan.recall_limit || "-"}`
      : "";
    const meta = document.createElement("p");
    meta.className = "material-meta";
    meta.textContent = `${result.original_filename || "未命名资料"} · 分块：${result.chunk_id}${headingPath}${matchedBy}${tableMeta}${planMeta}`;
    const reason = document.createElement("p");
    reason.className = "search-result-reason";
    reason.textContent = resultReason(result);
    const preview = document.createElement("pre");
    preview.className = "search-preview";
    preview.textContent = result.text || result.text_preview || "";
    const actions = document.createElement("div");
    actions.className = "material-actions";
    const openButton = document.createElement("button");
    openButton.type = "button";
    openButton.className = "small-button";
    openButton.textContent = "查看片段";
    openButton.addEventListener("click", () => openSearchResultDrawer(result));
    actions.appendChild(openButton);

    card.appendChild(titleRow);
    card.appendChild(meta);
    card.appendChild(reason);
    card.appendChild(preview);
    card.appendChild(actions);
    section.appendChild(card);
  });
  materialsSearchResults.appendChild(section);
}

function renderSearchResults(results, options = {}) {
  currentSearchResults = results;
  materialsSearchResults.innerHTML = "";
  if (!results || results.length === 0) {
    materialsSearchResults.className = "search-results empty-state";
    materialsSearchResults.textContent = options.emptyText || "当前范围中没有找到强匹配内容";
    return;
  }

  materialsSearchResults.className = "search-results";
  const coverage = renderConceptCoverage(results, options.query || materialsSearchInput.value);
  if (coverage) {
    materialsSearchResults.appendChild(coverage);
  }
  const primary = [];
  const related = [];
  results.forEach((result) => {
    if (resultDecisionLabel(result) === "相关参考") {
      related.push(result);
    } else {
      primary.push(result);
    }
  });
  appendSearchResultSection("强匹配", primary);
  appendSearchResultSection("相关参考", related);
}

async function refreshMaterialsList() {
  clearMaterialsFeedback();
  try {
    const userId = currentMaterialsUserId();
    const subject = activeMaterialsSubject();
    const data = await fetchJson(`/api/materials/list?user_id=${encodeURIComponent(userId)}&subject=${encodeURIComponent(subject)}`);
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

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const files = [...selectedFiles];
  let message = input.value.trim();
  if (!message && files.length > 0) {
    message = "这道题怎么做？";
  }
  await submitChatMessage(message, files);
});

function metadataConflictItems(conflict) {
  const conflicts = Array.isArray(conflict.conflicts) && conflict.conflicts.length
    ? conflict.conflicts
    : [conflict];
  return conflicts.filter((item) => item && item.field && item.detected);
}

function metadataFieldLabel(field) {
  return field === "material_type" ? "资料类型" : "学科";
}

function metadataValueLabel(field, value) {
  return materialLabel(field === "material_type" ? MATERIAL_TYPE_LABELS : MATERIAL_SUBJECT_LABELS, value);
}

function applyDetectedMetadata(conflict) {
  metadataConflictItems(conflict).forEach((item) => {
    if (item.field === "subject" && item.detected) {
      materialsSubject.value = item.detected;
    }
    if (item.field === "material_type" && item.detected) {
      materialsType.value = item.detected;
    }
  });
}

function metadataRetryOverrides(data) {
  const overrides = data?.metadata?.metadata_retry_overrides;
  if (!overrides || typeof overrides !== "object") return null;
  if (!overrides.cleaning_strategy || !overrides.document_zones || !overrides.metadata_profile) return null;
  return overrides;
}

function appendMetadataOverrideFields(formData, retryOverrides) {
  if (!retryOverrides) return;
  formData.append("cleaning_strategy_override", JSON.stringify(retryOverrides.cleaning_strategy));
  formData.append("document_zones_override", JSON.stringify(retryOverrides.document_zones));
  formData.append("metadata_profile_override", JSON.stringify(retryOverrides.metadata_profile));
}

function showMetadataConflictDialog(conflict) {
  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.className = "metadata-dialog-overlay";

    const dialog = document.createElement("section");
    dialog.className = "metadata-dialog";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "metadataDialogTitle");

    const title = document.createElement("h3");
    title.id = "metadataDialogTitle";
    title.textContent = "资料分类可能选错了";

    const intro = document.createElement("p");
    intro.textContent = "系统识别结果与你当前选择不一致。你可以继续使用当前选择，也可以改用系统识别结果。";

    const list = document.createElement("div");
    list.className = "metadata-dialog-list";
    metadataConflictItems(conflict).forEach((item) => {
      const row = document.createElement("p");
      row.textContent = `${metadataFieldLabel(item.field)}：你选择「${metadataValueLabel(item.field, item.selected)}」，系统识别「${metadataValueLabel(item.field, item.detected)}」`;
      list.appendChild(row);
    });

    const actions = document.createElement("div");
    actions.className = "metadata-dialog-actions";

    const resolveAndClose = (action) => {
      overlay.remove();
      resolve(action);
    };

    const continueButton = document.createElement("button");
    continueButton.type = "button";
    continueButton.className = "dark-button";
    continueButton.textContent = "仍按我的选择入库";
    continueButton.addEventListener("click", () => resolveAndClose("continue"));

    const reselectButton = document.createElement("button");
    reselectButton.type = "button";
    reselectButton.textContent = "改用系统识别";
    reselectButton.addEventListener("click", () => resolveAndClose("reselect"));

    const cancelButton = document.createElement("button");
    cancelButton.type = "button";
    cancelButton.className = "small-button";
    cancelButton.textContent = "取消";
    cancelButton.addEventListener("click", () => resolveAndClose("cancel"));

    actions.appendChild(continueButton);
    actions.appendChild(reselectButton);
    actions.appendChild(cancelButton);
    dialog.appendChild(title);
    dialog.appendChild(intro);
    dialog.appendChild(list);
    dialog.appendChild(actions);
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    reselectButton.focus();
  });
}

async function submitMaterialsUpload(options = {}) {
  const uploadOptions = typeof options === "boolean" ? { allowMetadataMismatch: options } : options;
  const allowMetadataMismatch = Boolean(uploadOptions.allowMetadataMismatch);
  const retryOverrides = uploadOptions.retryOverrides || null;
  clearMaterialsFeedback();

  const file = materialsFileInput.files[0];
  if (!file) {
    setBanner(materialsError, "请选择要上传的 .md、.txt 或 .pdf 文件");
    return;
  }
  const fileExt = (file.name.split(".").pop() || "").toLowerCase();
  const isPdf = fileExt === "pdf";

  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", currentMaterialsUserId());
  formData.append("subject", materialsSubject.value);
  formData.append("material_type", materialsType.value);
  formData.append("use_llm_cleanup", "true");
  formData.append("async_upload", "true");
  formData.append("allow_metadata_mismatch", allowMetadataMismatch ? "true" : "false");
  appendMetadataOverrideFields(formData, retryOverrides);

  try {
    materialsUploadButton.disabled = true;
    materialsUploadButton.textContent = isPdf ? "PDF 解析中..." : "AI 整理中...";
    setBanner(
      materialsStatus,
      isPdf
        ? "正在上传 PDF，并调用本地 MinerU 解析为 Markdown；随后会生成清洗策略、切块并建立索引。PDF 处理可能需要一两分钟。"
        : "正在上传资料，并按文件后缀选择解析器；随后调用 AI 生成清洗策略，请稍等。"
    );
    setUploadProgress({
      stage_label: "上传文件",
      progress: 2,
      message: "正在上传文件，上传完成后会继续显示解析、清洗、分块和索引进度。",
    });
    let data = await fetchJson("/api/materials/upload", {
      method: "POST",
      body: formData,
    });
    if (data.async && data.job_id) {
      setUploadProgress(data);
      data = await waitForUploadJob(data.job_id);
    }
    if (data?.error === "metadata_conflict") {
      const conflict = data.metadata?.metadata_conflict || {};
      const action = await showMetadataConflictDialog(conflict);
      if (action === "continue") {
        materialsUploadButton.disabled = false;
        return submitMaterialsUpload({
          allowMetadataMismatch: true,
          retryOverrides: metadataRetryOverrides(data),
        });
      }
      if (action === "reselect") {
        applyDetectedMetadata(conflict);
        materialsUploadButton.disabled = false;
        return submitMaterialsUpload({
          allowMetadataMismatch: true,
          retryOverrides: metadataRetryOverrides(data),
        });
      }
      setBanner(materialsError, "已取消上传。你可以调整学科或资料类型后重新上传。");
      return null;
    }
    if (data?.error === "metadata_detection_required") {
      setBanner(materialsError, "自动识别需要 AI 分类，但本次没有得到高置信度结果。请手动选择学科和资料类型后重新上传。");
      return null;
    }
    if (!data || data.error) {
      throw new Error(data?.error || "资料处理失败");
    }
    const cleaning = data.metadata?.raw_markdown_cleaning;
    const source = cleaning?.strategy_source ? `，策略来源：${cleaning.strategy_source}` : "";
    setBanner(materialsStatus, `资料已入库，生成 ${data.chunk_count} 个 chunks${source}`);
    materialsUploadForm.reset();
    materialsUserIdInput.value = currentMaterialsUserId();
    materialsSubject.value = "auto";
    materialsType.value = "auto";
    await refreshMaterialsList();
    return data;
  } catch (error) {
    setBanner(materialsError, `上传失败：${error.message}`);
    return null;
  } finally {
    materialsUploadButton.disabled = false;
    materialsUploadButton.textContent = "上传资料";
  }
}

materialsUploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitMaterialsUpload(false);
});

materialsRefreshButton.addEventListener("click", () => {
  void refreshMaterialsList();
});

materialsUserIdInput.addEventListener("change", () => {
  rememberMaterialsUserId();
  const changed = syncSystemUserScope();
  if (activeMaterialsMode === MATERIALS_MODE_SYSTEM) {
    if (changed) {
      renderSystemDrawerEmpty();
    }
    void loadSystemQuestions();
    return;
  }
  void refreshMaterialsList();
});

materialsUserIdInput.addEventListener("input", () => {
  rememberMaterialsUserId();
});

materialsLibraryTabs.forEach((button) => {
  button.addEventListener("click", () => {
    setActiveMaterialsSubject(button.dataset.materialsSubject);
  });
});

materialsModeTabs.forEach((button) => {
  button.addEventListener("click", () => {
    setMaterialsMode(button.dataset.materialsMode, { skipRefreshWhenCurrent: true });
  });
});

function bindSystemTabGroup(buttons, datasetKey) {
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const value = button.dataset[datasetKey];
      buttons.forEach((item) => {
        const active = item.dataset[datasetKey] === value;
        item.classList.toggle("active", active);
        item.setAttribute("aria-selected", active ? "true" : "false");
      });
      if (datasetKey === "systemSubject") {
        systemState.subject = value || "math";
      }
      if (datasetKey === "systemContent") {
        systemState.contentType = value === "topics" ? "knowledge" : (value || "questions");
      }
      if (systemTutor.active) {
        exitSystemQuestionTutor();
      }
      systemState.page = 1;
      systemState.selectedQuestionId = "";
      systemState.selectedQuestion = null;
      void loadSystemQuestions();
    });
  });
}

bindSystemTabGroup(systemSubjectTabs, "systemSubject");
bindSystemTabGroup(systemContentTabs, "systemContent");

function initializeSystemFilterOptions() {
  if (systemYearFilter && systemYearFilter.options.length <= 1) {
    for (let year = 2025; year >= 1987; year -= 1) {
      const option = document.createElement("option");
      option.value = String(year);
      option.textContent = String(year);
      systemYearFilter.appendChild(option);
    }
  }
  if (systemQuestionTypeFilter && systemQuestionTypeFilter.options.length <= 1) {
    [
      ["single_choice", "选择题"],
      ["fill_blank", "填空题"],
      ["solution", "解答题"],
    ].forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      systemQuestionTypeFilter.appendChild(option);
    });
  }
}

initializeSystemFilterOptions();

[
  systemLibraryNameFilter,
  systemYearFilter,
  systemQuestionTypeFilter,
  systemStatusFilter,
].forEach((element) => {
  element?.addEventListener("change", () => {
    systemState.page = 1;
    void loadSystemQuestions();
  });
});

systemTopicFilter?.addEventListener("change", () => {
  systemState.page = 1;
  void loadSystemQuestions();
});

systemSearchInput?.addEventListener("input", () => {
  window.clearTimeout(systemSearchInput.dataset.systemFilterTimer);
  systemSearchInput.dataset.systemFilterTimer = window.setTimeout(() => {
    systemState.page = 1;
    void loadSystemQuestions();
  }, 260);
});

document.querySelectorAll("[data-system-action]").forEach((button) => {
  button.addEventListener("click", () => {
    applySystemBatchAction(button.dataset.systemAction);
  });
});

reviewTasksRefreshButton?.addEventListener("click", () => {
  void loadReviewLearningInsights();
  void loadReviewTasks();
});
reviewAiPlanButton?.addEventListener("click", () => {
  void openAiReviewPlanModal();
});

reviewTaskList?.addEventListener("click", handleReviewTaskAction);
reviewLearningInsights?.addEventListener("click", handleReviewInsightAction);
reviewLearningInsights?.addEventListener("keydown", handleReviewInsightKeydown);

function bindReviewTaskFilters() {
  const refresh = () => {
    reviewTasksState.filters.subject = reviewSubjectFilter?.value || "";
    reviewTasksState.filters.targetType = reviewTargetTypeFilter?.value || "";
    reviewTasksState.filters.dateGroup = reviewDateGroupFilter?.value || "";
    reviewTasksState.filters.keyword = reviewKeywordFilter?.value.trim() || "";
    void loadReviewLearningInsights();
    void loadReviewTasks();
  };
  [reviewSubjectFilter, reviewTargetTypeFilter, reviewDateGroupFilter].forEach((element) => {
    element?.addEventListener("change", refresh);
  });
  reviewKeywordFilter?.addEventListener("input", () => {
    window.clearTimeout(reviewKeywordFilter.dataset.reviewFilterTimer);
    reviewKeywordFilter.dataset.reviewFilterTimer = window.setTimeout(refresh, 260);
  });
}

bindReviewTaskFilters();

document.addEventListener("selectionchange", updateSystemTutorSelectionActions);

restoreMaterialsUserIdFromStorage();

materialsSearchScope?.addEventListener("change", () => {
  const scopeValue = materialsSearchScope.value || "subject";
  activeMaterialSearchId = scopeValue.startsWith("material:")
    ? scopeValue.slice("material:".length)
    : "";
  updateMaterialCardSelection();
});

materialsSearchMode?.addEventListener("change", updateMaterialsSearchModeStatus);

materialDetailCloseButton?.addEventListener("click", closeMaterialDetailDrawer);
materialDetailBackdrop?.addEventListener("click", closeMaterialDetailDrawer);

materialsSearchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMaterialsFeedback();
  const query = materialsSearchInput.value.trim();
  if (!query) {
    setBanner(materialsError, "请输入搜索关键词");
    return;
  }

  try {
    const data = await fetchJson(buildMaterialsSearchUrl(query));
    renderMaterialsSearchSummary(data, query);
    renderSearchResults(data.results || [], { query });
    if (!data.results || data.results.length === 0) {
      setBanner(materialsStatus, "当前范围中没有找到强匹配内容，可以换关键词或扩大搜索范围");
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
syncMaterialsSearchScopeOptions();
updateMaterialsSearchModeStatus();
setActiveMaterialsSubject(activeMaterialsSubject(), { keepSearch: true, skipRefresh: true });
setMaterialsMode(activeMaterialsMode, { skipRefresh: true });
setActivePage(restoreActivePageFromStorage());
