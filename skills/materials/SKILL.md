# materials/SKILL.md

> 模块：用户资料整理 / 资料解析 / 用户资料库模块  
> 当前状态：`materials/` 模块已建立，网页版资料库页面已具备雏形  
> 当前重点：完善资料库页面的上传、列表、删除、搜索基础能力  
> 当前默认测试用户：`tester`  
> 适用目录：`materials/`、`scripts/ingest_material.py`、`scripts/query_materials.py`、`web/`、`data/user_materials/`

---

## 1. 模块定位

`materials` 是和 `qa` 同级的独立模块，负责用户资料库相关能力。

它负责：

1. 接收用户上传或指定的资料文件；
2. 识别文件格式；
3. 根据格式选择 parser；
4. 将资料转换为 Markdown / JSON / 图片资源；
5. 清洗 Markdown；
6. 切分 chunks；
7. 建立本地检索索引；
8. 管理用户资料列表；
9. 删除用户资料；
10. 提供资料库搜索能力；
11. 为 Web 页面和后续 `qa` 工具调用提供低耦合接口。

它不负责：

1. 生成最终问答答案；
2. 设计问答 prompt；
3. 直接参与 agent runtime；
4. 直接执行数学 / 政治 / 408 问答；
5. 在 `qa` 内部暴露 parser 细节。

---

## 2. 当前阶段边界

当前项目已经完成模块化迁移，本阶段不再要求迁移 `qa/`。

当前阶段重点：

```text
网页版资料库模块
├── 上传资料
├── 展示资料列表
├── 删除资料
└── 搜索资料
```

当前阶段的主用户是测试用户：

```text
tester
```

也就是说，当前阶段要优先实现：

```text
tester 在网页资料库界面上传资料
↓
资料进入 data/user_materials/tester/{material_id}/
↓
tester 可以查看列表
↓
tester 可以搜索资料
↓
tester 可以删除资料
```

当前阶段不优先做：

1. 聊天中上传并自动入库；
2. 资料库自然语言助手；
3. 根据资料生成总结；
4. 根据资料制定复习计划；
5. PDF / MinerU 深度解析；
6. ZIP 批量上传；
7. 登录注册；
8. 复杂权限系统。

---

## 3. 与 qa 的边界

### 3.1 允许

`qa` 后续可以通过以下接口使用资料库：

```python
from materials.search import search_user_materials
```

或：

```python
from materials.tools import search_user_materials_tool
```

### 3.2 禁止

禁止 `qa` 直接依赖 parser：

```python
from materials.parsers.mineru_parser import MinerUParser
```

禁止 `qa` 直接操作资料库目录：

```text
data/user_materials/{user_id}/{material_id}/
```

`qa` 只应该调用 `materials.search` 或 `materials.tools`。

---

## 4. 用户身份与默认测试用户规则

当前项目尚未接入真实登录系统，因此必须支持默认测试用户机制。

### 4.1 默认用户

如果请求或 CLI 没有显式传入 `user_id`，本阶段统一使用：

```text
tester
```

默认测试身份可理解为：

```text
user_id = tester
role = student
```

`role` 只表示权限身份，不能用于资料隔离。资料隔离必须以 `user_id` 为准。

### 4.2 不允许的 user_id 来源

不允许使用以下内容作为业务 `user_id`：

```text
操作系统用户名
Windows 登录名
Linux 用户名
uvicorn 启动用户
机器名
当前目录名
```

启动命令：

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

只代表启动服务，不代表业务用户。

### 4.3 Web 用户来源

Web API 可以从以下位置获取 `user_id`：

1. query 参数；
2. header，例如 `X-User-Id`；
3. request body；
4. 如果都没有，则使用 `tester`。

建议集中封装：

```python
DEFAULT_DEV_USER_ID = "tester"


def get_current_user_id(user_id: str | None = None) -> str:
    return user_id or DEFAULT_DEV_USER_ID
```

后续接登录系统时，只替换这个函数。

### 4.4 CLI 用户来源

CLI 必须支持：

```bash
--user-id
```

不传时默认：

```text
tester
```

---

## 5. 存储结构

所有用户资料必须存储在：

```text
data/user_materials/{user_id}/{material_id}/
```

当前阶段 tester 上传的资料必须存储在：

```text
data/user_materials/tester/{material_id}/
```

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

---

## 6. manifest 规则

每份资料必须有：

```text
manifest.json
```

manifest 推荐字段：

