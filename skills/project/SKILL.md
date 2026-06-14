---
name: project
description: 项目运维——开发流程、测试策略、架构决策、代码规范。修改代码或了解项目约定时使用。
---

# Project Skill

## 核心原则

### 泛化原则
**除非用户明确要求只修当前的 case，否则一律找根因、改底层逻辑，让同类问题一并解决。** 不为单个输入打补丁。详见 CLAUDE.md"开发约定"段。

## 修改流程

### 改前
1. 备份到 `data/runtime/code_backups/{filename}.{timestamp}.py`
2. `python -m unittest tests.test_agent_runtime tests.test_conversation_scenarios` 确认基线全绿

### 改中
- 运行时改动：用 `.env` flag + `env_flag()` 控制
- 新增 Tool：Pydantic args_schema → 实现 → 注册到 build_*_tools() → select_tools()
- 改 Prompt：集中在 `prompts.py`，改后跑真实 API 验证

### 改后
1. 单测防退化
2. 用真实输入验证行为是否符合本次修改的目标（**这才是真正的验证**）
3. DAG：真实 API 多轮 → 检查分类、parent、回答质量
4. 更新相关 SKILL.md 和 `dag_followup_project_status.md`

## 测试策略
- 单元测试：fake client，防逻辑退化
- 场景测试：JSON 多轮模拟，验证分类和链路
- 真实 API：`--debug` CLI，验证系统行为符合预期

## 代码规范
- 无循环导入：config → data_loader/prompts → tools → followup → agent_runtime → cli/web
- 模块单一职责，路径用 `ROOT` 常量 + `Path`
- 用户错误中文，开发者错误可英文

## 架构决策
- 不用 LangChain/LangGraph（自主 tool-calling loop）
- followup.py 分离（独立测试，不必 mock 整个 runtime）
- 双份会话存储（Markdown 人读 + JSON 机读）
- 实验开关用 .env（不改代码即可 A/B 对比）
