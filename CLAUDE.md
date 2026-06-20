# CLAUDE.md

> 项目：考研 Agent 助手  
> 当前优先任务：低风险目录重构 + 新增用户资料整理 / 资料解析模块  
> 适用对象：Claude Code / 维护者  
> 执行要求：先调整文件结构，再新增 materials 模块。每完成一项，把清单 `- [ ]` 改为 `- [x]`，并记录验证结果。

---

## 0. 项目当前阶段判断

本项目当前处于 MVP 到模块化过渡阶段。已有问答模块和部分检索能力，但核心业务代码较多集中在 `scripts/` 下。

本轮任务不是“大重构”，而是一次**低风险结构整理**：

1. 先让 `scripts/` 回归入口层，只保留启动脚本、调试脚本、一次性脚本。
2. 将当前问答核心业务整体迁移到根目录同级 `qa/`。
3. 新增根目录同级 `materials/`，作为用户资料整理 / 资料解析 / 资料入库模块。
4. 暂时不要把数学、政治、runtime 再拆成独立大模块。
5. 后续问答模块只调用用户资料检索接口，不直接关心 MinerU 或 OCR 细节。

---

## 1. 硬性原则

### 1.1 禁止事项

- [ ] 不要一次性大拆数学、政治、runtime 子模块。
- [ ] 不要重写现有问答主流程。
- [ ] 不要把 MinerU 直接塞进 `qa/agent_runtime.py`、`qa/kaoyan_agent.py` 或 Web 主逻辑。
- [ ] 不要让 `qa/` 直接 import `materials/parsers/mineru_parser.py`。
- [ ] 不要删除现有 `skills/math/`、`skills/politics/`、`skills/followup/`、`skills/project/`。
- [ ] 不要删除 `data/raw/`、`data/processed/` 中已有资料。
- [ ] 不要在本阶段实现 ZIP 批量解析，但必须预留 ZIP / 目录解析接口。
- [ ] 不要丢弃 PDF、图片、数学图、408 图、表格图等无法 OCR 的资源。
- [ ] 不要把真实 API Key、密钥、cookie、个人路径写入代码或文档。

### 1.2 必须遵守

- [ ] 先读现有项目结构，再修改。
- [ ] 先移动文件和修复 import，再新增大功能。
- [ ] 每次迁移后运行最小验证命令。
- [ ] 保持原有入口尽量可用。
- [ ] 新增模块必须有清晰边界和低耦合接口。
- [ ] 资料解析结果必须保留原文件、Markdown、JSON、图片资源、chunks、manifest。
- [ ] 用户资料必须按 `user_id/material_id` 隔离保存。
- [ ] 涉及资料整理模块时，必须同时遵守 `skills/materials/SKILL.md`；如果该文件不存在，先创建。

---

## 2. 推荐目标结构

本轮完成后，项目结构应接近：

