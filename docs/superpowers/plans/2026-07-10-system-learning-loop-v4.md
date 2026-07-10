# 系统资料库学习闭环 v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不改变系统题库公共内容和现有四个一级入口的前提下，把“生成练习 → 作答保存 → 提交判分 → 记录沉淀 → 错题/待核对处理 → 复习任务”建设成数据可信、可恢复、可追溯、可扩展的完整闭环。

**Architecture:** 第一阶段继续使用 `data/users/{user_id}/system_library/` 下的 JSONL 文件，但新增 repository、迁移和判分事件边界，业务层不再直接依赖整文件读写细节。第二阶段沿用现有前端视觉语言，把复习规划重排为每日工作台，并增加稳定的练习记录出口；所有页面读取真实 attempt、attempt item、grade event 和统计投影，不使用前端临时对象冒充历史记录。

**Tech Stack:** Python 3.14、FastAPI、JSONL、原生 HTML/CSS/JavaScript、KaTeX/现有 Markdown 渲染器、`unittest`、Codex in-app browser 产品审计。

## Global Constraints

- 不重构 `qa/`，AI 判分只通过现有轻量客户端适配层调用。
- 不移动或重构 `data/raw/`，系统题库内容继续只读。
- 系统题目、答案、解析属于公共层；作答、判分、收藏、错题、掌握、备注和复习任务只写用户层。
- 现有 API 路径保持兼容；新增字段必须为旧前端提供安全默认值。
- 第一版继续使用 JSONL，不引入 MySQL；repository 接口必须允许未来替换存储实现。
- 所有写操作必须按 `user_id` 隔离，并校验 `attempt_id + question_id` 的归属关系。
- 不使用透明按钮；按钮必须有可见文字/图标、可见边框或底色、键盘焦点和禁用态。
- 页面新增功能必须明确入口、数据变化、完成态、反向操作和返回出口。
- UI 实现前先完成并确认 `docs/superpowers/prototypes/system-learning-loop-v4-sketch.html`。
- 每个任务采用 TDD，任务结束时运行指定测试并形成独立中文提交。

---

## Target File Structure

```text
materials/
├── system_practice_review.py          # 业务编排，保留现有公开方法
├── system_practice_review_api.py      # HTTP 接口与请求校验
├── system_practice_ai_grader.py       # 轻量 AI 判分适配
├── system_practice_repository.py      # 新增：attempt/item/event/stats JSONL repository
├── system_practice_migration.py       # 新增：旧记录迁移与覆盖率报告
└── system_learning_stats.py           # 新增：规范维度、统计投影和优先级算法

scripts/
└── migrate_system_learning_records.py # 新增：dry-run/execute/verify CLI

web/
├── index.html                         # 复习页二级视图和状态区域
├── app.js                             # 练习记录、可靠保存、闭环动作
└── styles.css                         # 工作台、记录列表、弹窗和无障碍状态

tests/
├── test_system_practice_repository.py # 新增：repository 与并发/幂等契约
├── test_system_practice_migration.py  # 新增：旧数据迁移与覆盖率
├── test_system_learning_stats.py      # 新增：维度、统计、优先级
├── test_system_practice_review.py     # 业务/API 回归
└── test_system_library_frontend.py    # 前端交互契约

docs/superpowers/prototypes/
└── system-learning-loop-v4-sketch.html
```

## Stable Data Contracts

### Practice Attempt v2

```python
{
    "schema_version": 2,
    "attempt_id": "pa_xxx",
    "user_id": "tester",
    "practice_set_id": "ps_xxx",
    "review_task_id": "rt_xxx" | None,
    "status": "draft" | "submitted" | "abandoned",
    "client_attempt_token": "uuid",
    "submit_token": "uuid" | None,
    "save_revision": 3,
    "started_at": "ISO-8601",
    "last_saved_at": "ISO-8601",
    "submitted_at": "ISO-8601" | None,
    "abandoned_at": "ISO-8601" | None,
    "answer_count": 4,
    "answers": {},
    "summary": {},
    "source_meta": {},
}
```

`submitting`、`save_failed` 和 `submit_failed` 是前端请求状态，不作为稳定持久化状态。失败时后端 attempt 保持 `draft`，接口返回结构化错误；前端保留本地答案并允许重试。

### Grade Event v1

