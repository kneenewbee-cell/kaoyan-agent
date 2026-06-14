---
name: math
description: 考研数学一二三真题工具链、Qwen 模型分工、意图路由。维护或扩展数学能力时使用。
---

# Math Skill

## 领域
- `math_exam`：考研真题，需 exam_type + year + question_number
- `math_general`：通用数学（概念、定理、计算、证明）

## 题库
`data/raw/math/exam_papers/{math1,math2,math3}/{year}/{type}_{year}_questions.md + _answers.md`

## 12 个工具
真题：solve_exam_question（OCR→解题→核对→重试×3→兜底）、show_math_exam_question、show_math_exam_answer
局部操作：explain_math_step、clarify_math_symbol、rewrite_math_answer、summarize_math_solution
通用/图片：solve_general_math、ocr_math_image
核对：judge_math_answer
追问（需 DAG 开关）：answer_math_followup

## 模型分工
- Qwen-Math：解题、步骤解释
- Qwen-Max：总控、路由、符号解释兜底、改写、总结
- Qwen-VL：OCR、公式识别、图形描述

## 路由规则
1. 明确年份+科类+题号 → exam 工具
2. 图片无题号 → ocr → solve_general_math（屏蔽真题工具）
3. 图片文件名不可作真题定位依据
