# AGENTS.md

> 项目：考研 Agent 助手
> 当前阶段：`materials` 纵向链路稳定 + 系统资料库产品设计阶段
> 默认测试用户：`tester`
> 当前优先任务：继续稳住 `.md/.txt` 的 parse → formula clean → clean → quality report → chunk → index/search 链路；并行设计“资料库 → 我的资料 / 系统资料”的系统资料库体验

---

## 0. 当前判断

项目顶层结构方向正确，不需要推翻：

```text
qa/          问答、路由、追问、学科逻辑
materials/   用户资料库、解析、清洗、切块、检索
scripts/     CLI / 启动 / 调试入口
web/         前端页面
skills/      模块开发规范
```

本阶段不再重构 `qa/`，不横向扩展文件格式。前端允许围绕“资料库”入口做小范围产品设计和页面迭代，但不要重写整体前端架构。已有 PDF/MinerU/向量索引相关代码可做必要维护，但不要在本阶段顺手扩写；当前重点仍是完善 `materials/` 内部边界，先做好 `.md/.txt` 纵向主链路，同时把系统资料库的产品边界设计清楚。

---

## 1. 当前目标

本轮目标不是横向扩展文件格式，而是让 `.md/.txt` 这一条链路更标准：

```text
上传 .md/.txt
↓
保存 original/
↓
parser 读取并输出 raw markdown
↓
formula_cleaner 做本地公式渲染修复
↓
postprocess 清洗、整理、规范化
↓
输出 parsed/content.md
↓
quality 生成 parsed/parse_report.json
↓
chunking 按标题/段落/长度切块
↓
indexing 建关键词索引
↓
search 可检索
```

完成后再系统考虑数据库、向量库、PDF、DOCX 等横向扩展。系统资料库可以先基于现有本地题卡和 JSONL 做只读浏览、筛选和搜索，不要为了第一版引入大型数据库重构。

---

## 2. materials 模块边界

`materials/` 应按流水线阶段组织，不按文件类型大拆。

推荐结构：

```text
materials/
├── schemas.py
├── security.py
├── storage.py
├── detector.py
├── resolver.py
├── router.py
├── service.py
├── api.py
├── tools.py
│
├── parsers/        # 不同格式 → raw markdown
├── postprocess/    # raw markdown → clean markdown
├── quality/        # clean markdown + chunks → parse_report
├── chunking/       # clean markdown → chunks
├── indexing/       # chunks → keyword index
├── embeddings/     # 可选：chunks → embeddings
├── repositories/   # 后续：SQLite/PostgreSQL 读写
├── vectorstores/   # 可选：Chroma/Qdrant/FAISS
└── search/         # keyword/vector/hybrid search
```

当前优先保证 `.md/.txt` 纵向流程稳定；`embeddings/`、`vectorstores/` 已有能力不要反向污染基础入库链路，`repositories/` 暂不强制实现。

---

## 3. 职责划分

### 3.1 parser

parser 负责“读懂原文件并输出基础 Markdown”。

`.md`：

```text
读取 Markdown
统一编码/换行
提取 front matter、标题数、图片引用数、source_dir
输出 parsed/content.md
```

`.txt`：

```text
读取 txt
统一编码/换行
文件名作为一级标题
疑似标题行转 Markdown 标题
输出 parsed/content.md
```

parser 不负责大量清洗、不负责切块、不负责向量库、不负责数据库。

### 3.2 postprocess

postprocess 负责“把 raw markdown 整理成标准 Markdown”。

```text
markdown_cleaner.py       基础清洗
structure_normalizer.py   标题层级、Setext 标题、缺空格标题、兜底根标题
asset_rewriter.py         图片路径复制与改写
formula_cleaner.py        本地公式渲染修复
formula_extractor.py      完整公式边界抽取与完整性校验
llm_cleaner.py            可选 LLM 精修补丁层
```

`formula_cleaner.py` 当前职责是“本地公式渲染修复”，不是数学语义改写：

```text
默认启用 use_formula_cleanup = true
默认等级 formula_cleanup_level = safe

safe 规则：
- \textcircled { 1-20 } / 中文数字 → Unicode 圈号，解决 Obsidian/MathJax 渲染问题
- \operatorname* { l i m } → \lim，\operatorname* { m a x } → \max
- 其他 \operatorname { s g n } 这类拆字母参数 → \operatorname{sgn}
- \operatorname* { m } 这类单字符参数只清理空格，不猜成 max/min
- \mathrm { s i n } / \mathrm { c o s } / \mathrm { l n } → \sin / \cos / \ln
- \sp { ... } → ^{...}
- \displaylimits → \limits
- \textmu → \mu
- \lim 下标中 x/n/t \infty → x/n/t \to \infty
- \lim 下标中 x/n/t \right. \infty → x/n/t \to \infty
- \Big \int → \int
- \textbf{\em a} → \boldsymbol{a}；单字符 \em a → \mathit{a}
- 简单 \frac{0} { 0 } → \frac{0}{0}
- \operatorname{e} / \operatorname{d} → \mathrm{e} / \mathrm{d}
- \mathrm{ { e } }、\mathbf{ { x } } 这类单 token 双层括号 → \mathrm{e}、\mathbf{x}
- 常见命令参数边界空格清理，如 \mathbf { x } → \mathbf{x}

report-only：
- \operatorname* { m }、\operatorname* { \cdot } 这类疑似 OCR 残缺 operator
- \atop
- \kern -
- 非 \lim 下标场景的 \right. \infty
- { \begin{array}... } 外层分组候选
```