```json
{
  "material_id": "string",
  "user_id": "tester",
  "original_filename": "string",
  "file_ext": ".md",
  "mime_type": "text/markdown",
  "sha256": "string",
  "subject": "math|politics|408|english|unknown",
  "course": "string|null",
  "material_type": "lecture|note|exam|wrong_book|school_info|unknown",
  "parser_name": "markdown|text|mineru|docx|image|unsupported",
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

状态：

```text
pending
processing
ready
failed
```

失败时必须写入 error，不能静默失败。

---

## 7. 文件识别规则

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

不支持格式必须返回明确错误。

---

## 8. parser 规则

当前优先支持：

```text
.md
.txt
```

### 8.1 已实现或应优先实现

- `MarkdownParser`
- `TextParser`
- `UnsupportedParser`

### 8.2 可以占位

- `MinerUParser`
- `DocxParser`
- `ImageParser`

占位 parser 必须返回清晰错误，不要静默失败。

例如：

```text
MinerU is not available in current environment
DocxParser is not implemented yet
ImageParser is not implemented yet
ZIP upload is reserved but not implemented yet
```

---

## 9. 图片与资源规则

即使当前阶段主要支持 `.md` 和 `.txt`，也不能破坏图片引用。

Markdown 中已有图片引用时：

1. 不要删除；
2. 尽量重写到当前 material 内相对路径；
3. 如果图片存在，复制到 `assets/images/`；
4. chunk 中保留 `asset_paths`。

后续 PDF / MinerU 接入时，必须保留：

```text
数学函数图
几何图
公式截图
408 数据结构树图
操作系统页表图
计组 Cache 图
计网协议流程图
表格截图
扫描版图片题
```

---

## 10. chunk 规则

每个 chunk 至少包含：

```json
{
  "chunk_id": "string",
  "material_id": "string",
  "user_id": "tester",
  "chunk_index": 0,
  "text": "string",
  "section_title": "string|null",
  "heading_path": ["string"],
  "page_start": null,
  "page_end": null,
  "asset_paths": [],
  "token_count": 512,
  "metadata": {}
}
```

必须输出：

```text
chunks/chunks.jsonl
chunks/chunks_debug.md
```

---

## 11. search 规则

`materials/search.py` 必须实现或保持：

```python
def search_user_materials(
    user_id: str,
    query: str,
    top_k: int = 5,
    filters: dict | None = None,
) -> list:
    ...
```

要求：

1. 只搜索当前 `user_id`；
2. 默认 user_id 为 `tester`；
3. 支持 `material_id` 过滤；
4. 支持 `subject` 过滤；
5. 支持 `material_type` 过滤；
6. 返回 chunk text；
7. 返回 material_id / chunk_id；
8. 返回 source path；
9. 返回 asset_paths；
10. 不允许跨用户检索。

---

## 12. list 规则

本阶段资料库页面必须能展示资料列表，因此需要 list 能力。

推荐函数：

```python
def list_user_materials(
    user_id: str = "tester",
    filters: dict | None = None,
) -> list:
    ...
```

要求：

1. 只列出当前 `user_id` 目录下的资料；
2. 默认 user_id 为 `tester`；
3. 读取每份资料的 `manifest.json`；
4. manifest 缺失或损坏时，不要让整个列表崩溃；
5. 可以返回错误项，但要标记为 `failed` 或 `broken_manifest`；
6. 不允许列出其他用户资料。

返回字段建议：

```json
{
  "material_id": "string",
  "original_filename": "string",
  "subject": "unknown",
  "material_type": "unknown",
  "parse_status": "ready",
  "chunk_count": 0,
  "asset_count": 0,
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime",
  "error": null
}
```

---

## 13. delete 规则

本阶段需要实现资料删除能力。

推荐函数：

```python
def delete_user_material(
    user_id: str,
    material_id: str,
) -> dict:
    ...
