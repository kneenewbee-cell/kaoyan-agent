from __future__ import annotations

import queue
import shutil
import sys
import threading
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
UPLOAD_DIR = ROOT / "data" / "runtime" / "uploads"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa.kaoyan_agent import (  # noqa: E402
    load_session,
    safe_session_id,
    save_session,
    session_vector_path,
    session_path,
)
from qa.agent_runtime import iter_text_chunks, md_session_path, run_standard_message_loop  # noqa: E402

app = FastAPI(title="Kaoyan Assistant")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


def session_summary(path: Path) -> dict:
    session_id = path.stem
    data = load_session(session_id)
    turns = data.get("turns", [])
    last_turn = turns[-1] if turns else {}
    memory = last_turn.get("memory", {}) if isinstance(last_turn, dict) else {}
    return {
        "id": safe_session_id(session_id),
        "turn_count": len(turns),
        "updated_at": data.get("updated_at") or last_turn.get("time") or "",
        "title": memory.get("topic") or last_turn.get("user_query") or safe_session_id(session_id),
    }


@app.get("/api/sessions")
def list_sessions() -> dict:
    session_dir = session_path("default").parent
    session_dir.mkdir(parents=True, exist_ok=True)
    sessions = [session_summary(path) for path in session_dir.glob("*.json")]
    if not any(item["id"] == "default" for item in sessions):
        sessions.append({"id": "default", "turn_count": 0, "updated_at": "", "title": "default"})
    sessions.sort(key=lambda item: (item.get("updated_at") or "", item["id"]), reverse=True)
    return {"sessions": sessions}


@app.post("/api/sessions")
async def create_session(session: Annotated[str, Form()]) -> dict:
    session_id = safe_session_id(session)
    if not session_id:
        raise HTTPException(status_code=400, detail="会话名不能为空")
    path = session_path(session_id)
    if path.exists():
        raise HTTPException(status_code=409, detail="会话已存在")
    save_session(session_id, {"session_id": session_id, "turns": []})
    return {"session": session_summary(path)}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    clean_id = safe_session_id(session_id)
    data = load_session(clean_id)
    messages = []
    for turn in data.get("turns", []):
        user_query = turn.get("user_query")
        if user_query:
            messages.append({"role": "user", "content": user_query})
        assistant_answer = turn.get("assistant_answer") or turn.get("assistant_answer_preview")
        if assistant_answer:
            messages.append({"role": "assistant", "content": assistant_answer})
    return {
        "session": session_summary(session_path(clean_id)) if session_path(clean_id).exists() else {
            "id": clean_id,
            "turn_count": len(data.get("turns", [])),
            "updated_at": data.get("updated_at") or "",
            "title": clean_id,
        },
        "messages": messages,
    }


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str) -> dict:
    clean_id = safe_session_id(session_id)
    if clean_id == "default":
        save_session("default", {"session_id": "default", "turns": []})
        vector_path = session_vector_path("default")
        if vector_path.exists():
            shutil.rmtree(vector_path)
        md_path = md_session_path("default")
        if md_path.exists():
            md_path.unlink()
        return {"deleted": False, "cleared": True, "session": "default"}
    path = session_path(clean_id)
    if path.exists():
        path.unlink()
    vector_path = session_vector_path(clean_id)
    if vector_path.exists():
        shutil.rmtree(vector_path)
    md_path = md_session_path(clean_id)
    if md_path.exists():
        md_path.unlink()
    return {"deleted": True, "session": clean_id}


@app.post("/api/chat")
async def chat(
    message: Annotated[str, Form()],
    session: Annotated[str, Form()] = "default",
    output_format: Annotated[str, Form()] = "ui",
    debug: Annotated[bool, Form()] = False,
    images: Annotated[list[UploadFile] | None, File()] = None,
) -> dict:
    image_paths: list[Path] = []
    if images:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for index, image in enumerate(images, start=1):
            suffix = Path(image.filename or f"image_{index}.png").suffix or ".png"
            target = UPLOAD_DIR / f"{session}_{index}_{Path(image.filename or 'image').stem}{suffix}"
            with target.open("wb") as file:
                shutil.copyfileobj(image.file, file)
            image_paths.append(target)

    result = run_standard_message_loop(
        message,
        session_id=session,
        image_paths=image_paths,
        output_format=output_format,
        persist=True,
    )
    payload = {
        "answer": result.answer,
        "route": {"subject": result.subject, "intent": "tool_loop"},
        "session": session,
    }
    if debug:
        payload["metrics"] = result.metrics
        payload["tool_calls"] = result.tool_calls
    return payload


@app.post("/api/chat/stream")
async def chat_stream(
    message: Annotated[str, Form()],
    session: Annotated[str, Form()] = "default",
    output_format: Annotated[str, Form()] = "ui",
    images: Annotated[list[UploadFile] | None, File()] = None,
) -> StreamingResponse:
    image_paths: list[Path] = []
    if images:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for index, image in enumerate(images, start=1):
            suffix = Path(image.filename or f"image_{index}.png").suffix or ".png"
            target = UPLOAD_DIR / f"{session}_{index}_{Path(image.filename or 'image').stem}{suffix}"
            with target.open("wb") as file:
                shutil.copyfileobj(image.file, file)
            image_paths.append(target)

    def event_stream():
        progress_queue: queue.Queue[dict | object] = queue.Queue()
        done = object()
        output: dict[str, object] = {}

        def push_progress(event: dict) -> None:
            progress_queue.put(event)

        def worker() -> None:
            try:
                output["result"] = run_standard_message_loop(
                    message,
                    session_id=session,
                    image_paths=image_paths,
                    output_format=output_format,
                    persist=True,
                    progress_callback=push_progress,
                )
            except Exception as exc:
                output["error"] = exc
            finally:
                progress_queue.put(done)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        yield f"event: progress\ndata: {json_escape({'type': 'start', 'label': '已收到问题，开始处理'})}\n\n"

        while True:
            item = progress_queue.get()
            if item is done:
                break
            yield f"event: progress\ndata: {json_escape(item)}\n\n"

        error = output.get("error")
        if error is not None:
            answer = f"请求处理失败：{error}"
        else:
            answer = output["result"].answer  # type: ignore[union-attr]
        for chunk in iter_text_chunks(answer):
            yield f"data: {json_escape(chunk)}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def json_escape(value) -> str:
    import json

    return json.dumps(value, ensure_ascii=False)
