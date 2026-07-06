# 练习记录数据层 v1 设计

## 背景

系统资料库已经有练习单、练习作答、提交结果、本地判分和 AI 判分入口。当前提交记录保存在用户目录下的 JSONL 文件中，但数据仍偏向“整张练习单结果”，还不足以支撑后续的学习画像、薄弱知识点统计和 AI 复习规划。

本设计的目标是先把本地 JSONL 数据层整理成接近数据库表的结构。第一版不直接引入 MySQL 或 SQLite，避免在产品结构仍快速变化时增加迁移和调试成本。接口和数据模型按数据库思路设计，后续可以平滑迁移。

## 目标

1. 每次练习提交都能沉淀为可查询的历史记录。
2. 每道题的作答、判分、AI 修正和最终结果可独立查询。
3. 能按用户和题目聚合出单题统计。
4. 能按用户和知识点聚合出知识点统计。
5. 结果页、复习规划和后续 AI 学习规划使用同一套真实记录。
6. 数据量变大后，查询和 AI 规划仍然读取聚合摘要，而不是反复扫描全量历史。

## 非目标

1. 不在本阶段接入 MySQL、SQLite 或其他数据库。
2. 不做真实多用户权限系统。
3. 不重构系统题库公共内容。
4. 不让 AI 直接读取全部原始历史记录生成规划。
5. 不把解答题评分做成完全自动可信结论，第一版保留人工修正空间。

## 数据量增长设计

第一版虽然继续使用本地 JSONL，但模型必须按“大量历史记录”设计。核心原则是三层分离：

```text
原始明细层：保存每次作答和每题判分，保证可追溯。
聚合统计层：保存用户-题目、用户-知识点的当前统计，保证快速查询。
AI 摘要层：只给 AI 提供后端整理过的近期表现、薄弱点和代表样例。
```

### 分层存储

小数据阶段：

```text
data/users/{user_id}/system_library/
├── practice_attempts.jsonl
├── practice_attempt_items.jsonl
├── user_question_stats.jsonl
└── user_topic_stats.jsonl
```

中等数据阶段：

```text
data/users/{user_id}/system_library/
├── attempts/2026-07.jsonl
├── attempt_items/2026-07.jsonl
├── stats/question_stats.jsonl
├── stats/topic_stats.jsonl
└── indexes/
    ├── question_attempt_index.json
    ├── topic_attempt_index.json
    └── latest_attempt_index.json
```

数据库阶段：

```text
practice_attempts
practice_attempt_items
user_question_stats
user_topic_stats
learning_profile_snapshots
```

代码层只依赖 repository 接口，不依赖 JSONL 文件路径。这样后续迁移 SQLite 或 MySQL 时，不改前端和判分业务。

### 查询策略

随着记录变多，禁止常规页面每次扫描全部 `practice_attempt_items`。

常用查询必须走聚合表或索引：

```text
查看一道题历史：user_question_stats + question_attempt_index
查看知识点表现：user_topic_stats
生成 AI 规划：learning_profile_snapshots 或实时聚合摘要
结果页回看：attempt_id 精确读取
复习规划候选：stats 中的 repeated_wrong / weakness_level / latest_practiced_at
```

原始明细只用于：

```text
打开某一次练习结果
追溯某道题某次判分
重建统计
抽取少量代表样例给 AI
```

### 增量聚合

提交练习和 AI 判分后，同步更新当前统计：

```text
practice_attempt_items 追加或更新
-> user_question_stats 增量更新
-> user_topic_stats 增量更新
-> attempt summary 重新汇总
```

同时提供重建能力：

```text
rebuild_user_learning_stats(user_id)
```

重建逻辑从明细层重新计算统计，用于修复旧数据、算法升级或统计文件损坏。增量更新必须是幂等的：同一个 `attempt_id + question_id` 重新处理时，不应重复增加练习次数。

### 准确性策略

统计只以 `final_status` 为准，但必须保留判分来源：

```text
local_status
ai_status
manual_override
final_status
judge_method
judge_confidence
grading_version
graded_at
```

当 AI 或人工修正结果时，要重新计算该题、该知识点和该 attempt 的统计。不能只改页面展示。

低置信度或待核对结果不应被当成“确定错误”：

```text
correct: 计入正确
incorrect: 计入错误
partial: 单独统计，AI 规划时作为薄弱信号
pending_review / pending_grading: 单独统计，不直接拉低准确率
unanswered: 计入未作答，不计入正确率分母或单独展示
```

