from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from ..chunking.token_counter import estimate_tokens
from ..schemas import Chunk


HTML_TABLE_RE = re.compile(r"<table\b.*?</table>", re.IGNORECASE | re.DOTALL)


@dataclass
class _Cell:
    text: str
    rowspan: int = 1
    colspan: int = 1


class _HTMLTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[_Cell]] = []
        self._current_row: list[_Cell] | None = None
        self._cell_parts: list[str] | None = None
        self._rowspan = 1
        self._colspan = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value for key, value in attrs}
        if tag.lower() == "tr":
            self._current_row = []
        elif tag.lower() in {"td", "th"}:
            self._cell_parts = []
            self._rowspan = _safe_int(attrs_dict.get("rowspan"), default=1)
            self._colspan = _safe_int(attrs_dict.get("colspan"), default=1)
        elif tag.lower() == "br" and self._cell_parts is not None:
            self._cell_parts.append(" ")

    def handle_data(self, data: str) -> None:
        if self._cell_parts is not None:
            self._cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._current_row is not None and self._cell_parts is not None:
            text = _normalize_cell_text("".join(self._cell_parts))
            self._current_row.append(_Cell(text=text, rowspan=self._rowspan, colspan=self._colspan))
            self._cell_parts = None
            self._rowspan = 1
            self._colspan = 1
        elif tag == "tr" and self._current_row is not None:
            self.rows.append(self._current_row)
            self._current_row = None


def _safe_int(value: str | None, *, default: int) -> int:
    try:
        parsed = int(value or default)
    except (TypeError, ValueError):
        return default
    return max(parsed, 1)


def _normalize_cell_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _set_grid_cell(row: list[str], index: int, value: str) -> None:
    while len(row) <= index:
        row.append("")
    row[index] = value


def _expand_table(rows: list[list[_Cell]]) -> list[list[str]]:
    grid: list[list[str]] = []
    carry: dict[tuple[int, int], str] = {}
    max_cols = 0

    for row_index, cells in enumerate(rows):
        row: list[str] = []
        col_index = 0

        def fill_carried() -> None:
            nonlocal col_index
            while (row_index, col_index) in carry:
                _set_grid_cell(row, col_index, carry.pop((row_index, col_index)))
                col_index += 1

        fill_carried()
        for cell in cells:
            fill_carried()
            for offset in range(cell.colspan):
                _set_grid_cell(row, col_index + offset, cell.text)
            for row_offset in range(1, cell.rowspan):
                for col_offset in range(cell.colspan):
                    carry[(row_index + row_offset, col_index + col_offset)] = cell.text
            col_index += cell.colspan
        fill_carried()
        max_cols = max(max_cols, len(row))
        grid.append(row)

    for row in grid:
        while len(row) < max_cols:
            row.append("")
    return grid


def _dedupe_headers(headers: list[str]) -> list[str]:
    result: list[str] = []
    seen: dict[str, int] = {}
    for index, header in enumerate(headers, start=1):
        base = header.strip() or f"column_{index}"
        count = seen.get(base, 0) + 1
        seen[base] = count
        result.append(base if count == 1 else f"{base}_{count}")
    return result


