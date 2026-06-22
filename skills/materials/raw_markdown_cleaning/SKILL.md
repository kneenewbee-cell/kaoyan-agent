# Raw Markdown Cleaning Skill

## 1. 角色定位

你是项目中专门负责“用户上传资料 parse 后得到的 raw_markdown 的整理、结构识别与清洗”的实现助手。

当前项目是一个考研智能体助手，资料库模块的大流程是：

```text
用户上传文件
→ parser 解析为 raw_markdown
→ raw_markdown 整理与清洗
→ cleaned_markdown
→ chunk
→ index
→ retrieval / QA
```

本 skill 只负责其中这一段：

```text
raw_markdown
→ 构造格式探测样本 format_probe.json
→ 调用 Qwen 读取样本并输出 cleaning_strategy.json
→ 校验 cleaning_strategy.json
→ 本地规则执行清洗
→ cleaned_markdown + parse_report.json
```

不要在本 skill 中实现问答、RAG、向量检索、前端 UI 或数据库大改造。
本模块只处理 raw_markdown 的整理与清洗。

---

## 2. 核心目标

实现一套稳定、可扩展的 raw_markdown 清洗系统，用于把用户上传后 parse 出来的 Markdown / 类 Markdown 文本整理成结构更清晰的 Markdown。

核心目标：

1. 保留原文内容，不总结、不改写、不补充、不删除知识点。
2. 识别用户资料中的标题结构，例如：
   - `知识点一：极限的计算`
   - `考点1 函数的概念`
   - `要点二 导数定义`
   - `一、极限`
   - `1. 导数定义`
   - `1.1 函数连续性`
   - `第一章 函数、极限与连续`
3. 把可信的主标题转成 Markdown 标题，例如 `## 知识点一：极限的计算`。
4. 把可信的子栏目转成子标题，例如：
   - `### 核心概念`
   - `### 常用方法`
   - `### 经典例题`
   - `### 易错提醒`
5. 低置信度时保守处理，不强行把正文短句升为标题。
6. 输出清洗报告 `parse_report.json`，方便后续调试和优化。
7. 允许 LLM 只参与“格式判断 / 策略生成”，但不直接清洗全文。

---

## 3. 总体设计原则

### 3.1 不让 LLM 直接清洗全文

禁止采用这种方式：

```text
raw_markdown 全文 → LLM → cleaned_markdown 全文
```

原因：

- 长文容易漏段。
- 公式可能被改坏。
- 表格可能被破坏。
- 图片路径可能被破坏。
- LLM 可能擅自总结、补充或改写。
- 同一份资料多次输出可能不稳定。

推荐方式：

```text
raw_markdown 样本 → Qwen → cleaning_strategy.json
raw_markdown 全文 + cleaning_strategy.json → 本地规则清洗 → cleaned_markdown
```

LLM 只负责判断“这份资料的格式规律是什么”，本地代码负责稳定执行。

---

### 3.2 本地规则必须保守

任何结构识别都必须遵守：

- 只在行首识别标题候选。
- 不在代码块内识别标题。
- 不破坏 Markdown 表格。
- 不破坏 LaTeX 公式。
- 不破坏图片链接。
- 不改写正文内容。
- 不删除用户原文。
- 不合并、总结、翻译、润色正文。
- 不执行 LLM 返回的代码。
- 不直接执行 LLM 返回的正则表达式，除非经过白名单校验。

---

### 3.3 低置信度降级

如果无法可靠识别结构，应降级为：

```text
保留原 Markdown 结构
或只做基础格式清洗
或后续按长度切块
```

不要为了“看起来结构化”而强行添加标题。

---

## 4. Qwen 使用约定

### 4.1 固定模型

用于读取 `format_probe.json` 并输出 `cleaning_strategy.json` 的模型固定为：

```text
qwen3.6-plus-2026-04-02
```

### 4.2 API Key

API Key 用户本地已有，不要写死在代码中，不要提交到仓库。

推荐读取方式：

```text
环境变量：QWEN_API_KEY
```

也可以兼容项目已有配置，例如：

```text
.env
config.local.json
本地 settings 文件
```

但任何情况下都不要把真实 API Key 写进：

```text
SKILL.md
源码
测试文件
README
日志
parse_report.json
cleaning_strategy.json
```

### 4.3 Qwen 的职责

Qwen 只负责：

```text
读取 format_probe.json
判断 raw_markdown 的结构规律
输出 cleaning_strategy.json
```

