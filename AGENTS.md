# AGENTS.md

> 项目：考研 Agent 助手  
> 当前优先任务：低风险目录重构 + 新增用户资料整理 / 资料解析模块  
> 适用对象：Codex / 其他 AI coding agent / 维护者  
> 执行要求：先调整文件结构，再新增 materials 模块。每完成一项，把清单 `- [ ]` 改为 `- [x]`，并记录验证结果。

---

## 0. 任务背景

当前项目已经具备问答模块和部分检索能力，但业务核心代码较多集中在 `scripts/`。本轮目标是做一次**低风险、可回滚、不过度设计**的结构整理，并新增独立的用户资料整理模块。

请严格按顺序执行：

1. 先检查现有结构。
2. 再把问答核心脚本迁移到 `qa/`。
3. 修复 import 并验证原功能。
4. 再新增 `materials/`。
5. 实现单文件资料入库 MVP。
6. 最后让问答模块以低耦合方式调用用户资料检索。

不要一开始就大拆数学、政治、runtime。

---

## 1. 全局硬规则

### 1.1 禁止事项

- [ ] 禁止直接删除旧文件；移动文件前确认引用关系。
- [ ] 禁止一次性大拆 `math`、`politics`、`runtime` 子模块。
- [ ] 禁止重写现有问答主流程。
- [ ] 禁止把 MinerU 调用散落到 `qa/` 里。
- [ ] 禁止让 `qa/` 直接 import `materials/parsers/mineru_parser.py`。
- [ ] 禁止删除或破坏 `skills/math/`、`skills/politics/`、`skills/followup/`、`skills/project/`。
- [ ] 禁止删除 `data/raw/`、`data/processed/` 中已有资料。
- [ ] 禁止在本阶段实现复杂 ZIP 批量解析；只预留接口。
- [ ] 禁止丢弃无法识别的图片、图表、公式截图、408 图示。
- [ ] 禁止把密钥、API Key、cookie、个人绝对路径写入仓库。

### 1.2 必须事项

- [x] 每个阶段完成后运行对应验证命令。
- [x] 每次修改 import 后检查入口脚本是否还能启动。
- [ ] 新增资料模块必须保持与 `qa` 低耦合。
- [ ] 用户资料必须按 `user_id/material_id` 隔离。
- [ ] 每份资料必须保存 manifest。
- [ ] 每个 chunk 必须保留来源信息和图片资源路径。
- [ ] 如果实现困难，优先留清晰占位和错误信息，不要静默失败。
- [ ] 如果出现循环导入，优先使用函数内部局部导入解决，不要趁机大改架构。

---

## 2. 目标目录结构

本轮结束后，结构应接近：

```text
python_project/
├── qa/
│   ├── __init__.py
│   ├── agent_runtime.py
│   ├── kaoyan_agent.py
│   ├── kaoyan_tools.py
│   ├── politics_rag.py
│   ├── usage_tracking.py
│   └── web_server.py
│
├── materials/
│   ├── __init__.py
│   ├── service.py
│   ├── schemas.py
│   ├── detector.py
│   ├── resolver.py
│   ├── router.py
│   ├── storage.py
│   ├── search.py
│   ├── tools.py
│   ├── api.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── mineru_parser.py
│   │   ├── docx_parser.py
│   │   ├── image_parser.py
│   │   ├── markdown_parser.py
│   │   ├── text_parser.py
│   │   └── unsupported.py
│   │
│   ├── postprocess/
│   │   ├── __init__.py
│   │   ├── markdown_cleaner.py
│   │   ├── asset_rewriter.py
│   │   ├── formula_cleaner.py
│   │   └── metadata_extractor.py
│   │
│   ├── chunking/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── section_splitter.py
│   │   └── token_counter.py
│   │
│   └── indexing/
│       ├── __init__.py
│       ├── embedding_builder.py
│       └── material_indexer.py
│
├── scripts/
│   ├── ask_kaoyan.py
│   ├── ask_math.py
│   ├── ask_politics.py
│   ├── build_politics_db.py
│   ├── query_politics.py
│   ├── ingest_material.py
│   ├── query_materials.py
│   └── run_web.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── user_materials/
│
├── skills/
│   ├── math/
│   ├── politics/
│   ├── followup/
│   ├── project/
│   └── materials/
│       └── SKILL.md
│
├── tests/
├── web/
├── CLAUDE.md
└── AGENTS.md
```

