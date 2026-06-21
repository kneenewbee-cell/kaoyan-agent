"""
materials/schemas.py — 资料模块所有 Pydantic 模型与数据结构。

包含：material manifest、parse result、chunk、search result 等 schema。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


# —————————————————————————— 枚举 ——————————————————————————


class Subject(str, Enum):
    MATH = "math"
    POLITICS = "politics"
    COMPUTER_408 = "408"
    ENGLISH = "english"
    UNKNOWN = "unknown"


class MaterialType(str, Enum):
    LECTURE = "lecture"
    NOTE = "note"
    EXAM = "exam"
    WRONG_BOOK = "wrong_book"
    SCHOOL_INFO = "school_info"
    UNKNOWN = "unknown"


class ParseStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class ParserName(str, Enum):
    MARKDOWN = "markdown"
    TEXT = "text"
    MINERU = "mineru"
    DOCX = "docx"
    IMAGE = "image"
    UNSUPPORTED = "unsupported"


# —————————————————————————— 基础数据类 ——————————————————————————


@dataclass
class DetectedFile:
    """detector 输出的统一文件描述。"""
    path: Path
    original_filename: str
    file_ext: str           # 含点号，如 ".md"
    mime_type: str
    sha256: str
    size_bytes: int


@dataclass
class ResolvedUploadItem:
    """resolver 输出的单个待处理项目。"""
    path: Path
    original_filename: str
    file_ext: str
    is_supported: bool
    error: str | None = None


@dataclass
class ParsedAsset:
    """解析出的单个资源文件（图片、表格等）。"""
    filename: str
    relative_path: str      # 相对 material_dir 的路径
    asset_type: str          # "image" | "table" | "formula" | "diagram" | "unknown"
    page_no: int | None = None
    description: str | None = None


@dataclass
class ParseResult:
    """parser 统一返回结果。"""
    status: ParseStatus = ParseStatus.READY
    markdown_path: Path | None = None
    json_path: Path | None = None
    layout_path: Path | None = None
    assets: list[ParsedAsset] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class Chunk:
    """单个文本块。"""
    chunk_id: str
    material_id: str
    user_id: str
    chunk_index: int
    text: str
    section_title: str | None = None
    heading_path: list[str] = field(default_factory=list)
    page_start: int | None = None
    page_end: int | None = None
    asset_paths: list[str] = field(default_factory=list)
    token_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "material_id": self.material_id,
            "user_id": self.user_id,
            "chunk_index": self.chunk_index,
            "text": self.text,
            "section_title": self.section_title,
            "heading_path": self.heading_path,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "asset_paths": self.asset_paths,
            "token_count": self.token_count,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Chunk":
        return cls(
            chunk_id=d["chunk_id"],
            material_id=d["material_id"],
            user_id=d["user_id"],
            chunk_index=d["chunk_index"],
            text=d["text"],
            section_title=d.get("section_title"),
            heading_path=d.get("heading_path", []),
            page_start=d.get("page_start"),
            page_end=d.get("page_end"),
            asset_paths=d.get("asset_paths", []),
            token_count=d.get("token_count", 0),
            metadata=d.get("metadata", {}),
        )


@dataclass
class MaterialSearchResult:
    """search 统一返回结果。"""
    rank: int
    material_id: str
    user_id: str
    chunk_id: str
    score: float
    text: str
    section_title: str | None = None
    heading_path: list[str] = field(default_factory=list)
    asset_paths: list[str] = field(default_factory=list)
    source_markdown_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MaterialIngestionResult:
    """service.ingest_file 返回的完整入库结果。"""
    material_id: str
    user_id: str
    parse_status: ParseStatus
    manifest_path: str | None = None
    markdown_path: str | None = None
    chunk_count: int = 0
    asset_count: int = 0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


# —————————————————————————— Manifest ——————————————————————————


@dataclass
class MaterialManifest:
    """manifest.json 数据结构。"""
    material_id: str
    user_id: str
    original_filename: str
    file_ext: str  # ".md", ".pdf" 等
    mime_type: str
    sha256: str
    subject: Subject = Subject.UNKNOWN
    course: str | None = None
    material_type: MaterialType = MaterialType.UNKNOWN
    parser_name: ParserName = ParserName.UNSUPPORTED
    parse_status: ParseStatus = ParseStatus.PENDING
    paths: dict[str, str | None] = field(default_factory=lambda: {
        "original": None,
        "markdown": None,
        "json": None,
        "layout": None,
        "chunks": None,
        "search_index": None,
    })
    chunk_count: int = 0
    asset_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "material_id": self.material_id,
            "user_id": self.user_id,
            "original_filename": self.original_filename,
            "file_ext": self.file_ext,
            "mime_type": self.mime_type,
            "sha256": self.sha256,
            "subject": self.subject.value if isinstance(self.subject, Subject) else self.subject,
            "course": self.course,
            "material_type": self.material_type.value if isinstance(self.material_type, MaterialType) else self.material_type,
            "parser_name": self.parser_name.value if isinstance(self.parser_name, ParserName) else self.parser_name,
            "parse_status": self.parse_status.value if isinstance(self.parse_status, ParseStatus) else self.parse_status,
            "paths": self.paths,
            "chunk_count": self.chunk_count,
            "asset_count": self.asset_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "MaterialManifest":
        return cls(
            material_id=d["material_id"],
            user_id=d["user_id"],
            original_filename=d["original_filename"],
            file_ext=d["file_ext"],
            mime_type=d["mime_type"],
            sha256=d["sha256"],
            subject=Subject(d.get("subject", "unknown")),
            course=d.get("course"),
            material_type=MaterialType(d.get("material_type", "unknown")),
            parser_name=ParserName(d.get("parser_name", "unsupported")),
            parse_status=ParseStatus(d.get("parse_status", "pending")),
            paths=d.get("paths", {}),
            chunk_count=d.get("chunk_count", 0),
            asset_count=d.get("asset_count", 0),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            error=d.get("error"),
        )
