非步骤追问规则：
- “那如果...呢”“换成...还成立吗”“第一个/第二个题的余项”“总结一下”“改得更简洁”等不是步骤追问时，不要硬切到 explain_math_step。
- 这类问题应优先使用 answer_math_followup / summarize_math_solution / rewrite_math_answer；answer_math_followup 会由 runtime 根据最近 $FOLLOWUP_DAG_LOOKBACK 个 turn 的 DAG 溯源结果补齐 root_context 与 followup_context。
- 当前轮显式给出的参数覆盖历史参数；没有显式修改的函数、展开点、目标点、阶数、误差要求应从历史继承。
- 执行性很弱的非步骤追问（例如“这个呢”“为什么成立”“继续”“那如果换成...”）默认先指向上一轮；如果历史中存在多个可能 root，且最近 $FOLLOWUP_DAG_LOOKBACK 轮仍不足以定位，先请用户澄清。