---

## 3. 技术栈与实现策略

### 3.1 沿用技术

- Python：沿用项目当前版本，优先兼容 Python 3.11+。
- FastAPI：继续使用已有 Web 服务。
- Pydantic：定义资料、parser、chunk、manifest schema。
- pathlib / shutil / hashlib / json：本地文件处理。
- Markdown：作为资料解析中间格式。
- JSONL：保存 chunks、index、debug 数据。
- MinerU：封装为 parser，不直接暴露给问答模块。

### 3.2 MVP 策略

先跑通：

```text
单文件上传/传入路径
↓
识别格式
↓
解析成 Markdown
↓
清洗
↓
保留图片路径
↓
chunk
↓
保存 manifest/chunks
↓
用户资料检索
```

MVP 必须先支持：

- [ ] `.md`
- [ ] `.txt`

MVP 可先占位：

- [ ] `.pdf`
- [ ] `.docx`
- [ ] `.png/.jpg/.jpeg/.webp`

ZIP 本阶段只预留接口：

- [ ] 检测到 zip 时返回明确错误：`ZIP upload is reserved but not implemented yet`

---

## 4. 阶段 0：现状检查

- [x] 运行 `git status`。
- [x] 查看 `scripts/` 下 `.py` 文件。
- [x] 查看现有 `skills/*/SKILL.md`。
- [x] 确认当前可运行入口。
- [x] 确认是否已有 `qa/` 或 `materials/`。
- [x] 如果已有同名文件，先读取，不要盲目覆盖。

建议命令：

```bash
git status
find scripts -maxdepth 1 -type f -name "*.py" | sort
find skills -maxdepth 2 -name "SKILL.md" | sort
find . -maxdepth 2 -type d | sort
```

---

## 5. 阶段 1：创建 qa 包并迁移问答核心

### 5.1 创建 qa

- [x] 创建 `qa/`。
- [x] 创建 `qa/__init__.py`。

### 5.2 移动核心脚本

移动：

- [x] `scripts/agent_runtime.py` → `qa/agent_runtime.py`
- [x] `scripts/kaoyan_agent.py` → `qa/kaoyan_agent.py`
- [x] `scripts/kaoyan_tools.py` → `qa/kaoyan_tools.py`
- [x] `scripts/politics_rag.py` → `qa/politics_rag.py`
- [x] `scripts/usage_tracking.py` → `qa/usage_tracking.py`

可选移动：

- [ ] `scripts/web_server.py` → `qa/web_server.py`

如果移动 Web Server，启动命令改为：

```bash
python -m uvicorn qa.web_server:app --host 127.0.0.1 --port 8000
```

### 5.3 scripts 保留范围

`scripts/` 只保留：

- [x] CLI 入口脚本
- [x] Web 启动脚本
- [x] 构建脚本
- [x] 调试脚本
- [x] 一次性数据处理脚本

---

## 6. 阶段 2：修复 import

### 6.1 scripts 中使用绝对导入

示例：

```python
from qa.agent_runtime import ...
from qa.kaoyan_agent import ...
from qa.kaoyan_tools import ...
from qa.politics_rag import ...
from qa.usage_tracking import ...
```

需要检查：

- [x] `scripts/ask_kaoyan.py`
- [x] `scripts/ask_math.py`
- [x] `scripts/ask_politics.py`
- [x] `scripts/build_politics_db.py`
- [x] `scripts/query_politics.py`
- [ ] `scripts/run_web.py`
- [x] 其他仍留在 scripts 的入口脚本

### 6.2 qa 内部使用相对导入

示例：

```python
from .kaoyan_agent import ...
from .kaoyan_tools import ...
from .politics_rag import ...
from .usage_tracking import ...
```

需要检查：

- [x] `qa/agent_runtime.py`
- [x] `qa/kaoyan_agent.py`
- [x] `qa/kaoyan_tools.py`
- [x] `qa/politics_rag.py`
- [ ] `qa/web_server.py`，如果存在

