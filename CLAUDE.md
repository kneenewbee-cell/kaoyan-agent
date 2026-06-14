# 考研智能体助手

考研备考 AI 问答系统。后端基于阿里云 DashScope（Qwen 系列）和 Coze 子智能体，前端提供 CLI 和 Web UI。当前 MVP 阶段：数学一 2009-2025 真题完整，政治 RAG 已构建，DAG 追问链路通过 25 个单元测试。

## 架构

```
用户输入 → classify_subject()（正则 → LLM）→ select_tools() → tool-calling loop（最多 8 轮）
                                                    ↓
                                              [DAG 追问分支]
                              classify_followup_route_with_llm()
                              → parent 确定 → DAG 链路替代 15 轮历史 → LLM 答
                              → ambiguous → LLM 澄清
```

模型分工：Qwen-Max 总控路由，Qwen-Math 解题，Qwen-VL OCR。

## 目录

```
scripts/
├── agent_runtime.py    ← 核心：message loop + DAG + metrics
├── followup.py         ← DAG 追问链路模块
├── config.py           ← 全局配置、路径常量
├── data_loader.py      ← 题库加载、图片处理、OCR
├── prompts.py          ← 所有 Prompt 模板
├── kaoyan_tools.py     ← Tool 封装（12 个工具）
├── politics_tools.py   ← 政治 RAG + Coze 时政
├── web_server.py       ← FastAPI Web UI
├── cli.py              ← CLI 入口
skills/
├── math/SKILL.md       ← 数学子系统
├── politics/SKILL.md   ← 政治子系统
├── followup/SKILL.md   ← DAG 追问管理
└── project/SKILL.md    ← 项目运维与开发约定
data/
├── raw/math/exam_papers/{math1,math2,math3}/{year}/
├── raw/politics/*.md
├── processed/politics_vectors.jsonl
└── runtime/{sessions,sessions_md,logs,code_backups,test_reports}/
tests/
├── test_agent_runtime.py
└── test_conversation_scenarios.py
```

## 开发约定

### 泛化原则
**除非用户明确要求只修当前的 case，否则一律找根因、改底层逻辑，让同类问题一并解决。** 不给单个输入打补丁。

例：用户输入"21年19题怎么做"触发了拒答模板 → 应修复路由层对"缺少 exam_type 的真题请求"的处理，而非只为"21年19题"适配。

### 修改流程
1. **改前**：备份到 `data/runtime/code_backups/`，确认单测全绿
2. **改后**：先单测防退化，再用真实输入验证系统行为是否符合本次修改的目标（单测通过 ≠ 改对了）
3. **DAG 改动**：fake client 单测 → 真实 API 多轮 → 检查分类准确性、parent 判定、回答质量

```powershell
# 防退化
python -m unittest tests.test_agent_runtime tests.test_conversation_scenarios

# 验证行为是否符合目标
python scripts/cli.py "你的测试输入" --debug
```

### 添加新学科
`prompts.py` 加分类规则 → `agent_runtime.py` 加正则匹配 → `select_tools()` 加工具分支 → 创建 tools.py → `kaoyan_tools.py` 注册

### 代码规范
- 无循环导入：config → data_loader/prompts → tools → followup → agent_runtime → cli
- 模块单一职责，路径用 `ROOT` 常量 + `Path` 对象
- 用户错误中文，开发者错误可英文

## 快速启动

```powershell
pip install -r requirements.txt --break-system-packages
cp .env.example .env
python scripts/build_politics_db.py
python scripts/cli.py "2017年数学一第21题解析"
python scripts/cli.py "主要矛盾和矛盾的主要方面有什么区别"
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

## 在 Cowork 中使用

Claude 自动读取 CLAUDE.md，按任务加载对应 skills/*/SKILL.md，参考 `data/runtime/dag_followup_project_status.md` 了解 DAG 进展。
