# materials/SKILL.md

> 模块：用户资料整理 / 资料解析 / 用户资料库入库模块  
> 适用目录：`materials/`、`scripts/ingest_material.py`、`scripts/query_materials.py`、`data/user_materials/`  
> 核心目标：将用户上传或指定的单一资料文件解析为 Markdown / JSON / 图片资源 / chunks / index，并按用户隔离存入用户自己的资料库。  
> 当前阶段：MVP，优先跑通 `.md` 和 `.txt` 单文件入库；PDF、DOCX、图片、ZIP 先保留接口或明确占位。

---

## 1. 模块定位

`materials` 模块是和 `qa` 同级的独立业务模块，不是问答模块的子功能文件夹。

它负责：

1. 识别用户上传或指定的资料路径；
2. 判断文件格式；
3. 根据格式选择 parser；
4. 将资料转换为 Markdown / JSON / 图片资源；
5. 对 Markdown 做后处理清洗；
6. 保存无法识别为文字的图片、图表、公式截图、408 图示；
7. 切分 chunk；
8. 建立本地检索索引；
9. 将资料存入当前用户自己的资料库；
10. 为 `qa` 提供低耦合的资料检索接口。

它不负责：

1. 生成最终问答答案；
2. 决定用户问题属于数学、政治、408；
3. 直接修改问答 prompt；
4. 直接参与 agent runtime 的路由循环；
5. 直接暴露 MinerU 给 `qa` 模块。

---

## 2. 与 qa 模块的边界

### 2.1 允许的调用方向

允许：

```python
from materials.search import search_user_materials
```

或：

```python
from materials.tools import search_user_materials_tool
from materials.tools import ingest_user_material
```

### 2.2 禁止的调用方向

禁止 `qa` 直接调用 parser 细节：

```python
from materials.parsers.mineru_parser import MinerUParser
```

禁止 `qa` 直接操作：

```text
data/user_materials/{user_id}/{material_id}/parsed/content.md
data/user_materials/{user_id}/{material_id}/chunks/chunks.jsonl
```

`qa` 只能通过 `materials.search` 或 `materials.tools` 获取用户资料检索结果。

---

## 3. 用户身份与默认测试用户规则

当前项目尚未接入真实登录系统，因此 `materials` 模块必须支持本地开发默认用户机制。

### 3.1 核心原则

1. `materials` 模块必须按业务 `user_id` 隔离用户资料。
2. 不允许使用操作系统用户名、Windows 登录名、Linux 用户名、uvicorn 启动用户作为业务 `user_id`。
3. 启动命令：

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

只代表启动了服务，不代表当前业务用户是谁。

4. 本地开发阶段，如果请求或脚本没有显式传入 `user_id`，统一使用：

```text
local_dev_user
```

5. 默认测试用户可以认为是：

```text
user_id = local_dev_user
role = student
```

6. `role` 只表示权限身份，不能用于资料隔离；资料隔离必须以 `user_id` 为准。

### 3.2 CLI 规则

所有 `materials` 相关 CLI 脚本都应该支持：

```bash
--user-id
```

例如：

```bash
python scripts/ingest_material.py --user-id test_user --file data/demo/test.md
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
```

如果没有传入 `--user-id`，默认使用：

```text
local_dev_user
```

### 3.3 Web API 规则

`materials` Web API 可以从以下位置获取 `user_id`：

1. query 参数，例如 `?user_id=test_user`；
2. header，例如 `X-User-Id: test_user`；
3. request body；
4. 如果都没有，则使用 `local_dev_user`。

建议封装统一函数：

```python
def get_current_user_id(user_id: str | None = None) -> str:
    return user_id or "local_dev_user"
```

后续接入真实登录系统时，只替换这个函数的内部实现，不要修改 `materials` 主流程。

### 3.4 存储规则

所有用户资料必须保存到：

```text
data/user_materials/{user_id}/{material_id}/
```

例如：

```text
data/user_materials/local_dev_user/{material_id}/
data/user_materials/test_user_a/{material_id}/
data/user_materials/test_user_b/{material_id}/
```

### 3.5 检索规则

`search_user_materials(user_id, query, top_k=5, filters=None)` 必须只检索当前 `user_id` 下的资料。

禁止跨用户检索：

```text
data/user_materials/test_user_a/
```

不能被：

```text
test_user_b
```

检索到。

### 3.6 测试要求

`materials` 模块至少需要支持以下测试场景：

1. 不传 `user_id`，资料进入 `local_dev_user`；
2. 传入 `test_user_a`，资料进入 `test_user_a`；
3. 传入 `test_user_b`，资料进入 `test_user_b`；
4. `test_user_a` 不能检索到 `test_user_b` 的资料；
5. `test_user_b` 不能检索到 `test_user_a` 的资料。

---