Qwen 不负责：

```text
清洗全文
重写全文
总结内容
补充内容
删除内容
生成 Python 代码
生成需要执行的正则代码
```

### 4.4 Qwen 输入

Qwen 的输入必须是 JSON 样本，不是 raw_markdown 全文。

推荐输入文件名：

```text
format_probe.json
```

### 4.5 Qwen 输出

Qwen 必须只输出 JSON，不要输出 Markdown，不要输出解释，不要输出代码块。

推荐输出文件名：

```text
cleaning_strategy.json
```

如果 Qwen 输出不是合法 JSON，必须丢弃该输出，使用本地默认保守策略。

---

## 5. 建议新增文件

优先在 `materials/postprocess/` 下新增以下文件：

```text
materials/postprocess/format_probe.py
materials/postprocess/qwen_strategy_client.py
materials/postprocess/strategy_schema.py
materials/postprocess/strategy_validator.py
materials/postprocess/strategy_cleaner.py
materials/postprocess/raw_markdown_cleaner.py
```

职责如下：

### 5.1 `format_probe.py`

负责从 raw_markdown 中抽样，构造给 Qwen 或本地探测器使用的格式样本。

输入：

```python
raw_markdown: str
metadata: dict | None
```

输出：

```python
FormatProbe
```

`FormatProbe` 建议包含：

```json
{
  "version": "1.0",
  "filename": "高数知识点.txt",
  "char_count": 12000,
  "line_count": 500,
  "head_excerpt": "...文档开头若干行...",
  "middle_excerpts": [
    "...中间片段1...",
    "...中间片段2..."
  ],
  "tail_excerpt": "...文档末尾若干行...",
  "existing_headings": [
    "# 考研数学高等数学知识点"
  ],
  "candidate_marker_lines": [
    "知识点一：极限的计算",
    "知识点二：导数的定义",
    "一、函数的概念",
    "1. 极限的计算",
    "1.1 函数连续性"
  ],
  "short_line_candidates": [
    "核心概念",
    "常用计算方法",
    "经典例题",
    "易错提醒"
  ],
  "table_like_lines_count": 3,
  "formula_like_lines_count": 5,
  "image_lines_count": 2,
  "code_fence_count": 0
}
```

抽样建议：

- 文档前 120 行。
- 文档中间均匀抽取 2 到 3 段，每段 60 行以内。
- 文档末尾 80 行。
- 提取所有已有 Markdown 标题。
- 提取疑似标题行。
- 提取高频短行。
- 统计表格、公式、图片、代码块数量。

不要把全文直接塞给 Qwen。

---

### 5.2 `qwen_strategy_client.py`

负责调用 Qwen，把 `format_probe.json` 转换成 `cleaning_strategy.json`。

核心函数建议：

```python
def generate_strategy_with_qwen(
    format_probe: dict,
    *,
    model: str = "qwen3.6-plus-2026-04-02",
    api_key: str | None = None,
    timeout_seconds: int = 60,
) -> dict:
    ...
```

要求：

1. 默认模型必须是 `qwen3.6-plus-2026-04-02`。
2. API Key 优先从入参读取；没有入参则从 `QWEN_API_KEY` 环境变量读取。
3. 不能在日志中打印 API Key。
4. Qwen 返回值必须解析为 JSON。
5. 如果调用失败、超时、返回非 JSON，抛出可控异常或返回默认策略。
6. 不要让 Qwen 输出 cleaned_markdown 全文。
7. 不要执行 Qwen 返回的任何代码。

推荐系统提示词：

```text
你是 raw_markdown 格式分析器，只输出 JSON。

任务：
根据用户上传资料解析后的 raw_markdown 样本 format_probe，判断这份资料的结构规律，并输出 cleaning_strategy.json。

限制：
1. 只能输出 JSON。
2. 不要输出 Markdown。
3. 不要输出解释。
4. 不要输出代码块。
5. 不要输出 Python 代码。
6. 不要返回需要执行的正则表达式。
7. 不要清洗全文。
8. 不要总结、改写、补充、删除原文内容。
9. 只判断结构策略：主标题规则、子标题规则、元数据字段、保护规则、降级策略。
10. 如果不确定，使用保守策略。
```

推荐用户提示词：

```text
下面是 raw_markdown 的格式探测样本 format_probe.json。
请根据样本输出 cleaning_strategy.json。
必须严格符合指定 JSON schema。
不要输出 JSON 之外的任何内容。
```

