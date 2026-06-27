from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .strategy_schema import CleaningStrategy, DocumentZones
from .strategy_validator import summarize_strategy_payload
from .document_zones import summarize_document_zones_payload


DEFAULT_QWEN_STRATEGY_MODEL = "qwen3.5-plus-2026-04-20"
QWEN_STRATEGY_MODEL = DEFAULT_QWEN_STRATEGY_MODEL
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
ROOT = Path(__file__).resolve().parents[2]
QWEN_LOG_DIR = ROOT / "data" / "runtime" / "logs"


def _read_dotenv_value(env_path: Path, key: str) -> str:
    if not env_path.exists():
        return ""
    try:
        from dotenv import dotenv_values

        value = dotenv_values(env_path, encoding="utf-8-sig").get(key)
        return str(value or "").strip()
    except Exception:
        pass

    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() != key:
            continue
        return value.strip().strip('"').strip("'")
    return ""


def get_qwen_strategy_model(env_path: Path | str | None = None) -> str:
    target_env_path = Path(env_path) if env_path else ROOT / ".env"
    return (
        _read_dotenv_value(target_env_path, "QWEN_CLEANING_STRATEGY_MODEL")
        or os.getenv("QWEN_CLEANING_STRATEGY_MODEL", "").strip()
        or DEFAULT_QWEN_STRATEGY_MODEL
    )


SYSTEM_PROMPT = """你是 raw_markdown 格式分析器，只输出 JSON。
任务：根据 format_probe.json 判断资料结构规律，并输出 cleaning_strategy.json。

核心限制：
1. 只能输出 JSON，不要输出 Markdown、解释、代码块或 Python 代码。
2. 不要返回需要执行的正则表达式。
3. 不要清洗全文、总结、改写、补充或删除原文内容。
4. 只判断结构策略：可标题结构族、元数据字段、清理规则、保护规则、降级策略。
5. 不确定时使用保守策略；没有可信重复结构时 heading_families 置空。

heading_families 是本任务的核心输出，用它声明“哪些结构族可以成为标题”。main_section_rule 和 subsection_rules 仅保留保守兼容信息。
- heading_family 必须有稳定锚点 anchors、编号样式 ordinal_styles 或章节单位 units；禁止输出只有 title_text/任意短行都能命中的泛规则。
- anchors 是结构族行首稳定信号，如“知识组”“题组”“典型”“考点”“重难点”“出题角度”。
- ordinal_styles 描述编号样式，如 arabic、chinese、circled、paren_arabic、paren_chinese、decimal。
- units 只用于“第 + 编号 + 篇/章/节/部分”这类 strong_boundary。
- kind 可选 strong_boundary、major_section、block、item、outline；不需要固定 H2/H3/H4，本地会用动态栈定层级。
- 纯编号族（如“一、标题”“（一）标题”“1. 标题”“(1) 标题”“①标题”）应使用 kind="outline"、anchors=[]、ordinal_styles 填对应编号样式；不要把“一、/二、/（一）/（二）”枚举成 anchors。
- parent_hints 可以写父结构族 id，如 example 的 parent_hints 可包含 question_group；不确定可留空。
- “答案 / 分析 / 解析 / 点拨 / 点评 / 注 / 解 / 说明 / 提示 / 证明 / 方法”是局部正文标签，禁止作为 anchors。

本地清洗器会根据 heading_families、relation_hints 和动态栈确定 Markdown 层级。

章节层级建议：
1. “第一章 函数与极限”这类章标题，优先让“章”后面的空白成为规则的一部分；如果样本显示章标题确实无空白，也可以使用 optional whitespace。
2. “第一章小结 / 第二章总结 / 本章小结”通常是章内内容，不宜与章标题同级；如果反复出现，建议单独建 summary/subsection 规则。
3. “第一节 基本概念”这类节标题如果属于章内，通常只比章标题深一级；如果资料本身另有层级，以样本为准。
4. “定义 / 核心概念 / 基本概念 / 经典例题 / 易错提醒 / 注意事项 / 应用举例 / 常见题型”通常是固定栏目，不建议给 H5/H6 这类过深层级。
5. 目录点线行通常不是正文标题，例如“第一章 函数与极限 ........ 1”。
6. 完整正文句通常不是标题，即使它以“考点1 / 1.1 / 第一章”开头。
7. PDF/MinerU/OCR 工具生成的既有 Markdown 标题不一定可靠；如果 existing_headings 中出现“## 注... / ## 解... / ## 证明... / ## 分析...”这类明显正文步骤，应在策略中体现更合理的层级，不要因为它已有 ## 就默认同级保留。
8. HTML table 块通常应保护为表格，不要从 `<table>...</table>` 内部抽取标题规则。

示例：
- “模块一 标题”应声明 heading_family: anchors=["模块"], ordinal_styles=["chinese"], ordinal_required=true。
- “考点1 标题”应声明 heading_family: anchors=["考点"], ordinal_styles=["arabic"], ordinal_required=true。
- “典型③ 标题”应声明 heading_family: anchors=["典型"], ordinal_styles=["arabic","circled"], ordinal_required=true。
- “第一章 标题”和“第一节 标题”应声明 strong_boundary family: anchors=["第"], units=["章","节"], ordinal_styles=["chinese","arabic"], ordinal_required=true。

每条编号结构规则必须至少有两个真实 examples 时，min_repeats 才能设为 2；固定栏目可设为 1。"""


