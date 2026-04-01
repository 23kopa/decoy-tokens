from __future__ import annotations

from datetime import datetime


def build_timeline_summary(
    first_seen: datetime | None,
    last_seen: datetime | None,
    seen_count: int | None,
    is_first: bool,
) -> dict[str, object]:
    seen_count = seen_count or 0

    return {
        "first_seen": first_seen,
        "last_seen": last_seen,
        "seen_count": seen_count,
        "is_first": is_first,
        "is_repeat": seen_count > 1,
    }