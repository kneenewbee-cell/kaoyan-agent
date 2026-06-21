"""
materials/detector.py — 文件类型识别。

根据扩展名和 MIME 类型识别文件，计算 sha256，输出统一 DetectedFile。
"""

from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path

from .schemas import DetectedFile

# 受支持的扩展名列表
SUPPORTED_EXTENSIONS: set[str] = {
    ".md", ".txt", ".pdf", ".docx",
    ".png", ".jpg", ".jpeg", ".webp",
}

# 预留但未实现的扩展名
RESERVED_EXTENSIONS: set[str] = {".zip"}

# 扩展名 → 友好名称映射
EXT_DESCRIPTIONS: dict[str, str] = {
    ".md": "Markdown",
    ".txt": "Plain Text",
    ".pdf": "PDF Document",
    ".docx": "Word Document",
    ".png": "PNG Image",
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".webp": "WebP Image",
    ".zip": "ZIP Archive",
}


def _compute_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    """计算文件 SHA-256。"""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha.update(chunk)
    return sha.hexdigest()


def detect_file(file_path: Path) -> DetectedFile:
    """
    检测文件类型并返回 DetectedFile。

    参数
    ----
    file_path : Path
        文件路径。

    返回
    ----
    DetectedFile : 包含扩展名、mime、sha256、大小等信息。

    异常
    ----
    FileNotFoundError : 文件不存在。
    ValueError : 文件扩展名不受支持且不在预留列表中。
    """
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"路径不是文件: {file_path}")

    ext = file_path.suffix.lower()
    if not ext:
        raise ValueError(f"无法识别文件类型（无扩展名）: {file_path.name}")

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "application/octet-stream"

    sha256 = _compute_sha256(file_path)
    size_bytes = file_path.stat().st_size

    return DetectedFile(
        path=file_path,
        original_filename=file_path.name,
        file_ext=ext,
        mime_type=mime_type,
        sha256=sha256,
        size_bytes=size_bytes,
    )


def is_supported(ext: str) -> bool:
    """判断扩展名是否受支持。"""
    return ext.lower() in SUPPORTED_EXTENSIONS


def is_reserved(ext: str) -> bool:
    """判断扩展名是否为预留但未实现。"""
    return ext.lower() in RESERVED_EXTENSIONS


def get_ext_description(ext: str) -> str:
    """获取扩展名的友好描述。"""
    return EXT_DESCRIPTIONS.get(ext.lower(), f"Unknown ({ext})")
