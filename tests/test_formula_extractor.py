from __future__ import annotations

import unittest

from materials.postprocess.formula_extractor import extract_formula_candidates, extract_formula_occurrences


class FormulaExtractorTest(unittest.TestCase):
    def test_table_cell_formula_keeps_escaped_latex_pipe_inside_cell(self) -> None:
        markdown = (
            "| scope | parameter | condition | statistic | interval |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| one | mean | known | { \\frac { { \\overline { { X } } } - \\mu } "
            "{ \\sigma _ { \\circ } { \\mathord { \\left/ { \\vphantom { \\Biggl { \\| } } } "
            "\\right. \\kern - delimiterspace } { \\sqrt { n } } } } } \\sim N ( 0 , 1 ) "
            "| ci |\n"
        )

        occurrences = extract_formula_occurrences(
            markdown,
            issue_patterns=[r"\\kern\s*-\s*delimiterspace"],
        )

        self.assertEqual(len(occurrences), 1)
        occurrence = occurrences[0]
        self.assertEqual(occurrence.container, "table_cell")
        self.assertEqual(occurrence.line_start, 3)
        self.assertEqual(occurrence.extract_confidence, "high")
        self.assertTrue(occurrence.formula.startswith("{ \\frac"))
        self.assertIn("\\vphantom { \\Biggl { \\| } }", occurrence.formula)
        self.assertIn("\\kern - delimiterspace", occurrence.formula)
        self.assertNotRegex(occurrence.formula, r"^\s*\}\s*\}\s*\}")

    def test_incomplete_boundary_is_flagged_before_llm_use(self) -> None:
        markdown = "bad $} } } \\right. \\kern - delimiterspace } { \\sqrt { n } }$"

        occurrences = extract_formula_occurrences(
            markdown,
            issue_patterns=[r"\\kern\s*-\s*delimiterspace"],
        )

        self.assertEqual(len(occurrences), 1)
        self.assertEqual(occurrences[0].extract_confidence, "low")
        self.assertIn("starts_with_closing_braces", occurrences[0].completeness_errors)

    def test_table_cell_formula_keeps_left_right_absolute_value_pipes(self) -> None:
        markdown = (
            "| name | formula |\n"
            "| --- | --- |\n"
            "| abs | \\left| x \\right| + \\kern - delimiterspace |\n"
        )

        occurrences = extract_formula_occurrences(
            markdown,
            issue_patterns=[r"\\kern\s*-\s*delimiterspace"],
        )

        self.assertEqual(len(occurrences), 1)
        self.assertEqual(occurrences[0].container, "table_cell")
        self.assertTrue(occurrences[0].formula.startswith("\\left| x \\right|"))
        self.assertIn("\\kern - delimiterspace", occurrences[0].formula)

    def test_multiline_display_math_is_extracted_as_one_candidate(self) -> None:
        markdown = (
            "# Root\n\n"
            "$$\n"
            "\\begin{array}{r l}\n"
            "a &= b \\\\\n"
            "\\end{array}\n"
            "$$\n"
        )

        candidates = extract_formula_candidates(markdown)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].container, "display_math")
        self.assertEqual(candidates[0].line_start, 3)
        self.assertEqual(candidates[0].line_end, 7)
        self.assertIn("\\begin{array}{r l}", candidates[0].formula)
        self.assertIn("a &= b", candidates[0].formula)


if __name__ == "__main__":
    unittest.main()
