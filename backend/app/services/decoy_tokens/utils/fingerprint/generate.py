import hashlib
from typing import Any, Dict

def generate_fingerprint(request_info: dict[str, Any]) -> str:

    headers = request_info.get("headers", {})
    query = request_info.get("query_params", {})
    
    # Только стабильные характеристики браузера
    components = [
        headers.get("user-agent") or '',
        headers.get("accept-language") or '',
        headers.get("dnt") or '',
        headers.get("sec-ch-prefers-color-scheme") or '',
        query.get("screen") or '',
        query.get("tz") or '',
        query.get("timezone") or '',
    ]
    
    raw_string = '|'.join(components)
    return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()