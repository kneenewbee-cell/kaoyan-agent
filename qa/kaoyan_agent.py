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
from .kaoyan_tools import create_kaoyan_toolkit
from .prompts import load_prompt
from .tools.current_affairs_search import call_current_affairs_search
from .usage_tracking import notify_usage

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


QWEN_VL_OCR_PROMPT = load_prompt("qwen_vl_ocr_prompt")


IMAGE_ROUTING_OCR_PROMPT = load_prompt("image_routing_ocr_prompt")


QWEN_MATH_SOLVER_PROMPT = load_prompt("qwen_math_solver_prompt")


QWEN_GENERAL_MATH_SOLVER_PROMPT = load_prompt("qwen_general_math_solver_prompt")


TERMINAL_FORMAT_PROMPT = load_prompt("terminal_format_prompt")


UI_FORMAT_PROMPT = load_prompt("ui_format_prompt")


ANSWER_JUDGE_PROMPT = load_prompt("answer_judge_prompt")


SOLUTION_QUALITY_PROMPT = load_prompt("solution_quality_prompt")


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
    chat_model = os.getenv("QWEN_CHAT_MODEL", "qwen3.6-flash-2026-04-16")
    return AgentSettings(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        global_model=os.getenv("QWEN_GLOBAL_MODEL", chat_model),
        vl_model=os.getenv("QWEN_VL_MODEL", "qwen-vl-max"),
        math_model=os.getenv("QWEN_MATH_MODEL", "qwen-math-plus"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-v4"),
        embedding_dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "1024")),
        temperature=float(os.getenv("QWEN_TEMPERATURE", "0.2")),
    )


def make_client():
    settings = load_settings()
    if not settings.api_key:
        raise RuntimeError("请先在 .env 中设置 DASHSCOPE_API_KEY。")
    from openai import OpenAI

    return OpenAI(api_key=settings.api_key, base_url=settings.base_url)


def math_llm_provider() -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return (os.getenv("MATH_LLM_PROVIDER") or "dashscope").strip().lower()


def math_model_name(default_model: str) -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return os.getenv("MATH_MODEL") or default_model


def make_math_client():
    provider = math_llm_provider()
    if provider != "deepseek":
        return make_client()
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    api_key = os.getenv("MATH_API_KEY") or os.getenv("ROUTER_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("MATH_BASE_URL") or os.getenv("ROUTER_BASE_URL") or os.getenv("DEEPSEEK_BASE_URL")
    if not api_key or not base_url:
        raise RuntimeError("MATH_LLM_PROVIDER=deepseek 时，请设置 MATH_API_KEY/MATH_BASE_URL 或 DEEPSEEK_API_KEY/DEEPSEEK_BASE_URL。")
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url=base_url)


def deepseek_thinking_kwargs(thinking: str | None) -> dict[str, Any]:
    value = (thinking or "disabled").strip().lower()
    if value in {"", "0", "false", "no", "off", "disabled", "disable", "none"}:
        return {"extra_body": {"thinking": {"type": "disabled"}}}
    if value in {"max", "heavy"}:
        return {"extra_body": {"thinking": {"type": "enabled"}}, "reasoning_effort": "max"}
    # DeepSeek V4 当前最轻的可用 reasoning_effort 是 high；low/medium 会映射到 high。
    return {"extra_body": {"thinking": {"type": "enabled"}}, "reasoning_effort": "high"}


def chat_text(
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float | None = None,
    *,
    usage_name: str | None = None,
    tool_name: str | None = None,
) -> str:
    settings = load_settings()
    client = make_client()
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.temperature if temperature is None else temperature,
    )
    notify_usage(
        kind="chat",
        name=usage_name or "tool_llm:chat_text",
        model=model,
        response=response,
        started_at=started,
        tool_name=tool_name,
        provider="dashscope",
    )
    return response.choices[0].message.content or ""


