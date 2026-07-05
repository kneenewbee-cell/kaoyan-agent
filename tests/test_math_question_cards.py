from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_math_question_cards.py"


class MathQuestionCardsTest(unittest.TestCase):
    def test_builds_question_cards_from_exam_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            exam_root = Path(tmp) / "exam_papers"
            year_dir = exam_root / "math1" / "2099"
            images_dir = year_dir / "images"
            images_dir.mkdir(parents=True)
            (images_dir / "q01-q02.png").write_bytes(b"fake")
            (images_dir / "q02_detail.png").write_bytes(b"fake")

            (year_dir / "math1_2099_questions.md").write_text(
                "\n".join(
                    [
                        "# Math 1 2099 Exam Questions",
                        "",
                        "资料类型：考研数学一历年真题  ",
                        "年份：2099  ",
                        "科目：数学一  ",
                        "整理状态：待复核  ",
                        "",
                        "## 2099 数一 选择题 1-2",
                        "",
                        "截图：",
                        "",
                        "![2099 数一第 1-2 题截图](images/q01-q02.png)",
                        "",
                        "### 第 1 题",
                        "",
                        "- 题型：选择题",
                        "- 题号：1",
                        "- 分值：5",
                        "- 模块：高数",
                        "- 考点：极限、导数",
                        "- 校对状态：根据截图整理",
                        "",
                        "设函数 `f(x)` 连续，则（ ）",
                        "",
                        "选项：A. 正确  B. 错误",
                        "",
                        "### 第 2 题",
                        "",
                        "- 题型：填空题",
                        "- 题号：2",
                        "- 分值：5",
                        "- 模块：线代",
                        "- 考点：矩阵",
                        "- 校对状态：已校对",
                        "",
                        "配图：",
                        "",
                        "![第 2 题细节](images/q02_detail.png)",
                        "",
                        "答案应满足 `x=____`。",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (year_dir / "math1_2099_answers.md").write_text(
                "\n".join(
                    [
                        "# Math 1 2099 Answers",
                        "",
                        "资料类型：考研数学一答案速查  ",
                        "年份：2099  ",
                        "科目：数学一  ",
                        "校对状态：用户确认  ",
                        "",
                        "## 选择题",
                        "",
                        "| 题号 | 答案 |",
                        "|---|---|",
                        "| 1 | A |",
                        "",
                        "## 详细解析",
                        "",
                        "### 第 1 题",
                        "",
                        "- 答案：A",
                        "",
                        "由连续性和导数定义可得本题选择 A。",
                        "",
                        "## 填空题",
                        "",
                        "| 题号 | 答案 |",
                        "|---|---|",
                        "| 2 | `1` |",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            stale_card = year_dir / "questions" / "q003.md"
            stale_card.parent.mkdir()
            stale_card.write_text("stale placeholder", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(exam_root),
                    "--exam-type",
                    "math1",
                    "--year",
                    "2099",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            q001 = year_dir / "questions" / "q001.md"
            q002 = year_dir / "questions" / "q002.md"
            self.assertTrue(q001.exists())
            self.assertTrue(q002.exists())
            self.assertFalse(stale_card.exists())

            q001_text = q001.read_text(encoding="utf-8")
            self.assertIn("question_id: kaoyan_math1_2099_q001", q001_text)
            self.assertIn("question_type: single_choice", q001_text)
            self.assertIn("module: 高数", q001_text)
            self.assertIn("  - 极限", q001_text)
            self.assertIn("answer_status: confirmed", q001_text)
            self.assertIn("explanation_status: available", q001_text)
            self.assertIn("  - images/q01-q02.png", q001_text)
            self.assertIn("![2099 数一第 1-2 题截图](../images/q01-q02.png)", q001_text)
            self.assertIn("## 标准答案\n\nA", q001_text)
            self.assertIn("## 解析\n\n由连续性和导数定义可得本题选择 A。", q001_text)

            q002_text = q002.read_text(encoding="utf-8")
            self.assertIn("question_type: fill_blank", q002_text)
            self.assertIn("explanation_status: missing", q002_text)
            self.assertIn("review_status: confirmed", q002_text)
            self.assertIn("  - images/q02_detail.png", q002_text)
            self.assertIn("![第 2 题细节](../images/q02_detail.png)", q002_text)
            self.assertIn("## 标准答案\n\n`1`", q002_text)

            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual([row["question_id"] for row in rows], ["kaoyan_math1_2099_q001", "kaoyan_math1_2099_q002"])
            self.assertEqual(rows[0]["answer"], "A")
            self.assertEqual(rows[0]["explanation"], "由连续性和导数定义可得本题选择 A。")
            self.assertEqual(rows[0]["explanation_status"], "available")
            self.assertEqual(rows[1]["explanation_status"], "missing")
            self.assertEqual(rows[0]["assets"], ["images/q01-q02.png"])
            self.assertEqual(rows[1]["assets"], ["images/q01-q02.png", "images/q02_detail.png"])

            manifest = json.loads((year_dir / "paper_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["exam_id"], "kaoyan_math1_2099")
            self.assertEqual(manifest["question_count"], 2)
            self.assertEqual(manifest["card_dir"], "questions")

    def test_question_images_do_not_leak_to_later_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            exam_root = Path(tmp) / "exam_papers"
            year_dir = exam_root / "math1" / "2098"
            images_dir = year_dir / "images"
            images_dir.mkdir(parents=True)
            for name in ("group.png", "q001.png", "q002.png"):
                (images_dir / name).write_bytes(b"fake")

            (year_dir / "math1_2098_questions.md").write_text(
                "\n".join(
                    [
                        "# Math 1 2098 Exam Questions",
                        "",
                        "资料类型：考研数学一历年真题",
                        "年份：2098",
                        "科目：数学一",
                        "",
                        "## 2098 数一 选择题",
                        "",
                        "截图：",
                        "",
                        "![组图](images/group.png)",
                        "",
                        "### 第 1 题",
                        "",
                        "- 题型：选择题",
                        "- 题号：一(1)",
                        "- 分值：4",
                        "- 校对状态：人工视觉识别",
                        "",
                        "题干 1。",
                        "",
                        "![第 1 题图](images/q001.png)",
                        "",
                        "### 第 2 题",
                        "",
                        "- 题型：选择题",
                        "- 题号：一(2)",
                        "- 分值：4",
                        "- 校对状态：人工视觉识别",
                        "",
                        "题干 2。",
                        "",
                        "![第 2 题图](images/q002.png)",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (year_dir / "math1_2098_answers.md").write_text("# Answers\n", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(exam_root),
                    "--exam-type",
                    "math1",
                    "--year",
                    "2098",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(rows[0]["assets"], ["images/group.png", "images/q001.png"])
            self.assertEqual(rows[1]["assets"], ["images/group.png", "images/q002.png"])

            q002_text = (year_dir / "questions" / "q002.md").read_text(encoding="utf-8")
            self.assertIn("../images/q002.png", q002_text)
            self.assertNotIn("../images/q001.png", q002_text)


if __name__ == "__main__":
    unittest.main()
