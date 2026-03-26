from typing import Any


def parse_accept_language(value: str | None) -> str | None:
    if not value:
        return None

    first = value.split(",")[0].strip()
    return first.split(";")[0].strip() or None


def detect_device_type(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    ua = user_agent.lower()

    if "bot" in ua or "spider" in ua or "crawler" in ua:
        return "Bot"
    if "ipad" in ua or "tablet" in ua:
        return "Tablet"
    if "iphone" in ua or "android" in ua or "mobile" in ua:
        return "Mobile"
    return "Desktop"


def format_browser(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    rules = [
        ("Firefox/", "Firefox"),
        ("Edg/", "Edge"),
        ("Chrome/", "Chrome"),
        ("OPR/", "Opera"),
        ("Version/", "Safari"),
    ]

    for marker, name in rules:
        if marker in user_agent:
            try:
                version = user_agent.split(marker, 1)[1].split()[0].split(".")[0]
                return f"{name} {version}"
            except Exception:
                return name

    return None


def format_os(user_agent: str | None) -> str | None:
    if not user_agent:
        return None

    ua = user_agent

    if "Ubuntu" in ua:
        return "Ubuntu Linux"
    if "Windows NT 10.0" in ua:
        return "Windows 10/11"
    if "Windows NT 6.3" in ua:
        return "Windows 8.1"
    if "Windows NT 6.1" in ua:
        return "Windows 7"
    if "Android" in ua:
        return "Android"
    if "iPhone" in ua:
        return "iPhone iOS"
    if "iPad" in ua:
        return "iPadOS"
    if "Mac OS X" in ua:
        return "macOS"
    if "Linux" in ua:
        return "Linux"

    return None


def parse_client_profile(user_agent: str | None, headers: dict[str, Any] | None) -> dict[str, str | None]:
    headers = headers or {}
    accept_language = headers.get("accept-language")

    return {
        "device": detect_device_type(user_agent),
        "browser": format_browser(user_agent),
        "os": format_os(user_agent),
        "language": parse_accept_language(accept_language),
    }