---

### 5.3 `strategy_schema.py`

定义 `cleaning_strategy.json` 的 Pydantic schema。

建议 schema：

```json
{
  "version": "1.0",
  "document_profile": {
    "subject": "math|politics|english|cs408|unknown",
    "document_type": "knowledge_notes|exercise_notes|outline|table_like|mixed|unknown",
    "language": "zh|en|mixed",
    "confidence": 0.0
  },
  "main_section_rule": {
    "enabled": true,
    "target_level": 2,
    "marker_type": "label_ordinal|chinese_outline|arabic_outline|decimal_outline|chapter|existing_markdown|none",
    "aliases": ["知识点", "考点", "要点", "专题", "模块"],
    "number_styles": ["chinese", "arabic"],
    "requires_line_start": true,
    "requires_colon": false,
    "min_repeats": 2,
    "examples": []
  },
  "subsection_rules": [
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["核心概念", "基本概念", "概念"],
      "requires_line_start": true,
      "min_repeats": 1
    }
  ],
  "metadata_rules": {
    "recognize_bracket_fields": true,
    "fields": ["考频", "难度", "题型", "来源", "备注"]
  },
  "cleanup_rules": {
    "normalize_blank_lines": true,
    "strip_trailing_spaces": true,
    "remove_control_chars": true,
    "preserve_tables": true,
    "preserve_code_blocks": true,
    "preserve_formulas": true,
    "preserve_images": true
  },
  "fallback_policy": {
    "if_main_sections_less_than": 2,
    "action": "keep_original_structure",
    "chunk_by": "length",
    "reason": "主标题命中不足时不强行改写结构"
  },
  "safety_rules": {
    "do_not_rewrite_content": true,
    "do_not_summarize": true,
    "do_not_translate": true,
    "do_not_delete_unknown_lines": true
  }
}
```

schema 要做校验：

- `target_level` 只能是 1 到 6。
- `confidence` 必须在 0 到 1。
- `marker_type` 必须是枚举值。
- `aliases` 要去重。
- `fallback_policy.action` 必须是允许值。
- 不允许 LLM 返回任意代码。
- 不允许 LLM 返回未校验的可执行正则。

---

### 5.4 `strategy_validator.py`

负责校验 Qwen 或本地探测器生成的 strategy。

校验规则：

1. JSON 必须能被解析。
2. 必须符合 Pydantic schema。
3. 不允许包含可执行代码。
4. 不允许包含危险字段，例如：
   - `eval`
   - `exec`
   - `import`
   - `subprocess`
   - `os.system`
   - `open(`
   - `__`
5. 如果 strategy 不合法，使用默认保守策略。

默认保守策略：

```json
{
  "version": "1.0",
  "document_profile": {
    "subject": "unknown",
    "document_type": "unknown",
    "language": "zh",
    "confidence": 0.3
  },
  "main_section_rule": {
    "enabled": false,
    "target_level": 2,
    "marker_type": "none",
    "aliases": [],
    "number_styles": [],
    "requires_line_start": true,
    "requires_colon": false,
    "min_repeats": 2,
    "examples": []
  },
  "subsection_rules": [],
  "metadata_rules": {
    "recognize_bracket_fields": true,
    "fields": ["考频", "难度", "题型", "来源", "备注"]
  },
  "cleanup_rules": {
    "normalize_blank_lines": true,
    "strip_trailing_spaces": true,
    "remove_control_chars": true,
    "preserve_tables": true,
    "preserve_code_blocks": true,
    "preserve_formulas": true,
    "preserve_images": true
  },
  "fallback_policy": {
    "if_main_sections_less_than": 2,
    "action": "keep_original_structure",
    "chunk_by": "length",
    "reason": "未获得可信结构策略"
  },
  "safety_rules": {
    "do_not_rewrite_content": true,
    "do_not_summarize": true,
    "do_not_translate": true,
    "do_not_delete_unknown_lines": true
  }
}
```

---

### 5.5 `strategy_cleaner.py`

负责根据 `cleaning_strategy.json` 对全文 raw_markdown 执行本地规则清洗。

核心函数建议：

```python
def clean_with_strategy(
    raw_markdown: str,
    strategy: CleaningStrategy,
    *,
    source_name: str | None = None,
) -> CleanResult:
    ...
```

返回：

