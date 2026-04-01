from __future__ import annotations

from typing import Any

from backend.app.web.routes.api.v1.events.schemas import EventIpHistoryItem


def build_ip_history(items: list[dict[str, Any]] | None) -> list[EventIpHistoryItem]:
    if not items:
        return []

    result: list[EventIpHistoryItem] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        if "timestamp" not in item:
            continue

        result.append(
            EventIpHistoryItem(
                ip=item.get("ip"),
                timestamp=item["timestamp"],
                geo=item.get("geo") or {},
                asn=item.get("asn"),
                org=item.get("org"),
                connection_type=item.get("connection_type"),
            )
        )

    return result


def build_history_summary(
    first_ip: str | None,
    last_ip: str | None,
    unique_ip_count: int,
    ip_history: list[EventIpHistoryItem],
) -> dict[str, object]:
    return {
        "first_ip": first_ip,
        "last_ip": last_ip,
        "ip_history": ip_history,
        "unique_ip_count": unique_ip_count or 0,
        "has_ip_changes": (unique_ip_count or 0) > 1 or len(ip_history) > 0,
    }