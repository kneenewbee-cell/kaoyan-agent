from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_ROOT = ROOT / "data" / "raw"

SUPPORTED_MATH_EXAM_TYPES = ("math1", "math2", "math3")
EXAM_TYPE_LABELS = {
    "math1": "数一",
    "math2": "数二",
    "math3": "数三",
}
LIBRARY_NAMES = {
    "math1": "数一历年真题",
    "math2": "数二历年真题",
    "math3": "数三历年真题",
}
QUESTION_TYPE_LABELS = {
    "single_choice": "选择题",
    "fill_blank": "填空题",
    "solution": "解答题",
}


class SystemQuestionLibrary:
    def __init__(self, raw_root: Path | None = None) -> None:
        self.raw_root = Path(raw_root) if raw_root is not None else DEFAULT_RAW_ROOT

    def list_questions(
        self,
        subject: str = "math",
        exam_type: str = "math1",
        library_name: str | None = None,
        year: int | None = None,
        question_type: str | None = None,
        topic: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        page = max(1, int(page))
        page_size = min(50, max(1, int(page_size)))
        rows, topic_options = self._matching_question_items(
            subject=subject,
            exam_type=exam_type,
            library_name=library_name,
            year=year,
            question_type=question_type,
            topic=topic,
            query=query,
        )
        total = len(rows)
        start = (page - 1) * page_size
        return self._list_response(
            subject=subject,
            exam_type=exam_type,
            total=total,
            page=page,
            page_size=page_size,
            topic_options=topic_options,
            items=rows[start : start + page_size],
        )

    def list_all_questions(
        self,
        subject: str = "math",
        exam_type: str = "math1",
        library_name: str | None = None,
        year: int | None = None,
        question_type: str | None = None,
        topic: str | None = None,
        query: str | None = None,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        rows, topic_options = self._matching_question_items(
            subject=subject,
            exam_type=exam_type,
            library_name=library_name,
            year=year,
            question_type=question_type,
            topic=topic,
            query=query,
        )
        total = len(rows)
        response = self._list_response(
            subject=subject,
            exam_type=exam_type,
            total=total,
            page=1,
            page_size=max(1, total),
            topic_options=topic_options,
            items=rows,
        )
        return response, rows

    def _matching_question_items(
        self,
        *,
        subject: str,
        exam_type: str,
        library_name: str | None,
        year: int | None,
        question_type: str | None,
        topic: str | None,
        query: str | None,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        if subject != "math":
            return [], []

        rows = []
        topic_options: set[str] = set()
        for resolved_exam_type in self._math_exam_types(exam_type):
            for row, year_dir in self._iter_question_rows(subject, resolved_exam_type):
                try:
                    item = self._question_item(row, year_dir)
                except (OSError, UnicodeDecodeError, ValueError, TypeError):
                    continue
                if not self._matches_filters(
                    item,
                    library_name=library_name,
                    year=year,
                    question_type=question_type,
                    topic=None,
                    query=query,
                ):
                    continue
                topic_options.update(str(value) for value in item.get("topics") or [] if str(value).strip())
                if topic is not None and not self._matches_topic(item, topic):
                    continue
                rows.append(item)

        rows.sort(key=lambda item: (-(item.get("year") or 0), item.get("question_number") or 0))
        return rows, sorted(topic_options)

    def get_question(self, question_id: str) -> dict[str, Any]:
        for exam_type in SUPPORTED_MATH_EXAM_TYPES:
            for row, year_dir in self._iter_question_rows("math", exam_type):
                if row.get("question_id") != question_id:
                    continue
                try:
                    item = self._question_item(row, year_dir)
                except (OSError, UnicodeDecodeError, ValueError, TypeError):
                    item = self._fallback_question_item(row, year_dir)
                sections = self._safe_read_row_card_sections(row, year_dir)
                row_exam_type = str(row.get("exam_type") or exam_type)
                year = self._safe_int(row.get("year"), 0)
                question_markdown = self._detail_markdown(
                    sections.get("题目") or self._row_question_fallback(row),
                    row_exam_type,
                    year,
                )
                answer = self._detail_markdown(sections.get("标准答案") or row.get("answer") or "", row_exam_type, year)
                explanation = self._detail_markdown(sections.get("解析") or row.get("explanation") or "", row_exam_type, year)
                return {
                    **item,
                    "answer": answer,
                    "explanation": explanation,
                    "question_markdown": question_markdown,
                    "answer_markdown": answer,
                    "explanation_markdown": explanation,
                }
        raise KeyError(f"system question not found: {question_id}")

    def asset_path(self, exam_type: str, year: int, asset_path: str) -> Path:
        if exam_type not in SUPPORTED_MATH_EXAM_TYPES:
            raise ValueError(f"unsupported exam_type: {exam_type}")
        normalized_asset = self._normalize_asset_path(asset_path)
        year_dir = self.raw_root / "math" / "exam_papers" / exam_type / str(year)
        images_dir = (year_dir / "images").resolve()
        resolved = self._safe_year_path(year_dir, normalized_asset)
        if resolved != images_dir and images_dir not in resolved.parents:
            raise ValueError(f"asset path escapes images directory: {asset_path}")
        if not resolved.exists() or not resolved.is_file():
            raise FileNotFoundError(resolved)
        return resolved

    def _iter_question_rows(self, subject: str, exam_type: str) -> list[tuple[dict[str, Any], Path]]:
        base_dir = self.raw_root / subject / "exam_papers" / exam_type
        if not base_dir.exists():
            return []

        rows: list[tuple[dict[str, Any], Path]] = []
        for jsonl_path in sorted(base_dir.glob("*/questions.jsonl")):
            year_dir = jsonl_path.parent
            with jsonl_path.open("r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(row, dict):
                        normalized_row = dict(row)
                        normalized_row.setdefault("exam_type", exam_type)
                        rows.append((normalized_row, year_dir))
        return rows

    def _math_exam_types(self, exam_type: str) -> tuple[str, ...]:
        normalized = str(exam_type or "").strip()
        if normalized in ("", "all"):
            return SUPPORTED_MATH_EXAM_TYPES
        if normalized in SUPPORTED_MATH_EXAM_TYPES:
            return (normalized,)
        return ()

    def _fallback_question_item(self, row: dict[str, Any], year_dir: Path) -> dict[str, Any]:
        exam_type = str(row.get("exam_type") or "math1")
        year = self._safe_int(row.get("year") or year_dir.name)
        question_type = str(row.get("question_type") or "")
        return {
            "question_id": row.get("question_id", ""),
            "exam_id": row.get("exam_id", ""),
            "subject": "math",
            "exam_type": exam_type,
            "exam_type_label": EXAM_TYPE_LABELS.get(exam_type, exam_type),
            "library_name": LIBRARY_NAMES.get(exam_type, exam_type),
            "year": year,
            "question_number": self._safe_int(row.get("question_number")),
            "question_type": question_type,
            "question_type_label": QUESTION_TYPE_LABELS.get(question_type, question_type),
            "module": row.get("module", ""),
            "topics": list(row.get("topics") or []),
            "difficulty": row.get("difficulty", "unknown"),
            "preview": self._preview(self._row_question_fallback(row)),
            "asset_urls": self._asset_urls(exam_type, year, [str(asset) for asset in row.get("assets") or []]),
        }

    def _question_item(self, row: dict[str, Any], year_dir: Path) -> dict[str, Any]:
        exam_type = str(row.get("exam_type") or "math1")
        year = self._safe_int(row.get("year") or year_dir.name)
        question_type = str(row.get("question_type") or "")
        card_path = self._safe_year_path(year_dir, row.get("card_path", ""))
        sections = self._read_card_sections(card_path)
        question_markdown = sections.get("题目") or self._row_question_fallback(row)
        assets = [str(asset) for asset in row.get("assets") or []]

        return {
            "question_id": row.get("question_id", ""),
            "exam_id": row.get("exam_id", ""),
            "subject": "math",
            "exam_type": exam_type,
            "exam_type_label": EXAM_TYPE_LABELS.get(exam_type, exam_type),
            "library_name": LIBRARY_NAMES.get(exam_type, exam_type),
            "year": year,
            "question_number": self._safe_int(row.get("question_number")),
            "question_type": question_type,
            "question_type_label": QUESTION_TYPE_LABELS.get(question_type, question_type),
            "module": row.get("module", ""),
            "topics": list(row.get("topics") or []),
            "difficulty": row.get("difficulty", "unknown"),
            "preview": self._preview(question_markdown),
            "asset_urls": self._asset_urls(exam_type, year, assets),
        }

    def _matches_filters(
        self,
        item: dict[str, Any],
        *,
        library_name: str | None,
        year: int | None,
        question_type: str | None,
        topic: str | None,
        query: str | None,
    ) -> bool:
        if library_name is not None and item.get("library_name") != library_name:
            return False
        if year is not None and item.get("year") != year:
            return False
        if question_type is not None and item.get("question_type") != question_type:
            return False
        topics = [str(value) for value in item.get("topics") or []]
        if topic is not None and not self._matches_topic(item, topic):
            return False
        if query:
            haystack = " ".join(
                [
                    str(item.get("preview", "")),
                    str(item.get("library_name", "")),
                    str(item.get("question_type_label", "")),
                    " ".join(topics),
                    str(item.get("year", "")),
                ]
            ).casefold()
            if query.casefold() not in haystack:
                return False
        return True

    def _matches_topic(self, item: dict[str, Any], topic: str) -> bool:
        topics = [str(value) for value in item.get("topics") or []]
        return any(topic in topic_value for topic_value in topics)

    def _read_card_sections(self, card_path: Path) -> dict[str, str]:
        if not card_path.exists():
            return {}
        try:
            text = card_path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        except (OSError, UnicodeDecodeError):
            return {}
        lines = text.split("\n")
        if lines and lines[0].strip() == "---":
            for index in range(1, len(lines)):
                if lines[index].strip() == "---":
                    lines = lines[index + 1 :]
                    break

        sections: dict[str, list[str]] = {}
        current_title: str | None = None
        for line in lines:
            match = re.match(r"^##\s+(.+?)\s*$", line)
            if match:
                current_title = match.group(1).strip()
                sections.setdefault(current_title, [])
                continue
            if current_title is not None:
                sections[current_title].append(line)

        return {title: "\n".join(content).strip() for title, content in sections.items()}

    def _safe_read_row_card_sections(self, row: dict[str, Any], year_dir: Path) -> dict[str, str]:
        try:
            card_path = self._safe_year_path(year_dir, row.get("card_path", ""))
        except (ValueError, TypeError):
            return {}
        return self._read_card_sections(card_path)

    def _list_response(
        self,
        *,
        subject: str,
        exam_type: str,
        total: int,
        page: int,
        page_size: int,
        topic_options: list[str],
        items: list[dict[str, Any]],
    ) -> dict[str, Any]:
        total_pages = max(1, (total + page_size - 1) // page_size)
        return {
            "ok": True,
            "subject": subject,
            "exam_type": exam_type,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "topic_options": topic_options,
            "items": items,
        }

    def _row_question_fallback(self, row: dict[str, Any]) -> str:
        for key in ("question_markdown", "question", "summary", "preview"):
            value = row.get(key)
            if value:
                return str(value)
        return ""

    def _question_body(self, markdown: str) -> str:
        parts = []
        for line in markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("!["):
                continue
            parts.append(stripped)
        return "\n".join(parts).strip()

    def _detail_markdown(self, markdown: str, exam_type: str, year: int) -> str:
        parts = []
        for line in str(markdown or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            stripped = line.strip()
            if stripped:
                parts.append(stripped)
        return self._rewrite_markdown_image_urls("\n".join(parts), exam_type, year)

    def _rewrite_markdown_image_urls(self, markdown: str, exam_type: str, year: int) -> str:
        def replace(match: re.Match[str]) -> str:
            alt = match.group("alt")
            target = match.group("target").strip()
            url, suffix = self._split_markdown_image_target(target)
            if url.startswith("/api/materials/system/assets/"):
                return match.group(0)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
                return match.group(0)
            asset_path = self._markdown_asset_path(url)
            try:
                rewritten = self._asset_url(exam_type, year, asset_path)
            except (FileNotFoundError, OSError, ValueError):
                label = alt.strip() or "image"
                return f"[missing image: {label}]"
            return f"![{alt}]({rewritten}{suffix})"

        return re.sub(r"!\[(?P<alt>[^\]\n]*)\]\((?P<target>[^)\n]+)\)", replace, markdown)

    def _split_markdown_image_target(self, target: str) -> tuple[str, str]:
        if target.startswith("<"):
            closing = target.find(">")
            if closing != -1:
                suffix = target[closing + 1 :].strip()
                return target[1:closing], f" {suffix}" if suffix else ""
        parts = target.split(maxsplit=1)
        if len(parts) == 2:
            return parts[0], f" {parts[1]}"
        return target, ""

    def _markdown_asset_path(self, url: str) -> str:
        normalized = url.strip().strip("<>").replace("\\", "/")
        while normalized.startswith("../"):
            normalized = normalized[3:]
        if normalized.startswith("./"):
            normalized = normalized[2:]
        return normalized

    def _preview(self, markdown: str) -> str:
        parts = []
        for line in markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("!["):
                continue
            parts.append(stripped)
        preview = " ".join(parts)
        if len(preview) > 180:
            return preview[:180].rstrip()
        return preview

    def _safe_year_path(self, year_dir: Path, relative_path: str) -> Path:
        base = year_dir.resolve()
        resolved = (year_dir / relative_path).resolve()
        if resolved != base and base not in resolved.parents:
            raise ValueError(f"path escapes system library year directory: {relative_path}")
        return resolved

    def _safe_int(self, value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _normalize_asset_path(self, asset_path: str) -> str:
        normalized = str(asset_path).strip().replace("\\", "/")
        if normalized in ("", "."):
            raise ValueError("asset path is empty")
        if ".." in normalized.split("/"):
            raise ValueError(f"asset path must not contain parent segments: {asset_path}")
        if normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized):
            raise ValueError(f"absolute asset path is not allowed: {asset_path}")
        if not normalized.startswith("images/"):
            raise ValueError(f"asset path must start with images/: {asset_path}")
        return normalized

    def _asset_urls(self, exam_type: str, year: int, assets: list[str]) -> list[str]:
        urls = []
        for asset in assets:
            try:
                urls.append(self._asset_url(exam_type, year, asset))
            except (FileNotFoundError, OSError, ValueError):
                continue
        return urls

    def _asset_url(self, exam_type: str, year: int, asset: str) -> str:
        normalized_asset = self._normalize_asset_path(asset)
        self.asset_path(exam_type, year, asset)
        return f"/api/materials/system/assets/{exam_type}/{year}/{normalized_asset}"
