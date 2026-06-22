"""materials/quality/confidence.py — 置信度计算工具。"""

from __future__ import annotations


def clamp_score(value: float) -> float:
    return max(0.0, min(1.0, round(float(value), 4)))


def status_from_score(score: float) -> str:
    if score >= 0.80:
        return "high"
    if score >= 0.60:
        return "medium"
    if score >= 0.40:
        return "low"
    return "failed"


def weighted_average(parts: dict[str, tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in parts.values())
    if total_weight <= 0:
        return 0.0
    return clamp_score(sum(score * weight for score, weight in parts.values()) / total_weight)
