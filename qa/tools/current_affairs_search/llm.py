from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from dotenv import load_dotenv

from ...usage_tracking import notify_usage
from .constants import ROOT


def current_affairs_model_name() -> str:
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    return (
        os.getenv("CURRENT_AFFAIRS_MODEL")
        or os.getenv("ROUTER_MODEL")
        or "deepseek-v4-flash"
    )


def make_current_affairs_client():
    load_dotenv(ROOT / ".env", encoding="utf-8-sig")
    api_key = (
        os.getenv("CURRENT_AFFAIRS_API_KEY")
        or os.getenv("ROUTER_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
    )
    base_url = (
        os.getenv("CURRENT_AFFAIRS_BASE_URL")
        or os.getenv("ROUTER_BASE_URL")
        or os.getenv("DEEPSEEK_BASE_URL")
    )
    if not api_key or not base_url:
        raise RuntimeError("请先在 .env 中设置 DEEPSEEK_API_KEY 和 DEEPSEEK_BASE_URL，或 CURRENT_AFFAIRS_API_KEY/CURRENT_AFFAIRS_BASE_URL。")
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url=base_url)


def chat_current_affairs_text(
    system_prompt: str,
    user_payload: dict[str, Any],
    *,
    usage_name: str,
    temperature: float = 0.1,
    json_mode: bool = False,
) -> str:
    client = make_current_affairs_client()
    model = current_affairs_model_name()
    started = time.perf_counter()
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        "temperature": temperature,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**payload)
    notify_usage(
        kind="chat",
        name=usage_name,
        model=model,
        response=response,
        started_at=started,
        tool_name="get_current_affairs",
        provider="deepseek",
    )
    return response.choices[0].message.content or ""


def parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    match = re.search(r"\{.*\}", stripped, flags=re.S)
    if not match:
        raise ValueError(f"Model did not return JSON: {text}")
    return json.loads(match.group(0))
