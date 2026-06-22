from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .strategy_schema import CleaningStrategy


QWEN_STRATEGY_MODEL = os.getenv("QWEN_CLEANING_STRATEGY_MODEL", "qwen3.6-plus-2026-04-02")
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
ROOT = Path(__file__).resolve().parents[2]
QWEN_LOG_DIR = ROOT / "data" / "runtime" / "logs"


SYSTEM_PROMPT = """你是 raw_markdown 格式分析器，只输出 JSON。
任务：根据 format_probe.json 判断资料结构规律，并输出 cleaning_strategy.json。

核心限制：
1. 只能输出 JSON，不要输出 Markdown、解释、代码块或 Python 代码。
2. 不要返回需要执行的正则表达式。
3. 不要清洗全文、总结、改写、补充或删除原文内容。
4. 只判断结构策略：主标题规则、子标题规则、元数据字段、清理规则、保护规则、降级策略。
5. 不确定时使用保守策略；没有可信重复结构时 heading_rules 置空。

heading_rules 是安全的声明式规则，优先使用 heading_rules 表达标题规律；main_section_rule 和 subsection_rules 仅用于兼容旧策略。
- target_level 由文档层级决定，不存在固定的“章=H2、节=H3”。
- role=main 表示编号/章节结构；role=subsection 表示定义、核心概念、例题、提醒、小结等栏目。
- 如果能判断父子关系，优先填写 parent_rule，例如 section 的 parent_rule 可以是 chapter；不确定时可以留空。
- pattern 由 token 顺序组成：literal、ordinal、separator、whitespace、title_text。
- literal/样例：values=["第"]、values=["模块"]、values=["章"]。
- ordinal 的 styles 可选 chinese、arabic、decimal。
- separator 的 values 是普通文本，例如 ["、"] 或 [".", "、"]。
- whitespace optional=true 表示可有可无，否则至少一个空白。
- title_text 必须是最后一个 token。
- values 只能写普通字面量，禁止写正则表达式。

章节层级建议：
1. “第一章 函数与极限”这类章标题，优先让“章”后面的空白成为规则的一部分；如果样本显示章标题确实无空白，也可以使用 optional whitespace。
2. “第一章小结 / 第二章总结 / 本章小结”通常是章内内容，不宜与章标题同级；如果反复出现，建议单独建 summary/subsection 规则。
3. “第一节 基本概念”这类节标题如果属于章内，通常只比章标题深一级；如果资料本身另有层级，以样本为准。
4. “定义 / 核心概念 / 基本概念 / 经典例题 / 易错提醒 / 注意事项 / 应用举例 / 常见题型”通常是固定栏目，不建议给 H5/H6 这类过深层级。
5. 目录点线行通常不是正文标题，例如“第一章 函数与极限 ........ 1”。
6. 完整正文句通常不是标题，即使它以“考点1 / 1.1 / 第一章”开头。

示例：
- “模块一 标题”应用 literal(模块)+ordinal(chinese)+whitespace(optional)+title_text。
- “考点1 标题”应用 literal(考点)+ordinal(arabic)+whitespace(optional)+title_text。
- “第一章 标题”和“第一节 标题”应分别生成规则，并按文档实际结构选择不同层级和 parent_rule。

每条编号结构规则必须至少有两个真实 examples 时，min_repeats 才能设为 2；固定栏目可设为 1。"""


def _extract_content(response: Any) -> str:
    choice = response.choices[0]
    message = choice.message
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content or "")


def _usage_metrics(response: Any, *, model: str, started_at: float) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0)
    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens
    latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
    elapsed_seconds = latency_ms / 1000 if latency_ms else 0.0
    return {
        "model": model,
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "tokens_per_second": round(total_tokens / elapsed_seconds, 2) if elapsed_seconds and total_tokens else 0.0,
        "completion_tokens_per_second": (
            round(completion_tokens / elapsed_seconds, 2)
            if elapsed_seconds and completion_tokens
            else 0.0
        ),
    }


def write_qwen_strategy_log(metrics: dict[str, Any]) -> Path:
    QWEN_LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = QWEN_LOG_DIR / f"material_cleaning_qwen_{datetime.now().date().isoformat()}.jsonl"
    record = {
        "time": datetime.now(timezone.utc).isoformat(),
        "event": "material_cleaning_strategy",
        **metrics,
    }
    with target.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return target


def generate_strategy_with_qwen(
    format_probe: dict,
    *,
    model: str = QWEN_STRATEGY_MODEL,
    api_key: str | None = None,
    timeout_seconds: int = 60,
    usage_metrics: dict[str, Any] | None = None,
) -> dict:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass
    key = api_key or os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not key:
        raise RuntimeError("Qwen API key is not configured")

    from openai import OpenAI

    client = OpenAI(
        api_key=key,
        base_url=os.getenv("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        timeout=timeout_seconds,
        max_retries=0,
    )
    started_at = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "下面是 raw_markdown 的格式探测样本 format_probe.json。"
                        "请输出严格符合 schema 的 cleaning_strategy.json。"
                        "不要输出 JSON 之外的任何内容。"
                        "所有必填字段都必须提供，禁止新增 schema 外字段。\n\n"
                        "JSON Schema:\n"
                        + json.dumps(CleaningStrategy.model_json_schema(), ensure_ascii=False)
                        + "\n\nformat_probe.json:\n"
                        + json.dumps(format_probe, ensure_ascii=False)
                    ),
                },
            ],
        )
        metrics = _usage_metrics(response, model=model, started_at=started_at)
        metrics.update(
            {
                "api_success": True,
                "source_name": format_probe.get("filename"),
                "probe_char_count": format_probe.get("char_count", 0),
                "probe_line_count": format_probe.get("line_count", 0),
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen strategy response is not a JSON object")
        parsed["strategy_source"] = "qwen"
        return parsed
    except Exception as exc:
        if usage_metrics is not None:
            usage_metrics.update(
                {
                    "model": model,
                    "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "api_success": False,
                    "error_type": exc.__class__.__name__,
                    "source_name": format_probe.get("filename"),
                    "probe_char_count": format_probe.get("char_count", 0),
                    "probe_line_count": format_probe.get("line_count", 0),
                }
            )
        raise
