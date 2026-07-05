from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .security import ensure_within_base, resolve_user_id, validate_safe_id


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_USERS_DIR = ROOT / "data" / "users"
SYSTEM_LIBRARY_DIRNAME = "system_library"
QUESTION_STATE_FILENAME = "question_states.jsonl"
MASTERY_STATUSES = {"not_started", "learning", "mastered"}


class UserSystemQuestionStateStore:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = Path(base_dir) if base_dir is not None else DEFAULT_USERS_DIR

    def get_question_state(self, user_id: str, question_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_question_id = self._resolve_question_id(question_id)
        persisted = self._read_states(safe_user_id).get(safe_question_id)
        return self._state_with_defaults(safe_user_id, safe_question_id, persisted)

    def list_question_states(self, user_id: str, question_ids: list[str]) -> dict[str, dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        persisted = self._read_states(safe_user_id)
        states: dict[str, dict[str, Any]] = {}
        for question_id in question_ids:
            safe_question_id = self._resolve_question_id(question_id)
            states[safe_question_id] = self._state_with_defaults(
                safe_user_id,
                safe_question_id,
                persisted.get(safe_question_id),
            )
        return states

    def update_question_state(
        self,
        user_id: str,
        question_id: str,
        patch: dict[str, Any],
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_question_id = self._resolve_question_id(question_id)
        states = self._read_states(safe_user_id)
        state = self._state_with_defaults(safe_user_id, safe_question_id, states.get(safe_question_id))
        state.update(self._normalize_patch(patch))
        state["user_id"] = safe_user_id
        state["question_id"] = safe_question_id
        if self._is_default_state(state):
            states.pop(safe_question_id, None)
            self._write_states(safe_user_id, states)
            return self._default_state(safe_user_id, safe_question_id)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        states[safe_question_id] = state
        self._write_states(safe_user_id, states)
        return dict(state)

    def _resolve_question_id(self, question_id: str) -> str:
        return validate_safe_id(question_id, "question_id")

    def _state_path(self, safe_user_id: str) -> Path:
        user_dir = ensure_within_base(
            self.base_dir,
            self.base_dir / safe_user_id / SYSTEM_LIBRARY_DIRNAME,
        )
        return user_dir / QUESTION_STATE_FILENAME

    def _default_state(self, safe_user_id: str, safe_question_id: str) -> dict[str, Any]:
        return {
            "user_id": safe_user_id,
            "question_id": safe_question_id,
            "mastery_status": "not_started",
            "is_favorite": False,
            "in_wrong_book": False,
            "personal_note": "",
            "last_practiced_at": None,
            "review_due_at": None,
            "updated_at": None,
        }

    def _state_with_defaults(
        self,
        safe_user_id: str,
        safe_question_id: str,
        persisted: dict[str, Any] | None,
    ) -> dict[str, Any]:
        state = self._default_state(safe_user_id, safe_question_id)
        if persisted:
            state.update({key: value for key, value in persisted.items() if key in state})
        state["user_id"] = safe_user_id
        state["question_id"] = safe_question_id
        return state

    def _read_states(self, safe_user_id: str) -> dict[str, dict[str, Any]]:
        path = self._state_path(safe_user_id)
        if not path.exists():
            return {}

        states: dict[str, dict[str, Any]] = {}
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(row, dict):
                    continue
                question_id = row.get("question_id")
                if not isinstance(question_id, str):
                    continue
                try:
                    safe_question_id = self._resolve_question_id(question_id)
                except ValueError:
                    continue
                states[safe_question_id] = self._state_with_defaults(safe_user_id, safe_question_id, row)
        return states

    def _write_states(self, safe_user_id: str, states: dict[str, dict[str, Any]]) -> None:
        path = self._state_path(safe_user_id)
        if not states:
            if path.exists():
                path.unlink()
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            json.dumps(states[question_id], ensure_ascii=False, sort_keys=True)
            for question_id in sorted(states)
        ]
        path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    def _is_default_state(self, state: dict[str, Any]) -> bool:
        return (
            state.get("mastery_status") == "not_started"
            and state.get("is_favorite") is False
            and state.get("in_wrong_book") is False
            and state.get("personal_note") == ""
            and state.get("last_practiced_at") is None
            and state.get("review_due_at") is None
        )

    def _normalize_patch(self, patch: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(patch, dict):
            raise ValueError("state patch must be a JSON object")

        normalized: dict[str, Any] = {}
        if "mastery_status" in patch:
            mastery_status = str(patch["mastery_status"])
            if mastery_status not in MASTERY_STATUSES:
                raise ValueError("invalid mastery_status")
            normalized["mastery_status"] = mastery_status
        if "is_favorite" in patch:
            normalized["is_favorite"] = self._normalize_bool(patch["is_favorite"])
        if "in_wrong_book" in patch:
            normalized["in_wrong_book"] = self._normalize_bool(patch["in_wrong_book"])
        if "personal_note" in patch:
            normalized["personal_note"] = str(patch["personal_note"] or "")
        if "last_practiced_at" in patch:
            normalized["last_practiced_at"] = self._normalize_optional_string(patch["last_practiced_at"])
        if "review_due_at" in patch:
            normalized["review_due_at"] = self._normalize_optional_string(patch["review_due_at"])
        return normalized

    def _normalize_bool(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().casefold() in {"1", "true", "yes", "on"}
        return bool(value)

    def _normalize_optional_string(self, value: Any) -> str | None:
        if value in (None, ""):
            return None
        return str(value)