```python
@dataclass
class CleanResult:
    cleaned_markdown: str
    strategy: dict
    parse_report: dict
    warnings: list[str]
```

本地清洗流程：

```text
1. 统一换行
2. 删除不可见控制字符
3. 保护代码块
4. 保护表格块
5. 保护公式块
6. 逐行扫描
7. 判断是否命中主标题规则
8. 判断是否命中子标题规则
9. 命中则转换为对应 Markdown 标题
10. 未命中则原样保留
11. 连续空行压缩
12. 输出 cleaned_markdown 和 parse_report
```

---

### 5.6 `raw_markdown_cleaner.py`

作为本模块统一入口。

核心函数建议：

```python
def clean_raw_markdown(
    raw_markdown: str,
    *,
    source_name: str | None = None,
    use_llm_profile: bool = False,
    user_hints: dict | None = None,
) -> CleanResult:
    ...
```

执行逻辑：

```text
1. 构造 format_probe
2. 保存 format_probe.json
3. 如果 use_llm_profile=True：
   3.1 调用 Qwen 生成 strategy
   3.2 校验 strategy
   3.3 失败则降级到本地探测策略
4. 如果 use_llm_profile=False：
   4.1 使用本地探测策略
5. 如果本地探测也不可信：
   5.1 使用默认保守策略
6. 使用 strategy_cleaner 清洗全文
7. 返回 CleanResult
```

---

## 6. format_probe.json 输入样本

下面是一个 Qwen 应读取的 `format_probe.json` 样本：

```json
{
  "version": "1.0",
  "filename": "高数知识点.txt",
  "char_count": 5200,
  "line_count": 180,
  "head_excerpt": "考研数学高等数学五大核心知识点及讲解\n\n知识点一：极限的计算\n\n【考频】★★★★★\n【难度】★★★☆☆\n\n核心概念\n极限是高等数学的基础。\n\n常用计算方法\n（1）等价无穷小替换\n（2）洛必达法则\n\n经典例题\n例：求 lim...",
  "middle_excerpts": [
    "知识点二：导数的定义\n\n核心概念\n导数表示函数在某一点的瞬时变化率。\n\n常见题型\n（1）按定义求导\n（2）复合函数求导\n\n易错提醒\n注意导数存在与连续的关系。",
    "知识点三：中值定理\n\n核心概念\n罗尔定理、拉格朗日中值定理、柯西中值定理是常见考点。\n\n典型例题\n证明某方程至少存在一个根。"
  ],
  "tail_excerpt": "知识点五：多元函数微分法\n\n核心概念\n多元函数偏导数、全微分、极值与条件极值是重点。\n\n应用举例\n求二元函数的极值。\n\n易错点\n注意驻点不一定是极值点。",
  "existing_headings": [],
  "candidate_marker_lines": [
    "知识点一：极限的计算",
    "知识点二：导数的定义",
    "知识点三：中值定理",
    "知识点五：多元函数微分法"
  ],
  "short_line_candidates": [
    "核心概念",
    "常用计算方法",
    "经典例题",
    "易错提醒",
    "常见题型",
    "典型例题",
    "应用举例",
    "易错点"
  ],
  "table_like_lines_count": 0,
  "formula_like_lines_count": 3,
  "image_lines_count": 0,
  "code_fence_count": 0
}
```

---

## 7. cleaning_strategy.json 输出样本

下面是 Qwen 应输出的 `cleaning_strategy.json` 样本：