### 6.3 循环导入处理

如果出现循环导入：

- [ ] 优先把 import 移入函数内部。
- [ ] 不要大拆模块。
- [ ] 只在必要时抽出最小公共 schema/常量。

---

## 7. 阶段 3：验证原有功能

运行：

```bash
python scripts/ask_kaoyan.py
python scripts/ask_math.py
python scripts/ask_politics.py
python scripts/build_politics_db.py
python scripts/query_politics.py
```

Web：

```bash
python -m uvicorn qa.web_server:app --host 127.0.0.1 --port 8000
```

或保留旧入口：

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

完成标准：

- [x] 原有问答入口能启动。
- [x] 原有政治检索/构建能启动。
- [x] 原 Web 服务能启动。
- [x] import 迁移没有破坏主流程。

验证记录（本轮 qa 迁移）：

- `python -m py_compile qa/*.py scripts/ask_*.py scripts/build_politics_db.py scripts/query_politics.py scripts/math_agent.py scripts/web_server.py`：通过。
- `python scripts/ask_kaoyan.py` / `python scripts/ask_math.py`：入口可加载，因未提供必填 `query` 按 argparse usage 退出。
- `python scripts/ask_kaoyan.py 极限是什么 --no-memory --format terminal` / `python scripts/ask_math.py 极限是什么 --no-memory --format terminal`：通过。
- `python scripts/build_politics_db.py`：通过，写入 192 个政治知识块。
- `python scripts/query_politics.py`：入口可加载，因未提供必填 query 按 usage 退出。
- `python scripts/query_politics.py 主要矛盾和矛盾的主要方面有什么区别`：通过。
- `python scripts/ask_politics.py 主要矛盾和矛盾的主要方面有什么区别`：import 与检索通过，最终 Qwen 调用失败，原因是账号免费额度耗尽返回 403。
- `python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000`：应用启动通过，但 8000 端口已被占用；改用高位端口 `18765` 验证 Web 服务可启动。
- `python -m unittest tests.test_agent_runtime`：通过，61 个测试通过，1 个跳过。

---

## 8. 阶段 4：创建 materials 模块骨架

创建：

- [ ] `materials/__init__.py`
- [ ] `materials/schemas.py`
- [ ] `materials/service.py`
- [ ] `materials/detector.py`
- [ ] `materials/resolver.py`
- [ ] `materials/router.py`
- [ ] `materials/storage.py`
- [ ] `materials/search.py`
- [ ] `materials/tools.py`
- [ ] `materials/api.py`

创建子目录：

- [ ] `materials/parsers/__init__.py`
- [ ] `materials/parsers/base.py`
- [ ] `materials/parsers/markdown_parser.py`
- [ ] `materials/parsers/text_parser.py`
- [ ] `materials/parsers/mineru_parser.py`
- [ ] `materials/parsers/docx_parser.py`
- [ ] `materials/parsers/image_parser.py`
- [ ] `materials/parsers/unsupported.py`

- [ ] `materials/postprocess/__init__.py`
- [ ] `materials/postprocess/markdown_cleaner.py`
- [ ] `materials/postprocess/asset_rewriter.py`
- [ ] `materials/postprocess/formula_cleaner.py`
- [ ] `materials/postprocess/metadata_extractor.py`

- [ ] `materials/chunking/__init__.py`
- [ ] `materials/chunking/chunker.py`
- [ ] `materials/chunking/section_splitter.py`
- [ ] `materials/chunking/token_counter.py`

- [ ] `materials/indexing/__init__.py`
- [ ] `materials/indexing/embedding_builder.py`
- [ ] `materials/indexing/material_indexer.py`

---

## 9. 阶段 5：创建 materials skill

如果不存在，创建：

```text
skills/materials/SKILL.md
```

内容至少包含：

- [ ] 用户资料必须按 `data/user_materials/{user_id}/{material_id}/` 存储。
- [ ] 图片资源不能丢。
- [ ] Parser 与 QA 解耦。
- [ ] ZIP 预留但本阶段不实现。
- [ ] Chunk 必须保留来源和 `asset_paths`。
- [ ] Search 必须用户隔离。

