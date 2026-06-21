"""
materials/parsers/mineru_parser.py — MinerU PDF/图片解析器封装。

封装 MinerU CLI/API，将 PDF/图片解析为 Markdown。当前 MVP 阶段返回占位。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


class MinerUParser(BaseMaterialParser):
    """MinerU 解析器，处理 PDF 和复杂版面图片。"""

    parser_name = "mineru"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        """
        封装 MinerU CLI 调用来解析 PDF/图片。

        MVP 阶段：如果环境变量 MINERU_ENABLED 不为 "1"，返回占位错误。
        后续真正接入时，通过 mineru 命令行调用并收集输出。
        """
        mineru_enabled = os.environ.get("MINERU_ENABLED", "") == "1"
        mineru_bin = os.environ.get("MINERU_BIN", "mineru")

        if not mineru_enabled:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=(
                    "MinerU is not available in current environment. "
                    "Set MINERU_ENABLED=1 and MINERU_BIN to the correct path to enable MinerU parsing."
                ),
            )

        # TODO: 真正接入 MinerU CLI
        # 1. 调用 mineru CLI: subprocess.run([mineru_bin, str(input_path), "-o", str(output_dir)])
        # 2. 收集 Markdown 输出
        # 3. 收集图片资源
        # 4. 收集 layout.json

        try:
            import subprocess

            output_dir.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                [mineru_bin, str(input_path), "-o", str(output_dir)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 分钟超时
            )

            if result.returncode != 0:
                return ParseResult(
                    status=ParseStatus.FAILED,
                    error=f"MinerU 解析失败 (exit code {result.returncode}): {result.stderr}",
                )

            # 查找 MinerU 输出的 Markdown 文件
            md_files = list(output_dir.glob("**/*.md"))
            md_path = md_files[0] if md_files else None

            return ParseResult(
                status=ParseStatus.READY if md_path else ParseStatus.FAILED,
                markdown_path=md_path,
                json_path=None,
                layout_path=None,
                error=None if md_path else "MinerU 未生成 Markdown 输出",
            )

        except FileNotFoundError:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU binary '{mineru_bin}' not found. Please install MinerU first.",
            )
        except Exception as e:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU 调用异常: {e}",
            )
