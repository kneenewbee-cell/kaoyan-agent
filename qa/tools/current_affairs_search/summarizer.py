from __future__ import annotations

from typing import Any

from .llm import chat_current_affairs_text


ANSWER_PROMPT = """你是考研政治近期时政整理助手。

你会收到搜索计划、搜索结果和本地核验信息。请基于 evidence 作答，不要编造 evidence 中没有的会议、文件、日期、来源或官方表述。

要求：
1. 优先使用官方发布和权威媒体；地方媒体、热榜或无法核验信息只能作线索。
2. 合并重复事项，按重要性和时间顺序整理。
3. 如果结果不足，明确说明“当前检索结果不足以确认”。
4. 不要把“可联系的考研政治角度”写成“必考点”。
5. 每个重要事项尽量包含名称、时间、类型、来源、核心事实、关键词、考研政治可联系角度、可信度。

输出格式：
一、核心结论
二、近期重要时政事项
三、关键词
四、考研政治复习角度
五、需要继续关注的方向
"""


def summarize_current_affairs(query: str, current_time: dict[str, str], plan: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
    raw = chat_current_affairs_text(
        ANSWER_PROMPT,
        {
            "current_time": current_time,
            "user_query": query,
            "search_plan": plan,
            "evidence": evidence,
        },
        usage_name="tool_llm:get_current_affairs:summarize",
        temperature=0.2,
    )
    return raw.strip()
