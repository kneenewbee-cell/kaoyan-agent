"""
materials/schemas.py — materials 模块统一数据结构。

当前阶段重点：.md/.txt 纵向流程。
- parser 输出 ParseResult
- postprocess 输出 parsed/content.md
- quality 输出 parse_report.json
- chunking 输出 Chunk
- manifest 记录资料状态、路径、质量信息和元数据

说明：本文件继续使用 dataclass，保持与当前项目兼容；未来接数据库/Pydantic 时再统一升级。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class Subject(str, Enum):
    MATH = "math"
    POLITICS = "politics"
    COMPUTER_408 = "408"
    ENGLISH = "english"
    OTHER = "other"
    UNKNOWN = "unknown"


class MaterialType(str, Enum):
    LECTURE = "lecture"
    NOTE = "note"
    EXAM = "exam"
    WRONG_BOOK = "wrong_book"
    SCHOOL_INFO = "school_info"
    OTHER = "other"
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


class QualityStatus(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class DetectedFile:
    path: Path
    original_filename: str
    file_ext: str
    mime_type: str
    sha256: str
    size_bytes: int


@dataclass
class ResolvedUploadItem:
    path: Path
    original_filename: str
    file_ext: str
    is_supported: bool
    error: str | None = None


@dataclass
class ParsedAsset:
    filename: str
    relative_path: str
    asset_type: str
    page_no: int | None = None
    description: str | None = None


@dataclass
class ParseResult:
    """parser 统一返回结果。

    parser 只负责“读懂原文件并输出基础 Markdown”，不要在 parser 中堆太多清洗逻辑。
    """

    status: ParseStatus = ParseStatus.READY
    markdown_path: Path | None = None
    json_path: Path | None = None
    layout_path: Path | None = None
    assets: list[ParsedAsset] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class Chunk:
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
    material_id: str
    user_id: str
    parse_status: ParseStatus
    manifest_path: str | None = None
    markdown_path: str | None = None
    parse_report_path: str | None = None
    chunk_count: int = 0
    asset_count: int = 0
    quality_status: str = "unknown"
    overall_confidence: float | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityReport:
    """解析/清洗/切块质量报告。

    这个报告不替代人工判断，只用于自动提示、测试和后续 LLM 辅助入口。
    """

    quality_status: QualityStatus = QualityStatus.UNKNOWN
    overall_confidence: float = 0.0
    parse_confidence: float = 0.0
    structure_confidence: float = 0.0
    asset_confidence: float = 0.0
    chunk_confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "quality_status": self.quality_status.value if isinstance(self.quality_status, QualityStatus) else self.quality_status,
            "overall_confidence": self.overall_confidence,
            "parse_confidence": self.parse_confidence,
            "structure_confidence": self.structure_confidence,
            "asset_confidence": self.asset_confidence,
            "chunk_confidence": self.chunk_confidence,
            "warnings": self.warnings,
            "metrics": self.metrics,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "QualityReport":
        return cls(
            quality_status=QualityStatus(d.get("quality_status", "unknown")),
            overall_confidence=float(d.get("overall_confidence", 0.0)),
            parse_confidence=float(d.get("parse_confidence", 0.0)),
            structure_confidence=float(d.get("structure_confidence", 0.0)),
            asset_confidence=float(d.get("asset_confidence", 0.0)),
            chunk_confidence=float(d.get("chunk_confidence", 0.0)),
            warnings=list(d.get("warnings", [])),
            metrics=dict(d.get("metrics", {})),
        )


@dataclass
class MaterialManifest:
    material_id: str
    user_id: str
    original_filename: str
    file_ext: str
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
        "parse_report": None,
        "format_probe": None,
        "cleaning_strategy": None,
    })
    chunk_count: int = 0
    asset_count: int = 0
    quality_status: str = "unknown"
    overall_confidence: float | None = None
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
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
            "quality_status": self.quality_status,
            "overall_confidence": self.overall_confidence,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "MaterialManifest":
        paths = d.get("paths", {}) or {}
        paths.setdefault("original", None)
        paths.setdefault("markdown", None)
        paths.setdefault("json", None)
        paths.setdefault("layout", None)
        paths.setdefault("chunks", None)
        paths.setdefault("search_index", None)
        paths.setdefault("parse_report", None)
        paths.setdefault("format_probe", None)
        paths.setdefault("cleaning_strategy", None)
        return cls(
            material_id=d["material_id"],
            user_id=d["user_id"],
            original_filename=d.get("original_filename", ""),
            file_ext=d.get("file_ext", ""),
            mime_type=d.get("mime_type", ""),
            sha256=d.get("sha256", ""),
            subject=Subject(d.get("subject", "unknown")),
            course=d.get("course"),
            material_type=MaterialType(d.get("material_type", "unknown")),
            parser_name=ParserName(d.get("parser_name", "unsupported")),
            parse_status=ParseStatus(d.get("parse_status", "pending")),
            paths=paths,
            chunk_count=int(d.get("chunk_count", 0)),
            asset_count=int(d.get("asset_count", 0)),
            quality_status=d.get("quality_status", "unknown"),
            overall_confidence=d.get("overall_confidence"),
            warnings=list(d.get("warnings", [])),
            metadata=dict(d.get("metadata", {})),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            error=d.get("error"),
        )