公式清洗必须跳过 code fence、inline code、Markdown 表格行和图片行。清洗统计写入：

```text
manifest.metadata["formula_cleaning"]
parse_report.metrics["formula_cleaning"]
parsed/pipeline_events.jsonl 的 formula_clean 阶段
```

`llm_cleaner.py` 位于清洗层末端，但默认关闭：

```text
默认 use_llm_formula_cleanup = false
默认 llm_formula_min_confidence = 0.8

职责：
- 先让本地规则清洗确定性问题，再用 KaTeX 批量扫描剩余完整公式候选；
- 只接收本地抽取器确认完整边界、且 KaTeX/渲染器实际失败的 render_error 公式；不再只限于 \kern - delimiterspace；
- 给 LLM 的 payload 必须包含完整公式、原始 Markdown 行、heading_path、前后文和抽取置信度；
- LLM 不输出整篇 Markdown，也不输出单公式 replacement 补丁；
- 主路径使用 direct variants：让 LLM 一次给出 3 个纯 LaTeX 候选；
- 本地代码逐个 KaTeX 校验候选，并选择置信度达标且可渲染的最高置信候选替换；
- 视觉问题（如 \atop、array 外层分组、operatorname 可疑但可渲染）不送 LLM；
- direct variants 候选、选择结果、拒绝原因和 KaTeX 校验结果必须写入报告，方便人工追溯；
- 边界不确定、匹配不唯一、渲染验证失败时只写报告，不应用补丁。
```

LLM 精修统计写入：

```text
parsed/llm_cleaning_report.json
manifest.metadata["llm_cleaning"]
parse_report.metrics["llm_cleaning"]
parsed/pipeline_events.jsonl 的 llm_clean 阶段
```

### 3.3 quality

quality 负责“判断解析和整理质量”。输出：

```text
parsed/parse_report.json
```

并写入 manifest：

```text
quality_status
overall_confidence
warnings
metadata.formula_cleaning
metadata.llm_cleaning
```

### 3.4 chunking

chunking 负责“把 clean markdown 切成可检索片段”。规则：

```text
标题优先
段落兜底
长度硬切兜底
图片/公式/表格尽量不拆散
chunk metadata 保留 heading_path、subject、material_type、original_filename
```

---

## 4. LLM 清洗策略

LLM 有两类用途，必须分清边界：

```text
use_llm_cleanup:
  生成结构策略、文档分区和元数据画像，不接管全文改写。

use_llm_formula_cleanup:
  清洗层末端的残余公式渲染错误精修，默认关闭，只走 direct variants 候选和本地验收。
```

基础链路必须在 `use_llm_cleanup = false` 且 `use_llm_formula_cleanup = false` 时可独立运行；CLI/API 可以显式启用或关闭 LLM 策略生成和 LLM 公式精修。测试和排查基础链路时优先使用 `--no-llm-cleanup`，并保持 `use_llm_formula_cleanup = false`。

不要让 LLM 成为 `.md/.txt` 入库的必需依赖；公式清洗默认走本地 `formula_cleaner.py`。

---

## 5. 系统资料库产品边界

系统资料库不是用户上传资料库，也不应混入 `data/user_materials/`。当前推荐的信息架构是：

```text
左侧入口：资料库
↓
一级切换：我的资料 / 系统资料
↓
系统资料学科：数学 / 政治 / 英语 / 408 / 其他
↓
学科内内容：习题 / 知识点
```

第一版采用“公共库 + 个人状态”模型：

```text
系统层：
  题目、答案、解析、知识点、来源、资料库名、题型、年份等公共内容
  只读，不随单个用户操作被改写

用户层：
  收藏、掌握状态、错题、个人备注、练习记录、复习时间等
  按 user_id 单独保存
```

当前数学系统库优先使用已有数据：

```text
data/raw/math/exam_papers/math1/{year}/questions.jsonl
data/raw/math/exam_papers/math1/{year}/questions/qXXX.md
data/raw/math/exam_papers/math1/{year}/paper_manifest.json
```

系统资料库第一版筛选字段优先使用已有可靠元数据：

```text
资料库名
考试范围，例如 数一
年份
题型
知识点
个人状态
关键词
```

`difficulty` 当前大多仍是 `unknown`，第一版只保留为占位字段，不作为主筛选入口。后续批量标注或模型估计稳定后，再启用难度筛选。

### 5.1 功能闭环要求

