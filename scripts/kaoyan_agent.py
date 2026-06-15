from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from dotenv import load_dotenv
from kaoyan_tools import create_kaoyan_toolkit

ROOT = Path(__file__).resolve().parents[1]
MATH_EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
MATH_EXAM_QUESTION_DIRS = {
    "math1": MATH_EXAM_ROOT / "math1",
    "math2": MATH_EXAM_ROOT / "math2",
    "math3": MATH_EXAM_ROOT / "math3",
}
MATH_EXAM_LABELS = {"math1": "数学一", "math2": "数学二", "math3": "数学三"}
SESSION_DIR = ROOT / "data" / "runtime" / "sessions"
SESSION_VECTOR_DIR = ROOT / "data" / "runtime" / "session_vectors"
SESSION_MAX_TURNS = 20
_TOOLKIT = None


QWEN_VL_OCR_PROMPT = """你是考研数学图片 OCR 节点。
只识别图片中的题干、公式、选项、图形条件和表格；不要解题。
图形题必须按图中可见元素描述：坐标轴、刻度、点、直线/曲线、阴影、箭头、区域标号、选项小图。
有区域标号或阴影时，逐一写出每个区域的实际边界、相对位置、可读出的不等式或参数范围；不要只凭标签位置、题号顺序或常见图形模板推断。
看不清的符号用 [不确定: ...] 标出。输出 Markdown。"""


IMAGE_ROUTING_OCR_PROMPT = """你是考研助手的通用图片预识别节点。
只做 OCR、图像内容概述和学科线索判断；不要解题，不要回答用户问题。
图片可能是数学题、政治材料、英语文本、时政截图、表格、图形或其他内容。
不要根据文件名判断学科；只依据图片可见内容和用户文字补充。

只输出 JSON：
{"ocr_text":"图片中可识别的文字、公式、题干、选项或材料原文","visual_summary":"非文字视觉信息概述，如图像/表格/坐标轴/材料版式","subject_hint":"math|politics|english|current_affairs|unknown","confidence":0.0,"reason":"一句话说明"}

规则：
- subject_hint 只是线索；证据不足时用 unknown。
- 数学题常见证据：函数、极限、积分、矩阵、概率、几何图形、坐标轴、公式推导、选择/填空/解答题数学表达。
- 政治常见证据：马克思主义、中国特色社会主义、毛中特、史纲、思修、政策理论材料。
- current_affairs 常见证据：近期会议、政策、领导人活动、国际国内新闻热点。
- english 常见证据：英文阅读、完形、翻译、写作题、英语选项或长段英文。
- 看不清的内容在 ocr_text 中用 [不确定: ...] 标出。
"""


QWEN_MATH_SOLVER_PROMPT = """你是严谨的考研数学解题节点。
要求：
1. 严格基于输入题目和工具上下文，不要编造题目条件。
2. 先给关键思路，再给必要步骤，最后单独写“最终答案”。
3. 若提供标准答案速查，只用于最终核对，不要跳步抄答案。
4. 对选择题给出选项字母和理由；填空题给出填空结果；解答题按小问组织。
5. 图形题必须先根据题干和 OCR 写出区域、曲线、坐标轴或标号的准确含义；不要用区域名称、标签方位、常见模板或选项答案反推图形条件。
6. 二重积分图形题必须使用完整区域边界；若某区域关于 x 轴对称且被积函数关于 y 是奇函数，应先判定该区域积分为 0，不要只取上半区或下半区。
7. 如果收到核对反馈，优先定位错误并重新计算。"""


QWEN_GENERAL_MATH_SOLVER_PROMPT = """你是通用数学解题节点。
要求：
1. 只基于用户题目、历史上下文和 OCR 文本作答。
2. 条件不完整时先说明缺少什么；能在合理继承历史参数时，明确写出继承了哪些参数。
3. 先给关键思路，再给必要步骤，最后单独写“最终答案”。
4. 不要声称查阅本地真题库。"""


TERMINAL_FORMAT_PROMPT = """输出格式：terminal
面向 PowerShell 终端阅读；少用复杂表格；公式尽量简洁。"""


UI_FORMAT_PROMPT = """输出格式：ui
可以使用 Markdown 和 LaTeX，适合网页 KaTeX/MathJax 渲染。"""


