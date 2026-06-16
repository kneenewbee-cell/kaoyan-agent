# 版本记录

## 2026-06-16 - DAG 路由与上下文改进

版本标签：`dag-route-v2026.06.16`

这一版延续 `e49df26` 之后的 DAG 追问路由优化，重点是减少误挂父节点、改善独立问题上下文、统一政治/时政路由，并留下可复查的调试与测试痕迹。

### 改进内容

- 将时政统一归入 `politics` 学科，不再把 `current_affairs` 当作独立学科；政治请求现在同时具备政治 RAG 工具和 Coze 时政工具。
- 增加复合追问识别，例如“讲一下某方法，刚才那题能用吗”，会判为上下文追问，而不是误判成独立新问题。
- 给 DAG 追问最终回答增加简洁输出约束：默认控制在约 900 个汉字内，同时提高 `max_tokens`，避免回答中途截断。
- 独立问题不再回退到最近平铺历史，而是只注入最近同学科且关键词匹配的参考片段。
- 新增 `ROUTE_DEBUG_LOG` 调试开关，可记录路由模型原始输出、解析 JSON、解析错误和输出长度。
- 补充 fake-client 回归测试，覆盖本轮路由、上下文选择和 prompt 约束行为。

### 验证

```powershell
python -m unittest tests.test_agent_runtime tests.test_conversation_scenarios
```

结果：

```text
Ran 47 tests
OK (skipped=1)
```
