from __future__ import annotations

import unittest

from materials.indexing.material_indexer import build_search_index, search_in_index, tokenize_query
from materials.indexing.query_processor import process_query
from materials.schemas import Chunk


class MaterialKeywordIndexerTest(unittest.TestCase):
    def test_process_query_loads_stopwords_and_weights_domain_terms(self) -> None:
        plan = process_query("\u7f57\u5c14\u5b9a\u7406\u600e\u4e48\u8bc1\u660e")

        self.assertIn("\u7f57\u5c14\u5b9a\u7406", plan.term_weights)
        self.assertGreater(plan.term_weights["\u7f57\u5c14\u5b9a\u7406"], plan.term_weights["\u5b9a\u7406"])
        self.assertNotIn("\u600e\u4e48", plan.term_weights)
        self.assertNotIn("\u600e\u4e48\u8bc1", plan.term_weights)

    def test_process_query_keeps_ngram_fallback_when_domain_term_is_missing(self) -> None:
        plan = process_query("\u5939\u903c\u51c6\u5219\u5982\u4f55\u4f7f\u7528")

        self.assertNotIn("\u5982\u4f55", plan.term_weights)
        self.assertIn("\u5939\u903c", plan.term_weights)
        self.assertIn("\u5939\u903c\u51c6", plan.term_weights)
        self.assertIn("\u5939\u903c\u51c6\u5219", plan.term_weights)

    def test_process_query_uses_single_characters_only_as_last_resort(self) -> None:
        plan = process_query("\u89d2\u6709\u54ea\u4e9b\u5206\u7c7b")

        self.assertIn("\u5206\u7c7b", plan.term_weights)
        self.assertNotIn("\u89d2", plan.term_weights)
        self.assertNotIn("\u5206", plan.term_weights)
        self.assertNotIn("\u7c7b", plan.term_weights)

    def test_numbered_heading_query_matches_exact_label_before_digit_noise(self) -> None:
        chunks = [
            Chunk(
                chunk_id="kp4",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text=(
                    "\u8003\u70b94\u4e09\u89d2\u51fd\u6570\u7684\u6700\u503c\u53ca\u503c\u57df\n"
                    "\u4e09\u89d2\u51fd\u6570\u7684\u6700\u503c\u53ca\u503c\u57df\u95ee\u9898\u9700\u5229\u7528\u6709\u754c\u6027\u4e0e\u5355\u8c03\u6027\u3002"
                ),
                section_title="\u8003\u70b94\u4e09\u89d2\u51fd\u6570\u7684\u6700\u503c\u53ca\u503c\u57df",
            ),
            Chunk(
                chunk_id="kp6",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text=(
                    "\u8003\u70b96\u4e09\u89d2\u51fd\u6570\u7684\u5468\u671f\u6027\n"
                    "4 4 4 4 4 4 4 4 4 4"
                ),
                section_title="\u8003\u70b96\u4e09\u89d2\u51fd\u6570\u7684\u5468\u671f\u6027",
            ),
        ]

        index_data = build_search_index(chunks)
        terms = tokenize_query("\u8003\u70b94")
        results = search_in_index("\u8003\u70b94", index_data, chunks, top_k=2)

        self.assertIn("\u8003\u70b94", terms)
        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "kp4")

    def test_legal_relation_query_prefers_morality_and_law_relation(self) -> None:
        chunks = [
            Chunk(
                chunk_id="morality_law",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text=(
                    "\u8003\u70b94\uff1a\u601d\u60f3\u9053\u5fb7\u548c\u6cd5\u5f8b\u7684\u5173\u7cfb\n"
                    "\u601d\u60f3\u9053\u5fb7\u548c\u6cd5\u5f8b\u90fd\u662f\u8c03\u8282\u4eba\u4eec\u601d\u60f3\u884c\u4e3a\u7684\u91cd\u8981\u624b\u6bb5\u3002"
                    "\u601d\u60f3\u9053\u5fb7\u5efa\u8bbe\u4e3a\u6cd5\u6cbb\u5efa\u8bbe\u63d0\u4f9b\u601d\u60f3\u6307\u5f15\uff0c"
                    "\u6cd5\u6cbb\u5efa\u8bbe\u4e3a\u601d\u60f3\u9053\u5fb7\u63d0\u4f9b\u5236\u5ea6\u652f\u6491\u3002"
                ),
                section_title="\u8003\u70b94\uff1a\u601d\u60f3\u9053\u5fb7\u548c\u6cd5\u5f8b\u7684\u5173\u7cfb",
            ),
            Chunk(
                chunk_id="revolutionary_morality",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text=(
                    "\u8003\u70b943\uff1a\u53d1\u626c\u4e2d\u56fd\u9769\u547d\u7cbe\u795e\n"
                    "\u4e2d\u56fd\u9769\u547d\u9053\u5fb7\u4e0e\u4f20\u7edf\u7f8e\u5fb7\u7684\u5173\u7cfb\uff1a"
                    "\u4e2d\u56fd\u9769\u547d\u9053\u5fb7\u7ee7\u627f\u4e86\u4e2d\u56fd\u4f20\u7edf\u9053\u5fb7\u7684\u7cbe\u534e\u3002"
                ),
                section_title="\u8003\u70b943\uff1a\u53d1\u626c\u4e2d\u56fd\u9769\u547d\u7cbe\u795e",
            ),
            Chunk(
                chunk_id="rule_of_law",
                material_id="mat_1",
                user_id="tester",
                chunk_index=2,
                text="\u8003\u70b956\uff1a\u575a\u6301\u8d70\u4e2d\u56fd\u7279\u8272\u793e\u4f1a\u4e3b\u4e49\u6cd5\u6cbb\u9053\u8def\n\u6cd5\u6cbb\u6cd5\u6cbb\u6cd5\u6cbb\u6cd5\u6cbb\u6cd5\u6cbb\u3002",
                section_title="\u8003\u70b956\uff1a\u575a\u6301\u8d70\u4e2d\u56fd\u7279\u8272\u793e\u4f1a\u4e3b\u4e49\u6cd5\u6cbb\u9053\u8def",
            ),
        ]

        index_data = build_search_index(chunks)
        terms = tokenize_query("\u9053\u5fb7\u4e0e\u6cd5\u5236\u7684\u5173\u7cfb")
        results = search_in_index("\u9053\u5fb7\u4e0e\u6cd5\u5236\u7684\u5173\u7cfb", index_data, chunks, top_k=3)

        self.assertIn("\u6cd5\u5f8b", terms)
        self.assertIn("\u6cd5\u6cbb", terms)
        self.assertNotIn("\u9053\u5fb7\u4e0e", terms)
        self.assertNotIn("\u7684\u5173\u7cfb", terms)
        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "morality_law")

    def test_query_tokenizer_uses_2_3_4_grams_and_filters_function_words(self) -> None:
        terms = tokenize_query("\u4e09\u89d2\u51fd\u6570\u5982\u4f55\u5316\u7b80")

        self.assertIn("\u4e09\u89d2", terms)
        self.assertIn("\u4e09\u89d2\u51fd", terms)
        self.assertIn("\u4e09\u89d2\u51fd\u6570", terms)
        self.assertIn("\u5316\u7b80", terms)
        self.assertNotIn("\u5982\u4f55", terms)
        self.assertNotIn("\u5982\u4f55\u5316", terms)
        self.assertNotIn("\u5982\u4f55\u5316\u7b80", terms)

    def test_query_tokenizer_filters_question_phrases_without_losing_core_terms(self) -> None:
        terms = tokenize_query("\u89d2\u6709\u54ea\u4e9b\u5206\u7c7b")

        self.assertIn("\u5206\u7c7b", terms)
        self.assertNotIn("\u89d2", terms)
        self.assertNotIn("\u54ea\u4e9b", terms)
        self.assertNotIn("\u6709\u54ea\u4e9b", terms)

    def test_query_tokenizer_filters_generic_action_phrases(self) -> None:
        terms = tokenize_query("\u6b27\u62c9\u578b\u5fae\u5206\u65b9\u7a0b\u4e00\u822c\u600e\u4e48\u5904\u7406")

        self.assertIn("\u5fae\u5206\u65b9\u7a0b", terms)
        self.assertNotIn("\u4e00\u822c", terms)
        self.assertNotIn("\u5904\u7406", terms)
        self.assertNotIn("\u4e00\u822c\u600e", terms)
        self.assertNotIn("\u5904\u7406", terms)

    def test_chinese_query_matches_related_heading_terms(self) -> None:
        chunks = [
            Chunk(
                chunk_id="classification",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text="\u89d2\u7684\u5206\u7c7b\u2014\u6b63\u89d2\u3001\u8d1f\u89d2\u3001\u96f6\u89d2\n\u6b63\u89d2\u6309\u9006\u65f6\u9488\u65cb\u8f6c\u5f62\u6210\uff0c\u8d1f\u89d2\u6309\u987a\u65f6\u9488\u65cb\u8f6c\u5f62\u6210\u3002",
                section_title="\u89d2\u7684\u5206\u7c7b",
            ),
            Chunk(
                chunk_id="axis",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text="\u8f74\u7ebf\u89d2\u7684\u5b9a\u4e49\n\u7ec8\u8fb9\u843d\u5728\u5750\u6807\u8f74\u4e0a\u7684\u89d2\u53eb\u8f74\u7ebf\u89d2\u3002",
                section_title="\u8f74\u7ebf\u89d2\u7684\u5b9a\u4e49",
            ),
        ]

        index_data = build_search_index(chunks)
        results = search_in_index("\u89d2\u6709\u54ea\u4e9b\u5206\u7c7b", index_data, chunks, top_k=2)

        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "classification")

    def test_chinese_question_query_prefers_multi_character_terms_over_repeated_single_characters(self) -> None:
        chunks = [
            Chunk(
                chunk_id="classification",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text="\u89d2\u7684\u5206\u7c7b\u2014\u6b63\u89d2\u3001\u8d1f\u89d2\u3001\u96f6\u89d2",
                section_title="\u89d2\u7684\u5206\u7c7b",
            ),
            Chunk(
                chunk_id="distractor",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text=(
                    "\u4efb\u610f\u89d2\u7684\u7ec8\u8fb9\u6240\u5728\u8c61\u9650\u7684\u5224\u5b9a\u3002"
                    "\u8fd9\u91cc\u6709\u5f88\u591a\u89d2\u7684\u9898\u578b\uff0c"
                    "\u89d2\u89d2\u89d2\u89d2\u89d2\u89d2\u89d2\u89d2\u89d2\u89d2\u3002"
                ),
                section_title="\u4efb\u610f\u89d2\u7684\u7ec8\u8fb9\u6240\u5728\u8c61\u9650\u7684\u5224\u5b9a",
            ),
        ]

        index_data = build_search_index(chunks)
        results = search_in_index("\u89d2\u6709\u54ea\u4e9b\u5206\u7c7b", index_data, chunks, top_k=2)

        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "classification")

    def test_chinese_query_matches_overlapping_math_terms(self) -> None:
        chunks = [
            Chunk(
                chunk_id="simplify",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text="\u4e09\u89d2\u51fd\u6570\u5f0f\u7684\u5316\u7b80\n\u5e38\u7528\u65b9\u6cd5\uff1a\u76f4\u63a5\u5e94\u7528\u516c\u5f0f\u3001\u5207\u5316\u5f26\u3001\u5f02\u89d2\u5316\u540c\u89d2\u3002",
                section_title="\u4e09\u89d2\u51fd\u6570\u5f0f\u7684\u5316\u7b80",
            ),
            Chunk(
                chunk_id="image",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text="\u4e09\u89d2\u51fd\u6570\u7684\u56fe\u50cf\u4e0e\u6027\u8d28\n\u5468\u671f\u6027\u3001\u5947\u5076\u6027\u548c\u5355\u8c03\u6027\u3002",
                section_title="\u4e09\u89d2\u51fd\u6570\u7684\u56fe\u50cf\u4e0e\u6027\u8d28",
            ),
        ]

        index_data = build_search_index(chunks)
        results = search_in_index("\u4e09\u89d2\u51fd\u6570\u5982\u4f55\u5316\u7b80", index_data, chunks, top_k=2)

        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "simplify")

    def test_function_words_do_not_make_keyword_noise_rank_first(self) -> None:
        chunks = [
            Chunk(
                chunk_id="simplify",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text="\u4e09\u89d2\u51fd\u6570\u5f0f\u7684\u5316\u7b80\n\u5e38\u7528\u65b9\u6cd5\u5305\u62ec\u5207\u5316\u5f26\u548c\u5f02\u89d2\u5316\u540c\u89d2\u3002",
                section_title="\u4e09\u89d2\u51fd\u6570\u5f0f\u7684\u5316\u7b80",
            ),
            Chunk(
                chunk_id="question_words",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text="\u5982\u4f55\u5982\u4f55\u5982\u4f55\u3002\u8fd9\u4e00\u6bb5\u53ea\u662f\u95ee\u6cd5\u8bcd\u6c47\uff0c\u6ca1\u6709\u6838\u5fc3\u77e5\u8bc6\u70b9\u3002",
                section_title="\u95ee\u6cd5\u8bcd\u6c47",
            ),
        ]

        index_data = build_search_index(chunks)
        results = search_in_index("\u4e09\u89d2\u51fd\u6570\u5982\u4f55\u5316\u7b80", index_data, chunks, top_k=2)

        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "simplify")

    def test_domain_phrase_bonus_beats_scattered_generic_terms(self) -> None:
        chunks = [
            Chunk(
                chunk_id="rolle",
                material_id="mat_1",
                user_id="tester",
                chunk_index=0,
                text="\u7f57\u5c14\u5b9a\u7406\u662f\u4e2d\u503c\u5b9a\u7406\u7684\u91cd\u8981\u7279\u4f8b\uff0c\u5e38\u7528\u4e8e\u8bc1\u660e\u5bfc\u6570\u96f6\u70b9\u5b58\u5728\u3002",
                section_title="\u7f57\u5c14\u5b9a\u7406",
            ),
            Chunk(
                chunk_id="generic",
                material_id="mat_1",
                user_id="tester",
                chunk_index=1,
                text="\u5b9a\u7406\u5b9a\u7406\u5b9a\u7406\u5b9a\u7406\u3002\u8fd9\u4e00\u6bb5\u53ea\u91cd\u590d\u6cdb\u5316\u7684\u5b9a\u7406\u4e00\u8bcd\u3002",
                section_title="\u6cdb\u5316\u5b9a\u7406",
            ),
        ]

        index_data = build_search_index(chunks)
        results = search_in_index("\u7f57\u5c14\u5b9a\u7406\u600e\u4e48\u8bc1\u660e", index_data, chunks, top_k=2)

        self.assertTrue(results)
        self.assertEqual(results[0][0].chunk_id, "rolle")
        self.assertEqual([result[0].chunk_id for result in results], ["rolle"])


if __name__ == "__main__":
    unittest.main()
