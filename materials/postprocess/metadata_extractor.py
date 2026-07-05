from __future__ import annotations

from ..schemas import MaterialType, Subject


def extract_title_from_markdown(markdown: str) -> str | None:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or None
    return None


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def guess_subject_from_filename(filename: str) -> Subject:
    name = filename.lower()
    if _contains_any(
        name,
        [
            "math",
            "数学",
            "高数",
            "高等数学",
            "线代",
            "线性代数",
            "概率",
            "概率统计",
            "函数",
            "极限",
            "导数",
            "微分",
            "积分",
            "级数",
            "无穷级数",
            "数列",
            "三角",
            "复数",
            "向量",
            "立体几何",
            "解析几何",
            "常微分方程",
            "多元函数",
            "二重积分",
        ],
    ):
        return Subject.MATH
    if _contains_any(name, ["politics", "政治", "马原", "毛中特", "毛概", "史纲", "思修", "时政"]):
        return Subject.POLITICS
    if _contains_any(name, ["408", "计算机", "数据结构", "计组", "组成原理", "操作系统", "计网", "计算机网络"]):
        return Subject.COMPUTER_408
    if _contains_any(name, ["english", "英语", "翻译", "阅读", "作文", "单词", "完形", "新题型"]):
        return Subject.ENGLISH
    return Subject.UNKNOWN


def guess_material_type_from_filename(filename: str) -> MaterialType:
    name = filename.lower()
    if _contains_any(name, ["textbook", "教材", "课本", "教科书", "主册"]):
        return MaterialType.TEXTBOOK
    if _contains_any(name, ["lecture", "讲义", "课件", "强化班", "基础班", "冲刺班", "笔记", "note"]):
        return MaterialType.LECTURE
    if _contains_any(name, ["exercise", "习题", "练习", "题集", "真题", "试题", "试卷", "考试", "错题", "exam", "wrong"]):
        return MaterialType.EXERCISE
    return MaterialType.UNKNOWN


def infer_subject_from_markdown(markdown: str) -> Subject:
    text = markdown.lower()
    if _contains_any(text, ["学科：数学", "高等数学", "罗尔定理", "拉格朗日", "极限", "导数", "积分", "级数"]):
        return Subject.MATH
    if _contains_any(text, ["学科：政治", "主要矛盾", "马原", "毛中特", "史纲", "思修", "时政"]):
        return Subject.POLITICS
    if _contains_any(text, ["学科：408", "数据结构", "计算机", "计网", "操作系统", "组成原理"]):
        return Subject.COMPUTER_408
    if _contains_any(text, ["学科：英语", "翻译", "阅读理解", "作文", "单词"]):
        return Subject.ENGLISH
    return Subject.UNKNOWN


def infer_material_type_from_markdown(markdown: str) -> MaterialType:
    text = markdown.lower()
    if _contains_any(text, ["资料类型：教材", "textbook", "教材", "课本", "教科书"]):
        return MaterialType.TEXTBOOK
    if _contains_any(text, ["资料类型：讲义", "lecture", "讲义", "课件", "强化班", "基础班", "冲刺班", "笔记"]):
        return MaterialType.LECTURE
    if _contains_any(text, ["资料类型：习题", "exercise", "习题", "练习", "真题", "试题", "试卷", "错题"]):
        return MaterialType.EXERCISE
    return MaterialType.UNKNOWN