## 4. 当前阶段范围

### 4.1 本阶段必须完成

优先跑通：

```text
.md / .txt 单文件
↓
识别文件
↓
保存原文件
↓
解析为 Markdown
↓
清洗 Markdown
↓
保留图片引用
↓
切分 chunks
↓
生成本地 search index
↓
按 user_id/material_id 入库
↓
可以通过 query_materials.py 检索
```

### 4.2 本阶段可以占位

以下能力本阶段可以只保留接口或明确错误：

1. PDF 真正调用 MinerU；
2. DOCX 真正解析；
3. 图片 OCR / VLM caption；
4. ZIP 批量解析；
5. 目录批量解析；
6. 重型向量数据库；
7. 异步任务队列；
8. Web 前端上传页面。

### 4.3 本阶段禁止过度扩展

不要在本阶段做：

1. 登录系统；
2. 用户权限系统；
3. 多租户数据库；
4. 复杂前端；
5. 大规模重构 `qa`；
6. 重新设计问答 prompt；
7. 深度接入 MinerU 并要求必须成功运行。

---

## 5. 推荐目录结构

`materials/` 推荐结构：

```text
materials/
├── __init__.py
├── service.py
├── schemas.py
├── detector.py
├── resolver.py
├── router.py
├── storage.py
├── search.py
├── tools.py
├── api.py
│
├── parsers/
│   ├── __init__.py
│   ├── base.py
│   ├── markdown_parser.py
│   ├── text_parser.py
│   ├── mineru_parser.py
│   ├── docx_parser.py
│   ├── image_parser.py
│   └── unsupported.py
│
├── postprocess/
│   ├── __init__.py
│   ├── markdown_cleaner.py
│   ├── asset_rewriter.py
│   ├── formula_cleaner.py
│   └── metadata_extractor.py
│
├── chunking/
│   ├── __init__.py
│   ├── chunker.py
│   ├── section_splitter.py
│   └── token_counter.py
│
└── indexing/
    ├── __init__.py
    ├── embedding_builder.py
    └── material_indexer.py
```

`scripts/` 只保留调试入口：

```text
scripts/
├── ingest_material.py
└── query_materials.py
```

---

## 6. 用户资料库存储结构

不要使用全局散落结构：

```text
user_materials/
├── original_files/
├── parsed_markdown/
├── parsed_json/
├── images/
├── chunks/
└── embeddings/
```

推荐按用户和资料聚合：

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

好处：

1. 一份资料的所有产物集中在一个目录；
2. 方便删除；
3. 方便重解析；
4. 方便调试；
5. 方便迁移到对象存储；
6. 方便做用户隔离。

---

## 7. manifest 规则

每份资料必须有：

```text
manifest.json
```

推荐字段：

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
    "layout": "string|null",
    "chunks": "string|null",
    "search_index": "string|null"
  },
  "chunk_count": 0,
  "asset_count": 0,
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime",
  "error": null
}
```

状态规则：

```text
pending     尚未开始
processing  处理中
ready       成功入库
failed      失败
```

失败时必须写入：

```json
{
  "parse_status": "failed",
  "error": "清晰错误信息"
}
```

不要静默失败。

---

## 8. 文件识别规则

`materials/detector.py` 负责识别文件类型。

必须识别：

```text
.md
.txt
.pdf
.docx
.png
.jpg
.jpeg
.webp
.zip
```

至少返回：

```python
DetectedFile(
    path=...,
    original_filename=...,
    file_ext=...,
    mime_type=...,
    sha256=...,
    size_bytes=...
)
```

不支持格式必须返回明确错误，而不是报模糊异常。

---

## 9. resolver 规则

`materials/resolver.py` 负责将用户传入路径解析为待处理项目。

当前阶段只支持：

```text
单一文件
```

如果输入是 `.zip`：

```text
ZIP upload is reserved but not implemented yet
```

如果输入是目录：

```text
Directory upload is reserved but not implemented yet
```

必须保留未来扩展接口，例如：

```python
def resolve_upload_path(path: Path) -> list[ResolvedUploadItem]:
    ...
```

即使当前只返回一个 item，也不要把 service 写死成只能处理一个 path。

---

## 10. parser router 规则

`materials/router.py` 根据文件格式选择 parser。

推荐映射：

```text
.md      -> MarkdownParser
.txt     -> TextParser
.pdf     -> MinerUParser
.png     -> ImageParser 或 MinerUParser
.jpg     -> ImageParser 或 MinerUParser
.jpeg    -> ImageParser 或 MinerUParser
.webp    -> ImageParser 或 MinerUParser
.docx    -> DocxParser
.zip     -> reserved but not implemented
other    -> UnsupportedParser
```

parser router 只负责选择 parser，不负责具体解析逻辑。

---

## 11. parser 规则

所有 parser 必须继承或遵守统一接口：

```python
class BaseMaterialParser:
    parser_name: str

    def parse(self, input_path, output_dir, context) -> ParseResult:
        ...
