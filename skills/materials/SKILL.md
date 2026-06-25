# skills/materials/SKILL.md

> 模块：`materials` 用户资料库
> 当前阶段：`.md/.txt` 纵向链路整理
> 默认测试用户：`tester`

---

## 1. 模块定位

`materials` 负责用户资料从上传到检索的完整资料库链路：

```text
upload
parse
postprocess
quality report
chunk
index/search
后续 embedding/vector/db
```

`materials` 不负责学科问答本身。`qa` 后续只通过 `materials.tools` 或统一 search 接口低耦合调用资料库。

---

## 2. 当前阶段范围

当前只做 `.md/.txt` 的纵向流程：

```text
.md/.txt
↓
parser 输出基础 Markdown
↓
postprocess 清洗整理
↓
parsed/content.md
↓
quality 生成 parse_report.json
↓
chunking 切块
↓
indexing 建关键词索引
↓
search 可检索
```

不做 PDF/MinerU、DOCX、图片 OCR、ZIP、真实向量库、数据库重构、聊天中上传入库。

---

## 3. 推荐目录结构

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
├── parsers/
│   ├── base.py
│   ├── markdown_parser.py
│   ├── text_parser.py
│   ├── mineru_parser.py
│   ├── docx_parser.py
│   ├── image_parser.py
│   └── unsupported.py
│
├── postprocess/
│   ├── markdown_cleaner.py
│   ├── structure_strategy.py
│   ├── marker_parser.py
│   ├── section_builder.py
│   ├── structure_normalizer.py
│   ├── asset_rewriter.py
│   ├── formula_cleaner.py
│   ├── table_normalizer.py      # 后续
│   └── llm_cleanup.py           # 后续，用户选择才启用
│
├── quality/
│   ├── confidence.py
│   ├── validators.py
│   └── report.py
│
├── chunking/
│   ├── section_splitter.py
│   ├── chunker.py
│   └── token_counter.py
│
├── indexing/
│   └── material_indexer.py
│
├── embeddings/                  # 后续
├── repositories/                # 后续
├── vectorstores/                # 后续
└── search/                      # 后续，可由 search.py 演进
```

新增功能必须放在对应阶段目录里，不要把所有逻辑塞进 `service.py`。

---

## 4. 职责边界

一句话边界：

```text
parser 读懂原文件；
postprocess 整理成标准 Markdown；
quality 判断解析质量；
chunking 切成可检索片段；
indexing/search 负责检索；
service 只串流程。
```

### parser

不同格式输出统一基础 Markdown。

`.md` parser 不需要转换格式，但需要读取、统一编码、提取基础 metadata。
`.txt` parser 需要将纯文本轻量转换为 Markdown。

### postprocess
raw_markdown 整理与清洗相关实现，优先参考 `skill/material/raw_markdown_cleaning/SKILL.md`。
所有 parser 输出的 Markdown 都必须经过统一 postprocess。包括：

```text
基础清洗
结构规范化
图片路径改写
公式保护
```

### quality

必须输出：

```text
parsed/parse_report.json
```

并写入 manifest：

```text
quality_status
overall_confidence
warnings
```

### chunking

当前采用“强结构标题切块”：优先按 strategy 指定的 main section 切，一个主
section 对应一个主 chunk；超长时再按长度切，所有 part 保留相同 heading_path。
无编号、无 Markdown 标题符号的短行默认归入当前 section，不自动升为标题，
也不能据此切 chunk。

---

## 5. 数据存放结构

本地开发使用：

```text
data/user_materials/{user_id}/{material_id}/
├── manifest.json
├── original/
├── parsed/
│   ├── content.md
│   └── parse_report.json
├── chunks/
│   └── chunks.jsonl
├── index/
│   └── search_index.json
└── assets/
    └── images/
```

原文件默认保留，便于重解析、质量回溯和用户下载。后续可提供“删除原文件，仅保留解析结果”的用户选项。

---

## 6. LLM 智能整理策略

LLM 暂时只作为用户选择项，不默认启用。

默认：

```text
use_llm_cleanup = false
```

函数规则优先处理：编码、换行、标题、图片、公式、代码块、表格保护、chunk。
LLM 后续只允许输出受控的 strategy JSON，不输出代码、不提供任意正则、不直接
处理全文，也不得读写文件路径。本地规则通过 marker family + strategy schema
泛化不同资料格式；strategy 校验失败必须 fallback 到默认本地规则并记录 warning。

---

## 7. 质量评估规则

质量评估至少关注：

```text
文本长度
乱码比例
重复行比例
标题数量和层级
图片引用是否存在
chunk 是否为空/过长/重复
```

质量状态建议：

```text
high    >= 0.80
medium  >= 0.60
low     >= 0.40
failed  <  0.40
```

低置信度不等于失败。`.md/.txt` 可入库但应记录 warning。

---

## 8. 后续扩展规则

新增 PDF：只新增/完善 `parsers/mineru_parser.py`，输出 Markdown 后复用 postprocess/quality/chunking。
新增 DOCX：只新增/完善 `parsers/docx_parser.py`，输出 Markdown 后复用后续链路。
新增数据库：放入 `repositories/`。
新增向量库：放入 `embeddings/` 和 `vectorstores/`。
新增混合检索：演进 `search.py` 或新建 `search/` 包。

不要让 parser 直接写数据库、直接写向量库、直接调用 qa。

---

## 9. 验证要求

必须验证：

```bash
python -m compileall materials scripts tests
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"
python -m unittest tests.test_materials_mvp
python -m unittest tests.test_structure_strategy
```

结构策略新增测试必须覆盖知识点型、要点型和 decimal outline 型。

检查每次入库都生成：

```text
parsed/content.md
parsed/parse_report.json
chunks/chunks.jsonl
index/search_index.json
manifest.json
```
