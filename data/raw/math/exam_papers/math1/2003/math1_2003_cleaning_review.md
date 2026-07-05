# 2003 数学一清洗核对记录

## 本轮核对范围

- 核对 `math1_2003_questions.md`、`math1_2003_answers.md`、`questions.jsonl` 与 `questions/q001.md` 至 `questions/q022.md`。
- 对照源页图像 `images/source_pages/page_052.png` 至 `page_054.png` 抽查题面、题号和题型。
- 全卷共 22 题，答案与解析均为 `available`，题卡与 JSONL 已同步。

## 结论

- 总题面、单题题卡、答案速查表、`questions.jsonl` 四处结构一致。
- 已核对答案和解析的题意对应关系，未发现数学答案错误。
- 解析整体适合直接呈现给用户。

## 本轮优化

- 第 1、6 题补全 `\sqrt{...}` 的参数花括号。
- 第 17 题总题面中的单 token 分数写法统一补全为 `\frac{3}{2}`。
- 第 19 题将特征多项式中的行列式竖线写法统一为 `\det(\lambda E-(B+2E))`。
- 第 20 题将增广矩阵行列式统一写为 `\det(\bar A)`。

## 保留说明

- `\begin{vmatrix}...\end{vmatrix}` 用于小行列式展示，保留。
- 概率事件、绝对值和表格中的竖线保留原语义。