```json
{
  "version": "1.0",
  "document_profile": {
    "subject": "math",
    "document_type": "knowledge_notes",
    "language": "zh",
    "confidence": 0.9
  },
  "main_section_rule": {
    "enabled": true,
    "target_level": 2,
    "marker_type": "label_ordinal",
    "aliases": ["知识点"],
    "number_styles": ["chinese"],
    "requires_line_start": true,
    "requires_colon": false,
    "min_repeats": 2,
    "examples": [
      "知识点一：极限的计算",
      "知识点二：导数的定义",
      "知识点三：中值定理"
    ]
  },
  "subsection_rules": [
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["核心概念"],
      "requires_line_start": true,
      "min_repeats": 1
    },
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["常用计算方法", "常用方法", "解题方法"],
      "requires_line_start": true,
      "min_repeats": 1
    },
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["经典例题", "典型例题", "经典例子"],
      "requires_line_start": true,
      "min_repeats": 1
    },
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["易错提醒", "易错点", "注意事项"],
      "requires_line_start": true,
      "min_repeats": 1
    },
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["常见题型", "题型总结"],
      "requires_line_start": true,
      "min_repeats": 1
    },
    {
      "enabled": true,
      "target_level": 3,
      "type": "fixed_label",
      "aliases": ["应用举例", "应用", "实际应用"],
      "requires_line_start": true,
      "min_repeats": 1
    }
  ],
  "metadata_rules": {
    "recognize_bracket_fields": true,
    "fields": ["考频", "难度", "题型", "来源", "备注"]
  },
  "cleanup_rules": {
    "normalize_blank_lines": true,
    "strip_trailing_spaces": true,
    "remove_control_chars": true,
    "preserve_tables": true,
    "preserve_code_blocks": true,
    "preserve_formulas": true,
    "preserve_images": true
  },
  "fallback_policy": {
    "if_main_sections_less_than": 2,
    "action": "keep_original_structure",
    "chunk_by": "length",
    "reason": "主标题命中不足时不强行改写结构"
  },
  "safety_rules": {
    "do_not_rewrite_content": true,
    "do_not_summarize": true,
    "do_not_translate": true,
    "do_not_delete_unknown_lines": true
  }
}
```

---

## 8. 标题识别规则

### 8.1 通用限制

标题识别必须满足：

- 候选标题必须在行首。
- 行长度不能过长，建议不超过 80 个中文字符或 120 个英文字符。
- 不能在代码块内。
- 不能是 Markdown 表格行。
- 不能是图片行。
- 不能是公式行。
- 不能是普通正文中的中途短语。

---

### 8.2 `label_ordinal`

识别：

```text
知识点一：极限的计算
知识点二 导数的定义
考点1 函数连续
要点3：中值定理
专题四 多元函数微分法
模块2 线性代数基础
```

需要支持：

- 中文数字：一、二、三、四、五、六、七、八、九、十、十一、十二……
- 阿拉伯数字：1、2、3……
- 冒号可选。
- 冒号支持 `:` 和 `：`。
- alias 来自 strategy。

输出示例：

```markdown
## 知识点一：极限的计算
```

---

### 8.3 `chinese_outline`

识别：

```text
一、函数、极限与连续
二、导数与微分
三、中值定理
```

输出：

```markdown
## 一、函数、极限与连续
```

注意：

- 必须在行首。
- 至少命中 `min_repeats` 次才启用。
- 不要把正文里的“一、”误识别。

---

### 8.4 `arabic_outline`

识别：

```text
1. 函数的概念
2. 极限的计算
3、导数的定义
（1）等价无穷小替换
1）洛必达法则
```

需要谨慎：

- `1. xxx` 可以作为主标题或子标题，取决于 strategy。
- `（1）xxx` 和 `1）xxx` 更常见于子内容，不要默认升为主标题。
- 如果同一文档中主结构是 `知识点一/二`，则 `（1）` 通常保留为正文列表，不升标题。

---

### 8.5 `decimal_outline`

识别：

```text
1.1 函数连续性
1.2 间断点分类
2.1 导数定义
```

通常作为二级或三级标题。

输出层级由 strategy 决定：

```markdown
### 1.1 函数连续性
```

---

### 8.6 `chapter`

识别：

```text
第一章 函数、极限与连续
第二节 导数的定义
第3章 线性代数
```

输出：

```markdown
## 第一章 函数、极限与连续
```

---

### 8.7 `fixed_label` 子栏目

识别固定短行，例如：

```text
核心概念
基本概念
常用方法
常用计算方法
经典例题
典型例题
易错提醒
易错点
注意事项
应用举例
```

输出：

```markdown
### 核心概念
```

限制：

- 必须整行匹配或接近整行匹配。
- 不要匹配正文中的短语。
- 如果同一类标签在全文只出现一次，也可以升标题，但要记录较低置信度。
- 如果命中后附近没有正文内容，要记录 warning。

---

## 9. 公式、表格、代码块、图片保护

### 9.1 代码块

代码块内部不得做标题识别、空格整理、内容改写。

例如：

````markdown
```python
print("知识点一：不要识别我")
```
````

代码块内的 `知识点一：不要识别我` 不得转成标题。

---

### 9.2 Markdown 表格

类似：

```markdown
| 学校 | 学院 | 分数线 |
| --- | --- | --- |
| 南昌大学 | 信息工程学院 | 320 |
```

