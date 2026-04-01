from __future__ import annotations

from typing import Any


def build_headers_summary(
    current_user_agent: str | None,
    current_headers: dict[str, Any] | None,
) -> dict[str, Any]:
    headers = current_headers or {}

    return {
        "current_user_agent": current_user_agent,
        "current_headers": headers,
        "accept_header": headers.get("accept"),
        "accept_language_header": headers.get("accept-language"),
        "accept_encoding_header": headers.get("accept-encoding"),
        "referer_header": headers.get("referer"),
        "origin_header": headers.get("origin"),
        "fetch_site_header": headers.get("sec-fetch-site"),
        "fetch_mode_header": headers.get("sec-fetch-mode"),
        "fetch_dest_header": headers.get("sec-fetch-dest"),
    }