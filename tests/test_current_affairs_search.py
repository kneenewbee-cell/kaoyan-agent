import os
import unittest
from unittest.mock import patch

import qa.agent_runtime as agent_runtime
from qa.tools import current_affairs_search as cas
from qa.tools.current_affairs_search import service


class CurrentAffairsSearchTests(unittest.TestCase):
    def test_extract_dates_uses_default_year_for_chinese_month_day(self) -> None:
        dates = cas.extract_dates("会议于6月23日举行，发布时间为2026年6月16日。", "2026")
        self.assertIn("2026-06-23", dates)
        self.assertIn("2026-06-16", dates)

    def test_normalize_plan_adds_authoritative_domain_defaults(self) -> None:
        plan = {
            "source_groups": {"official": ["moa.gov.cn"], "authoritative_media": ["news.cn"]},
            "query_groups": [{"name": "docs", "queries": ["农业 文件 发布"]}],
        }
        cas.normalize_plan(plan, "最近农业文件", {"date": "2026-06-23"})
        domains = plan["source_groups"]["all_authoritative"]
        self.assertIn("moa.gov.cn", domains)
        self.assertIn("gov.cn", domains)
        self.assertIn("people.com.cn", domains)

    def test_build_search_jobs_interleaves_queries_with_domains_and_caps_count(self) -> None:
        plan = {
            "source_groups": {"all_authoritative": ["gov.cn", "moa.gov.cn", "news.cn"]},
            "query_groups": [
                {"name": "docs", "queries": ["农业 文件 发布", "农业 草案 审议"]},
            ],
        }
        with patch.dict(os.environ, {"NEWS_SEARCH_MAX_REQUESTS": "4"}, clear=False):
            jobs = cas.build_search_jobs(plan)

        self.assertEqual(len(jobs), 4)
        self.assertEqual(jobs[0].rendered_query, "site:gov.cn 农业 文件 发布")
        self.assertEqual(jobs[1].rendered_query, "site:moa.gov.cn 农业 草案 审议")
        self.assertEqual(jobs[2].rendered_query, "site:moa.gov.cn 农业 文件 发布")
        self.assertEqual(jobs[3].rendered_query, "site:news.cn 农业 草案 审议")

    def test_tavily_request_preview_uses_news_domain_and_date_params(self) -> None:
        plan = {
            "time": {"time_range": {"from": "2026-04-01", "to": "2026-05-31"}},
            "source_groups": {"all_authoritative": ["gov.cn", "mee.gov.cn"]},
            "query_groups": [
                {
                    "name": "eco_docs",
                    "domains": ["mee.gov.cn"],
                    "priority": 5,
                    "quota": 1,
                    "queries": ["2026年4月 5月 生态文明 文件"],
                }
            ],
        }
        with patch.dict(os.environ, {"NEWS_SEARCH_RESULTS_PER_QUERY": "6"}, clear=False):
            previews = cas.build_api_request_previews(plan, provider="tavily")

        payload = previews[0]["payload"]
        self.assertEqual(payload["topic"], "news")
        self.assertEqual(payload["include_domains"], ["mee.gov.cn"])
        self.assertEqual(payload["start_date"], "2026-04-01")
        self.assertEqual(payload["end_date"], "2026-05-31")
        self.assertEqual(payload["max_results"], 6)
        self.assertEqual(payload["api_key"], "<redacted>")

    def test_preview_current_affairs_search_stops_before_network_search(self) -> None:
        plan = {
            "task": {"original_query": "最近两月的重要会议"},
            "time": {"time_range": {"from": "2026-04-23", "to": "2026-06-23"}},
            "source_groups": {"all_authoritative": ["gov.cn", "news.cn"]},
            "query_groups": [
                {
                    "name": "meetings",
                    "domains": ["gov.cn"],
                    "priority": 5,
                    "quota": 1,
                    "queries": ["2026年5月 6月 国务院 常务会议"],
                }
            ],
        }
        with (
            patch.object(service, "beijing_time_info", return_value={"date": "2026-06-23", "timezone": "Asia/Shanghai"}),
            patch.object(service, "plan_current_affairs_search", return_value=plan),
            patch.object(service, "execute_news_searches") as searcher,
            patch.object(service, "write_search_trace"),
        ):
            preview = service.preview_current_affairs_search("最近两月的重要会议", provider="tavily")

        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["jobs"][0]["payload"]["query"], "2026年5月 6月 国务院 常务会议")
        searcher.assert_not_called()

    def test_service_returns_structured_evidence_with_mocked_backends(self) -> None:
        plan = {
            "task": {"original_query": "最近两月重要会议"},
            "time": {"time_range": {"from": "2026-04-23", "to": "2026-06-23"}},
            "source_groups": {"all_authoritative": ["news.cn"]},
            "query_groups": [{"name": "meetings", "queries": ["中央 重要会议"]}],
        }
        evidence = [{"title": "中共中央政治局召开会议", "source_domain": "news.cn"}]
        with (
            patch.object(service, "beijing_time_info", return_value={"date": "2026-06-23", "timezone": "Asia/Shanghai"}),
            patch.object(service, "plan_current_affairs_search", return_value=plan) as planner,
            patch.object(service, "execute_news_searches", return_value=["raw-hit"]) as searcher,
            patch.object(service, "clean_and_verify_hits", return_value=evidence) as verifier,
            patch.object(service, "fallback_enabled", return_value=False),
            patch.object(service, "write_search_trace"),
        ):
            result = service.call_current_affairs_search("最近两月重要会议")

        self.assertEqual(result["type"], "current_affairs_evidence")
        self.assertEqual(result["query"], "最近两月重要会议")
        self.assertEqual(result["items"][0]["title"], "中共中央政治局召开会议")
        self.assertEqual(result["items"][0]["source_domain"], "news.cn")
        planner.assert_called_once()
        searcher.assert_called_once_with(plan)
        verifier.assert_called_once_with(plan, ["raw-hit"])

    def test_second_layer_query_shape_invokes_current_affairs_tool(self) -> None:
        agent_runtime.legacy_agent._TOOLKIT = None
        expected = {"type": "current_affairs_evidence", "items": []}
        with patch("qa.kaoyan_agent.call_current_affairs_search", return_value=expected) as mocked:
            tools = agent_runtime.build_current_affairs_tools()
            result = tools["get_current_affairs"].func({"query": "最近两月重要会议"})

        self.assertEqual(result, expected)
        mocked.assert_called_once_with("最近两月重要会议")


if __name__ == "__main__":
    unittest.main()
