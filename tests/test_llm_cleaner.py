from __future__ import annotations

import unittest

from materials.postprocess.llm_cleaner import build_heading_review_context, clean_markdown_with_llm_patches


class FakeFormulaRepairClient:
    def __init__(
        self,
        *,
        variants: list[dict] | None = None,
    ) -> None:
        self.variants = variants or []
        self.variant_payloads: list[dict] = []
        self.heading_payloads: list[dict] = []

    def repair_formula_variants(self, payload: dict) -> dict:
        self.variant_payloads.append(payload)
        return {
            "formula_id": payload["formula_id"],
            "variants": self.variants,
        }

    def review_headings(self, payload: dict) -> dict:
        self.heading_payloads.append(payload)
        return {
            "quality": "warning",
            "issues": [
                {
                    "line": 3,
                    "type": "heading_level_jump",
                    "suggestion": "review level",
                }
            ],
        }


class LLMCleanerTest(unittest.TestCase):
    def test_llm_formula_repair_receives_complete_table_cell_and_applies_validated_variant(self) -> None:
        markdown = (
            "# Root\n\n"
            "| scope | parameter | condition | statistic | interval |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| one | mean | known | { \\frac { { \\overline { { X } } } - \\mu } "
            "{ \\sigma _ { \\circ } { \\mathord { \\left/ { \\vphantom { \\Biggl { \\| } } } "
            "\\right. \\kern - delimiterspace } { \\sqrt { n } } } } } \\sim N ( 0 , 1 ) "
            "| ci |\n"
        )
        client = FakeFormulaRepairClient(
            variants=[
                {
                    "formula": r"\frac{\bar X-\mu}{\sigma/\sqrt n}\sim N(0,1)",
                    "confidence": 0.91,
                    "reason": "test repair",
                }
            ]
        )

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            render_issue_patterns=[r"\\kern\s*-\s*delimiterspace"],
            render_validator=lambda latex: "\\kern" not in latex and latex.count("{") == latex.count("}"),
        )

        self.assertEqual(len(client.variant_payloads), 1)
        self.assertTrue(client.variant_payloads[0]["formula"].startswith("{ \\frac"))
        self.assertIn("\\vphantom { \\Biggl { \\| } }", client.variant_payloads[0]["formula"])
        self.assertIn(r"\frac{\bar X-\mu}{\sigma/\sqrt n}\sim N(0,1)", result.cleaned_markdown)
        self.assertNotIn("\\kern - delimiterspace", result.cleaned_markdown)
        self.assertEqual(result.report["formula_repair"]["applied_count"], 1)
        self.assertEqual(result.report["formula_repair"]["applied"][0]["source"], "direct_variant")

    def test_visual_formula_warnings_are_not_sent_to_llm(self) -> None:
        markdown = "# Root\n\nvisual only $a \\atop b$"
        client = FakeFormulaRepairClient(variants=[{"formula": r"\frac{a}{b}", "confidence": 0.9}])

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            render_issue_patterns=[r"\\kern\s*-\s*delimiterspace"],
        )

        self.assertEqual(client.variant_payloads, [])
        self.assertEqual(result.cleaned_markdown, markdown)
        self.assertEqual(result.report["formula_repair"]["candidate_count"], 0)

    def test_render_failure_without_known_pattern_is_sent_to_llm(self) -> None:
        markdown = "# Root\n\nbroken $x + \\operatornamesharp y$"
        client = FakeFormulaRepairClient(
            variants=[{"formula": r"x + \operatorname{sharp} y", "confidence": 0.91}]
        )

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            formula_render_checker=lambda latex, container: (
                False,
                "Undefined control sequence: \\operatornamesharp",
            )
            if "\\operatornamesharp" in latex
            else (True, None),
            render_validator=lambda latex: "\\operatornamesharp" not in latex,
        )

        self.assertEqual(len(client.variant_payloads), 1)
        self.assertEqual(client.variant_payloads[0]["formula"], "x + \\operatornamesharp y")
        self.assertIn("Undefined control sequence", client.variant_payloads[0]["render_issue"])
        self.assertIn(r"x + \operatorname{sharp} y", result.cleaned_markdown)
        self.assertEqual(result.report["formula_repair"]["candidate_source"], "render_checker")

    def test_render_checker_allows_visual_only_formula_to_stay_local(self) -> None:
        markdown = "# Root\n\nvisual $a \\atop b$"
        client = FakeFormulaRepairClient(variants=[{"formula": r"\frac{a}{b}", "confidence": 0.9}])

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            formula_render_checker=lambda latex, container: (True, None),
        )

        self.assertEqual(client.variant_payloads, [])
        self.assertEqual(result.cleaned_markdown, markdown)
        self.assertEqual(result.report["formula_repair"]["candidate_count"], 0)

    def test_unbalanced_formula_can_be_sent_for_review_without_auto_apply(self) -> None:
        markdown = "# Root\n\nbroken $f_Y(y)=\\mathrm{E$"
        client = FakeFormulaRepairClient(
            variants=[
                {
                    "formula": r"f_Y(y)=\begin{cases}1,&0\le y\le1\\0,&\text{otherwise}\end{cases}",
                    "confidence": 0.9,
                    "needs_human_review": True,
                }
            ],
        )

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            formula_render_checker=lambda latex, container: (False, "Unexpected end of input"),
            render_validator=lambda latex: True,
        )

        self.assertEqual(len(client.variant_payloads), 1)
        self.assertIn("unbalanced_braces", client.variant_payloads[0]["completeness_errors"])
        self.assertEqual(result.cleaned_markdown, markdown)
        self.assertEqual(result.report["formula_repair"]["skipped"][0]["reason"], "no_valid_variant")
        self.assertIn("direct_variants", result.report["formula_repair"]["skipped"][0])

    def test_direct_variants_selects_highest_confidence_renderable_candidate(self) -> None:
        markdown = "# Root\n\nbroken $x + \\operatornamesharp y$"
        client = FakeFormulaRepairClient(
            variants=[
                {"formula": r"x + \operatornamesharp y", "confidence": 0.99, "reason": "still broken"},
                {"formula": r"x + \operatorname{sharp} y", "confidence": 0.92, "reason": "renderable"},
                {"formula": r"x + \mathrm{sharp} y", "confidence": 0.75, "reason": "lower confidence"},
            ],
        )

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            formula_render_checker=lambda latex, container: (
                False,
                "Undefined control sequence: \\operatornamesharp",
            )
            if "\\operatornamesharp" in latex
            else (True, None),
            render_validator=lambda latex: "\\operatornamesharp" not in latex,
        )

        self.assertEqual(len(client.variant_payloads), 1)
        self.assertIn(r"x + \operatorname{sharp} y", result.cleaned_markdown)
        self.assertEqual(result.report["formula_repair"]["applied_count"], 1)
        self.assertEqual(result.report["formula_repair"]["applied"][0]["source"], "direct_variant")
        self.assertEqual(len(result.report["formula_repair"]["applied"][0]["variants"]), 3)

    def test_bare_formula_line_render_failure_is_sent_to_llm(self) -> None:
        markdown = "# Root\n\nf ( x ) = \\left\\{ { 1 } & { x > 0 } \\\\ { 0 } & { x \\leq 0 } \\right. \\kern - delimiterspace\n"
        client = FakeFormulaRepairClient(
            variants=[{"formula": r"f(x)=\begin{cases}1\\0\end{cases}", "confidence": 0.91}]
        )

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=client,
            formula_render_checker=lambda latex, container: (False, "Invalid size: '- '")
            if "\\kern - delimiterspace" in latex
            else (True, None),
            render_validator=lambda latex: "\\kern" not in latex,
        )

        self.assertEqual(len(client.variant_payloads), 1)
        self.assertEqual(client.variant_payloads[0]["container"], "formula_line")
        self.assertIn(r"f(x)=\begin{cases}1\\0\end{cases}", result.cleaned_markdown)

    def test_heading_context_comes_from_dynamic_stack(self) -> None:
        markdown = "# Root\n\n##### Deep Jump\n\nText\n\n## Sibling\n"

        context = build_heading_review_context(markdown)

        self.assertEqual(context["heading_tree"][0]["title"], "Root")
        self.assertEqual(context["heading_tree"][0]["children"][0]["title"], "Deep Jump")
        self.assertEqual(context["heading_events"][0]["event"], "heading_level_jump")
        self.assertEqual(context["heading_events"][0]["from_level"], 1)
        self.assertEqual(context["heading_events"][0]["to_level"], 5)

    def test_heading_review_client_receives_dynamic_stack_context(self) -> None:
        markdown = "# Root\n\n##### Deep Jump\n\nText\n"
        client = FakeFormulaRepairClient()

        result = clean_markdown_with_llm_patches(
            markdown,
            formula_repair_client=None,
            heading_review_client=client,
        )

        self.assertEqual(len(client.heading_payloads), 1)
        self.assertEqual(client.heading_payloads[0]["heading_context"]["heading_events"][0]["event"], "heading_level_jump")
        self.assertTrue(result.report["heading_review"]["enabled"])
        self.assertEqual(result.report["heading_review"]["review"]["quality"], "warning")


if __name__ == "__main__":
    unittest.main()