def _infer_headers_and_rows(grid: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    grid = [row for row in grid if any(cell.strip() for cell in row)]
    if not grid:
        return [], []
    if len(grid) >= 2 and grid[0] and grid[1] and grid[0][0] and grid[0][0] == grid[1][0]:
        headers = [grid[0][0]] + [cell or grid[0][index] for index, cell in enumerate(grid[1][1:], start=1)]
        return _dedupe_headers(headers), grid[2:]
    return _dedupe_headers(grid[0]), grid[1:]


def parse_html_table(raw_html: str) -> dict[str, Any]:
    parser = _HTMLTableParser()
    parser.feed(raw_html)
    grid = _expand_table(parser.rows)
    columns, body_rows = _infer_headers_and_rows(grid)
    row_dicts: list[dict[str, str]] = []
    for row in body_rows:
        padded = list(row[: len(columns)])
        while len(padded) < len(columns):
            padded.append("")
        row_dicts.append({column: padded[index] for index, column in enumerate(columns)})
    return {
        "columns": columns,
        "rows": row_dicts,
        "grid": grid,
        "row_count": len(row_dicts),
        "column_count": len(columns),
    }


def _extract_text_from_block(block: dict[str, Any]) -> str:
    parts: list[str] = []
    for line in block.get("lines", []) or []:
        for span in line.get("spans", []) or []:
            content = span.get("content")
            if isinstance(content, str):
                parts.append(content)
    return _normalize_cell_text(" ".join(parts))


def _extract_table_html(block: dict[str, Any]) -> str:
    for child in block.get("blocks", []) or []:
        for line in child.get("lines", []) or []:
            for span in line.get("spans", []) or []:
                if span.get("type") == "table" and isinstance(span.get("html"), str):
                    return span["html"]
    return ""


def _guess_table_kind(columns: list[str]) -> str:
    joined = " ".join(columns)
    if "考试内容" in joined and ("数一" in joined or "数二" in joined or "数三" in joined):
        return "exam_requirement_table"
    if len(columns) >= 2:
        return "data_table"
    return "unknown_table"


def _guess_table_title(table_id: str, columns: list[str], kind: str) -> str:
    if kind == "exam_requirement_table":
        return "考试内容与考试要求"
    if columns:
        return " / ".join(columns[:3])
    return f"表格 {table_id}"


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _html_table_visible_text(raw_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw_html)
    return _normalize_cell_text(html.unescape(text))


def render_table_markdown(table: dict[str, Any]) -> str:
    columns = list(table.get("columns", []))
    rows = list(table.get("rows", []))
    title = str(table.get("title") or table.get("table_id") or "table")
    table_id = str(table.get("table_id") or "table")
    page = table.get("page")
    lines = [
        f"<!-- table: {table_id} page={page} source=layout.json -->",
        f"**表格：{title}**",
        "",
    ]
    if not columns:
        raw_html = str(table.get("raw_html") or "")
        if _html_table_visible_text(raw_html):
            lines.append(raw_html)
        else:
            lines.append("（空表，已忽略）")
        return "\n".join(lines).strip()
    lines.append("| " + " | ".join(_escape_markdown_cell(column) for column in columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        lines.append("| " + " | ".join(_escape_markdown_cell(str(row.get(column, ""))) for column in columns) + " |")
    return "\n".join(lines).strip()


def build_layout_context(layout_path: Path) -> dict[str, Any]:
    data = json.loads(layout_path.read_text(encoding="utf-8"))
    pdf_info = data.get("pdf_info", []) or []
    block_counts: dict[str, int] = {}
    title_samples: list[dict[str, Any]] = []
    page_sequence_samples: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []

    for page_index, page in enumerate(pdf_info, start=1):
        blocks = page.get("preproc_blocks", []) or []
        page_blocks: list[dict[str, Any]] = []
        for block in blocks:
            block_type = str(block.get("type") or "unknown")
            block_counts[block_type] = block_counts.get(block_type, 0) + 1
            if block_type == "title":
                text = _extract_text_from_block(block)
                if text:
                    sample = {
                        "page": page_index,
                        "text": text[:120],
                        "level": block.get("level"),
                        "bbox": block.get("bbox"),
                        "score": block.get("score"),
                    }
                    if len(title_samples) < 90:
                        title_samples.append(sample)
                    page_blocks.append({"type": "title", "text": text[:80], "level": block.get("level")})
            elif block_type == "table":
                raw_html = _extract_table_html(block)
                parsed = parse_html_table(raw_html) if raw_html else {
                    "columns": [],
                    "rows": [],
                    "grid": [],
                    "row_count": 0,
                    "column_count": 0,
                }
                table_id = f"table_{len(tables) + 1:03d}"
                kind = _guess_table_kind(parsed["columns"])
                table = {
                    "table_id": table_id,
                    "page": page_index,
                    "bbox": block.get("bbox"),
                    "kind_guess": kind,
                    "title": _guess_table_title(table_id, parsed["columns"], kind),
                    "columns": parsed["columns"],
                    "rows": parsed["rows"],
                    "row_count": parsed["row_count"],
                    "column_count": parsed["column_count"],
                    "raw_html": raw_html,
                }
                table["markdown"] = render_table_markdown(table)
                tables.append(table)
                page_blocks.append(
                    {
                        "type": "table",
                        "table_id": table_id,
                        "rows": parsed["row_count"],
                        "columns": parsed["columns"][:8],
                        "kind_guess": kind,
                    }
                )
            elif block_type in {"image", "interline_equation"}:
                page_blocks.append({"type": block_type, "bbox": block.get("bbox")})
        if page_index <= 3 or page_blocks and any(item["type"] == "table" for item in page_blocks):
            page_sequence_samples.append({"page": page_index, "blocks": page_blocks[:30]})

    table_samples = []
    for table in tables[:12]:
        table_samples.append(
            {
                "table_id": table["table_id"],
                "page": table["page"],
                "bbox": table["bbox"],
                "rows": table["row_count"],
                "columns": table["columns"][:6],
                "first_rows": [
                    [row.get(column, "")[:100] for column in table["columns"][:6]]
                    for row in table["rows"][:2]
                ],
                "kind_guess": table["kind_guess"],
            }
        )

    summary = {
        "source": "mineru_layout",
        "layout_path_name": layout_path.name,
        "page_count": len(pdf_info),
        "block_counts": block_counts,
        "title_samples": title_samples,
        "table_samples": table_samples,
        "page_sequence_samples": page_sequence_samples[:10],
    }
    return {"summary": summary, "tables": tables}


def replace_html_tables_with_layout_markdown(
    markdown: str,
    tables: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    warnings: list[str] = []
    table_index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal table_index
        raw_html = match.group(0)
        if table_index >= len(tables):
            warnings.append("layout_table_replacement_missing_table")
            parsed = parse_html_table(raw_html)
            table_id = f"html_table_{table_index + 1:03d}"
            kind = _guess_table_kind(parsed["columns"])
            fallback_table = {
                "table_id": table_id,
                "page": None,
                "kind_guess": kind,
                "title": _guess_table_title(table_id, parsed["columns"], kind),
                "columns": parsed["columns"],
                "rows": parsed["rows"],
                "row_count": parsed["row_count"],
                "column_count": parsed["column_count"],
                "raw_html": raw_html,
            }
            table_index += 1
            return "\n\n" + render_table_markdown(fallback_table) + "\n\n"
        rendered = str(tables[table_index].get("markdown") or match.group(0))
        table_index += 1
        return "\n\n" + rendered + "\n\n"

    replaced = HTML_TABLE_RE.sub(replace, markdown)
    if table_index < len(tables):
        warnings.append("layout_table_replacement_extra_tables")
    return replaced, warnings


def save_layout_artifacts(
    parsed_dir: Path,
    layout_context: dict[str, Any],
) -> dict[str, Any]:
    parsed_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = parsed_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    summary_path = parsed_dir / "layout_summary.json"
    summary_path.write_text(
        json.dumps(layout_context["summary"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    table_records: list[dict[str, Any]] = []
    for table in layout_context["tables"]:
        table_id = table["table_id"]
        json_path = tables_dir / f"{table_id}.json"
        markdown_path = tables_dir / f"{table_id}.md"
        json_path.write_text(json.dumps(table, ensure_ascii=False, indent=2), encoding="utf-8")
        markdown_path.write_text(str(table.get("markdown") or ""), encoding="utf-8")
        table_records.append(
            {
                "table_id": table_id,
                "json_path": json_path,
                "markdown_path": markdown_path,
                "row_count": table.get("row_count", 0),
                "column_count": table.get("column_count", 0),
                "kind_guess": table.get("kind_guess"),
            }
        )
    return {"summary_path": summary_path, "tables_dir": tables_dir, "tables": table_records}


def _table_chunk_id(material_id: str, table_id: str, row_index: int) -> str:
    return hashlib.sha256(f"{material_id}:table:{table_id}:{row_index}".encode("utf-8")).hexdigest()[:16]


def build_table_chunks(
    tables: list[dict[str, Any]],
    *,
    material_id: str,
    user_id: str,
    start_index: int,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for table in tables:
        table_id = str(table.get("table_id") or "table")
        title = str(table.get("title") or table_id)
        columns = [str(column) for column in table.get("columns", [])]
        for row_index, row in enumerate(table.get("rows", []), start=1):
            values = [f"{column}: {row.get(column, '')}".strip() for column in columns if row.get(column, "") != ""]
            if not values:
                continue
            text = f"表格：{title}\n" + "\n".join(values)
            chunk_index = start_index + len(chunks)
            chunks.append(
                Chunk(
                    chunk_id=_table_chunk_id(material_id, table_id, row_index),
                    material_id=material_id,
                    user_id=user_id,
                    chunk_index=chunk_index,
                    text=text,
                    section_title=title,
                    heading_path=[title],
                    token_count=estimate_tokens(text),
                    metadata={
                        "source_type": "table",
                        "table_id": table_id,
                        "table_row_index": row_index,
                        "page": table.get("page"),
                        "bbox": table.get("bbox"),
                        "kind_guess": table.get("kind_guess"),
                    },
                )
            )
    return chunks
