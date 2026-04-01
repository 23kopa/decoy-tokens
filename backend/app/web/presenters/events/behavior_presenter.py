from __future__ import annotations

from typing import Any


def build_visit_kind_label(headers: dict[str, Any] | None) -> str | None:
    headers = headers or {}

    fetch_mode = headers.get("sec-fetch-mode")
    fetch_dest = headers.get("sec-fetch-dest")
    fetch_user = headers.get("sec-fetch-user")
    purpose = headers.get("purpose") or headers.get("x-purpose") or headers.get("sec-purpose")

    if purpose:
        return "Prefetch / Preview"

    if fetch_mode == "navigate" and fetch_dest == "document" and fetch_user == "?1":
        return "Открытие страницы"

    if fetch_dest in {"image", "script", "style"}:
        return "Загрузка ресурса"

    if fetch_mode or fetch_dest:
        return "Фоновый запрос"

    return None


def build_event_status_label(is_first: bool, additional_data: dict[str, Any] | None, seen_count: int) -> str:
    additional_data = additional_data or {}
    bot_info = additional_data.get("bot_info", {}) or {}

    if bot_info.get("is_bot"):
        return "Бот"
    if is_first:
        return "Первый"
    if seen_count > 1:
        return "Повтор"

    return "Событие"


def build_behavior_summary(
    headers: dict[str, Any] | None,
    is_first: bool,
    additional_data: dict[str, Any] | None,
    seen_count: int,
) -> dict[str, str | None]:
    return {
        "visit_kind_label": build_visit_kind_label(headers),
        "event_status_label": build_event_status_label(is_first, additional_data, seen_count),
    }