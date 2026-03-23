# backend/tests/unit/services/decoy_tokens/utils/ip/test_validation.py

import pytest
from backend.app.services.decoy_tokens.utils.ip.validation import (
    is_public_ip,
    parse_trusted_proxies,
    get_ip_version,
)
from ipaddress import ip_network


class TestIPValidation:

    def test_is_public_ip_with_public(self, public_ips):
        for name, ip in public_ips.items():
            assert is_public_ip(ip) is True, f"{name} ({ip}) должен быть публичным"

    def test_is_public_ip_with_private(self, private_ips):
        for name, ip in private_ips.items():
            assert is_public_ip(ip) is False, f"{name} ({ip}) не должен быть публичным"

    def test_is_public_ip_with_invalid(self, invalid_ips):
        for ip in invalid_ips:
            assert is_public_ip(ip) is False, f"{ip} должен возвращать False"

    @pytest.mark.parametrize("ip,expected", [
        ("8.8.8.8", "IPv4"),
        ("1.1.1.1", "IPv4"),
        ("2001:4860:4860::8888", "IPv6"),
        ("::1", "IPv6"),
        ("invalid", None),
        ("", None),
        (None, None),
    ])
    def test_get_ip_version(self, ip, expected):
        assert get_ip_version(ip) == expected

    def test_parse_trusted_proxies_with_ips(self):
        proxies = ["8.8.8.8", "1.1.1.1", "10.0.0.1"]
        networks = parse_trusted_proxies(proxies)
        
        assert len(networks) == 3
        assert str(networks[0]) == "8.8.8.8/32"
        assert str(networks[1]) == "1.1.1.1/32"
        assert str(networks[2]) == "10.0.0.1/32"

    def test_parse_trusted_proxies_with_networks(self):
        proxies = ["192.168.1.0/24", "10.0.0.0/8"]
        networks = parse_trusted_proxies(proxies)
        
        assert len(networks) == 2
        assert str(networks[0]) == "192.168.1.0/24"
        assert str(networks[1]) == "10.0.0.0/8"

    def test_parse_trusted_proxies_mixed(self):
        proxies = ["8.8.8.8", "192.168.1.0/24", "invalid"]
        networks = parse_trusted_proxies(proxies)
        
        assert len(networks) == 2
        assert str(networks[0]) == "8.8.8.8/32"
        assert str(networks[1]) == "192.168.1.0/24"

    def test_parse_trusted_proxies_empty(self):
        assert parse_trusted_proxies([]) == []
        assert parse_trusted_proxies(None) == []
        assert parse_trusted_proxies(set()) == []