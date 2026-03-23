import pytest
from typing import Dict, List, Any

@pytest.fixture
def public_ips() -> Dict[str, str]:
    """Публичные IP адреса для тестов"""
    return {
        "google_dns": "8.8.8.8",
        "cloudflare_dns": "1.1.1.1",
        "yandex_dns": "77.88.55.77",
        "google_ipv6": "2001:4860:4860::8888",
        "cloudflare_ipv6": "2606:4700:4700::1111",
    }


@pytest.fixture
def private_ips() -> Dict[str, str]:
    """Приватные/специальные IP адреса"""
    return {
        "localhost": "127.0.0.1",
        "private_a": "10.0.0.1",
        "private_b": "172.16.0.1",
        "private_c": "192.168.1.1",
        "link_local": "169.254.1.1",
        "multicast": "224.0.0.1",
        "reserved": "240.0.0.1",
        "ipv6_private": "fd00::1",
        "ipv6_loopback": "::1",
    }


@pytest.fixture
def invalid_ips() -> List[str]:
    """Невалидные IP адреса"""
    return [
        "not-an-ip",
        "256.256.256.256",
        "1.2.3.4.5",
        "abc.def.ghi.jkl",
        "",
        None,
    ]


@pytest.fixture
def xff_scenarios() -> List[Dict[str, Any]]:
    """Сценарии для X-Forwarded-For заголовков"""
    return [
        {
            "name": "single_ip",
            "xff": "8.8.8.8",
            "expected_list": ["8.8.8.8"],
            "expected_dict": [
                {"position": 1, "ip": "8.8.8.8", "is_public": True, "version": "IPv4"}
            ]
        },
        {
            "name": "chain_with_private",
            "xff": "8.8.8.8, 10.0.0.1, 192.168.1.1",
            "expected_list": ["8.8.8.8", "10.0.0.1", "192.168.1.1"],
            "expected_dict": [
                {"position": 1, "ip": "8.8.8.8", "is_public": True, "version": "IPv4"},
                {"position": 2, "ip": "10.0.0.1", "is_public": False, "version": "IPv4"},
                {"position": 3, "ip": "192.168.1.1", "is_public": False, "version": "IPv4"},
            ]
        },
        {
            "name": "with_spaces",
            "xff": "8.8.8.8 , 1.1.1.1 , 4.4.4.4",
            "expected_list": ["8.8.8.8", "1.1.1.1", "4.4.4.4"],
        },
        {
            "name": "empty",
            "xff": "",
            "expected_list": [],
            "expected_dict": [],
        },
        {
            "name": "none",
            "xff": None,
            "expected_list": [],
            "expected_dict": [],
        }
    ]


@pytest.fixture
def detection_scenarios() -> List[Dict[str, Any]]:
    """Сценарии для определения IP клиента"""
    return [
        {
            "name": "direct_no_headers",
            "direct_ip": "127.0.0.1",
            "headers": {},
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "127.0.0.1",
                "detection_method": "Direct Fallback",
                "confidence": 0.5,
                "direct_ip": "127.0.0.1",
                "proxy_chain": []
            }
        },
        {
            "name": "xff_single_public",
            "direct_ip": "10.0.0.1",
            "headers": {"x-forwarded-for": "8.8.8.8"},
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "8.8.8.8",
                "detection_method": "X-Forwarded-For",
                "confidence": 0.95,
                "proxy_chain": ["8.8.8.8"]
            }
        },
        {
            "name": "xff_chain_first_public",
            "direct_ip": "192.168.1.1",
            "headers": {"x-forwarded-for": "8.8.8.8, 10.0.0.1, 192.168.1.1"},
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "8.8.8.8",
                "detection_method": "X-Forwarded-For",
                "proxy_chain": ["8.8.8.8", "10.0.0.1", "192.168.1.1"]
            }
        },
        {
            "name": "xff_all_private",
            "direct_ip": "192.168.1.1",
            "headers": {"x-forwarded-for": "10.0.0.1, 192.168.1.1"},
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "192.168.1.1",  # fallback к direct
                "detection_method": "Direct Fallback",
                "proxy_chain": ["10.0.0.1", "192.168.1.1"]
            }
        },
        {
            "name": "x_real_ip",
            "direct_ip": "10.0.0.1",
            "headers": {"x-real-ip": "8.8.8.8"},
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "8.8.8.8",
                "detection_method": "X-Real-IP",
                "confidence": 0.9,
                "x_real_ip": "8.8.8.8"
            }
        },
        {
            "name": "xff_takes_priority",
            "direct_ip": "10.0.0.1",
            "headers": {
                "x-forwarded-for": "8.8.8.8",
                "x-real-ip": "1.1.1.1"
            },
            "trusted_proxies": None,
            "expected": {
                "detected_ip": "8.8.8.8",
                "detection_method": "X-Forwarded-For",
            }
        }
    ]