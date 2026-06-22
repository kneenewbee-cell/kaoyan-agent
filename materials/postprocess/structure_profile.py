"""结构画像预留：当前仅汇总强主 section 的数量。"""

from __future__ import annotations

from .section_builder import Section


def build_structure_profile(sections: list[Section], main_level: int = 2) -> dict[str, int]:
    return {
        "section_count": len(sections),
        "main_section_count": sum(section.level == main_level for section in sections),
    }