SYSTEM_PROMPT += """
If format_probe.json contains layout_summary, treat it as layout evidence from a PDF/MinerU parser.
Use title_samples, table_samples, and page_sequence_samples to infer hierarchy, but do not ask for full
layout.json and do not derive heading rules from inside tables. Tables should be protected as tables.
"""

SYSTEM_PROMPT += """
Alpha outline guidance:
- If body headings use uppercase letter prefixes followed by Chinese titles, such as
  "A基础知识完全解读", "B重点疑难专项突破", "C核心题型题组例解", "D高考高频考题详解",
  express this as a heading_family with anchors=[], ordinal_styles=["alpha"], ordinal_required=true,
  units=[], kind="major_section", and useful parent_hints.
- Do not output an empty heading_family with anchors=[], ordinal_styles=[], units=[].
- Do not enumerate A/B/C/D headings as exact anchors unless the document uses them as literal fixed labels
  without a reusable alphabetic order.
- Do not treat mathematical variable statements such as "A为锐角", "A是...", "若A...", or "已知A..."
  as alpha outline headings.
"""

SYSTEM_PROMPT += """
format_probe.json 里如果包含 heading_outline / heading_pattern_counts / heading_level_counts：
- heading_outline 是全文标题轮廓摘要，不是全文正文；请用它判断全局层级，不要只根据 head_excerpt 局部样本下结论。
- metadata_badge（如“难度：中”“题型：选择题”“4个知识点”）通常不是知识结构标题，不要写成 heading_families。
- circled_outline（如“①平移变换”）通常是最近知识点下面的小点，不要与“第2篇/第2章/知识组/考点”同级。
- compact_chinese_outline（如“一函数”“三函数的表示”）常见于 PDF/OCR 丢了“、”的编号标题，若它反复出现在某个知识组/考点之下，应作为更深子层级，而不是 H2。
- chapter_unit 可能包含“篇/章/部分”，且 PDF/OCR 样本可能没有空格，例如“第2篇函数”“第1章函数”。规则应允许 arabic/chinese 编号和可选空白。
- 对未确定的既有 Markdown 标题，不要因为它已经是 ## 就直接保留同级；请结合 heading_outline 里的上下文决定它是主结构、子结构，还是元信息。
"""