```

`ParseResult` 至少包含：

```python
markdown_path
json_path
layout_path
assets
metadata
status
error
```

### 11.1 MarkdownParser

必须实现：

1. 读取 `.md`；
2. 保存为 `parsed/content.md`；
3. 保留原始图片引用；
4. 返回成功状态。

### 11.2 TextParser

必须实现：

1. 读取 `.txt`；
2. 转成简单 Markdown；
3. 保存为 `parsed/content.md`；
4. 返回成功状态。

### 11.3 MinerUParser

当前阶段可以接口先行：

1. 封装 MinerU CLI/API 调用；
2. 不能把 MinerU 命令散落到其他模块；
3. 如果 MinerU 不可用，返回清晰错误；
4. 不要让 `.md` / `.txt` MVP 因 MinerU 不可用而失败；
5. 后续真正接入时，输出必须进入当前 material 目录。

### 11.4 DocxParser / ImageParser

当前阶段可以占位：

1. 返回明确 NotImplemented；
2. 不要静默失败；
3. 不要阻塞 `.md` / `.txt` 主链路。

### 11.5 UnsupportedParser

必须返回明确错误，例如：

```text
Unsupported file type: .xxx
```

---

## 12. Markdown 后处理规则

资料解析后必须进入 postprocess，不能直接 chunk。

### 12.1 markdown_cleaner

`materials/postprocess/markdown_cleaner.py` 应做到：

1. 清理多余空行；
2. 清理明显重复页眉页脚，MVP 可先轻量处理；
3. 不破坏数学公式；
4. 不删除图片引用；
5. 不强行重写所有表格；
6. 不主动丢失原文结构。

### 12.2 formula_cleaner

MVP 可轻量实现或占位。

禁止：

1. 大规模改写 LaTeX；
2. 删除公式；
3. 把无法理解的公式清空。

---

## 13. 图片与资源处理规则

这是本模块的重点。

### 13.1 核心原则

解析后的图片、图表、公式截图、408 图示不能丢。

尤其是：

1. 数学函数图；
2. 几何图；
3. 公式截图；
4. 408 数据结构树图；
5. 操作系统页表图；
6. 计组 Cache 图；
7. 计网协议流程图；
8. 表格截图；
9. 扫描版图片题。

### 13.2 asset_rewriter

`materials/postprocess/asset_rewriter.py` 应做到：

1. 识别 Markdown 中的图片引用；
2. 将图片复制或移动到：

```text
assets/images/
```

3. 将 Markdown 图片路径改写为 material 内相对路径；
4. 如果图片无法识别为文字，也要保留；
5. chunk 中必须能记录相关图片路径。

推荐图片占位格式：

```md
![第 23 页图 1：原文图片，OCR 未识别，已保留原图](../assets/images/page_023_img_001.png)
```

### 13.3 图片命名建议

推荐：

```text
page_001_img_001.png
page_001_table_001.png
page_008_diagram_002.png
page_012_formula_001.png
```

如果没有页码，使用：

```text
img_001.png
diagram_001.png
formula_001.png
```

---

## 14. chunk 切分规则

`materials/chunking/chunker.py` 负责将 Markdown 切为 chunks。

### 14.1 切分策略

优先级：

1. 按 Markdown 标题切分；
2. 超长 section 按段落切分；
3. 仍然过长时按长度切分；
4. 不要把图片引用和对应说明拆得太远；
5. 不要把公式和上下文拆散。

### 14.2 chunk schema

每个 chunk 至少包含：

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

### 14.3 输出文件

必须输出：

```text
chunks/chunks.jsonl
chunks/chunks_debug.md
```

`chunks_debug.md` 用于人工检查切分质量。

---

## 15. indexing / search 规则

### 15.1 MVP indexing

`materials/indexing/material_indexer.py` 应该：

1. 读取 `chunks/chunks.jsonl`；
2. 生成简单本地 search index；
3. 保存为：

```text
index/search_index.json
```

4. 预留 embedding 接口。

### 15.2 embedding_builder

`materials/indexing/embedding_builder.py` 当前可先：

1. 使用 mock embedding；
2. 使用 local hash；
3. 复用项目已有 embedding；
4. 不要强制依赖 Qwen；
5. 不要因为 Qwen 403 导致 materials MVP 失败。

### 15.3 search

`materials/search.py` 必须实现：

```python
def search_user_materials(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
) -> list[MaterialSearchResult]:
    ...
