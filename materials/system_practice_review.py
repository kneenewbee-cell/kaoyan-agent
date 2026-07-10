from __future__ import annotations

import hashlib
import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import user_state
from .security import ensure_within_base, resolve_user_id, validate_safe_id
from .system_practice_ai_grader import grade_practice_item_with_ai
from .system_library import SystemQuestionLibrary


PRACTICE_SET_FILENAME = "practice_sets.jsonl"
PRACTICE_ATTEMPT_FILENAME = "practice_attempts.jsonl"
PRACTICE_ATTEMPT_ITEM_FILENAME = "practice_attempt_items.jsonl"
USER_QUESTION_STATS_FILENAME = "user_question_stats.jsonl"
USER_TOPIC_STATS_FILENAME = "user_topic_stats.jsonl"
REVIEW_TASK_FILENAME = "review_tasks.jsonl"
PRACTICE_SET_STATUSES = {"active", "archived"}
PRACTICE_ATTEMPT_STATUSES = {"draft", "submitted", "submit_failed", "abandoned"}
PRACTICE_ANSWER_TYPES = {"choice", "blank", "solution"}
PRACTICE_FINAL_STATUSES = {"correct", "incorrect", "partial", "pending_review", "unanswered"}
PRACTICE_JUDGE_METHODS = {"local", "ai", "manual"}
REVIEW_TARGET_TYPES = {"question", "practice_set", "knowledge_point"}
REVIEW_TASK_STATUSES = {"pending", "completed", "cancelled"}
PRACTICE_SOURCE_SCOPES = {"exam_type", "same_library", "same_year", "subject"}
MATH_SUBJECT_ALIASES = {
    "math",
    "数学",
    "数学一",
    "数学二",
    "数学三",
    "高数",
    "高等数学",
    "线代",
    "线性代数",
    "概率",
    "概率论",
    "概率统计",
    "概率论与数理统计",
}
QUESTION_TYPE_DISPLAY_ORDER = {
    "single_choice": 0,
    "multiple_choice": 0,
    "choice": 0,
    "fill_blank": 1,
    "blank": 1,
    "solution": 2,
}
DEFAULT_PRACTICE_RANKING_PRESET = "topic_first_v2"
PRACTICE_RANKING_PRESETS: dict[str, dict[str, int]] = {
    "legacy_linear": {
        "topic": 100,
        "type": 20,
        "library": 10,
    },
    "type_heavy": {
        "topic": 60,
        "type": 70,
        "library": 10,
    },
    "topic_first_v2": {
        "topic": 100,
        "all_topic_bonus": 35,
        "missing_topic_penalty": 15,
        "extra_topic_penalty": 20,
        "type": 18,
        "library": 8,
    },
}
LEARNING_PRIORITY_WEIGHTS: dict[str, float] = {
    "risk_confidence": 0.5928,
    "recent_risk": 0.0829,
    "wrong_streak": 0.0794,
    "pending_review": 0.0616,
    "repeated_skip": 0.0679,
    "unstarted_not_mastered": 0.0466,
    "manual_signal": 0.0582,
    "question_importance": 0.0106,
}
LEARNING_PRIORITY_RELIEF_SINGLE_CORRECT = 0.9616
LEARNING_PRIORITY_RELIEF_STABLE_CORRECT = 0.7030
LEARNING_PRIORITY_SKIP_ONLY_CAP = 0.4984
LEARNING_PRIORITY_UNSTARTED_ONLY_CAP = 0.4588
LEARNING_PRIORITY_MANUAL_CAP_ADD = 0.0999