ANSWER_JUDGE_PROMPT = """你是答案核对节点。判断“模型解答”的最终答案是否与“标准答案速查”核心一致。
只比较最终结论，不要求步骤完全一致。输出 JSON：
{"match": true/false, "reason": "原因", "expected": "标准答案核心", "actual": "模型答案核心"}
不要输出 JSON 以外的文字。"""


SOLUTION_QUALITY_PROMPT = """你是数学解题过程审核节点。检查“模型解答”的推导是否有明显数学错误。
输出 JSON：
{"valid": true/false, "reason": "原因", "fix_hint": "若 invalid，指出关键修正点"}
不要输出 JSON 以外的文字。"""


@dataclass
class AgentSettings:
    api_key: str | None
    base_url: str
    global_model: str
    vl_model: str
    math_model: str
    embedding_model: str
    embedding_dimensions: int
    temperature: float
    coze_api_base: str
    coze_api_token: str | None
    coze_bot_id: str | None
    coze_timeout_seconds: int
    coze_debug: bool


@dataclass
class Route:
    subject: str
    intent: str
    year: int | None
    question_number: int | None
    need_vl: bool
    notes: str = ""
    exam_type: str | None = None


@dataclass
class MathProblem:
    exam_type: str
    year: int
    question_number: int
    question_text: str
    answer_text: str | None
    question_source: Path
    answer_source: Path | None


@dataclass
class AgentResult:
    answer: str
    route: Route
    memory_payload: dict[str, Any]


def get_toolkit():
    global _TOOLKIT
    if _TOOLKIT is None:
        _TOOLKIT = create_kaoyan_toolkit(sys.modules[__name__])
    return _TOOLKIT


def load_settings() -> AgentSettings:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    chat_model = os.getenv("QWEN_CHAT_MODEL", "qwen-max")
    return AgentSettings(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        global_model=os.getenv("QWEN_GLOBAL_MODEL", chat_model),
        vl_model=os.getenv("QWEN_VL_MODEL", "qwen-vl-max"),
        math_model=os.getenv("QWEN_MATH_MODEL", "qwen-math-plus"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-v4"),
        embedding_dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "1024")),
        temperature=float(os.getenv("QWEN_TEMPERATURE", "0.2")),
        coze_api_base=os.getenv("COZE_API_BASE", "https://api.coze.cn").rstrip("/"),
        coze_api_token=os.getenv("COZE_API_TOKEN"),
        coze_bot_id=os.getenv("COZE_BOT_ID"),
        coze_timeout_seconds=int(os.getenv("COZE_TIMEOUT_SECONDS", "180")),
        coze_debug=os.getenv("COZE_DEBUG", "").lower() in {"1", "true", "yes", "on"},
    )


def make_client():
    settings = load_settings()
    if not settings.api_key:
        raise RuntimeError("请先在 .env 中设置 DASHSCOPE_API_KEY。")
    from openai import OpenAI

    return OpenAI(api_key=settings.api_key, base_url=settings.base_url)


def chat_text(model: str, system_prompt: str, user_prompt: str, temperature: float | None = None) -> str:
    settings = load_settings()
    client = make_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.temperature if temperature is None else temperature,
    )
    return response.choices[0].message.content or ""


def global_model_name() -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return os.getenv("ROUTER_MODEL") or load_settings().global_model


def global_temperature(default: float | None = None) -> float | None:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    value = os.getenv("ROUTER_TEMPERATURE")
    if value is None or not value.strip():
        return default
    try:
        return float(value)
    except ValueError:
        return default


