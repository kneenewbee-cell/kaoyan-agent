# AGENTS.md

> 项目：考研 Agent 助手  
> 当前阶段：模块化已完成，进入“网页版资料库模块”建设阶段  
> 当前默认测试用户：`tester`  
> 当前优先任务：完善网页版“我的资料库”页面，让 tester 可以上传、查看、搜索、删除自己的资料  
> 适用对象：Codex / Claude Code / 其他 AI coding agent / 维护者

---

## 0. 当前项目状态

当前项目已经完成基础模块化：

```text
qa/          当前问答核心模块
materials/   用户资料整理 / 资料解析 / 用户资料库模块
scripts/     启动脚本、调试脚本、构建脚本
web/         前端页面资源
skills/      各模块开发规范
data/        数据与用户资料库
```

当前重点不再是迁移 `qa/`，也不是重写问答主流程，而是继续完善：

```text
网页版资料库模块
```

当前阶段的产品目标是：

```text
tester 用户可以在网页“我的资料库”页面上传资料、看到资料列表、搜索资料、删除资料。
```

---

## 1. 本阶段核心目标

本阶段只聚焦资料库基础交互闭环：

```text
打开网页
↓
进入“我的资料库”
↓
当前用户默认为 tester
↓
上传 .md / .txt 资料
↓
资料进入 data/user_materials/tester/{material_id}/
↓
页面显示资料列表
↓
可以搜索该用户资料
↓
可以删除该用户资料
```

优先级：

1. Web 资料上传；
2. Web 资料列表；
3. Web 资料删除；
4. Web 资料搜索；
5. 后端 API 稳定；
6. 用户隔离；
7. 错误提示；
8. 保证原问答入口不被破坏。

---

## 2. 本阶段不做

本阶段暂不做：

- [ ] 聊天中上传文件并自动入库；
- [ ] 根据用户资料库自动回答；
- [ ] 资料库自然语言助手；
- [ ] PDF / MinerU 深度解析；
- [ ] DOCX 完整解析；
- [ ] 图片 OCR / VLM caption；
- [ ] ZIP 批量解析；
- [ ] 登录注册系统；
- [ ] 复杂权限系统；
- [ ] Obsidian 插件；
- [ ] 大规模重构 `qa/`；
- [ ] 大规模重构前端框架。

如果看到 PDF、DOCX、图片、ZIP 相关入口，允许保留接口或返回明确错误，不要为了这些阻塞 `.md/.txt` 和资料库页面闭环。

---

## 3. 必须遵守的规范

涉及 `materials/`、资料上传、资料列表、删除、搜索、资料库页面时，必须阅读并遵守：

```text
skills/materials/SKILL.md
```

涉及问答、数学、政治、追问、项目通用规则时，尽量遵守：

```text
skills/math/SKILL.md
skills/politics/SKILL.md
skills/followup/SKILL.md
skills/project/SKILL.md
```

如果规范与当前代码存在差异，优先级为：

```text
不破坏现有可运行功能
↓
保持用户资料隔离
↓
逐步补齐资料库页面功能
↓
每一步都可验证
```

---

## 4. 硬性禁止事项

- [ ] 不要再次大规模迁移 `qa/`。
- [ ] 不要拆分 `qa/math`、`qa/politics`、`qa/runtime` 等新大模块。
- [ ] 不要重写现有问答主流程。
- [ ] 不要删除现有可运行的 CLI 脚本。
- [ ] 不要删除 `data/raw/`、`data/processed/` 中已有资料。
- [ ] 不要删除用户已经上传生成的 `data/user_materials/`，除非用户明确要求。
- [ ] 不要把 MinerU 调用散落到 `qa/` 或 Web 前端里。
- [ ] 不要让 `qa/` 直接 import `materials/parsers/mineru_parser.py`。
- [ ] 不要把真实 API Key、cookie、token、`.env` 内容写入代码或文档。
- [ ] 不要依赖 Qwen 调用完成 materials 页面功能；Qwen 403 不能阻塞资料库上传、列表、删除、搜索。
- [ ] 不要在本阶段强行实现 ZIP 批量解析。
- [ ] 不要在本阶段做复杂登录系统。
- [ ] 不要让 `tester` 可以看到、搜索、删除其他 user_id 的资料。

---

## 5. 当前默认测试用户规则

当前阶段默认测试用户为：

```text
tester
```

这意味着：

