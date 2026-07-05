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
        self.assertEqual(client.payloads[0]["candidate_type"], "previous_problem_absorption")

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


if __name__ == "__main__":
    unittest.main()
