#!/usr/bin/env python3
"""Generate long raw-markdown stress materials for the materials pipeline."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "demo" / "raw_markdown_stress"


def _repeat_paragraph(seed: str, count: int) -> str:
    lines: list[str] = []
    for i in range(1, count + 1):
        lines.append(
            f"{seed} 第{i}段：本段用于模拟真实讲义中的连续正文，包含定义、条件、适用范围、"
            f"常见误区和解题时的判断依据。这里故意保持普通正文形态，不应被提升为标题。"
        )
    return "\n".join(lines)


def _math_knowledge_txt() -> str:
    sections = []
    for n, title in [
        ("一", "极限的计算"),
        ("二", "导数的定义与几何意义"),
        ("三", "中值定理"),
        ("四", "多元函数微分法"),
        ("五", "二重积分"),
        ("六", "无穷级数"),
    ]:
        sections.append(
            f"知识点{n}：{title}\n\n"
            "【考频】★★★★\n【难度】★★★☆\n\n"
            "核心概念\n"
            + _repeat_paragraph(title + "核心概念", 5)
            + "\n\n常用计算方法\n"
            + _repeat_paragraph(title + "方法", 4)
            + "\n\n经典例题\n"
            + _repeat_paragraph(title + "例题", 4)
            + "\n\n易错提醒\n"
            + _repeat_paragraph(title + "易错", 3)
        )
    return "考研数学高等数学长文知识点讲义\n\n" + "\n\n".join(sections) + "\n"


def _cs408_mixed_md() -> str:
    blocks = ["# 408 数据结构与组成原理混合长文\n"]
    modules = [
        ("一", "数据结构基础", ["考点1 线性表", "考点2 栈和队列", "一、树与二叉树", "二、图的遍历"]),
        ("二", "计算机组成原理", ["1. 存储系统", "2. 指令系统", "3. CPU 数据通路", "4. 总线与 IO"]),
        ("三", "操作系统", ["考点1 进程管理", "考点2 内存管理", "一、文件系统", "二、设备管理"]),
    ]
    for ordinal, title, subs in modules:
        blocks.append(f"模块{ordinal} {title}\n")
        for sub in subs:
            blocks.append(f"{sub}\n")
            blocks.append(_repeat_paragraph(sub, 5))
            blocks.append("| 项目 | 说明 | 易错点 |\n| --- | --- | --- |\n| 知识点一 | 表格内文字 | 不应当成标题 |\n")
            blocks.append("$$\nT(n)=O(n\\log n)\n$$\n")
    return "\n\n".join(blocks)


def _directory_interference_md() -> str:
    lines = [
        "# 高等数学目录干扰长文",
        "",
        "目录",
        "第一章 函数与极限 ........ 1",
        "第一节 函数 ........ 2",
        "第二节 极限 ........ 9",
        "第一章小结 ........ 18",
        "第二章 导数与微分 ........ 22",
        "第一节 导数概念 ........ 23",
        "第二节 导数应用 ........ 35",
        "",
    ]
    for chapter in ["第一章 函数与极限", "第二章 导数与微分", "第三章 积分学"]:
        lines.append(chapter)
        lines.append(_repeat_paragraph(chapter, 4))
        for section in ["第一节 基本概念", "第二节 计算方法"]:
            lines.append(section)
            lines.append("定义")
            lines.append(_repeat_paragraph(section + "定义", 3))
            lines.append("核心概念")
            lines.append(_repeat_paragraph(section + "核心", 3))
            lines.append("经典例题")
            lines.append(_repeat_paragraph(section + "例题", 3))
        lines.append(chapter.split()[0] + "小结")
        lines.append(_repeat_paragraph(chapter + "小结", 2))
    return "\n\n".join(lines) + "\n"


def _politics_outline_txt() -> str:
    parts = ["考研政治马原长文提纲\n"]
    for n, title in [("一", "唯物论"), ("二", "辩证法"), ("三", "认识论"), ("四", "历史观")]:
        parts.append(f"{n}、{title}\n")
        for label in ["核心概念", "常见题型", "易错提醒", "应用举例"]:
            parts.append(label)
            parts.append(_repeat_paragraph(title + label, 5))
    return "\n\n".join(parts) + "\n"


def _english_questions_txt() -> str:
    parts = ["考研英语阅读与写作题型长文\n"]
    for n, title in [("一", "主旨题"), ("二", "细节题"), ("三", "推断题"), ("四", "作文论证")]:
        parts.append(f"题型{n}：{title}\n")
        for label in ["命题特征", "解题步骤", "常见陷阱", "经典例题"]:
            parts.append(label)
            parts.append(_repeat_paragraph(title + label, 5))
            parts.append("Example: The argument is valid only when the hidden assumption is accepted.")
    return "\n\n".join(parts) + "\n"


def _existing_markdown_md() -> str:
    parts = ["# 线性代数长文讲义\n"]
    for chapter in ["第一章 行列式", "第二章 矩阵", "第三章 向量组", "第四章 特征值"]:
        parts.append(f"## {chapter}")
        for i in range(1, 4):
            parts.append(f"### {chapter[:3]}.{i} 小节标题")
            parts.append(_repeat_paragraph(chapter + str(i), 6))
    return "\n\n".join(parts) + "\n"


def _protection_md() -> str:
    return (
        "# 保护场景长文\n\n"
        "知识点一：函数极限\n\n"
        + _repeat_paragraph("函数极限", 6)
        + "\n\n| 列A | 列B |\n| --- | --- |\n| 知识点二：表格中的标题 | 不应转换 |\n| 核心概念 | 表格内短语 |\n\n"
        "```python\n# 知识点三：代码块里的标题\ntext = \"核心概念\"\nprint(text)\n```\n\n"
        "$$\n\\lim_{x\\to0}\\frac{\\sin x}{x}=1\n$$\n\n"
        "![limit-demo](assets/images/limit_demo.png)\n\n"
        "核心概念\n\n"
        + _repeat_paragraph("保护场景核心", 5)
        + "\n\n知识点二：导数应用\n\n"
        + _repeat_paragraph("导数应用", 6)
        + "\n\n经典例题\n\n"
        + _repeat_paragraph("导数例题", 5)
    )


def _table_heavy_md() -> str:
    parts = ["# 表格密集型资料\n"]
    for title in ["要点1：函数性质", "要点2：导数符号", "要点3：积分区域"]:
        parts.append(title)
        parts.append("| 名称 | 条件 | 结论 |\n| --- | --- | --- |")
        for i in range(1, 8):
            parts.append(f"| 知识点{i} | 条件{i} | 表格内容不应变标题 |")
        parts.append("注意事项")
        parts.append(_repeat_paragraph(title + "注意", 5))
    return "\n\n".join(parts) + "\n"


def _low_confidence_txt() -> str:
    return (
        "零散课堂记录长文\n\n"
        "知识点一：这只是开头出现一次的短句\n\n"
        + _repeat_paragraph("零散记录", 35)
        + "\n\n核心概念这个词偶尔出现在正文中，但不是独立标题。\n"
        + _repeat_paragraph("后续普通正文", 20)
    )


def _decimal_outline_md() -> str:
    parts = ["数学习题讲评 decimal outline 长文\n"]
    for prefix, title in [("1", "函数"), ("2", "极限"), ("3", "导数")]:
        parts.append(f"{prefix}. {title}")
        for sub in range(1, 4):
            parts.append(f"{prefix}.{sub} {title}小节{sub}")
            parts.append(_repeat_paragraph(f"{prefix}.{sub}", 6))
    return "\n\n".join(parts) + "\n"


def _bilingual_mixed_txt() -> str:
    parts = ["考研英语翻译与数学符号混合资料\n"]
    for n, title in [("一", "长难句结构"), ("二", "翻译中的逻辑关系"), ("三", "数学表达翻译")]:
        parts.append(f"专题{n}：{title}")
        parts.append("核心概念")
        parts.append(_repeat_paragraph(title + "中文说明", 4))
        parts.append("Common Patterns")
        for i in range(1, 6):
            parts.append(f"Pattern {i}: when A is proportional to B, translate the relation before details.")
        parts.append("经典例题")
        parts.append(_repeat_paragraph(title + "例题", 4))
    return "\n\n".join(parts) + "\n"


MATERIALS = {
    "stress_01_math_knowledge_long.txt": _math_knowledge_txt,
    "stress_02_cs408_mixed_numbering.md": _cs408_mixed_md,
    "stress_03_directory_interference.md": _directory_interference_md,
    "stress_04_politics_outline_long.txt": _politics_outline_txt,
    "stress_05_english_question_types.txt": _english_questions_txt,
    "stress_06_existing_markdown_long.md": _existing_markdown_md,
    "stress_07_protection_blocks.md": _protection_md,
    "stress_08_table_heavy.md": _table_heavy_md,
    "stress_09_low_confidence.txt": _low_confidence_txt,
    "stress_10_decimal_outline.md": _decimal_outline_md,
    "stress_11_bilingual_mixed.txt": _bilingual_mixed_txt,
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, builder in MATERIALS.items():
        path = OUT_DIR / filename
        path.write_text(builder(), encoding="utf-8", newline="\n")
        print(f"{path} chars={len(path.read_text(encoding='utf-8'))}")


if __name__ == "__main__":
    main()
