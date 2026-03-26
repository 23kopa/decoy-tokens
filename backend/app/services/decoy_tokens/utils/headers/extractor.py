from typing import Any, Dict
from starlette.requests import Request

ALLOWED_HEADERS = {
    # IP / proxy
    "x-forwarded-for",
    "x-real-ip",
    "forwarded",
    "x-forwarded-proto",
    "x-forwarded-host",
    "x-forwarded-port",
    "cf-connecting-ip",
    "cf-ipcountry",

    # Browser identity
    "user-agent",
    "accept-language",
    "accept",
    "accept-encoding",

    # Client hints
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
    "sec-ch-ua-platform-version",
    "sec-ch-ua-arch",
    "sec-ch-ua-bitness",
    "sec-ch-ua-full-version",
    "sec-ch-ua-full-version-list",

    # Navigation / fetch
    "sec-fetch-site",
    "sec-fetch-mode",
    "sec-fetch-user",
    "sec-fetch-dest",

    # Referrer
    "referer",
    "origin",

    # Behavior hints
    "dnt",
    "upgrade-insecure-requests",

    # Prefetch / scanners
    "purpose",
    "x-purpose",
    "sec-purpose",

    # UI hints
    "sec-ch-prefers-color-scheme",
    "sec-ch-viewport-width",
    "sec-ch-viewport-height",

    # Host
    "host",
}

def extract_headers(request: Request) -> dict[str, Any]:
    result = {}
    for key, value in request.headers.items():
        key_lower = key.lower()
        if key_lower in ALLOWED_HEADERS:
            result[key_lower] = value
    return result