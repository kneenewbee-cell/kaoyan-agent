# Tool Selection Prompt Structure

本文档记录 `scripts/agent_runtime.py` 中第一层路由与第二层 `tool_selection` prompt 的组成，方便后续改 prompt 时避免重复、遗漏或职责混杂。

## 总体链路

```text
用户输入
  -> 第一层路由：学科 + 追问关系 + parent 判定
  -> 工具集合选择：select_tools()
  -> 第二层 tool_selection LLM
       -> 直接回答
       -> 调用工具
       -> 工具非 direct 时再由 LLM 组织最终回答
```

第二层 prompt 的核心职责是决定“直接回答还是调用工具”。回答长短与组织方式统一由 `DEFAULT_ANSWER_SHAPE_POLICY` 控制；数学、政治等学科策略只负责工具选择边界。

## 第一层路由

第一层路由主要由 `build_route_decision()` / `route_with_llm()` 产生 `RouteDecision`，统一判断：

```text
subject: math | politics | english | unsupported
followup_category:
  independent
  step_followup
  weak_nonstep_followup
  contextual_nonstep_followup
  ambiguous
parent_turn_id: number | null
parent_turn_ids: list[number]
clarification: string | null
```

注意：

- `unsupported` 是学科标签，不是追问标签。它表示学科证据不足，通常会进入澄清或无工具可用的提示。
- `ambiguous` 表示追问 parent 无法确定，通常先进入澄清，不进入第二层 `tool_selection`。
- `independent` 表示独立新问题，系统会清空 parent。
- `step_followup` 是步骤追问，例如“第二步为什么可以这样换元”。它不走 DAG，通常进入普通 `tool_selection`，再选择 `explain_math_step`。
- `weak_nonstep_followup` / `contextual_nonstep_followup` 是非步骤追问，例如“七阶呢”“这个条件下还成立吗”。若有 parent，则进入 DAG tool_selection。

## 第一层标签去向

```text
independent
  -> build_tool_selection_messages()
  -> context_mode = independent
  -> 不带平铺短期历史
  -> 可带同学科、关键词匹配的少量参考片段

step_followup
  -> build_tool_selection_messages()
  -> context_mode = plain
  -> 带最近短期平铺历史
  -> 第二层通常选择 explain_math_step

weak_nonstep_followup / contextual_nonstep_followup + parent
  -> format_followup_dag_context()
  -> build_dag_tool_selection_messages()
  -> context_mode = dag
  -> 使用 DAG 链路替代最近 15 轮平铺历史

weak_nonstep_followup / contextual_nonstep_followup 无 parent
  -> 通常先澄清

ambiguous
  -> build_followup_clarification_messages()
  -> 先澄清，不进入 tool_selection
```

`plain` 不是第一层标签，而是第二层 prompt 组装时的默认上下文模式名。它表示“非 DAG、非 independent，使用最近短期平铺历史”。

## 第二层 Prompt 组成

### 普通问答 / plain

普通非 DAG、非 independent 的问题使用 `build_tool_selection_messages()`，再通过 `append_tool_selection_policy()` 追加工具选择策略。

组成：

```text
MAIN_SYSTEM_PROMPT
+ CONTEXT_FOLLOWUP_PROMPT（仅 ENABLE_CONTEXT_FOLLOWUP_TOOLS=1 时）
+ format_hint
+ 最近短期平铺历史：history[-SHORT_TERM_TURNS * 2:]
+ 当前 user_input
+ 当前第二层上下文模式：plain
+ 学科 tool_selection 策略
   - MATH_TOOL_SELECTION_POLICY
   - POLITICS_TOOL_SELECTION_POLICY
   - GENERIC_TOOL_SELECTION_POLICY
+ DEFAULT_ANSWER_SHAPE_POLICY
```

### 独立问题 / independent

独立问题同样走 `build_tool_selection_messages()`，但 `use_independent_context=True`。

组成：

```text
MAIN_SYSTEM_PROMPT
+ CONTEXT_FOLLOWUP_PROMPT（仅 ENABLE_CONTEXT_FOLLOWUP_TOOLS=1 时）
+ format_hint
+ 不带平铺短期历史
+ 可选 independent 参考片段：
   - 最近 INDEPENDENT_CONTEXT_LOOKBACK 轮
   - 同学科
   - 关键词匹配
   - 最多 INDEPENDENT_CONTEXT_MAX_TURNS 轮
   - 明确提示不要把当前问题强行挂到历史
+ 当前 user_input
+ 当前第二层上下文模式：independent
+ 学科 tool_selection 策略
+ DEFAULT_ANSWER_SHAPE_POLICY
```

### 步骤追问 / step_followup

步骤追问不走 DAG。它进入普通 `build_tool_selection_messages()`，所以第二层模式通常是 `plain`。

组成：

```text
MAIN_SYSTEM_PROMPT
+ CONTEXT_FOLLOWUP_PROMPT
+ format_hint
+ 最近短期平铺历史
+ 当前 user_input
+ 当前第二层上下文模式：plain
+ 学科 tool_selection 策略
+ DEFAULT_ANSWER_SHAPE_POLICY
```

第二层通常应选择 `explain_math_step`，而不是直接完整重做整题。

### 非步骤追问 / DAG

非步骤追问在有 parent 时进入 `build_dag_tool_selection_messages()`。

组成：

```text
MAIN_SYSTEM_PROMPT
+ CONTEXT_FOLLOWUP_PROMPT
+ DAG 专属规则：
   - 当前轮已经定位到 DAG 追问链路
   - DAG 链路记忆替代最近 15 轮平铺历史
   - 回答或调用工具只能沿链路继承对象、参数、条件、阶数和上一轮结论
   - 不虚构链路外历史
   - 调工具时必须在 tool arguments 中写出继承后的完整问题和必要上下文
   - 指代不明时直接澄清
+ format_hint
+ 当前第二层上下文模式：dag
+ 学科 tool_selection 策略
+ DEFAULT_ANSWER_SHAPE_POLICY
+ user message:
   - DAG 追问链路记忆
   - root_context
   - 当前 user_input
```

## Prompt 职责边界

为避免重复和冲突，保持以下职责边界：

- `MAIN_SYSTEM_PROMPT`：定义助手身份、总体工作方式。
- `CONTEXT_FOLLOWUP_PROMPT`：定义追问和上下文继承的通用规则。
- `MATH_TOOL_SELECTION_POLICY`：定义数学场景何时直答、何时调用数学工具。
- `POLITICS_TOOL_SELECTION_POLICY`：定义政治场景何时查知识库、何时查时政、何时组合工具。
- `GENERIC_TOOL_SELECTION_POLICY`：定义未知或其他学科的通用工具选择边界。
- `DEFAULT_ANSWER_SHAPE_POLICY`：统一控制直答或工具后总结的回答形态，目标是“最小充分回答”。
- `build_dag_tool_selection_messages()` 中的 DAG 专属文字：只保留 DAG 链路继承、parent、工具参数补全和澄清规则，不再重复写通用长度控制。

## DEFAULT_ANSWER_SHAPE_POLICY 的影响范围

会影响：

- 第二层 LLM 不调用工具时的直接回答。
- 工具调用后，如果工具不是 `return_mode="direct"`，再由 LLM 组织最终回答的场景。

不会直接影响：

- `return_mode="direct"` 的工具直返结果，例如完整数学真题解析。
- 工具内部 prompt，例如 `solve_with_qwenmath()`、`solve_general_math_with_qwenmath()`。

这样可以让普通概念题、追问和建议类问题不啰嗦，同时避免把真题解析、复杂推导、政治分析题答残。
