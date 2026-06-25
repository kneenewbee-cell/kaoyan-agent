# AGENTS.md

> 项目：考研 Agent 助手
> 当前阶段：`materials` 纵向链路整理阶段
> 默认测试用户：`tester`
> 当前优先任务：先把 `.md/.txt` 的 parse → clean → quality report → chunk → index/search 链路做稳

---

## 0. 当前判断

项目顶层结构方向正确，不需要推翻：

```text
qa/          问答、路由、追问、学科逻辑
materials/   用户资料库、解析、清洗、切块、检索
scripts/     CLI / 启动 / 调试入口
web/         前端页面
skills/      模块开发规范
```

本阶段不再重构 `qa/`，不大改前端，不接 PDF/MinerU/DOCX/图片/ZIP。当前重点是完善 `materials/` 内部边界，并先做好 `.md/.txt` 纵向主链路。

---

## 1. 当前目标

本轮目标不是横向扩展文件格式，而是让 `.md/.txt` 这一条链路更标准：

```text
上传 .md/.txt
↓
保存 original/
↓
parser 读取并输出 raw markdown
↓
postprocess 清洗、整理、规范化
↓
输出 parsed/content.md
↓
quality 生成 parsed/parse_report.json
↓
chunking 按标题/段落/长度切块
↓
indexing 建关键词索引
↓
search 可检索
```

完成后再考虑数据库、向量库、PDF、DOCX。

---

## 2. materials 模块边界

`materials/` 应按流水线阶段组织，不按文件类型大拆。

推荐结构：

```text
materials/
├── schemas.py
├── security.py
├── storage.py
├── detector.py
├── resolver.py
├── router.py
├── service.py
├── api.py
├── tools.py
│
├── parsers/        # 不同格式 → raw markdown
├── postprocess/    # raw markdown → clean markdown
├── quality/        # clean markdown + chunks → parse_report
├── chunking/       # clean markdown → chunks
├── indexing/       # chunks → keyword index
├── embeddings/     # 后续：chunks → embeddings
├── repositories/   # 后续：SQLite/PostgreSQL 读写
├── vectorstores/   # 后续：Chroma/Qdrant/FAISS
└── search/         # 后续：keyword/vector/hybrid search
```

当前只要求 `.md/.txt` 纵向流程，不强制实现 `embeddings/`、`repositories/`、`vectorstores/`。

---

## 3. 职责划分

### 3.1 parser

parser 负责“读懂原文件并输出基础 Markdown”。

`.md`：

```text
读取 Markdown
统一编码/换行
提取 front matter、标题数、图片引用数、source_dir
输出 parsed/content.md
```

`.txt`：

```text
读取 txt
统一编码/换行
文件名作为一级标题
疑似标题行转 Markdown 标题
输出 parsed/content.md
```

parser 不负责大量清洗、不负责切块、不负责向量库、不负责数据库。

### 3.2 postprocess

postprocess 负责“把 raw markdown 整理成标准 Markdown”。

```text
markdown_cleaner.py       基础清洗
structure_normalizer.py   标题层级、Setext 标题、缺空格标题、兜底根标题
asset_rewriter.py         图片路径复制与改写
formula_cleaner.py        公式保护
```

### 3.3 quality

quality 负责“判断解析和整理质量”。输出：

```text
parsed/parse_report.json
```

并写入 manifest：

```text
quality_status
overall_confidence
warnings
```

### 3.4 chunking

chunking 负责“把 clean markdown 切成可检索片段”。规则：

```text
标题优先
段落兜底
长度硬切兜底
图片/公式/表格尽量不拆散
chunk metadata 保留 heading_path、subject、material_type、original_filename
```

---

## 4. LLM 清洗策略

LLM 清洗暂时只作为用户可选项，不默认进入主链路。

当前默认：

```text
use_llm_cleanup = false
```

只有用户显式选择“智能整理”或后续低置信度片段需要处理时，才考虑调用 LLM。不要让 LLM 成为 `.md/.txt` 入库的必需依赖。

---

## 5. 当前不做

本阶段不要做：

```text
PDF/MinerU 完整解析
DOCX 完整解析
图片 OCR/VLM
ZIP 批量解析
真实向量库接入
数据库重构
聊天中上传入库
根据资料库回答
资料库自然语言助手
qa 大重构
```

---

## 6. 验证命令

修改后必须运行：

```bash
python -m compileall materials scripts tests

python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"

python -m unittest tests.test_materials_mvp
python -m unittest tests.test_agent_runtime
```

重点检查生成目录：

```text
data/user_materials/tester/{material_id}/
├── manifest.json
├── original/
├── parsed/
│   ├── content.md
│   └── parse_report.json
├── chunks/chunks.jsonl
└── index/search_index.json
```

---

## 7. 完成汇报

每次修改后汇报：

1. 修改/新增了哪些文件；
2. 是否改动 `qa`；
3. `.md/.txt` 入库是否成功；
4. 是否生成 `parsed/content.md`；
5. 是否生成 `parsed/parse_report.json`；
6. chunk/index/search 是否可用；
7. 测试命令结果；
8. 仍保留哪些占位功能。
