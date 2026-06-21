"""
materials/resolver.py — 上传路径解析器。

将用户传入路径解析为待处理项目列表。当前只支持单文件，
为未来 ZIP/目录批量解析预留接口。
"""

from __future__ import annotations

from pathlib import Path

from .detector import is_reserved, is_supported, get_ext_description
from .schemas import ResolvedUploadItem


def resolve_upload_path(path: Path) -> list[ResolvedUploadItem]:
    """
    解析上传路径，返回待处理项目列表。

    当前只支持单文件。如果是目录或 ZIP，返回明确错误。

    参数
    ----
    path : Path
        文件路径。

    返回
    ----
    list[ResolvedUploadItem] : 待处理项目列表，当前只含一个元素。
    """
    if not path.exists():
        raise FileNotFoundError(f"路径不存在: {path}")

    if path.is_dir():
        raise NotImplementedError(
            "Directory upload is reserved but not implemented yet"
        )

    ext = path.suffix.lower()

    if is_reserved(ext):
        raise NotImplementedError(
            f"ZIP upload is reserved but not implemented yet: {path.name}"
        )

    is_sup = is_supported(ext)
    error = None
    if not is_sup:
        error = f"Unsupported file type: {ext} ({get_ext_description(ext)})"

    return [
        ResolvedUploadItem(
            path=path,
            original_filename=path.name,
            file_ext=ext,
            is_supported=is_sup,
            error=error,
        )
    ]
