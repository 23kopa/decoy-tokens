# backend/tests/conftest.py

import pytest
from typing import Dict, List, Any

@pytest.fixture
def public_ips() -> Dict[str, str]:
    return {
        "google_dns": "8.8.8.8",
        "cloudflare_dns": "1.1.1.1",
        "yandex_dns": "77.88.55.77",
        "google_ipv6": "2001:4860:4860::8888",
        "cloudflare_ipv6": "2606:4700:4700::1111",
    }

@pytest.fixture
def private_ips() -> Dict[str, str]:
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
    ]

@pytest.fixture
def mock_geoip_responses() -> Dict[str, Any]:
    return {
        "ip-api": {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "region": "California",
            "regionName": "California",
            "city": "Mountain View",
            "zip": "94043",
            "lat": 37.4056,
            "lon": -122.0775,
            "timezone": "America/Los_Angeles",
            "isp": "Google LLC",
            "org": "Google LLC",
            "as": "AS15169 Google LLC",
            "query": "8.8.8.8"
        },
        "ipinfo": {
            "ip": "8.8.8.8",
            "city": "Mountain View",
            "region": "California",
            "country": "US",
            "loc": "37.4056,-122.0775",
            "postal": "94043",
            "timezone": "America/Los_Angeles",
            "asn": {
                "asn": "AS15169",
                "name": "Google LLC"
            },
            "org": "AS15169 Google LLC"
        }
    }


@pytest.fixture
def mock_local_db_data() -> Dict[str, Any]:
    return {
        "8.8.8.8": {
            "country": "United States",
            "country_code": "US",
            "city": "Mountain View",
            "region": "California",
            "postal_code": "94043",
            "latitude": 37.4056,
            "longitude": -122.0775,
            "timezone": "America/Los_Angeles",
            "asn": 15169,
            "as_org": "Google LLC",
            "network": "8.8.8.0/24",
            "connection_type": "hosting"
        },
        "1.1.1.1": {
            "country": "Australia",
            "country_code": "AU",
            "city": "Sydney",
            "region": "New South Wales",
            "asn": 13335,
            "as_org": "Cloudflare Inc",
            "connection_type": "hosting"
        },
        "192.168.1.1": {
            "country": None,
            "country_code": None,
            "city": None,
            "asn": None,
            "as_org": None
        }
    }