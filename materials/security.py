from __future__ import annotations

import re
from pathlib import Path

DEFAULT_USER_ID = "tester"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def get_default_user_id() -> str:
    return DEFAULT_USER_ID


def validate_safe_id(value: str, field_name: str) -> str:
    candidate = (value or "").strip()
    if not candidate or not SAFE_ID_RE.fullmatch(candidate):
        raise ValueError(f"Invalid {field_name}")
    return candidate


def resolve_user_id(user_id: str | None = None) -> str:
    return validate_safe_id(user_id or DEFAULT_USER_ID, "user_id")


def resolve_material_id(material_id: str) -> str:
    return validate_safe_id(material_id, "material_id")


def ensure_within_base(base_dir: Path, target_dir: Path) -> Path:
    base_resolved = base_dir.resolve()
    target_resolved = target_dir.resolve()
    target_resolved.relative_to(base_resolved)
    return target_resolved
