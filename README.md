# 考研政治资料库 Demo

这是一个最小可用的政治知识库原型：

1. 把政治资料放到 `data/raw/politics/`
2. 运行脚本切块并写入本地 JSONL 向量文件
3. 用查询脚本检索相关知识点
4. 用 `qwen-max` 基于检索结果生成回答

## 安装依赖

```powershell
pip install -r requirements.txt
```

## 配置 Qwen / 百炼

项目读取本地 `.env`：

```text
DASHSCOPE_API_KEY=你的百炼或 DashScope API Key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EMBEDDING_MODEL=text-embedding-v4
EMBEDDING_DIMENSIONS=1024
QWEN_CHAT_MODEL=qwen-max
QWEN_GLOBAL_MODEL=qwen-max
QWEN_VL_MODEL=qwen-vl-max
QWEN_MATH_MODEL=qwen-math-plus
QWEN_TEMPERATURE=0.2
```

如需启用 Coze 时政小智能体，在本地 `.env` 中继续配置：

```powershell
$env:COZE_API_BASE="https://api.coze.cn"
$env:COZE_API_TOKEN="你的 Coze PAT Token"
$env:COZE_BOT_ID="你的 Coze Bot ID"
```

也可以写入 `.env`：

```text
COZE_API_BASE=https://api.coze.cn
COZE_API_TOKEN=你的 Coze PAT Token
COZE_BOT_ID=你的 Coze Bot ID
COZE_TIMEOUT_SECONDS=180
COZE_DEBUG=false
```

不要把真实 API Key 或 PAT Token 提交到 README 或代码仓库。

`text-embedding-v4` 用来做资料库向量检索，`qwen-max` 用来生成最终回答。

数学真题 agent 中：

- `QWEN_GLOBAL_MODEL`：全局总控，默认 `qwen-max`，负责识别意图、年份题号、是否需要解题。
- `QWEN_VL_MODEL`：图片解释器，只在用户提供图片时启用，负责 OCR、公式识别和图形说明。
- `QWEN_MATH_MODEL`：数学解题节点，负责生成解题步骤。
- `COZE_BOT_ID`：时政信息小智能体，由总控识别到时政请求后调用。
- 解题结果会与本地答案速查核对；若不一致，最多让 `QWEN_MATH_MODEL` 重算 3 次。

## 构建政治知识库

```powershell
python scripts/build_politics_db.py
```

## 只检索资料

```powershell
python scripts/query_politics.py "主要矛盾和矛盾的主要方面有什么区别"
```

## 检索后调用 qwen-max 回答

```powershell
python scripts/ask_politics.py "主要矛盾和矛盾的主要方面有什么区别"
```

资料库生成在 `data/processed/politics_vectors.jsonl`。资料量变大后，可以再把这一层替换成 Chroma、Milvus 或 pgvector。

## 考研小助手统一入口

统一入口由 `qwen-max` 做总控路由，目前已接入：

- 数学一真题展示与解析；
- 普通数学题文字解答；
- Qwen-VL 数学图片 OCR；
- Qwen-Math 数学解题；
- Coze 时政小智能体。

当前脚本结构：

- `scripts/ask_kaoyan.py`：推荐使用的统一命令行入口；
- `scripts/kaoyan_agent.py`：考研小助手总控 agent；
- `scripts/kaoyan_tools.py`：LangChain-style 工具层，将真题检索、图片 OCR、数学解题、答案核对和时政查询封装为 Tool；
- `scripts/math_agent.py`：旧兼容层，转发到 `kaoyan_agent.py`；
- `scripts/ask_math.py`：旧兼容入口，转发到 `kaoyan_agent.py`。

当前总控 agent 仍保留自定义路由逻辑，但具体能力已通过工具层调用：

- `search_math_exam`：查询数学一真题题目与答案速查；
- `ocr_math_image`：调用 Qwen-VL 识别数学图片；
- `solve_math_exam`：调用 Qwen-Math 解答数学一真题；
- `solve_general_math`：调用 Qwen-Math 解答普通数学题；
- `judge_math_answer`：核对模型答案与本地标准答案；
- `get_current_affairs`：调用 Coze 时政小智能体。

如果安装了 `langchain-core`，这些工具会以 `StructuredTool` 形式创建；未安装时会退回到兼容的本地 `LocalTool`，仍然支持 `.invoke(...)` 调用。

只展示题目：

```powershell
python scripts/ask_kaoyan.py "2017 年数学一第 21 题"
```

解答并核对答案：

```powershell
python scripts/ask_kaoyan.py "2017 年数学一第 21 题解析"
```

终端友好输出：

```powershell
python scripts/ask_kaoyan.py "2017 年数学一第 21 题解析" --format terminal
```

前端/UI 输出（默认，保留 Markdown/LaTeX，适合 KaTeX/MathJax 渲染）：

```powershell
python scripts/ask_kaoyan.py "2017 年数学一第 21 题解析" --format ui
```

带图片输入时会先启用 Qwen-VL：

```powershell
python scripts/ask_kaoyan.py "这张数学题怎么做" --image "E:\桌面\数学\题目.png" --format terminal
```

普通数学题不需要年份题号：

```powershell
python scripts/ask_kaoyan.py "求极限 lim_{x->0} (sin x - x)/x^3" --format terminal
```

时政信息会调用 Coze 小智能体：

```powershell
python scripts/ask_kaoyan.py "请帮我整理2026年3月考研政治时政信息" --format terminal
```

旧入口 `scripts/ask_math.py` 仍保留兼容，但后续建议使用 `scripts/ask_kaoyan.py`。

## 本地 Web UI

安装依赖：

```powershell
pip install -r requirements.txt
```

启动服务：

```powershell
python -m uvicorn scripts.web_server:app --host 127.0.0.1 --port 8000
```

然后浏览器打开：

```text
http://127.0.0.1:8000
```

Web UI 默认使用 `ui` 输出格式，保留 Markdown 和 LaTeX，并在浏览器中用 KaTeX 渲染数学公式。
