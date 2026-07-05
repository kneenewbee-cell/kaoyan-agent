"""Optional KaTeX-backed formula render validation."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]


def find_katex_package_dir() -> Path | None:
    env_path = os.getenv("KATEX_PACKAGE_DIR", "").strip()
    candidates = [
        Path(env_path) if env_path else None,
        ROOT / "node_modules" / "katex",
        ROOT / "web" / "node_modules" / "katex",
        ROOT / "data" / "debug" / "katex_runtime" / "node_modules" / "katex",
    ]
    for candidate in candidates:
        if candidate and (candidate / "package.json").exists():
            return candidate
    return None


def validate_latex_with_katex_batch(
    items: Sequence[tuple[str, bool]],
    *,
    timeout_seconds: int = 60,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate formulas with KaTeX in a single Node process when available."""

    katex_dir = find_katex_package_dir()
    metadata: dict[str, Any] = {
        "engine": "katex",
        "available": katex_dir is not None,
        "package_dir": str(katex_dir) if katex_dir else None,
    }
    if katex_dir is None:
        return (
            [
                {
                    "ok": True,
                    "error": None,
                    "engine": "unavailable",
                }
                for _ in items
            ],
            metadata,
        )

    payload = [
        {
            "latex": latex,
            "displayMode": bool(display_mode),
        }
        for latex, display_mode in items
    ]
    script = f"""
const katex = require({json.dumps(str(katex_dir))});
const version = require({json.dumps(str(katex_dir / "package.json"))}).version;
let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => input += chunk);
process.stdin.on("end", () => {{
  const items = JSON.parse(input);
  const results = items.map(item => {{
    try {{
      const html = katex.renderToString(item.latex, {{
        displayMode: Boolean(item.displayMode),
        throwOnError: true,
        strict: "ignore"
      }});
      return {{ ok: true, error: null, htmlLength: html.length, version }};
    }} catch (err) {{
      return {{
        ok: false,
        error: String((err && err.message) || err),
        version
      }};
    }}
  }});
  process.stdout.write(JSON.stringify({{ version, results }}));
}});
"""
    try:
        completed = subprocess.run(
            ["node", "-e", script],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=timeout_seconds,
            check=True,
        )
        parsed = json.loads(completed.stdout)
    except Exception as exc:
        metadata.update(
            {
                "available": False,
                "error_type": exc.__class__.__name__,
                "error": str(exc),
            }
        )
        return (
            [
                {
                    "ok": True,
                    "error": None,
                    "engine": "unavailable",
                }
                for _ in items
            ],
            metadata,
        )

    metadata["version"] = parsed.get("version")
    results = []
    for result in parsed.get("results", []):
        results.append(
            {
                "ok": bool(result.get("ok")),
                "error": result.get("error"),
                "engine": "katex",
                "version": parsed.get("version"),
                "html_length": result.get("htmlLength"),
            }
        )
    return results, metadata

