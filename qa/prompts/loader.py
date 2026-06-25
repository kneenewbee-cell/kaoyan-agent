from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import Any

PROMPT_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PROMPT_ROOT / "manifest.json"


@lru_cache(maxsize=1)
def load_prompt_manifest() -> dict[str, dict[str, Any]]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Prompt manifest must be an object: {MANIFEST_PATH}")
    return data


@lru_cache(maxsize=None)
def load_prompt(name: str, version: str | None = None, **template_vars: Any) -> str:
    manifest = load_prompt_manifest()
    item = manifest.get(name)
    if not isinstance(item, dict):
        raise KeyError(f"Unknown prompt: {name}")
    if version is not None and item.get("version") != version:
        raise ValueError(f"Prompt {name} version mismatch: expected {version}, got {item.get('version')}")
    rel_path = item.get("path")
    if not isinstance(rel_path, str) or not rel_path:
        raise ValueError(f"Prompt {name} has no path in manifest")
    prompt_path = (PROMPT_ROOT / rel_path).resolve()
    if PROMPT_ROOT.resolve() not in prompt_path.parents:
        raise ValueError(f"Prompt path escapes prompt root: {rel_path}")
    text = prompt_path.read_text(encoding="utf-8")
    return Template(text).safe_substitute(**template_vars) if template_vars else text
