---
name: followup
description: DAG 追问链路——分类、溯源、因果链替代平铺历史。修改追问系统时使用。
---

# Followup Skill

用 DAG（有向无环图）替代"最近 15 轮平铺历史"。当前 turn 沿 parent 边递归回溯到 root，只把相关链路拼入 prompt。实测 prompt token 约 80% 节省。

## 图模型
- 每轮 = 节点（turn_id）
- 独立问题 → 父节点 EMPTY(0)
- 追问 → 父节点 = 被追问的 turn

## 5 分类器
`classify_followup_route_with_llm()`：
- `independent` → 正常 tool loop
- `step_followup` → explain_math_step
- `weak_nonstep_followup` → DAG 链路 → LLM 直答
- `contextual_nonstep_followup` → DAG 链路 → LLM 直答
- `ambiguous` → LLM 请用户澄清

## 关键函数
- `followup_subgraph_for_parents()` — 从所有 parent 递归收集祖先（BFS）
- `format_followup_dag_context()` — 组装 root + chain + dag 元数据
- `build_dag_followup_messages()` — DAG 链路替代平铺历史

## 性能
prompt_tokens DAG ~2,200 vs 平铺 ~10,500；每轮 2 次 LLM 调用（分类器 + 回答）；max_tokens=900 控制回答长度。

## 当前限制
- 仅 math 学科，回溯窗口 5 轮
- step_followup 未强制 tool_choice
- 跨会话 DAG 不支持

## 测试
`python -m unittest tests.test_agent_runtime tests.test_conversation_scenarios`
