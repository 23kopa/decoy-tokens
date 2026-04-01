from __future__ import annotations

from typing import Any

from backend.app.services.decoy_tokens.utils.headers.parser import parse_client_profile


def build_client_summary(headers: dict[str, Any] | None) -> dict[str, str | None]:
    profile = parse_client_profile(headers or {})

    return {
        "current_browser": profile.get("browser"),
        "current_device": profile.get("device"),
        "current_os": profile.get("os"),
        "current_language": profile.get("language"),
    }