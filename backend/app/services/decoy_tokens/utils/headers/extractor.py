from typing import Any, Dict
from starlette.requests import Request

ALLOWED_HEADERS = {
    "x-forwarded-for",                # Реальный IP через прокси
    "x-real-ip",                      # Альтернативный IP
    "accept-language",                # Языки пользователя
    "dnt",                            # Запрет на отслеживание
    "user-agent",                     # Полный User-Agent
    "referer",                        # Откуда пришел пользователь
    "origin",                         # Источник запроса
    "host",                           # Хост запроса              
    "sec-ch-prefers-color-scheme",    # Темная/светлая тема
    "sec-ch-viewport-width",          # Ширина вьюпорта
    "sec-ch-viewport-height",         # Высота вьюпорта
}

def extract_headers(request: Request) -> dict[str, Any]:
    result = {}
    for key, value in request.headers.items():
        key_lower = key.lower()
        if key_lower in ALLOWED_HEADERS:
            result[key_lower] = value
    return result