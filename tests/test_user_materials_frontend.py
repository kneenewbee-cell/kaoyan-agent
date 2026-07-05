from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "web" / "app.js"
INDEX_HTML = ROOT / "web" / "index.html"
STYLES_CSS = ROOT / "web" / "styles.css"


class UserMaterialsFrontendTests(unittest.TestCase):
    def test_search_workbench_exposes_scope_mode_limit_and_drawer(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")
        styles = STYLES_CSS.read_text(encoding="utf-8")

        self.assertIn('id="materialsSearchScope"', html)
        self.assertIn('id="materialsSearchMode"', html)
        self.assertIn('id="materialsSearchLimit"', html)
        self.assertIn('id="materialDetailDrawer"', html)
        self.assertIn("function setMaterialSearchScope", source)
        self.assertIn("function openMaterialDetailDrawer", source)
        self.assertIn("function buildMaterialsSearchUrl", source)
        self.assertIn(".material-detail-drawer", styles)
        self.assertIn(".materials-search-controls", styles)

    def test_search_results_render_llm_reason_and_concept_coverage(self) -> None:
        source = APP_JS.read_text(encoding="utf-8")

        self.assertIn("function renderConceptCoverage", source)
        self.assertIn("function resultDecisionLabel", source)
        self.assertIn("result.llm_rerank", source)
        self.assertIn("retrieval_plan", source)
        self.assertIn("强匹配", source)
        self.assertIn("相关参考", source)

    def test_user_material_type_labels_only_expose_three_active_types(self) -> None:
        html = INDEX_HTML.read_text(encoding="utf-8")
        source = APP_JS.read_text(encoding="utf-8")

        select_start = html.index('id="materialsType"')
        select_end = html.index("</select>", select_start)
        upload_select = html[select_start:select_end]
        self.assertIn('value="textbook"', upload_select)
        self.assertIn('value="lecture"', upload_select)
        self.assertIn('value="exercise"', upload_select)
        self.assertNotIn('value="note"', upload_select)
        self.assertNotIn('value="exam"', upload_select)
        self.assertNotIn('value="wrong_book"', upload_select)
        self.assertNotIn('value="school_info"', upload_select)

        labels_start = source.index("const MATERIAL_TYPE_LABELS")
        labels_end = source.index("const MATERIAL_STATUS_LABELS", labels_start)
        labels_block = source[labels_start:labels_end]
        self.assertIn("textbook:", labels_block)
        self.assertIn("lecture:", labels_block)
        self.assertIn("exercise:", labels_block)
        self.assertNotIn("note:", labels_block)
        self.assertNotIn("exam:", labels_block)
        self.assertNotIn("wrong_book:", labels_block)
        self.assertNotIn("school_info:", labels_block)


if __name__ == "__main__":
    unittest.main()
