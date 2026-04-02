from typing import Optional, List, Dict, Any, Union, Literal, overload
from .validation import is_public_ip, get_ip_version
from ipaddress import ip_address, ip_network

@overload
def parse_proxy_chain(
    xff_header: Optional[str],
    return_format: Literal["list"] = "list"
) -> List[str]:
    ...


@overload
def parse_proxy_chain(
    xff_header: Optional[str],
    return_format: Literal["dict"]
) -> List[Dict[str, Any]]:
    ...

def is_trusted_proxy(ip: str, trusted_proxies: Optional[Union[set[str], list[str]]]) -> bool:
    if not trusted_proxies:
        return False

    try:
        candidate = ip_address(ip)
    except ValueError:
        return False

    for proxy in trusted_proxies:
        try:
            if "/" in proxy:
                if candidate in ip_network(proxy, strict=False):
                    return True
            else:
                if candidate == ip_address(proxy):
                    return True
        except ValueError:
            continue

    return False

def parse_proxy_chain(
    xff_header: Optional[str],
    return_format: Literal["list", "dict"] = "list"
) -> Union[List[str], List[Dict[str, Any]]]:
    if not xff_header:
        return []

    ips = [ip.strip() for ip in xff_header.split(",") if ip.strip()]

    if return_format == "list":
        return ips

    if return_format == "dict":
        chain: List[Dict[str, Any]] = []

        for i, ip in enumerate(ips):
            chain.append({
                "position": i + 1,
                "ip": ip,
                "is_public": is_public_ip(ip),
                "version": get_ip_version(ip),
            })

        return chain

    raise ValueError(f"Unsupported return_format: {return_format}")