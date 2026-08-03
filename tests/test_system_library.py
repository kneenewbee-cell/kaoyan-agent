from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from materials.api import router as materials_router
from materials.system_library import SystemQuestionLibrary


class SystemQuestionLibraryTest(unittest.TestCase):
    def test_lists_filtered_questions_with_preview_and_asset_urls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            library = SystemQuestionLibrary(raw_root=raw_root)

            result = library.list_questions(
                subject="math",
                exam_type="math1",
                query="连续",
                page=1,
                page_size=10,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(result["subject"], "math")
            self.assertEqual(result["exam_type"], "math1")
            self.assertEqual(result["total"], 1)
            self.assertEqual(result["page"], 1)
            self.assertEqual(result["page_size"], 10)
            self.assertEqual(result["total_pages"], 1)
            self.assertEqual(len(result["items"]), 1)
            item = result["items"][0]
            self.assertEqual(item["question_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(item["library_name"], "数一历年真题")
            self.assertEqual(item["preview"], "设函数 `f(x)` 连续，则（ ）。")
            self.assertEqual(
                item["asset_urls"],
                ["/api/materials/system/assets/math1/2099/images/q001.png"],
            )

    def test_reuses_question_list_preview_cache_across_library_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            read_card_calls: list[str] = []
            original_read_text = Path.read_text

            def counting_read_text(path: Path, *args: object, **kwargs: object) -> str:
                if path.name == "q001.md":
                    read_card_calls.append(str(path))
                return original_read_text(path, *args, **kwargs)

            with patch.object(Path, "read_text", counting_read_text):
                first = SystemQuestionLibrary(raw_root=raw_root).list_questions(subject="math", exam_type="math1")
                second = SystemQuestionLibrary(raw_root=raw_root).list_questions(subject="math", exam_type="math1")

            self.assertEqual(first["total"], 1)
            self.assertEqual(second["total"], 1)
            self.assertEqual(len(read_card_calls), 1)

    def test_returns_complete_empty_shape_for_unsupported_subject_or_exam_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            library = SystemQuestionLibrary(raw_root=raw_root)

            for result in (
                library.list_questions(subject="english", exam_type="math1"),
                library.list_questions(subject="math", exam_type="math4"),
            ):
                self.assertEqual(
                    result,
                    {
                        "ok": True,
                        "subject": result["subject"],
                        "exam_type": result["exam_type"],
                        "total": 0,
                        "page": 1,
                        "page_size": 10,
                        "total_pages": 1,
                        "topic_options": [],
                        "items": [],
                    },
                )

    def test_lists_math2_and_math3_question_collections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            self._add_exam_question(
                raw_root,
                exam_type="math2",
                year=2099,
                question_number=1,
                topic="二重积分",
            )
            self._add_exam_question(
                raw_root,
                exam_type="math3",
                year=2098,
                question_number=2,
                topic="概率分布",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            math2 = library.list_questions(subject="math", exam_type="math2", page_size=10)
            math3 = library.list_questions(subject="math", exam_type="math3", page_size=10)
            all_math = library.list_questions(subject="math", exam_type="", page_size=10)

            self.assertEqual(math2["total"], 1)
            self.assertEqual(math2["items"][0]["question_id"], "kaoyan_math2_2099_q001")
            self.assertEqual(math2["items"][0]["exam_type_label"], "数二")
            self.assertEqual(math2["items"][0]["library_name"], "数二历年真题")
            self.assertEqual(math3["total"], 1)
            self.assertEqual(math3["items"][0]["question_id"], "kaoyan_math3_2098_q002")
            self.assertEqual(math3["items"][0]["exam_type_label"], "数三")
            self.assertEqual(math3["items"][0]["library_name"], "数三历年真题")
            self.assertIn("kaoyan_math1_2099_q001", [item["question_id"] for item in all_math["items"]])
            self.assertIn("kaoyan_math2_2099_q001", [item["question_id"] for item in all_math["items"]])
            self.assertIn("kaoyan_math3_2098_q002", [item["question_id"] for item in all_math["items"]])

    def test_topic_filter_matches_part_of_any_topic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            library = SystemQuestionLibrary(raw_root=raw_root)

            result = library.list_questions(subject="math", exam_type="math1", topic="续")

            self.assertEqual(result["total"], 1)
            self.assertEqual(result["items"][0]["question_id"], "kaoyan_math1_2099_q001")

    def test_topic_options_ignore_selected_topic_but_respect_other_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            rows.extend(
                [
                    {
                        **rows[0],
                        "question_id": "kaoyan_math1_2099_q101",
                        "question_number": 101,
                        "question_type": "single_choice",
                        "topics": ["topic-a"],
                        "card_path": "questions/q001.md",
                    },
                    {
                        **rows[0],
                        "question_id": "kaoyan_math1_2099_q102",
                        "question_number": 102,
                        "question_type": "single_choice",
                        "topics": ["topic-b"],
                        "card_path": "questions/q001.md",
                    },
                    {
                        **rows[0],
                        "question_id": "kaoyan_math1_2099_q103",
                        "question_number": 103,
                        "question_type": "solution",
                        "topics": ["topic-c"],
                        "card_path": "questions/q001.md",
                    },
                ]
            )
            (year_dir / "questions.jsonl").write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
                encoding="utf-8",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            result = library.list_questions(
                subject="math",
                exam_type="math1",
                question_type="single_choice",
                topic="topic-a",
            )

            self.assertEqual(result["total"], 1)
            self.assertIn("topic-a", result["topic_options"])
            self.assertIn("topic-b", result["topic_options"])
            self.assertNotIn("topic-c", result["topic_options"])

    def test_sorts_year_descending_and_question_number_ascending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            rows.extend(
                [
                    {
                        **rows[0],
                        "question_id": "kaoyan_math1_2099_q003",
                        "question_number": 3,
                        "card_path": "questions/q001.md",
                    },
                    {
                        **rows[0],
                        "question_id": "kaoyan_math1_2098_q001",
                        "exam_id": "kaoyan_math1_2098",
                        "year": 2098,
                        "question_number": 1,
                        "card_path": "questions/q001.md",
                    },
                ]
            )
            (year_dir / "questions.jsonl").write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
                encoding="utf-8",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            result = library.list_questions(subject="math", exam_type="math1", page_size=10)

            self.assertEqual(
                [item["question_id"] for item in result["items"][:3]],
                [
                    "kaoyan_math1_2099_q001",
                    "kaoyan_math1_2099_q003",
                    "kaoyan_math1_2098_q001",
                ],
            )

    def test_reads_question_detail_from_card_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            library = SystemQuestionLibrary(raw_root=raw_root)

            detail = library.get_question("kaoyan_math1_2099_q001")

            self.assertEqual(detail["answer"], "B")
            self.assertEqual(detail["explanation"], "由定义可得。")
            self.assertIn("`f(x)`", detail["question_markdown"])
            self.assertIn(
                "![题图](/api/materials/system/assets/math1/2099/images/q001.png)",
                detail["question_markdown"],
            )
            self.assertNotIn("../images/q001.png", detail["question_markdown"])
            self.assertLess(
                detail["question_markdown"].index("`f(x)`"),
                detail["question_markdown"].index("!["),
            )
            self.assertEqual(detail["answer_markdown"], "B")
            self.assertEqual(detail["explanation_markdown"], "由定义可得。")

    def test_question_detail_falls_back_when_card_or_sections_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            rows.extend(
                [
                    {
                        "question_id": "kaoyan_math1_2099_q002",
                        "exam_id": "kaoyan_math1_2099",
                        "exam_type": "math1",
                        "year": 2099,
                        "question_number": 2,
                        "question_type": "fill_blank",
                        "module": "高等数学",
                        "topics": ["导数"],
                        "difficulty": "unknown",
                        "card_path": "questions/q002.md",
                        "assets": [],
                        "answer": "ROW-ANSWER",
                        "explanation": "ROW-EXPLANATION",
                        "summary": "row summary question",
                    },
                    {
                        "question_id": "kaoyan_math1_2099_q003",
                        "exam_id": "kaoyan_math1_2099",
                        "exam_type": "math1",
                        "year": 2099,
                        "question_number": 3,
                        "question_type": "solution",
                        "module": "高等数学",
                        "topics": ["积分"],
                        "difficulty": "unknown",
                        "card_path": "questions/q003.md",
                        "assets": [],
                        "answer": "ROW-ONLY-ANSWER",
                        "explanation": "ROW-ONLY-EXPLANATION",
                        "preview": "row preview question",
                    },
                ]
            )
            (year_dir / "questions.jsonl").write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
                encoding="utf-8",
            )
            (year_dir / "questions" / "q002.md").write_text(
                "\n".join(
                    [
                        "---",
                        "question_id: kaoyan_math1_2099_q002",
                        "---",
                        "",
                        "## 题目",
                        "",
                        "题卡只有题目。",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            missing_sections = library.get_question("kaoyan_math1_2099_q002")
            self.assertEqual(missing_sections["question_markdown"], "题卡只有题目。")
            self.assertEqual(missing_sections["answer"], "ROW-ANSWER")
            self.assertEqual(missing_sections["explanation"], "ROW-EXPLANATION")

            missing_card = library.get_question("kaoyan_math1_2099_q003")
            self.assertEqual(missing_card["question_markdown"], "row preview question")
            self.assertEqual(missing_card["answer"], "ROW-ONLY-ANSWER")
            self.assertEqual(missing_card["explanation"], "ROW-ONLY-EXPLANATION")

    def test_question_detail_falls_back_when_card_path_traverses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            bad_row = {
                "question_id": "bad_card",
                "exam_id": "kaoyan_math1_2099",
                "exam_type": "math1",
                "year": 2099,
                "question_number": 4,
                "question_type": "single_choice",
                "module": "高等数学",
                "topics": ["连续"],
                "difficulty": "unknown",
                "card_path": "../outside.md",
                "assets": [],
                "answer": "ROW-BAD-ANSWER",
                "explanation": "ROW-BAD-EXPLANATION",
                "preview": "bad card row preview",
            }
            with (year_dir / "questions.jsonl").open("a", encoding="utf-8") as file:
                file.write(json.dumps(bad_row, ensure_ascii=False) + "\n")
            library = SystemQuestionLibrary(raw_root=raw_root)

            detail = library.get_question("bad_card")

            self.assertEqual(detail["question_markdown"], "bad card row preview")
            self.assertEqual(detail["answer"], "ROW-BAD-ANSWER")
            self.assertEqual(detail["explanation"], "ROW-BAD-EXPLANATION")

    def test_list_skips_malformed_rows_bad_numbers_and_missing_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            year_dir = raw_root / "math" / "exam_papers" / "math1" / "2099"
            rows = [
                json.loads(line)
                for line in (year_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            rows[0]["assets"] = ["images/q001.png", "images/missing.png", "../questions.jsonl"]
            bad_numeric_row = {
                "question_id": "kaoyan_math1_2099_q999",
                "exam_id": "kaoyan_math1_2099",
                "exam_type": "math1",
                "year": "not-a-year",
                "question_number": "not-a-number",
                "question_type": "single_choice",
                "module": "bad row",
                "topics": ["bad"],
                "difficulty": "unknown",
                "card_path": "questions/missing.md",
                "assets": ["images/missing.png"],
                "answer": "bad",
                "explanation": "bad",
                "preview": "bad row preview",
            }
            (year_dir / "questions.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(rows[0], ensure_ascii=False),
                        "{malformed json",
                        json.dumps(bad_numeric_row, ensure_ascii=False),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            library = SystemQuestionLibrary(raw_root=raw_root)

            result = library.list_questions(subject="math", exam_type="math1", query="连续")

            self.assertEqual(result["total"], 1)
            self.assertEqual(result["items"][0]["question_id"], "kaoyan_math1_2099_q001")
            self.assertEqual(
                result["items"][0]["asset_urls"],
                ["/api/materials/system/assets/math1/2099/images/q001.png"],
            )

    def test_asset_path_rejects_invalid_resource_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            library = SystemQuestionLibrary(raw_root=raw_root)

            safe_path = library.asset_path("math1", 2099, "images/q001.png")
            self.assertEqual(safe_path.name, "q001.png")

            for bad_path in (
                "../questions.jsonl",
                r"C:\Windows\win.ini",
                "C:/Windows/win.ini",
                "/Windows/win.ini",
                "",
                ".",
                "images/../images/q001.png",
                r"images\..\images\q001.png",
                r"images\..\questions.jsonl",
                "questions.jsonl",
            ):
                with self.subTest(asset_path=bad_path):
                    with self.assertRaises(ValueError):
                        library.asset_path("math1", 2099, bad_path)

    def test_asset_path_requires_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            images_dir = raw_root / "math" / "exam_papers" / "math1" / "2099" / "images"
            (images_dir / "nested").mkdir()
            library = SystemQuestionLibrary(raw_root=raw_root)

            with self.assertRaises(FileNotFoundError):
                library.asset_path("math1", 2099, "images/missing.png")

            with self.assertRaises(FileNotFoundError):
                library.asset_path("math1", 2099, "images/nested")

    def test_api_lists_system_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                response = client.get(
                    "/api/materials/system/questions",
                    params={"subject": "math", "exam_type": "math1", "query": "连续"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["items"][0]["question_id"], "kaoyan_math1_2099_q001")

    def test_api_returns_question_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                response = client.get("/api/materials/system/questions/kaoyan_math1_2099_q001")

            self.assertEqual(response.status_code, 200)
            question_markdown = response.json()["question_markdown"]
            self.assertIn("`f(x)`", question_markdown)
            self.assertIn(
                "![题图](/api/materials/system/assets/math1/2099/images/q001.png)",
                question_markdown,
            )

    def test_api_persists_and_merges_user_question_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw")
            users_root = base / "users"
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                patch_response = client.patch(
                    "/api/materials/system/questions/kaoyan_math1_2099_q001/state",
                    params={"user_id": "tester"},
                    json={
                        "mastery_status": "learning",
                        "is_favorite": True,
                        "in_wrong_book": True,
                        "personal_note": "review limit definition",
                    },
                )
                list_response = client.get(
                    "/api/materials/system/questions",
                    params={"subject": "math", "exam_type": "math1", "user_id": "tester"},
                )
                detail_response = client.get(
                    "/api/materials/system/questions/kaoyan_math1_2099_q001",
                    params={"user_id": "tester"},
                )

            self.assertEqual(patch_response.status_code, 200)
            patched_state = patch_response.json()["personal_state"]
            self.assertEqual(patched_state["mastery_status"], "learning")
            self.assertTrue(patched_state["is_favorite"])
            self.assertTrue(patched_state["in_wrong_book"])
            self.assertEqual(patched_state["personal_note"], "review limit definition")

            self.assertEqual(list_response.status_code, 200)
            list_state = list_response.json()["items"][0]["personal_state"]
            self.assertEqual(list_state["mastery_status"], "learning")
            self.assertTrue(list_state["is_favorite"])

            self.assertEqual(detail_response.status_code, 200)
            detail_state = detail_response.json()["personal_state"]
            self.assertTrue(detail_state["in_wrong_book"])
            self.assertEqual(detail_state["personal_note"], "review limit definition")

    def test_api_filters_system_questions_by_user_status_before_pagination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_second_question=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                client.patch(
                    "/api/materials/system/questions/kaoyan_math1_2099_q002/state",
                    params={"user_id": "tester"},
                    json={"mastery_status": "learning", "is_favorite": True},
                )
                favorite_response = client.get(
                    "/api/materials/system/questions",
                    params={
                        "subject": "math",
                        "exam_type": "math1",
                        "user_id": "tester",
                        "user_status": "favorite",
                    },
                )
                default_response = client.get(
                    "/api/materials/system/questions",
                    params={
                        "subject": "math",
                        "exam_type": "math1",
                        "user_id": "tester",
                        "user_status": "not_started",
                    },
                )

            self.assertEqual(favorite_response.status_code, 200)
            favorite_payload = favorite_response.json()
            self.assertEqual(favorite_payload["total"], 1)
            self.assertEqual(favorite_payload["items"][0]["question_id"], "kaoyan_math1_2099_q002")
            self.assertTrue(favorite_payload["items"][0]["personal_state"]["is_favorite"])

            self.assertEqual(default_response.status_code, 200)
            default_payload = default_response.json()
            self.assertEqual(default_payload["total"], 1)
            self.assertEqual(default_payload["items"][0]["question_id"], "kaoyan_math1_2099_q001")
            self.assertFalse(default_payload["items"][0]["personal_state"]["is_favorite"])

    def test_api_summarizes_system_question_user_states_for_current_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            raw_root = self._make_raw_root(base / "raw", include_second_question=True)
            users_root = base / "users"
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with (
                patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                client.patch(
                    "/api/materials/system/questions/kaoyan_math1_2099_q002/state",
                    params={"user_id": "tester"},
                    json={
                        "mastery_status": "learning",
                        "is_favorite": True,
                        "in_wrong_book": True,
                        "personal_note": "revisit derivative definition",
                    },
                )
                response = client.get(
                    "/api/materials/system/questions/state-summary",
                    params={"subject": "math", "exam_type": "math1", "user_id": "tester"},
                )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["user_id"], "tester")
            self.assertEqual(
                payload["state_summary"],
                {
                    "all": 2,
                    "not_started": 1,
                    "learning": 1,
                    "mastered": 0,
                    "favorite": 1,
                    "wrong_book": 1,
                    "noted": 1,
                },
            )

    def test_api_state_summary_uses_single_collection_scan(self) -> None:
        class CountingLibrary:
            def __init__(self) -> None:
                self.list_all_calls = 0
                self.list_questions_calls = 0

            def list_all_questions(self, **kwargs) -> tuple[dict, list[dict]]:
                self.list_all_calls += 1
                return (
                    {
                        "ok": True,
                        "subject": kwargs["subject"],
                        "exam_type": kwargs["exam_type"],
                        "total": 2,
                        "page": 1,
                        "page_size": 2,
                        "total_pages": 1,
                        "topic_options": ["limit"],
                        "items": [],
                    },
                    [
                        {"question_id": "kaoyan_math1_2099_q001"},
                        {"question_id": "kaoyan_math1_2099_q002"},
                    ],
                )

            def list_questions(self, **kwargs) -> dict:
                self.list_questions_calls += 1
                raise AssertionError("state summary must not collect items through paginated list_questions")

        with tempfile.TemporaryDirectory() as tmp:
            fake_library = CountingLibrary()
            users_root = Path(tmp) / "users"
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with (
                patch("materials.api.SystemQuestionLibrary", return_value=fake_library),
                patch("materials.user_state.DEFAULT_USERS_DIR", users_root),
            ):
                response = client.get(
                    "/api/materials/system/questions/state-summary",
                    params={"subject": "math", "exam_type": "math1", "user_id": "tester"},
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(fake_library.list_all_calls, 1)
            self.assertEqual(fake_library.list_questions_calls, 0)
            self.assertEqual(response.json()["state_summary"]["all"], 2)

    def test_api_rejects_invalid_system_question_user_id_as_400(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app, raise_server_exceptions=False)

            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                list_response = client.get(
                    "/api/materials/system/questions",
                    params={"subject": "math", "exam_type": "math1", "user_id": "../evil"},
                )
                detail_response = client.get(
                    "/api/materials/system/questions/kaoyan_math1_2099_q001",
                    headers={"X-User-Id": "../evil"},
                )
                patch_response = client.patch(
                    "/api/materials/system/questions/kaoyan_math1_2099_q001/state",
                    params={"user_id": "../evil"},
                    json={"mastery_status": "learning"},
                )

            self.assertEqual(list_response.status_code, 400)
            self.assertEqual(detail_response.status_code, 400)
            self.assertEqual(patch_response.status_code, 400)

    def test_api_returns_404_for_missing_question_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                response = client.get("/api/materials/system/questions/missing_id")

            self.assertEqual(response.status_code, 404)

    def test_api_returns_system_asset_and_rejects_non_asset_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = self._make_raw_root(Path(tmp))
            secret_path = raw_root / "math" / "exam_papers" / "math1" / "2099" / "images" / "secret.txt"
            secret_path.write_text("secret", encoding="utf-8")
            app = FastAPI()
            app.include_router(materials_router)
            client = TestClient(app)

            with patch("materials.system_library.DEFAULT_RAW_ROOT", raw_root):
                asset_response = client.get("/api/materials/system/assets/math1/2099/images/q001.png")
                blocked_response = client.get("/api/materials/system/assets/math1/2099/questions.jsonl")
                secret_response = client.get("/api/materials/system/assets/math1/2099/images/secret.txt")
                missing_image_response = client.get("/api/materials/system/assets/math1/2099/images/missing.png")

            self.assertEqual(asset_response.status_code, 200)
            self.assertEqual(asset_response.content, b"image")
            self.assertEqual(blocked_response.status_code, 400)
            self.assertEqual(secret_response.status_code, 400)
            self.assertEqual(missing_image_response.status_code, 404)

    def _make_raw_root(self, tmp: Path, *, include_second_question: bool = False) -> Path:
        year_dir = tmp / "math" / "exam_papers" / "math1" / "2099"
        questions_dir = year_dir / "questions"
        images_dir = year_dir / "images"
        questions_dir.mkdir(parents=True)
        images_dir.mkdir()
        (images_dir / "q001.png").write_bytes(b"image")

        row = {
            "question_id": "kaoyan_math1_2099_q001",
            "exam_id": "kaoyan_math1_2099",
            "exam_type": "math1",
            "year": 2099,
            "question_number": 1,
            "question_type": "single_choice",
            "module": "高等数学",
            "topics": ["连续"],
            "difficulty": "unknown",
            "card_path": "questions/q001.md",
            "assets": ["images/q001.png"],
            "answer": "ROW-A",
            "explanation": "ROW-EXPLANATION",
        }
        row2 = {
            **row,
            "question_id": "kaoyan_math1_2099_q002",
            "question_number": 2,
            "topics": ["导数"],
            "card_path": "questions/q002.md",
            "assets": [],
        }
        rows = [row, row2] if include_second_question else [row]
        (year_dir / "questions.jsonl").write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in rows),
            encoding="utf-8",
        )
        (questions_dir / "q001.md").write_text(
            "\r\n".join(
                [
                    "---",
                    "question_id: kaoyan_math1_2099_q001",
                    "year: 2099",
                    "---",
                    "",
                    "## 题目",
                    "",
                    "设函数 `f(x)` 连续，则（ ）。",
                    "",
                    "![题图](../images/q001.png)",
                    "",
                    "## 标准答案",
                    "",
                    "B",
                    "",
                    "## 解析",
                    "",
                    "由定义可得。",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        if include_second_question:
            (questions_dir / "q002.md").write_text(
                "\r\n".join(
                    [
                        "---",
                        "question_id: kaoyan_math1_2099_q002",
                        "year: 2099",
                        "---",
                        "",
                        "## 题目",
                        "",
                        "设函数 `g(x)` 可导，则（ ）。",
                        "",
                        "## 标准答案",
                        "",
                        "A",
                        "",
                        "## 解析",
                        "",
                        "由导数定义可得。",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        return tmp

    def _add_exam_question(
        self,
        raw_root: Path,
        *,
        exam_type: str,
        year: int,
        question_number: int,
        topic: str,
    ) -> None:
        year_dir = raw_root / "math" / "exam_papers" / exam_type / str(year)
        questions_dir = year_dir / "questions"
        questions_dir.mkdir(parents=True)
        question_id = f"kaoyan_{exam_type}_{year}_q{question_number:03d}"
        row = {
            "question_id": question_id,
            "exam_id": f"kaoyan_{exam_type}_{year}",
            "exam_type": exam_type,
            "year": year,
            "question_number": question_number,
            "question_type": "single_choice",
            "module": "高等数学",
            "topics": [topic],
            "difficulty": "unknown",
            "card_path": f"questions/q{question_number:03d}.md",
            "assets": [],
            "answer": "A",
            "explanation": "解析。",
        }
        (year_dir / "questions.jsonl").write_text(
            json.dumps(row, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (questions_dir / f"q{question_number:03d}.md").write_text(
            "\n".join(
                [
                    "---",
                    f"question_id: {question_id}",
                    f"year: {year}",
                    "---",
                    "",
                    "## 题目",
                    "",
                    f"{exam_type} 测试题。",
                    "",
                    "## 标准答案",
                    "",
                    "A",
                    "",
                    "## 解析",
                    "",
                    "解析。",
                    "",
                ]
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