SYSTEM_PROMPT += """
局部解题标签约束：
- “注 / 解 / 分析 / 证明 / 答 / 答案 / 解析 / 点拨 / 点评 / 提示 / 评注 / 说明”如果只是局部步骤标签，不要写入 heading_families 或 subsection_rules。
- “方法 / 方法一 / 方法二 / 方法如下”如果只是解题步骤标签，也不要写入 heading_families 或 subsection_rules。
- 只有“常用方法 / 解题方法 / 方法总结 / 证明方法 / 证明技巧 / 证明专题 / 证明思路总结”等明确结构栏目，才可以作为标题规则。
- 本地清洗器会把局部步骤标签转成正文标签；你只需要描述稳定、可重复的文档结构。
- 资料库清洗中 H1 通常保留给整份资料标题；“第一章/第二章/第一节/一、/（一）”这类重复结构不要设为 H1，通常从 H2 或更深层级开始。
"""
SYSTEM_PROMPT += """
前置区/目录区识别要求：
- 如果 format_probe.json 包含 front_block_index，请用它判断文档前部是否存在封面、前言、使用说明、考情综述、目录、章节导航或章节概览。
- front_block_index 是本地生成的压缩结构索引，包含真实 start_line/end_line；它不是全文，也不是让你清洗正文。
- 如果前部存在目录或章节导航，例如密集出现“第X章/第X篇”、图片、难度、几个知识点、几个题型、几个考点，并且相同章节标题在后文再次出现，请在 document_zones.front_matter_zones 中输出 catalog_or_navigation 范围。
- 如果前部存在前言、封面、使用说明、考情综述等非正文内容，请在 document_zones.front_matter_zones 中输出 preface_or_overview 或 cover_or_metadata 范围。
- 前置区和目录区的 action 必须是 preserve_unprocessed；目录区 chunk_policy 用 single_catalog_chunk；前言/封面/说明区 chunk_policy 用 exclude。
- 请输出 body_start_line，表示正文结构清洗应从哪一行开始；不确定时可以为 null。
- 标题 family 应描述正文区的稳定结构，不要把目录区里的章标题当作正文结构证据。
- 不要删除前置区或目录区，不要输出 cleaned_markdown，只输出 cleaning_strategy.json。
示例 document_zones：
{
  "front_matter_zones": [
    {
      "type": "catalog_or_navigation",
      "start_line": 11,
      "end_line": 36,
      "title": "目录与章节概览",
      "action": "preserve_unprocessed",
      "chunk_policy": "single_catalog_chunk",
      "confidence": 0.86,
      "signals": ["appears_near_document_head", "dense_chapter_headings", "contains_images_or_count_badges", "chapter_heading_reappears_later"]
    }
  ],
  "body_start_line": 37,
  "confidence": 0.86
}
不确定存在前置区/目录区时，front_matter_zones 输出 []，不要硬猜。
"""


SYSTEM_PROMPT += """
Direct relation_hints rules:
- relation_hints may declare only direct parent-child family relations, never transitive/grandparent relations and never Markdown levels.
- Output relation_hints only for strong relations with score >= 85 using the schema score fields:
  interval_structure 0-25, coverage_density 0-25, numbering_anchor 0-20, sample_evidence 0-20, counter_evidence 0 to -50.
- Use body evidence only. If relation evidence comes only from catalog/front matter, do not output it.
- If A contains B and B contains C, output A>B and B>C only; do not output A>C.
- If uncertain, set relation_hints=[] and let local rules handle hierarchy.
- Example: output lesson_unit > exam_point only when body evidence shows repeated "第N课" regions covering multiple "考点N" headings.
"""


def _extract_content(response: Any) -> str:
    choice = response.choices[0]
    message = choice.message
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content or "")


def _trim_text(value: Any, limit: int) -> Any:
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "\n[TRUNCATED_FOR_STRATEGY_PROMPT]"
    return value


def _strategy_system_prompt() -> str:
    marker = "鍓嶇疆鍖?"
    if marker in SYSTEM_PROMPT:
        return SYSTEM_PROMPT.split(marker, 1)[0]
    return SYSTEM_PROMPT


def _compact_probe_for_strategy(format_probe: dict[str, Any]) -> dict[str, Any]:
    compact = dict(format_probe)
    compact.pop("front_block_index", None)
    compact.pop("repeated_heading_candidates", None)
    compact.pop("body_start_candidates", None)
    return compact