```python
{
    "schema_version": 1,
    "event_id": "ge_xxx",
    "user_id": "tester",
    "attempt_id": "pa_xxx",
    "question_id": "kaoyan_math1_2024_q011",
    "method": "local" | "ai" | "manual",
    "status": "correct" | "incorrect" | "partial" | "pending_review" | "failed",
    "confidence": 0.92,
    "reason": "",
    "feedback": "",
    "evidence": {},
    "request_id": "agr_xxx" | None,
    "supersedes_event_id": "ge_xxx" | None,
    "grading_version": "practice-grade-v2",
    "created_at": "ISO-8601",
}
```

`practice_attempt_items.final_status` 是事件流的当前投影。AI 请求失败只追加 `status=failed` 事件，不改变已有 `final_status`。

### Canonical Learning Dimension v1

```python
{
    "discipline": "math",
    "module": "calculus" | "linear_algebra" | "probability" | "unknown",
    "exam_scope": "math1" | "math2" | "math3" | "unknown",
    "topic": "导数应用",
    "raw_subject": "高数",
    "dimension_version": "learning-dimension-v1",
}
```

题目含多个知识点时，主知识点贡献权重为 `1.0`，其余知识点共享剩余贡献；第一版统一使用：

```python
topic_weight = 1.0 if topic_index == 0 else 1.0 / max(1, topic_count - 1)
```

统计记录必须保存 `score_version="learning-priority-v3"` 和各特征分量，页面只显示解释后的原因标签。

---

### Task 1: 先确认学习闭环 v4 静态草图

**Files:**
- Create: `docs/superpowers/prototypes/system-learning-loop-v4-sketch.html`
- Reference: `web/index.html`
- Reference: `web/styles.css`
- Reference: `E:/temp/product-audit-20260710-current-flow/01-review-overview.png`
- Reference: `E:/temp/product-audit-20260710-current-flow/02-topic-panel.png`
- Reference: `E:/temp/product-audit-20260710-current-flow/03-wrong-pool.png`

**Interfaces:**
- Consumes: 现有左侧四个一级入口、资料库视觉语言和本计划的数据状态。
- Produces: 六个可切换画面的单文件原型，以及用户确认后的布局基线。

- [ ] **Step 1: 创建沿用现有视觉系统的单文件原型**

原型必须可点击切换以下画面：系统题库与抽屉、生成练习、单题作答、提交结果、复习工作台、练习记录与二次处理中心。不能新造配色、字体或卡片圆角体系。

- [ ] **Step 2: 在复习工作台实现推荐布局**

使用 12 栏：顶部紧凑指标；左 8 栏为逾期/今日/未来任务；右 4 栏为 Top 3 薄弱知识点和下一步建议。完成/取消任务放归档切换，不与待办同屏展开。

- [ ] **Step 3: 在练习记录画面实现完整生命周期**

二级切换固定为 `未完成草稿 / 已提交练习 / 练习单`。每条草稿有“继续”和“放弃”，提交记录有“查看结果”和“再次练习”，练习单有“开始练习、加入规划、删除”。

- [ ] **Step 4: 使用 in-app browser 截图并执行 `product-design:audit`**

截图保存到 `E:/temp/system-learning-loop-v4-prototype-audit/`。检查 1268×911 和 390×844 两个视口，重点检查按钮可见性、题目/公式不截断、弹窗返回出口、焦点顺序和页面滚动归属。

- [ ] **Step 5: 用户确认草图后再进入 Task 2**

未确认时只修改原型，不修改 `web/` 和 `materials/`。

- [ ] **Step 6: 提交原型**

```bash
git add docs/superpowers/prototypes/system-learning-loop-v4-sketch.html
git commit -m "docs: 确认系统资料库学习闭环 v4 草图"
```

---

### Task 2: 建立 JSONL Repository 与原子写入边界

**Files:**
- Create: `materials/system_practice_repository.py`
- Create: `tests/test_system_practice_repository.py`
- Modify: `materials/system_practice_review.py`

**Interfaces:**
- Consumes: `resolve_user_id()`、`validate_safe_id()` 和当前用户目录结构。
- Produces: `PracticeAttemptRepository`、`GradeEventRepository`、`LearningStatsRepository`。

- [ ] **Step 1: 写 repository 失败测试**

