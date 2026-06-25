from __future__ import annotations

import re
from datetime import datetime
from typing import Any
from urllib.parse import urlparse


def unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value or "").strip().lower()
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def clean_html(text: str) -> str:
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_dates(text: str, default_year: str | None = None) -> list[str]:
    dates: list[str] = []
    for match in re.finditer(r"(20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})日?", text):
        dates.append(normal_date(match.group(1), match.group(2), match.group(3)))
    if default_year:
        for match in re.finditer(r"(?<!\d)(\d{1,2})月(\d{1,2})日", text):
            dates.append(normal_date(default_year, match.group(1), match.group(2)))
    return unique_strings([item for item in dates if item])


def normal_date(year: str, month: str, day: str) -> str:
    try:
        return datetime(int(year), int(month), int(day)).date().isoformat()
    except ValueError:
        return ""


def domain_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def domain_allowed(domain: str, allowed_domains: list[str]) -> bool:
    clean = domain.lower().removeprefix("www.")
    return any(clean == item or clean.endswith("." + item) for item in allowed_domains)
