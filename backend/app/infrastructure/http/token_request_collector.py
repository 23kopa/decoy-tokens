from datetime import datetime
from starlette.requests import Request
from typing import Optional, Union, Any

from ...services.decoy_tokens.utils.ip.detection import get_client_ip
from ...services.decoy_tokens.utils.ip.validation import get_ip_version
from ...services.decoy_tokens.utils.headers.extractor import extract_headers
from ...services.decoy_tokens.utils.geo.geoip import geo_service

async def collect_request_info(
    request: Request,
    trusted_proxies: Optional[Union[set[str], list[str]]] = None
) -> dict[str, Any]:

    # Получаем информацию об IP и прокси
    ip_data = get_client_ip(request, trusted_proxies)

    geo_info = {}
    if ip_data and ip_data.get("detected_ip"):
        geo_info = await geo_service.get_geo_info(ip_data["detected_ip"])
    
    browser_info = {
        k: v for k, v in request.query_params.items() 
        if k in ['screen', 'tz', 'timezone', 'language', 'platform', 'vendor']
    }

    # Получаем базовую информация
    info = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip_data": ip_data,
        "geo": geo_info,
        "direct_ip": request.client.host if request.client else None,
        "method": request.method,
        "path": request.url.path,
        "headers": extract_headers(request),
        "query_params": browser_info
    }

    # Добавляем порт клиента
    if request.client:
        info["client_port"] = request.client.port

    # Добавляем версию IP
    if ip_data and ip_data.get("detected_ip"):
        info["ip_version"] = get_ip_version(ip_data["detected_ip"])

    return info
