from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "data" / "raw" / "math" / "exam_papers"
REPORT_PATH = EXAM_ROOT / "math_topics_methods_split_report.json"

METHOD_ALIASES = {
    "Taylor 展开": "泰勒展开",
    "Taylor展开": "泰勒展开",
    "泰勒公式": "泰勒展开",
    "麦克劳林公式": "泰勒展开",
    "幂级数展开": "泰勒展开",
    "对数展开": "泰勒展开",
    "无穷小展开": "泰勒展开",
    "初等函数展开": "泰勒展开",
    "洛必达": "洛必达法则",
    "洛必达法则": "洛必达法则",
    "罗必塔法则": "洛必达法则",
    "罗必塔": "洛必达法则",
    "分部积分": "分部积分",
    "换元积分": "换元积分",
    "换元积分法": "换元积分",
    "积分换元": "换元积分",
    "变量代换": "换元积分",
    "积分变量替换": "换元积分",
    "定积分变量代换": "换元积分",
    "三角代换": "换元积分",
    "反三角函数代换": "换元积分",
    "隐函数求导": "隐函数求导",
    "复合函数求导": "复合函数求导",
    "复合求导": "复合函数求导",
    "多元复合函数求导": "复合函数求导",
    "链式法则": "链式法则",
    "乘积求导": "乘积求导",
    "参数方程求导": "参数方程求导",
    "对数求导": "对数求导",
    "变限积分求导": "变限积分求导",
    "变上限积分求导": "变限积分求导",
    "求导公式": "求导公式",
    "极坐标变换": "极坐标变换",
    "交换积分次序": "交换积分次序",
    "积分次序交换": "交换积分次序",
    "二重积分换序": "交换积分次序",
    "换序积分": "交换积分次序",
    "区域变换": "积分区域变换",
    "二重积分区域变换": "积分区域变换",
    "比较判别法": "比较判别法",
    "比值判别法": "比值判别法",
    "夹逼定理": "夹逼定理",
    "根式有理化": "有理化",
    "有理化": "有理化",
    "拉格朗日乘数法": "拉格朗日乘数法",
    "拉格朗日乘子法": "拉格朗日乘数法",
    "拉格朗日乘子": "拉格朗日乘数法",
    "Hessian判别": "Hessian判别",
    "Hessian 判别": "Hessian判别",
    "二阶导数判别法": "二阶导数判别法",
    "二阶偏导数判别法": "二阶偏导数判别法",
    "驻点判别": "驻点判别",
    "极值判别": "极值判别",
    "待定系数法": "待定系数法",
    "降阶法": "降阶法",
    "降阶": "降阶法",
    "积分因子": "积分因子",
    "柱壳法": "柱壳法",
    "微元法": "微元法",
    "截面法": "截面法",
}

TOPIC_BACKFILL = {
    "泰勒展开": "极限",
    "洛必达法则": "极限",
    "夹逼定理": "极限",
    "有理化": "极限",
    "比较判别法": "敛散性",
    "比值判别法": "敛散性",
    "分部积分": "积分",
    "换元积分": "积分",
    "隐函数求导": "导数",
    "复合函数求导": "导数",
    "链式法则": "导数",
    "乘积求导": "导数",
    "参数方程求导": "导数",
    "对数求导": "导数",
    "变限积分求导": "导数",
    "求导公式": "导数",
    "极坐标变换": "二重积分",
    "交换积分次序": "二重积分",
    "积分区域变换": "二重积分",
    "拉格朗日乘数法": "条件极值",
    "Hessian判别": "多元函数极值",
    "二阶导数判别法": "极值与最值",
    "二阶偏导数判别法": "多元函数极值",
    "驻点判别": "极值与最值",
    "极值判别": "极值与最值",
    "待定系数法": "微分方程",
    "降阶法": "微分方程",
    "积分因子": "微分方程",
    "柱壳法": "定积分",
    "微元法": "定积分",
    "截面法": "定积分",
}