def _compact_probe_for_zones(format_probe: dict[str, Any]) -> dict[str, Any]:
    """Keep saved format_probe rich while avoiding duplicate prompt context for Qwen."""
    compact = dict(format_probe)
    compact["head_excerpt"] = _trim_text(compact.get("head_excerpt", ""), 2200)
    compact["tail_excerpt"] = ""
    compact["middle_excerpts"] = []
    compact["existing_headings"] = list(compact.get("existing_headings", []) or [])[:80]
    compact["candidate_marker_lines"] = list(compact.get("candidate_marker_lines", []) or [])[:80]
    compact["short_line_candidates"] = list(compact.get("short_line_candidates", []) or [])[:50]
    compact["front_block_index"] = list(compact.get("front_block_index", []) or [])[:160]
    compact["repeated_heading_candidates"] = list(compact.get("repeated_heading_candidates", []) or [])[:50]
    compact["body_start_candidates"] = list(compact.get("body_start_candidates", []) or [])[:3]
    for key in ("layout_summary",):
        if isinstance(compact.get(key), dict):
            compact[key] = {"summary": compact[key]}
    return compact


def _compact_probe_for_bundle(format_probe: dict[str, Any]) -> dict[str, Any]:
    compact = dict(format_probe)
    compact["head_excerpt"] = _trim_text(compact.get("head_excerpt", ""), 2200)
    compact["tail_excerpt"] = _trim_text(compact.get("tail_excerpt", ""), 1800)
    compact["middle_excerpts"] = [
        _trim_text(excerpt, 1200)
        for excerpt in list(compact.get("middle_excerpts", []) or [])[:2]
    ]
    compact["existing_headings"] = list(compact.get("existing_headings", []) or [])[:140]
    compact["candidate_marker_lines"] = list(compact.get("candidate_marker_lines", []) or [])[:140]
    compact["short_line_candidates"] = list(compact.get("short_line_candidates", []) or [])[:80]
    compact["heading_outline"] = list(compact.get("heading_outline", []) or [])[:220]
    compact["front_block_index"] = list(compact.get("front_block_index", []) or [])[:160]
    compact["repeated_heading_candidates"] = list(compact.get("repeated_heading_candidates", []) or [])[:50]
    compact["body_start_candidates"] = list(compact.get("body_start_candidates", []) or [])[:3]
    return compact


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


def write_qwen_strategy_log(metrics: dict[str, Any], *, event: str = "material_cleaning_strategy") -> Path:
    QWEN_LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = QWEN_LOG_DIR / f"material_cleaning_qwen_{datetime.now().date().isoformat()}.jsonl"
    record = {
        "time": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **metrics,
    }
    with target.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return target


def write_qwen_zone_log(metrics: dict[str, Any]) -> Path:
    return write_qwen_strategy_log(metrics, event="material_document_zones")