### AI 摘要策略

AI 学习规划不读取全部历史流水。后端先生成摘要：

```text
最近 N 次练习表现
错误率最高的知识点
反复错的题
收藏但未掌握的题
近期改善或退步趋势
待核对和低置信度判分数量
每个薄弱点最多附带 2-3 个代表题
```

AI 输入应包含统计摘要和少量代表样例，而不是几百条原始作答记录。这样更省 token，也更准确。

### 数据保留与压缩

默认保留所有明细记录，但页面不直接扫全量明细。数据很大时可以做冷热分层：

```text
近 90 天：明细直接可查
更早历史：保留明细文件，但主要走统计摘要
长期分析：使用月度 snapshot 或 learning_profile_snapshots
```

任何压缩或归档都不能删除用户可见的练习结果；至少应保留 attempt_id、题目、用户答案、最终判分和提交时间。

## 数据模型

### practice_attempts

表示一次练习会话或一次练习单提交。

字段：

```text
attempt_id
user_id
practice_set_id
schema_version
status: draft / submitted / abandoned
started_at
submitted_at
duration_seconds
total_count
answered_count
correct_count
incorrect_count
partial_count
pending_review_count
pending_grading_count
summary
source_meta
```

当前已有 `practice_attempts.jsonl`，第一版继续保留，但需要让它成为 attempt 级别的主记录，而不是所有逐题细节的唯一来源。

### practice_attempt_items

表示一次练习中的一道题作答记录。第一版可以落在独立 JSONL 文件，也可以由 repository 从 attempt 中派生后再逐步拆分；对业务层暴露为独立 item 接口。

字段：

```text
attempt_id
user_id
practice_set_id
question_id
schema_version
question_type
answer_type: choice / blank / solution
topics
user_answer
standard_answer
local_status: correct / incorrect / partial / pending_review / pending_grading / unanswered
ai_status
final_status
judge_method: local / ai / manual
judge_confidence
judge_reason
ai_feedback
manual_override
grading_version
submitted_at
graded_at
```

`final_status` 是页面最终展示和统计使用的结果。`local_status` 与 `ai_status` 都保留，方便追溯“本地判错但 AI 修正为正确”的情况。

### user_question_stats

表示某个用户对某道题的累计状态。

字段：

```text
user_id
question_id
stats_version
practice_count
answered_count
correct_count
incorrect_count
partial_count
pending_review_count
latest_attempt_id
latest_practice_set_id
latest_answer
latest_final_status
latest_judge_method
latest_practiced_at
first_practiced_at
wrong_streak
correct_streak
is_repeated_wrong
updated_at
source_attempt_ids_recent
```

该表不替代 `question_states.jsonl`。`question_states` 继续负责收藏、错题、掌握、备注等用户主动状态；`user_question_stats` 负责练习行为统计。

### user_topic_stats

表示某个用户在某个知识点上的累计练习表现。

字段：

```text
user_id
subject
topic
stats_version
practice_count
question_count
correct_count
incorrect_count
partial_count
pending_count
accuracy
latest_practiced_at
weakness_level: none / light / medium / heavy
trend: unknown / improving / stable / declining
updated_at
representative_question_ids
```

一个题可以有多个知识点。提交后每个相关知识点都更新一次统计。

## 判分规则

### 选择题

选择题本地精确判分。提交后直接显示正确或错误，不显示 AI 判分按钮。

### 填空题

提交后先使用标准答案做本地归一化判分，显示正确或错误。如果用户认为等价表达被误判，点击 AI 判分。AI 判分后如果改为正确，`ai_status` 和 `final_status` 更新为正确，结果页显示正确。

### 解答题

提交后默认待评分，显示参考答案和解析。用户点击 AI 判分后写入 `ai_status`、`judge_confidence`、`judge_reason` 和 `ai_feedback`。后续保留手动修正入口，用户可把 AI 结果改为最终状态。

## 数据流

### 创建练习单

```text
生成同类训练
-> create_practice_set
-> 写入 practice_sets.jsonl
-> 返回练习单详情
```

### 开始练习

```text
打开练习单
-> create_practice_attempt
-> 写入 practice_attempts.jsonl，status=draft
-> 前端进入作答页
```

### 保存草稿答案

```text
用户选择或输入答案
-> update_practice_attempt_answers
-> 更新 attempt.answers
```