METHOD_SCAN_PATTERNS = [
    (re.compile(re.escape(raw)), normalized)
    for raw, normalized in sorted(METHOD_ALIASES.items(), key=lambda item: len(item[0]), reverse=True)
]

BROAD_TOPICS = {"历年真题", "函数", "综合题", "计算"}


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = str(value).strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    return None


def read_yaml_list(frontmatter: list[str], key: str) -> list[str]:
    values: list[str] = []
    for index, line in enumerate(frontmatter):
        if line.strip() == f"{key}: []":
            return []
        if line.strip() == f"{key}:":
            cursor = index + 1
            while cursor < len(frontmatter) and frontmatter[cursor].startswith("  - "):
                values.append(frontmatter[cursor][4:].strip())
                cursor += 1
            return values
    return []


def render_yaml_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:"] + [f"  - {value}" for value in values]


def replace_topic_method_lists(frontmatter: list[str], topics: list[str], methods: list[str]) -> list[str]:
    output: list[str] = []
    inserted = False
    index = 0
    while index < len(frontmatter):
        line = frontmatter[index]
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key in {"topics", "methods"}:
            if not inserted:
                output.extend(render_yaml_list("topics", topics))
                output.extend(render_yaml_list("methods", methods))
                inserted = True
            index += 1
            while index < len(frontmatter) and frontmatter[index].startswith("  - "):
                index += 1
            continue
        if not inserted and key == "difficulty":
            output.extend(render_yaml_list("topics", topics))
            output.extend(render_yaml_list("methods", methods))
            inserted = True
        output.append(line)
        index += 1
    if not inserted:
        output.extend(render_yaml_list("topics", topics))
        output.extend(render_yaml_list("methods", methods))
    return output


def infer_topics_from_text(text: str) -> list[str]:
    rules = [
        ("二重积分", ["二重积分", "\\iint", "交换积分次序"]),
        ("定积分", ["定积分", "旋转体", "曲边梯形", "\\int_"]),
        ("不定积分", ["不定积分", "+ C", "+C"]),
        ("极限", ["极限", "\\lim"]),
        ("无穷小比较", ["等价无穷小", "无穷小", "同阶", "高阶"]),
        ("连续性", ["连续"]),
        ("导数", ["导数", "求导", "\\mathrm{d}y", "切线", "法线", "边际", "弹性"]),
        ("偏导数", ["偏导", "\\partial"]),
        ("多元函数极值", ["多元函数", "驻点", "Hessian", "条件极值"]),
        ("级数", ["级数", "\\sum"]),
        ("幂级数", ["幂级数", "收敛半径", "收敛域"]),
        ("微分方程", ["微分方程", "通解"]),
        ("矩阵", ["矩阵"]),
        ("线性方程组", ["线性方程组", "基础解系"]),
        ("向量组线性相关性", ["向量组", "线性相关", "线性无关"]),
        ("特征值与特征向量", ["特征值", "特征向量"]),
        ("行列式", ["行列式", "范德蒙"]),
        ("概率", ["概率", "事件", "古典概型", "条件概率"]),
        ("随机变量分布", ["随机变量", "分布函数", "概率密度", "联合分布"]),
        ("数学期望", ["数学期望", "期望"]),
        ("方差", ["方差"]),
        ("正态分布", ["正态分布"]),
        ("置信区间", ["置信区间", "置信度"]),
        ("假设检验", ["假设检验"]),
    ]
    topics: list[str] = []
    for label, needles in rules:
        if any(needle in text for needle in needles):
            topics.append(label)
    return dedupe(topics)


def infer_methods_from_text(text: str) -> list[str]:
    methods: list[str] = []
    if "方程" in text and "确定" in text and ("\\mathrm{d}y" in text or "dy" in text or "y'" in text):
        methods.append("隐函数求导")
    if "参数方程" in text and ("导数" in text or "切线" in text or "法线" in text):
        methods.append("参数方程求导")
    if "极坐标" in text and ("二重积分" in text or "\\iint" in text or "累次积分" in text):
        methods.append("极坐标变换")
    return methods