表格内部不得升标题。

---

### 9.3 公式

保护块级公式：

```markdown
$$
\lim_{x \to 0} \frac{\sin x}{x}=1
$$
```

保护行内公式：

```markdown
当 $x \to 0$ 时，$\sin x \sim x$。
```

不得改写公式内容。

---

### 9.4 图片

保护：

```markdown
![alt](../assets/images/img_001.png)
```

不得破坏图片路径。

图片复制、路径改写可以继续放在已有 `asset_rewriter.py` 中，不强制迁入本模块。

---

## 10. parse_report.json 格式

每次清洗都要生成报告。

建议格式：

```json
{
  "source_name": "高数知识点.txt",
  "strategy_source": "qwen|local|default",
  "qwen_model": "qwen3.6-plus-2026-04-02",
  "document_profile": {
    "subject": "math",
    "document_type": "knowledge_notes",
    "confidence": 0.9
  },
  "stats": {
    "line_count": 500,
    "char_count": 12000,
    "main_sections_detected": 5,
    "subsections_detected": 24,
    "existing_markdown_headings": 1,
    "converted_headings": 29,
    "warnings_count": 2
  },
  "main_section_matches": [
    {
      "line_no": 12,
      "raw": "知识点一：极限的计算",
      "converted": "## 知识点一：极限的计算",
      "rule": "label_ordinal",
      "confidence": 0.94
    }
  ],
  "subsection_matches": [
    {
      "line_no": 18,
      "raw": "核心概念",
      "converted": "### 核心概念",
      "rule": "fixed_label",
      "confidence": 0.82
    }
  ],
  "warnings": [
    {
      "line_no": 88,
      "message": "疑似标题但命中次数不足，已保留为正文",
      "raw": "重点提醒"
    }
  ],
  "fallback_used": false
}
```

---

## 11. cleaned_markdown 输出要求

输出的 Markdown 应满足：

1. 文档开头最好有一个 H1。
2. 主知识点或主章节使用 H2。
3. 子栏目使用 H3。
4. 原文正文顺序不变。
5. 原文内容不被总结、不被删减。
6. 连续空行最多保留 2 个。
7. 行尾空格清理。
8. 表格、公式、图片、代码块保持可用。

示例：

原始 raw_markdown：

```text
考研数学高等数学五大核心知识点及讲解

知识点一：极限的计算

【考频】★★★★★
【难度】★★★☆☆

核心概念
极限是高等数学的基础。

常用计算方法
（1）等价无穷小替换
（2）洛必达法则

知识点二：导数的定义
...
```

清洗后：

```markdown
# 考研数学高等数学五大核心知识点及讲解

## 知识点一：极限的计算

【考频】★★★★★
【难度】★★★☆☆

### 核心概念

极限是高等数学的基础。

### 常用计算方法

（1）等价无穷小替换
（2）洛必达法则

## 知识点二：导数的定义

...
```

---

## 12. 集成到现有 service.py

在 `MaterialIngestionService.ingest_file()` 中，parser 生成 `content.md` 后，调用新的 raw_markdown 清洗流程。

建议伪代码：

```python
raw_markdown = markdown_path.read_text(encoding="utf-8")

clean_result = clean_raw_markdown(
    raw_markdown=raw_markdown,
    source_name=source_path.name,
    use_llm_profile=options.use_llm_cleanup,
    user_hints={
        "subject": options.subject,
        "material_type": options.material_type,
    },
)

markdown_path.write_text(clean_result.cleaned_markdown, encoding="utf-8")

write_json(parsed_dir / "format_probe.json", clean_result.format_probe)
write_json(parsed_dir / "cleaning_strategy.json", clean_result.strategy)
write_json(parsed_dir / "parse_report.json", clean_result.parse_report)
```

注意：

- `use_llm_cleanup` 这个名字可以暂时沿用，但语义应改为“是否允许 Qwen 生成 cleaning_strategy”，不是“让 LLM 清洗全文”。
- 如果 Qwen 不可用，使用本地探测策略。
- 如果本地探测也不可信，使用默认保守策略。

---

## 13. 本地自动探测策略

即使不开 Qwen，也应该有一个本地探测器。

本地探测顺序建议：

