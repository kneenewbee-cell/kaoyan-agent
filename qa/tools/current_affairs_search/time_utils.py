from __future__ import annotations

from datetime import datetime, timedelta, timezone


def beijing_time_info() -> dict[str, str]:
    now = datetime.now(timezone(timedelta(hours=8)))
    return {
        "date": now.date().isoformat(),
        "datetime": now.isoformat(timespec="seconds"),
        "weekday": now.strftime("%A"),
        "timezone": "Asia/Shanghai",
    }