```

要求：

1. 只搜索当前 `user_id`；
2. 支持 `material_id` 过滤；
3. 支持 `subject` 过滤；
4. 支持 `material_type` 过滤；
5. 返回 chunk text；
6. 返回 material_id / chunk_id；
7. 返回 source path；
8. 返回 asset_paths；
9. 不允许跨用户检索。

---

## 16. service 主流程

`materials/service.py` 推荐实现：

```python
class MaterialIngestionService:
    def ingest_file(
        self,
        file_path,
        user_id: str = "local_dev_user",
        subject: str = "unknown",
        material_type: str = "unknown",
        metadata: dict | None = None,
    ) -> MaterialIngestionResult:
        ...
```

主流程：

```text
resolve upload path
↓
detect file
↓
create material_id
↓
create material dir
↓
save original
↓
select parser
↓
parse to markdown/json/assets
↓
postprocess markdown
↓
chunk
↓
index
↓
write manifest
↓
return result
```

失败时：

1. 写入 manifest；
2. 设置 `parse_status = failed`；
3. 写入 error；
4. 返回清晰错误；
5. 不要静默吞异常。

---

## 17. CLI 脚本规则

### 17.1 ingest_material.py

必须支持：

```bash
python scripts/ingest_material.py --user-id test_user --file data/demo/test.md
```

参数：

```text
--user-id       可选，默认 local_dev_user
--file          必填
--subject       可选，默认 unknown
--material-type 可选，默认 unknown
```

输出至少包含：

```text
material_id
user_id
parse_status
manifest_path
markdown_path
chunk_count
error
```

### 17.2 query_materials.py

必须支持：

```bash
python scripts/query_materials.py --user-id test_user --query "罗尔定理"
```

参数：

```text
--user-id      可选，默认 local_dev_user
--query        必填
--top-k        可选，默认 5
--material-id  可选
--subject      可选
```

输出至少包含：

```text
rank
material_id
chunk_id
score
text preview
asset_paths
```

---

## 18. Web API 规则

MVP 可选，但如果实现，应遵守：

```text
POST /api/materials/upload
GET  /api/materials/{material_id}
GET  /api/materials/search
```

用户身份来源：

1. query；
2. header `X-User-Id`；
3. body；
4. 默认 `local_dev_user`。

大文件解析后续应走异步任务，本阶段可以同步，但必须留 TODO。

---

## 19. 测试要求

至少验证：

### 19.1 入库

```bash
python scripts/ingest_material.py --file data/demo/test.md
python scripts/ingest_material.py --file data/demo/test.txt
python scripts/ingest_material.py --user-id test_user_a --file data/demo/test.md
python scripts/ingest_material.py --user-id test_user_b --file data/demo/test.txt
```

### 19.2 检索

```bash
python scripts/query_materials.py --query "罗尔定理"
python scripts/query_materials.py --user-id test_user_a --query "罗尔定理"
python scripts/query_materials.py --user-id test_user_b --query "罗尔定理"
```

### 19.3 用户隔离

必须验证：

1. `test_user_a` 查不到 `test_user_b` 的资料；
2. `test_user_b` 查不到 `test_user_a` 的资料；
3. 不传 user_id 时使用 `local_dev_user`；
4. `local_dev_user` 与 `test_user_a`、`test_user_b` 互相隔离。

### 19.4 原有功能不破坏

资料模块完成后，应尽量验证：

```bash
python scripts/ask_kaoyan.py 极限是什么 --no-memory --format terminal
python scripts/ask_math.py 极限是什么 --no-memory --format terminal
python -m unittest tests.test_agent_runtime
```

如果 Qwen 403 导致问答命令失败，必须说明这是账号额度问题，不要误判为 materials 模块失败。

---

## 20. 错误处理规则

错误必须清晰。

常见错误：

```text
Unsupported file type: .xxx
ZIP upload is reserved but not implemented yet
Directory upload is reserved but not implemented yet
MinerU is not available in current environment
Input file does not exist
Permission denied
Failed to write manifest
Failed to parse markdown
```

禁止：

1. 静默失败；
2. 只打印 traceback 不写 manifest；
3. 出错后留下半成品但状态仍为 ready；
4. 把 parser 错误伪装成检索错误。

---

## 21. 完成汇报规则

每次修改 materials 模块后，向用户汇报：

1. 新增/修改了哪些文件；
2. 哪些 parser 已实现；
3. 哪些 parser 是占位；
4. `.md` / `.txt` 入库是否成功；
5. manifest、chunks、search_index 是否生成；
6. search 是否能查到内容；
7. 是否验证了用户隔离；
8. 哪些命令通过；
9. 哪些命令失败；
10. 下一步建议。

---

## 22. 总结原则

本模块最重要的原则：

```text
用户上传可以自由；
系统入库必须规范；
图片资源不能丢；
资料检索必须用户隔离；
qa 只调用检索接口，不关心 parser 细节；
MVP 先跑通 md/txt，再接 MinerU/PDF/图片。
```