BUNDLE_SYSTEM_PROMPT = """You are a raw_markdown structure analyst. Output JSON only.

Task:
Return one JSON object with exactly two top-level objects:
{
  "cleaning_strategy": {...},
  "document_zones": {...}
}

Hard boundaries:
- cleaning_strategy must match the CleaningStrategy schema and must NOT contain document_zones.
- document_zones must match the DocumentZones schema and must NOT contain heading_families,
  cleanup_rules, metadata_rules, or any other cleaning_strategy fields.
- Never output cleaned_markdown. Never output code, regex to execute, explanations, or text outside JSON.
- Do not summarize, rewrite, translate, add, or delete source content.

Independence rule to reduce contamination:
- First decide document_zones from front_block_index, repeated_heading_candidates, and body_start_candidates.
- Then infer cleaning_strategy for the BODY structure only. If body_start_line is known, ignore front matter and catalog
  lines as evidence for heading_families. Catalog chapter titles are navigation evidence, not body hierarchy evidence.
- Do not let catalog/preface detection change body heading families unless the same pattern is repeated in body evidence.
- Treat the two subtasks as independent: document_zones may use front/catalog evidence; cleaning_strategy must use
  body evidence from heading_outline, middle/tail excerpts, and body-side marker candidates. Do not make a body family
  stronger just because it appears in the catalog.
- If a body structural family appears in heading_outline (for example 题型, 知识组, 题组, 典型, 考点, 重难点,
  出题角度, 第一章/第一节 units), preserve that family even when lower-level labels such as 方法 also appear.
- A lower-level label family such as 方法1/方法2 must never replace or suppress a higher-level family such as 题型
  or 知识组. If 方法 is truly structural, make it a child via parent_hints; otherwise leave it to local label handling.

cleaning_strategy guidance:
- heading_families declares positive families that may enter the heading tree for this specific document.
- Prefer stable anchors such as 知识组, 题组, 典型, 考点, 重难点, 出题角度, 第一章/第一节 units, and repeated outline markers.
- Pure outline families should use anchors=[] and ordinal_styles such as chinese, paren_chinese, arabic, paren_arabic, circled, alpha.
- For uppercase letter + Chinese title families such as "A基础知识完全解读", "B重点疑难专项突破",
  "C核心题型题组例解", "D高考高频考题详解", use anchors=[], ordinal_styles=["alpha"],
  ordinal_required=true, units=[], kind="major_section". Do not output anchors=[], ordinal_styles=[], units=[].
  Do not enumerate A/B/C/D headings as exact anchors unless they are literal fixed labels rather than a reusable alphabetic order.
  Do not treat mathematical variable statements such as "A为锐角", "A是...", "若A...", or "已知A..." as alpha headings.
- For "第一章/第一节/第3章" style units, use anchors=["第"], units=["章","节",...], ordinal_styles=["chinese","arabic"].
  Do not output anchors like "第章" or "第节".
- For "题型二 函数性态", use anchors=["题型"], ordinal_styles=["chinese"], ordinal_required=true, units=[].
  Do not use units=["型"], because 型 is already part of the anchor.
- For "知识组2排列与组合", use anchors=["知识组"], ordinal_styles=["arabic"], ordinal_required=true, units=[].
- Do not create broad title_text-only rules.
- Local solution labels such as 注/解/分析/证明/答案/解析/点拨/提示/说明 usually should not be families.
- If a label like 方法1/方法2 is truly a repeated body structure in this document, it may be a family; otherwise leave it to local label handling.
- relation_hints may declare only direct parent-child family relations, never transitive/grandparent relations and never Markdown levels.
- Output relation_hints only for strong relations with score >= 85 using the schema score fields:
  interval_structure 0-25, coverage_density 0-25, numbering_anchor 0-20, sample_evidence 0-20, counter_evidence 0 to -50.
- Use body evidence only. If relation evidence comes only from catalog/front matter, do not output it.
- If A contains B and B contains C, output A>B and B>C only; do not output A>C.
- If uncertain, set relation_hints=[] and let local rules handle hierarchy.
- Keep the original CleaningStrategy field format exactly; no document_zones inside it.

document_zones guidance:
- Use real line numbers from front_block_index/body_start_candidates.
- catalog_or_navigation: dense table of contents/navigation near the front, often with repeated chapter headings, images,
  difficulty/count badges, page references, or headings that reappear later in body.
- A front HTML table alone is not enough to mark catalog_or_navigation. Tables like 考试内容/考试要求/考试范围 are
  study content or overview evidence, not a catalog, unless they also contain chapter navigation/page references or
  repeated body headings.
- preface_or_overview: preface, usage notes, exam overview, or non-body overview.
- cover_or_metadata: title page, copyright, ISBN, author/publisher metadata.
- action must be preserve_unprocessed.
- catalog_or_navigation chunk_policy must be single_catalog_chunk.
- cover_or_metadata/preface_or_overview/front_matter chunk_policy must be exclude.
- If uncertain, output empty front_matter_zones and confidence <= 0.5.
"""


def generate_strategy_bundle_with_qwen(
    format_probe: dict,
    *,
    model: str | None = None,
    api_key: str | None = None,
    timeout_seconds: int = 120,
    usage_metrics: dict[str, Any] | None = None,
) -> dict:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass
    model = model or get_qwen_strategy_model()
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
        qwen_probe = _compact_probe_for_bundle(format_probe)
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": BUNDLE_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Return the strategy bundle JSON. The two schemas are below.\n\n"
                        "CleaningStrategy JSON Schema:\n"
                        + json.dumps(CleaningStrategy.model_json_schema(), ensure_ascii=False)
                        + "\n\nDocumentZones JSON Schema:\n"
                        + json.dumps(DocumentZones.model_json_schema(), ensure_ascii=False)
                        + "\n\nformat_probe.json:\n"
                        + json.dumps(qwen_probe, ensure_ascii=False)
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
                "probe_prompt_compacted": True,
                "call_mode": "bundle",
            }
        )
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen strategy bundle response is not a JSON object")
        cleaning_strategy = parsed.get("cleaning_strategy")
        document_zones = parsed.get("document_zones")
        if not isinstance(cleaning_strategy, dict) or not isinstance(document_zones, dict):
            raise ValueError("Qwen strategy bundle must include cleaning_strategy and document_zones objects")
        cleaning_strategy["strategy_source"] = "qwen"
        parsed["cleaning_strategy"] = cleaning_strategy
        if usage_metrics is not None:
            metrics["response_summary"] = {
                "cleaning_strategy": summarize_strategy_payload(cleaning_strategy),
                "document_zones": summarize_document_zones_payload(document_zones),
            }
            usage_metrics.update(metrics)
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
                    "call_mode": "bundle",
                }
            )
        raise


