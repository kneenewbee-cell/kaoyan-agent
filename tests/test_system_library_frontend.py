from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "web" / "app.js"
INDEX_HTML = ROOT / "web" / "index.html"
STYLES_CSS = ROOT / "web" / "styles.css"


class SystemLibraryFrontendTests(unittest.TestCase):
    def test_question_cards_expose_preview_dialog_entry(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function openSystemQuestionPreview", source)
        self.assertIn("system-preview-button", source)
        self.assertIn("system-eye-icon", source)
        self.assertIn("openSystemQuestionPreview(item.question_id)", source)

    def test_question_markdown_images_render_in_place(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderSystemQuestionMarkdown(question)", source)
        self.assertIn("renderSystemQuestionMarkdown(question)", source)
        self.assertIn("function latestSubmittedPracticeAttempt", source)
        self.assertIn("data-practice-latest-result-open", source)
        self.assertIn("practice-attempts?practice_set_id", source)
        self.assertIn("renderPracticeAttemptResult(overlay, practiceSet, questions, detailAttempt", source)
        self.assertIn("function renderSystemAssetFallback(question)", source)
        self.assertNotIn("template.content.querySelectorAll(\"img\").forEach((image) => image.remove())", source)

    def test_question_markdown_images_have_drawer_and_preview_size_rules(self) -> None:
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn(".system-markdown img", styles)
        self.assertIn("object-fit: contain", styles)
        self.assertIn(".system-preview-dialog-body .system-markdown img", styles)
        self.assertIn("#systemQuestionDrawer .system-markdown img", styles)

    def test_system_question_ask_ai_uses_temporary_tutor_stream(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertIn("function askAiForSystemQuestion(question)", source)
        self.assertIn("function startSystemQuestionTutor(question)", source)
        self.assertIn("async function sendSystemTutorMessage(message", source)
        self.assertIn("/tutor/stream", source)
        self.assertIn("systemTutor.history", source)
        self.assertIn('id="systemQuestionTutorPanel"', html)
        self.assertIn("data-system-ask-ai", source)
        ask_function = source[source.index("async function askAiForSystemQuestion") : source.index("async function saveSystemQuestionState")]
        self.assertNotIn('setActivePage("chat")', ask_function)
        self.assertNotIn("submitChatMessage", ask_function)

    def test_system_question_tutor_can_add_selected_answer_text_to_note(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function updateSystemTutorSelectionActions", source)
        self.assertIn("function appendSelectedSystemTutorTextToNote", source)
        self.assertIn("system-tutor-selection-actions", source)
        self.assertIn("data-system-tutor-add-note", source)
        self.assertIn("saveSystemQuestionState(systemTutor.questionId", source)
        self.assertIn(".system-tutor-selection-actions.visible", styles)

    def test_chat_submit_uses_reusable_submit_function(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("async function submitChatMessage(message, files = [])", source)
        self.assertIn("await submitChatMessage(message, files)", source)
        self.assertIn('form.addEventListener("submit"', source)

    def test_question_type_and_mastery_status_share_pill_treatment(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('class="status-pill type"', source)
        self.assertIn(".status-pill.not_started", styles)
        self.assertIn(".status-pill.learning", styles)
        self.assertIn(".status-pill.mastered", styles)

    def test_preview_has_modal_and_clipped_card_affordance(self) -> None:
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn(".system-preview-overlay", styles)
        self.assertIn(".system-preview-dialog", styles)
        self.assertIn(".system-question-preview::after", styles)

    def test_pagination_exposes_visible_previous_and_next_controls(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("system-pagination-current", source)
        self.assertIn("上一页", source)
        self.assertIn("下一页", source)
        self.assertIn(".system-pagination .small-button", styles)

    def test_buttons_have_non_transparent_visible_treatment(self) -> None:
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("--button-bg: #ffffff", styles)
        self.assertIn("--button-text: #172033", styles)
        self.assertIn("--button-border: rgba(23, 32, 51, 0.16)", styles)
        self.assertIn("background: var(--button-bg);", styles)
        self.assertIn("color: var(--button-text);", styles)
        self.assertNotIn("background: rgba(255, 255, 255, 0.08);", styles)
        self.assertNotIn("opacity: 0.6;", styles)
        self.assertIn("cursor: not-allowed;", styles)

    def test_workflow_dialog_buttons_are_visible_and_cache_busted(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("styles.css?v=20260709-review-workflow-v1", html)
        self.assertIn("app.js?v=20260709-review-workflow-v1", html)
        self.assertIn(".system-workflow-dialog .small-button", styles)
        self.assertIn(".system-workflow-dialog .dark-button", styles)
        self.assertIn("background: #ffffff;", styles)
        self.assertIn("color: #172033;", styles)

    def test_topic_filter_is_select_backed_by_topic_options(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('<select id="systemTopicFilter">', html)
        self.assertNotIn('<input id="systemTopicFilter"', html)
        self.assertIn("function renderSystemTopicOptions", source)
        self.assertIn("data.topic_options", source)
        self.assertIn('systemTopicFilter?.addEventListener("change"', source)

    def test_system_library_filter_exposes_math2_and_math3_collections(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('<option value="math1">数学一真题</option>', html)
        self.assertIn('<option value="math2">数学二真题</option>', html)
        self.assertIn('<option value="math3">数学三真题</option>', html)
        self.assertIn('systemState.examType = systemLibraryNameFilter ? systemLibraryNameFilter.value : "math1";', source)
        self.assertIn('exam_type: systemState.examType', source)
        self.assertIn("function systemExamTypeLabel", source)
        self.assertIn('当前${currentExamLabel}题库', source)

    def test_review_wrong_action_opens_filterable_wrong_pool_workflow(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function openWrongQuestionPoolModal", source)
        self.assertIn("function renderWrongQuestionPoolModal", source)
        self.assertIn("/api/materials/system/wrong-question-pool", source)
        self.assertIn("/api/materials/system/practice-sets/from-wrong-pool", source)
        self.assertIn("data-wrong-pool-topic", source)
        self.assertIn("data-wrong-pool-risk-type", source)
        self.assertIn("data-wrong-pool-create", source)
        self.assertIn("risk_type", source)
        self.assertIn("priority_reasons", source)
        self.assertIn("priority-reason-list", source)
        self.assertIn("openWrongQuestionPoolModal();", source)
        self.assertIn("共练", source)
        self.assertIn("判断可信度", source)
        self.assertIn(".wrong-pool-list", styles)
        self.assertIn(".wrong-pool-item", styles)
        self.assertIn(".priority-reason-list", styles)
        self.assertIn(".priority-reason-chip", styles)

    def test_system_question_state_patch_is_saved_with_current_user(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("async function saveSystemQuestionState(questionId, patch", source)
        self.assertIn("/api/materials/system/questions/${encodeURIComponent(questionId)}/state", source)
        self.assertIn("user_id=${encodeURIComponent(currentMaterialsUserId())}", source)
        self.assertIn('method: "PATCH"', source)
        self.assertIn('headers: { "Content-Type": "application/json" }', source)
        self.assertIn("JSON.stringify(patch)", source)
        self.assertIn("data.personal_state", source)

    def test_system_question_personal_state_is_hydrated_from_list_and_detail(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function hydrateSystemQuestionPersonalState(questionId, personalState)", source)
        self.assertIn("item.personal_state", source)
        self.assertIn("hydrateSystemQuestionPersonalState(item.question_id, item.personal_state)", source)
        self.assertIn("detail.personal_state", source)
        self.assertIn("hydrateSystemQuestionPersonalState(detail.question_id, detail.personal_state)", source)

    def test_system_fetches_propagate_current_user_id(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('params.set("user_id", currentMaterialsUserId())', source)
        self.assertIn("function systemQuestionDetailUrl(questionId)", source)
        self.assertIn("/api/materials/system/questions/${encodeURIComponent(questionId)}", source)
        self.assertIn("user_id=${encodeURIComponent(currentMaterialsUserId())}", source)
        self.assertGreaterEqual(source.count("fetchJson(systemQuestionDetailUrl(questionId))"), 3)

    def test_system_status_filter_is_sent_to_api_before_pagination(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('if (systemState.status) params.set("user_status", systemState.status);', source)
        self.assertNotIn("当前页筛出", source)

    def test_system_question_state_cache_is_cleared_when_user_changes(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('userId: ""', source)
        self.assertIn("function syncSystemUserScope()", source)
        self.assertIn("window.clearTimeout(systemNoteSaveTimer)", source)
        self.assertIn("systemState.userState.clear()", source)
        self.assertIn("systemState.selectedIds.clear()", source)
        self.assertIn("systemState.selectedQuestionId = \"\"", source)
        self.assertIn("systemState.selectedQuestion = null", source)
        self.assertIn("syncSystemUserScope();", source)
        self.assertIn('materialsUserIdInput.addEventListener("change"', source)

    def test_system_question_state_saves_use_stable_user_scope(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("const userId = options.userId || currentMaterialsUserId();", source)
        self.assertIn("user_id=${encodeURIComponent(userId)}", source)
        self.assertIn("void loadSystemQuestions();\n    return;", source)
        self.assertIn("saveSystemQuestionState(questionId, patch, { ...options, userId })", source)
        self.assertIn("const noteUserId = systemState.userId || currentMaterialsUserId();", source)
        self.assertIn("if (noteUserId !== currentMaterialsUserId()) return;", source)
        self.assertIn("{ renderDrawer: false, userId: noteUserId }", source)

    def test_question_topics_live_in_card_footer_near_actions(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('footer.className = "system-question-footer"', source)
        self.assertIn("footer.appendChild(topics)", source)
        self.assertIn("footer.appendChild(actions)", source)
        self.assertLess(source.index("body.appendChild(preview)"), source.index("body.appendChild(footer)"))
        self.assertNotIn("body.appendChild(topics);", source)
        self.assertIn(".system-question-footer", styles)

    def test_favorited_question_cards_have_persistent_visual_marker(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('card.classList.toggle("favorite", personal.is_favorite)', source)
        self.assertIn('favoriteButton.className = `small-button ${personal.is_favorite ? "active" : ""}`', source)
        self.assertIn(".system-question-card.favorite", styles)

    def test_materials_user_id_survives_page_reload(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("const MATERIALS_USER_ID_STORAGE_KEY", source)
        self.assertIn("function restoreMaterialsUserIdFromStorage()", source)
        self.assertIn("function rememberMaterialsUserId()", source)
        self.assertIn("restoreMaterialsUserIdFromStorage();", source)
        self.assertIn("rememberMaterialsUserId();", source)

    def test_active_page_and_materials_mode_survive_page_reload(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("const ACTIVE_PAGE_STORAGE_KEY", source)
        self.assertIn("const MATERIALS_MODE_STORAGE_KEY", source)
        self.assertIn("function restoreActivePageFromStorage()", source)
        self.assertIn("function rememberActivePage(pageId)", source)
        self.assertIn("function restoreMaterialsModeFromStorage()", source)
        self.assertIn("function rememberMaterialsMode(mode)", source)
        startup_block = source[source.rfind("switchSession(activeSessionId())") :]
        self.assertIn("setActivePage(restoreActivePageFromStorage());", startup_block)
        self.assertNotIn('setActivePage("chat");', startup_block)

    def test_system_state_summary_chips_have_api_backed_entry(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="systemStatusSummary"', html)
        self.assertIn("function loadSystemStatusSummary", source)
        self.assertIn("/api/materials/system/questions/state-summary", source)
        self.assertIn("data-system-status-chip", source)
        self.assertIn(".system-status-summary", styles)

    def test_system_state_save_feedback_has_visible_status_entry(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="systemSaveStatus"', html)
        self.assertIn("function setSystemSaveStatus", source)
        self.assertIn("system-save-status saving", source)
        self.assertIn("system-save-status saved", source)
        self.assertIn("system-save-status error", source)
        self.assertIn(".system-save-status", styles)

    def test_drawer_practice_and_review_actions_are_not_placeholder_bound(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertNotIn("data-system-placeholder-action", source)
        self.assertIn("data-system-open-practice", source)
        self.assertIn("data-system-open-review", source)
        self.assertIn("function openSystemPracticeModal", source)
        self.assertIn("function openSystemReviewModal", source)

    def test_practice_modal_exposes_complete_configuration_and_creation_flow(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderSystemPracticeModal", source)
        self.assertIn("data-system-practice-count", source)
        self.assertIn("data-system-practice-same-type", source)
        self.assertIn("data-system-practice-exclude-mastered", source)
        self.assertIn("data-system-practice-candidates", source)
        self.assertIn("data-system-practice-create", source)
        self.assertIn("/api/materials/system/practice-sets", source)
        self.assertIn("/api/materials/system/practice-candidates", source)
        self.assertIn("function loadSystemPracticeCandidatePreview", source)
        self.assertIn("previewCandidates", source)
        self.assertIn("function renderSystemPracticeSetSummary", source)

    def test_review_modal_exposes_due_date_priority_note_and_save_flow(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderSystemReviewModal", source)
        self.assertIn("data-system-review-due-date", source)
        self.assertIn("data-system-review-priority", source)
        self.assertIn("data-system-review-note", source)
        self.assertIn("data-system-review-save", source)
        self.assertIn("/api/materials/system/review-tasks", source)
        self.assertIn("function markQuestionReviewScheduled", source)

    def test_plan_page_has_review_task_workbench_sections_and_actions(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="reviewTaskList"', html)
        self.assertIn("function loadReviewTasks", source)
        self.assertIn("function renderReviewTasks", source)
        self.assertIn("data-review-task-complete", source)
        self.assertIn("data-review-task-postpone", source)
        self.assertIn("data-review-task-cancel", source)
        self.assertIn("data-review-task-delete", source)
        self.assertIn("data-review-task-open", source)
        self.assertIn("data-review-task-restore", source)
        self.assertIn("开始复习", source)
        self.assertIn("推迟", source)
        self.assertIn("取消", source)
        self.assertIn("删除", source)
        self.assertIn("grid-template-columns: minmax(0, 1fr);", styles)
        self.assertIn(".review-task-actions .small-button:not(.dark-button)", styles)
        self.assertIn("color: #172033;", styles)
        self.assertIn(".plan-workbench", styles)

    def test_plan_page_has_subject_type_date_and_keyword_filters(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn('id="reviewSubjectFilter"', html)
        self.assertIn('id="reviewTargetTypeFilter"', html)
        self.assertIn('id="reviewDateGroupFilter"', html)
        self.assertIn('id="reviewKeywordFilter"', html)
        self.assertIn("function buildReviewTaskQuery", source)
        self.assertIn('params.set("subject", reviewTasksState.filters.subject)', source)
        self.assertIn('params.set("target_type", reviewTasksState.filters.targetType)', source)
        self.assertIn('params.set("date_group", reviewTasksState.filters.dateGroup)', source)
        self.assertIn('params.set("keyword", reviewTasksState.filters.keyword)', source)
        self.assertIn("bindReviewTaskFilters", source)

    def test_review_plan_workbench_uses_unified_start_and_confirmed_actions(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        active_card_renderer = source[source.rfind("function renderReviewTaskCard"):]

        self.assertIn("function reviewTaskTargetTypeLabel", source)
        self.assertIn("function reviewTaskStatusLabel", source)
        self.assertIn("function renderReviewTaskActions", source)
        self.assertNotIn("legacy-review-task-actions", source)
        self.assertIn("function openReviewTaskPostponeDialog", source)
        self.assertIn("data-review-postpone-date", source)
        self.assertIn("data-review-postpone-save", source)
        self.assertNotIn("legacy-review-task-actions", active_card_renderer)
        self.assertIn("开始复习", source)
        self.assertIn("已完成", source)
        self.assertIn("已取消", source)
        self.assertNotIn("function promptReviewTaskDueDate", source)
        self.assertIn("openReviewTaskPostponeDialog(task)", source)
        self.assertIn("window.confirm", source)
        self.assertIn("renderReviewTaskSection(\"已完成\", groups.completed)", source)
        self.assertIn("renderReviewTaskSection(\"已取消\", groups.cancelled)", source)

    def test_practice_modal_exposes_topic_filter_subset(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function systemPracticeTopicOptions", source)
        self.assertIn("data-system-practice-source-scope", source)
        self.assertIn("config.sourceScope", source)
        self.assertIn("source_scope: config.sourceScope", source)
        self.assertIn("data-system-practice-topic-filter", source)
        self.assertIn("config.topicFilters", source)
        self.assertIn("topic_filters: config.topicFilters", source)

    def test_practice_modal_waits_for_candidates_and_offers_empty_recovery(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function systemPracticeCanCreate", source)
        self.assertIn("!config.previewLoading", source)
        self.assertIn("config.previewLoaded", source)
        self.assertIn("function reloadSystemPracticeCandidatePreview", source)
        self.assertIn("data-system-practice-relax-topics", source)
        self.assertIn("data-system-practice-relax-type", source)
        self.assertIn("data-system-practice-expand-scope", source)
        self.assertIn('config.topicFilters = [];', source)
        self.assertIn('config.sameType = false;', source)
        self.assertIn('config.sourceScope = "subject";', source)
        self.assertIn('data-system-practice-create ${canCreate ? "" : "disabled"}', source)
        self.assertNotIn("window.alert(\"当前没有可生成练习单的候选题。\")", source)
        self.assertIn(".system-practice-empty-actions", styles)

    def test_system_markdown_normalizes_split_choice_options(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function normalizeSystemChoiceOptionMarkdown", source)
        self.assertIn("normalizeSystemChoiceOptionMarkdown(text)", source)
        self.assertIn("optionParts.join(\" \")", source)
        self.assertIn("function systemChoiceMarker", source)
        self.assertIn("isSystemChoiceBoundary(nextLine)", source)
        self.assertIn("isSystemChoiceSectionEnd(nextLine)", source)

    def test_system_markdown_turns_math_code_spans_into_latex(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function normalizeSystemMathCodeSpans", source)
        self.assertIn("normalizeSystemMathCodeSpans(normalizeSystemChoiceOptionMarkdown(text))", source)
        self.assertIn("function normalizeSystemMathCodeExpression", source)
        self.assertIn("sqrtMatch", source)
        self.assertIn("`([^`\\n]+)`", source)

    def test_practice_set_detail_is_continuous_paper_with_question_menus(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function openSystemPracticeSetDetail", source)
        self.assertIn("function renderSystemPracticeSetDetail", source)
        self.assertIn("查看练习单", source)
        self.assertIn("data-practice-detail-paper", source)
        self.assertIn("practice-paper-question", source)
        self.assertIn("data-practice-question-menu", source)
        self.assertIn("data-practice-question-wrong", source)
        self.assertIn("data-practice-question-mastered", source)
        self.assertIn("practice-detail-back-button", source)
        self.assertIn('querySelectorAll("[data-practice-detail-return]")', source)
        self.assertIn("renderSystemQuestionMarkdown(question)", source)
        self.assertIn("返回复习规划", source)
        self.assertIn("加入复习规划", source)
        self.assertIn("data-practice-download-pdf", source)
        self.assertIn("打印/另存 PDF", source)
        self.assertIn("function openSystemPracticeSetPrintable", source)
        self.assertIn("function showPracticeSetPrintOverlay", source)
        self.assertIn("practice-print-overlay", source)
        self.assertIn("practice-printing", source)
        self.assertIn(".print()", source)
        self.assertNotIn("window.open(\"\", \"_blank\")", source)
        self.assertIn(".practice-result-actions", styles)
        self.assertIn(".practice-detail-paper", styles)
        self.assertIn(".practice-detail-back-button", styles)
        self.assertIn(".practice-paper-question", styles)
        self.assertIn(".practice-latest-result", styles)
        self.assertIn(".practice-question-menu-panel", styles)
        self.assertIn(".practice-print-overlay", styles)

    def test_practice_set_detail_links_to_latest_submitted_result(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function latestSubmittedPracticeAttempt", source)
        self.assertIn("function practiceAttemptSummaryText", source)
        self.assertIn("data-practice-latest-result", source)
        self.assertIn("data-practice-latest-result-open", source)
        self.assertIn("practice-attempts?practice_set_id", source)
        self.assertIn("renderPracticeAttemptResult(overlay, practiceSet, questions, detailAttempt", source)
        self.assertIn(".practice-latest-result", styles)

    def test_practice_attempt_flow_exposes_draft_submit_and_result_surfaces(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function openPracticeAttempt", source)
        self.assertIn("function renderPracticeAttemptDraft", source)
        self.assertIn("function renderPracticeAttemptResult", source)
        self.assertIn("body.scrollTop = 0;", source)
        self.assertIn("function renderPracticeAnswerInput", source)
        self.assertIn("async function savePracticeAttemptAnswers", source)
        self.assertIn("async function submitPracticeAttempt", source)
        self.assertIn("data-practice-start-attempt", source)
        self.assertIn("data-practice-answer-input", source)
        self.assertIn("data-practice-attempt-submit", source)
        self.assertIn("data-practice-card-link", source)
        self.assertIn("data-practice-current-index", source)
        self.assertIn("data-practice-prev", source)
        self.assertIn("data-practice-next", source)
        self.assertIn("practice-answer-nav-button", source)
        self.assertIn("practice-choice-option-content", source)
        self.assertIn("practiceChoiceOptions", source)
        self.assertIn("normalizePracticeChoiceText", source)
        self.assertIn("renderPracticeQuestionMarkdown", source)
        self.assertIn("async function resolvePracticeAttemptQuestions", source)
        self.assertIn("await fetchJson(systemQuestionDetailUrl(questionId))", source)
        self.assertIn("const detailQuestions = await resolvePracticeAttemptQuestions(practiceSet, questions, options);", source)
        self.assertIn("renderPracticeAttemptDraft(overlay, practiceSet, detailQuestions", source)
        self.assertIn("renderPracticeAttemptResult(overlay, practiceSet, detailQuestions", source)
        self.assertIn("function stripPracticeChoiceOptionsFromMarkdown", source)
        self.assertIn("function practiceQuestionMarkdownForAttempt", source)
        self.assertIn("const strippedMarkdown = practiceQuestionMarkdownForAttempt(question);", source)
        self.assertIn("return renderSystemQuestionMarkdown({ ...question, question_markdown: strippedMarkdown });", source)
        self.assertNotIn("return renderSystemQuestionMarkdown(question);", source)
        self.assertNotIn("practiceQuestionStemMarkdown(currentQuestion)", source)
        self.assertIn("practiceSetCurrentQuestionIndex", source)
        self.assertIn("renderPracticeAttemptDraft(overlay, practiceSet, questions, practiceAttempt, { ...options, currentQuestionIndex:", source)
        self.assertIn("/api/materials/system/practice-sets/${encodeURIComponent(practiceSetId)}/attempts", source)
        self.assertIn("/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/answers", source)
        self.assertIn("/api/materials/system/practice-attempts/${encodeURIComponent(attemptId)}/submit", source)
        self.assertIn("async function fetchPracticeAttemptDetail", source)
        self.assertIn("practice_attempt", source)
        self.assertIn("提交后本次练习记录不可修改", source)
        self.assertIn("再次练习将在后续版本开放", source)
        self.assertIn('return "blank";', source)
        self.assertNotIn('return "fill_blank";', source)
        self.assertIn("practice-attempt-dialog", source)
        self.assertIn("practice-attempt-overlay", source)
        self.assertIn(".system-workflow-overlay.practice-attempt-overlay", styles)
        self.assertIn("width: min(1280px, calc(100vw - 16px));", styles)
        self.assertIn("height: calc(100vh - 16px);", styles)
        self.assertIn(".practice-attempt-dialog .system-workflow-header", styles)
        self.assertIn(".practice-attempt-dialog .system-workflow-header .helper-text", styles)
        self.assertIn(".practice-attempt-dialog .system-workflow-body", styles)
        self.assertIn("padding: 10px;", styles)
        self.assertIn("gap: 8px;", styles)
        self.assertIn("max-height: none;", styles)
        self.assertIn(".practice-paper-question-body", styles)
        self.assertIn("min-height: 360px;", styles)
        self.assertIn("overflow: visible;", styles)
        self.assertIn("grid-template-columns: minmax(0, 1fr) 150px;", styles)
        self.assertIn(".practice-attempt-layout", styles)
        self.assertIn(".practice-paper-question.current", styles)
        self.assertIn("min-height: calc(100vh - 190px);", styles)
        self.assertIn(".practice-answer-nav-button", styles)
        self.assertIn(".practice-answer-nav-button.answered", styles)
        self.assertIn("grid-template-columns: repeat(auto-fit, minmax(34px, 1fr));", styles)
        self.assertIn(".practice-answer-nav-button:not(.answered)", styles)
        self.assertIn("background: #ffffff;", styles)
        self.assertIn(".practice-answer-card", styles)
        self.assertIn(".practice-result-table", styles)

    def test_practice_attempt_navigation_and_result_feedback_are_explicit(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("data-system-practice-start", source)
        self.assertIn("data-system-practice-view", source)
        self.assertIn("开始练习", source)
        self.assertIn("查看练习单", source)
        self.assertIn("openPracticeAttempt(config.createdPracticeSet", source)
        self.assertNotIn("data-practice-attempt-return", source)
        self.assertNotIn("data-practice-result-return", source)
        self.assertIn("practice-attempt-submit-bar", source)
        self.assertIn('if (answerType === "blank")', source)
        self.assertIn("practiceResultStatusClass", source)
        self.assertIn("function practiceAttemptFinalStatus", source)
        self.assertIn("result.final_status", source)
        self.assertIn("pending_review:", source)
        self.assertIn("data-practice-ai-grade", source)
        self.assertIn("/items/${encodeURIComponent(questionId)}/grade", source)
        self.assertIn('judge_method: "ai"', source)
        self.assertIn("function setPracticeAiGradeButtonLoading", source)
        self.assertIn('button.textContent = "正在评分...";', source)
        self.assertIn("button.disabled = true;", source)
        self.assertIn('button.setAttribute("aria-busy", "true");', source)
        self.assertIn("const currentScrollTop = body ? body.scrollTop : 0;", source)
        self.assertIn("restoreWorkflowBodyScroll(body, options.restoreScrollTop);", source)
        self.assertIn('needs_review: "待核对"', source)
        self.assertIn("practice-result-status correct", source)
        self.assertIn("practice-result-status incorrect", source)
        self.assertIn("practice-result-status needs_review", source)
        self.assertIn(".practice-result-status.correct", styles)
        self.assertIn(".practice-result-status.incorrect", styles)
        self.assertIn(".practice-result-status.needs_review", styles)
        self.assertIn(".small-button.is-loading:disabled", styles)

    def test_practice_result_renders_learning_record_insights(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function renderPracticeAttemptInsights", source)
        self.assertIn("data-practice-record-insights", source)
        self.assertIn("practice-record-insights", source)
        self.assertIn("insights: detail.insights ||", source)
        self.assertIn(".practice-record-insights", styles)

    def test_practice_result_next_actions_are_clickable(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("data-practice-next-action", source)
        self.assertIn("applyPracticeResultFocus", source)
        self.assertIn("practice-result-focus-message", source)
        self.assertIn("data-practice-result-status", source)
        self.assertIn("data-practice-result-topics", source)
        self.assertIn(".practice-result-row.is-emphasized", styles)
        self.assertIn(".practice-result-row.is-dimmed", styles)

    def test_practice_result_row_exposes_state_menu(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("practice-result-menu", source)
        self.assertIn("data-practice-result-toggle-favorite", source)
        self.assertIn("data-practice-result-toggle-wrong", source)
        self.assertIn("data-practice-result-toggle-mastery", source)
        self.assertIn("data-practice-result-add-review", source)
        self.assertIn("function savePracticeResultQuestionState", source)
        self.assertIn(".practice-result-menu", styles)

    def test_question_drawer_exposes_learning_history_snapshot(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function loadSystemQuestionLearningSnapshot", source)
        self.assertIn("function renderSystemQuestionLearningSnapshot", source)
        self.assertIn("learning-snapshot", source)
        self.assertIn("data-system-learning-history", source)
        self.assertIn(".system-learning-history", styles)

    def test_review_tasks_render_learning_reasons(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("learning_reasons", source)
        self.assertIn("review-task-reasons", source)
        self.assertIn(".review-task-reasons", styles)

    def test_review_page_renders_learning_insights_dashboard(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="reviewLearningInsights"', html)
        self.assertIn("const reviewLearningInsights", source)
        self.assertIn("learningInsights", source)
        self.assertIn("function loadReviewLearningInsights", source)
        self.assertIn("function renderReviewLearningInsights", source)
        self.assertIn("/api/materials/system/learning-insights", source)
        self.assertIn("data-review-insight-action", source)
        self.assertIn("learningTopicReasonTags", source)
        self.assertIn(".review-learning-insights", styles)
        self.assertIn("grid-template-columns: repeat(auto-fit, minmax(210px, 1fr))", styles)
        self.assertIn(".review-insight-action", styles)

    def test_review_insights_open_topic_panel_and_pending_review_list(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn("function openLearningTopicPanel", source)
        self.assertIn("data-learning-topic-card", source)
        self.assertIn("openPendingReviewModal", source)
        self.assertIn("/api/materials/system/pending-review-items", source)
        self.assertIn("data-pending-review-ai", source)
        self.assertIn("data-pending-review-correct", source)
        self.assertIn("data-pending-review-incorrect", source)
        self.assertIn(".learning-topic-panel", styles)
        self.assertIn(".pending-review-list", styles)
        self.assertIn(".pending-review-item", styles)

    def test_pending_review_manual_confirmation_warns_on_conflicting_evidence(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function pendingReviewManualConflictSources", source)
        self.assertIn("function confirmPendingReviewManualGrade", source)
        self.assertIn("window.confirm", source)
        self.assertIn("manual_conflict_sources", source)
        self.assertIn("manual_evidence", source)
        self.assertIn("config.items.find", source)

    def test_practice_attempt_parses_inline_choice_options(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function parsePracticeChoiceOptionsFromMarkdown", source)
        self.assertIn("function findPracticeChoiceMarkers", source)
        self.assertIn("function orderedPracticeChoiceMarkers", source)
        self.assertIn("parsePracticeChoiceOptionsFromMarkdown(markdown)", source)
        self.assertIn("PRACTICE_CHOICE_KEYS", source)

    def test_practice_attempt_unwraps_object_answers_and_strips_duplicate_choice_options(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function practiceAnswerTextValue", source)
        self.assertIn('practiceAnswerTextValue(answer.value)', source)
        self.assertIn('practiceAnswerTextValue(answer.text)', source)
        self.assertIn('practiceAnswerTextValue(answer.content)', source)
        self.assertIn('practiceAnswerTextValue(answer.markdown)', source)
        self.assertIn("function stripPracticeChoiceOptionsFromMarkdown", source)
        self.assertIn("function stripPracticeChoiceLeadIn", source)
        self.assertIn("stripPracticeChoiceLeadIn(source.slice(0, optionStart).trimEnd())", source)
        self.assertIn("const markers = orderedPracticeChoiceMarkers(findPracticeChoiceMarkers(source));", source)
        self.assertIn("return renderSystemQuestionMarkdown({ ...question, question_markdown: strippedMarkdown });", source)

    def test_system_markdown_normalizes_inline_choice_options(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function normalizeInlineSystemChoiceOptionMarkdown", source)
        self.assertIn("normalizeInlineSystemChoiceOptionMarkdown(text)", source)
        self.assertIn("orderedPracticeChoiceMarkers(findPracticeChoiceMarkers(source))", source)


if __name__ == "__main__":
    unittest.main()
