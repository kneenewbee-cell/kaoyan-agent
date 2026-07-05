from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


DANGEROUS_TOKENS = ("eval", "exec", "import", "subprocess", "os.system", "open(", "__")
SubjectName = Literal["math", "politics", "english", "408", "other", "unknown"]
MaterialTypeName = Literal["textbook", "lecture", "exercise", "unknown"]


class MetadataProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: SubjectName = "unknown"
    material_type: MaterialTypeName = "unknown"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list, max_length=8)
    source: Literal["qwen", "fallback", "unknown"] = "qwen"

    @field_validator("evidence", mode="before")
    @classmethod
    def normalize_evidence(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value[:160]]
        if not isinstance(value, list):
            return []
        return [str(item)[:160] for item in value[:8] if str(item).strip()]


def default_metadata_profile() -> MetadataProfile:
    return MetadataProfile(subject="unknown", material_type="unknown", confidence=0.0, evidence=[], source="fallback")


def _contains_dangerous_token(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_dangerous_token(k) or _contains_dangerous_token(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_dangerous_token(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in DANGEROUS_TOKENS)
    return False


def summarize_metadata_profile_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"subject": None, "material_type": None, "confidence": None, "evidence_count": 0}
    evidence = payload.get("evidence") or []
    return {
        "subject": payload.get("subject"),
        "material_type": payload.get("material_type"),
        "confidence": payload.get("confidence"),
        "evidence_count": len(evidence) if isinstance(evidence, list) else 0,
    }


def validate_metadata_profile_payload(
    payload: Any,
    *,
    diagnostics: dict[str, Any] | None = None,
) -> tuple[MetadataProfile, list[str], bool]:
    warnings: list[str] = []
    if not isinstance(payload, dict):
        warnings.append("metadata_profile_payload_not_object")
        if diagnostics is not None:
            diagnostics["result"] = "fallback"
        return default_metadata_profile(), warnings, True

    if diagnostics is not None:
        diagnostics["payload_summary"] = summarize_metadata_profile_payload(payload)

    if _contains_dangerous_token(payload):
        warnings.append("metadata_profile_rejected_dangerous_token")
        if diagnostics is not None:
            diagnostics["result"] = "dangerous_token_rejected"
        return default_metadata_profile(), warnings, True

    try:
        profile = MetadataProfile.model_validate(payload)
    except ValidationError as exc:
        warnings.append("metadata_profile_schema_validation_failed")
        if diagnostics is not None:
            diagnostics["result"] = "schema_validation_failed"
            diagnostics["errors"] = exc.errors()
        return default_metadata_profile(), warnings, True

    if diagnostics is not None:
        diagnostics["result"] = "accepted"
    return profile, warnings, False