def chat_math_text(
    default_model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float | None = None,
    *,
    thinking: str | None = None,
    usage_name: str | None = None,
    tool_name: str | None = None,
) -> str:
    settings = load_settings()
    provider = math_llm_provider()
    if provider != "deepseek":
        return chat_text(
            default_model,
            system_prompt,
            user_prompt,
            temperature,
            usage_name=usage_name,
            tool_name=tool_name,
        )

    client = make_math_client()
    model = math_model_name(default_model)
    thinking_kwargs = deepseek_thinking_kwargs(thinking)
    started = time.perf_counter()
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **thinking_kwargs,
    }
    if (thinking or "disabled").strip().lower() in {"", "0", "false", "no", "off", "disabled", "disable", "none"}:
        payload["temperature"] = settings.temperature if temperature is None else temperature
    response = client.chat.completions.create(**payload)
    notify_usage(
        kind="chat",
        name=usage_name or "tool_llm:chat_math_text",
        model=model,
        response=response,
        started_at=started,
        tool_name=tool_name,
        provider="deepseek",
        thinking=(thinking or "disabled"),
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


def chat_global_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float | None = None,
    *,
    usage_name: str | None = None,
    tool_name: str | None = None,
) -> str:
    settings = load_settings()
    client = make_global_client()
    model_name = global_model_name()
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=global_temperature(settings.temperature if temperature is None else temperature),
    )
    notify_usage(
        kind="chat",
        name=usage_name or "tool_llm:chat_global_text",
        model=model_name,
        response=response,
        started_at=started,
        tool_name=tool_name,
        provider="global",
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
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=settings.vl_model,
        messages=[
            {"role": "system", "content": QWEN_VL_OCR_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0,
    )
    notify_usage(
        kind="chat",
        name="tool_llm:ocr_math_image:qwen_vl",
        model=settings.vl_model,
        response=response,
        started_at=started,
        tool_name="ocr_math_image",
        image_count=len(image_paths),
        provider="dashscope",
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
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=settings.vl_model,
        messages=[
            {"role": "system", "content": IMAGE_ROUTING_OCR_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0,
    )
    notify_usage(
        kind="chat",
        name="runtime_internal:image_routing_ocr:qwen_vl",
        model=settings.vl_model,
        response=response,
        started_at=started,
        tool_name="image_routing_ocr",
        image_count=len(image_paths),
        provider="dashscope",
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


def solve_with_qwenmath(
    problem: MathProblem,
    user_query: str,
    vl_text: str | None,
    output_format: str = "ui",
    feedback: str | None = None,
    thinking: str | None = None,
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
    return chat_math_text(
        settings.math_model,
        QWEN_MATH_SOLVER_PROMPT,
        "\n\n".join(prompt_parts),
        thinking=thinking or "light",
        usage_name="tool_llm:solve_math_exam:qwen_math",
        tool_name="solve_math_exam",
    )


def solve_general_math_with_qwenmath(
    user_query: str,
    vl_text: str | None,
    output_format: str = "ui",
    thinking: str | None = None,
) -> str:
    settings = load_settings()
    prompt_parts = [f"用户题目/问题：{user_query}"]
    if vl_text:
        prompt_parts.append(f"Qwen-VL 图片识别结果：\n{vl_text}")
    prompt_parts.append(TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT)
    prompt_parts.append(
        "请解答这道普通数学题。若本轮是参数修改或追问，请继承历史中未被显式修改的函数、展开点、目标点、阶数和误差要求。"
    )
    return chat_math_text(
        settings.math_model,
        QWEN_GENERAL_MATH_SOLVER_PROMPT,
        "\n\n".join(prompt_parts),
        thinking=thinking or "disabled",
        usage_name="tool_llm:solve_general_math:qwen_math",
        tool_name="solve_general_math",
    )


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
        return parse_json_object(chat_global_text(
            ANSWER_JUDGE_PROMPT,
            prompt,
            temperature=0,
            usage_name="tool_llm:judge_math_answer:global",
            tool_name="judge_math_answer",
        ))
    except Exception as exc:
        return {"match": False, "reason": f"核对 JSON 解析失败：{exc}", "expected": problem.answer_text, "actual": ""}


def judge_solution_quality(problem: MathProblem, solution: str) -> dict[str, Any]:
    prompt = f"题目：\n{problem.question_text}\n\n标准答案：{problem.answer_text or '无'}\n\n模型解答：\n{solution}"
    try:
        return parse_json_object(chat_global_text(
            SOLUTION_QUALITY_PROMPT,
            prompt,
            temperature=0,
            usage_name="tool_llm:judge_solution_quality:global",
            tool_name="judge_solution_quality",
        ))
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
    thinking: str | None = None,
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
        explanation = chat_math_text(
            settings.math_model,
            "你是考研数学真题纠偏讲解节点。",
            prompt,
            temperature=0,
            thinking=thinking or "disabled",
            usage_name="tool_llm:solve_exam_question:fallback_explanation",
            tool_name="solve_exam_question",
        ).strip()
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
    return chat_global_text(
        "你是考研数学真题的局部答疑助手。",
        prompt,
        temperature=0,
        usage_name="tool_llm:clarify_math_symbol:global",
        tool_name="clarify_math_symbol",
    )


def explain_math_step_with_qwenmath(
    problem: MathProblem,
    user_query: str,
    previous_context: str = "",
    output_format: str = "ui",
    thinking: str | None = None,
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
    return chat_math_text(
        settings.math_model,
        "你是 Qwen-Math 局部讲解节点。",
        prompt,
        temperature=0,
        thinking=thinking or "disabled",
        usage_name="tool_llm:explain_math_step:qwen_math",
        tool_name="explain_math_step",
    )


def explain_math_followup_with_qwenmath(
    user_query: str,
    root_context: str,
    followup_context: str,
    followup_type: str = "contextual_followup",
    output_format: str = "ui",
    thinking: str | None = None,
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
    return chat_math_text(
        settings.math_model,
        "你是 Qwen-Math 上下文追问讲解节点。",
        prompt,
        temperature=0,
        thinking=thinking or "disabled",
        usage_name="tool_llm:answer_math_followup:qwen_math",
        tool_name="answer_math_followup",
    )


def rewrite_math_answer_with_qwen(user_query: str, previous_context: str, output_format: str = "ui") -> str:
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = f"用户改写要求：{user_query}\n\n已有回答/上下文：\n{previous_context}\n\n{format_hint}"
    return chat_global_text(
        "你只改写已有数学回答，不重新解题。",
        prompt,
        temperature=0.2,
        usage_name="tool_llm:rewrite_math_answer:global",
        tool_name="rewrite_math_answer",
    )


def summarize_math_solution_with_qwen(user_query: str, previous_context: str, output_format: str = "ui") -> str:
    format_hint = TERMINAL_FORMAT_PROMPT if output_format == "terminal" else UI_FORMAT_PROMPT
    prompt = f"用户总结要求：{user_query}\n\n已有回答/上下文：\n{previous_context}\n\n{format_hint}"
    return chat_global_text(
        "你只总结已有数学解法，不重新解题。",
        prompt,
        temperature=0.2,
        usage_name="tool_llm:summarize_math_solution:global",
        tool_name="summarize_math_solution",
    )


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
    from .agent_runtime import run_standard_message_loop

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
    from .agent_runtime import run_standard_message_loop

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
    from .agent_runtime import main as runtime_main

    runtime_main()


if __name__ == "__main__":
    main()