---

## 10. 阶段 6：实现资料存储结构

推荐结构：

```text
data/user_materials/
└── {user_id}/
    └── {material_id}/
        ├── original/
        │   └── source.{ext}
        ├── parsed/
        │   ├── content.md
        │   ├── content.json
        │   └── layout.json
        ├── assets/
        │   └── images/
        ├── chunks/
        │   ├── chunks.jsonl
        │   └── chunks_debug.md
        ├── index/
        │   ├── embeddings.jsonl
        │   └── search_index.json
        └── manifest.json
```

实现：

- [ ] `create_material_dir`
- [ ] `save_original`
- [ ] `save_markdown`
- [ ] `save_json`
- [ ] `save_asset_image`
- [ ] `save_chunks_jsonl`
- [ ] `save_manifest`
- [ ] `load_manifest`

---

## 11. 阶段 7：实现格式识别和 parser 路由

### 11.1 detector

- [ ] 识别扩展名。
- [ ] 识别 mime type。
- [ ] 计算 sha256。
- [ ] 输出统一 `DetectedFile`。

### 11.2 resolver

- [ ] 当前只支持单文件。
- [ ] zip 返回明确未实现错误。
- [ ] 目录返回明确未实现错误。
- [ ] 预留未来扩展接口。

### 11.3 router

- [ ] `.md` → MarkdownParser
- [ ] `.txt` → TextParser
- [ ] `.pdf` → MinerUParser
- [ ] 图片 → ImageParser 或 MinerUParser
- [ ] `.docx` → DocxParser
- [ ] 其他 → UnsupportedParser

---

## 12. 阶段 8：实现 parser MVP

### 12.1 Base Parser

- [ ] 定义 `BaseMaterialParser`。
- [ ] 定义 `ParseResult`。
- [ ] 定义 `ParsedAsset`。
- [ ] 统一 `parse(...)` 接口。

### 12.2 MarkdownParser

- [ ] 读取 `.md`。
- [ ] 保存 `parsed/content.md`。
- [ ] 保留图片引用。
- [ ] 返回 ParseResult。

### 12.3 TextParser

- [ ] 读取 `.txt`。
- [ ] 转成 Markdown。
- [ ] 保存 `parsed/content.md`。
- [ ] 返回 ParseResult。

### 12.4 MinerUParser

- [ ] 封装 MinerU CLI/API。
- [ ] 不可用时返回明确错误。
- [ ] 输出进入当前 material 目录。
- [ ] 保留图片、layout/json、表格等资源。

### 12.5 占位 parser

- [ ] DocxParser 可先占位。
- [ ] ImageParser 可先占位。
- [ ] UnsupportedParser 返回明确错误。

---

## 13. 阶段 9：后处理与图片保留

### 13.1 markdown cleaner

- [ ] 清理多余空行。
- [ ] 清理轻量噪声。
- [ ] 不破坏公式。
- [ ] 不删除图片引用。

### 13.2 asset rewriter

- [ ] 重写 Markdown 图片路径。
- [ ] 图片保存到 `assets/images/`。
- [ ] 无法识别文字的图片也保留。
- [ ] chunk 中保留 `asset_paths`。

图片占位建议：

```md
![第 23 页图 1：原文图片，OCR 未识别，已保留原图](../assets/images/page_023_img_001.png)
```

### 13.3 408 / 数学资料规则

- [ ] 结构图不能丢。
- [ ] 表格图不能丢。
- [ ] 流程图不能丢。
- [ ] 树图、Cache 图、页表图不能丢。
- [ ] 公式截图不能丢。

---

## 14. 阶段 10：chunk、index、search

### 14.1 chunk

- [ ] 按标题优先切分。
- [ ] 超长 section 按段落切分。
- [ ] 保留 heading path。
- [ ] 保留 page no，如果有。
- [ ] 保留 asset paths。
- [ ] 写入 `chunks/chunks.jsonl`。
- [ ] 写入 `chunks/chunks_debug.md`。

### 14.2 index

- [ ] 读取 chunks。
- [ ] 生成 search index。
- [ ] 预留 embedding。
- [ ] 可先使用 mock/local hash。

