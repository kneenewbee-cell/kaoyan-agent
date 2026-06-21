from __future__ import annotations

import re
import shutil
from pathlib import Path

IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def extract_image_refs(markdown: str) -> list[tuple[str, str]]:
    return [(match.group(1), match.group(2)) for match in IMAGE_RE.finditer(markdown)]


def resolve_image_source(source_url: str, md_dir: Path) -> Path | None:
    if source_url.startswith(("http://", "https://", "data:")):
        return None

    source_path = Path(source_url)
    if not source_path.is_absolute():
        source_path = (md_dir / source_path).resolve()

    return source_path if source_path.exists() and source_path.is_file() else None


def save_and_rewrite_images(
    markdown: str,
    md_dir: Path,
    assets_images_dir: Path,
    page_no: int | None = None,
) -> tuple[str, list[Path]]:
    assets_images_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: list[Path] = []

    def _rewrite(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        source_url = match.group(2)
        source_path = resolve_image_source(source_url, md_dir)
        if source_path is None:
            return match.group(0)

        index = len(saved_paths) + 1
        prefix = f"page_{page_no:03d}_" if page_no is not None else ""
        new_name = f"{prefix}img_{index:03d}{source_path.suffix.lower()}"
        target_path = assets_images_dir / new_name
        shutil.copy2(source_path, target_path)
        saved_paths.append(target_path)

        return f"![{alt_text or 'image'}](../assets/images/{new_name})"

    rewritten = IMAGE_RE.sub(_rewrite, markdown)
    return rewritten, saved_paths
