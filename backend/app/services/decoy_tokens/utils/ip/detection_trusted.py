# backend/app/services/decoy_tokens/utils/ip/detection.py

from typing import Optional, Union, Dict, Any
from ipaddress import ip_address
from starlette.requests import Request

from .validation import is_public_ip, parse_trusted_proxies, get_ip_version
from .proxy import parse_proxy_chain


def get_client_ip(
    request: Request, 
    trusted_proxies: Optional[Union[set[str], list[str]]] = None
) -> Dict[str, Any]:

    result = {
        "detected_ip": None,        # Реальный IP клиента
        "detection_method": None,   # Как определили
        "direct_ip": None,          # Прямой IP соединения
        "proxy_chain": [],          # Цепочка прокси из X-Forwarded-For (список строк)
        "confidence": 1.0,          # Уверенность в определении
    }
    
    # Получаем прямой IP соединения
    direct_ip = request.client.host if request.client else None
    result["direct_ip"] = direct_ip
    
    if not direct_ip:
        return result

    # Если нет доверенных прокси - возвращаем прямой IP
    if not trusted_proxies:
        result["detected_ip"] = direct_ip
        result["detection_method"] = "direct"
        return result

    # Проверяем, доверяем ли мы этому IP
    trusted_networks = parse_trusted_proxies(trusted_proxies)
    try:
        remote_ip = ip_address(direct_ip)
        is_trusted = any(remote_ip in network for network in trusted_networks)
    except ValueError:
        is_trusted = False

    # Если IP не доверенный - возвращаем его как есть
    if not is_trusted:
        result["detected_ip"] = direct_ip
        result["detection_method"] = "Untrusted"
        return result

    # Получаем X-Real-IP если есть
    xri = request.headers.get("x-real-ip")
    if xri:
        result["x_real_ip"] = xri

    # Получаем и парсим X-Forwarded-For
    xff = request.headers.get("x-forwarded-for")
    if xff:
        # Получаем список строк IP-адресов
        proxy_chain = parse_proxy_chain(xff, return_format="list")
        result["proxy_chain"] = proxy_chain
        
        # Ищем первый публичный IP в цепочке
        for ip in proxy_chain:  # ip теперь строка, а не словарь
            if is_public_ip(ip):  # Используем функцию is_public_ip
                result["detected_ip"] = ip
                result["detection_method"] = "X-Forwarded-For"
                result["confidence"] = 0.95
                break
    
    # Если не нашли в XFF, пробуем X-Real-IP
    if not result["detected_ip"] and xri and is_public_ip(xri):
        result["detected_ip"] = xri
        result["detection_method"] = "X-Real-IP"
        result["confidence"] = 0.9
    
    # Если ничего не нашли, возвращаем прямой IP
    if not result["detected_ip"]:
        result["detected_ip"] = direct_ip
        result["detection_method"] = "Direct Fallback"
        result["confidence"] = 0.5
    
    print(f"DEBUG: direct_ip={direct_ip}")
    print(f"DEBUG: is_trusted={is_trusted}")
    print(f"DEBUG: xff={xff}")
    print(f"DEBUG: xri={xri}")
    print(f"DEBUG: result={result}")

    return result