def generate_strategy_with_qwen(
    format_probe: dict,
    *,
    model: str | None = None,
    api_key: str | None = None,
    timeout_seconds: int = 120,
    usage_metrics: dict[str, Any] | None = None,
) -> dict:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass
    model = model or get_qwen_strategy_model()
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
        qwen_probe = _compact_probe_for_strategy(format_probe)
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": _strategy_system_prompt()},
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
                        + json.dumps(qwen_probe, ensure_ascii=False)
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
                "probe_prompt_compacted": qwen_probe is not format_probe,
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen strategy response is not a JSON object")
        parsed["strategy_source"] = "qwen"
        if usage_metrics is not None:
            usage_metrics["response_summary"] = summarize_strategy_payload(parsed)
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


ZONE_SYSTEM_PROMPT = """You are a document-zone detector for parsed raw_markdown. Output JSON only.

Task:
- Read format_probe.json samples only; never ask for or output cleaned_markdown.
- Detect non-body zones near the beginning of a parsed document: cover/metadata, preface/overview,
  catalog/navigation, and the first likely body line.
- Do not describe body heading rules. Do not output heading_families, cleanup_rules,
  or any cleaning_strategy fields.

Rules:
- Use start_line/end_line from front_block_index or body_start_candidates.
- catalog_or_navigation means a compact table of contents or chapter navigation block, often with
  dense chapter titles, images, difficulty/count badges, page references, or headings repeated later.
- preface_or_overview means front matter such as preface, usage notes, exam overview, or summary text
  that is not the main body.
- cover_or_metadata means title page, copyright, ISBN, author/publisher metadata, or pure book info.
- action must be preserve_unprocessed.
- catalog_or_navigation must use chunk_policy single_catalog_chunk.
- cover_or_metadata, preface_or_overview, and front_matter must use chunk_policy exclude.
- If uncertain, output an empty front_matter_zones list and confidence <= 0.5.

Output shape:
{
  "front_matter_zones": [],
  "body_start_line": null,
  "confidence": 0.0
}
"""


def generate_document_zones_with_qwen(
    format_probe: dict,
    *,
    model: str | None = None,
    api_key: str | None = None,
    timeout_seconds: int = 120,
    usage_metrics: dict[str, Any] | None = None,
) -> dict:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env", encoding="utf-8-sig", override=False)
    except Exception:
        pass
    model = model or get_qwen_strategy_model()
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
        qwen_probe = _compact_probe_for_zones(format_probe)
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            extra_body={"enable_thinking": False},
            messages=[
                {"role": "system", "content": ZONE_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Return document_zones JSON matching this schema. "
                        "Do not output cleaning_strategy and do not output cleaned_markdown.\n\n"
                        "JSON Schema:\n"
                        + json.dumps(DocumentZones.model_json_schema(), ensure_ascii=False)
                        + "\n\nformat_probe.json:\n"
                        + json.dumps(qwen_probe, ensure_ascii=False)
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
                "probe_prompt_compacted": True,
            }
        )
        if usage_metrics is not None:
            usage_metrics.update(metrics)
        content = _extract_content(response).strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Qwen document zones response is not a JSON object")
        if usage_metrics is not None:
            usage_metrics["response_summary"] = summarize_document_zones_payload(
                parsed.get("document_zones") if isinstance(parsed.get("document_zones"), dict) else parsed
            )
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
