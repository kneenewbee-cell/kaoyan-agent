"""MinerU parser backend for PDF/image materials.

The parser keeps MinerU's raw output under ``parsed/mineru_raw`` and exposes
stable project entry points at ``parsed/content.md`` and ``parsed/layout.json``.
Downstream cleaning/chunking code should only depend on those stable paths.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import time
import urllib.error
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any

from .base import BaseMaterialParser
from ..schemas import ParseResult, ParseStatus


DEFAULT_TIMEOUT_SECONDS = 900
DEFAULT_CLOUD_TIMEOUT_SECONDS = 1800
DEFAULT_CLOUD_POLL_INTERVAL_SECONDS = 3.0
MINERU_API_BASE_URL = "https://mineru.net"
DEFAULT_COMMAND_TEMPLATE = "{bin} -p {input} -o {output} -b pipeline"
IMAGE_RE = re.compile(r'!\[[^\]]*]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _load_local_env() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env", encoding="utf-8-sig", override=False)


def _safe_read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gbk", "cp936"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _safe_extract_zip(zip_bytes: bytes, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_root = output_dir.resolve()
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        for info in archive.infolist():
            target = (output_dir / info.filename).resolve()
            if output_root != target and output_root not in target.parents:
                raise ValueError(f"Unsafe zip member path: {info.filename}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)


def _redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {key: ("<redacted>" if key.lower() == "authorization" else value) for key, value in headers.items()}


def _json_http_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout_seconds: int = 60,
) -> dict[str, Any]:
    data = None
    request_headers = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8", errors="replace")
    return json.loads(body) if body else {}


def _put_file(upload_url: str, input_path: Path, *, timeout_seconds: int) -> int:
    data = input_path.read_bytes()
    # Alibaba OSS pre-signed URLs used by MinerU are signed without a content
    # type. urllib adds application/x-www-form-urlencoded for byte bodies unless
    # a header is present, which breaks the OSS signature.
    request = urllib.request.Request(upload_url, data=data, headers={"Content-Type": ""}, method="PUT")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        response.read()
        return int(response.status)


def _download_bytes(url: str, *, timeout_seconds: int) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
        return response.read()


def _api_success(payload: dict[str, Any]) -> bool:
    code = payload.get("code")
    if code is None:
        return True
    return code in {0, 200, "0", "200", "success", "ok"}


def _api_data(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data")
    return data if isinstance(data, dict) else {}


def _find_first(root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(path for path in root.rglob(pattern) if path.is_file())
        if matches:
            return matches[0]
    return None


def _find_full_markdown(raw_dir: Path) -> Path | None:
    full_md = _find_first(raw_dir, ["full.md"])
    if full_md:
        return full_md
    return _find_first(raw_dir, ["*.md"])


def _find_layout_json(markdown_path: Path, raw_dir: Path) -> Path | None:
    nearby = markdown_path.parent / "layout.json"
    if nearby.exists() and nearby.is_file():
        return nearby
    return _find_first(raw_dir, ["layout.json"])


def _find_content_list_json(markdown_path: Path, raw_dir: Path) -> Path | None:
    patterns = ["*_content_list.json", "content_list.json", "*_content_list_v2.json"]
    for base in (markdown_path.parent, raw_dir):
        result = _find_first(base, patterns)
        if result:
            return result
    return None


def _materialize_mineru_output(
    *,
    output_dir: Path,
    raw_dir: Path,
    input_path: Path,
    parser_backend: str,
    metadata_extra: dict[str, Any] | None = None,
    warnings_extra: list[str] | None = None,
) -> ParseResult:
    markdown_source = _find_full_markdown(raw_dir)
    if markdown_source is None:
        return ParseResult(
            status=ParseStatus.FAILED,
            error="MinerU did not produce full.md or any Markdown output.",
            metadata={"parser_backend": parser_backend, "mineru_raw_dir": str(raw_dir), **(metadata_extra or {})},
        )

    markdown_text = _safe_read_text(markdown_source).replace("\r\n", "\n").replace("\r", "\n")
    content_path = output_dir / "content.md"
    content_path.write_text(markdown_text, encoding="utf-8")

    layout_source = _find_layout_json(markdown_source, raw_dir)
    layout_path: Path | None = None
    if layout_source is not None:
        layout_path = output_dir / "layout.json"
        shutil.copy2(layout_source, layout_path)

    content_list_path = _find_content_list_json(markdown_source, raw_dir)
    image_refs = [match.group(1) for match in IMAGE_RE.finditer(markdown_text)]
    source_dir = markdown_source.parent

    metadata: dict[str, Any] = {
        "source_format": "pdf",
        "parser_backend": parser_backend,
        "source_dir": str(source_dir),
        "mineru_raw_dir": str(raw_dir),
        "mineru_markdown_source": str(markdown_source),
        "mineru_layout_source": str(layout_source) if layout_source else None,
        "line_count": len(markdown_text.splitlines()),
        "char_count": len(markdown_text),
        "image_ref_count": len(image_refs),
        "layout_available": layout_path is not None,
        "content_list_available": content_list_path is not None,
        "original_filename": input_path.name,
        **(metadata_extra or {}),
    }

    warnings = list(warnings_extra or [])
    if layout_path is None:
        warnings.append("mineru_layout_json_missing")
    if content_list_path is None:
        warnings.append("mineru_content_list_json_missing")

    return ParseResult(
        status=ParseStatus.READY,
        markdown_path=content_path,
        json_path=content_list_path,
        layout_path=layout_path,
        metadata=metadata,
        warnings=warnings,
    )


def _build_command(*, mineru_bin: str, input_path: Path, output_dir: Path) -> tuple[list[str], str]:
    template = os.environ.get("MINERU_COMMAND_TEMPLATE")
    if not template:
        args = [mineru_bin, "-p", str(input_path), "-o", str(output_dir), "-b", "pipeline"]
        return args, " ".join(subprocess.list2cmdline([arg]) for arg in args)

    command_text = template.format(
        bin=mineru_bin,
        input=str(input_path),
        output=str(output_dir),
    )
    args = shlex.split(command_text, posix=os.name != "nt")
    args = [arg[1:-1] if len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in {"'", '"'} else arg for arg in args]
    return args, command_text


class MinerUParser(BaseMaterialParser):
    """Parse PDFs/images with a locally installed MinerU CLI."""

    parser_name = "mineru"

    def parse(
        self,
        input_path: Path,
        output_dir: Path,
        context: dict[str, Any] | None = None,
    ) -> ParseResult:
        _load_local_env()

        if not input_path.exists():
            return ParseResult(status=ParseStatus.FAILED, error=f"Input file does not exist: {input_path}")

        if not _env_flag("MINERU_ENABLED"):
            return ParseResult(
                status=ParseStatus.FAILED,
                error=(
                    "MinerU is disabled. Set MINERU_ENABLED=1 and configure MINERU_BIN "
                    "or MINERU_COMMAND_TEMPLATE to enable PDF parsing."
                ),
            )

        backend = os.environ.get("MINERU_BACKEND", "cli").strip().lower()
        if backend == "api":
            backend = "cloud"
        if backend == "auto":
            backend = "cloud" if os.environ.get("MINERU_API_TOKEN") else "cli"
        if backend == "cloud":
            result = self._parse_cloud(input_path, output_dir)
            if result.status == ParseStatus.READY:
                return result
            if _env_flag("MINERU_CLOUD_FALLBACK_TO_CLI", default=False):
                fallback = self._parse_cli(input_path, output_dir)
                fallback.warnings.insert(0, "mineru_cloud_failed_fell_back_to_cli")
                fallback.metadata["mineru_cloud_error"] = result.error
                return fallback
            return result
        if backend == "cli":
            return self._parse_cli(input_path, output_dir)

        return ParseResult(
            status=ParseStatus.FAILED,
            error=f"Unsupported MinerU backend '{backend}'. Use MINERU_BACKEND=cloud, cli, or auto.",
        )

    def _parse_cli(self, input_path: Path, output_dir: Path) -> ParseResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "mineru_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        mineru_bin = os.environ.get("MINERU_BIN", "mineru")
        timeout_seconds = int(os.environ.get("MINERU_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))
        args, command_text = _build_command(mineru_bin=mineru_bin, input_path=input_path, output_dir=raw_dir)

        command_record = {
            "backend": "cli",
            "command": command_text,
            "args": args,
            "input_path": str(input_path),
            "output_dir": str(raw_dir),
            "timeout_seconds": timeout_seconds,
            "started_at": time.time(),
        }
        (raw_dir / "mineru_command.json").write_text(
            json.dumps(command_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        try:
            completed = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except FileNotFoundError:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU binary '{mineru_bin}' not found. Configure MINERU_BIN or MINERU_COMMAND_TEMPLATE.",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )
        except subprocess.TimeoutExpired as exc:
            (raw_dir / "mineru_stdout.txt").write_text(exc.stdout or "", encoding="utf-8", errors="replace")
            (raw_dir / "mineru_stderr.txt").write_text(exc.stderr or "", encoding="utf-8", errors="replace")
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU parsing timed out after {timeout_seconds}s.",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )
        except Exception as exc:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU invocation failed: {exc}",
                metadata={"parser_backend": "mineru_cli", "mineru_raw_dir": str(raw_dir)},
            )

        (raw_dir / "mineru_stdout.txt").write_text(completed.stdout or "", encoding="utf-8", errors="replace")
        (raw_dir / "mineru_stderr.txt").write_text(completed.stderr or "", encoding="utf-8", errors="replace")

        if completed.returncode != 0:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU parsing failed with exit code {completed.returncode}.",
                metadata={
                    "parser_backend": "mineru_cli",
                    "mineru_raw_dir": str(raw_dir),
                    "mineru_exit_code": completed.returncode,
                },
            )

        return _materialize_mineru_output(
            output_dir=output_dir,
            raw_dir=raw_dir,
            input_path=input_path,
            parser_backend="mineru_cli",
            metadata_extra={
                "mineru_exit_code": completed.returncode,
            },
        )

    def _parse_cloud(self, input_path: Path, output_dir: Path) -> ParseResult:
        token = os.environ.get("MINERU_API_TOKEN", "").strip()
        if not token:
            return ParseResult(
                status=ParseStatus.FAILED,
                error="MINERU_API_TOKEN is required when MINERU_BACKEND=cloud.",
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "mineru_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        base_url = os.environ.get("MINERU_API_BASE_URL", MINERU_API_BASE_URL).rstrip("/")
        timeout_seconds = _env_int("MINERU_CLOUD_TIMEOUT_SECONDS", DEFAULT_CLOUD_TIMEOUT_SECONDS)
        poll_interval = _env_float("MINERU_CLOUD_POLL_INTERVAL_SECONDS", DEFAULT_CLOUD_POLL_INTERVAL_SECONDS)
        model_version = os.environ.get("MINERU_MODEL_VERSION", "pipeline").strip() or "pipeline"
        language = os.environ.get("MINERU_LANGUAGE", "ch").strip() or "ch"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "*/*",
        }
        data_id = f"{input_path.stem}-{int(time.time())}"
        payload = {
            "files": [{"name": input_path.name, "data_id": data_id}],
            "model_version": model_version,
            "language": language,
            "enable_formula": _env_flag("MINERU_ENABLE_FORMULA", default=True),
            "enable_table": _env_flag("MINERU_ENABLE_TABLE", default=True),
        }
        if _env_flag("MINERU_CLOUD_NO_CACHE", default=False):
            payload["no_cache"] = True
        page_ranges = os.environ.get("MINERU_PAGE_RANGES")
        if page_ranges:
            payload["page_ranges"] = page_ranges

        started_at = time.time()
        request_record = {
            "backend": "cloud",
            "base_url": base_url,
            "request_url": f"{base_url}/api/v4/file-urls/batch",
            "headers": _redact_headers(headers),
            "payload": payload,
            "input_path": str(input_path),
            "output_dir": str(raw_dir),
            "timeout_seconds": timeout_seconds,
            "started_at": started_at,
        }
        (raw_dir / "mineru_cloud_request.json").write_text(
            json.dumps(request_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        try:
            create_payload = _json_http_request(
                "POST",
                f"{base_url}/api/v4/file-urls/batch",
                headers=headers,
                payload=payload,
                timeout_seconds=60,
            )
            if not _api_success(create_payload):
                return ParseResult(
                    status=ParseStatus.FAILED,
                    error=f"MinerU cloud upload-url request failed: {create_payload.get('msg') or create_payload.get('message') or create_payload.get('code')}",
                    metadata={"parser_backend": "mineru_cloud", "mineru_raw_dir": str(raw_dir)},
                )
            data = _api_data(create_payload)
            batch_id = data.get("batch_id")
            file_urls = data.get("file_urls") or []
            upload_url = file_urls[0] if file_urls else None
            if not batch_id or not upload_url:
                return ParseResult(
                    status=ParseStatus.FAILED,
                    error="MinerU cloud did not return batch_id and upload URL.",
                    metadata={"parser_backend": "mineru_cloud", "mineru_raw_dir": str(raw_dir)},
                )

            upload_status = _put_file(upload_url, input_path, timeout_seconds=min(timeout_seconds, 600))
            result_url = f"{base_url}/api/v4/extract-results/batch/{batch_id}"
            states: list[dict[str, Any]] = []
            full_zip_url: str | None = None
            final_result: dict[str, Any] = {}
            deadline = time.time() + timeout_seconds
            while time.time() < deadline:
                result_payload = _json_http_request(
                    "GET",
                    result_url,
                    headers=headers,
                    timeout_seconds=60,
                )
                result_data = _api_data(result_payload)
                extract_results = result_data.get("extract_result") or []
                current = extract_results[0] if extract_results else result_data
                if not isinstance(current, dict):
                    current = {}
                state = str(current.get("state") or current.get("status") or "").lower()
                states.append(
                    {
                        "state": state,
                        "progress": current.get("extract_progress") or current.get("progress"),
                        "updated_at": time.time(),
                    }
                )
                final_result = current
                if state == "done":
                    full_zip_url = current.get("full_zip_url") or current.get("zip_url") or current.get("result_url")
                    break
                if state == "failed":
                    return ParseResult(
                        status=ParseStatus.FAILED,
                        error=f"MinerU cloud parsing failed: {current.get('err_msg') or current.get('message') or current}",
                        metadata={
                            "parser_backend": "mineru_cloud",
                            "mineru_raw_dir": str(raw_dir),
                            "mineru_batch_id": batch_id,
                        },
                    )
                time.sleep(max(poll_interval, 0.5))

            cloud_result_record = {
                "backend": "cloud",
                "batch_id": batch_id,
                "upload_status": upload_status,
                "poll_count": len(states),
                "states": states[-120:],
                "final_result": final_result,
                "elapsed_seconds": round(time.time() - started_at, 2),
            }
            (raw_dir / "mineru_cloud_result.json").write_text(
                json.dumps(cloud_result_record, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            if not full_zip_url:
                return ParseResult(
                    status=ParseStatus.FAILED,
                    error=f"MinerU cloud parsing timed out after {timeout_seconds}s.",
                    metadata={
                        "parser_backend": "mineru_cloud",
                        "mineru_raw_dir": str(raw_dir),
                        "mineru_batch_id": batch_id,
                    },
                )

            zip_bytes = _download_bytes(full_zip_url, timeout_seconds=min(timeout_seconds, 600))
            (raw_dir / "mineru_result.zip").write_bytes(zip_bytes)
            _safe_extract_zip(zip_bytes, raw_dir)
            return _materialize_mineru_output(
                output_dir=output_dir,
                raw_dir=raw_dir,
                input_path=input_path,
                parser_backend="mineru_cloud",
                metadata_extra={
                    "mineru_batch_id": batch_id,
                    "mineru_model_version": model_version,
                    "mineru_language": language,
                    "mineru_cloud_elapsed_seconds": round(time.time() - started_at, 2),
                    "mineru_cloud_poll_count": len(states),
                    "mineru_cloud_upload_status": upload_status,
                },
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU cloud HTTP {exc.code}: {body[:500]}",
                metadata={"parser_backend": "mineru_cloud", "mineru_raw_dir": str(raw_dir)},
            )
        except Exception as exc:
            return ParseResult(
                status=ParseStatus.FAILED,
                error=f"MinerU cloud invocation failed: {exc}",
                metadata={"parser_backend": "mineru_cloud", "mineru_raw_dir": str(raw_dir)},
            )