1. Web 资料库页面默认显示 `tester`；
2. 上传时不传 `user_id`，默认进入 `tester`；
3. 列表不传 `user_id`，默认列出 `tester`；
4. 搜索不传 `user_id`，默认搜索 `tester`；
5. 删除不传 `user_id`，默认删除 `tester` 名下指定资料；
6. CLI 脚本不传 `--user-id`，默认也可以使用 `tester`。

不要使用操作系统用户名、Windows 登录名、Linux 用户名、机器名、uvicorn 启动用户作为业务用户。

启动命令：

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

只代表服务启动，不代表业务用户。业务用户由 query/header/body/默认值决定。

---

## 6. 用户资料隔离要求

所有资料必须存储在：

```text
data/user_materials/{user_id}/{material_id}/
```

当前阶段 tester 上传的资料必须进入：

```text
data/user_materials/tester/{material_id}/
```

`list`、`search`、`delete` 必须只作用于当前 `user_id`。

例如 `tester` 不能 list/search/delete：

```text
test_user_a
test_user_b
local_dev_user
其他用户
```

除非显式传入对应 `user_id` 并且操作范围仍然被限制在该用户目录内。

---

## 7. 必须保持的模块边界

### 7.1 qa/

负责问答、路由、工具调用、学科问答逻辑、追问处理。

`qa/` 允许低耦合调用：

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

### 7.2 materials/

负责资料上传接收、文件识别、parser 路由、Markdown/Text 入库、后处理、chunk 切分、index/search、manifest 管理、资料列表、资料删除。

### 7.3 scripts/

只保留启动脚本、调试脚本、构建脚本、CLI 测试入口。

### 7.4 web/

负责左侧导航、考研问答页面、我的资料库页面、资料上传、资料列表、资料删除、资料搜索、状态提示、错误提示。

---

## 8. 当前资料库页面目标

### 8.1 tester 上传资料

- [ ] 默认用户显示为 `tester`；
- [ ] 可以修改 user_id，但默认是 `tester`；
- [ ] 可以选择文件；
- [ ] 可以选择学科 `subject`；
- [ ] 可以选择资料类型 `material_type`；
- [ ] 调用 `POST /api/materials/upload`；
- [ ] 上传成功后显示结果；
- [ ] 上传成功后刷新资料列表；
- [ ] 上传失败后显示明确错误。

当前优先支持：

```text
.md
.txt
```

PDF、DOCX、图片、ZIP 可以显示明确错误，不要阻塞页面。

### 8.2 tester 查看资料列表

- [ ] 调用 `GET /api/materials/list`；
- [ ] 默认列出 `tester` 的资料；
- [ ] 显示文件名；
- [ ] 显示 material_id；
- [ ] 显示 subject；
- [ ] 显示 material_type；
- [ ] 显示 parse_status；
- [ ] 显示 chunk_count；
- [ ] 显示 created_at / updated_at；
- [ ] 提供刷新按钮；
- [ ] manifest 损坏时不要让整个列表崩溃。

### 8.3 tester 删除资料

本阶段需要实现或完善删除能力。

推荐后端：

```text
DELETE /api/materials/{material_id}
```

要求：

- [ ] 默认 user_id 为 `tester`；
- [ ] 只能删除 `data/user_materials/tester/{material_id}/`；
- [ ] 不允许删除其他用户资料；
- [ ] 不允许路径穿越；
- [ ] 删除前前端必须确认；
- [ ] 删除成功后刷新资料列表；
- [ ] 删除成功后清理或刷新搜索结果；
- [ ] 删除失败时显示明确错误。

前端删除确认文案建议：

```text
确定要删除这份资料吗？此操作会删除该资料的原文件副本、解析结果、chunks 和索引。
```

### 8.4 tester 搜索资料

- [ ] 调用 `GET /api/materials/search`；
- [ ] 默认搜索 `tester`；
- [ ] 展示命中的 chunk；
- [ ] 展示 material_id；
- [ ] 展示 chunk_id；
- [ ] 展示 score；
- [ ] 展示 asset_paths，如果有；
- [ ] 没有结果时显示友好提示。

---

## 9. 推荐 API 设计

本阶段后端至少应具备：

```text
POST   /api/materials/upload
GET    /api/materials/list
GET    /api/materials/search
DELETE /api/materials/{material_id}
```

### 9.1 POST /api/materials/upload

输入：

```text
file
user_id，可选，默认 tester
subject，可选，默认 unknown
material_type，可选，默认 unknown
```

输出建议：

