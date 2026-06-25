from __future__ import annotations

from typing import Any

from .constants import OFFICIAL_SOURCE_DOMAINS
from .llm import chat_current_affairs_text, parse_json_object
from .time_utils import beijing_time_info
from .utils import unique_strings


PLANNER_PROMPT = """你是考研政治时政搜索计划生成器，不回答用户问题。

输入包含 current_time 和 query。你的任务是生成一个可执行搜索计划，供程序调用新闻搜索 API。

硬性要求：
1. 只输出 JSON，不要输出解释。
2. 所有相对时间必须以 current_time.date 为基准，直接换算成 YYYY-MM-DD。
3. 如果用户没有明确年份，默认使用 current_time.date 所在年份。
4. 如果用户说“最近/近期”，默认按最近两个月。
5. 如果用户问“本月/今年/近期/最近”等截至当前的问题，time_range.to 不得晚于 current_time.date；只有用户明确问未来安排、即将举行、下个月时，才允许晚于 current_time.date。
6. 如果时间含义不确定，仍给出 best_effort time_range，并在 warnings 中说明。
7. 不要编造具体新闻事实或具体事件名称，只规划怎么搜索。
8. 先判断搜索复杂度 search_scope，并给出 suggested_queries：
   - simple：简单事实核验。用户询问一个明确事项、日期、文件、会议或单点真假；建议 2-4 条 query。
   - normal：普通时政整理。用户给出明确主题或短时间范围，需要覆盖少数机构/来源；建议 5-8 条 query。
   - broad：宽泛时政专题。用户问“最近两个月重要会议/近期重要政策/某领域文件有哪些”等，需要覆盖多个机构、多个文种或多个事件方向；建议 8-12 条 query。
   - complex：年度/季度/大型专题盘点，或同时跨多个主题、多个国家/领域、多个文种；建议 12-20 条 query，并在 warnings 中说明应分批搜索。
9. query 不要做笛卡尔积，不要过量枚举；根据 search_scope 给出足量但受控的 query 关键词组。
10. 关键词扩展按固定维度进行：topic_terms、event_or_document_types、institution_terms、source_domains、query_groups。
11. 每条 query 应包含时间词（年份或明确月份）+ 主题/事项类型 + 机构/来源方向，避免只写“重大活动”“时政要闻”“汇总”等泛词。
12. 每个 query_group 必须给出 domains、priority、quota：
   - domains：该组最适合的官方/权威域名，不要全局乱配。
   - priority：1-5，越高越应优先搜索。
   - quota：建议该组最多消耗多少搜索请求。
13. 按任务类型选择权威域名：
   - 会议：gov.cn、news.cn、people.com.cn、cctv.com、npc.gov.cn、cppcc.gov.cn。
   - 法律草案/文件：gov.cn、npc.gov.cn、moj.gov.cn、对应部委官网、news.cn、people.com.cn。
   - 农业农村：moa.gov.cn、gov.cn、npc.gov.cn、moj.gov.cn、news.cn、people.com.cn。
   - 国际会晤/外交活动：mfa.gov.cn、news.cn、people.com.cn、cctv.com、gov.cn。
14. 国际类问题不要主动列举 G20、APEC、上合、金砖、联合国等具体组织，除非用户明确提到；优先用“外交部、访问、会晤、峰会、论坛、国际活动”等中性词搜索。
15. 文件/草案类问题必须覆盖“草案、征求意见、法律、条例、意见、通知、办法、方案”等文种方向。

输出 JSON schema：
{
  "task": {
    "type": "meeting_search | policy_document_search | law_or_draft_search | international_event_search | speech_article_search | general_current_affairs_search",
    "original_query": "...",
    "topic_terms": ["..."],
    "event_or_document_types": ["..."],
    "institution_terms": ["..."],
    "need_kaoyan_angle": true
  },
  "search_scope": {
    "level": "simple | normal | broad | complex",
    "suggested_queries": 8,
    "reason": "一句话说明为什么这样分档"
  },
  "time": {
    "expression": "...",
    "time_range": {"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"},
    "basis": "一句话说明如何根据 current_time.date 换算"
  },
  "source_groups": {
    "official": ["gov.cn"],
    "authoritative_media": ["news.cn", "people.com.cn", "cctv.com"],
    "clue_only": []
  },
  "query_groups": [
    {
      "name": "official_documents",
      "domains": ["gov.cn"],
      "priority": 5,
      "quota": 4,
      "queries": ["..."]
    }
  ],
  "verify_rules": {
    "must_match_time_range": true,
    "prefer_official_source": true,
    "cross_check_when_possible": true
  },
  "warnings": []
}
"""

PLANNER_PROMPT += """
补充硬性要求：query 字符串只写关键词，不要包含 site:domain，也不要把 gov.cn、news.cn、people.com.cn 等裸域名写进 query。
域名只能放在 query_groups[].domains；工具层会用 domains 生成 include_domains 或等价搜索约束。
"""
PLANNER_PROMPT += """

Job budget rules:
1. search_scope.suggested_queries means the recommended number of first-round search API jobs.
2. Use simple=2-4 jobs, normal=5-8 jobs, broad=8-12 jobs, complex=12-20 jobs.
3. query text must contain keywords only; do not put site:domain or bare domains in query text.
4. Put domains only in query_groups[].domains. The tool will convert domains to include_domains or equivalent search constraints.
"""


def plan_current_affairs_search(query: str, current_time: dict[str, str] | None = None) -> dict[str, Any]:
    current_time = current_time or beijing_time_info()
    raw = chat_current_affairs_text(
        PLANNER_PROMPT,
        {"current_time": current_time, "query": query},
        usage_name="tool_llm:get_current_affairs:planner",
        temperature=0.1,
        json_mode=True,
    )
    plan = parse_json_object(raw)
    normalize_plan(plan, query, current_time)
    return plan


def normalize_plan(plan: dict[str, Any], query: str, current_time: dict[str, str]) -> None:
    plan.setdefault("task", {})
    plan["task"].setdefault("original_query", query)
    plan["task"]["need_kaoyan_angle"] = True
    plan.setdefault("time", {})
    plan["time"].setdefault("time_range", {"from": current_time["date"], "to": current_time["date"]})
    plan.setdefault("source_groups", {})
    plan["source_groups"].setdefault("official", [])
    plan["source_groups"].setdefault("authoritative_media", [])
    plan.setdefault("query_groups", [])
    plan.setdefault("verify_rules", {})
    plan.setdefault("warnings", [])
    domains = unique_strings(
        list(plan["source_groups"].get("official") or [])
        + list(plan["source_groups"].get("authoritative_media") or [])
        + OFFICIAL_SOURCE_DOMAINS
    )
    plan["source_groups"]["all_authoritative"] = domains
    plan.setdefault("search_scope", {})
    plan["search_scope"].setdefault("level", "normal")
    plan["search_scope"].setdefault("suggested_queries", 8)
    for index, group in enumerate(plan.get("query_groups") or []):
        if not isinstance(group, dict):
            continue
        group.setdefault("domains", domains[:4])
        group.setdefault("priority", max(1, 5 - index))
        group.setdefault("quota", 4)