```

### 13.1 删除范围

只允许删除：

```text
data/user_materials/{user_id}/{material_id}/
```

当前默认：

```text
data/user_materials/tester/{material_id}/
```

禁止删除：

```text
data/raw/
data/processed/
qa/
materials/
scripts/
web/
其他 user_id 的资料目录
```

### 13.2 安全校验

删除前必须校验：

1. `user_id` 合法；
2. `material_id` 合法；
3. 目标路径在 `data/user_materials/{user_id}/` 下；
4. 目标路径确实存在；
5. 目标路径确实是目录。

推荐使用：

```python
target.resolve().relative_to(base.resolve())
```

验证目标路径没有越界。

### 13.3 ID 安全规则

`user_id` 和 `material_id` 建议只允许：

```text
A-Z
a-z
0-9
_
-
```

禁止：

```text
/
\
..
空字符串
```

### 13.4 删除结果

删除成功返回：

```json
{
  "ok": true,
  "deleted": true,
  "user_id": "tester",
  "material_id": "string"
}
```

删除失败返回清晰错误：

```text
Invalid material_id
Material not found
Permission denied
Failed to delete material
```

不要静默失败。

---

## 14. Web API 规则

本阶段后端至少应支持：

```text
POST   /api/materials/upload
GET    /api/materials/list
GET    /api/materials/search
DELETE /api/materials/{material_id}
```

### 14.1 上传

```text
POST /api/materials/upload
```

支持：

```text
file
user_id，可选，默认 tester
subject
material_type
```

### 14.2 列表

```text
GET /api/materials/list
```

支持：

```text
user_id，可选，默认 tester
subject，可选
material_type，可选
```

### 14.3 搜索

```text
GET /api/materials/search
```

支持：

```text
user_id，可选，默认 tester
query
top_k
material_id，可选
subject，可选
material_type，可选
```

### 14.4 删除

```text
DELETE /api/materials/{material_id}
```

支持：

```text
user_id，可选，默认 tester
```

删除必须用户隔离。

---

## 15. Web 页面规则

资料库页面应包含：

```text
当前用户
上传资料
资料列表
资料搜索
删除按钮
状态提示
错误提示
```

### 15.1 上传交互

上传成功后：

1. 展示成功提示；
2. 展示 material_id；
3. 展示 chunk_count；
4. 刷新资料列表。

上传失败后：

1. 展示错误；
2. 不要只写 console。

### 15.2 列表交互

资料列表至少展示：

```text
文件名
material_id
学科
类型
状态
chunks
更新时间
操作
```

### 15.3 删除交互

删除前必须确认：

```text
确定要删除这份资料吗？此操作会删除该资料的原文件副本、解析结果、chunks 和索引。
```

删除成功后：

1. 刷新资料列表；
2. 清理相关搜索结果或提示用户重新搜索；
3. 展示“资料已删除”。

删除失败后：

1. 展示错误；
2. 不要只写 console。

### 15.4 搜索交互

搜索无结果时提示：

```text
当前用户资料库中没有找到相关内容
```

---

## 16. CLI 脚本规则

### 16.1 ingest_material.py

必须支持：

```bash
python scripts/ingest_material.py --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
```

不传 `--user-id` 默认 `tester`。

### 16.2 query_materials.py

必须支持：

```bash
python scripts/query_materials.py --query "罗尔定理"
python scripts/query_materials.py --user-id tester --query "罗尔定理"
```

不传 `--user-id` 默认 `tester`。

### 16.3 后续可选 delete_material.py

如果需要，也可以新增：

```bash
python scripts/delete_material.py --user-id tester --material-id xxx
```

但当前阶段优先保证 Web 删除 API 和页面按钮。

---

## 17. 测试要求

### 17.1 CLI 验证

```bash
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"
```

### 17.2 Web API 验证

上传：

```bash
curl -X POST "http://127.0.0.1:8000/api/materials/upload?user_id=tester" -F "file=@data/demo/test.md"
```

列表：

```bash
curl "http://127.0.0.1:8000/api/materials/list?user_id=tester"
```

搜索：

```bash
curl "http://127.0.0.1:8000/api/materials/search?user_id=tester&query=罗尔定理"
```

删除：

```bash
curl -X DELETE "http://127.0.0.1:8000/api/materials/{material_id}?user_id=tester"
```

### 17.3 用户隔离验证

必须验证：

- [ ] `tester` 上传的资料只进入 `data/user_materials/tester/`；
- [ ] `tester` 只能 list 自己的资料；
- [ ] `tester` 只能 search 自己的资料；
- [ ] `tester` 只能 delete 自己的资料；
- [ ] `tester` 删除不了 `test_user_a` 或 `test_user_b` 的资料；
- [ ] 不传 user_id 时默认使用 `tester`。

### 17.4 原有功能验证

尽量运行：

```bash
python scripts/ask_kaoyan.py 极限是什么 --no-memory --format terminal
python scripts/ask_math.py 极限是什么 --no-memory --format terminal
python -m unittest tests.test_agent_runtime
```

如果 Qwen 403 导致问答命令失败，说明是账号额度问题，不要误判为资料库模块失败。

---

## 18. 完成汇报要求

每次修改后必须汇报：

- [ ] 新增/修改了哪些文件；
- [ ] 是否改动了 `qa` 主流程；
- [ ] tester 上传功能是否可用；
- [ ] tester 列表功能是否可用；
- [ ] tester 删除功能是否可用；
- [ ] tester 搜索功能是否可用；
- [ ] 用户隔离是否验证；
- [ ] 运行了哪些命令；
- [ ] 哪些命令失败，原因是什么；
- [ ] 下一步建议。

---

## 19. 当前阶段完成标准

本阶段完成标准：

- [ ] 网页能打开；
- [ ] 左侧能进入“我的资料库”；
- [ ] 默认用户为 `tester`；
- [ ] `tester` 能上传 `.md` 或 `.txt`；
- [ ] 上传后资料进入 `data/user_materials/tester/{material_id}/`；
- [ ] 页面能展示 tester 的资料列表；
- [ ] 页面能搜索 tester 的资料；
- [ ] 页面能删除 tester 的资料；
- [ ] 删除后对应 material 目录被移除；
- [ ] 删除后列表刷新；
- [ ] 删除后搜索不到该资料；
- [ ] 不会跨用户 list/search/delete；
- [ ] 原问答入口未被破坏。

---

## 20. 后续阶段建议

完成本阶段后，再考虑：

1. 资料详情页；
2. 查看 chunks；
3. 重新解析；
4. PDF / MinerU 接入；
5. 图片 OCR / VLM caption；
6. 聊天中上传并入库；
7. 聊天中根据用户资料库回答；
8. 资料库自然语言助手；
9. Obsidian 插件客户端接入。
