from __future__ import annotations

import unittest

from materials.postprocess.formula_cleaner import clean_formulas, clean_formulas_with_report


class FormulaCleanerTest(unittest.TestCase):
    def test_textcircled_digits_and_chinese_numerals_render_as_unicode(self) -> None:
        markdown = (
            "步骤 $\\textcircled { 1 }$ 已正常，"
            "$\\textcircled { 2 }$、$\\textcircled { 四 }$ 在 Obsidian 中应可渲染。"
        )

        result = clean_formulas_with_report(markdown)

        self.assertIn("$①$", result.cleaned_markdown)
        self.assertIn("$②$", result.cleaned_markdown)
        self.assertIn("$④$", result.cleaned_markdown)
        self.assertEqual(result.stats["rules"]["textcircled_unicode"]["changed"], 3)
        self.assertEqual(clean_formulas(markdown), result.cleaned_markdown)

    def test_textcircled_unknown_content_is_reported_but_not_changed(self) -> None:
        markdown = "保留非序号：$\\textcircled { X }$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\textcircled { X }", result.cleaned_markdown)
        self.assertEqual(result.stats["rules"]["textcircled_unsupported"]["reported"], 1)
        self.assertIn("formula_textcircled_unsupported", result.warnings)

    def test_safe_latex_noise_rules_are_idempotent(self) -> None:
        markdown = (
            "$\\operatorname* { l i m } _ { x  \\infty } "
            "\\mathbf { x } \\boldsymbol { y } \\mathrm { e } "
            "\\sp { 2 } \\displaylimits$"
        )

        once = clean_formulas_with_report(markdown)
        twice = clean_formulas_with_report(once.cleaned_markdown)

        self.assertIn("\\lim _ { x \\to \\infty }", once.cleaned_markdown)
        self.assertIn("\\mathbf{x}", once.cleaned_markdown)
        self.assertIn("\\boldsymbol{y}", once.cleaned_markdown)
        self.assertIn("\\mathrm{e}", once.cleaned_markdown)
        self.assertIn("^{ 2 }", once.cleaned_markdown)
        self.assertIn("\\limits", once.cleaned_markdown)
        self.assertEqual(once.cleaned_markdown, twice.cleaned_markdown)

    def test_code_fences_inline_code_tables_and_images_are_not_changed(self) -> None:
        markdown = (
            "正文 $\\textcircled { 2 }$\n\n"
            "`\\textcircled { 3 }`\n\n"
            "```tex\n\\textcircled { 4 }\n```\n\n"
            "| raw |\n| --- |\n| \\textcircled { 5 } |\n\n"
            "![\\textcircled { 6 }](images/figure.png)\n"
        )

        result = clean_formulas_with_report(markdown)

        self.assertIn("正文 $②$", result.cleaned_markdown)
        self.assertIn("`\\textcircled { 3 }`", result.cleaned_markdown)
        self.assertIn("```tex\n\\textcircled { 4 }\n```", result.cleaned_markdown)
        self.assertIn("| \\textcircled { 5 } |", result.cleaned_markdown)
        self.assertIn("![\\textcircled { 6 }](images/figure.png)", result.cleaned_markdown)

    def test_spaced_function_names_are_normalized(self) -> None:
        markdown = "$\\mathrm { s i n } x + \\mathrm{c o s} x + \\mathrm{l n} x + \\mathrm{e}$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\sin x", result.cleaned_markdown)
        self.assertIn("\\cos x", result.cleaned_markdown)
        self.assertIn("\\ln x", result.cleaned_markdown)
        self.assertIn("\\mathrm{e}", result.cleaned_markdown)

    def test_operatorname_spaced_letters_are_collapsed_or_mapped(self) -> None:
        markdown = "$\\operatorname* { m a x } x + \\operatorname { s g n } x + \\operatorname* { d i m } V$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\max x", result.cleaned_markdown)
        self.assertIn("\\operatorname{sgn} x", result.cleaned_markdown)
        self.assertIn("\\dim V", result.cleaned_markdown)

    def test_operatorname_star_argument_spacing_is_normalized_without_guessing(self) -> None:
        markdown = "$\\operatorname* { m } _x + \\operatorname* { \\cdot } _ { x \\to 0 }$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\operatorname*{m} _x", result.cleaned_markdown)
        self.assertIn("\\operatorname*{\\cdot} _ { x \\to 0 }", result.cleaned_markdown)
        self.assertNotIn("\\max", result.cleaned_markdown)
        self.assertEqual(result.stats["rules"]["operatorname_star_ambiguous"]["reported"], 2)

    def test_safe_visual_operator_and_nested_style_noise_is_normalized(self) -> None:
        markdown = "$\\operatorname{e}^x + \\operatorname{d} x + \\mathrm{ { e } } + \\mathbf{ { x } }$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\mathrm{e}^x", result.cleaned_markdown)
        self.assertIn("\\mathrm{d} x", result.cleaned_markdown)
        self.assertIn("\\mathbf{x}", result.cleaned_markdown)
        self.assertNotIn("\\mathrm{ { e } }", result.cleaned_markdown)

    def test_targeted_visual_repairs_for_right_dot_big_int_and_em(self) -> None:
        markdown = "$\\lim _ { t \\right. \\infty } \\Big \\int_0^1 x dx + |\\textbf{\\em a}|$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\lim _ { t \\to \\infty }", result.cleaned_markdown)
        self.assertIn("\\int_0^1", result.cleaned_markdown)
        self.assertIn("|\\boldsymbol{a}|", result.cleaned_markdown)

    def test_simple_frac_argument_spacing_is_normalized(self) -> None:
        markdown = "$\\frac{0} { 0 } + \\frac{ } { }$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\frac{0}{0}", result.cleaned_markdown)
        self.assertIn("\\frac{}{}", result.cleaned_markdown)

    def test_textmu_is_normalized_to_math_mu(self) -> None:
        markdown = "$\\mathrm{\\textmu} + \\textmu$"

        result = clean_formulas_with_report(markdown)

        self.assertIn("\\mathrm{\\mu} + \\mu", result.cleaned_markdown)
        self.assertEqual(result.stats["rules"]["textmu_to_mu"]["changed"], 2)

    def test_safe_render_error_noise_is_normalized(self) -> None:
        markdown = (
            "$\\lim_{x\\to0} x\\tag{#} + \\hfill + \\medskip + \\mathbb{\\} "
            "+ a \\nA \\gg y + \\pi \\1 _ { 0 } ^ { 1 } f(x) dx$"
        )

        result = clean_formulas_with_report(markdown)

        self.assertNotIn("\\tag{#}", result.cleaned_markdown)
        self.assertNotIn("\\hfill", result.cleaned_markdown)
        self.assertNotIn("\\medskip", result.cleaned_markdown)
        self.assertNotIn("\\mathbb{\\}", result.cleaned_markdown)
        self.assertIn("a \\quad \\gg y", result.cleaned_markdown)
        self.assertIn("\\pi \\int _ { 0 } ^ { 1 }", result.cleaned_markdown)
        self.assertEqual(result.stats["rules"]["invalid_hash_tag_removed"]["changed"], 1)
        self.assertEqual(result.stats["rules"]["formula_layout_command_removed"]["changed"], 2)
        self.assertEqual(result.stats["rules"]["mathbb_backslash_removed"]["changed"], 1)
        self.assertEqual(result.stats["rules"]["ocr_nA_to_quad"]["changed"], 1)
        self.assertEqual(result.stats["rules"]["ocr_backslash_one_to_int"]["changed"], 1)


if __name__ == "__main__":
    unittest.main()