```json
{
  "ok": true,
  "material_id": "string",
  "user_id": "tester",
  "parse_status": "ready",
  "manifest_path": "string",
  "markdown_path": "string|null",
  "chunk_count": 0,
  "error": null
}
```

### 9.2 GET /api/materials/list

输入：

```text
user_id，可选，默认 tester
subject，可选
material_type，可选
```

### 9.3 GET /api/materials/search

输入：

```text
user_id，可选，默认 tester
query，必填
top_k，可选，默认 5
material_id，可选
subject，可选
material_type，可选
```

### 9.4 DELETE /api/materials/{material_id}

输入：

```text
path: material_id
query/header/body: user_id，可选，默认 tester
```

输出建议：

```json
{
  "ok": true,
  "user_id": "tester",
  "material_id": "string",
  "deleted": true
}
```

---

## 10. 删除功能安全要求

删除功能必须非常谨慎。

### 10.1 路径校验

必须确认待删除目录在：

```text
data/user_materials/{user_id}/
```

之下。

推荐逻辑：

```python
base = DATA_DIR / "user_materials" / safe_user_id
target = base / safe_material_id
target.resolve().relative_to(base.resolve())
```

如果 `relative_to` 失败，拒绝删除。

### 10.2 ID 校验

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

### 10.3 删除范围

允许删除：

```text
data/user_materials/{user_id}/{material_id}/
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

### 10.4 删除失败

删除失败时返回清晰错误：

```text
Invalid material_id
Material not found
Permission denied
Failed to delete material
```

不要静默失败。

---

## 11. 前端交互建议

资料库页面推荐结构：

```text
我的资料库
├── 当前用户
│   └── user_id 输入框，默认 tester
│
├── 上传资料
│   ├── 文件选择
│   ├── 学科选择
│   ├── 资料类型选择
│   └── 上传按钮
│
├── 资料列表
│   ├── 刷新按钮
│   ├── 文件名
│   ├── 学科
│   ├── 类型
│   ├── 状态
│   ├── chunks
│   └── 删除按钮
│
└── 搜索资料库
    ├── 搜索框
    └── 搜索结果
```

上传成功提示：

```text
资料已入库，生成 {chunk_count} 个 chunks
```

删除成功提示：

```text
资料已删除
```

搜索无结果提示：

```text
当前用户资料库中没有找到相关内容
```

上传、列表、删除、搜索失败都必须在页面显示错误，不要只写 `console.error`。

---

## 12. 当前阶段不要求的功能

本阶段不要求：

```text
聊天中上传并自动入库
资料库自然语言助手
根据资料生成总结
根据资料制定复习计划
PDF/MinerU 完整解析
ZIP 批量上传
登录注册
复杂权限系统
Obsidian 插件
```

---

## 13. 验证命令

### 13.1 启动 Web

```bash
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

浏览器打开：

```text
http://127.0.0.1:8000
```

进入“我的资料库”，默认用户应为：

```text
tester
```

### 13.2 CLI 验证

```bash
python scripts/ingest_material.py --user-id tester --file data/demo/test.md
python scripts/ingest_material.py --user-id tester --file data/demo/test.txt
python scripts/query_materials.py --user-id tester --query "罗尔定理"
```

### 13.3 API 验证

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

### 13.4 用户隔离验证

需要验证：

- [ ] `tester` 上传的资料只进入 `data/user_materials/tester/`；
- [ ] `tester` 只能 list 自己的资料；
- [ ] `tester` 只能 search 自己的资料；
- [ ] `tester` 只能 delete 自己的资料；
- [ ] `tester` 删除不了 `test_user_a` 或 `test_user_b` 的资料；
- [ ] 不传 user_id 时默认使用 `tester`。

### 13.5 原有功能验证

尽量运行：

```bash
python scripts/ask_kaoyan.py 极限是什么 --no-memory --format terminal
python scripts/ask_math.py 极限是什么 --no-memory --format terminal
python -m unittest tests.test_agent_runtime
```

如果 Qwen 403 导致问答命令失败，说明是账号额度问题，不要误判为资料库模块失败。

---

## 14. 完成汇报要求

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

## 15. 当前阶段完成标准

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

## 16. 后续阶段建议

完成本阶段后，再考虑：

1. 资料详情页；
2. 查看 chunks；
3. 重新解析；
4. PDF/MinerU 接入；
5. 图片 OCR / VLM caption；
6. 聊天中上传并入库；
7. 聊天中根据用户资料库回答；
8. 资料库自然语言助手；
9. Obsidian 插件客户端接入。