新增任何系统资料库功能前，必须先说明完整闭环，不要只摆按钮：

```text
功能是什么
从哪里设置
点完修改什么数据
在哪里显示完成态
在哪里取消或反向操作
结果流向哪里
是否影响系统层内容
是否写入用户层状态
```

当前个人状态建议拆分为：

```text
mastery_status: not_started / learning / mastered
is_favorite: true / false
in_wrong_book: true / false
personal_note: string
last_practiced_at: datetime | null
review_due_at: datetime | null
```

功能入口和出口必须清晰：

```text
掌握状态：
  设置入口：题目列表行、批量操作、题目详情抽屉
  完成态：列表状态列、知识点掌握统计、复习规划统计
  取消/反向：原入口改回未开始或学习中

收藏：
  设置入口：列表行、题目详情、知识点详情
  完成态：收藏筛选、收藏标记、我的收藏视图
  取消/反向：原入口再次点击取消收藏

错题：
  设置入口：列表行、批量操作、题目详情
  完成态：错题筛选、复习规划待复习池
  取消/反向：错题视图或题目详情移出错题

个人备注：
  设置入口：题目详情、知识点详情
  完成态：详情页展示备注摘要，可按有备注筛选
  取消/反向：备注编辑器删除或清空

生成练习：
  设置入口：筛选结果批量、知识点详情、题目详情同类练习
  完成态：生成练习单或复习任务
  取消/反向：练习单中移除题目或删除练习单

问 AI 讲题：
  设置入口：题目详情、列表快捷入口
  完成态：跳转或带上下文打开问答
  取消/反向：不改变题目状态，除非用户显式标记
```

### 5.2 前端设计约束

系统资料库前端应参考已确认方向：

```text
左侧仍保持四个一级入口：问答、资料库、规划、院校查询
原“我的资料库”改为“资料库”
资料库页内使用“我的资料 / 系统资料”切换
系统资料页面采用类似视频题库的筛选器 + 表格/卡片浏览
习题页和知识点页使用相近布局，避免两套交互
列表负责筛选和批量操作，详情抽屉负责单题/单知识点状态和备注
```

前端设计和实现前，优先用草图或设计说明确认：

```text
页面层级
筛选字段
表格列
详情抽屉内容
每个动作的入口、完成态、取消态
空状态、加载态、错误态
```

## 6. 推荐协作方式和技能

涉及产品设计、页面结构、功能闭环时，优先使用：

```text
superpowers:brainstorming
product-design:get-context
```

推荐流程：

```text
1. 先读 AGENTS.md 和当前相关代码；
2. 先做产品边界和功能闭环，不直接写代码；
3. 给出 2-3 个方案或草图；
4. 等用户选择后再进入实现计划；
5. 实现前使用 superpowers:writing-plans；
6. 实现功能或 bugfix 前优先使用 superpowers:test-driven-development；
7. 遇到失败或异常时使用 superpowers:systematic-debugging；
8. 完成前使用 superpowers:verification-before-completion；
9. 大改或合并前可使用 superpowers:requesting-code-review。
```

如果后续要把“系统资料库设计流程”沉淀为可复用能力，可以再考虑：

```text
skill-creator：创建一个项目专用设计/实现 skill
superpowers:writing-skills：编写或维护该 skill 的说明
```

但当前阶段不必急着创建新 skill，先把 AGENTS.md 作为项目内最高优先级约束维护好。

## 7. 当前不做

本阶段不要做：

```text
新增或重构 PDF/MinerU 完整解析
DOCX 完整解析扩展
图片 OCR/VLM 扩展
ZIP 批量解析扩展
真实向量库接入
数据库重构
真实多用户权限系统
系统题库在线共同编辑
难度自动批量标注的生产化流程
聊天中上传入库
根据资料库回答
资料库自然语言助手
qa 大重构
```

---

## 8. 验证命令

修改后必须运行：

```bash
python -m compileall materials scripts tests

python -m unittest tests.test_formula_cleaner
python -m unittest tests.test_formula_extractor
python -m unittest tests.test_llm_cleaner
python -m unittest tests.test_qwen_formula_client
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"

python -m unittest tests.test_materials_mvp
python -m unittest tests.test_agent_runtime
```

重点检查生成目录：

```text
data/user_materials/tester/{subject}/{material_id}/
├── manifest.json
├── original/
├── parsed/
│   ├── content.md
│   ├── parse_report.json
│   └── pipeline_events.jsonl
├── chunks/chunks.jsonl
└── index/search_index.json
```

---

## 9. 完成汇报

每次修改后汇报：

1. 修改/新增了哪些文件；
2. 是否改动 `qa`；
3. `.md/.txt` 入库是否成功；
4. 是否生成 `parsed/content.md`；
5. 是否生成 `parsed/parse_report.json`；
6. formula_cleaning 是否写入 manifest 和 parse_report；
7. chunk/index/search 是否可用；
8. 测试命令结果；
9. 仍保留哪些占位功能。
