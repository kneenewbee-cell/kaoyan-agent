from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import unquote

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from materials.system_library import SystemQuestionLibrary
from materials.tools import get_current_user_id
from materials.user_state import UserSystemQuestionStateStore

from .service import normalize_tutor_history, stream_system_question_tutor


router = APIRouter(prefix="/api/qa/system-questions", tags=["system-question-tutor"])

SYSTEM_ASSET_URL_PATTERN = re.compile(r"^/api/materials/system/assets/([^/]+)/(\d+)/(.+)$")


def _resolve_user_id(request: Request, explicit_user_id: str | None = None) -> str:
    try:
        return get_current_user_id(explicit_user_id or request.headers.get("X-User-Id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _parse_optional_json_array(raw_value: str | None, field_name: str) -> list[Any]:
    if raw_value in (None, ""):
        return []
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"{field_name} must be valid JSON") from exc
    if not isinstance(value, list):
        raise HTTPException(status_code=400, detail=f"{field_name} must be a JSON array")
    return value


def _system_question_asset_paths(library: SystemQuestionLibrary, detail: dict[str, Any]) -> list[Path]:
    urls = {str(url) for url in detail.get("asset_urls") or [] if str(url).strip()}
    for markdown_field in ("question_markdown", "answer_markdown", "explanation_markdown"):
        markdown = str(detail.get(markdown_field) or "")
        for match in re.finditer(r"!\[[^\]\n]*]\((/api/materials/system/assets/[^)\s]+)[^)]*\)", markdown):
            urls.add(match.group(1))

    paths: list[Path] = []
    seen: set[Path] = set()
    for url in sorted(urls):
        match = SYSTEM_ASSET_URL_PATTERN.match(url)
        if not match:
            continue
        exam_type, year_text, asset_path = match.groups()
        try:
            path = library.asset_path(exam_type, int(year_text), unquote(asset_path))
        except (FileNotFoundError, ValueError):
            continue
        if path not in seen:
            seen.add(path)
            paths.append(path)
    return paths


def _sse_data(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


@router.post("/{question_id}/tutor/stream")
async def stream_system_question_tutor_endpoint(
    question_id: str,
    request: Request,
    message: Annotated[str, Form()],
    history: Annotated[str | None, Form()] = None,
    user_id: str | None = Query(None),
) -> StreamingResponse:
    uid = _resolve_user_id(request, user_id)
    library = SystemQuestionLibrary()
    try:
        detail = library.get_question(question_id)
    except (FileNotFoundError, KeyError) as exc:
        raise HTTPException(status_code=404, detail="System question not found") from exc

    parsed_history = normalize_tutor_history(_parse_optional_json_array(history, "history"))
    personal_state = UserSystemQuestionStateStore().get_question_state(uid, question_id)
    image_paths = _system_question_asset_paths(library, detail)

    def event_stream():
        try:
            for chunk in stream_system_question_tutor(
                question=detail,
                personal_state=personal_state,
                user_message=message,
                history=parsed_history,
                image_paths=image_paths,
            ):
                yield f"data: {_sse_data(chunk)}\n\n"
        except Exception as exc:
            yield f"event: error\ndata: {_sse_data(str(exc))}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
