from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import Chunk, MaterialManifest, MaterialType, ParseStatus, ParserName, Subject
from .security import ensure_within_base, resolve_material_id, resolve_user_id

DEFAULT_USER_MATERIALS_DIR: Path = Path(__file__).resolve().parents[1] / "data" / "user_materials"


class MaterialStorage:
    def __init__(self, base_dir: Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else DEFAULT_USER_MATERIALS_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def user_dir(self, user_id: str) -> Path:
        safe_user_id = resolve_user_id(user_id)
        target = self.base_dir / safe_user_id
        ensure_within_base(self.base_dir, target)
        return target

    def material_dir(self, user_id: str, material_id: str) -> Path:
        safe_user_id = resolve_user_id(user_id)
        safe_material_id = resolve_material_id(material_id)
        user_dir = self.user_dir(safe_user_id)
        target = user_dir / safe_material_id
        ensure_within_base(user_dir, target)
        return target

    def create_material_dir(self, user_id: str, material_id: str) -> Path:
        root = self.material_dir(user_id, material_id)
        for sub_dir in ["original", "parsed", "assets/images", "chunks", "index"]:
            (root / sub_dir).mkdir(parents=True, exist_ok=True)
        return root

    def save_original(self, user_id: str, material_id: str, source_path: Path) -> Path:
        target = self.material_dir(user_id, material_id) / "original" / source_path.name
        shutil.copy2(source_path, target)
        return target

    def save_chunks_jsonl(self, user_id: str, material_id: str, chunks: list[Chunk]) -> Path:
        target = self.material_dir(user_id, material_id) / "chunks" / "chunks.jsonl"
        with target.open("w", encoding="utf-8") as file:
            for chunk in chunks:
                file.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")
        return target

    def save_chunks_debug(self, user_id: str, material_id: str, chunks: list[Chunk]) -> Path:
        target = self.material_dir(user_id, material_id) / "chunks" / "chunks_debug.md"
        lines: list[str] = [f"# Chunks Debug - {material_id}", "", f"total chunks: {len(chunks)}", ""]
        for chunk in chunks:
            lines.append(f"## Chunk #{chunk.chunk_index}: {chunk.section_title or '(no section)'}")
            lines.append(f"- chunk_id: {chunk.chunk_id}")
            lines.append(f"- heading_path: {' > '.join(chunk.heading_path) if chunk.heading_path else '(none)'}")
            lines.append(f"- token_count: {chunk.token_count}")
            lines.append(f"- asset_paths: {chunk.asset_paths}")
            lines.append("")
            lines.append(chunk.text[:500] if chunk.text else "(empty)")
            lines.append("")
        target.write_text("\n".join(lines), encoding="utf-8")
        return target

    def save_search_index(self, user_id: str, material_id: str, index_data: dict[str, Any]) -> Path:
        target = self.material_dir(user_id, material_id) / "index" / "search_index.json"
        target.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8")
        return target

    def save_manifest(self, user_id: str, material_id: str, manifest: MaterialManifest) -> Path:
        manifest.updated_at = datetime.now(timezone.utc).isoformat()
        target = self.material_dir(user_id, material_id) / "manifest.json"
        target.write_text(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return target

    def load_manifest(self, user_id: str, material_id: str) -> MaterialManifest | None:
        target = self.material_dir(user_id, material_id) / "manifest.json"
        if not target.exists():
            return None
        return MaterialManifest.from_dict(json.loads(target.read_text(encoding="utf-8")))

    def list_user_manifests(self, user_id: str) -> list[MaterialManifest]:
        user_dir = self.user_dir(user_id)
        if not user_dir.exists():
            return []

        manifests: list[MaterialManifest] = []
        for material_dir in sorted(user_dir.iterdir()):
            if not material_dir.is_dir():
                continue

            manifest_path = material_dir / "manifest.json"
            if not manifest_path.exists():
                manifests.append(
                    MaterialManifest(
                        material_id=material_dir.name,
                        user_id=resolve_user_id(user_id),
                        original_filename="",
                        file_ext="",
                        mime_type="",
                        sha256="",
                        subject=Subject.UNKNOWN,
                        material_type=MaterialType.UNKNOWN,
                        parser_name=ParserName.UNSUPPORTED,
                        parse_status=ParseStatus.FAILED,
                        error="broken_manifest",
                    )
                )
                continue

            try:
                manifests.append(MaterialManifest.from_dict(json.loads(manifest_path.read_text(encoding="utf-8"))))
            except Exception as exc:
                manifests.append(
                    MaterialManifest(
                        material_id=material_dir.name,
                        user_id=resolve_user_id(user_id),
                        original_filename="",
                        file_ext="",
                        mime_type="",
                        sha256="",
                        subject=Subject.UNKNOWN,
                        material_type=MaterialType.UNKNOWN,
                        parser_name=ParserName.UNSUPPORTED,
                        parse_status=ParseStatus.FAILED,
                        error=f"broken_manifest: {exc}",
                    )
                )

        return manifests

    def delete_material(self, user_id: str, material_id: str) -> None:
        user_dir = self.user_dir(user_id)
        target = self.material_dir(user_id, material_id)
        ensure_within_base(user_dir, target)
        if not target.exists() or not target.is_dir():
            raise FileNotFoundError("Material not found")
        shutil.rmtree(target)