def make_global_client():
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    router_model = os.getenv("ROUTER_MODEL")
    router_api_key = os.getenv("ROUTER_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    router_base_url = os.getenv("ROUTER_BASE_URL") or os.getenv("DEEPSEEK_BASE_URL")
    if not router_model or not router_api_key or not router_base_url:
        return make_client()
    from openai import OpenAI

    return OpenAI(api_key=router_api_key, base_url=router_base_url)


def chat_global_text(system_prompt: str, user_prompt: str, temperature: float | None = None) -> str:
    settings = load_settings()
    client = make_global_client()
    response = client.chat.completions.create(
        model=global_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=global_temperature(settings.temperature if temperature is None else temperature),
    )
    return response.choices[0].message.content or ""


def parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    match = re.search(r"\{.*\}", stripped, flags=re.S)
    if not match:
        raise ValueError(f"Model did not return JSON: {text}")
    return json.loads(match.group(0))


def safe_session_id(session_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", session_id.strip())
    return cleaned or "default"


def session_path(session_id: str) -> Path:
    return SESSION_DIR / f"{safe_session_id(session_id)}.json"


def load_session(session_id: str) -> dict[str, Any]:
    path = session_path(session_id)
    if not path.exists():
        return {"session_id": safe_session_id(session_id), "turns": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"session_id": safe_session_id(session_id), "turns": []}


def save_session(session_id: str, session: dict[str, Any]) -> None:
    path = session_path(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    session["turns"] = session.get("turns", [])[-SESSION_MAX_TURNS:]
    session["session_id"] = safe_session_id(session_id)
    session["updated_at"] = datetime.now().isoformat(timespec="seconds")
    path.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")


def session_vector_path(session_id: str) -> Path:
    return SESSION_VECTOR_DIR / safe_session_id(session_id)


def store_turn_vector(session_id: str, turn: dict[str, Any]) -> None:
    """Compatibility no-op.

    The current runtime uses the Markdown/JSON short-term session only.  The
    old LanceDB long-term memory path is intentionally disabled to avoid an
    extra embedding API call on every turn.
    """


def turn_full_text(turn: dict[str, Any]) -> str:
    return (
        f"User:\n{turn.get('user_query') or ''}\n\n"
        f"Assistant:\n{turn.get('assistant_answer') or turn.get('assistant_answer_preview') or ''}"
    ).strip()


def recent_session_full_context(session: dict[str, Any], max_turns: int = 15) -> str:
    turns = session.get("turns", [])[-max_turns:]
    if not turns:
        return "No recent turns."
    blocks = []
    for turn in turns:
        blocks.append(f"[turn {turn.get('turn_id', '?')} at {turn.get('time', '')}]\n{turn_full_text(turn)}")
    return "\n\n".join(blocks)


def normalize_exam_type(exam_type: str | None) -> str:
    value = (exam_type or "math1").strip().lower()
    aliases = {
        "数学一": "math1",
        "数一": "math1",
        "math1": "math1",
        "1": "math1",
        "数学二": "math2",
        "数二": "math2",
        "math2": "math2",
        "2": "math2",
        "数学三": "math3",
        "数三": "math3",
        "math3": "math3",
        "3": "math3",
    }
    return aliases.get(value, value)


def exam_label(exam_type: str | None) -> str:
    return MATH_EXAM_LABELS.get(normalize_exam_type(exam_type), "数学")


def exam_questions_dir(exam_type: str | None) -> Path:
    clean_type = normalize_exam_type(exam_type)
    configured = MATH_EXAM_QUESTION_DIRS.get(clean_type)
    if configured is None:
        raise ValueError(f"Unsupported math exam type: {exam_type}")
    return configured


def question_path(year: int, exam_type: str | None = "math1") -> Path:
    clean_type = normalize_exam_type(exam_type)
    return exam_questions_dir(clean_type) / str(year) / f"{clean_type}_{year}_questions.md"


def answer_path(year: int, exam_type: str | None = "math1") -> Path:
    clean_type = normalize_exam_type(exam_type)
    return exam_questions_dir(clean_type) / str(year) / f"{clean_type}_{year}_answers.md"


def extract_question(markdown: str, question_number: int) -> str:
    lines = markdown.splitlines()
    heading_pattern = re.compile(r"^#{2,3}\s+")
    metadata_pattern = re.compile(r"^\s*[-*]\s*题号[：:]\s*" + re.escape(str(question_number)) + r"\s*$")
    heading_number_pattern = re.compile(
        r"(?:第\s*" + re.escape(str(question_number)) + r"\s*题|(?:选择题|填空题|解答题)\s*" + re.escape(str(question_number)) + r")\s*$"
    )

    headings = [index for index, line in enumerate(lines) if heading_pattern.match(line)]
    for position, start in enumerate(headings):
        end = headings[position + 1] if position + 1 < len(headings) else len(lines)
        block_lines = lines[start:end]
        heading = block_lines[0]
        has_matching_metadata = any(metadata_pattern.match(line) for line in block_lines)
        has_matching_heading = heading.startswith("### ") and bool(heading_number_pattern.search(heading))
        if has_matching_metadata or has_matching_heading:
            return "\n".join(block_lines).strip()

    raise ValueError(f"未找到第 {question_number} 题。")


def extract_answer(markdown: str, question_number: int) -> str | None:
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == str(question_number):
            return cells[1]
    return None


def load_problem(year: int, question_number: int, exam_type: str | None = "math1") -> MathProblem:
    clean_type = normalize_exam_type(exam_type)
    q_path = question_path(year, clean_type)
    if not q_path.exists():
        raise FileNotFoundError(f"暂未找到 {year} 年{exam_label(clean_type)}真题文件：{q_path}")
    question_text = extract_question(q_path.read_text(encoding="utf-8"), question_number)

    a_path = answer_path(year, clean_type)
    answer_text = extract_answer(a_path.read_text(encoding="utf-8"), question_number) if a_path.exists() else None
    return MathProblem(
        exam_type=clean_type,
        year=year,
        question_number=question_number,
        question_text=question_text,
        answer_text=answer_text,
        question_source=q_path,
        answer_source=a_path if a_path.exists() else None,
    )


def math_problem_from_tool_payload(payload: dict[str, Any]) -> MathProblem:
    return MathProblem(
        exam_type=normalize_exam_type(payload.get("exam_type")),
        year=int(payload["year"]),
        question_number=int(payload["question_number"]),
        question_text=str(payload["question_text"]),
        answer_text=payload.get("answer_text"),
        question_source=Path(payload["question_source"]),
        answer_source=Path(payload["answer_source"]) if payload.get("answer_source") else None,
    )


def markdown_image_targets(markdown: str) -> list[str]:
    targets: list[str] = []
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", markdown):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        else:
            target = target.split()[0].strip("'\"")
        if not target or target.startswith("#"):
            continue
        if target.lower().startswith(("http://", "https://", "data:")):
            continue
        targets.append(unquote(target))
    return targets


def resolve_markdown_image_paths(markdown: str, base_dir: Path) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    for target in markdown_image_targets(markdown):
        path = Path(target)
        if not path.is_absolute():
            path = base_dir / path
        try:
            resolved = path.resolve()
        except OSError:
            continue
        key = str(resolved).lower()
        if key in seen or not resolved.is_file():
            continue
        paths.append(resolved)
        seen.add(key)
    return paths


def question_needs_group_visual_context(markdown: str) -> bool:
    content_lines = [line for line in markdown.splitlines() if not line.strip().startswith("- ")]
    content = "\n".join(content_lines)
    return bool(re.search(r"(如图|右图|左图|下图|图所示|图示|图像|配图)", content))


def question_group_markdown(markdown: str, question_number: int) -> str:
    lines = markdown.splitlines()
    headings: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{2,3})\s+", line)
        if match:
            headings.append((index, len(match.group(1))))

    metadata_pattern = re.compile(r"^\s*[-*]\s*题号[：:]\s*" + re.escape(str(question_number)) + r"\s*$")
    heading_pattern = re.compile(r"^###\s+第\s*" + re.escape(str(question_number)) + r"\s*题\s*$")
    for position, (start, level) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        block_lines = lines[start:end]
        if level != 3:
            continue
        if not (heading_pattern.match(block_lines[0]) or any(metadata_pattern.match(line) for line in block_lines)):
            continue
        group_start = None
        for previous_start, previous_level in reversed(headings[:position]):
            if previous_level == 2:
                group_start = previous_start
                break
        if group_start is None:
            return ""
        return "\n".join(lines[group_start:start]).strip()
    return ""


def problem_image_paths(problem: MathProblem) -> list[Path]:
    base_dir = problem.question_source.parent
    direct_paths = resolve_markdown_image_paths(problem.question_text, base_dir)
    if direct_paths:
        return direct_paths
    if not question_needs_group_visual_context(problem.question_text):
        return []
    try:
        full_markdown = problem.question_source.read_text(encoding="utf-8")
    except OSError:
        return []
    return resolve_markdown_image_paths(question_group_markdown(full_markdown, problem.question_number), base_dir)


def image_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{data}"


def ocr_images_with_qwenvl(image_paths: list[Path], user_query: str) -> str:
    settings = load_settings()
    client = make_client()
    image_list = "\n".join(f"{index}. {path}" for index, path in enumerate(image_paths, start=1))
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                f"用户文字补充：{user_query}\n\n"
                f"图片顺序：\n{image_list or '无'}\n\n"
                "请只做 OCR、公式识别和图形说明，不要解题。若图片来自整页真题截图，请优先识别用户指定题号相关区域。"
            ),
        }
    ]
    for path in image_paths:
        if not path.exists():
            raise FileNotFoundError(f"图片不存在：{path}")
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(path)}})
    response = client.chat.completions.create(
        model=settings.vl_model,
        messages=[
            {"role": "system", "content": QWEN_VL_OCR_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""


def recognize_images_for_routing(image_paths: list[Path], user_query: str, client: Any | None = None) -> dict[str, Any]:
    settings = load_settings()
    client = client or make_client()
    image_list = "\n".join(f"{index}. {path}" for index, path in enumerate(image_paths, start=1))
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                f"用户文字补充：{user_query}\n\n"
                f"图片顺序：\n{image_list or '无'}\n\n"
                "请输出 JSON，用于后续学科分类、追问判定和父节点定位。"
            ),
        }
    ]
    for path in image_paths:
        if not path.exists():
            raise FileNotFoundError(f"图片不存在：{path}")
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(path)}})
    response = client.chat.completions.create(
        model=settings.vl_model,
        messages=[
            {"role": "system", "content": IMAGE_ROUTING_OCR_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0,
    )
    raw = response.choices[0].message.content or "{}"
    try:
        data = parse_json_object(raw)
    except Exception:
        data = {"ocr_text": raw, "visual_summary": "", "subject_hint": "unknown", "confidence": 0.0, "reason": "image_routing_json_parse_failed"}
    subject_hint = str(data.get("subject_hint") or "unknown")
    if subject_hint not in {"math", "politics", "english", "current_affairs", "unknown"}:
        subject_hint = "unknown"
    try:
        confidence = float(data.get("confidence", 0.0) or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0
    return {
        "ocr_text": str(data.get("ocr_text") or "").strip(),
        "visual_summary": str(data.get("visual_summary") or "").strip(),
        "subject_hint": subject_hint,
        "confidence": max(0.0, min(1.0, confidence)),
        "reason": str(data.get("reason") or "").strip(),
    }


def build_coze_current_affairs_prompt(user_query: str) -> str:
    current_date = datetime.now().date().isoformat()
    return (
        "请按考研政治时政复习口径回答用户问题。优先整理具体事件、时间、来源、关键词、"
        "对应模块和可能考查角度；不要编造未提供或无法确认的信息。\n"
        f"当前日期：{current_date}\n\n用户问题：{user_query}"
    )


def call_coze_current_affairs(user_query: str, timeout_seconds: int | None = None) -> str:
    settings = load_settings()
    if not settings.coze_api_token or not settings.coze_bot_id:
        raise RuntimeError("请先在 .env 中设置 COZE_API_TOKEN 和 COZE_BOT_ID。")
    timeout_seconds = timeout_seconds or settings.coze_timeout_seconds

    import requests

    headers = {
        "Authorization": f"Bearer {settings.coze_api_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "bot_id": settings.coze_bot_id,
        "user_id": "kaoyan_assistant_cli",
        "stream": False,
        "additional_messages": [
            {
                "role": "user",
                "content": build_coze_current_affairs_prompt(user_query),
                "content_type": "text",
            }
        ],
    }
    response = requests.post(f"{settings.coze_api_base}/v3/chat", headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    chat_data = data.get("data") or data
    chat_id = chat_data.get("id") or chat_data.get("chat_id")
    conversation_id = chat_data.get("conversation_id")
    if not chat_id or not conversation_id:
        direct_answer = extract_coze_answer(data)
        if direct_answer:
            return direct_answer
        raise RuntimeError(f"Coze response missing chat id or conversation id: {data}")

    deadline = time.time() + timeout_seconds
    status = chat_data.get("status")
    while status not in {"completed", "failed", "requires_action", "canceled"} and time.time() < deadline:
        time.sleep(2)
        retrieve = requests.get(
            f"{settings.coze_api_base}/v3/chat/retrieve",
            headers=headers,
            params={"conversation_id": conversation_id, "chat_id": chat_id},
            timeout=30,
        )
        retrieve.raise_for_status()
        status = (retrieve.json().get("data") or retrieve.json()).get("status")

    answer = fetch_coze_answer_messages(settings, headers, conversation_id, chat_id)
    if answer:
        return answer
    if status != "completed":
        raise TimeoutError(f"Coze 时政智能体仍在处理，当前状态为 {status}，已等待 {timeout_seconds} 秒。")
    raise RuntimeError("Coze message list did not contain an answer.")


def fetch_coze_answer_messages(
    settings: AgentSettings,
    headers: dict[str, str],
    conversation_id: str,
    chat_id: str,
) -> str:
    import requests

    messages = requests.get(
        f"{settings.coze_api_base}/v3/chat/message/list",
        headers=headers,
        params={"conversation_id": conversation_id, "chat_id": chat_id},
        timeout=30,
    )
    messages.raise_for_status()
    payload = messages.json()
    if settings.coze_debug:
        debug_coze_payload(payload)
    return extract_coze_answer(payload)


def extract_coze_answer(payload: dict[str, Any]) -> str:
    data = payload.get("data", payload)
    messages: list[dict[str, Any]] = []
    if isinstance(data, list):
        messages = [item for item in data if isinstance(item, dict)]
    elif isinstance(data, dict):
        for key in ("messages", "message_list", "items"):
            value = data.get(key)
            if isinstance(value, list):
                messages = [item for item in value if isinstance(item, dict)]
                break

    answer_candidates: list[str] = []
    assistant_candidates: list[str] = []
    other_candidates: list[str] = []
    for item in messages:
        role = item.get("role")
        message_type = item.get("type")
        content_type = item.get("content_type")
        content = item.get("content")
        if not content:
            continue
        if message_type == "answer":
            answer_candidates.append(str(content))
        elif role == "assistant" and content_type == "text":
            assistant_candidates.append(str(content))
        elif role == "assistant" or message_type in {"verbose"}:
            other_candidates.append(str(content))
    for candidates in (answer_candidates, assistant_candidates, other_candidates):
        if candidates:
            return candidates[-1].strip()

    if isinstance(data, dict):
        for key in ("content", "answer", "output"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def debug_coze_payload(payload: dict[str, Any]) -> None:
    data = payload.get("data", payload)
    messages = data if isinstance(data, list) else data.get("messages", []) if isinstance(data, dict) else []
    print("\n[COZE DEBUG] message count:", len(messages))
    for index, item in enumerate(messages, start=1):
        content = str(item.get("content") or "")
        print(
            f"[COZE DEBUG] #{index} role={item.get('role')} "
            f"type={item.get('type')} content_type={item.get('content_type')} "
            f"len={len(content)} preview={content[:120].replace(chr(10), ' ')}"
        )


def solve_with_qwenmath(
    problem: MathProblem,
    user_query: str,
    vl_text: str | None,
    output_format: str = "ui",
    feedback: str | None = None,
) -> str:
    settings = load_settings()
    prompt_parts = [
        f"用户问题：{user_query}",
        f"资料库题目：\n{problem.question_text}",
    ]
    if vl_text:
        prompt_parts.append(f"Qwen-VL 图片识别结果：\n{vl_text}")
    if problem.answer_text:
        prompt_parts.append(f"标准答案速查（仅用于最后核对）：{problem.answer_text}")
    if feedback:
        prompt_parts.append(f"上一轮核对反馈：{feedback}")
    prompt_parts.append(TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT)
    prompt_parts.append("图形积分题请先列出每个相关区域的完整边界或参数范围，再判断奇偶性、对称性和抵消关系；不要根据标签方位或常见模板跳过建模。")
    prompt_parts.append("请给出清晰解题步骤，并在末尾写“最终答案：...”。")
    return chat_text(settings.math_model, QWEN_MATH_SOLVER_PROMPT, "\n\n".join(prompt_parts))


def solve_general_math_with_qwenmath(
    user_query: str,
    vl_text: str | None,
    output_format: str = "ui",
) -> str:
    settings = load_settings()
    prompt_parts = [f"用户题目/问题：{user_query}"]
    if vl_text:
        prompt_parts.append(f"Qwen-VL 图片识别结果：\n{vl_text}")
    prompt_parts.append(TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT)
    prompt_parts.append(
        "请解答这道普通数学题。若本轮是参数修改或追问，请继承历史中未被显式修改的函数、展开点、目标点、阶数和误差要求。"
    )
    return chat_text(settings.math_model, QWEN_GENERAL_MATH_SOLVER_PROMPT, "\n\n".join(prompt_parts))


def judge_answer(problem: MathProblem, solution: str) -> dict[str, Any]:
    if not problem.answer_text:
        return {"match": True, "reason": "资料库没有标准答案，跳过核对。", "expected": "", "actual": ""}
    prompt = (
        f"题目：\n{problem.question_text}\n\n"
        f"标准答案速查：{problem.answer_text}\n\n"
        f"模型解答：\n{solution}\n\n"
        "请判断核心最终答案是否一致。"
    )
    try:
        return parse_json_object(chat_global_text(ANSWER_JUDGE_PROMPT, prompt, temperature=0))
    except Exception as exc:
        return {"match": False, "reason": f"核对 JSON 解析失败：{exc}", "expected": problem.answer_text, "actual": ""}


def judge_solution_quality(problem: MathProblem, solution: str) -> dict[str, Any]:
    prompt = f"题目：\n{problem.question_text}\n\n标准答案：{problem.answer_text or '无'}\n\n模型解答：\n{solution}"
    try:
        return parse_json_object(chat_global_text(SOLUTION_QUALITY_PROMPT, prompt, temperature=0))
    except Exception as exc:
        return {"valid": True, "reason": f"过程审核失败，跳过：{exc}", "fix_hint": ""}


def render_answer_only(answer_text: str) -> str:
    cleaned = re.sub(r"`([^`]+)`", r"\1", answer_text.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return f"最终答案：{cleaned}"


def render_standard_answer_with_explanation(
    problem: MathProblem,
    user_query: str,
    vl_text: str | None = None,
    output_format: str = "ui",
) -> str:
    if not problem.answer_text:
        return ""
    settings = load_settings()
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = (
        f"用户请求：{user_query}\n\n"
        f"题目：\n{problem.question_text}\n\n"
        f"标准答案速查：{problem.answer_text}\n\n"
        f"图片识别结果：\n{vl_text or '无'}\n\n"
        f"{format_hint}\n\n"
        "请以标准答案为最终结论，给一段简短、可核对的解释。"
    )
    try:
        explanation = chat_text(settings.math_model, "你是考研数学真题纠偏讲解节点。", prompt, temperature=0).strip()
    except Exception:
        return render_answer_only(problem.answer_text)
    if not explanation:
        return render_answer_only(problem.answer_text)
    if "最终答案" not in explanation:
        explanation = f"{explanation.rstrip()}\n\n{render_answer_only(problem.answer_text)}"
    return explanation


def extract_symbol_target(user_query: str, question_text: str) -> str | None:
    backtick_match = re.search(r"`([^`]+)`", user_query)
    if backtick_match:
        return normalize_symbol_name(backtick_match.group(1))
    if re.search(r"\balpha\^t\s*alpha\b|alpha\^T\s*alpha|\\alpha\^T\\alpha", user_query, flags=re.I):
        return "alpha^T alpha"
    if re.search(r"(?<![A-Za-z])E(?![A-Za-z])", user_query):
        return "E"
    match = re.search(r"([A-Za-z][A-Za-z0-9_]{0,20}|\\alpha|α)\s*(?:是什么|代表什么|什么意思|是否|是不是)", user_query)
    if match:
        return normalize_symbol_name(match.group(1))
    return None


def normalize_symbol_name(symbol: str) -> str:
    cleaned = symbol.strip().strip("，。.?？：:")
    if cleaned.lower() in {"alpha", "\\alpha", "α"}:
        return "alpha"
    if cleaned == "e":
        return "E"
    return cleaned


def clarify_symbol_from_question(target: str, question_text: str) -> str | None:
    target = normalize_symbol_name(target or "")
    if not target:
        return None
    if target == "E":
        return "`E` 表示单位矩阵，线性代数中也常记作 `I` 或 `I_n`。"
    if target in {"alpha", "alpha^T alpha"}:
        if "单位" in question_text or "unit" in question_text.lower():
            return "`alpha` 是题干中的单位列向量，因此 `alpha^T alpha = ||alpha||^2 = 1`。"
        return "`alpha` 是题干中的列向量；若题干说明它是单位向量，则有 `alpha^T alpha = 1`。"
    sentence = find_question_sentence_for_symbol(target, question_text)
    if sentence:
        return f"题干里和 `{target}` 相关的表述是：{sentence}"
    return None


def find_question_sentence_for_symbol(target: str, question_text: str) -> str | None:
    if not target:
        return None
    for part in re.split(r"[。；;\n]", question_text):
        cleaned = part.strip()
        if cleaned and re.search(re.escape(target), cleaned, flags=re.I):
            return cleaned
    return None


def clarify_symbol_with_qwen(target: str, problem: MathProblem) -> str:
    prompt = (
        f"题目：\n{problem.question_text}\n\n"
        f"用户追问的符号或对象：{target}\n\n"
        "请只解释这个符号或对象在题干中的含义，不要重新解题。"
    )
    return chat_global_text("你是考研数学真题的局部答疑助手。", prompt, temperature=0)


def explain_math_step_with_qwenmath(
    problem: MathProblem,
    user_query: str,
    previous_context: str = "",
    output_format: str = "ui",
) -> str:
    settings = load_settings()
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = (
        f"用户局部追问：{user_query}\n\n"
        f"题目：\n{problem.question_text}\n\n"
        f"原始解题过程或历史上下文：\n{previous_context or '无'}\n\n"
        f"{format_hint}\n\n"
        "请只解释用户追问的这一步、这个结论或这个疑问。不要完整重做整题。"
    )
    return chat_text(settings.math_model, "你是 Qwen-Math 局部讲解节点。", prompt, temperature=0)


def explain_math_followup_with_qwenmath(
    user_query: str,
    root_context: str,
    followup_context: str,
    followup_type: str = "contextual_followup",
    output_format: str = "ui",
) -> str:
    settings = load_settings()
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = (
        f"当前追问：{user_query}\n\n"
        f"追问类型：{followup_type}\n\n"
        f"根话题上下文：\n{root_context or '无'}\n\n"
        f"从根话题到当前追问的对话链路：\n{followup_context or '无'}\n\n"
        f"{format_hint}\n\n"
        "请只回答当前追问，必须沿着给定链路解释，不要切换到无关话题。"
        "如果链路信息不足以确定指代对象，请直接请用户澄清。"
    )
    return chat_text(settings.math_model, "你是 Qwen-Math 上下文追问讲解节点。", prompt, temperature=0)


def rewrite_math_answer_with_qwen(user_query: str, previous_context: str, output_format: str = "ui") -> str:
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = f"用户改写要求：{user_query}\n\n已有回答/上下文：\n{previous_context}\n\n{format_hint}"
    return chat_global_text("你只改写已有数学回答，不重新解题。", prompt, temperature=0.2)


def summarize_math_solution_with_qwen(user_query: str, previous_context: str, output_format: str = "ui") -> str:
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = f"用户总结要求：{user_query}\n\n已有回答/上下文：\n{previous_context}\n\n{format_hint}"
    return chat_global_text("你只总结已有数学解法，不重新解题。", prompt, temperature=0.2)


def render_question_for_user(problem: MathProblem) -> str:
    lines = problem.question_text.splitlines()
    rendered: list[str] = [f"## {problem.year} 年{exam_label(problem.exam_type)}第 {problem.question_number} 题"]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            rendered.append(line)
            continue
        if re.match(r"^#{2,3}\s+", stripped):
            continue
        if stripped.startswith("- "):
            continue
        if stripped.startswith("![") and "](" in stripped:
            continue
        if "截图" in stripped:
            continue
        rendered.append(line)
    text = "\n".join(rendered)
    text = re.sub(r"```text\s*\n", "```\n", text)
    text = re.sub(r"```\s*\n", "", text)
    text = re.sub(r"\n```", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def answer_math_query(
    user_query: str,
    image_paths: list[Path] | None = None,
    output_format: str = "ui",
    debug: bool = False,
) -> str:
    from agent_runtime import run_standard_message_loop

    return run_standard_message_loop(
        user_query,
        image_paths=image_paths or [],
        output_format=output_format,
        persist=False,
    ).answer


def answer_math_query_result(
    user_query: str,
    image_paths: list[Path] | None = None,
    output_format: str = "ui",
    debug: bool = False,
    session_id: str | None = None,
    session: dict[str, Any] | None = None,
) -> AgentResult:
    from agent_runtime import run_standard_message_loop

    result = run_standard_message_loop(
        user_query,
        session_id=session_id or "default",
        image_paths=image_paths or [],
        output_format=output_format,
        persist=False,
    )
    route = Route(result.subject, "tool_loop", None, None, False)
    return AgentResult(result.answer, route, {"route": route.__dict__, "memory": {}})


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ask the standard kaoyan assistant.")
    parser.add_argument("query", nargs="+", help="用户问题")
    parser.add_argument("--image", "-i", action="append", default=[], help="本地图片路径，可传多次")
    parser.add_argument("--format", choices=["ui", "terminal"], default="terminal")
    parser.add_argument("--session", default="default")
    parser.add_argument("--debug", action="store_true")
    return parser


def main() -> None:
    from agent_runtime import main as runtime_main

    runtime_main()


if __name__ == "__main__":
    main()