```text
python_project/
├── qa/                                  # 当前问答核心模块，先整体收进去
│   ├── __init__.py
│   ├── agent_runtime.py                 # 原 scripts/agent_runtime.py
│   ├── kaoyan_agent.py                  # 原 scripts/kaoyan_agent.py
│   ├── kaoyan_tools.py                  # 原 scripts/kaoyan_tools.py
│   ├── politics_rag.py                  # 原 scripts/politics_rag.py
│   ├── usage_tracking.py                # 原 scripts/usage_tracking.py
│   └── web_server.py                    # 原 scripts/web_server.py，可选移动
│
├── materials/                           # 新增：资料整理 / 资料解析 / 资料入库模块
│   ├── __init__.py
│   ├── service.py                       # 资料入库主流程
│   ├── schemas.py                       # Material、ParseResult、Chunk 等 schema
│   ├── detector.py                      # 文件类型识别
│   ├── resolver.py                      # 单文件 / 未来 ZIP / 目录解析入口
│   ├── router.py                        # parser 路由
│   ├── storage.py                       # 原文件、md、json、图片、chunk 保存
│   ├── api.py                           # 可选：资料上传/查询 API router
│   ├── search.py                        # 用户资料检索接口
│   ├── tools.py                         # 暴露给 qa 的工具函数
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py                      # BaseMaterialParser / ParseResult
│   │   ├── mineru_parser.py             # PDF/图片/复杂文档，封装 MinerU CLI/API
│   │   ├── docx_parser.py               # DOCX parser，可先占位
│   │   ├── image_parser.py              # 图片 parser，可先占位或走 MinerU
│   │   ├── markdown_parser.py           # MD 直读 parser
│   │   ├── text_parser.py               # TXT 直读 parser
│   │   └── unsupported.py               # 不支持格式的明确错误
│   │
│   ├── postprocess/
│   │   ├── __init__.py
│   │   ├── markdown_cleaner.py          # 清洗页眉页脚、空行、噪声
│   │   ├── asset_rewriter.py            # 重写图片路径、保存图片引用
│   │   ├── formula_cleaner.py           # 公式文本轻度修复
│   │   └── metadata_extractor.py        # 提取标题、学科、资料类型等元数据
│   │
│   ├── chunking/
│   │   ├── __init__.py
│   │   ├── chunker.py                   # Markdown chunk 切分
│   │   ├── section_splitter.py          # 按标题切分
│   │   └── token_counter.py             # token 估算
│   │
│   └── indexing/
│       ├── __init__.py
│       ├── embedding_builder.py         # embedding 构建，可先 mock/local hash
│       └── material_indexer.py          # chunks 写入索引
│
├── scripts/                             # 只保留入口/调试/一次性脚本
│   ├── ask_kaoyan.py
│   ├── ask_math.py
│   ├── ask_politics.py
│   ├── build_politics_db.py
│   ├── query_politics.py
│   ├── ingest_material.py               # 调试入口，调用 materials.service
│   └── run_web.py                       # 可选入口
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

## 3. 技术栈

### 3.1 当前优先采用

- Python：沿用项目当前版本，优先兼容 Python 3.11+。
- FastAPI：沿用现有 Web 服务。
- Pydantic：用于请求、解析结果、manifest、chunk schema。
- pathlib / shutil / hashlib / json / mimetypes：文件存储、hash、格式识别。
- Markdown：作为资料解析后的 LLM/RAG 友好中间格式。
- JSON / JSONL：保存 manifest、chunks、embedding/debug index。
- MinerU：作为 PDF、图片、复杂版面文档的主 parser 封装对象。
- 现有 embedding / RAG 能力：优先复用，不强行引入新向量库。

### 3.2 MVP 可先简化

- `.md`、`.txt`：必须先实现直读入库，跑通链路。
- `.pdf`、`.docx`、图片：先实现 parser 接口和清晰错误；有 MinerU 环境时再调用。
- embedding：可先 mock/local hash 或复用现有 embedding。
- 检索：可先用 JSONL + 简单关键词/BM25-like 检索，后续再接 FAISS / Chroma / Qdrant / pgvector。
- ZIP：本阶段只预留 resolver 接口，不实现批量解析。

### 3.3 后续增强方向

- MinerU CLI/API 双模式。
- OCR / Qwen-VL 对未识别图片生成 caption。
- 表格结构化保存为 Markdown table / HTML / JSON。
- 用户资料删除、重解析、版本管理。
- 多资料联合检索和答案引用来源。

---

## 4. 执行计划总览

按顺序执行，不要跳阶段。

- [ ] 阶段 0：备份与现状检查
- [ ] 阶段 1：低风险调整文件结构，创建 `qa/`
- [ ] 阶段 2：修复 import 和入口脚本
- [ ] 阶段 3：验证原有问答功能
- [ ] 阶段 4：新增 `materials/` 骨架
- [ ] 阶段 5：实现用户资料存储结构
- [ ] 阶段 6：实现文件识别、resolver、parser router
- [ ] 阶段 7：实现 parser MVP
- [ ] 阶段 8：实现 Markdown 后处理和图片资源保留
- [ ] 阶段 9：实现 chunk 切分
- [ ] 阶段 10：实现 indexing / search MVP
- [ ] 阶段 11：新增脚本和可选 API
- [ ] 阶段 12：让 qa 以低耦合方式接入用户资料检索
- [ ] 阶段 13：测试、文档、验收

---

## 5. 阶段 0：备份与现状检查

目标：先确认现有结构，避免盲改。

- [ ] 查看项目根目录结构。
- [ ] 查看 `scripts/` 下所有 `.py` 文件职责。
- [ ] 查看现有 `CLAUDE.md`、`AGENTS.md`、`skills/*/SKILL.md`。
- [ ] 记录当前可运行命令。
- [ ] 如果是 Git 项目，确认工作区状态。
- [ ] 不要删除旧文件；移动前确保能回滚。

建议命令：

```bash
git status
find scripts -maxdepth 1 -type f -name "*.py" | sort
find skills -maxdepth 2 -name "SKILL.md" | sort
```

完成标准：

- [ ] 明确哪些脚本是业务核心，哪些是入口脚本。
- [ ] 明确迁移范围。
- [ ] 没有开始写 materials 代码之前，先完成结构迁移准备。

---

## 6. 阶段 1：创建 qa 包并移动问答核心脚本

目标：让 `scripts/` 回归入口层。

### 6.1 创建目录

- [ ] 新建 `qa/`。
- [ ] 新建 `qa/__init__.py`。

### 6.2 移动文件

将以下文件从 `scripts/` 移动到 `qa/`：

- [ ] `scripts/agent_runtime.py` → `qa/agent_runtime.py`
- [ ] `scripts/kaoyan_agent.py` → `qa/kaoyan_agent.py`
- [ ] `scripts/kaoyan_tools.py` → `qa/kaoyan_tools.py`
- [ ] `scripts/politics_rag.py` → `qa/politics_rag.py`
- [ ] `scripts/usage_tracking.py` → `qa/usage_tracking.py`

可选：

- [ ] 如果 `scripts/web_server.py` 包含大量 FastAPI 路由逻辑，将其移动为 `qa/web_server.py`。
- [ ] 如果暂不移动 `web_server.py`，必须修复其 import，让它从 `qa` 导入业务代码。

### 6.3 scripts 保留范围

`scripts/` 只保留：

- [ ] `ask_kaoyan.py`
- [ ] `ask_math.py`
- [ ] `ask_politics.py`
- [ ] `build_politics_db.py`
- [ ] `query_politics.py`
- [ ] `run_web.py`，如果需要
- [ ] `ingest_material.py`，后续新增
- [ ] 一次性数据处理脚本

---

## 7. 阶段 2：修复 import

### 7.1 scripts 中的导入

`scripts/` 下入口脚本统一使用绝对导入：

```python
from qa.agent_runtime import ...
from qa.kaoyan_agent import ...
from qa.kaoyan_tools import ...
from qa.politics_rag import ...
from qa.usage_tracking import ...
```

- [ ] 修改 `scripts/ask_kaoyan.py`。
- [ ] 修改 `scripts/ask_math.py`。
- [ ] 修改 `scripts/ask_politics.py`。
- [ ] 修改 `scripts/build_politics_db.py`。
- [ ] 修改 `scripts/query_politics.py`。
- [ ] 修改 Web 启动脚本或 `web_server.py`。

### 7.2 qa 内部导入

`qa/` 内部模块优先使用相对导入：

```python
from .kaoyan_agent import ...
from .kaoyan_tools import ...
from .politics_rag import ...
from .usage_tracking import ...
```

- [ ] 修复 `qa/agent_runtime.py`。
- [ ] 修复 `qa/kaoyan_agent.py`。
- [ ] 修复 `qa/kaoyan_tools.py`。
- [ ] 修复 `qa/politics_rag.py`。
- [ ] 修复 `qa/web_server.py`，如果存在。

### 7.3 循环导入处理规则

如果出现 `ImportError: cannot import name ... from partially initialized module`：

- [ ] 不要大改业务。
- [ ] 优先将少量 import 改到函数内部。
- [ ] 必要时只抽出最小公共 schema / 常量。
- [ ] 不要借机拆出 `math/`、`politics/`、`runtime/` 大模块。

---

## 8. 阶段 3：验证原有功能

必须尽量验证原有入口仍可用。

- [ ] `python scripts/ask_kaoyan.py`
- [ ] `python scripts/ask_math.py`
- [ ] `python scripts/ask_politics.py`
- [ ] `python scripts/build_politics_db.py`
- [ ] `python scripts/query_politics.py`

Web 验证二选一：

```bash
python -m uvicorn qa.web_server:app --host 127.0.0.1 --port 8000
```

或：

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

完成标准：

- [ ] 原有问答功能能启动。
- [ ] 政治检索/构建脚本能启动。
- [ ] 没有因为路径迁移导致主流程崩溃。
- [ ] `scripts/` 已基本回归入口层。

---

## 9. 阶段 4：新增 materials 模块骨架

目标：先创建清晰模块，不急着实现所有 parser。

- [ ] 新建 `materials/`。
- [ ] 新建 `materials/__init__.py`。
- [ ] 新建 `materials/schemas.py`。
- [ ] 新建 `materials/service.py`。
- [ ] 新建 `materials/detector.py`。
- [ ] 新建 `materials/resolver.py`。
- [ ] 新建 `materials/router.py`。
- [ ] 新建 `materials/storage.py`。
- [ ] 新建 `materials/search.py`。
- [ ] 新建 `materials/tools.py`。
- [ ] 新建 `materials/api.py`，如果需要接 FastAPI。

子目录：

- [ ] 新建 `materials/parsers/` 和 `__init__.py`。
- [ ] 新建 `materials/postprocess/` 和 `__init__.py`。
- [ ] 新建 `materials/chunking/` 和 `__init__.py`。
- [ ] 新建 `materials/indexing/` 和 `__init__.py`。

---

## 10. 阶段 5：用户资料存储结构

目标：不要使用全局散落结构，而是按用户和资料聚合。

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
        │       ├── page_001_img_001.png
        │       └── page_008_diagram_002.png
        ├── chunks/
        │   ├── chunks.jsonl
        │   └── chunks_debug.md
        ├── index/
        │   ├── embeddings.jsonl
        │   └── search_index.json
        └── manifest.json
```

必须实现：

- [ ] `MaterialStorage.create_material_dir(user_id, material_id)`。
- [ ] `MaterialStorage.save_original(...)`。
- [ ] `MaterialStorage.save_markdown(...)`。
- [ ] `MaterialStorage.save_json(...)`。
- [ ] `MaterialStorage.save_asset_image(...)`。
- [ ] `MaterialStorage.save_chunks_jsonl(...)`。
- [ ] `MaterialStorage.save_manifest(...)`。
- [ ] `MaterialStorage.load_manifest(...)`。

manifest 至少包含：

```json
{
  "material_id": "string",
  "user_id": "string",
  "original_filename": "string",
  "file_ext": ".pdf",
  "mime_type": "application/pdf",
  "sha256": "string",
  "subject": "math|politics|408|english|unknown",
  "course": "string|null",
  "material_type": "lecture|note|exam|wrong_book|school_info|unknown",
  "parser_name": "mineru|markdown|text|docx|image|unsupported",
  "parse_status": "pending|processing|ready|failed",
  "paths": {
    "original": "string",
    "markdown": "string|null",
    "json": "string|null",
    "chunks": "string|null"
  },
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime",
  "error": null
}
```

---

## 11. 阶段 6：文件识别、resolver、parser router

### 11.1 detector

`materials/detector.py` 必须实现：

- [ ] 根据扩展名识别：`.pdf`、`.docx`、`.md`、`.txt`、`.png`、`.jpg`、`.jpeg`、`.webp`。
- [ ] 计算 sha256。
- [ ] 返回 mime type。
- [ ] 对未知格式返回明确 unsupported。

### 11.2 resolver

`materials/resolver.py` 必须实现：

- [ ] `resolve_upload_path(path) -> list[ResolvedUploadItem]`。
- [ ] 当前只支持单文件。
- [ ] 如果是 zip，返回明确错误：`ZIP upload is reserved but not implemented yet`。
- [ ] 为未来 zip/目录预留接口，不要把单文件逻辑写死在 service 里。

### 11.3 router

`materials/router.py` 必须实现：

- [ ] `.md` → `MarkdownParser`
- [ ] `.txt` → `TextParser`
- [ ] `.pdf` → `MinerUParser`，如果配置启用；否则返回清晰错误或占位结果
- [ ] 图片 → `ImageParser` 或 `MinerUParser`
- [ ] `.docx` → `DocxParser`，可先占位
- [ ] unsupported → `UnsupportedParser`

---

## 12. 阶段 7：parser MVP

### 12.1 base parser

`materials/parsers/base.py` 定义：

- [ ] `BaseMaterialParser`
- [ ] `ParseResult`
- [ ] `ParsedAsset`
- [ ] 统一 parser 接口：`parse(input_path, output_dir, context) -> ParseResult`

### 12.2 MarkdownParser

- [ ] 读取 `.md`。
- [ ] 输出 `content.md`。
- [ ] 保留原始图片引用。
- [ ] 返回 ParseResult。

### 12.3 TextParser

- [ ] 读取 `.txt`。
- [ ] 转为简单 Markdown。
- [ ] 返回 ParseResult。

### 12.4 MinerUParser

- [ ] 封装 MinerU，不要把命令行调用散落在其他模块。
- [ ] 支持 CLI 配置项，例如 `MINERU_ENABLED`、`MINERU_BIN`。
- [ ] 如果 MinerU 不可用，返回清晰错误，不要静默失败。
- [ ] 解析输出应进入该 material 的 `parsed/` 与 `assets/`。
- [ ] 保留 MinerU 生成的图片、表格、layout/json 信息。

### 12.5 ImageParser / DocxParser

MVP 可先占位：

- [ ] 如果实现困难，给出明确 `NotImplementedError` 或 failed status。
- [ ] 不要影响 `.md` / `.txt` 入库主链路。

---

## 13. 阶段 8：后处理与图片资源保留

资料解析后必须进入 postprocess，而不是直接 chunk。

### 13.1 markdown_cleaner

- [ ] 清理多余空行。
- [ ] 清理明显重复页眉页脚，可先做轻量规则。
- [ ] 不要破坏数学公式。
- [ ] 不要删除图片引用。
- [ ] 不要强行改写所有表格。

### 13.2 asset_rewriter

- [ ] 将 Markdown 中的图片路径改写为 material 内相对路径。
- [ ] 将图片资源复制或移动到 `assets/images/`。
- [ ] 为无法识别的图保留占位说明。
- [ ] 图片引用格式建议：

```md
![第 23 页图 1：原文图片，OCR 未识别，已保留原图](../assets/images/page_023_img_001.png)
```

### 13.3 408 / 数学图处理原则

- [ ] 结构图、流程图、网络图、Cache 图、树图、页表图不能丢。
- [ ] 如果无法转成文字，至少保存图片并在 Markdown 中保留引用。
- [ ] chunk 中必须保留相关图片路径。
- [ ] 后续可再用 VLM 为图片生成 caption，本阶段只需预留字段。

---

## 14. 阶段 9：chunk 切分

`materials/chunking/chunker.py` 实现：

- [ ] 按 Markdown 标题优先切分。
- [ ] 超长 section 再按段落切分。
- [ ] 保留 `section_title` / `heading_path`。
- [ ] 保留 `page_no`，如果 parser 能提供。
- [ ] 保留 `asset_paths`。
- [ ] 每个 chunk 有稳定 `chunk_id`。
- [ ] 输出 `chunks.jsonl`。
- [ ] 输出 `chunks_debug.md` 方便人工查看。

chunk schema 建议：

```json
{
  "chunk_id": "string",
  "material_id": "string",
  "user_id": "string",
  "chunk_index": 0,
  "text": "string",
  "section_title": "string|null",
  "heading_path": ["string"],
  "page_start": null,
  "page_end": null,
  "asset_paths": ["assets/images/page_001_img_001.png"],
  "token_count": 512,
  "metadata": {}
}
```

---

## 15. 阶段 10：indexing / search MVP

### 15.1 indexing

`materials/indexing/material_indexer.py`：

- [ ] 读取 chunks。
- [ ] 生成本地 search index。
- [ ] 保存到 `index/search_index.json` 或 JSONL。
- [ ] 预留 embedding 接口。

`materials/indexing/embedding_builder.py`：

- [ ] 可先实现 mock/local hash。
- [ ] 如果项目已有 embedding，优先复用。
- [ ] 不要强制引入重型向量库。

### 15.2 search

`materials/search.py`：

- [ ] 实现 `search_user_materials(user_id, query, top_k=5, filters=None)`。
- [ ] 只搜索当前用户目录。
- [ ] 支持 material_id / subject / material_type 过滤。
- [ ] 返回 chunk text、metadata、source path、asset paths。
- [ ] 不允许跨用户检索。

---

## 16. 阶段 11：脚本和 API

### 16.1 scripts/ingest_material.py

新增调试脚本：

```bash
python scripts/ingest_material.py --user-id test_user --file path/to/demo.md
```

要求：

- [ ] 调用 `materials.service.MaterialIngestionService`。
- [ ] 打印 material_id、状态、markdown_path、chunk_count。
- [ ] 失败时打印清晰错误。

### 16.2 scripts/query_materials.py

可选新增：

```bash
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
```

### 16.3 FastAPI

如果接 Web：

- [ ] 新增上传接口：`POST /api/materials/upload`
- [ ] 新增状态接口：`GET /api/materials/{material_id}`
- [ ] 新增检索接口：`GET /api/materials/search`
- [ ] 不要阻塞现有聊天接口。
- [ ] 大文件解析后续应走异步任务；MVP 可同步但要留 TODO。

---

## 17. 阶段 12：qa 接入用户资料检索

原则：`qa` 可以调用 `materials.tools` 或 `materials.search`，但不要直接调用 parser。

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

- [ ] 在 `qa/kaoyan_tools.py` 或工具注册处新增用户资料检索工具。
- [ ] 工具输入包含 `user_id`、`query`、`top_k`、可选 filters。
- [ ] 回答时能把资料来源返回给 LLM。
- [ ] 如果用户没有要求查自己资料，不要默认强行检索用户资料库。
- [ ] 如果用户明确说“根据我上传的资料”，优先检索用户资料库。

---

## 18. 阶段 13：测试与验收

至少新增或手动验证：

- [ ] `.txt` 文件入库成功。
- [ ] `.md` 文件入库成功。
- [ ] unsupported 文件返回明确错误。
- [ ] zip 文件返回“预留但未实现”。
- [ ] chunk 文件生成。
- [ ] manifest 文件生成。
- [ ] 图片引用不会被 cleaner 删除。
- [ ] 用户 A 无法检索用户 B 的资料。
- [ ] 原有问答入口仍可用。
- [ ] Web 服务仍可启动。

建议命令：

```bash
python scripts/ingest_material.py --user-id test_user --file data/demo/test.md
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
python scripts/ask_kaoyan.py
python -m uvicorn qa.web_server:app --host 127.0.0.1 --port 8000
```

---

## 19. 完成后必须输出的总结

每次任务结束时，向用户汇报：

- [ ] 移动了哪些文件。
- [ ] 修改了哪些 import。
- [ ] 新增了哪些 materials 文件。
- [ ] 哪些 parser 已实现，哪些只是占位。
- [ ] 运行了哪些验证命令。
- [ ] 哪些命令失败，失败原因是什么。
- [ ] 下一步建议。

---

## 20. 与 skills 的关系

本文件是项目级任务说明。模块级规范放在 `skills/*/SKILL.md`。

涉及资料整理模块时，必须读取：

```text
skills/materials/SKILL.md
```

如果该文件不存在，创建它，并写入资料整理模块规范，至少包含：

- 用户资料按 `user_id/material_id` 存储。
- 图片资源不能丢。
- parser 与 qa 解耦。
- ZIP 预留但本阶段不实现。
- chunk 必须保留来源和 asset paths。
- search 必须用户隔离。

涉及数学、政治、追问、项目通用规则时，也应尽量遵守已有：

```text
skills/math/SKILL.md
skills/politics/SKILL.md
skills/followup/SKILL.md
skills/project/SKILL.md
```

---

## 21. 任务完成勾选区

总清单：

- [ ] 已完成现状检查。
- [ ] 已创建 `qa/` 包。
- [ ] 已迁移问答核心脚本到 `qa/`。
- [ ] 已修复 scripts 入口 import。
- [ ] 已修复 qa 内部 import。
- [ ] 已验证原有问答入口。
- [ ] 已创建 `materials/` 模块骨架。
- [ ] 已创建 `skills/materials/SKILL.md`。
- [ ] 已实现资料存储结构。
- [ ] 已实现文件识别。
- [ ] 已实现 resolver。
- [ ] 已实现 parser router。
- [ ] 已实现 Markdown/TXT parser。
- [ ] 已封装 MinerU parser 接口。
- [ ] 已实现后处理 cleaner。
- [ ] 已实现图片路径重写与保存。
- [ ] 已实现 chunk 切分。
- [ ] 已实现 indexing/search MVP。
- [ ] 已新增 ingest/query 调试脚本。
- [ ] 已让 qa 低耦合接入用户资料检索。
- [ ] 已完成最小测试。
- [ ] 已向用户汇报变更和未完成项。
