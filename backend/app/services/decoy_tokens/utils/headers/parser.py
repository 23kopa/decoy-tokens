from __future__ import annotations

from typing import Any

from user_agents import parse as parse


def parse_accept_language(value: str | None) -> str | None:
    if not value:
        return None

    parts = [part.strip() for part in value.split(",") if part.strip()]
    if not parts:
        return None

    primary = parts[0].split(";")[0].strip()
    return primary or None


def detect_device_type(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    ua = parse(user_agent)

    if ua.is_bot:
        return "Bot"
    if ua.is_mobile:
        return "Mobile"
    if ua.is_tablet:
        return "Tablet"
    if ua.is_pc:
        return "Desktop"

    return "Unknown"


def _join_version(parts: Any) -> str:
    if not parts:
        return ""
    return ".".join(str(part) for part in parts if part is not None)


def format_browser(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    ua = parse(user_agent)
    family = ua.browser.family
    version = _join_version(ua.browser.version)

    if family and version:
        major = version.split(".")[0]
        return f"{family} {major}"

    return family or None


def format_os(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    ua = parse(user_agent)
    family = ua.os.family
    version = _join_version(ua.os.version)

    if family and version:
        return f"{family} {version}"

    return family or None


def parse_client_profile(headers: dict[str, Any]) -> dict[str, str | None]:
    user_agent = headers.get("user-agent")
    accept_language = headers.get("accept-language")

    return {
        "device": detect_device_type(user_agent),
        "browser": format_browser(user_agent),
        "os": format_os(user_agent),
        "language": parse_accept_language(accept_language),
    }