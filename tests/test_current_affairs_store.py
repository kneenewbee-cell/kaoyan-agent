from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from qa.tools.current_affairs_store import CurrentAffairsStore, ingest_verified_evidence


class CurrentAffairsStoreTests(unittest.TestCase):
    def test_ingest_reuses_same_source_url_and_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = CurrentAffairsStore(Path(tmp))
            evidence = [
                {
                    "title": "人大常委会丨律师法修正草案提请全国人大常委会会议审议",
                    "url": "https://www.news.cn/politics/20260623/9a02bd7d52a143e9a4f0ae0465f6c953/c.html?utm_source=test",
                    "source_domain": "news.cn",
                    "published_at": "2026-06-23",
                    "extracted_dates": ["2026-06-23"],
                    "text_preview": "6月23日，律师法修正草案提请十四届全国人大常委会第二十三次会议审议。",
                    "confidence_hint": "high",
                    "group": "npc_cppcc_meetings",
                }
            ]

            first = ingest_verified_evidence(evidence, store=store)
            second = ingest_verified_evidence(evidence, store=store)

            self.assertEqual(first[0]["event_id"], second[0]["event_id"])
            self.assertEqual(first[0]["source_doc_id"], second[0]["source_doc_id"])
            self.assertEqual(len(store.list_events()), 1)
            self.assertEqual(len(store.list_sources()), 1)
            self.assertTrue(first[0]["event_id"].startswith("cae_20260623_"))
            self.assertTrue(first[0]["source_doc_id"].startswith("cas_20260623_news_cn_"))

    def test_same_event_from_different_sources_keeps_one_event_and_multiple_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = CurrentAffairsStore(Path(tmp))
            base = {
                "title": "律师法修正草案提请十四届全国人大常委会会议审议",
                "published_at": "2026-06-23",
                "extracted_dates": ["2026-06-23"],
                "text_preview": "律师法修正草案提请十四届全国人大常委会第二十三次会议审议。",
                "confidence_hint": "high",
                "group": "law_or_draft",
            }

            first = ingest_verified_evidence([
                {
                    **base,
                    "url": "https://www.news.cn/politics/20260623/lawyer.html",
                    "source_domain": "news.cn",
                }
            ], store=store)
            second = ingest_verified_evidence([
                {
                    **base,
                    "url": "https://www.npc.gov.cn/c2/c30834/202606/t20260623_lawyer.html",
                    "source_domain": "npc.gov.cn",
                }
            ], store=store)

            self.assertEqual(first[0]["event_id"], second[0]["event_id"])
            events = store.list_events()
            sources = store.list_sources()
            self.assertEqual(len(events), 1)
            self.assertEqual(len(sources), 2)
            self.assertEqual(events[0]["primary_source_doc_id"], second[0]["source_doc_id"])
            self.assertEqual(set(events[0]["source_doc_ids"]), {first[0]["source_doc_id"], second[0]["source_doc_id"]})


if __name__ == "__main__":
    unittest.main()
