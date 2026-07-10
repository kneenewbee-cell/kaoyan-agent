from __future__ import annotations

import unittest

from materials.postprocess.exercise_structure import analyze_exercise_structure
from materials.postprocess.exercise_structure_repair import repair_exercise_structure


class FakeBoundaryClient:
    model = "deepseek-v4-flash"

    def __init__(self, judgement: dict) -> None:
        self.judgement = judgement
        self.payloads: list[dict] = []

    def judge_problem_boundary(self, payload: dict) -> dict:
        self.payloads.append(payload)
        return dict(self.judgement)


class ExerciseStructureRepairTest(unittest.TestCase):
    def test_repairs_missing_problem_absorbed_by_previous_group(self) -> None:
        markdown = """# 真题

## 填空题(本题共3小题)

(1) 第一题
正文一。
干扰(2) 已知线性方程组有解，求参数。
参数条件继续。

(3) 第三题
正文三。
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "split_previous_problem",
                "target_problem_index": 2,
                "start_line": 7,
                "end_line": 8,
                "confidence": 0.91,
                "title": "(2) 已知线性方程组有解，求参数。",
                "reason_codes": ["contaminated_marker_inside_previous_problem"],
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)
        groups = result["problem_groups"]

        self.assertEqual([group["problem_index"] for group in groups], [1, 2, 3])
        self.assertEqual(groups[0]["end_line"], 6)
        self.assertEqual(groups[1]["problem_id"], "problem_002")
        self.assertEqual(groups[1]["start_line"], 7)
        self.assertEqual(groups[1]["end_line"], 8)
        self.assertEqual(result["report"]["applied_count"], 1)
        self.assertEqual(result["report"]["candidate_count"], 1)
        self.assertEqual(client.payloads[0]["target_missing_index"], 2)
        self.assertEqual(client.payloads[0]["candidate_type"], "sequence_gap")

    def test_rejects_llm_split_on_option_line(self) -> None:
        markdown = """# 真题

## 选择题(本题共3小题)

(1) 第一题
A. 选项一
B. 选项二

(3) 第三题
正文三。
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "split_previous_problem",
                "target_problem_index": 2,
                "start_line": 6,
                "end_line": 7,
                "confidence": 0.96,
                "title": "(2) 选项误判",
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)

        self.assertEqual([group["problem_index"] for group in result["problem_groups"]], [1, 3])
        self.assertEqual(result["report"]["applied_count"], 0)
        self.assertEqual(result["report"]["skipped"][0]["reason"], "candidate_starts_on_non_problem_line")

    def test_without_llm_client_reports_candidates_but_does_not_apply(self) -> None:
        markdown = """# 真题

## 填空题(本题共3小题)

(1) 第一题
疑似(2) 第二题被粘连。

(3) 第三题
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")

        result = repair_exercise_structure(markdown, initial, llm_client=None)

        self.assertFalse(result["report"]["enabled"])
        self.assertEqual(result["report"]["candidate_count"], 1)
        self.assertEqual(result["report"]["applied_count"], 0)
        self.assertEqual([group["problem_index"] for group in result["problem_groups"]], [1, 3])

    def test_payload_highlights_orphan_problem_like_lines_without_marker(self) -> None:
        markdown = """# 真题

## 解答题(本题共3小题)

(1) 第一问
已知区域 A，求面积。

设平面有界区域D位于第一象限，计算二重积分。
2-3 题 APP扫码听课

