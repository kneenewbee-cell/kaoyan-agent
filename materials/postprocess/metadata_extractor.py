from __future__ import annotations

from ..schemas import MaterialType, Subject


def extract_title_from_markdown(markdown: str) -> str | None:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or None
    return None


def guess_subject_from_filename(filename: str) -> Subject:
    name = filename.lower()
    if any(keyword in name for keyword in ["math", "高数", "数学", "线代", "概率", "极限", "导数", "积分"]):
        return Subject.MATH
    if any(keyword in name for keyword in ["politics", "政治", "马原", "毛概", "史纲", "时政"]):
        return Subject.POLITICS
    if any(keyword in name for keyword in ["408", "计算机", "数据结构", "计组", "操作系统", "计网"]):
        return Subject.COMPUTER_408
    if any(keyword in name for keyword in ["english", "英语", "翻译", "阅读", "作文", "单词"]):
        return Subject.ENGLISH
    return Subject.UNKNOWN


def guess_material_type_from_filename(filename: str) -> MaterialType:
    name = filename.lower()
    if any(keyword in name for keyword in ["lecture", "讲义", "课件"]):
        return MaterialType.LECTURE
    if any(keyword in name for keyword in ["note", "笔记"]):
        return MaterialType.NOTE
    if any(keyword in name for keyword in ["exam", "真题", "试题", "试卷", "考试"]):
        return MaterialType.EXAM
    if any(keyword in name for keyword in ["wrong", "错题"]):
        return MaterialType.WRONG_BOOK
    if any(keyword in name for keyword in ["school", "学校", "院校", "招生"]):
        return MaterialType.SCHOOL_INFO
    return MaterialType.UNKNOWN


def infer_subject_from_markdown(markdown: str) -> Subject:
    text = markdown.lower()
    if any(keyword in text for keyword in ["学科：数学", "高等数学", "罗尔定理", "拉格朗日", "极限", "导数", "积分"]):
        return Subject.MATH
    if any(keyword in text for keyword in ["学科：政治", "主要矛盾", "马原", "毛概", "时政"]):
        return Subject.POLITICS
    if any(keyword in text for keyword in ["学科：408", "数据结构", "计算机", "计网", "操作系统"]):
        return Subject.COMPUTER_408
    if any(keyword in text for keyword in ["学科：英语", "翻译", "阅读理解", "作文", "单词"]):
        return Subject.ENGLISH
    return Subject.UNKNOWN


def infer_material_type_from_markdown(markdown: str) -> MaterialType:
    text = markdown.lower()
    if any(keyword in text for keyword in ["资料类型：讲义", "lecture", "讲义", "课件"]):
        return MaterialType.LECTURE
    if any(keyword in text for keyword in ["资料类型：笔记", "note", "笔记"]):
        return MaterialType.NOTE
    if any(keyword in text for keyword in ["资料类型：真题", "exam", "真题", "试题", "试卷"]):
        return MaterialType.EXAM
    if any(keyword in text for keyword in ["资料类型：错题", "wrong", "错题"]):
        return MaterialType.WRONG_BOOK
    if any(keyword in text for keyword in ["资料类型：院校信息", "school", "院校", "学校", "招生"]):
        return MaterialType.SCHOOL_INFO
    return MaterialType.UNKNOWN
