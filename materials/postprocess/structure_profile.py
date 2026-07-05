from __future__ import annotations

from ..schemas import MaterialType


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def infer_exercise_kind(filename: str, markdown: str) -> str | None:
    text = f"{filename}\n{markdown}".lower()
    if _contains_any(text, ("真题", "试题", "试卷", "考试", "exam", "paper", "全国硕士研究生招生考试")):
        return "exam_paper"
    if _contains_any(text, ("错题", "wrong")):
        return "wrong_book_like"
    if _contains_any(text, ("例题", "典型例题", "worked example", "example")):
        return "worked_examples"
    if _contains_any(text, ("习题", "练习", "题集", "exercise", "problem set")):
        return "problem_set"
    return None


def infer_material_structure_profile(filename: str, markdown: str, material_type: MaterialType) -> dict[str, str]:
    if material_type != MaterialType.EXERCISE:
        return {}
    exercise_kind = infer_exercise_kind(filename, markdown) or "problem_set"
    return {"exercise_kind": exercise_kind}
