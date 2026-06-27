from __future__ import annotations

import time
import uuid
from copy import deepcopy
from threading import RLock
from typing import Any


TERMINAL_STATUSES = {"completed", "failed"}


STAGE_PROGRESS: dict[str, tuple[int, str]] = {
    "upload": (2, "上传文件"),
    "ingest": (5, "准备入库"),
    "resolve_upload": (7, "识别上传内容"),
    "detect_file": (10, "检测文件类型"),
    "create_material_dir": (12, "创建资料目录"),
    "save_original": (15, "保存原始文件"),
    "parse": (35, "解析为 Markdown"),
    "formula_clean": (45, "保护公式内容"),
    "layout_sidecar": (48, "读取版面信息"),
    "asset_rewrite": (52, "整理图片资源"),
    "raw_markdown_cleaning": (65, "清洗 Markdown"),
    "table_markdown_replace": (72, "整理表格"),
    "write_clean_artifacts": (76, "写入清洗结果"),
    "metadata_infer": (80, "识别资料信息"),
    "chunk": (86, "切分知识片段"),
    "save_chunks": (90, "保存分块"),
    "index": (94, "写入检索索引"),
    "quality_report": (97, "生成质量报告"),
    "save_manifest": (98, "更新资料状态"),
}


def _now() -> float:
    return time.time()


def _new_job_id() -> str:
    return f"job_{uuid.uuid4().hex[:16]}"


def _stage_message(stage: str, status: str, label: str) -> str:
    if status == "started":
        return f"正在{label}"
    if status == "failed":
        return f"{label}失败"
    if stage == "ingest" and status == "completed":
        return "入库完成"
    return f"{label}完成"


class UploadJobStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._jobs: dict[str, dict[str, Any]] = {}

    def create(self, *, filename: str, user_id: str) -> dict[str, Any]:
        now = _now()
        job = {
            "job_id": _new_job_id(),
            "filename": filename,
            "user_id": user_id,
            "status": "queued",
            "stage": "upload",
            "stage_label": "上传文件",
            "message": "上传文件已接收，等待处理",
            "progress": 2,
            "material_id": None,
            "result": None,
            "error": None,
            "events": [],
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
        }
        with self._lock:
            self._jobs[job["job_id"]] = job
            return deepcopy(job)

    def get(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            return deepcopy(job) if job else None

    def update(
        self,
        job_id: str,
        *,
        status: str | None = None,
        stage: str | None = None,
        message: str | None = None,
        progress: int | None = None,
        material_id: str | None = None,
        result: dict[str, Any] | None = None,
        error: str | None = None,
        event: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None

            if stage:
                job["stage"] = stage
                base_progress, label = STAGE_PROGRESS.get(stage, (job.get("progress", 0), stage))
                job["stage_label"] = label
                if progress is None:
                    progress = base_progress
            if status:
                job["status"] = status
            if progress is not None:
                job["progress"] = max(int(job.get("progress", 0)), min(max(int(progress), 0), 100))
            if message is not None:
                job["message"] = message
            if material_id:
                job["material_id"] = material_id
            if result is not None:
                job["result"] = result
            if error is not None:
                job["error"] = error
            if event is not None:
                job["events"].append(event)
                job["events"] = job["events"][-60:]
            if job.get("status") in TERMINAL_STATUSES and job.get("completed_at") is None:
                job["completed_at"] = _now()
            job["updated_at"] = _now()
            return deepcopy(job)

    def apply_pipeline_event(self, job_id: str, event: dict[str, Any]) -> None:
        stage = str(event.get("stage") or "")
        event_status = str(event.get("status") or "completed")
        if not stage:
            return
        label = STAGE_PROGRESS.get(stage, (0, stage))[1]
        job_status = "processing"
        progress = STAGE_PROGRESS.get(stage, (0, label))[0]
        if stage == "save_manifest":
            progress = 13 if event.get("phase") == "initial" else 98
        if stage == "ingest" and event_status == "completed":
            job_status = "completed"
            progress = 100
        elif event_status == "failed":
            job_status = "failed"

        self.update(
            job_id,
            status=job_status,
            stage=stage,
            progress=progress,
            material_id=event.get("material_id"),
            message=_stage_message(stage, event_status, label),
            event={
                "stage": stage,
                "status": event_status,
                "message": _stage_message(stage, event_status, label),
                "progress": progress,
                "duration_ms": event.get("duration_ms"),
                "chunk_count": event.get("chunk_count") or event.get("total_chunk_count"),
                "quality_status": event.get("quality_status"),
                "warnings": event.get("warnings"),
                "updated_at": _now(),
            },
        )


UPLOAD_JOBS = UploadJobStore()
