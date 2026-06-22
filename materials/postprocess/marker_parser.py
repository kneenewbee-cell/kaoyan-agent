"""通用行首结构标记解析器。"""

from __future__ import annotations

import re
from dataclasses import dataclass

CHINESE_NUMBER = "零〇一二三四五六七八九十百千万两"


@dataclass
class Marker:
    family: str
    title: str
    raw_marker: str
    alias: str | None = None
    number_text: str | None = None
    depth: int | None = None


def parse_label_ordinal_marker(line: str, aliases: list[str]) -> Marker | None:
    if not aliases:
        return None
    alias_pattern = "|".join(re.escape(alias) for alias in sorted(aliases, key=len, reverse=True))
    match = re.match(
        rf"^(?P<alias>{alias_pattern})(?P<number>[{CHINESE_NUMBER}]+|\d+)[：:]\s*(?P<title>\S.*)$",
        line.rstrip(),
    )
    if not match:
        return None
    raw = match.group(0)[: match.start("title")].rstrip()
    return Marker(
        family="label_ordinal_marker",
        title=line.rstrip(),
        raw_marker=raw,
        alias=match.group("alias"),
        number_text=match.group("number"),
        depth=1,
    )


def parse_decimal_outline_marker(line: str) -> Marker | None:
    match = re.match(r"^(?P<number>\d+(?:\.\d+)+)\s+(?P<title>\S.*)$", line.rstrip())
    if not match:
        return None
    number = match.group("number")
    return Marker("decimal_outline_marker", line.rstrip(), number, number_text=number, depth=number.count(".") + 1)


def parse_chinese_outline_marker(line: str) -> Marker | None:
    match = re.match(rf"^(?P<number>[{CHINESE_NUMBER}]+)、\s*(?P<title>\S.*)$", line.rstrip())
    if not match:
        return None
    return Marker("chinese_outline_marker", line.rstrip(), match.group("number") + "、", number_text=match.group("number"), depth=1)


def parse_arabic_outline_marker(line: str) -> Marker | None:
    match = re.match(r"^(?:（(?P<paren>\d+)）|(?P<number>\d+)(?P<suffix>[.、）]))\s*(?P<title>\S.*)$", line.rstrip())
    if not match:
        return None
    number = match.group("paren") or match.group("number")
    raw = f"（{number}）" if match.group("paren") else number + match.group("suffix")
    return Marker("arabic_outline_marker", line.rstrip(), raw, number_text=number, depth=1)


def parse_chapter_marker(line: str) -> Marker | None:
    match = re.match(
        rf"^第(?P<number>[{CHINESE_NUMBER}]+|\d+)(?P<unit>章|节|部分)\s*(?P<title>\S.*)$",
        line.rstrip(),
    )
    if not match:
        return None
    raw = f"第{match.group('number')}{match.group('unit')}"
    return Marker("chapter_marker", line.rstrip(), raw, number_text=match.group("number"), depth=1)


def parse_marker_for_rule(line: str, rule: dict) -> Marker | None:
    family = rule.get("family")
    if family == "label_ordinal_marker":
        return parse_label_ordinal_marker(line, list(rule.get("aliases", [])))
    if family == "decimal_outline_marker":
        marker = parse_decimal_outline_marker(line)
        observed_depth = rule.get("observed_depth")
        if marker and observed_depth and marker.depth != observed_depth:
            return None
        return marker
    if family == "chinese_outline_marker":
        return parse_chinese_outline_marker(line)
    if family == "arabic_outline_marker":
        return parse_arabic_outline_marker(line)
    if family == "chapter_marker":
        return parse_chapter_marker(line)
    if family == "letter_marker":
        match = re.match(r"^(?P<letter>[A-Za-z])[.、）]\s*(?P<title>\S.*)$", line.rstrip())
        if match:
            return Marker("letter_marker", line.rstrip(), match.group("letter"), number_text=match.group("letter"), depth=1)
    return None