```python
def test_attempt_repository_upsert_is_atomic_and_keeps_one_record_per_id():
    repo = PracticeAttemptRepository(users_root=temp_root)
    repo.upsert("tester", {"attempt_id": "pa_1", "status": "draft", "save_revision": 1})
    repo.upsert("tester", {"attempt_id": "pa_1", "status": "draft", "save_revision": 2})
    assert repo.get("tester", "pa_1")["save_revision"] == 2
    assert len(repo.list("tester")) == 1


def test_grade_event_repository_is_append_only_and_request_idempotent():
    repo = GradeEventRepository(users_root=temp_root)
    event = grade_event(event_id="ge_1", request_id="agr_1")
    first = repo.append("tester", event)
    second = repo.append("tester", event)
    assert first == second
    assert len(repo.list_for_item("tester", "pa_1", "q_1")) == 1
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_practice_repository -v`

Expected: FAIL，提示 repository 模块不存在。

- [ ] **Step 3: 实现固定接口**

| 类 | 方法 | 精确行为 |
|---|---|---|
| `PracticeAttemptRepository` | `get(user_id, attempt_id) -> dict` | 不存在时抛出 `KeyError`，返回记录副本 |
| `PracticeAttemptRepository` | `list(user_id, status=None) -> list[dict]` | 按 `started_at` 倒序，可按稳定状态筛选 |
| `PracticeAttemptRepository` | `upsert(user_id, attempt) -> dict` | 以 `attempt_id` 唯一覆盖并原子写入 |
| `GradeEventRepository` | `append(user_id, event) -> dict` | 只追加；相同 `request_id` 返回已有事件 |
| `GradeEventRepository` | `list_for_item(user_id, attempt_id, question_id) -> list[dict]` | 按 `created_at` 正序返回完整证据链 |
| `LearningStatsRepository` | `replace_question_stats(user_id, rows) -> None` | 原子替换单题统计文件 |
| `LearningStatsRepository` | `replace_topic_stats(user_id, rows) -> None` | 原子替换知识点统计文件 |

所有 replace/upsert 先写同目录临时文件，再用 `Path.replace()` 原子替换。类内部使用 `threading.RLock`，禁止业务层直接调用 `_write_records()` 写 attempt、grade event 和 stats。

- [ ] **Step 4: 将 `SystemPracticeReviewStore` 接到 repository**

构造函数注入 repository；默认创建 JSONL 实现。保留当前公开方法签名，使 API 与前端不受影响。

- [ ] **Step 5: 运行 repository 与现有回归测试**

Run: `python -m unittest tests.test_system_practice_repository tests.test_system_practice_review -v`

Expected: PASS。

- [ ] **Step 6: 提交 repository 边界**

```bash
git add materials/system_practice_repository.py materials/system_practice_review.py tests/test_system_practice_repository.py tests/test_system_practice_review.py
git commit -m "refactor: 建立练习记录存储边界"
```

---

### Task 3: 修复草稿保存与提交可靠性

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Modify: `web/app.js`
- Modify: `tests/test_system_practice_review.py`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: `PracticeAttemptRepository`。
- Produces: `create_or_resume_practice_attempt()`、带 revision 的答案保存、幂等提交和前端 dirty state。

- [ ] **Step 1: 写后端失败测试**

- `test_create_attempt_reuses_draft_for_same_client_token`：连续两次使用相同 token 创建，断言 `attempt_id` 相同且 repository 仅有一条 draft。
- `test_answer_save_rejects_stale_revision_without_overwriting_newer_answer`：先保存 revision 1，再用 revision 0 更新，断言抛出 `PracticeRevisionConflict` 且服务器答案不变。
- `test_submit_token_is_idempotent_and_stats_increment_once`：相同 submit token 提交两次，断言 attempt item 数和 `attempt_count` 都只增加一次。
- `test_failed_submit_keeps_attempt_draft_and_answers_editable`：注入 item 写入异常，断言 attempt 仍为 draft，答案完整，并可再次保存。

- [ ] **Step 2: 运行后端测试并确认失败**

Run: `python -m unittest tests.test_system_practice_review.SystemPracticeReviewTests -v`

Expected: 新增四项测试 FAIL。

- [ ] **Step 3: 扩展业务接口**