```text
1. 如果已有 H2 数量 >= 2，优先尊重原始 Markdown 结构。
2. 如果 label_ordinal 命中 >= 2，使用 label_ordinal 作为主结构。
3. 如果 chinese_outline 命中 >= 2，使用 chinese_outline。
4. 如果 chapter 命中 >= 2，使用 chapter。
5. 如果 decimal_outline 命中 >= 2，使用 decimal_outline。
6. 如果都不满足，保留原结构。
```

子栏目本地探测：

```text
如果短行候选中反复出现：
核心概念 / 基本概念 / 常用方法 / 经典例题 / 易错提醒 / 注意事项 / 应用举例 / 常见题型
则加入 fixed_label subsection_rules。
```

---

## 14. 测试要求

必须新增测试，覆盖以下场景：

### 14.1 Qwen strategy JSON 校验

输入一个合法 `cleaning_strategy.json`，期望通过校验。

输入一个非 JSON 文本，期望降级为默认保守策略。

输入一个包含危险字段的 JSON，例如：

```json
{
  "eval": "print(1)"
}
```

期望拒绝。

---

### 14.2 知识点结构

输入：

```text
知识点一：极限
核心概念
正文
知识点二：导数
经典例题
正文
```

期望：

```markdown
## 知识点一：极限
### 核心概念
## 知识点二：导数
### 经典例题
```

---

### 14.3 中文大纲结构

输入：

```text
一、函数
正文
二、极限
正文
三、导数
正文
```

期望识别为 H2。

---

### 14.4 已有 Markdown 标题

输入：

```markdown
# 总标题
## 第一节
正文
## 第二节
正文
```

期望不要重复添加标题符号。

---

### 14.5 代码块保护

输入代码块内含：

```text
一、不要识别我
知识点一：不要识别我
```

期望代码块内不被转换。

---

### 14.6 表格保护

表格内含 `知识点一`，不得转换为标题。

---

### 14.7 低置信度降级

只有一个：

```text
知识点一：极限
```

但没有 `知识点二`，不应强行认定整篇结构，除非 strategy 明确允许。

---

## 15. 不要做的事情

不要做以下事情：

1. 不要让 Qwen 直接输出 cleaned_markdown 全文。
2. 不要让 Qwen 返回 Python 代码然后执行。
3. 不要在正文中间识别标题。
4. 不要破坏公式、表格、图片、代码块。
5. 不要删除无法识别的行。
6. 不要擅自总结内容。
7. 不要为了美观改写用户原句。
8. 不要把所有短行都升成标题。
9. 不要把 `（1）` 默认升成主标题。
10. 不要让清洗逻辑和 chunk / index 强耦合。
11. 不要把 API Key 写入仓库或日志。

---

## 16. 最终验收标准

完成后应满足：

1. `.md` / `.txt` parser 产出的 raw_markdown 可以进入统一清洗流程。
2. 清洗前生成 `format_probe.json`。
3. 启用 `use_llm_cleanup=True` 时，调用 `qwen3.6-plus-2026-04-02` 根据 `format_probe.json` 生成 `cleaning_strategy.json`。
4. Qwen 不可用时，本地规则仍可运行。
5. 清洗后生成 `cleaned_markdown`，并写回 `parsed/content.md`。
6. 同时生成：
   - `format_probe.json`
   - `cleaning_strategy.json`
   - `parse_report.json`
7. 对“知识点一/二/三”格式有明显改善。
8. 对“一、二、三”格式有明显改善。
9. 对“核心概念/经典例题/易错提醒”等子栏目有明显改善。
10. 没有破坏公式、表格、图片、代码块。
11. 低置信度时保守降级。
12. 所有新增测试通过。

---

## 17. 推荐实现顺序

按以下顺序实现：

```text
1. strategy_schema.py
2. format_probe.py
3. strategy_validator.py
4. 本地 strategy detector
5. qwen_strategy_client.py
6. strategy_cleaner.py
7. raw_markdown_cleaner.py
8. 接入 service.py
9. 新增 tests/test_raw_markdown_cleaning.py
10. 跑 py_compile 和 pytest
```

先保证本地规则跑通，再接入 Qwen profile。
Qwen 只增强策略判断，不作为清洗主执行器。

---

## 18. 给 Codex 的执行提醒

实现时优先保证：

```text
可运行
可测试
可降级
不破坏原文
不泄露 API Key
```

不要一次性大改整个资料库模块。
优先让 `.md` / `.txt` 的 raw_markdown 清洗链路跑通，然后再扩展 PDF / DOCX / 图片解析后的 raw_markdown。