### 14.3 search

- [ ] 实现 `search_user_materials(user_id, query, top_k=5, filters=None)`。
- [ ] 只搜索当前 user_id。
- [ ] 返回 chunk text、metadata、source、asset_paths。
- [ ] 支持按 material_id、subject、material_type 过滤。

---

## 15. 阶段 11：新增调试脚本

### 15.1 ingest_material.py

新增：

```bash
python scripts/ingest_material.py --user-id test_user --file path/to/demo.md
```

要求：

- [ ] 调用 `materials.service.MaterialIngestionService`。
- [ ] 打印 material_id。
- [ ] 打印 parse status。
- [ ] 打印 markdown path。
- [ ] 打印 chunk count。
- [ ] 失败时打印错误。

### 15.2 query_materials.py

新增：

```bash
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
```

要求：

- [ ] 调用 `materials.search.search_user_materials`。
- [ ] 打印 top_k 结果。
- [ ] 打印来源 material_id、chunk_id、asset_paths。

---

## 16. 阶段 12：接入 qa

只允许 qa 调用检索接口：

允许：

```python
from materials.search import search_user_materials
```

或：

```python
from materials.tools import search_user_materials_tool
```

禁止：

```python
from materials.parsers.mineru_parser import MinerUParser
```

需要完成：

- [ ] 在问答工具注册处新增用户资料检索工具。
- [ ] 工具入参包含 `user_id`、`query`、`top_k`、可选 filters。
- [ ] 当用户明确说“根据我上传的资料/我的资料库”时，优先检索用户资料库。
- [ ] 用户未要求时，不默认强行检索用户资料库。
- [ ] 回答时保留资料来源信息。

---

## 17. 验收命令

至少运行：

```bash
python scripts/ingest_material.py --user-id test_user --file data/demo/test.md
python scripts/ingest_material.py --user-id test_user --file data/demo/test.txt
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
python scripts/ask_kaoyan.py
python scripts/ask_math.py
python scripts/ask_politics.py
```

Web：

```bash
python -m uvicorn qa.web_server:app --host 127.0.0.1 --port 8000
```

验收：

- [ ] `.md` 入库成功。
- [ ] `.txt` 入库成功。
- [ ] unsupported 格式有明确错误。
- [ ] zip 有“预留但未实现”的明确错误。
- [ ] manifest 生成。
- [ ] chunks 生成。
- [ ] 图片引用不会被 cleaner 删除。
- [ ] 用户资料检索不跨用户。
- [ ] 原有问答入口仍可用。
- [ ] Web 服务仍可启动。

---

## 18. 完成汇报要求

每次任务结束必须汇报：

- [ ] 移动了哪些文件。
- [ ] 修改了哪些 import。
- [ ] 新增了哪些 materials 文件。
- [ ] 哪些 parser 已实现。
- [ ] 哪些 parser 是占位。
- [ ] 运行了哪些验证命令。
- [ ] 哪些命令失败。
- [ ] 失败原因和下一步建议。
- [ ] 已勾选哪些任务，未完成哪些任务。

---

## 19. 最终总清单

- [x] 已完成现状检查。
- [x] 已创建 `qa/` 包。
- [x] 已迁移问答核心脚本。
- [x] 已修复 scripts import。
- [x] 已修复 qa 内部 import。
- [x] 已验证原问答入口。
- [ ] 已创建 `materials/` 模块。
- [ ] 已创建 `skills/materials/SKILL.md`。
- [ ] 已实现 storage。
- [ ] 已实现 detector。
- [ ] 已实现 resolver。
- [ ] 已实现 router。
- [ ] 已实现 MarkdownParser。
- [ ] 已实现 TextParser。
- [ ] 已封装 MinerUParser 接口。
- [ ] 已实现 cleaner。
- [ ] 已实现 asset rewriter。
- [ ] 已实现 chunker。
- [ ] 已实现 index/search MVP。
- [ ] 已新增 ingest/query 脚本。
- [ ] 已接入 qa 用户资料检索工具。
- [ ] 已完成最小验收。
- [ ] 已向用户汇报结果。