class SystemPracticeReviewStore:
    def __init__(
        self,
        users_dir: Path | None = None,
        library: SystemQuestionLibrary | None = None,
        state_store: user_state.UserSystemQuestionStateStore | None = None,
    ) -> None:
        self.users_dir = Path(users_dir) if users_dir is not None else user_state.DEFAULT_USERS_DIR
        self.library = library or SystemQuestionLibrary()
        self.state_store = state_store or user_state.UserSystemQuestionStateStore(base_dir=self.users_dir)

    def create_practice_set(
        self,
        user_id: str,
        *,
        source_question_id: str,
        count: int = 5,
        same_type_only: bool = False,
        exclude_mastered: bool = True,
        topic_filters: list[str] | None = None,
        source_scope: str = "exam_type",
        title: str | None = None,
        subject: str = "math",
        exam_type: str = "math1",
    ) -> dict[str, Any]:
        preview = self.preview_practice_candidates(
            user_id,
            source_question_id=source_question_id,
            count=count,
            same_type_only=same_type_only,
            exclude_mastered=exclude_mastered,
            topic_filters=topic_filters,
            source_scope=source_scope,
            subject=subject,
            exam_type=exam_type,
        )
        safe_user_id = str(preview["user_id"])
        safe_source_id = str(preview["source_question_id"])
        source = dict(preview["source_question"])
        ranked = list(preview["items"])
        criteria = dict(preview["criteria"])
        display_items = self._practice_set_display_order(ranked)
        question_ids = [str(item["question_id"]) for item in display_items]
        now = self._utc_now()
        practice_set = {
            "set_id": self._new_id("ps"),
            "user_id": safe_user_id,
            "source_question_id": safe_source_id,
            "question_ids": question_ids,
            "matching_topics": criteria.get("topic_filters") or self._matching_topics(source, ranked),
            "title": self._clean_string(title) or f"Similar practice for {safe_source_id}",
            "created_at": now,
            "status": "active",
            "subject": subject,
            "exam_type": exam_type,
            "library_name": str(source.get("library_name") or ""),
            "criteria": criteria,
        }
        records = self._read_records(safe_user_id, PRACTICE_SET_FILENAME, "set_id")
        records.append(practice_set)
        self._write_records(safe_user_id, PRACTICE_SET_FILENAME, records)
        return dict(practice_set)

    def list_wrong_question_pool(
        self,
        user_id: str,
        *,
        subject: str = "math",
        exam_type: str = "",
        topic: str | None = None,
        question_type: str | None = None,
        risk_type: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        normalized_subject = self._clean_string(subject) or "math"
        normalized_exam_type = self._clean_string(exam_type)
        normalized_topic = self._optional_string(topic)
        normalized_question_type = self._optional_string(question_type)
        normalized_risk_type = self._normalize_wrong_pool_risk_type(risk_type)
        safe_limit = max(1, min(int(limit or 50), 200))
        _, questions = self.library.list_all_questions(subject=normalized_subject, exam_type=normalized_exam_type)
        by_question_id = {str(item.get("question_id") or ""): item for item in questions if item.get("question_id")}
        stats = self._read_records(safe_user_id, USER_QUESTION_STATS_FILENAME, "question_id")
        if not any(self._question_stat_risk_count(stat) > 0 for stat in stats):
            attempt_items = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
            if attempt_items:
                self.rebuild_user_learning_stats(safe_user_id)
                stats = self._read_records(safe_user_id, USER_QUESTION_STATS_FILENAME, "question_id")
        states = self.state_store.list_question_states(safe_user_id, list(by_question_id))
        items: list[dict[str, Any]] = []
        topic_options: set[str] = set()
        question_type_options: set[str] = set()
        for stat in stats:
            question_id = str(stat.get("question_id") or "")
            question = by_question_id.get(question_id)
            if not question:
                continue
            question_topics = [str(value).strip() for value in question.get("topics") or stat.get("topics") or [] if str(value).strip()]
            topic_options.update(question_topics)
            question_type_value = str(question.get("question_type") or "")
            if question_type_value:
                question_type_options.add(question_type_value)
            if normalized_topic and normalized_topic not in question_topics:
                continue
            if normalized_question_type and question_type_value != normalized_question_type:
                continue
            pool_item = self._wrong_question_pool_item(
                safe_user_id,
                question,
                stat,
                states.get(question_id, {}),
            )
            if int(pool_item.get("risk_count") or 0) <= 0:
                continue
            items.append(pool_item)
        risk_type_options = self._wrong_pool_risk_type_options(items)
        if normalized_risk_type:
            items = [
                item
                for item in items
                if self._wrong_pool_matches_risk_type(item, normalized_risk_type)
            ]
        items.sort(
            key=lambda item: (
                -float(item.get("priority_score") or 0),
                -int(item.get("risk_count") or 0),
                self._question_type_display_rank(item),
                -(int(item.get("year") or 0)),
                int(item.get("question_number") or 0),
                str(item.get("question_id") or ""),
            )
        )
        limited_items = items[:safe_limit]
        return {
            "user_id": safe_user_id,
            "subject": normalized_subject,
            "exam_type": normalized_exam_type,
            "filters": {
                "topic": normalized_topic or "",
                "question_type": normalized_question_type or "",
                "risk_type": normalized_risk_type or "",
                "limit": safe_limit,
            },
            "total": len(items),
            "items": [dict(item) for item in limited_items],
            "default_selected_question_ids": [str(item["question_id"]) for item in limited_items[:5]],
            "topic_options": sorted(topic_options),
            "question_type_options": sorted(question_type_options),
            "risk_type_options": risk_type_options,
            "feedback_hook": "wrong_pool_review_v1",
        }

    def list_pending_review_items(
        self,
        user_id: str,
        *,
        subject: str = "math",
        exam_type: str = "",
        topic: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        normalized_subject = self._clean_string(subject) or "math"
        normalized_exam_type = self._clean_string(exam_type)
        normalized_topic = self._optional_string(topic)
        safe_limit = max(1, min(int(limit or 50), 200))
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        pending_items: list[dict[str, Any]] = []
        topic_options: set[str] = set()
        for record in records:
            final_status = str(record.get("final_status") or record.get("status") or "")
            if final_status != "pending_review":
                continue
            source_meta = record.get("source_meta") if isinstance(record.get("source_meta"), dict) else {}
            record_subject = str(source_meta.get("subject") or "math")
            record_exam_type = str(source_meta.get("exam_type") or "")
            if not self._matches_subject_filter(record_subject, normalized_subject, exam_type=record_exam_type):
                continue
            if normalized_exam_type and record_exam_type != normalized_exam_type:
                continue
            question_id = str(record.get("question_id") or "")
            question: dict[str, Any] = {}
            try:
                question = self.library.get_question(question_id)
            except (KeyError, ValueError):
                question = {}
            answer_type = str(record.get("answer_type") or self._question_answer_type(question) or "")
            question_type = str(record.get("question_type") or question.get("question_type") or "")
            if self._is_choice_pending_review_item(answer_type, question_type):
                continue
            topics = [
                str(value).strip()
                for value in (question.get("topics") or record.get("topics") or [])
                if str(value).strip()
            ]
            topic_options.update(topics)
            if normalized_topic and normalized_topic not in topics:
                continue
            enriched = {
                **dict(record),
                "question_id": question_id,
                "question_title": str(record.get("question_title") or self._question_title(question) or question_id),
                "question_type": question_type,
                "question_type_label": str(question.get("question_type_label") or ""),
                "answer_type": answer_type,
                "topics": topics,
                "source_meta": {
                    **source_meta,
                    "subject": record_subject,
                    "exam_type": record_exam_type,
                    "library_name": str(source_meta.get("library_name") or question.get("library_name") or ""),
                    "year": source_meta.get("year") or question.get("year"),
                    "question_number": source_meta.get("question_number") or question.get("question_number"),
                },
                "preview": str(question.get("preview") or ""),
            }
            pending_items.append(enriched)
        pending_items.sort(
            key=lambda item: (
                str(item.get("graded_at") or item.get("submitted_at") or ""),
                str(item.get("question_id") or ""),
            ),
            reverse=True,
        )
        question_level_items: list[dict[str, Any]] = []
        seen_question_ids: set[str] = set()
        for item in pending_items:
            question_id = str(item.get("question_id") or "")
            if question_id in seen_question_ids:
                continue
            seen_question_ids.add(question_id)
            question_level_items.append(item)
        return {
            "user_id": safe_user_id,
            "subject": normalized_subject,
            "exam_type": normalized_exam_type,
            "filters": {
                "topic": normalized_topic or "",
                "limit": safe_limit,
            },
            "total": len(question_level_items),
            "items": [dict(item) for item in question_level_items[:safe_limit]],
            "topic_options": sorted(topic_options),
            "feedback_hook": "pending_review_question_items_v1",
        }

    def create_practice_set_from_wrong_pool(
        self,
        user_id: str,
        *,
        question_ids: list[str],
        title: str | None = None,
        subject: str = "math",
        exam_type: str = "",
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        normalized_subject = self._clean_string(subject) or "math"
        normalized_exam_type = self._clean_string(exam_type)
        if not isinstance(question_ids, list) or not question_ids:
            raise ValueError("question_ids must be a non-empty list")
        selected_ids: list[str] = []
        seen_ids: set[str] = set()
        for raw_question_id in question_ids:
            question_id = validate_safe_id(str(raw_question_id), "question_id")
            if question_id in seen_ids:
                continue
            selected_ids.append(question_id)
            seen_ids.add(question_id)
        if not selected_ids:
            raise ValueError("question_ids must be a non-empty list")
        if len(selected_ids) > 50:
            raise ValueError("question_ids cannot exceed 50")
        _, all_items = self.library.list_all_questions(subject=normalized_subject, exam_type=normalized_exam_type)
        by_question_id = {str(item.get("question_id") or ""): item for item in all_items if item.get("question_id")}
        missing_ids = [question_id for question_id in selected_ids if question_id not in by_question_id]
        if missing_ids:
            raise KeyError(f"system question not found: {missing_ids[0]}")
        selected_items = self._practice_set_display_order([dict(by_question_id[question_id]) for question_id in selected_ids])
        display_question_ids = [str(item["question_id"]) for item in selected_items]
        libraries = {str(item.get("library_name") or "") for item in selected_items if item.get("library_name")}
        library_name = next(iter(libraries)) if len(libraries) == 1 else "错题池"
        matching_topics = self._union_topics(selected_items)
        now = self._utc_now()
        criteria_filters = filters if isinstance(filters, dict) else {}
        practice_set = {
            "set_id": self._new_id("ps"),
            "user_id": safe_user_id,
            "source_question_id": "",
            "source_type": "wrong_pool",
            "question_ids": display_question_ids,
            "question_count": len(display_question_ids),
            "matching_topics": matching_topics,
            "title": self._clean_string(title) or "错题复习练习单",
            "created_at": now,
            "status": "active",
            "subject": normalized_subject,
            "exam_type": normalized_exam_type,
            "library_name": library_name,
            "criteria": {
                "source": "wrong_pool",
                "selected_question_ids": display_question_ids,
                "filters": criteria_filters,
                "feedback_hook": "wrong_pool_review_v1",
            },
        }
        records = self._read_records(safe_user_id, PRACTICE_SET_FILENAME, "set_id")
        records.append(practice_set)
        self._write_records(safe_user_id, PRACTICE_SET_FILENAME, records)
        return dict(practice_set)

    def preview_practice_candidates(
        self,
        user_id: str,
        *,
        source_question_id: str,
        count: int = 5,
        same_type_only: bool = False,
        exclude_mastered: bool = True,
        topic_filters: list[str] | None = None,
        source_scope: str = "exam_type",
        subject: str = "math",
        exam_type: str = "math1",
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_source_id = validate_safe_id(source_question_id, "source_question_id")
        normalized_count = self._normalize_count(count)
        normalized_topic_filters = self._normalize_topic_filters(topic_filters)
        normalized_source_scope = self._normalize_source_scope(source_scope)
        _, items = self.library.list_all_questions(subject=subject, exam_type=exam_type)
        source = self._find_question(items, safe_source_id)
        if source is None:
            raise KeyError(f"system question not found: {safe_source_id}")

        ranked = self._rank_similar_questions(
            safe_user_id,
            source,
            items,
            count=normalized_count,
            same_type_only=same_type_only,
            exclude_mastered=exclude_mastered,
            topic_filters=normalized_topic_filters,
            source_scope=normalized_source_scope,
        )
        return {
            "user_id": safe_user_id,
            "source_question_id": safe_source_id,
            "source_question": dict(source),
            "total": len(ranked),
            "items": [dict(item) for item in ranked],
            "criteria": {
                "count": normalized_count,
                "same_type_only": bool(same_type_only),
                "exclude_mastered": bool(exclude_mastered),
                "topic_filters": normalized_topic_filters,
                "source_scope": normalized_source_scope,
            },
        }

    def list_practice_sets(self, user_id: str, status: str | None = None) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        if status is not None and status not in PRACTICE_SET_STATUSES:
            raise ValueError("invalid practice set status")
        records = self._read_records(safe_user_id, PRACTICE_SET_FILENAME, "set_id")
        if status is not None:
            records = [record for record in records if record.get("status") == status]
        return sorted(records, key=lambda record: str(record.get("created_at") or ""), reverse=True)

    def get_practice_set(self, user_id: str, practice_set_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_set_id = validate_safe_id(practice_set_id, "practice_set_id")
        for record in self._read_records(safe_user_id, PRACTICE_SET_FILENAME, "set_id"):
            if record.get("set_id") == safe_set_id:
                return dict(record)
        raise KeyError(f"practice set not found: {safe_set_id}")

    def delete_practice_set(self, user_id: str, practice_set_id: str) -> bool:
        safe_user_id = resolve_user_id(user_id)
        safe_set_id = validate_safe_id(practice_set_id, "practice_set_id")
        records = self._read_records(safe_user_id, PRACTICE_SET_FILENAME, "set_id")
        kept = [record for record in records if record.get("set_id") != safe_set_id]
        if len(kept) == len(records):
            raise KeyError(f"practice set not found: {safe_set_id}")
        self._write_records(safe_user_id, PRACTICE_SET_FILENAME, kept)
        return True

    def create_practice_attempt(self, user_id: str, practice_set_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_set_id = validate_safe_id(practice_set_id, "practice_set_id")
        practice_set = self.get_practice_set(safe_user_id, safe_set_id)
        now = self._utc_now()
        attempt = {
            "attempt_id": self._new_id("pa"),
            "user_id": safe_user_id,
            "practice_set_id": safe_set_id,
            "status": "draft",
            "started_at": now,
            "submitted_at": None,
            "duration_seconds": None,
            "answers": {},
            "results": {},
            "summary": self._empty_attempt_summary(len(practice_set.get("question_ids") or [])),
            "source_meta": self._practice_attempt_source_meta(practice_set),
        }
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        records.append(attempt)
        self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
        return dict(attempt)

    def update_practice_attempt_answers(
        self,
        user_id: str,
        attempt_id: str,
        answers: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(answers, dict):
            raise ValueError("answers must be a JSON object")
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        for index, record in enumerate(records):
            if record.get("attempt_id") != safe_attempt_id:
                continue
            if record.get("status") != "draft":
                raise ValueError("practice attempt is not editable")
            practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
            existing_answers = record.get("answers") if isinstance(record.get("answers"), dict) else {}
            normalized_answers = {
                **existing_answers,
                **self._normalize_practice_answers(answers, practice_set),
            }
            updated = dict(record)
            updated["answers"] = normalized_answers
            records[index] = updated
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def submit_practice_attempt(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        for index, record in enumerate(records):
            if record.get("attempt_id") != safe_attempt_id:
                continue
            if record.get("status") == "submitted":
                submitted = self._backfill_practice_attempt_result(record)
                practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
                self._write_attempt_items_for_attempt(safe_user_id, submitted, practice_set)
                self._mark_answered_questions_learning(safe_user_id, submitted)
                self.rebuild_user_learning_stats(safe_user_id)
                return dict(submitted)
            if record.get("status") != "draft":
                raise ValueError("practice attempt is not submittable")
            practice_set = self.get_practice_set(safe_user_id, str(record.get("practice_set_id") or ""))
            results, summary = self._grade_practice_attempt(practice_set, record.get("answers") or {})
            now = self._utc_now()
            updated = dict(record)
            updated["status"] = "submitted"
            updated["submitted_at"] = now
            updated["duration_seconds"] = self._duration_seconds(str(record.get("started_at") or ""), now)
            updated["results"] = results
            updated["summary"] = summary
            records[index] = updated
            self._write_attempt_items_for_attempt(safe_user_id, updated, practice_set)
            self._mark_answered_questions_learning(safe_user_id, updated)
            self.rebuild_user_learning_stats(safe_user_id)
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def _mark_answered_questions_learning(self, user_id: str, attempt: dict[str, Any]) -> None:
        submitted_at = str(attempt.get("submitted_at") or self._utc_now())
        results = attempt.get("results") if isinstance(attempt.get("results"), dict) else {}
        for question_id, raw_result in results.items():
            if not isinstance(raw_result, dict):
                continue
            final_status = str(
                raw_result.get("final_status")
                or raw_result.get("status")
                or raw_result.get("result")
                or ""
            )
            if final_status == "unanswered":
                continue
            safe_question_id = validate_safe_id(str(question_id), "question_id")
            current = self.state_store.get_question_state(user_id, safe_question_id)
            patch: dict[str, Any] = {"last_practiced_at": submitted_at}
            if current.get("mastery_status") == "not_started":
                patch["mastery_status"] = "learning"
            self.state_store.update_question_state(user_id, safe_question_id, patch)

    def get_practice_attempt(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        for record in self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id"):
            if record.get("attempt_id") == safe_attempt_id:
                return self._backfill_practice_attempt_result(record)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def list_practice_attempt_items(
        self,
        user_id: str,
        *,
        attempt_id: str | None = None,
        question_id: str | None = None,
    ) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id") if attempt_id else None
        safe_question_id = validate_safe_id(question_id, "question_id") if question_id else None
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        if safe_attempt_id:
            records = [record for record in records if record.get("attempt_id") == safe_attempt_id]
        if safe_question_id:
            records = [record for record in records if record.get("question_id") == safe_question_id]
        return sorted(records, key=lambda record: str(record.get("submitted_at") or ""))

    def list_user_question_stats(self, user_id: str) -> dict[str, dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, USER_QUESTION_STATS_FILENAME, "stat_id")
        return {str(record.get("question_id") or record.get("stat_id")): dict(record) for record in records}

    def list_user_topic_stats(self, user_id: str) -> dict[str, dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, USER_TOPIC_STATS_FILENAME, "stat_id")
        return {str(record.get("stat_id")): dict(record) for record in records}

    def build_practice_attempt_insights(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        attempt = self.get_practice_attempt(safe_user_id, safe_attempt_id)
        items = self.list_practice_attempt_items(safe_user_id, attempt_id=safe_attempt_id)
        question_stats = self.list_user_question_stats(safe_user_id)
        topic_stats = self.list_user_topic_stats(safe_user_id)
        summary = dict(attempt.get("summary") or {})
        topic_impacts = self._practice_attempt_topic_impacts(items, topic_stats)
        question_impacts = self._practice_attempt_question_impacts(items, question_stats)
        next_actions = self._practice_attempt_next_actions(summary, topic_impacts)
        return {
            "attempt_id": safe_attempt_id,
            "practice_set_id": attempt.get("practice_set_id"),
            "record_status": "recorded" if items else "missing_items",
            "headline": self._practice_attempt_insight_headline(summary, topic_impacts),
            "summary": summary,
            "topic_impacts": topic_impacts,
            "question_impacts": question_impacts,
            "next_actions": next_actions,
            "recorded_fields": [
                "practice_attempt",
                "practice_attempt_items",
                "question_stats_updated",
                "topic_stats_updated",
            ],
        }

    def build_question_learning_snapshot(self, user_id: str, question_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_question_id = validate_safe_id(question_id, "question_id")
        stats = self.list_user_question_stats(safe_user_id).get(safe_question_id, {})
        items = self.list_practice_attempt_items(safe_user_id, question_id=safe_question_id)
        recent_items = sorted(
            items,
            key=lambda item: str(item.get("submitted_at") or item.get("graded_at") or ""),
            reverse=True,
        )[:5]
        return {
            "question_id": safe_question_id,
            "attempt_count": int(stats.get("attempt_count") or 0),
            "correct_count": int(stats.get("correct_count") or 0),
            "incorrect_count": int(stats.get("incorrect_count") or 0),
            "partial_count": int(stats.get("partial_count") or 0),
            "pending_review_count": int(stats.get("pending_review_count") or 0),
            "unanswered_count": int(stats.get("unanswered_count") or 0),
            "latest_status": str(stats.get("latest_status") or ""),
            "latest_answer": stats.get("latest_answer"),
            "latest_practiced_at": stats.get("latest_practiced_at"),
            "wrong_streak": int(stats.get("wrong_streak") or 0),
            "correct_streak": int(stats.get("correct_streak") or 0),
            "last_wrong_at": stats.get("last_wrong_at"),
            "last_risk_at": stats.get("last_risk_at"),
            "topics": list(stats.get("topics") or []),
            "recent_attempts": [
                {
                    "attempt_id": item.get("attempt_id"),
                    "practice_set_id": item.get("practice_set_id"),
                    "status": item.get("final_status") or item.get("status"),
                    "judge_method": item.get("judge_method"),
                    "submitted_at": item.get("submitted_at"),
                    "user_answer": item.get("user_answer"),
                }
                for item in recent_items
            ],
        }

    def apply_practice_item_grade(
        self,
        user_id: str,
        attempt_id: str,
        question_id: str,
        *,
        judge_method: str,
        final_status: str,
        judge_confidence: float | None = None,
        judge_reason: str | None = None,
        ai_feedback: str | None = None,
        manual_override: bool | None = None,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        safe_question_id = validate_safe_id(question_id, "question_id")
        normalized_method = self._normalize_judge_method(judge_method)
        normalized_status = self._normalize_final_status(final_status)
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        for index, record in enumerate(records):
            if record.get("attempt_id") != safe_attempt_id:
                continue
            if record.get("status") != "submitted":
                raise ValueError("practice attempt is not gradeable")
            results = record.get("results") if isinstance(record.get("results"), dict) else {}
            current_result = results.get(safe_question_id)
            if not isinstance(current_result, dict):
                raise KeyError(f"practice attempt item not found: {safe_question_id}")
            updated_result = dict(current_result)
            updated_result["final_status"] = normalized_status
            updated_result["status"] = normalized_status
            updated_result["judge_method"] = normalized_method
            updated_result["judge_confidence"] = self._normalize_confidence(judge_confidence)
            updated_result["judge_reason"] = self._clean_string(judge_reason)
            updated_result["ai_feedback"] = self._clean_string(ai_feedback)
            updated_result["graded_at"] = self._utc_now()
            if normalized_method == "ai":
                updated_result["ai_status"] = normalized_status
                updated_result["manual_override"] = False
                updated_result["manual_direction"] = ""
                updated_result["manual_conflict"] = False
                updated_result["manual_conflict_sources"] = []
                updated_result["manual_evidence"] = {}
            if normalized_method == "manual" or manual_override is not None:
                updated_result["manual_override"] = bool(manual_override if manual_override is not None else True)
                updated_result.update(self._manual_grade_metadata(updated_result, normalized_status))

            updated_results = dict(results)
            updated_results[safe_question_id] = updated_result
            updated = dict(record)
            updated["results"] = updated_results
            updated["summary"] = self._summarize_practice_results(updated_results, len(updated_results))
            records[index] = updated
            practice_set = self.get_practice_set(safe_user_id, str(updated.get("practice_set_id") or ""))
            self._write_attempt_items_for_attempt(safe_user_id, updated, practice_set)
            self.rebuild_user_learning_stats(safe_user_id)
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def request_practice_item_ai_grade(
        self,
        user_id: str,
        attempt_id: str,
        question_id: str,
        *,
        grader: Any | None = None,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        safe_question_id = validate_safe_id(question_id, "question_id")
        attempt = self.get_practice_attempt(safe_user_id, safe_attempt_id)
        if attempt.get("status") != "submitted":
            raise ValueError("practice attempt is not gradeable")
        results = attempt.get("results") if isinstance(attempt.get("results"), dict) else {}
        current_result = results.get(safe_question_id)
        if not isinstance(current_result, dict):
            raise KeyError(f"practice attempt item not found: {safe_question_id}")
        answers = attempt.get("answers") if isinstance(attempt.get("answers"), dict) else {}
        answer = answers.get(safe_question_id) if isinstance(answers, dict) else {}
        answer_value = self._clean_answer_value(answer.get("value") if isinstance(answer, dict) else current_result.get("user_answer"))
        question = self.library.get_question(safe_question_id)
        context = {
            "question": question,
            "question_title": self._question_title(question),
            "answer_type": current_result.get("answer_type") or self._question_answer_type(question),
            "user_answer": answer_value,
            "standard_answer": current_result.get("standard_answer") or question.get("answer") or question.get("answer_markdown") or "",
            "local_status": current_result.get("local_status") or current_result.get("status") or "",
            "current_result": dict(current_result),
            "attempt_id": safe_attempt_id,
            "question_id": safe_question_id,
        }
        grade_result = (grader or grade_practice_item_with_ai)(context)
        if not isinstance(grade_result, dict):
            raise ValueError("AI grade result must be a JSON object")
        return self.apply_practice_item_grade(
            safe_user_id,
            safe_attempt_id,
            safe_question_id,
            judge_method="ai",
            final_status=str(grade_result.get("final_status") or grade_result.get("status") or "pending_review"),
            judge_confidence=grade_result.get("judge_confidence"),
            judge_reason=grade_result.get("judge_reason"),
            ai_feedback=grade_result.get("ai_feedback"),
        )

    def list_practice_attempts(
        self,
        user_id: str,
        practice_set_id: str | None = None,
    ) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        safe_set_id = validate_safe_id(practice_set_id, "practice_set_id") if practice_set_id else None
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id")
        if safe_set_id is not None:
            records = [record for record in records if record.get("practice_set_id") == safe_set_id]
        normalized_records = [self._backfill_practice_attempt_result(record) for record in records]
        return sorted(normalized_records, key=lambda record: str(record.get("started_at") or ""), reverse=True)

    def create_review_task(
        self,
        user_id: str,
        *,
        target_type: str,
        target_id: str,
        title: str | None = None,
        due_at: str | None = None,
        priority: int = 2,
        note: str | None = None,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        normalized_target_type = self._normalize_target_type(target_type)
        safe_target_id = validate_safe_id(target_id, "target_id")
        source_meta = self._review_target_metadata(safe_user_id, normalized_target_type, safe_target_id)
        normalized_due_at = self._optional_string(due_at)
        records = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        duplicate = self._find_duplicate_review_task(
            records,
            target_type=normalized_target_type,
            target_id=safe_target_id,
            due_at=normalized_due_at,
        )
        if duplicate is not None:
            return {**duplicate, "duplicate": True}
        now = self._utc_now()
        review_task = {
            "task_id": self._new_id("rt"),
            "user_id": safe_user_id,
            "target_type": normalized_target_type,
            "target_id": safe_target_id,
            "title": self._clean_string(title) or source_meta.get("source_title") or f"Review {normalized_target_type} {safe_target_id}",
            "due_at": normalized_due_at,
            "priority": self._normalize_priority(priority),
            "status": "pending",
            "note": self._clean_string(note),
            "subject": source_meta.get("subject") or "",
            "exam_type": source_meta.get("exam_type") or "",
            "library_name": source_meta.get("library_name") or "",
            "source_title": source_meta.get("source_title") or "",
            "source_meta": source_meta,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
            "cancelled_at": None,
        }
        records.append(review_task)
        self._write_records(safe_user_id, REVIEW_TASK_FILENAME, records)
        return {**review_task, "duplicate": False}

    def list_review_tasks(
        self,
        user_id: str,
        status: str | None = None,
        *,
        subject: str | None = None,
        target_type: str | None = None,
        date_group: str | None = None,
        keyword: str | None = None,
    ) -> list[dict[str, Any]]:
        safe_user_id = resolve_user_id(user_id)
        if status is not None and status not in REVIEW_TASK_STATUSES:
            raise ValueError("invalid review task status")
        if target_type is not None:
            target_type = self._normalize_target_type(target_type)
        records = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        if status is not None:
            records = [record for record in records if record.get("status") == status]
        if subject is not None:
            records = [record for record in records if record.get("subject") == subject]
        if target_type is not None:
            records = [record for record in records if record.get("target_type") == target_type]
        if date_group is not None:
            records = [record for record in records if self._review_date_group(record) == date_group]
        if keyword:
            normalized_keyword = str(keyword).strip().lower()
            records = [
                record
                for record in records
                if normalized_keyword in self._review_task_search_text(record).lower()
            ]
        records = [
            {**record, "learning_reasons": self._review_task_learning_reasons(safe_user_id, record)}
            for record in records
        ]
        return sorted(records, key=lambda record: str(record.get("created_at") or ""), reverse=True)

    def review_task_summary(self, user_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        records = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        summary: dict[str, Any] = {
            "total": len(records),
            "by_subject": {},
            "by_target_type": {},
            "by_status": {},
            "by_date_group": {},
        }
        for record in records:
            subject = str(record.get("subject") or "other")
            target_type = str(record.get("target_type") or "unknown")
            status = str(record.get("status") or "pending")
            date_group = self._review_date_group(record)
            summary["by_subject"].setdefault(subject, {"total": 0, "pending": 0, "completed": 0, "cancelled": 0})
            summary["by_subject"][subject]["total"] += 1
            if status in summary["by_subject"][subject]:
                summary["by_subject"][subject][status] += 1
            summary["by_target_type"][target_type] = summary["by_target_type"].get(target_type, 0) + 1
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
            summary["by_date_group"][date_group] = summary["by_date_group"].get(date_group, 0) + 1
        return summary

    def build_learning_insights(
        self,
        user_id: str,
        *,
        subject: str | None = None,
        limit: int = 5,
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        normalized_subject = self._optional_string(subject)
        safe_limit = max(1, min(int(limit or 5), 10))
        items = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        if normalized_subject:
            items = [
                item
                for item in items
                if self._matches_subject_filter(
                    (item.get("source_meta") or {}).get("subject"),
                    normalized_subject,
                    exam_type=(item.get("source_meta") or {}).get("exam_type"),
                )
            ]
        summary = self._learning_items_summary(items)
        topic_stats = list(self.list_user_topic_stats(safe_user_id).values())
        if normalized_subject:
            topic_stats = [stat for stat in topic_stats if self._matches_subject_filter(stat.get("subject"), normalized_subject)]
        review_tasks = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        if normalized_subject:
            review_tasks = [task for task in review_tasks if self._matches_subject_filter(task.get("subject"), normalized_subject)]
        review_summary = self._learning_review_summary(review_tasks)
        weak_topics = self._learning_weak_topics(topic_stats, review_summary, limit=safe_limit)
        next_actions = self._learning_next_actions(summary, weak_topics, review_summary)
        return {
            "user_id": safe_user_id,
            "subject": normalized_subject or "all",
            "summary": summary,
            "review_summary": review_summary,
            "weak_topics": weak_topics,
            "next_actions": next_actions,
            "score_weights": {
                **LEARNING_PRIORITY_WEIGHTS,
                "single_correct_relief": LEARNING_PRIORITY_RELIEF_SINGLE_CORRECT,
                "stable_correct_relief": LEARNING_PRIORITY_RELIEF_STABLE_CORRECT,
                "skip_only_cap": LEARNING_PRIORITY_SKIP_ONLY_CAP,
                "unstarted_only_cap": LEARNING_PRIORITY_UNSTARTED_ONLY_CAP,
            },
        }

    def update_review_task(self, user_id: str, review_task_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(patch, dict):
            raise ValueError("review task patch must be a JSON object")
        safe_user_id = resolve_user_id(user_id)
        safe_task_id = validate_safe_id(review_task_id, "review_task_id")
        records = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        for index, record in enumerate(records):
            if record.get("task_id") != safe_task_id:
                continue
            updated = dict(record)
            if "title" in patch:
                updated["title"] = self._clean_string(patch.get("title"))
            if "due_at" in patch:
                updated["due_at"] = self._optional_string(patch.get("due_at"))
            if "priority" in patch:
                updated["priority"] = self._normalize_priority(patch.get("priority"))
            if "note" in patch:
                updated["note"] = self._clean_string(patch.get("note"))
            if "status" in patch:
                updated["status"] = self._normalize_review_status(patch.get("status"))
                now = self._utc_now()
                updated["completed_at"] = now if updated["status"] == "completed" else None
                updated["cancelled_at"] = now if updated["status"] == "cancelled" else None
            updated["updated_at"] = self._utc_now()
            records[index] = updated
            self._write_records(safe_user_id, REVIEW_TASK_FILENAME, records)
            return dict(updated)
        raise KeyError(f"review task not found: {safe_task_id}")

    def delete_review_task(self, user_id: str, review_task_id: str) -> bool:
        safe_user_id = resolve_user_id(user_id)
        safe_task_id = validate_safe_id(review_task_id, "review_task_id")
        records = self._read_records(safe_user_id, REVIEW_TASK_FILENAME, "task_id")
        kept = [record for record in records if record.get("task_id") != safe_task_id]
        if len(kept) == len(records):
            raise KeyError(f"review task not found: {safe_task_id}")
        self._write_records(safe_user_id, REVIEW_TASK_FILENAME, kept)
        return True

    def evaluate_practice_ranking_presets(
        self,
        user_id: str,
        evaluation_cases: list[dict[str, Any]],
        *,
        subject: str = "math",
        exam_type: str = "math1",
    ) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        if not isinstance(evaluation_cases, list) or not evaluation_cases:
            raise ValueError("evaluation_cases must be a non-empty list")
        preset_names = list(PRACTICE_RANKING_PRESETS)
        aggregate_scores: dict[str, list[float]] = {name: [] for name in preset_names}
        case_results: list[dict[str, Any]] = []
        source_question_ids: set[str] = set()
        labelled_candidate_ids: set[str] = set()
        source_topics: set[str] = set()

        for raw_case in evaluation_cases:
            if not isinstance(raw_case, dict):
                raise ValueError("each evaluation case must be a JSON object")
            source_question_id = validate_safe_id(str(raw_case.get("source_question_id") or ""), "source_question_id")
            relevance = self._normalize_relevance_map(raw_case.get("relevance"))
            count = self._normalize_count(raw_case.get("count", 5))
            same_type_only = bool(raw_case.get("same_type_only", False))
            exclude_mastered = bool(raw_case.get("exclude_mastered", False))
            topic_filters = self._normalize_topic_filters(raw_case.get("topic_filters"))
            source_scope = self._normalize_source_scope(raw_case.get("source_scope", "exam_type"))
            case_subject = str(raw_case.get("subject") or subject)
            case_exam_type = str(raw_case.get("exam_type") or exam_type)
            _, items = self.library.list_all_questions(subject=case_subject, exam_type=case_exam_type)
            source = self._find_question(items, source_question_id)
            if source is None:
                raise KeyError(f"system question not found: {source_question_id}")
            source_question_ids.add(source_question_id)
            labelled_candidate_ids.update(relevance)
            source_topics.update(self._topic_set(source))

            preset_results: dict[str, Any] = {}
            for preset_name in preset_names:
                ranked = self._rank_similar_questions(
                    safe_user_id,
                    source,
                    items,
                    count=count,
                    same_type_only=same_type_only,
                    exclude_mastered=exclude_mastered,
                    topic_filters=topic_filters,
                    source_scope=source_scope,
                    ranking_preset=preset_name,
                )
                ndcg = self._ndcg_at_k(ranked, relevance, count)
                aggregate_scores[preset_name].append(ndcg)
                preset_results[preset_name] = {
                    "ndcg_at_k": ndcg,
                    "items": [
                        {
                            "question_id": item.get("question_id"),
                            "score": item.get("score"),
                            "score_breakdown": item.get("score_breakdown"),
                        }
                        for item in ranked
                    ],
                }
            case_results.append(
                {
                    "source_question_id": source_question_id,
                    "count": count,
                    "relevance": relevance,
                    "presets": preset_results,
                }
            )

        preset_summary = {
            name: {
                "weights": dict(PRACTICE_RANKING_PRESETS[name]),
                "case_count": len(scores),
                "mean_ndcg_at_k": round(sum(scores) / len(scores), 6) if scores else 0.0,
            }
            for name, scores in aggregate_scores.items()
        }
        best_preset = sorted(
            preset_summary,
            key=lambda name: (
                -float(preset_summary[name]["mean_ndcg_at_k"]),
                0 if name == DEFAULT_PRACTICE_RANKING_PRESET else 1,
                name,
            ),
        )[0]
        return {
            "best_preset": best_preset,
            "default_preset": DEFAULT_PRACTICE_RANKING_PRESET,
            "case_count": len(case_results),
            "coverage": {
                "source_question_count": len(source_question_ids),
                "labelled_candidate_count": len(labelled_candidate_ids),
                "source_topics": sorted(source_topics),
            },
            "presets": preset_summary,
            "cases": case_results,
        }

    def _rank_similar_questions(
        self,
        safe_user_id: str,
        source: dict[str, Any],
        items: list[dict[str, Any]],
        *,
        count: int,
        same_type_only: bool,
        exclude_mastered: bool,
        topic_filters: list[str],
        source_scope: str,
        ranking_preset: str = DEFAULT_PRACTICE_RANKING_PRESET,
    ) -> list[dict[str, Any]]:
        source_id = str(source.get("question_id") or "")
        source_type = str(source.get("question_type") or "")
        self._practice_ranking_preset(ranking_preset)

        candidates: list[dict[str, Any]] = []
        for item in items:
            question_id = str(item.get("question_id") or "")
            if not question_id or question_id == source_id:
                continue
            if not self._matches_source_scope(item, source, source_scope):
                continue
            if same_type_only and str(item.get("question_type") or "") != source_type:
                continue
            if topic_filters and not (set(topic_filters) & self._topic_set(item)):
                continue
            candidates.append(item)

        if exclude_mastered and candidates:
            states = self.state_store.list_question_states(
                safe_user_id,
                [str(item.get("question_id") or "") for item in candidates],
            )
            candidates = [
                item
                for item in candidates
                if states.get(str(item.get("question_id") or ""), {}).get("mastery_status") != "mastered"
            ]

        scored = []
        for item in candidates:
            score, breakdown = self._score_practice_candidate(source, item, ranking_preset=ranking_preset)
            ranked_item = dict(item)
            ranked_item["score"] = score
            ranked_item["score_breakdown"] = breakdown
            scored.append((score, -(int(item.get("year") or 0)), int(item.get("question_number") or 0), ranked_item))

        scored.sort(key=lambda value: (-value[0], value[1], value[2], str(value[3].get("question_id") or "")))
        return [item for _, _, _, item in scored[:count]]

    def _score_practice_candidate(
        self,
        source: dict[str, Any],
        item: dict[str, Any],
        *,
        ranking_preset: str,
    ) -> tuple[int, dict[str, Any]]:
        weights = self._practice_ranking_preset(ranking_preset)
        source_topics = self._topic_set(source)
        item_topics = self._topic_set(item)
        shared_topics = source_topics & item_topics
        missing_topics = source_topics - item_topics
        extra_topics = item_topics - source_topics if source_topics else set()
        same_type_score = 1 if str(item.get("question_type") or "") == str(source.get("question_type") or "") else 0
        source_library = str(source.get("library_name") or source.get("exam_type") or "")
        item_library = str(item.get("library_name") or item.get("exam_type") or "")
        same_library_score = 1 if item_library == source_library else 0
        full_topic_match = bool(source_topics and not missing_topics)

        score = len(shared_topics) * int(weights.get("topic", 0))
        if full_topic_match:
            score += int(weights.get("all_topic_bonus", 0))
        if source_topics:
            score -= len(missing_topics) * int(weights.get("missing_topic_penalty", 0))
            score -= len(extra_topics) * int(weights.get("extra_topic_penalty", 0))
        score += same_type_score * int(weights.get("type", 0))
        score += same_library_score * int(weights.get("library", 0))

        return score, {
            "preset": ranking_preset,
            "weights": dict(weights),
            "score": score,
            "shared_topic_count": len(shared_topics),
            "shared_topics": sorted(shared_topics),
            "missing_topic_count": len(missing_topics),
            "missing_topics": sorted(missing_topics),
            "extra_topic_count": len(extra_topics),
            "extra_topics": sorted(extra_topics),
            "full_topic_match": full_topic_match,
            "same_type": bool(same_type_score),
            "same_library": bool(same_library_score),
        }

    def _practice_ranking_preset(self, ranking_preset: str) -> dict[str, int]:
        preset_name = str(ranking_preset or DEFAULT_PRACTICE_RANKING_PRESET)
        if preset_name not in PRACTICE_RANKING_PRESETS:
            raise ValueError("invalid practice ranking preset")
        return PRACTICE_RANKING_PRESETS[preset_name]

    def _normalize_relevance_map(self, value: Any) -> dict[str, int]:
        if not isinstance(value, dict) or not value:
            raise ValueError("evaluation case relevance must be a non-empty object")
        relevance: dict[str, int] = {}
        for raw_question_id, raw_score in value.items():
            question_id = validate_safe_id(str(raw_question_id), "question_id")
            try:
                score = int(raw_score)
            except (TypeError, ValueError) as exc:
                raise ValueError("relevance scores must be integers") from exc
            if score < 0:
                raise ValueError("relevance scores must be non-negative")
            relevance[question_id] = score
        return relevance

    def _ndcg_at_k(self, ranked: list[dict[str, Any]], relevance: dict[str, int], count: int) -> float:
        def gain(score: int, rank: int) -> float:
            return ((2 ** score) - 1) / math.log2(rank + 1)

        selected = ranked[:count]
        dcg = sum(gain(int(relevance.get(str(item.get("question_id") or ""), 0)), index + 1) for index, item in enumerate(selected))
        ideal_scores = sorted((int(score) for score in relevance.values()), reverse=True)[:count]
        ideal_dcg = sum(gain(score, index + 1) for index, score in enumerate(ideal_scores))
        if ideal_dcg <= 0:
            return 0.0
        return round(dcg / ideal_dcg, 6)

    def _practice_set_display_order(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(
            items,
            key=lambda item: (
                self._question_type_display_rank(item),
                -(int(item.get("year") or 0)),
                int(item.get("question_number") or 0),
                str(item.get("question_id") or ""),
            ),
        )

    def _question_type_display_rank(self, item: dict[str, Any]) -> int:
        return QUESTION_TYPE_DISPLAY_ORDER.get(str(item.get("question_type") or ""), 9)

    def _matches_source_scope(self, item: dict[str, Any], source: dict[str, Any], source_scope: str) -> bool:
        if source_scope == "same_year":
            return item.get("year") == source.get("year")
        if source_scope == "same_library":
            return str(item.get("library_name") or item.get("exam_type") or "") == str(source.get("library_name") or source.get("exam_type") or "")
        if source_scope == "subject":
            return str(item.get("module") or item.get("subject") or "math") == str(source.get("module") or source.get("subject") or "math")
        return str(item.get("exam_type") or "") == str(source.get("exam_type") or "")

    def _matching_topics(self, source: dict[str, Any], selected: list[dict[str, Any]]) -> list[str]:
        source_topics = self._topic_set(source)
        matched: set[str] = set()
        for item in selected:
            matched.update(source_topics & self._topic_set(item))
        return sorted(matched)

    def _union_topics(self, items: list[dict[str, Any]]) -> list[str]:
        topics: set[str] = set()
        for item in items:
            topics.update(self._topic_set(item))
        return sorted(topics)[:20]

    def _wrong_question_pool_item(
        self,
        safe_user_id: str,
        question: dict[str, Any],
        stat: dict[str, Any],
        state: dict[str, Any],
    ) -> dict[str, Any]:
        attempt_count = int(stat.get("attempt_count") or 0)
        incorrect_count = int(stat.get("incorrect_count") or 0)
        partial_count = int(stat.get("partial_count") or 0)
        pending_review_count = int(stat.get("pending_review_count") or 0)
        unanswered_count = int(stat.get("unanswered_count") or 0)
        wrong_count = incorrect_count + partial_count
        risk_count = wrong_count + pending_review_count + unanswered_count
        features = self._learning_priority_features(
            stat=stat,
            state=state,
            question=question,
        )
        priority_score = self._learning_priority_score(features, stat=stat)
        return {
            "user_id": safe_user_id,
            "question_id": str(question.get("question_id") or ""),
            "title": self._question_title(question),
            "subject": str(question.get("subject") or "math"),
            "exam_type": str(question.get("exam_type") or ""),
            "exam_type_label": str(question.get("exam_type_label") or ""),
            "library_name": str(question.get("library_name") or ""),
            "year": question.get("year"),
            "question_number": question.get("question_number"),
            "question_type": str(question.get("question_type") or ""),
            "question_type_label": str(question.get("question_type_label") or ""),
            "topics": list(question.get("topics") or stat.get("topics") or []),
            "preview": str(question.get("preview") or ""),
            "attempt_count": attempt_count,
            "wrong_count": wrong_count,
            "pending_review_count": pending_review_count,
            "unanswered_count": unanswered_count,
            "risk_count": risk_count,
            "latest_status": str(stat.get("latest_status") or ""),
            "latest_answer": str(stat.get("latest_answer") or ""),
            "latest_practiced_at": str(stat.get("latest_practiced_at") or ""),
            "wrong_streak": int(stat.get("wrong_streak") or 0),
            "confidence": round(features.get("attempt_confidence", 0.0), 4),
            "priority_score": round(priority_score, 4),
            "priority_features": {key: round(float(value), 4) for key, value in features.items()},
            "priority_reasons": self._learning_priority_reasons(features, stat=stat, state=state),
            "is_favorite": bool(state.get("is_favorite")),
            "in_wrong_book": bool(state.get("in_wrong_book")),
            "feedback_hook": "wrong_pool_review_v1",
        }

    def _question_stat_risk_count(self, stat: dict[str, Any]) -> int:
        return (
            int(stat.get("incorrect_count") or 0)
            + int(stat.get("partial_count") or 0)
            + int(stat.get("pending_review_count") or 0)
            + int(stat.get("unanswered_count") or 0)
        )

    def _normalize_wrong_pool_risk_type(self, value: str | None) -> str:
        normalized = self._optional_string(value) or ""
        if normalized in {"", "all"}:
            return ""
        allowed = {"wrong", "pending", "skipped", "manual"}
        if normalized not in allowed:
            raise ValueError("invalid wrong pool risk type")
        return normalized

    def _wrong_pool_matches_risk_type(self, item: dict[str, Any], risk_type: str) -> bool:
        if risk_type == "wrong":
            return int(item.get("wrong_count") or 0) > 0
        if risk_type == "pending":
            return int(item.get("pending_review_count") or 0) > 0
        if risk_type == "skipped":
            return int(item.get("unanswered_count") or 0) > 0
        if risk_type == "manual":
            return bool(item.get("is_favorite") or item.get("in_wrong_book"))
        return True

    def _wrong_pool_risk_type_options(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        definitions = [
            ("wrong", "错题"),
            ("pending", "待核对"),
            ("skipped", "多次未答"),
            ("manual", "手动标记"),
        ]
        options = [{"value": "", "label": "全部风险", "count": len(items)}]
        for value, label in definitions:
            count = sum(1 for item in items if self._wrong_pool_matches_risk_type(item, value))
            options.append({"value": value, "label": label, "count": count})
        return options

    def _is_choice_pending_review_item(self, answer_type: str, question_type: str) -> bool:
        normalized_answer_type = str(answer_type or "").strip().lower()
        normalized_question_type = str(question_type or "").strip().lower()
        return normalized_answer_type == "choice" or normalized_question_type in {
            "single_choice",
            "multiple_choice",
            "choice",
        }

    def _matches_subject_filter(self, record_subject: Any, filter_subject: Any, *, exam_type: Any = "") -> bool:
        normalized_filter = self._optional_string(filter_subject)
        if not normalized_filter or normalized_filter == "all":
            return True
        normalized_record = self._optional_string(record_subject) or ""
        if normalized_record == normalized_filter:
            return True
        if normalized_filter == "math":
            normalized_exam_type = self._optional_string(exam_type) or ""
            return normalized_record in MATH_SUBJECT_ALIASES or normalized_exam_type.startswith("math")
        return False

    def _learning_priority_reasons(
        self,
        features: dict[str, float],
        *,
        stat: dict[str, Any],
        state: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        state = state or {}
        reasons: list[dict[str, Any]] = []
        incorrect_count = int(stat.get("incorrect_count") or 0)
        partial_count = int(stat.get("partial_count") or 0)
        wrong_count = incorrect_count + partial_count
        pending_review_count = int(stat.get("pending_review_count") or 0)
        unanswered_count = int(stat.get("unanswered_count") or 0)
        manual_conflict_count = int(stat.get("manual_conflict_count") or 0)
        wrong_streak = int(stat.get("wrong_streak") or 0)
        correct_streak = int(stat.get("correct_streak") or 0)

        if wrong_streak > 0:
            reasons.append({"type": "wrong_streak", "label": f"连续错 {wrong_streak} 次"})
        elif wrong_count > 0:
            reasons.append({"type": "risk_confidence", "label": f"历史错题 {wrong_count} 次"})
        if pending_review_count > 0:
            reasons.append({"type": "pending_review", "label": f"待核对 {pending_review_count} 题"})
        if unanswered_count > 0:
            reasons.append({"type": "repeated_skip", "label": f"未答 {unanswered_count} 次"})
        if float(features.get("recent_risk") or 0.0) >= 0.65:
            reasons.append({"type": "recent_risk", "label": "近期风险"})
        if state.get("in_wrong_book"):
            reasons.append({"type": "manual_signal", "label": "已在错题"})
        elif state.get("is_favorite"):
            reasons.append({"type": "manual_signal", "label": "已收藏"})
        if correct_streak >= 2:
            reasons.append({"type": "relief", "label": "连续做对，优先级已缓释"})
        elif correct_streak == 1:
            reasons.append({"type": "relief", "label": "最近做对，优先级轻微缓释"})
        if not reasons and float(features.get("risk_confidence") or 0.0) > 0:
            reasons.append({"type": "risk_confidence", "label": "历史表现需复习"})
        if manual_conflict_count > 0 and len(reasons) < 4:
            reasons.append({"type": "manual_signal", "label": f"人工改判 {manual_conflict_count} 次"})
        return reasons[:4]

    def _learning_priority_features(
        self,
        *,
        stat: dict[str, Any],
        state: dict[str, Any] | None = None,
        question: dict[str, Any] | None = None,
        manual_signal: float | None = None,
    ) -> dict[str, float]:
        state = state or {}
        attempt_count = max(0, int(stat.get("attempt_count") or 0))
        correct_count = max(0, int(stat.get("correct_count") or 0))
        incorrect_count = max(0, int(stat.get("incorrect_count") or 0))
        partial_count = max(0, int(stat.get("partial_count") or 0))
        pending_review_count = max(0, int(stat.get("pending_review_count") or 0))
        unanswered_count = max(0, int(stat.get("unanswered_count") or 0))
        unstarted_not_mastered = 1.0 if attempt_count == 0 and str(state.get("mastery_status") or "not_started") != "mastered" else 0.0
        weighted_risk = (
            incorrect_count
            + partial_count * 0.70
            + pending_review_count * 0.55
            + unanswered_count * 0.62
            + unstarted_not_mastered * 0.45
        )
        base_risk = (weighted_risk + 1.0) / (attempt_count + 3.0)
        attempt_confidence = min(1.0, attempt_count / 6.0)
        risk_confidence = min(1.0, base_risk * (0.60 + 0.40 * attempt_confidence))
        latest_status = str(stat.get("latest_status") or "")
        recent_at = str(stat.get("last_risk_at") or stat.get("last_wrong_at") or "")
        if not recent_at and latest_status in {"incorrect", "partial", "pending_review", "unanswered"}:
            recent_at = str(stat.get("latest_practiced_at") or "")
        recent_risk = self._learning_recent_weight(
            recent_at,
            has_risk=weighted_risk > 0,
        )
        wrong_streak = min(1.0, max(0, int(stat.get("wrong_streak") or 0)) / 3.0)
        pending_review = min(1.0, pending_review_count / max(attempt_count, 1))
        skip_rate = min(1.0, unanswered_count / max(attempt_count, 1))
        repeated_skip = min(1.0, (min(unanswered_count, 5) / 5.0) * 0.70 + skip_rate * 0.30)
        if manual_signal is None:
            manual_signal = 1.0 if state.get("in_wrong_book") or state.get("is_favorite") else 0.0
        manual_conflict_count = max(0, int(stat.get("manual_conflict_count") or 0))
        if manual_conflict_count > 0:
            manual_signal = max(float(manual_signal or 0.0), min(1.0, manual_conflict_count / 3.0))
        question_importance = self._question_importance_signal(question or {})
        return {
            "risk_confidence": risk_confidence,
            "attempt_confidence": attempt_confidence,
            "recent_risk": recent_risk,
            "wrong_streak": wrong_streak,
            "pending_review": pending_review,
            "repeated_skip": repeated_skip,
            "unstarted_not_mastered": unstarted_not_mastered,
            "manual_signal": min(1.0, max(0.0, float(manual_signal or 0.0))),
            "question_importance": question_importance,
            "correct_count": float(correct_count),
            "risk_without_skip": float(incorrect_count + partial_count + pending_review_count),
        }

    def _learning_priority_score(self, features: dict[str, float], *, stat: dict[str, Any] | None = None) -> float:
        score = sum(float(features.get(key) or 0.0) * weight for key, weight in LEARNING_PRIORITY_WEIGHTS.items())
        manual_signal = float(features.get("manual_signal") or 0.0)
        if manual_signal:
            score = min(1.0, score + min(LEARNING_PRIORITY_MANUAL_CAP_ADD, manual_signal * LEARNING_PRIORITY_MANUAL_CAP_ADD))
        skip_only = float(features.get("repeated_skip") or 0.0) > 0 and float(features.get("risk_without_skip") or 0.0) <= 0
        unstarted_only = float(features.get("unstarted_not_mastered") or 0.0) > 0 and float(features.get("risk_without_skip") or 0.0) <= 0 and float(features.get("repeated_skip") or 0.0) <= 0
        if skip_only:
            score = min(score, LEARNING_PRIORITY_SKIP_ONLY_CAP)
        if unstarted_only:
            score = min(score, LEARNING_PRIORITY_UNSTARTED_ONLY_CAP)
        if stat and str(stat.get("latest_status") or "") == "correct":
            correct_streak = int(stat.get("correct_streak") or 0)
            if correct_streak >= 2:
                score *= LEARNING_PRIORITY_RELIEF_STABLE_CORRECT
            elif correct_streak == 1:
                score *= LEARNING_PRIORITY_RELIEF_SINGLE_CORRECT
        return max(0.0, min(1.0, score))

    def _question_importance_signal(self, question: dict[str, Any]) -> float:
        raw_importance = question.get("importance") or question.get("importance_score")
        if raw_importance is not None:
            try:
                return max(0.0, min(1.0, float(raw_importance)))
            except (TypeError, ValueError):
                return 0.0
        question_number = int(question.get("question_number") or 0)
        if 1 <= question_number <= 3:
            return 0.25
        if 4 <= question_number <= 8:
            return 0.15
        return 0.0

    def _ensure_review_target_exists(self, safe_user_id: str, target_type: str, target_id: str) -> None:
        if target_type == "question":
            self.library.get_question(target_id)
            return
        if target_type == "practice_set":
            self.get_practice_set(safe_user_id, target_id)
            return

    def _review_target_metadata(self, safe_user_id: str, target_type: str, target_id: str) -> dict[str, Any]:
        if target_type == "question":
            question = self.library.get_question(target_id)
            return {
                "subject": "math",
                "exam_type": str(question.get("exam_type") or ""),
                "library_name": str(question.get("library_name") or ""),
                "source_title": self._question_title(question),
                "year": question.get("year"),
                "question_number": question.get("question_number"),
                "question_type": question.get("question_type"),
                "topics": list(question.get("topics") or []),
            }
        if target_type == "practice_set":
            practice_set = self.get_practice_set(safe_user_id, target_id)
            return {
                "subject": str(practice_set.get("subject") or ""),
                "exam_type": str(practice_set.get("exam_type") or ""),
                "library_name": str(practice_set.get("library_name") or ""),
                "source_title": str(practice_set.get("title") or ""),
                "source_question_id": practice_set.get("source_question_id"),
                "question_count": len(practice_set.get("question_ids") or []),
                "matching_topics": list(practice_set.get("matching_topics") or []),
            }
        return {
            "subject": "other",
            "exam_type": "",
            "library_name": "",
            "source_title": target_id,
        }

    def _practice_attempt_source_meta(self, practice_set: dict[str, Any]) -> dict[str, Any]:
        return {
            "practice_set_id": practice_set.get("set_id"),
            "practice_set_title": practice_set.get("title") or "",
            "source_question_id": practice_set.get("source_question_id"),
            "subject": practice_set.get("subject") or "",
            "exam_type": practice_set.get("exam_type") or "",
            "library_name": practice_set.get("library_name") or "",
            "question_ids": list(practice_set.get("question_ids") or []),
            "question_count": len(practice_set.get("question_ids") or []),
            "matching_topics": list(practice_set.get("matching_topics") or []),
        }

    def _normalize_practice_answers(
        self,
        answers: dict[str, Any],
        practice_set: dict[str, Any],
    ) -> dict[str, dict[str, str]]:
        allowed_question_ids = {str(question_id) for question_id in practice_set.get("question_ids") or []}
        normalized: dict[str, dict[str, str]] = {}
        for question_id, answer in answers.items():
            safe_question_id = validate_safe_id(str(question_id), "question_id")
            if safe_question_id not in allowed_question_ids:
                raise ValueError("answer question_id is not in practice set")
            if not isinstance(answer, dict):
                raise ValueError("answer must be a JSON object")
            answer_type = self._normalize_answer_type(answer.get("answer_type"))
            normalized[safe_question_id] = {
                "answer_type": answer_type,
                "value": self._clean_answer_value(answer.get("value")),
            }
        return normalized

    def _grade_practice_attempt(
        self,
        practice_set: dict[str, Any],
        answers: dict[str, Any],
    ) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
        question_ids = [str(question_id) for question_id in practice_set.get("question_ids") or []]
        results: dict[str, dict[str, Any]] = {}
        for question_id in question_ids:
            question = self.library.get_question(question_id)
            answer = answers.get(question_id) if isinstance(answers, dict) else None
            answer_value = self._clean_answer_value(answer.get("value") if isinstance(answer, dict) else "")
            answer_type = self._question_answer_type(question)
            standard_answer = self._clean_answer_value(question.get("answer") or question.get("answer_markdown") or "")
            if not answer_value:
                local_status = "unanswered"
                final_status = "unanswered"
                judge_method = "local"
                judge_reason = "未作答。"
            elif answer_type == "choice":
                local_status = "correct" if self._normalize_choice_answer(answer_value) == self._normalize_choice_answer(standard_answer) else "incorrect"
                final_status = local_status
                judge_method = "local"
                judge_reason = "选择题按标准答案本地判分。"
            elif answer_type == "blank":
                local_status = "correct" if self._normalize_text_answer(answer_value) == self._normalize_text_answer(standard_answer) else "incorrect"
                final_status = local_status
                judge_method = "local"
                judge_reason = "填空题先按参考答案本地判分；如表达等价可再请求 AI 判分。"
            else:
                local_status = "pending_review"
                final_status = "pending_review"
                judge_method = "manual"
                judge_reason = "解答题不做本地自动判分，可请求 AI 判分或人工确认。"
            results[question_id] = {
                "question_id": question_id,
                "answer_type": answer_type,
                "status": final_status,
                "local_status": local_status,
                "ai_status": "not_used",
                "final_status": final_status,
                "judge_method": judge_method,
                "judge_confidence": 1.0 if final_status in {"correct", "incorrect", "unanswered"} else 0.0,
                "judge_reason": judge_reason,
                "ai_feedback": "",
                "manual_override": False,
                "manual_direction": "",
                "manual_conflict": False,
                "manual_conflict_sources": [],
                "manual_evidence": {},
                "standard_answer": standard_answer,
                "user_answer": answer_value,
            }
        return results, self._summarize_practice_results(results, len(question_ids))

    def _attempt_item_from_result(
        self,
        *,
        safe_user_id: str,
        attempt: dict[str, Any],
        practice_set: dict[str, Any],
        question_id: str,
        result: dict[str, Any],
        submitted_at: str,
    ) -> dict[str, Any]:
        question = self.library.get_question(question_id)
        source_meta = {
            "subject": str(question.get("module") or question.get("subject") or "math"),
            "exam_type": str(question.get("exam_type") or ""),
            "library_name": str(question.get("library_name") or ""),
            "year": question.get("year"),
            "question_number": question.get("question_number"),
        }
        attempt_id = validate_safe_id(str(attempt.get("attempt_id") or ""), "attempt_id")
        safe_question_id = validate_safe_id(question_id, "question_id")
        final_status = str(result.get("final_status") or result.get("status") or "pending_review")
        return {
            "attempt_item_id": f"{attempt_id}__{safe_question_id}",
            "attempt_id": attempt_id,
            "practice_set_id": str(practice_set.get("set_id") or attempt.get("practice_set_id") or ""),
            "user_id": safe_user_id,
            "question_id": safe_question_id,
            "question_title": self._question_title(question),
            "question_type": str(question.get("question_type") or ""),
            "answer_type": str(result.get("answer_type") or self._question_answer_type(question)),
            "topics": list(question.get("topics") or []),
            "source_meta": source_meta,
            "user_answer": self._clean_answer_value(result.get("user_answer")),
            "standard_answer": self._clean_answer_value(result.get("standard_answer")),
            "local_status": str(result.get("local_status") or result.get("status") or "pending_review"),
            "ai_status": str(result.get("ai_status") or "not_used"),
            "final_status": final_status,
            "status": final_status,
            "judge_method": str(result.get("judge_method") or "local"),
            "judge_confidence": self._normalize_confidence(result.get("judge_confidence")),
            "judge_reason": self._clean_string(result.get("judge_reason")),
            "ai_feedback": self._clean_string(result.get("ai_feedback")),
            "manual_override": bool(result.get("manual_override", False)),
            "manual_direction": str(result.get("manual_direction") or ""),
            "manual_conflict": bool(result.get("manual_conflict", False)),
            "manual_conflict_sources": list(result.get("manual_conflict_sources") or []),
            "manual_evidence": dict(result.get("manual_evidence") or {}),
            "submitted_at": submitted_at,
            "graded_at": result.get("graded_at"),
            "grading_version": str(result.get("grading_version") or "local_v1"),
        }

    def _write_attempt_items_for_attempt(
        self,
        safe_user_id: str,
        attempt: dict[str, Any],
        practice_set: dict[str, Any],
    ) -> list[dict[str, Any]]:
        results = attempt.get("results") if isinstance(attempt.get("results"), dict) else {}
        submitted_at = str(attempt.get("submitted_at") or self._utc_now())
        next_items: list[dict[str, Any]] = []
        for question_id, result in results.items():
            if not isinstance(result, dict):
                continue
            safe_question_id = validate_safe_id(str(question_id), "question_id")
            next_items.append(
                self._attempt_item_from_result(
                    safe_user_id=safe_user_id,
                    attempt=attempt,
                    practice_set=practice_set,
                    question_id=safe_question_id,
                    result=result,
                    submitted_at=submitted_at,
                )
            )
        records = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        replacing_ids = {item["attempt_item_id"] for item in next_items}
        kept = [record for record in records if record.get("attempt_item_id") not in replacing_ids]
        kept.extend(next_items)
        self._write_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, kept)
        return next_items

    def rebuild_user_learning_stats(self, user_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        items = self._read_records(safe_user_id, PRACTICE_ATTEMPT_ITEM_FILENAME, "attempt_item_id")
        question_stats: dict[str, dict[str, Any]] = {}
        topic_stats: dict[str, dict[str, Any]] = {}
        for item in sorted(items, key=lambda row: str(row.get("submitted_at") or "")):
            question_id = str(item.get("question_id") or "")
            if not question_id:
                continue
            status = str(item.get("final_status") or item.get("status") or "pending_review")
            count_key = self._status_count_key(status)
            question_stat = question_stats.setdefault(
                question_id,
                {
                    "stat_id": question_id,
                    "user_id": safe_user_id,
                    "question_id": question_id,
                    "attempt_count": 0,
                    "correct_count": 0,
                    "incorrect_count": 0,
                    "partial_count": 0,
                    "pending_review_count": 0,
                    "unanswered_count": 0,
                    "manual_override_count": 0,
                    "manual_conflict_count": 0,
                    "latest_attempt_id": "",
                    "latest_status": "",
                    "latest_answer": "",
                    "latest_practiced_at": "",
                    "wrong_streak": 0,
                    "correct_streak": 0,
                    "last_wrong_at": "",
                    "last_risk_at": "",
                    "topics": list(item.get("topics") or []),
                },
            )
            question_stat["attempt_count"] += 1
            question_stat[count_key] += 1
            if bool(item.get("manual_override")):
                question_stat["manual_override_count"] += 1
            if bool(item.get("manual_conflict")):
                question_stat["manual_conflict_count"] += 1
                question_stat["last_risk_at"] = str(item.get("submitted_at") or "")
            question_stat["latest_attempt_id"] = str(item.get("attempt_id") or "")
            question_stat["latest_status"] = status
            question_stat["latest_answer"] = self._clean_answer_value(item.get("user_answer"))
            question_stat["latest_practiced_at"] = str(item.get("submitted_at") or "")
            question_stat["topics"] = list(item.get("topics") or [])
            if status in {"incorrect", "partial"}:
                question_stat["wrong_streak"] += 1
                question_stat["correct_streak"] = 0
                question_stat["last_wrong_at"] = str(item.get("submitted_at") or "")
                question_stat["last_risk_at"] = str(item.get("submitted_at") or "")
            elif status in {"pending_review", "unanswered"}:
                question_stat["correct_streak"] = 0
                question_stat["last_risk_at"] = str(item.get("submitted_at") or "")
            elif status == "correct":
                question_stat["wrong_streak"] = 0
                question_stat["correct_streak"] += 1

            source_meta = item.get("source_meta") if isinstance(item.get("source_meta"), dict) else {}
            subject = str(source_meta.get("subject") or "math")
            for topic in [str(topic).strip() for topic in item.get("topics") or [] if str(topic).strip()]:
                stat_id = self._topic_stat_id(subject, topic)
                topic_stat = topic_stats.setdefault(
                    stat_id,
                    {
                        "stat_id": stat_id,
                        "user_id": safe_user_id,
                        "subject": subject,
                        "topic": topic,
                        "attempt_count": 0,
                        "correct_count": 0,
                        "incorrect_count": 0,
                        "partial_count": 0,
                        "pending_review_count": 0,
                        "unanswered_count": 0,
                        "manual_override_count": 0,
                        "manual_conflict_count": 0,
                        "latest_attempt_id": "",
                        "latest_practiced_at": "",
                        "last_risk_at": "",
                        "representative_wrong_question_ids": [],
                    },
                )
                topic_stat["attempt_count"] += 1
                topic_stat[count_key] += 1
                if bool(item.get("manual_override")):
                    topic_stat["manual_override_count"] += 1
                if bool(item.get("manual_conflict")):
                    topic_stat["manual_conflict_count"] += 1
                    topic_stat["last_risk_at"] = str(item.get("submitted_at") or "")
                topic_stat["latest_attempt_id"] = str(item.get("attempt_id") or "")
                topic_stat["latest_practiced_at"] = str(item.get("submitted_at") or "")
                if status in {"incorrect", "partial", "pending_review", "unanswered"}:
                    topic_stat["last_risk_at"] = str(item.get("submitted_at") or "")
                if status in {"incorrect", "partial"} and question_id not in topic_stat["representative_wrong_question_ids"]:
                    topic_stat["representative_wrong_question_ids"].append(question_id)
                    topic_stat["representative_wrong_question_ids"] = topic_stat["representative_wrong_question_ids"][-5:]

        self._write_records(safe_user_id, USER_QUESTION_STATS_FILENAME, list(question_stats.values()))
        self._write_records(safe_user_id, USER_TOPIC_STATS_FILENAME, list(topic_stats.values()))
        return {"question_stats": question_stats, "topic_stats": topic_stats}

    def _learning_items_summary(self, items: list[dict[str, Any]]) -> dict[str, Any]:
        status_counts = {
            "correct_count": 0,
            "incorrect_count": 0,
            "partial_count": 0,
            "pending_review_count": 0,
            "unanswered_count": 0,
        }
        latest_practiced_at = ""
        latest_attempt_id = ""
        latest_pending_attempt_id = ""
        latest_pending_at = ""
        attempt_ids: set[str] = set()
        question_ids: set[str] = set()
        pending_review_question_ids: set[str] = set()
        for item in items:
            attempt_id = str(item.get("attempt_id") or "")
            question_id = str(item.get("question_id") or "")
            if attempt_id:
                attempt_ids.add(attempt_id)
            if question_id:
                question_ids.add(question_id)
            status = str(item.get("final_status") or item.get("status") or "pending_review")
            count_key = self._status_count_key(status)
            status_counts[count_key] = status_counts.get(count_key, 0) + 1
            practiced_at = str(item.get("submitted_at") or item.get("graded_at") or "")
            if practiced_at and practiced_at > latest_practiced_at:
                latest_practiced_at = practiced_at
                latest_attempt_id = attempt_id
            if count_key == "pending_review_count" and practiced_at and practiced_at >= latest_pending_at:
                latest_pending_at = practiced_at
                latest_pending_attempt_id = attempt_id
            if count_key == "pending_review_count" and question_id:
                answer_type = str(item.get("answer_type") or "")
                question_type = str(item.get("question_type") or "")
                if not self._is_choice_pending_review_item(answer_type, question_type):
                    pending_review_question_ids.add(question_id)
        return {
            "practice_attempt_count": len(attempt_ids),
            "question_attempt_count": len(items),
            "unique_question_count": len(question_ids),
            "latest_practiced_at": latest_practiced_at,
            "latest_attempt_id": latest_attempt_id,
            "latest_pending_attempt_id": latest_pending_attempt_id,
            "pending_review_question_count": len(pending_review_question_ids),
            **status_counts,
        }

    def _learning_review_summary(self, review_tasks: list[dict[str, Any]]) -> dict[str, Any]:
        counts = {
            "total": len(review_tasks),
            "overdue_count": 0,
            "today_count": 0,
            "future_count": 0,
            "completed_count": 0,
            "cancelled_count": 0,
            "unscheduled_count": 0,
        }
        for task in review_tasks:
            group = self._review_date_group(task)
            key = f"{group}_count"
            counts[key] = counts.get(key, 0) + 1
        counts["due_count"] = counts.get("overdue_count", 0) + counts.get("today_count", 0)
        return counts

    def _learning_weak_topics(
        self,
        topic_stats: list[dict[str, Any]],
        review_summary: dict[str, Any],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        weak_topics: list[dict[str, Any]] = []
        for stat in topic_stats:
            attempt_count = int(stat.get("attempt_count") or 0)
            if attempt_count <= 0:
                continue
            incorrect_count = int(stat.get("incorrect_count") or 0)
            partial_count = int(stat.get("partial_count") or 0)
            pending_review_count = int(stat.get("pending_review_count") or 0)
            unanswered_count = int(stat.get("unanswered_count") or 0)
            wrong_count = incorrect_count + partial_count
            manual_signal = 1.0 if stat.get("representative_wrong_question_ids") or int(stat.get("manual_conflict_count") or 0) > 0 else 0.0
            features = self._learning_priority_features(
                stat=stat,
                manual_signal=manual_signal,
            )
            priority_score = self._learning_priority_score(features, stat=stat)
            weak_topics.append(
                {
                    "topic": str(stat.get("topic") or ""),
                    "subject": str(stat.get("subject") or ""),
                    "attempt_count": attempt_count,
                    "wrong_count": wrong_count,
                    "pending_review_count": pending_review_count,
                    "unanswered_count": unanswered_count,
                    "smoothed_error_rate": round(features.get("risk_confidence", 0.0), 4),
                    "confidence": round(features.get("attempt_confidence", 0.0), 4),
                    "priority_score": round(priority_score, 4),
                    "priority_features": {key: round(float(value), 4) for key, value in features.items()},
                    "priority_reasons": self._learning_priority_reasons(features, stat=stat),
                    "latest_practiced_at": stat.get("latest_practiced_at") or "",
                    "representative_wrong_question_ids": list(stat.get("representative_wrong_question_ids") or [])[:5],
                }
            )
        return sorted(
            weak_topics,
            key=lambda item: (
                -float(item.get("priority_score") or 0),
                -int(item.get("wrong_count") or 0),
                str(item.get("topic") or ""),
            ),
        )[:limit]

    def _learning_next_actions(
        self,
        summary: dict[str, Any],
        weak_topics: list[dict[str, Any]],
        review_summary: dict[str, Any],
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        wrong_total = int(summary.get("incorrect_count") or 0) + int(summary.get("partial_count") or 0)
        pending_total = int(summary.get("pending_review_count") or 0)
        pending_question_total = int(summary.get("pending_review_question_count") or 0)
        due_total = int(review_summary.get("due_count") or 0)
        if due_total:
            actions.append({"type": "review_due", "label": f"处理 {due_total} 个到期复习", "status": "due"})
        if wrong_total:
            actions.append({"type": "review_wrong", "label": f"复习 {wrong_total} 道错题", "status": "incorrect"})
        if pending_question_total:
            actions.append({"type": "confirm_grading", "label": f"确认 {pending_question_total} 道待核对题", "status": "pending_review"})
        if weak_topics:
            actions.append(
                {
                    "type": "topic_review",
                    "label": f"优先复习 {weak_topics[0]['topic']}",
                    "topic": weak_topics[0]["topic"],
                    "priority_score": weak_topics[0]["priority_score"],
                }
            )
        if not actions:
            actions.append({"type": "keep_practicing", "label": "暂无明显风险，保持当前节奏"})
        return actions[:4]

    def _learning_recent_weight(self, value: Any, *, has_risk: bool) -> float:
        if not has_risk:
            return 0.0
        raw_value = str(value or "")
        if not raw_value:
            return 0.2
        try:
            practiced_at = datetime.fromisoformat(raw_value)
        except ValueError:
            return 0.2
        if practiced_at.tzinfo is None:
            practiced_at = practiced_at.replace(tzinfo=timezone.utc)
        age_days = max(0, (datetime.now(timezone.utc) - practiced_at).days)
        if age_days <= 7:
            return 1.0
        if age_days <= 30:
            return 0.65
        if age_days <= 90:
            return 0.35
        return 0.2

    def _practice_attempt_topic_impacts(
        self,
        items: list[dict[str, Any]],
        topic_stats: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        by_topic: dict[str, dict[str, Any]] = {}
        for item in items:
            status = str(item.get("final_status") or item.get("status") or "pending_review")
            for raw_topic in item.get("topics") or []:
                topic = str(raw_topic).strip()
                if not topic:
                    continue
                impact = by_topic.setdefault(
                    topic,
                    {
                        "topic": topic,
                        "attempt_count": 0,
                        "wrong_count": 0,
                        "correct_count": 0,
                        "pending_review_count": 0,
                    },
                )
                impact["attempt_count"] += 1
                if status == "correct":
                    impact["correct_count"] += 1
                elif status == "pending_review":
                    impact["pending_review_count"] += 1
                    impact["wrong_count"] += 1
                elif status in {"incorrect", "partial"}:
                    impact["wrong_count"] += 1

        for impact in by_topic.values():
            stat = next(
                (value for value in topic_stats.values() if value.get("topic") == impact["topic"]),
                {},
            )
            lifetime_attempts = int(stat.get("attempt_count") or 0)
            lifetime_wrong = (
                int(stat.get("incorrect_count") or 0)
                + int(stat.get("partial_count") or 0)
                + int(stat.get("pending_review_count") or 0)
            )
            impact["lifetime_attempt_count"] = lifetime_attempts
            impact["lifetime_wrong_count"] = lifetime_wrong
            impact["wrong_rate"] = (
                impact["wrong_count"] / impact["attempt_count"]
                if impact["attempt_count"]
                else 0
            )
        return sorted(
            by_topic.values(),
            key=lambda item: (
                -float(item.get("wrong_rate") or 0),
                -int(item.get("wrong_count") or 0),
                str(item.get("topic") or ""),
            ),
        )[:3]

    def _practice_attempt_question_impacts(
        self,
        items: list[dict[str, Any]],
        question_stats: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        impacts: list[dict[str, Any]] = []
        for item in items:
            question_id = str(item.get("question_id") or "")
            if not question_id:
                continue
            stat = question_stats.get(question_id, {})
            impacts.append(
                {
                    "question_id": question_id,
                    "title": item.get("question_title") or question_id,
                    "final_status": item.get("final_status") or item.get("status") or "pending_review",
                    "judge_method": item.get("judge_method") or "local",
                    "attempt_count": int(stat.get("attempt_count") or 0),
                    "wrong_count": int(stat.get("incorrect_count") or 0),
                    "last_practiced_at": stat.get("latest_practiced_at"),
                }
            )
        return impacts

    def _practice_attempt_next_actions(
        self,
        summary: dict[str, Any],
        topic_impacts: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        wrong_total = int(summary.get("incorrect") or 0) + int(summary.get("partial") or 0)
        pending_total = int(summary.get("pending_review") or 0)
        if wrong_total:
            actions.append(
                {
                    "type": "review_wrong",
                    "label": f"复习 {wrong_total} 道错题",
                    "status": "incorrect",
                }
            )
        if pending_total:
            actions.append(
                {
                    "type": "confirm_grading",
                    "label": f"确认 {pending_total} 道待核对题",
                    "status": "pending_review",
                }
            )
        if topic_impacts:
            actions.append(
                {
                    "type": "topic_review",
                    "label": f"优先复习 {topic_impacts[0]['topic']}",
                    "topic": topic_impacts[0]["topic"],
                }
            )
        if not actions:
            actions.append({"type": "keep_practicing", "label": "本次表现稳定，可继续同类训练"})
        return actions

    def _practice_attempt_insight_headline(
        self,
        summary: dict[str, Any],
        topic_impacts: list[dict[str, Any]],
    ) -> str:
        if topic_impacts and int(topic_impacts[0].get("wrong_count") or 0):
            return f"薄弱知识点：{topic_impacts[0]['topic']}"
        if int(summary.get("incorrect") or 0) == 0 and int(summary.get("pending_review") or 0) == 0:
            return "本次练习记录已保存，暂无明显薄弱点"
        return "本次练习记录已保存，建议处理错题和待核对题"

    def _backfill_practice_attempt_result(self, record: dict[str, Any]) -> dict[str, Any]:
        if record.get("status") != "submitted":
            return dict(record)
        results = record.get("results") if isinstance(record.get("results"), dict) else {}
        if not results:
            return dict(record)
        answers = record.get("answers") if isinstance(record.get("answers"), dict) else {}
        updated_results: dict[str, dict[str, Any]] = {}
        changed = False
        for question_id, raw_result in results.items():
            if not isinstance(raw_result, dict):
                continue
            result = dict(raw_result)
            safe_question_id = str(result.get("question_id") or question_id)
            answer = answers.get(safe_question_id) if isinstance(answers.get(safe_question_id), dict) else {}
            try:
                question = self.library.get_question(safe_question_id)
            except KeyError:
                question = {}
            answer_type = (
                result.get("answer_type")
                or answer.get("answer_type")
                or (self._question_answer_type(question) if question else "solution")
            )
            answer_type = "blank" if answer_type == "fill_blank" else str(answer_type or "solution")
            if answer_type not in PRACTICE_ANSWER_TYPES:
                answer_type = "solution"
            standard_answer = self._clean_answer_value(
                result.get("standard_answer")
                or (question.get("answer") if question else "")
                or (question.get("answer_markdown") if question else "")
            )
            answer_value = self._clean_answer_value(
                result.get("user_answer")
                or answer.get("value")
            )
            local_status, judge_reason = self._local_grade_for_answer(
                answer_type=answer_type,
                answer_value=answer_value,
                standard_answer=standard_answer,
            )
            current_method = str(result.get("judge_method") or "")
            final_status = str(result.get("final_status") or result.get("status") or "")
            is_ai_or_manual = current_method in {"ai", "manual"} or bool(result.get("manual_override"))
            should_replace_final = (
                not is_ai_or_manual
                and answer_type in {"choice", "blank"}
                and final_status in {"", "pending_review", "needs_review", "needs_grading", "pending"}
            )
            next_result = {
                **result,
                "question_id": safe_question_id,
                "answer_type": answer_type,
                "local_status": result.get("local_status") or local_status,
                "ai_status": result.get("ai_status") or "not_used",
                "standard_answer": standard_answer,
                "user_answer": answer_value,
            }
            if should_replace_final:
                next_result["status"] = local_status
                next_result["final_status"] = local_status
                next_result["judge_method"] = "local"
                next_result["judge_confidence"] = 1.0 if local_status in {"correct", "incorrect", "unanswered"} else 0.0
                next_result["judge_reason"] = judge_reason
            else:
                next_result["status"] = result.get("status") or result.get("final_status") or local_status
                next_result["final_status"] = result.get("final_status") or result.get("status") or local_status
                next_result["judge_method"] = result.get("judge_method") or ("local" if answer_type in {"choice", "blank"} else "manual")
                next_result["judge_confidence"] = self._normalize_confidence(result.get("judge_confidence"))
                next_result["judge_reason"] = result.get("judge_reason") or judge_reason
            next_result["ai_feedback"] = result.get("ai_feedback") or ""
            next_result["manual_override"] = bool(result.get("manual_override", False))
            next_result["manual_direction"] = result.get("manual_direction") or ""
            next_result["manual_conflict"] = bool(result.get("manual_conflict", False))
            next_result["manual_conflict_sources"] = list(result.get("manual_conflict_sources") or [])
            next_result["manual_evidence"] = dict(result.get("manual_evidence") or {})
            if next_result != result:
                changed = True
            updated_results[safe_question_id] = next_result
        if not changed:
            return dict(record)
        updated = dict(record)
        updated["results"] = updated_results
        updated["summary"] = self._summarize_practice_results(updated_results, len(updated_results))
        return updated

    def _local_grade_for_answer(self, *, answer_type: str, answer_value: str, standard_answer: str) -> tuple[str, str]:
        if not answer_value:
            return "unanswered", "未作答。"
        if answer_type == "choice":
            status = "correct" if self._normalize_choice_answer(answer_value) == self._normalize_choice_answer(standard_answer) else "incorrect"
            return status, "选择题按标准答案本地判分。"
        if answer_type == "blank":
            status = "correct" if self._normalize_text_answer(answer_value) == self._normalize_text_answer(standard_answer) else "incorrect"
            return status, "填空题先按参考答案本地判分；如表达等价可再请求 AI 判分。"
        return "pending_review", "解答题不做本地自动判分，可请求 AI 判分或人工确认。"

    def _question_answer_type(self, question: dict[str, Any]) -> str:
        question_type = str(question.get("question_type") or "")
        if question_type in {"single_choice", "multiple_choice", "choice"}:
            return "choice"
        if question_type in {"fill_blank", "blank"}:
            return "blank"
        return "solution"

    def _normalize_answer_type(self, value: Any) -> str:
        answer_type = str(value or "").strip()
        if answer_type == "fill_blank":
            return "blank"
        if answer_type not in PRACTICE_ANSWER_TYPES:
            raise ValueError("invalid answer_type")
        return answer_type

    def _clean_answer_value(self, value: Any) -> str:
        if value in (None, ""):
            return ""
        return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()

    def _normalize_choice_answer(self, value: str) -> str:
        normalized = self._normalize_text_answer(value).upper()
        return normalized.strip(" .。:：;；、，,")

    def _normalize_text_answer(self, value: str) -> str:
        return " ".join(str(value or "").strip().split())

    def _empty_attempt_summary(self, total: int) -> dict[str, int]:
        return {
            "total": int(total),
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "pending_review": 0,
            "unanswered": 0,
        }

    def _summarize_practice_results(self, results: dict[str, Any], total: int) -> dict[str, int]:
        summary = self._empty_attempt_summary(total)
        for result in results.values():
            if not isinstance(result, dict):
                continue
            status = str(result.get("final_status") or result.get("status") or "pending_review")
            if status == "needs_review" or status == "needs_grading":
                status = "pending_review"
            if status not in summary:
                status = "pending_review"
            summary[status] += 1
        return summary

    def _status_count_key(self, status: Any) -> str:
        normalized = str(status or "pending_review")
        if normalized in {"needs_review", "needs_grading", "pending"}:
            normalized = "pending_review"
        if normalized not in {"correct", "incorrect", "partial", "pending_review", "unanswered"}:
            normalized = "pending_review"
        return f"{normalized}_count"

    def _manual_grade_metadata(self, result: dict[str, Any], final_status: str) -> dict[str, Any]:
        local_status = str(result.get("local_status") or "")
        ai_status = str(result.get("ai_status") or "not_used")
        evidence = {
            "local_status": local_status or "unknown",
            "ai_status": ai_status or "not_used",
        }
        conflict_sources: list[str] = []
        if local_status in {"correct", "incorrect", "partial"} and local_status != final_status:
            conflict_sources.append("local")
        if ai_status in {"correct", "incorrect", "partial"} and ai_status != final_status:
            conflict_sources.append("ai")
        return {
            "manual_direction": f"confirm_{final_status}",
            "manual_conflict": bool(conflict_sources),
            "manual_conflict_sources": conflict_sources,
            "manual_evidence": evidence,
        }

    def _topic_stat_id(self, subject: str, topic: str) -> str:
        raw_subject = str(subject or "other").strip() or "other"
        try:
            subject_id = validate_safe_id(raw_subject.replace(" ", "_"), "subject")
        except ValueError:
            subject_id = f"subject_{hashlib.sha1(raw_subject.encode('utf-8')).hexdigest()[:8]}"
        digest = hashlib.sha1(topic.encode("utf-8")).hexdigest()[:16]
        return f"{subject_id}_{digest}"

    def _duration_seconds(self, started_at: str, submitted_at: str) -> int:
        try:
            started = datetime.fromisoformat(started_at)
            submitted = datetime.fromisoformat(submitted_at)
        except ValueError:
            return 0
        return max(0, int((submitted - started).total_seconds()))

    def _find_duplicate_review_task(
        self,
        records: list[dict[str, Any]],
        *,
        target_type: str,
        target_id: str,
        due_at: str | None,
    ) -> dict[str, Any] | None:
        for record in records:
            if (
                record.get("target_type") == target_type
                and record.get("target_id") == target_id
                and record.get("due_at") == due_at
            ):
                return dict(record)
        return None

    def _review_task_learning_reasons(self, safe_user_id: str, task: dict[str, Any]) -> list[dict[str, str]]:
        target_type = str(task.get("target_type") or "")
        target_id = str(task.get("target_id") or "")
        reasons: list[dict[str, str]] = []
        if target_type == "question" and target_id:
            try:
                snapshot = self.build_question_learning_snapshot(safe_user_id, target_id)
            except (KeyError, ValueError):
                snapshot = {}
            incorrect_count = int(snapshot.get("incorrect_count") or 0)
            wrong_streak = int(snapshot.get("wrong_streak") or 0)
            if incorrect_count:
                reasons.append({"type": "wrong_history", "label": f"历史错 {incorrect_count} 次"})
            if wrong_streak:
                reasons.append({"type": "wrong_streak", "label": f"连续错 {wrong_streak} 次"})
            if snapshot.get("latest_status") == "pending_review":
                reasons.append({"type": "pending_review", "label": "最近一次待核对"})
        if target_type == "practice_set":
            source_meta = task.get("source_meta") if isinstance(task.get("source_meta"), dict) else {}
            question_count = source_meta.get("question_count")
            label = "来自同类训练练习单"
            if question_count:
                label = f"来自同类训练练习单 · {question_count} 题"
            reasons.append({"type": "practice_set", "label": label})
        return reasons[:3]

    def _question_title(self, question: dict[str, Any]) -> str:
        year = question.get("year") or ""
        number = question.get("question_number") or ""
        label = question.get("exam_type_label") or question.get("exam_type") or ""
        if year and number:
            return f"{year} {label} Q{number}"
        return str(question.get("question_id") or "系统题")

    def _review_date_group(self, task: dict[str, Any]) -> str:
        status = str(task.get("status") or "pending")
        if status in {"completed", "cancelled"}:
            return status
        due_at = self._optional_string(task.get("due_at"))
        if not due_at:
            return "unscheduled"
        due_date_text = due_at[:10]
        today_text = datetime.now(timezone.utc).date().isoformat()
        if due_date_text < today_text:
            return "overdue"
        if due_date_text == today_text:
            return "today"
        return "future"

    def _review_task_search_text(self, task: dict[str, Any]) -> str:
        meta = task.get("source_meta") if isinstance(task.get("source_meta"), dict) else {}
        parts = [
            task.get("title"),
            task.get("target_id"),
            task.get("library_name"),
            task.get("source_title"),
            task.get("note"),
            *list(meta.get("topics") or []),
            *list(meta.get("matching_topics") or []),
        ]
        return " ".join(str(part) for part in parts if part not in (None, ""))

    def _find_question(self, items: list[dict[str, Any]], question_id: str) -> dict[str, Any] | None:
        for item in items:
            if item.get("question_id") == question_id:
                return item
        return None

    def _read_records(self, safe_user_id: str, filename: str, id_field: str) -> list[dict[str, Any]]:
        path = self._record_path(safe_user_id, filename)
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
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
                record_id = row.get(id_field)
                if not isinstance(record_id, str):
                    continue
                try:
                    validate_safe_id(record_id, id_field)
                except ValueError:
                    continue
                records.append(row)
        return records

    def _write_records(self, safe_user_id: str, filename: str, records: list[dict[str, Any]]) -> None:
        path = self._record_path(safe_user_id, filename)
        if not records:
            if path.exists():
                path.unlink()
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _record_path(self, safe_user_id: str, filename: str) -> Path:
        user_dir = ensure_within_base(
            self.users_dir,
            self.users_dir / safe_user_id / user_state.SYSTEM_LIBRARY_DIRNAME,
        )
        return user_dir / filename

    def _topic_set(self, item: dict[str, Any]) -> set[str]:
        return {str(topic).strip() for topic in item.get("topics") or [] if str(topic).strip()}

    def _normalize_count(self, value: Any) -> int:
        try:
            count = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("count must be an integer") from exc
        if count < 1:
            raise ValueError("count must be at least 1")
        return min(count, 50)

    def _normalize_topic_filters(self, value: Any) -> list[str]:
        if value in (None, ""):
            return []
        if isinstance(value, str):
            raw_items = [value]
        elif isinstance(value, list):
            raw_items = value
        else:
            raise ValueError("topic_filters must be a list of strings")
        topics: list[str] = []
        seen: set[str] = set()
        for item in raw_items:
            topic = str(item).strip()
            if not topic or topic in seen:
                continue
            topics.append(topic)
            seen.add(topic)
        return topics[:20]

    def _normalize_source_scope(self, value: Any) -> str:
        source_scope = str(value or "exam_type")
        if source_scope not in PRACTICE_SOURCE_SCOPES:
            raise ValueError("invalid practice source_scope")
        return source_scope

    def _normalize_target_type(self, value: Any) -> str:
        target_type = str(value or "")
        if target_type not in REVIEW_TARGET_TYPES:
            raise ValueError("invalid review target_type")
        return target_type

    def _normalize_review_status(self, value: Any) -> str:
        status = str(value or "")
        if status not in REVIEW_TASK_STATUSES:
            raise ValueError("invalid review task status")
        return status

    def _normalize_final_status(self, value: Any) -> str:
        status = str(value or "")
        if status in {"needs_review", "needs_grading", "pending"}:
            status = "pending_review"
        if status not in PRACTICE_FINAL_STATUSES:
            raise ValueError("invalid practice final_status")
        return status

    def _normalize_judge_method(self, value: Any) -> str:
        method = str(value or "")
        if method not in PRACTICE_JUDGE_METHODS:
            raise ValueError("invalid judge_method")
        return method

    def _normalize_confidence(self, value: Any) -> float | None:
        if value in (None, ""):
            return None
        try:
            confidence = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("judge_confidence must be a number") from exc
        if math.isnan(confidence):
            raise ValueError("judge_confidence must be a number")
        return max(0.0, min(1.0, confidence))

    def _normalize_priority(self, value: Any) -> int:
        try:
            priority = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("priority must be an integer") from exc
        if priority < 1 or priority > 5:
            raise ValueError("priority must be between 1 and 5")
        return priority

    def _optional_string(self, value: Any) -> str | None:
        if value in (None, ""):
            return None
        return str(value)

    def _clean_string(self, value: Any) -> str:
        if value in (None, ""):
            return ""
        return str(value).strip()

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:16]}"

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