(3) 第三问
证明不等式。
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "split_previous_problem",
                "target_problem_index": 2,
                "start_line": 8,
                "end_line": 9,
                "confidence": 0.86,
                "title": "(2) 设平面有界区域D位于第一象限，计算二重积分。",
                "reason_codes": ["orphan_problem_like_block"],
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)

        self.assertEqual(result["report"]["applied_count"], 1)
        self.assertEqual(client.payloads[0]["suspected_orphan_lines"][0]["line_no"], 8)
        self.assertIn("设平面有界区域D", client.payloads[0]["suspected_orphan_lines"][0]["text"])

    def test_repair_does_not_merge_late_subquestion_numbers_into_early_problems(self) -> None:
        markdown = """# 真题

1. 第一题

2. 第二题

21. 第二十一题

(1) 第一小问

22. 第二十二题

（2）第二小问
"""
        exercise_report = {
            "missing_problem_indices": [],
            "problem_groups": [
                {"problem_id": "problem_001", "problem_index": 1, "problem_kind": "question", "title": "1. 第一题", "start_line": 3, "end_line": 4, "heading_path": ["1. 第一题"]},
                {"problem_id": "problem_002", "problem_index": 2, "problem_kind": "question", "title": "2. 第二题", "start_line": 5, "end_line": 6, "heading_path": ["2. 第二题"]},
                {"problem_id": "problem_021", "problem_index": 21, "problem_kind": "question", "title": "21. 第二十一题", "start_line": 7, "end_line": 8, "heading_path": ["21. 第二十一题"]},
                {"problem_id": "problem_001", "problem_index": 1, "problem_kind": "question", "title": "(1) 第一小问", "start_line": 9, "end_line": 10, "heading_path": ["21. 第二十一题", "(1) 第一小问"]},
                {"problem_id": "problem_022", "problem_index": 22, "problem_kind": "question", "title": "22. 第二十二题", "start_line": 11, "end_line": 12, "heading_path": ["22. 第二十二题"]},
                {"problem_id": "problem_002", "problem_index": 2, "problem_kind": "question", "title": "（2）第二小问", "start_line": 13, "end_line": 13, "heading_path": ["22. 第二十二题", "（2）第二小问"]},
            ],
        }

        result = repair_exercise_structure(markdown, exercise_report, llm_client=None)
        groups = result["problem_groups"]

        self.assertEqual(groups[0]["problem_index"], 1)
        self.assertEqual(groups[0]["end_line"], 4)
        self.assertEqual(groups[1]["problem_index"], 2)
        self.assertEqual(groups[1]["end_line"], 6)
        self.assertEqual([group["start_line"] for group in groups], [3, 5, 7, 9, 11, 13])

    def test_repair_uses_sequence_gap_candidate_scope_when_numbers_restart(self) -> None:
        markdown = """# 分类练习

## 一、选择题

1. 选择第一题

2. 选择第二题

## 二、填空题

1. 填空第一题
疑似第二题被粘在这里。

3. 填空第三题
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "split_previous_problem",
                "target_problem_index": 2,
                "start_line": 12,
                "end_line": 12,
                "confidence": 0.9,
                "title": "2. 填空第二题",
                "reason_codes": ["sequence_gap_in_restarted_scope"],
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)
        payload = client.payloads[0]
        groups = result["problem_groups"]

        self.assertEqual(payload["previous_problem"]["title"], "1. 填空第一题")
        self.assertEqual(payload["next_problem"]["title"], "3. 填空第三题")
        self.assertEqual([group["title"] for group in groups], ["1. 选择第一题", "2. 选择第二题", "1. 填空第一题", "2. 填空第二题", "3. 填空第三题"])

    def test_tail_candidate_sends_last_problem_window_to_llm(self) -> None:
        markdown = """# 真题

22. 第二十二题
第一行正文。
第二行正文。
第三行正文。
设另一个新问题，求参数。
继续新问题正文。
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "split_previous_problem",
                "target_problem_index": 23,
                "start_line": 7,
                "end_line": 8,
                "confidence": 0.88,
                "title": "23. 设另一个新问题，求参数。",
                "reason_codes": ["tail_problem_absorption"],
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)

        self.assertEqual(client.payloads[0]["candidate_type"], "tail_problem_absorption")
        self.assertEqual(result["report"]["applied_count"], 1)
        self.assertEqual([group["problem_index"] for group in result["problem_groups"]], [22, 23])

    def test_strong_local_gap_evidence_can_override_llm_no_split(self) -> None:
        markdown = """# 真题

(19) 第十九题
已知平面区域 D。
(I）求D的面积；
（Ⅱ）求D绕x轴旋转所成旋转体的体积。

设平面有界区域D位于第一象限，计算二重积分。
20-22 题 APP扫码听课

(21) 第二十一题
证明命题。
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "no_split",
                "target_problem_index": 20,
                "start_line": None,
                "end_line": None,
                "confidence": 0.9,
                "title": "",
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)

        self.assertEqual(result["report"]["applied_count"], 1)
        self.assertIn("local_high_confidence_sequence_gap", result["report"]["applied"][0]["reason_codes"])
        self.assertEqual([group["problem_index"] for group in result["problem_groups"]], [19, 20, 21])

    def test_low_paren_sequence_in_single_gap_can_repair_missing_problem_stem(self) -> None:
        markdown = """# 真题

6. 第六题有完整 A B C D 选项。

(1）若条件一成立；

（2）若条件二成立；

（3）若条件三成立；

8. 第八题
"""
        initial = analyze_exercise_structure(markdown, material_type="exercise")
        client = FakeBoundaryClient(
            {
                "decision": "no_split",
                "target_problem_index": 7,
                "start_line": None,
                "end_line": None,
                "confidence": 0.9,
                "title": "",
            }
        )

        result = repair_exercise_structure(markdown, initial, llm_client=client)

        self.assertEqual(result["report"]["applied_count"], 1)
        self.assertIn("low_paren_sequence_after_previous_problem", result["report"]["applied"][0]["reason_codes"])
        self.assertEqual([group["problem_index"] for group in result["problem_groups"]], [6, 7, 8])


if __name__ == "__main__":
    unittest.main()