```text
create_or_resume_practice_attempt(
    user_id: str,
    practice_set_id: str,
    client_attempt_token: str,
    review_task_id: str | None = None,
) -> dict

update_practice_attempt_answers(
    user_id: str,
    attempt_id: str,
    answers: dict[str, object],
    expected_revision: int,
) -> dict

submit_practice_attempt(
    user_id: str,
    attempt_id: str,
    submit_token: str,
    expected_revision: int,
) -> dict
```

revision 冲突返回 HTTP 409，并返回服务器 revision。提交前答案保存失败时不得调用 submit。

- [ ] **Step 4: 写前端契约失败测试**

断言 `web/app.js` 包含：`localDirtyAnswers`、`saveRevision`、`save_failed`、`submit_failed`、`retryPracticeSave`，并且 submit 分支在 save 失败时提前返回。

- [ ] **Step 5: 实现前端保存状态机**

```text
idle → dirty → saving → saved
                 ↘ save_failed → retrying
saved → submitting → submitted
                   ↘ submit_failed → retrying
```

输入时只更新当前题局部 DOM 和本地答案，不重绘整张作答页面。顶栏显示“保存中 / 已保存 10:32 / 保存失败，重试”。

- [ ] **Step 6: 运行测试**

Run: `python -m unittest tests.test_system_practice_review tests.test_system_library_frontend -v`

Expected: PASS。

- [ ] **Step 7: 提交可靠作答链路**

```bash
git add materials/system_practice_review.py materials/system_practice_review_api.py web/app.js tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "fix: 保证练习草稿保存与提交可靠"
```

---

### Task 4: 迁移旧提交并显化数据覆盖率

**Files:**
- Create: `materials/system_practice_migration.py`
- Create: `scripts/migrate_system_learning_records.py`
- Create: `tests/test_system_practice_migration.py`
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`

**Interfaces:**
- Consumes: repository、旧 `practice_attempts.jsonl`、practice set 快照和当前本地判分器。
- Produces: `PracticeRecordMigrationService.audit_user()`、`migrate_user()`、`verify_user()` 和 insights coverage。

- [ ] **Step 1: 写迁移失败测试**

- `test_migration_backfills_items_for_submitted_attempt_without_duplicates`：准备一个 submitted attempt 和零条 item，执行迁移后断言 item 数等于练习单题数且 `(attempt_id, question_id)` 唯一。
- `test_migration_does_not_touch_draft_attempt_answers`：准备 draft，迁移前后深比较 answers、revision 和 status 完全一致。
- `test_migration_is_idempotent`：连续执行两次，第二次 `migrated_count=0`，全部 JSONL 记录数不变。
- `test_coverage_reports_submitted_total_and_item_complete_total`：准备两个 submitted、一个缺 item，断言迁移前 ratio 为 0.5、迁移后为 1.0。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_practice_migration -v`

Expected: FAIL。

- [ ] **Step 3: 实现迁移服务**

| 方法 | 返回值约束 |
|---|---|
| `audit_user(user_id) -> dict` | 返回 submitted、complete、missing、duplicate、coverage_ratio |
| `migrate_user(user_id, dry_run=True) -> dict` | dry-run 不写文件；execute 返回 migrated/skipped/failed 和 backup_path |
| `verify_user(user_id) -> dict` | 返回 coverage、重复键、孤立 item 和 stats 一致性 |

迁移只处理 `status=submitted` 且缺少 item 的 attempt；从 attempt 现有 `answers/results` 优先恢复，不重新调用 AI。执行前把相关 JSONL 复制到用户目录下 `migration_backups/{timestamp}/`。

- [ ] **Step 4: 实现 CLI**

```bash
python scripts/migrate_system_learning_records.py --user-id tester --dry-run
python scripts/migrate_system_learning_records.py --user-id tester --execute
python scripts/migrate_system_learning_records.py --user-id tester --verify
```

命令输出：已提交数、已有 item 数、待迁移数、迁移成功数、无法恢复数、统计重建结果。

- [ ] **Step 5: 在学习概览返回 coverage**

```python
"data_coverage": {
    "submitted_attempt_count": 25,
    "item_complete_attempt_count": 25,
    "coverage_ratio": 1.0,
    "migration_required": False,
}
```

coverage 小于 1 时页面显示“部分历史尚未纳入分析”，不再显示“全部练习记录摘要”。

- [ ] **Step 6: 运行迁移与回归测试**

