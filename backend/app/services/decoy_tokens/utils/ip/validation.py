# backend/app/services/decoy_tokens/utils/ip/validation.py

import ipaddress
from typing import Optional, Union
from ipaddress import ip_network, ip_address
from functools import lru_cache


@lru_cache(maxsize=1024)
def is_public_ip(ip: str) -> bool:
    """Проверяет, является ли IP публичным."""
    if not ip:
        return False
    
    try:
        obj = ipaddress.ip_address(ip)
        return not (
            obj.is_private 
            or obj.is_loopback 
            or obj.is_reserved 
            or obj.is_multicast 
            or obj.is_link_local
        )
    except ValueError:
        return False


def parse_trusted_proxies(proxies: Optional[Union[set[str], list[str]]]) -> list:
    """Парсит список доверенных прокси в объекты ip_network."""
    networks = []
    if not proxies:
        return networks

    for proxy in proxies:
        try:
            if '/' in proxy:
                networks.append(ip_network(proxy))
            else:
                networks.append(ip_network(f"{proxy}/32"))
        except ValueError:
            continue
    
    return networks


def get_ip_version(ip: str) -> Optional[str]:
    """Определяет версию IP (IPv4 или IPv6)."""
    if not ip:
        return None
    
    try:
        addr = ipaddress.ip_address(ip)
        return f"IPv{addr.version}"
    except ValueError:
        return None