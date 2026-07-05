from __future__ import annotations

import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import user_state
from .security import ensure_within_base, resolve_user_id, validate_safe_id
from .system_library import SystemQuestionLibrary


PRACTICE_SET_FILENAME = "practice_sets.jsonl"
PRACTICE_ATTEMPT_FILENAME = "practice_attempts.jsonl"
REVIEW_TASK_FILENAME = "review_tasks.jsonl"
PRACTICE_SET_STATUSES = {"active", "archived"}
PRACTICE_ATTEMPT_STATUSES = {"draft", "submitted", "abandoned"}
PRACTICE_ANSWER_TYPES = {"choice", "blank", "solution"}
REVIEW_TARGET_TYPES = {"question", "practice_set", "knowledge_point"}
REVIEW_TASK_STATUSES = {"pending", "completed", "cancelled"}
PRACTICE_SOURCE_SCOPES = {"exam_type", "same_library", "same_year", "subject"}
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
            self._write_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, records)
            return dict(updated)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

    def get_practice_attempt(self, user_id: str, attempt_id: str) -> dict[str, Any]:
        safe_user_id = resolve_user_id(user_id)
        safe_attempt_id = validate_safe_id(attempt_id, "attempt_id")
        for record in self._read_records(safe_user_id, PRACTICE_ATTEMPT_FILENAME, "attempt_id"):
            if record.get("attempt_id") == safe_attempt_id:
                return dict(record)
        raise KeyError(f"practice attempt not found: {safe_attempt_id}")

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
        return sorted(records, key=lambda record: str(record.get("started_at") or ""), reverse=True)

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
        summary = self._empty_attempt_summary(len(question_ids))
        results: dict[str, dict[str, Any]] = {}
        for question_id in question_ids:
            question = self.library.get_question(question_id)
            answer = answers.get(question_id) if isinstance(answers, dict) else None
            answer_value = self._clean_answer_value(answer.get("value") if isinstance(answer, dict) else "")
            answer_type = self._question_answer_type(question)
            standard_answer = self._clean_answer_value(question.get("answer") or question.get("answer_markdown") or "")
            if not answer_value:
                status = "unanswered"
            elif answer_type == "choice":
                status = "correct" if self._normalize_choice_answer(answer_value) == self._normalize_choice_answer(standard_answer) else "incorrect"
            elif answer_type == "blank":
                status = "correct" if self._normalize_text_answer(answer_value) == self._normalize_text_answer(standard_answer) else "needs_review"
            else:
                status = "needs_grading"
            summary[status] += 1
            results[question_id] = {
                "question_id": question_id,
                "answer_type": answer_type,
                "status": status,
                "standard_answer": standard_answer,
                "user_answer": answer_value,
            }
        return results, summary

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
            "unanswered": 0,
            "needs_review": 0,
            "needs_grading": 0,
        }

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