Run: `python -m unittest tests.test_system_practice_migration tests.test_system_practice_review -v`

Expected: PASS。

- [ ] **Step 7: 提交迁移能力**

```bash
git add materials/system_practice_migration.py materials/system_practice_review.py materials/system_practice_review_api.py scripts/migrate_system_learning_records.py tests/test_system_practice_migration.py tests/test_system_practice_review.py
git commit -m "feat: 补齐历史练习记录迁移与覆盖率"
```

---

### Task 5: 建立可追溯判分事件与 AI 失败语义

**Files:**
- Modify: `materials/system_practice_ai_grader.py`
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Modify: `web/app.js`
- Modify: `tests/test_system_practice_review.py`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: `GradeEventRepository`。
- Produces: `request_practice_item_ai_grade(user_id, attempt_id, question_id, request_id)`、`record_manual_grade(user_id, attempt_id, question_id, final_status, reason)` 和 `grade_events` 响应。

- [ ] **Step 1: 写判分事件失败测试**

- `test_ai_failure_appends_failed_event_without_changing_final_status`：本地 incorrect 后注入 AI 异常，断言 final 仍为 incorrect，事件链新增一条 failed。
- `test_duplicate_ai_request_id_returns_existing_event`：相同 request id 请求两次，断言 AI 客户端只调用一次且事件 id 相同。
- `test_manual_grade_preserves_local_and_ai_events`：local incorrect、AI incorrect、manual correct 后，断言三条事件均存在，投影为 manual correct，并标记两项冲突来源。
- `test_attempt_detail_returns_ordered_grade_events_for_each_item`：断言 API 按 created_at 正序返回证据链且不返回其他用户事件。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_practice_review -v`

Expected: 新增测试 FAIL。

- [ ] **Step 3: 修改 AI grader 错误契约**

`system_practice_ai_grader.py` 不再把异常转换成 `pending_review`。改为抛出 `PracticeAIGradeError(request_id, message, retryable)`；业务层捕获后追加 failed event，并返回原 item 投影。

- [ ] **Step 4: 修改业务层投影规则**

```python
def project_final_grade(events: list[dict], fallback_status: str) -> dict:
    successful = [event for event in events if event["status"] != "failed"]
    latest = successful[-1] if successful else None
    return {
        "final_status": latest["status"] if latest else fallback_status,
        "judge_method": latest["method"] if latest else "local",
        "latest_grade_event_id": latest["event_id"] if latest else None,
    }
```

manual 是用户最终决定，但页面保留冲突提示；统计同时保存 `manual_conflict_count`，不删除 AI/local 证据。

- [ ] **Step 5: 完善结果页判分状态**

按钮依次显示：`AI 判分 → 正在评分 → 已完成`；失败显示 `评分失败，重试`。更新局部题目行并保持 modal 的 `scrollTop`。每题“判分依据”折叠区按时间展示 local、AI、manual 事件。

- [ ] **Step 6: 运行测试**

Run: `python -m unittest tests.test_system_practice_review tests.test_system_library_frontend -v`

Expected: PASS。

- [ ] **Step 7: 提交判分事件链**

```bash
git add materials/system_practice_ai_grader.py materials/system_practice_review.py materials/system_practice_review_api.py web/app.js tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "feat: 增加可追溯判分事件与失败重试"
```

---

### Task 6: 统一学习维度、统计口径与优先级版本

**Files:**
- Create: `materials/system_learning_stats.py`
- Create: `tests/test_system_learning_stats.py`
- Modify: `materials/system_practice_review.py`
- Modify: `tests/test_system_practice_review.py`

**Interfaces:**
- Consumes: attempt item、question state、review task。
- Produces: `canonical_learning_dimension()`、`build_question_stats()`、`build_topic_stats()`、`score_learning_priority()`。

- [ ] **Step 1: 写维度和统计失败测试**

- `test_gaoshu_and_unknown_derivative_application_merge_into_math_calculus_topic`：两种原始 subject 输入生成相同 canonical stat id。
- `test_math1_math2_math3_remain_distinct_exam_scopes`：同一知识点的三种考试范围生成三个可筛选统计分组。
- `test_multi_topic_question_does_not_add_full_error_to_every_topic`：三知识点题的总贡献不超过 2.0，主知识点贡献为 1.0。
- `test_wrong_action_uses_unique_question_count_not_wrong_attempt_count`：同题错三次，指标显示错误 3 次，动作显示复习 1 道错题。
- `test_priority_result_exposes_score_version_and_feature_breakdown`：断言返回固定版本、八项特征和非空 reason code。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_learning_stats -v`

