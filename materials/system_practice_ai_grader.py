from __future__ import annotations

import json
from typing import Any


AI_GRADE_STATUSES = {"correct", "incorrect", "partial", "pending_review", "unanswered"}


def grade_practice_item_with_ai(context: dict[str, Any]) -> dict[str, Any]:
    """Grade one submitted practice item with a lightweight LLM prompt.

    The store owns persistence; this helper only returns a normalized grading
    decision. If the model is unavailable, keep the item reviewable instead of
    pretending to know the answer.
    """

    user_answer = str(context.get("user_answer") or "").strip()
    answer_type = str(context.get("answer_type") or "").strip()
    if not user_answer:
        return {
            "final_status": "unanswered",
            "judge_confidence": 1.0,
            "judge_reason": "用户未作答，AI 判分跳过。",
            "ai_feedback": "",
        }

    try:
        from qa.kaoyan_agent import chat_global_text, parse_json_object

        prompt = _build_ai_grade_prompt(context)
        parsed = parse_json_object(
            chat_global_text(
                "你是考研练习判分助手，只输出 JSON。",
                prompt,
                temperature=0,
                usage_name="tool_llm:practice_item_grade",
                tool_name="practice_item_grade",
            )
        )
        return _normalize_ai_grade_payload(parsed, answer_type=answer_type)
    except Exception as exc:
        return {
            "final_status": "pending_review",
            "judge_confidence": 0.0,
            "judge_reason": f"AI 判分暂不可用：{exc.__class__.__name__}",
            "ai_feedback": "请先按参考答案人工核对，稍后可重试 AI 判分。",
        }


def _build_ai_grade_prompt(context: dict[str, Any]) -> str:
    question = context.get("question") if isinstance(context.get("question"), dict) else {}
    topic_text = " / ".join(str(item) for item in question.get("topics") or [] if str(item).strip())
    payload = {
        "question_title": context.get("question_title") or question.get("question_id") or "",
        "question_type": context.get("answer_type") or question.get("question_type") or "",
        "topics": topic_text,
        "question_markdown": question.get("question_markdown") or question.get("preview") or "",
        "standard_answer": context.get("standard_answer") or "",
        "standard_explanation": question.get("explanation_markdown") or question.get("explanation") or "",
        "user_answer": context.get("user_answer") or "",
        "local_status": context.get("local_status") or "",
    }
    return (
        "请根据当前考研题、参考答案和用户答案判分。\n"
        "判分边界：\n"
        "- 填空题：用户表达与参考答案数学等价即可判 correct；明显不等价判 incorrect；不确定判 pending_review。\n"
        "- 解答题：可按核心结论和关键步骤判 correct / partial / incorrect；信息不足判 pending_review。\n"
        "- 不要因为书写形式不同就判错，但也不要放过本质错误。\n"
        "只输出 JSON，不要输出解释性正文。JSON 格式：\n"
        "{\"final_status\":\"correct|incorrect|partial|pending_review\",\"judge_confidence\":0.0-1.0,"
        "\"judge_reason\":\"一句话理由\",\"ai_feedback\":\"给用户看的简短反馈\"}\n\n"
        f"判分输入：\n{json.dumps(payload, ensure_ascii=False)}"
    )


def _normalize_ai_grade_payload(payload: Any, *, answer_type: str) -> dict[str, Any]:
    data = payload if isinstance(payload, dict) else {}
    raw_status = str(data.get("final_status") or data.get("status") or "").strip()
    if not raw_status and "match" in data:
        raw_status = "correct" if bool(data.get("match")) else "incorrect"
    if raw_status == "needs_review":
        raw_status = "pending_review"
    if answer_type == "blank" and raw_status == "partial":
        raw_status = "pending_review"
    if raw_status not in AI_GRADE_STATUSES:
        raw_status = "pending_review"
    try:
        confidence = float(data.get("judge_confidence", data.get("confidence", 0.0)))
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = min(max(confidence, 0.0), 1.0)
    return {
        "final_status": raw_status,
        "judge_confidence": confidence,
        "judge_reason": str(data.get("judge_reason") or data.get("reason") or "").strip(),
        "ai_feedback": str(data.get("ai_feedback") or data.get("feedback") or "").strip(),
    }
