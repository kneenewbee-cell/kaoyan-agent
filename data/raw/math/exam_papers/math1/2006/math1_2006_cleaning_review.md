# 2006 数学一清洗核对记录

## 本轮核对范围

- 核对 `math1_2006_questions.md`、`math1_2006_answers.md`、`questions.jsonl` 与 `questions/q001.md` 至 `questions/q023.md`。
- 对照源页图像 `images/source_pages/page_061.png` 至 `page_063.png` 抽查题面、题号、题型和来源页。
- 全卷共 23 题，答案与解析均为 `available`，题卡与 JSONL 已同步。

## 结论

- 总题面、单题题卡、答案速查表、`questions.jsonl` 四处结构一致。
- 已核对答案和解析与题意的对应关系，未发现数学答案错误。
- 解析整体适合直接呈现给用户。

## 本轮优化

- 第 4、8、9、21、22 题等处补全 `\sqrt{...}` 的参数花括号。
- 第 22 题补全 `\frac{1}{2}`、`\frac{1}{4}` 以及 `\sqrt{y}` 等展示写法，保证概率密度分段式稳定渲染。
- 第 5 题将用户可见的行列式竖线写法统一为 `\det`，避免与绝对值混淆。
- 重新从题卡同步 `questions.jsonl` 的答案与解析，保证题卡和检索数据一致。

## 保留说明

- 源页图像和 OCR 原始证据文件未改动。
- 表格分隔线、概率事件、绝对值和小行列式 `\begin{vmatrix}...\end{vmatrix}` 保留原语义。