Expected: FAIL。

- [ ] **Step 3: 实现规范化函数**

```text
canonical_learning_dimension(source_meta: dict, topic: str) -> dict
topic_contribution_weights(topics: list[str]) -> dict[str, float]
score_learning_priority(features: dict) -> dict
```

`raw_subject` 仅用于追溯，不参与 stat id。topic stat id 固定为：

```python
f"{discipline}::{module}::{exam_scope}::{normalized_topic}"
```

- [ ] **Step 4: 固化优先级输出**

```python
{
    "score": 0.7821,
    "score_version": "learning-priority-v3",
    "features": {
        "risk_conf": 0.64,
        "recent": 0.73,
        "streak": 0.40,
        "pending": 0.00,
        "skip": 0.20,
        "unstarted": 0.00,
        "manual": 0.10,
        "important": 0.30,
    },
    "reason_codes": ["repeated_wrong", "recent_wrong"],
}
```

学习概览同时返回 `wrong_attempt_count` 和 `unique_wrong_question_count`。动作标签只使用唯一题数：`复习 16 道错题`。

- [ ] **Step 5: 运行统计回归**

Run: `python -m unittest tests.test_system_learning_stats tests.test_system_practice_review -v`

Expected: PASS。

- [ ] **Step 6: 提交统计口径**

```bash
git add materials/system_learning_stats.py materials/system_practice_review.py tests/test_system_learning_stats.py tests/test_system_practice_review.py
git commit -m "fix: 统一学习统计维度与错题口径"
```

---

### Task 7: 增加练习记录与草稿生命周期页面

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_practice_review.py`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: attempt v2 和 practice set API。
- Produces: 可分页 `GET /practice-attempts`、`POST /practice-attempts/{id}/abandon`、复习页二级“练习记录”。

- [ ] **Step 1: 写 API 失败测试**

覆盖：按 status 分页、草稿继续、草稿放弃、已提交结果读取、只允许本人操作、27 个以上记录分页不丢失。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_practice_review -v`

Expected: 新增测试 FAIL。

- [ ] **Step 3: 实现分页与放弃接口**

```text
GET  /api/materials/system/practice-attempts?status=draft&page=1&page_size=20
POST /api/materials/system/practice-attempts/{attempt_id}/abandon
POST /api/materials/system/practice-attempts/{attempt_id}/resume
```

返回 `items/page/page_size/total/total_pages`。abandon 写 `status=abandoned` 和 `abandoned_at`，不删除答案；resume 仅允许 abandoned 恢复成 draft。

- [ ] **Step 4: 写前端契约失败测试**

断言练习记录存在 `draft/submitted/practice_sets` 三个分段视图，并包含 `继续练习、放弃草稿、查看结果、再次练习` 的入口和空/加载/错误态。

- [ ] **Step 5: 实现练习记录页面**

复习规划页顶部增加二级切换 `复习工作台 / 练习记录`。一级侧栏仍只有问答、资料库、复习规划、院校查询。列表每页 20 条，状态筛选不一次加载全部历史。

- [ ] **Step 6: 运行测试**

Run: `python -m unittest tests.test_system_practice_review tests.test_system_library_frontend -v`

Expected: PASS。

- [ ] **Step 7: 提交练习记录页**

```bash
git add materials/system_practice_review.py materials/system_practice_review_api.py web/index.html web/app.js web/styles.css tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "feat: 增加练习记录与草稿恢复页面"
```

---

### Task 8: 打通结果页、二次处理池和复习任务

**Files:**
- Modify: `materials/system_practice_review.py`
- Modify: `materials/system_practice_review_api.py`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_practice_review.py`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: attempt item、wrong pool、pending pool、review task。
- Produces: 基于真实 question id 的错题练习、待核对记录处理、attempt 与 review task 联动。

- [ ] **Step 1: 写业务失败测试**

- `test_result_wrong_action_creates_set_from_unique_wrong_questions`：同题多次错误只进入练习单一次，顺序按当前优先级分数稳定排序。
- `test_pending_pool_groups_records_by_question_and_exposes_record_count`：两条同题待核对记录聚合为一行，同时返回 `unresolved_record_count=2`。
- `test_resolving_latest_pending_record_does_not_hide_older_unresolved_record`：只解决最新记录后，列表仍返回同题且 count 从 2 变为 1。
- `test_attempt_from_review_task_updates_task_after_submit`：携带 task id 创建并提交 attempt，确认完成后 task 变 completed 并记录 completed_attempt_id。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_practice_review -v`

