# backend/tests/unit/services/decoy_tokens/utils/ip/test_proxy.py

import pytest
from backend.app.services.decoy_tokens.utils.ip.proxy import parse_proxy_chain


class TestProxyParsing:
    """Тесты для парсинга прокси цепочек"""

    def test_parse_proxy_chain_list_format(self, xff_scenarios):
        """Тест парсинга в формат списка"""
        for scenario in xff_scenarios:
            result = parse_proxy_chain(scenario["xff"], return_format="list")
            assert result == scenario["expected_list"], f"Failed for {scenario['name']}"

    def test_parse_proxy_chain_dict_format(self, xff_scenarios):
        """Тест парсинга в формат словаря с деталями"""
        for scenario in xff_scenarios:
            if "expected_dict" in scenario:
                result = parse_proxy_chain(scenario["xff"], return_format="dict")
                
                # Проверяем длину
                assert len(result) == len(scenario["expected_dict"])
                
                # Проверяем каждый элемент
                for i, expected in enumerate(scenario["expected_dict"]):
                    assert result[i]["position"] == expected["position"]
                    assert result[i]["ip"] == expected["ip"]
                    assert result[i]["is_public"] == expected["is_public"]
                    assert result[i]["version"] == expected["version"]

    def test_parse_proxy_chain_with_ipv6(self):
        """Тест парсинга с IPv6 адресами"""
        xff = "2001:4860:4860::8888, 8.8.8.8"
        result = parse_proxy_chain(xff, return_format="dict")
        
        assert len(result) == 2
        assert result[0]["ip"] == "2001:4860:4860::8888"
        assert result[0]["version"] == "IPv6"
        assert result[0]["is_public"] is True
        
        assert result[1]["ip"] == "8.8.8.8"
        assert result[1]["version"] == "IPv4"
        assert result[1]["is_public"] is True

    @pytest.mark.parametrize("xff,expected_count", [
        ("8.8.8.8", 1),
        ("8.8.8.8,1.1.1.1,4.4.4.4", 3),
        ("  8.8.8.8  ,  1.1.1.1  ", 2),
    ])
    def test_parse_proxy_chain_various_formats(self, xff, expected_count):
        """Тест различных форматов X-Forwarded-For"""
        result = parse_proxy_chain(xff, return_format="list")
        assert len(result) == expected_count