def split_topics_methods(topics: list[str], methods: list[str], text: str) -> tuple[list[str], list[str], list[str]]:
    new_topics: list[str] = []
    new_methods = list(methods)
    moved: list[str] = []

    for topic in topics:
        normalized = METHOD_ALIASES.get(topic)
        if normalized:
            new_methods.append(normalized)
            moved.append(f"{topic}->{normalized}")
        else:
            new_topics.append(topic)

    for pattern, normalized in METHOD_SCAN_PATTERNS:
        if pattern.search(text):
            new_methods.append(normalized)
    new_methods.extend(infer_methods_from_text(text))

    new_topics = dedupe(new_topics)
    new_methods = dedupe(new_methods)

    if not new_topics or all(topic in BROAD_TOPICS for topic in new_topics):
        inferred = infer_topics_from_text(text)
        new_topics = dedupe([topic for topic in new_topics if topic not in BROAD_TOPICS] + inferred)

    if not new_topics:
        for method in new_methods:
            backfill = TOPIC_BACKFILL.get(method)
            if backfill:
                new_topics.append(backfill)
        new_topics = dedupe(new_topics)

    if not new_topics:
        new_topics = ["综合题"]

    return new_topics, new_methods, moved


def update_card(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    split = split_frontmatter(text)
    if split is None:
        return None
    frontmatter, body = split
    old_topics = read_yaml_list(frontmatter, "topics")
    old_methods = read_yaml_list(frontmatter, "methods")
    new_topics, new_methods, moved = split_topics_methods(old_topics, old_methods, body)
    new_frontmatter = replace_topic_method_lists(frontmatter, new_topics, new_methods)
    new_text = "---\n" + "\n".join(new_frontmatter) + "\n---\n" + body.rstrip() + "\n"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return {
        "question_id": next((line.split(":", 1)[1].strip() for line in frontmatter if line.startswith("question_id:")), ""),
        "topics": new_topics,
        "methods": new_methods,
        "moved": moved,
        "changed": new_text != text,
    }


def update_jsonl(path: Path, card_updates: dict[str, dict[str, Any]]) -> int:
    if not path.exists():
        return 0
    rows: list[dict[str, Any]] = []
    changed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        update = card_updates.get(str(row.get("question_id", "")))
        if update:
            if row.get("topics") != update["topics"] or row.get("methods") != update["methods"]:
                changed += 1
            row["topics"] = update["topics"]
            row["methods"] = update["methods"]
        rows.append(row)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    changed_cards = 0
    changed_rows = 0
    moved_counter: Counter[str] = Counter()
    methods_counter: Counter[str] = Counter()
    by_exam: dict[str, int] = defaultdict(int)
    empty_methods = 0
    card_updates_by_year: dict[Path, dict[str, dict[str, Any]]] = defaultdict(dict)

    for exam_type in ("math1", "math2", "math3"):
        for card_path in sorted((EXAM_ROOT / exam_type).glob("*/questions/q*.md")):
            update = update_card(card_path)
            if update is None:
                continue
            qid = update["question_id"]
            year_dir = card_path.parents[1]
            card_updates_by_year[year_dir][qid] = update
            if update["changed"]:
                changed_cards += 1
                by_exam[exam_type] += 1
            if not update["methods"]:
                empty_methods += 1
            for moved in update["moved"]:
                moved_counter[moved] += 1
            for method in update["methods"]:
                methods_counter[method] += 1

    for year_dir, updates in sorted(card_updates_by_year.items()):
        changed_rows += update_jsonl(year_dir / "questions.jsonl", updates)

    report = {
        "changed_cards": changed_cards,
        "changed_jsonl_rows": changed_rows,
        "changed_cards_by_exam": dict(sorted(by_exam.items())),
        "moved_topic_to_method_counts": dict(moved_counter.most_common()),
        "method_counts": dict(methods_counter.most_common()),
        "cards_without_methods": empty_methods,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