Expected: FAIL。

- [ ] **Step 3: 明确二次处理接口**

```text
POST /practice-sets/from-attempt-errors
GET  /pending-review-items?group_by=question
POST /pending-review-items/{attempt_id}/{question_id}/resolve
POST /review-tasks/{task_id}/complete-from-attempt
```

待核对项显示“该题有 N 条未解决记录”，用户可选择只解决当前记录或按相同答案范围批量解决，不静默隐藏旧记录。

- [ ] **Step 4: 修改结果页动作语义**

`复习 N 道错题` 打开错题选择池并默认勾选本次错误；`确认 N 道待核对题` 打开待核对名单；`优先复习 X` 打开知识点处理面板。任何只定位本页的动作改名为 `定位本次错题`。

- [ ] **Step 5: 联动复习任务**

从复习任务打开练习单时把 `review_task_id` 传入 attempt。提交后若题目全部作答，弹出“完成本次复习任务 / 暂不完成”；用户确认后任务变为 completed。系统不得无提示自动删除任务。

- [ ] **Step 6: 运行测试**

Run: `python -m unittest tests.test_system_practice_review tests.test_system_library_frontend -v`

Expected: PASS。

- [ ] **Step 7: 提交闭环动作**

```bash
git add materials/system_practice_review.py materials/system_practice_review_api.py web/app.js web/styles.css tests/test_system_practice_review.py tests/test_system_library_frontend.py
git commit -m "feat: 打通练习结果与复习任务闭环"
```

---

### Task 9: 落地复习工作台和弹窗布局

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_system_library_frontend.py`

**Interfaces:**
- Consumes: 已确认的 v4 静态草图和真实 API 数据。
- Produces: 复习工作台、知识点面板、错题池、待核对池和结果页的稳定响应式布局。

- [ ] **Step 1: 写布局契约失败测试**

断言：Top 3 洞察、`查看全部`、归档切换、sticky selection footer、零数量禁用态、结果筛选 chip、modal focus restore 标记均存在。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_system_library_frontend -v`

Expected: FAIL。

- [ ] **Step 3: 重排复习工作台**

桌面为 8/4 两列；移动端为任务在前、洞察在后。Top 3 知识点信息卡保持可点击但视觉上不是普通按钮；重复知识点在后端已合并后只显示一次。

- [ ] **Step 4: 优化知识点和二次处理弹窗**

知识点面板使用 `知识内容 / 我的表现 / 相关题目` 分段视图；数量为 0 的动作禁用。错题池使用紧凑列表、统一 Markdown/KaTeX renderer 和底部固定“已选 N 题 / 生成练习单”。

- [ ] **Step 5: 优化结果和任务动作**

结果页顶部增加 `全部/错误/待核对/正确` 筛选；判分证据折叠。pending 任务显示开始/完成/推迟/取消/删除；completed/cancelled 只显示打开来源/恢复/删除。

- [ ] **Step 6: 补 modal 无障碍行为**

`createSystemWorkflowOverlay()` 打开后聚焦首个可操作控件，Tab 被限制在 modal 内；关闭后恢复到触发按钮。Esc 和遮罩关闭保持现有行为。

- [ ] **Step 7: 运行前端契约测试和语法检查**

Run: `python -m unittest tests.test_system_library_frontend -v`

Expected: PASS。

Run: `node --check web/app.js`

Expected: exit 0。

- [ ] **Step 8: 提交布局优化**

```bash
git add web/index.html web/app.js web/styles.css tests/test_system_library_frontend.py
git commit -m "feat: 优化复习工作台与二次处理布局"
```

---

### Task 10: 全链路验证、产品审计和发布留痕

**Files:**
- Create: `docs/superpowers/audits/2026-07-10-system-learning-loop-v4-audit.md`
- Modify: `docs/superpowers/plans/2026-07-10-system-learning-loop-v4.md`

