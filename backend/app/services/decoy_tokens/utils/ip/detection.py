from typing import Optional, Union, Dict, Any
from starlette.requests import Request

from .validation import is_public_ip
from .proxy import parse_proxy_chain
from ...shared.logging import logger, log_ip_detection

def get_client_ip(
    request: Request, 
    trusted_proxies: Optional[Union[set[str], list[str]]] = None
) -> Dict[str, Any]:

    result = {
        "detected_ip": None,
        "detection_method": None,
        "direct_ip": None,
        "x_real_ip": None,
        "proxy_chain": [],
        "confidence": 1.0,
    }
    
    direct_ip = request.client.host if request.client else None
    result["direct_ip"] = direct_ip
    
    if not direct_ip:
        logger.warning("No direct IP found in request")
        return result

    xri = request.headers.get("x-real-ip")
    result["x_real_ip"] = xri
    if xri:
        logger.debug(f"X-Real-IP header present: {xri}")

    xff = request.headers.get("x-forwarded-for")
    ip_from_headers = None
    
    if xff:
        logger.debug(f"X-Forwarded-For header: {xff}")
        proxy_chain = parse_proxy_chain(xff, return_format="list")
        result["proxy_chain"] = proxy_chain
        logger.debug(f"Proxy chain: {proxy_chain}")

        for ip in proxy_chain:
            if is_public_ip(ip):
                ip_from_headers = ip
                result["detected_ip"] = ip
                result["detection_method"] = "X-Forwarded-For"
                result["confidence"] = 0.95
                logger.info(f"Found public IP in X-Forwarded-For: {ip}")
                break
    
    if not result["detected_ip"] and xri and is_public_ip(xri):
        ip_from_headers = xri
        result["detected_ip"] = xri
        result["detection_method"] = "X-Real-IP"
        result["confidence"] = 0.9
        logger.info(f"Found public IP in X-Real-IP: {xri}")
    
    if ip_from_headers:
        log_ip_detection(result)
        return result
    
    result["detected_ip"] = direct_ip
    result["detection_method"] = "Direct Fallback"
    result["confidence"] = 0.5
    
    logger.info(f"No proxy headers, using direct IP: {direct_ip}")
    
    return result