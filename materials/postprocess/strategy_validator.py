from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from .strategy_schema import CleaningStrategy


DANGEROUS_TOKENS = ("eval", "exec", "import", "subprocess", "os.system", "open(", "__")


def default_conservative_strategy(*, reason: str = "未获得可信结构策略") -> CleaningStrategy:
    return CleaningStrategy(
        document_profile={"subject": "unknown", "document_type": "unknown", "language": "zh", "confidence": 0.3},
        main_section_rule={
            "enabled": False,
            "target_level": 2,
            "marker_type": "none",
            "aliases": [],
            "number_styles": [],
            "requires_line_start": True,
            "requires_colon": False,
            "min_repeats": 2,
            "examples": [],
        },
        subsection_rules=[],
        fallback_policy={
            "if_main_sections_less_than": 2,
            "action": "keep_original_structure",
            "chunk_by": "length",
            "reason": reason,
        },
        strategy_source="default",
    )


def _contains_dangerous_token(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_dangerous_token(k) or _contains_dangerous_token(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_contains_dangerous_token(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in DANGEROUS_TOKENS)
    return False


def parse_strategy_payload(payload: str | dict[str, Any] | CleaningStrategy) -> tuple[dict[str, Any] | None, list[str]]:
    if isinstance(payload, CleaningStrategy):
        return payload.to_dict(), []
    if isinstance(payload, dict):
        return payload, []
    if not isinstance(payload, str):
        return None, ["strategy_payload_not_json_or_dict"]
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return None, ["strategy_payload_not_json"]
    if not isinstance(parsed, dict):
        return None, ["strategy_payload_not_object"]
    return parsed, []


def validate_cleaning_strategy(
    payload: str | dict[str, Any] | CleaningStrategy,
    *,
    fallback_source: str = "default",
) -> tuple[CleaningStrategy, list[str], bool]:
    warnings: list[str] = []
    data, parse_warnings = parse_strategy_payload(payload)
    warnings.extend(parse_warnings)
    if data is None:
        strategy = default_conservative_strategy(reason="strategy JSON 不合法")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    if _contains_dangerous_token(data):
        warnings.append("strategy_rejected_dangerous_token")
        strategy = default_conservative_strategy(reason="strategy 包含危险字段或内容")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    try:
        strategy = CleaningStrategy.model_validate(data)
    except ValidationError as exc:
        warnings.append("strategy_schema_validation_failed")
        warnings.extend(error["type"] for error in exc.errors()[:5])
        strategy = default_conservative_strategy(reason="strategy schema 校验失败")
        strategy.strategy_source = "default"
        return strategy, warnings, True

    if strategy.strategy_source == "default" and fallback_source in {"qwen", "local"}:
        strategy.strategy_source = fallback_source  # preserve source when payload omitted the optional field
    return strategy, warnings, False
