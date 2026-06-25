import os
import unittest
from unittest.mock import patch

from qa.agent_runtime import build_tool_selection_messages
from qa.tools import current_affairs_search as cas
from qa.tools.current_affairs_search.search_api import SearchHit
from qa.tools.current_affairs_search.verify import (
    clean_and_verify_hits,
    deduplicate_evidence_items,
    domain_rank_score,
    source_confidence_hint,
)


class CurrentAffairsBudgetTests(unittest.TestCase):
    def test_simple_scope_clamps_final_jobs_to_four(self) -> None:
        plan = {
            "search_scope": {"level": "simple", "suggested_queries": 9},
            "time": {"time_range": {"from": "2026-06-18", "to": "2026-06-18"}},
            "source_groups": {"all_authoritative": ["gov.cn", "news.cn", "people.com.cn"]},
            "query_groups": [
                {
                    "name": "fact_check",
                    "domains": ["gov.cn", "news.cn", "people.com.cn"],
                    "priority": 5,
                    "quota": 9,
                    "queries": ["event one", "event two", "event three"],
                }
            ],
        }
        with patch.dict(os.environ, {"NEWS_SEARCH_QUERY_BUDGET": "12"}, clear=False):
            self.assertEqual(cas.resolve_job_budget(plan), 4)
            self.assertEqual(len(cas.build_search_jobs(plan)), 4)

    def test_broad_scope_uses_suggested_jobs_inside_range(self) -> None:
        plan = {
            "search_scope": {"level": "broad", "suggested_queries": 10},
            "time": {"time_range": {"from": "2026-01-01", "to": "2026-06-23"}},
            "source_groups": {"all_authoritative": ["gov.cn", "news.cn", "people.com.cn", "cctv.com"]},
            "query_groups": [
                {
                    "name": "topic",
                    "domains": ["gov.cn", "news.cn", "people.com.cn", "cctv.com"],
                    "priority": 5,
                    "quota": 20,
                    "queries": ["belt road policy", "belt road meeting", "belt road report"],
                }
            ],
        }
        with patch.dict(os.environ, {"NEWS_SEARCH_QUERY_BUDGET": "12"}, clear=False):
            self.assertEqual(cas.resolve_job_budget(plan), 10)
            self.assertEqual(len(cas.build_search_jobs(plan)), 10)

    def test_global_budget_still_caps_scope_budget(self) -> None:
        plan = {
            "search_scope": {"level": "complex", "suggested_queries": 20},
            "time": {"time_range": {"from": "2026-01-01", "to": "2026-06-23"}},
            "source_groups": {"all_authoritative": ["gov.cn", "news.cn", "people.com.cn", "cctv.com"]},
            "query_groups": [
                {
                    "name": "topic",
                    "domains": ["gov.cn", "news.cn", "people.com.cn", "cctv.com"],
                    "priority": 5,
                    "quota": 30,
                    "queries": ["policy", "meeting", "report", "law", "forum"],
                }
            ],
        }
        with patch.dict(os.environ, {"NEWS_SEARCH_QUERY_BUDGET": "12"}, clear=False):
            self.assertEqual(cas.resolve_job_budget(plan), 12)
            self.assertEqual(len(cas.build_search_jobs(plan)), 12)

    def test_verify_filters_generic_low_relevance_homepage(self) -> None:
        plan = {
            "time": {"time_range": {"from": "2026-04-01", "to": "2026-05-31"}},
            "source_groups": {"all_authoritative": ["gov.cn", "nea.gov.cn"]},
            "task": {
                "topic_terms": ["ecology"],
                "event_or_document_types": ["draft"],
                "institution_terms": ["environment"],
            },
        }
        hit = SearchHit(
            title="国家能源局",
            url="https://www.nea.gov.cn/",
            snippet="agency homepage",
            source_domain="nea.gov.cn",
            query="2026 May ecology draft",
            provider="test",
            fetched_text="general navigation 2026-05-08",
        )
        with patch("qa.tools.current_affairs_search.verify.fetch_candidate_pages", return_value=[hit]):
            evidence = clean_and_verify_hits(plan, [hit])

        self.assertEqual(evidence, [])

    def test_local_gov_subdomain_is_not_ranked_like_exact_gov_cn(self) -> None:
        allowed = ["gov.cn", "news.cn"]
        self.assertGreater(domain_rank_score("gov.cn", allowed), domain_rank_score("lzxq.gov.cn", allowed))
        self.assertEqual(source_confidence_hint("lzxq.gov.cn"), "medium")

    def test_deduplicates_same_news_from_different_queries(self) -> None:
        items = [
            {
                "title": "受权发布丨重要会议召开",
                "url": "https://www.news.cn/politics/202606/test.html?utm_source=a",
                "source_domain": "news.cn",
                "query": "2026年6月 重要会议",
                "group": "meetings",
                "relevance_score": 5,
                "confidence_hint": "high",
                "extracted_dates": ["2026-06-18"],
            },
            {
                "title": "受权发布丨重要会议召开",
                "url": "https://news.cn/politics/202606/test.html",
                "source_domain": "news.cn",
                "query": "2026年6月 中央会议",
                "group": "central_meetings",
                "relevance_score": 6,
                "confidence_hint": "high",
                "extracted_dates": ["2026-06-18"],
            },
        ]

        deduped = deduplicate_evidence_items(items)

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["query"], "2026年6月 中央会议")
        self.assertEqual(
            deduped[0]["matched_queries"],
            ["2026年6月 重要会议", "2026年6月 中央会议"],
        )

    def test_politics_second_layer_prompt_includes_dynamic_beijing_date_policy(self) -> None:
        with patch("qa.agent_runtime.beijing_date_iso", return_value="2026-06-25"):
            messages = build_tool_selection_messages(
                "current affairs query",
                [],
                "terminal",
                subject="politics",
                recent_turns=[],
            )

        system_prompt = messages[0]["content"]
        self.assertIn("2026-06-25", system_prompt)
        self.assertIn("当前北京时间日期", system_prompt)
        self.assertIn("避免误补旧年份", system_prompt)
        self.assertNotIn("剥离理论映射诉求", system_prompt)


if __name__ == "__main__":
    unittest.main()