**Interfaces:**
- Consumes: Tasks 1-9 的实现。
- Produces: 可复现测试证据、浏览器截图、残余风险和发布提交。

- [ ] **Step 1: 运行完整代码验证**

Run: `python -m compileall materials scripts tests`

Expected: exit 0。

Run: `python -m unittest tests.test_formula_cleaner tests.test_formula_extractor tests.test_llm_cleaner tests.test_qwen_formula_client tests.test_materials_mvp tests.test_agent_runtime tests.test_system_practice_repository tests.test_system_practice_migration tests.test_system_learning_stats tests.test_system_practice_review tests.test_system_library tests.test_system_library_frontend`

Expected: PASS，允许现有明确标注的 1 项 skip。

Run: `node --check web/app.js`

Expected: exit 0。

- [ ] **Step 2: 运行用户级迁移演练**

Run: `python scripts/migrate_system_learning_records.py --user-id tester --dry-run`

Expected: 无写入，报告待迁移数量。

Run: `python scripts/migrate_system_learning_records.py --user-id tester --execute`

Expected: 迁移完成且生成备份。

Run: `python scripts/migrate_system_learning_records.py --user-id tester --verify`

Expected: submitted attempt 覆盖率 100%，无重复 attempt item。

- [ ] **Step 3: 使用 in-app browser 跑真实主链路**

```text
系统资料 → 生成同类训练 → 开始练习 → 保存草稿 → 刷新恢复
→ 提交 → 本地判分 → AI 判分成功/失败 → 人工确认
→ 生成错题练习单 → 加入复习规划 → 从任务开始练习 → 完成任务
→ 练习记录查看历史结果
```

截图保存到 `E:/temp/system-learning-loop-v4-final-audit/`，不得提交截图到仓库。

- [ ] **Step 4: 使用 `product-design:audit` 审计页面和流程**

审计必须覆盖桌面和移动端：页面层级、卡片信息密度、按钮可见性、空/加载/错误态、返回出口、滚动区域、公式与图片、键盘焦点、结果到下一步动作的闭环。

- [ ] **Step 5: 写审计文档**

文档列出每步健康度、修复证据、未解决风险和下一阶段边界。AI 自动规划仍不进入本计划实现，只记录为数据稳定后的独立项目。

- [ ] **Step 6: 最终提交**

```bash
git add docs/superpowers/audits/2026-07-10-system-learning-loop-v4-audit.md docs/superpowers/plans/2026-07-10-system-learning-loop-v4.md
git commit -m "docs: 完成系统资料库学习闭环 v4 审计"
```

---

## Success Criteria

1. 用户最新答案保存失败时不能提交旧答案，失败后可在原位置重试。
2. 同一 `client_attempt_token` 不重复创建草稿，同一 `submit_token` 不重复累计统计。
3. 所有已提交 attempt 都有可查询的 attempt item，学习概览公开数据覆盖率。
4. AI 判分失败不覆盖本地/人工最终结果，所有 local/AI/manual 判定均可追溯。
5. `导数应用` 等知识点不因 `高数/unknown/math` 重复，数一/数二/数三仍可独立筛选。
6. 错误次数与唯一错题数分开显示，动作使用唯一题数。
7. 草稿、已提交练习和练习单均有稳定入口、分页、反向操作和返回出口。
8. 结果页按钮真实进入错题池、待核对池、知识点处理或复习任务，不再只做无提示定位。
9. 从复习任务开始的练习可在提交后完成该任务，状态变化可恢复和追溯。
10. 桌面与移动端页面没有透明按钮、题干截断、公式原始标记、不可达操作或 modal 焦点逃逸。

## Self-Review

- Spec coverage: 数据可靠性、旧记录迁移、判分事件、统计维度、练习历史、二次处理、复习任务联动、布局和审计均有独立任务。
- Placeholder scan: 每项均给出文件、接口、测试命令、精确断言和验收结果，没有未定义实现项。
- Type consistency: attempt v2、grade event v1、canonical dimension v1、score version 和任务接口在各任务中保持一致。
- Scope boundary: 不修改 `qa/`、不移动 `data/raw/`、不引入 MySQL、不实现 AI 自动规划。
- Risk control: 先完成数据与迁移，再改页面；UI 修改受已确认静态草图约束。
