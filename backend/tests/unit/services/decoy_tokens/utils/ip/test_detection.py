# backend/tests/unit/services/decoy_tokens/utils/ip/test_detection_unit.py

import pytest
from unittest.mock import Mock, patch
from starlette.requests import Request
from backend.app.services.decoy_tokens.utils.ip.detection import get_client_ip


class TestIPDetectionUnit:
    """Модульные тесты для определения IP (с моками)"""

    def create_mock_request(self, direct_ip: str = "127.0.0.1", headers: dict[str, str] | None = None):
        """Создание mock request"""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = direct_ip
        mock_request.headers = headers or {}
        return mock_request

    def test_direct_no_headers(self):
        """Тест без заголовков"""
        mock_request = self.create_mock_request(direct_ip="127.0.0.1")
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] == "127.0.0.1"
        assert result["detection_method"] == "Direct Fallback"
        assert result["direct_ip"] == "127.0.0.1"
        assert result["confidence"] == 0.5
        assert result["proxy_chain"] == []

    def test_xff_single_public(self):
        """Тест с одним публичным IP в XFF"""
        mock_request = self.create_mock_request(
            direct_ip="10.0.0.1",
            headers={"x-forwarded-for": "8.8.8.8"}
        )
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] == "8.8.8.8"
        assert result["detection_method"] == "X-Forwarded-For"
        assert result["confidence"] == 0.95
        assert result["proxy_chain"] == ["8.8.8.8"]

    def test_xff_chain_first_public(self):
        """Тест с цепочкой где первый публичный"""
        mock_request = self.create_mock_request(
            direct_ip="192.168.1.1",
            headers={"x-forwarded-for": "8.8.8.8, 10.0.0.1, 192.168.1.1"}
        )
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] == "8.8.8.8"
        assert result["proxy_chain"] == ["8.8.8.8", "10.0.0.1", "192.168.1.1"]

    def test_xff_all_private(self):
        """Тест когда все IP в XFF приватные"""
        mock_request = self.create_mock_request(
            direct_ip="192.168.1.1",
            headers={"x-forwarded-for": "10.0.0.1, 172.16.0.1"}
        )
        
        result = get_client_ip(mock_request)
        
        # Должен упасть на direct IP
        assert result["detected_ip"] == "192.168.1.1"
        assert result["detection_method"] == "Direct Fallback"
        assert result["proxy_chain"] == ["10.0.0.1", "172.16.0.1"]

    def test_x_real_ip(self):
        """Тест с X-Real-IP"""
        mock_request = self.create_mock_request(
            direct_ip="10.0.0.1",
            headers={"x-real-ip": "8.8.8.8"}
        )
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] == "8.8.8.8"
        assert result["detection_method"] == "X-Real-IP"
        assert result["x_real_ip"] == "8.8.8.8"
        assert result["confidence"] == 0.9

    def test_xff_takes_priority(self):
        """Тест что XFF имеет приоритет над X-Real-IP"""
        mock_request = self.create_mock_request(
            direct_ip="10.0.0.1",
            headers={
                "x-forwarded-for": "8.8.8.8",
                "x-real-ip": "1.1.1.1"
            }
        )
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] == "8.8.8.8"
        assert result["detection_method"] == "X-Forwarded-For"

    def test_no_client(self):
        """Тест когда нет client в request"""
        mock_request = Mock(spec=Request)
        mock_request.client = None
        
        result = get_client_ip(mock_request)
        
        assert result["detected_ip"] is None
        assert result["direct_ip"] is None

    @patch('backend.app.services.decoy_tokens.utils.ip.detection.is_public_ip')
    def test_with_mocked_is_public_ip(self, mock_is_public):
        """Тест с замоканной функцией is_public_ip"""
        mock_is_public.side_effect = lambda ip: ip == "81.22.45.67"
        
        mock_request = self.create_mock_request(
            direct_ip="10.0.0.1",
            headers={"x-forwarded-for": "81.22.45.67, 10.0.0.1, 172.16.0.1"}
        )
        
        result = get_client_ip(mock_request)
        
        # Должен найти 8.8.8.8 как первый публичный
        assert result["detected_ip"] == "81.22.45.67"
        
        # Проверяем что is_public_ip вызывалась для каждого IP
        assert mock_is_public.call_count == 1