### 提交练习

```text
submit_practice_attempt
-> 校验 attempt 属于当前用户且 status=draft
-> 逐题生成 practice_attempt_items
-> 本地判分
-> 汇总 attempt summary
-> 写入 practice_attempts
-> 写入或更新 practice_attempt_items
-> 更新 user_question_stats
-> 更新 user_topic_stats
-> 返回完整 attempt + items + stats 摘要
```

### AI 判分

```text
grade_practice_attempt_item
-> 读取 attempt item
-> 构造题目、标准答案、用户答案、已有本地判分上下文
-> 调用 AI 判分
-> 写入 item.ai_status 和 item.final_status
-> 重新汇总 attempt summary
-> 更新 user_question_stats
-> 更新 user_topic_stats
-> 返回更新后的 attempt
```

## API 设计

保留现有接口，逐步增强返回值。

```text
POST /api/materials/system/practice-sets/{practice_set_id}/attempts
PATCH /api/materials/system/practice-attempts/{attempt_id}/answers
POST /api/materials/system/practice-attempts/{attempt_id}/submit
POST /api/materials/system/practice-attempts/{attempt_id}/items/{question_id}/grade
GET  /api/materials/system/practice-attempts
GET  /api/materials/system/practice-attempts/{attempt_id}
GET  /api/materials/system/questions/{question_id}/practice-history
GET  /api/materials/system/user-topic-stats
```

第一版优先实现内部 repository 能力。新增 GET 接口可以在结果页回看和 AI 画像阶段逐步开放。

## Repository 边界

新增或重构为以下边界：

```text
SystemPracticeReviewStore
  负责练习单、练习 attempt、复习任务的外部业务入口。

PracticeAttemptRepository
  负责 attempt 和 attempt item 的读写。

UserLearningStatsRepository
  负责 user_question_stats 和 user_topic_stats 的读写。

PracticeGradingService
  负责本地判分、AI 判分结果合并、summary 重新计算。
```

第一版可以在现有 `materials/system_practice_review.py` 内部逐步拆出私有方法；当文件继续膨胀时，再拆成独立模块。

## 前端影响

第一阶段前端只做最小改动：

1. 结果页继续使用当前结构。
2. 结果数据改为后端返回的真实 attempt/item。
3. AI 判分后保持当前滚动位置。
4. 后续结果页可以展示“这题第几次练习”“上次结果”“相关知识点表现”。

## 错误处理

1. attempt 不属于当前用户时返回 404。
2. submitted attempt 不允许再次修改答案。
3. AI 判分失败时不覆盖本地判分和最终结果。
4. 统计更新失败时不应导致提交记录丢失；记录错误并允许重建统计。
5. 旧 attempt 缺少新字段时读取时做 backfill。

## 测试计划

1. 创建练习单、开始练习、保存答案、提交后生成 attempt 和 item。
2. 选择题提交后本地判为正确或错误。
3. 填空题本地判错后，AI 判分可修正 final_status。
4. 解答题提交后为待评分，AI 判分后更新结果。
5. 提交后更新 user_question_stats。
6. 提交后更新 user_topic_stats。
7. 已提交 attempt 不可修改答案。
8. 旧数据读取时能 backfill。
9. 统计可从 attempt items 重建。

## 迁移策略

现有 `practice_attempts.jsonl` 继续可读。新增 item 和 stats 后，读取旧 attempt 时生成兼容结构。需要时提供脚本从历史 attempts 重建：

```text
practice_attempt_items.jsonl
user_question_stats.jsonl
user_topic_stats.jsonl
```

该脚本只读取用户目录，不修改系统题库公共内容。

## 实施顺序

1. 加 repository 和数据模型辅助函数。
2. 提交练习时生成 attempt item。
3. 增加单题统计更新。
4. 增加知识点统计更新。
5. AI 判分后重算 item、attempt summary 和统计。
6. 增加历史读取和重建统计测试。
7. 前端结果页逐步展示统计摘要。

## 成功标准

1. 提交练习后，能按 attempt 查询整次练习。
2. 提交练习后，能按 question_id 查询用户历史作答。
3. 提交练习后，能按 topic 查询知识点统计。
4. AI 判分修正后，最终结果和统计同步更新。
5. 旧 JSONL 记录不丢失，仍能被读取。
6. 不影响系统题库公共数据，不改 `data/raw` 结构。
