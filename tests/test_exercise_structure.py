from __future__ import annotations

import unittest

from materials.chunking.chunker import chunk_markdown
from materials.postprocess.exercise_structure import analyze_exercise_structure


class ExerciseStructureTest(unittest.TestCase):
    def test_extracts_problem_groups_and_solution_labels(self) -> None:
        markdown = """# 2023 math paper

## 一、选择题

### (1) 设函数 f(x) 连续，求极限

A. 0
B. 1

**解析：** 先化简再代入。

### (2) 已知矩阵 A，求行列式

**答案：** 2
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["status"], "high")
        self.assertEqual(report["problem_count"], 2)
        self.assertEqual(report["solution_label_count"], 2)
        self.assertEqual(report["problem_groups"][0]["problem_id"], "problem_001")
        self.assertEqual(report["problem_groups"][0]["problem_index"], 1)
        self.assertEqual(report["problem_groups"][0]["problem_kind"], "question")
        self.assertEqual(report["problem_groups"][0]["title"], "(1) 设函数 f(x) 连续，求极限")
        self.assertLess(report["problem_groups"][0]["start_line"], report["problem_groups"][0]["end_line"])

    def test_ignores_non_exercise_materials(self) -> None:
        report = analyze_exercise_structure("## 1. 极限定义\n\n正文", material_type="lecture")

        self.assertEqual(report["status"], "skipped")
        self.assertEqual(report["problem_count"], 0)
        self.assertEqual(report["problem_groups"], [])

    def test_does_not_treat_options_as_problem_groups(self) -> None:
        markdown = """# exercise

## 第 1 题

A. 正确选项
B. 干扰项
C. 干扰项
D. 干扰项

**答案：** A
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 1)
        self.assertEqual(report["suspicious_option_marker_count"], 4)
        self.assertEqual(report["problem_groups"][0]["problem_id"], "problem_001")

    def test_plain_problem_lines_detect_sequence_gap_without_parent_count(self) -> None:
        markdown = """# 真题

## 一、选择题(本题共4小题，每小题5分)

(1) 第一题

(2) 第二题

(4) 第四题
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 3)
        self.assertIsNone(report["expected_problem_count"])
        self.assertEqual(report["missing_problem_indices"], [3])
        self.assertEqual(report["status"], "medium")
        self.assertEqual(report["problem_groups"][0]["problem_index"], 1)
        self.assertEqual(report["problem_groups"][2]["problem_index"], 4)
        self.assertEqual(report["sequence_gap_candidates"][0]["target_problem_index"], 3)
        self.assertNotIn("expected_problem_count_source_parent_heading", report["warnings"])

    def test_reports_low_when_no_problem_groups_are_found(self) -> None:
        markdown = "# 习题资料\n\n这是一段没有题号的普通正文。\n\n**解析：** 只有解析没有题目。"

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["status"], "low")
        self.assertEqual(report["problem_count"], 0)
        self.assertEqual(report["solution_label_count"], 1)
        self.assertIn("exercise_no_problem_groups", report["warnings"])


class ExerciseProblemChunkingTest(unittest.TestCase):
    def test_chunker_prefers_problem_groups_and_adds_problem_metadata(self) -> None:
        markdown = """# 试题

## 一、选择题

### (1) 第一题

题干一。

### (2) 第二题

题干二。
"""
        exercise_report = analyze_exercise_structure(markdown, material_type="exercise")

        chunks = chunk_markdown(
            markdown,
            "mat_exercise",
            "tester",
            problem_groups=exercise_report["problem_groups"],
        )

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["problem_id"], "problem_001")
        self.assertEqual(chunks[0].metadata["problem_unit_id"], "problem_unit_001")
        self.assertEqual(chunks[0].metadata["problem_index"], 1)
        self.assertEqual(chunks[0].metadata["problem_kind"], "question")
        self.assertEqual(chunks[1].metadata["problem_id"], "problem_002")
        self.assertEqual(chunks[1].metadata["problem_unit_id"], "problem_unit_002")
        self.assertEqual(chunks[1].metadata["problem_part_index"], 1)


class ExerciseStructureEdgeCaseTest(unittest.TestCase):
    def test_example_items_are_problem_groups(self) -> None:
        markdown = """# 例题讲义

## 二项分布

### 例1 二项分布的期望

题干。

**解：** 使用公式。

### 例题2 泊松分布近似

题干。

**评注：** 注意条件。
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 2)
        self.assertEqual([group["problem_kind"] for group in report["problem_groups"]], ["example", "example"])
        self.assertEqual(report["solution_label_count"], 2)

    def test_formula_numbers_are_not_problem_groups(self) -> None:
        markdown = """# 公式

## 二项分布

### (1.1)

$E(X)=np$

### (1) 设 X 服从二项分布，求期望

**答案：** np
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["problem_count"], 1)
        self.assertEqual(report["problem_groups"][0]["title"], "(1) 设 X 服从二项分布，求期望")

    def test_parent_heading_ranges_do_not_drive_missing_problem_detection(self) -> None:
        markdown = """# 2024 真题

## 三、解答题：（17-22小题，共70分。）

17. 第十七题

18. 第十八题

20. 第二十题
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertIsNone(report["expected_problem_count"])
        self.assertEqual(report["missing_problem_indices"], [19])
        self.assertEqual([group["problem_index"] for group in report["problem_groups"]], [17, 18, 20])

    def test_repeated_numbering_under_new_category_starts_new_problem_scope(self) -> None:
        markdown = """# 分类练习

## 一、选择题

1. 第一题

2. 第二题

3. 第三题

## 二、填空题

1. 第一题

2. 第二题

3. 第三题

4. 第四题
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")
        groups = report["problem_groups"]

        self.assertEqual(report["missing_problem_indices"], [])
        self.assertEqual([group["problem_index"] for group in groups], [1, 2, 3, 1, 2, 3, 4])
        self.assertEqual([group["problem_unit_id"] for group in groups], [f"problem_unit_{index:03d}" for index in range(1, 8)])
        self.assertNotEqual(groups[0]["problem_scope_id"], groups[3]["problem_scope_id"])

    def test_demotes_late_paren_subquestions_inside_arabic_problem_run(self) -> None:
        markdown = """# 真题

20. 第二十题

21. 第二十一题

(1) 第一小问

22. 第二十二题

（2）第二小问
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual([group["problem_index"] for group in report["problem_groups"]], [20, 21, 22])
        self.assertEqual(report["problem_count"], 3)
        self.assertIn("exercise_nested_question_markers_demoted", report["warnings"])

    def test_demotes_low_paren_subquestions_after_arabic_problem_in_same_scope(self) -> None:
        markdown = """# 真题

6. 第六题

(1）若条件一成立；

（2）若条件二成立；

（3）若条件三成立；

8. 第八题
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual([group["problem_index"] for group in report["problem_groups"]], [6, 8])
        self.assertEqual(report["missing_problem_indices"], [7])
        self.assertIn("exercise_nested_question_markers_demoted", report["warnings"])

    def test_sequence_gaps_are_reported_per_actual_problem_run(self) -> None:
        markdown = """# 真题

1. 第一题

2. 第二题

3. 第三题

5. 第五题

## 二、填空题

1. 第一题

2. 第二题
"""

        report = analyze_exercise_structure(markdown, material_type="exercise")

        self.assertEqual(report["missing_problem_indices"], [4])
        self.assertEqual(len(report["sequence_gap_candidates"]), 1)
        self.assertEqual(report["sequence_gap_candidates"][0]["target_problem_index"], 4)


if __name__ == "__main__":
    unittest.main()
