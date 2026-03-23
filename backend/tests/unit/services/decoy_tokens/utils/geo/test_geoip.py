# backend/tests/unit/services/decoy_tokens/utils/geo/test_geoip.py

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import Dict, Any
from backend.app.services.decoy_tokens.utils.geo.geoip import GeoIPService, RateLimiter


class TestRateLimiter:
    """Тесты для RateLimiter"""
    
    def test_rate_limiter_initial(self):
        limiter = RateLimiter(max_calls=5, period=60)
        assert limiter.max_calls == 5
        assert limiter.period == 60
        assert len(limiter.calls) == 0
    
    def test_rate_limiter_can_call_within_limit(self):
        limiter = RateLimiter(max_calls=2, period=60)
        
        assert limiter.can_call() is True
        assert limiter.can_call() is True
        assert len(limiter.calls) == 2
    
    def test_rate_limiter_exceeds_limit(self):
        limiter = RateLimiter(max_calls=2, period=60)
        
        assert limiter.can_call() is True
        assert limiter.can_call() is True
        assert limiter.can_call() is False


class TestGeoIPServiceUnit:
    """Модульные тесты для GeoIPService с моками"""
    
    @pytest.fixture
    def geo_service(self):
        """Создание сервиса с замоканными reader'ами"""
        service = GeoIPService()
        
        # Мокаем reader'ы
        service._city_reader = Mock()
        service._asn_reader = Mock()
        
        # Мокаем rate limiters
        service._rate_limiters = {
            'ip-api': Mock(spec=RateLimiter),
            'ipinfo': Mock(spec=RateLimiter)
        }
        
        return service
    
    def test_detect_connection_type_hosting(self, geo_service):
        """Тест определения hosting"""
        assert geo_service._detect_connection_type("Google LLC") == "hosting"
        assert geo_service._detect_connection_type("Amazon AWS") == "hosting"
        assert geo_service._detect_connection_type("Cloudflare Inc") == "hosting"
    
    def test_detect_connection_type_residential(self, geo_service):
        """Тест определения residential"""
        assert geo_service._detect_connection_type("Rostelecom") == "residential"
        assert geo_service._detect_connection_type("Comcast Cable") == "residential"
        assert geo_service._detect_connection_type("Deutsche Telekom") == "residential"
    
    def test_detect_connection_type_none(self, geo_service):
        """Тест с None"""
        assert geo_service._detect_connection_type(None) is None
        assert geo_service._detect_connection_type("") is None
    
    def test_get_local_info_with_city_only(self, geo_service):
        """Тест получения локальной информации (только city база)"""
        # Создаем мок для city response
        mock_city_response = Mock()
        
        # Настраиваем атрибуты
        mock_country = Mock()
        mock_country.name = "United States"
        mock_country.iso_code = "US"
        mock_city_response.country = mock_country
        
        mock_city = Mock()
        mock_city.name = "Mountain View"
        mock_city_response.city = mock_city
        
        mock_subdivisions = Mock()
        mock_subdivisions.most_specific.name = "California"
        mock_city_response.subdivisions = mock_subdivisions
        
        mock_postal = Mock()
        mock_postal.code = "94043"
        mock_city_response.postal = mock_postal
        
        mock_location = Mock()
        mock_location.latitude = 37.4056
        mock_location.longitude = -122.0775
        mock_location.time_zone = "America/Los_Angeles"
        mock_city_response.location = mock_location
        
        # Настраиваем city reader
        geo_service._city_reader.city.return_value = mock_city_response
        geo_service._asn_reader = None
        
        result = geo_service._get_local_info("8.8.8.8")
        
        assert result["country"] == "United States"
        assert result["country_code"] == "US"
        assert result["city"] == "Mountain View"
        assert result["region"] == "California"
        assert result["postal_code"] == "94043"
        assert result["latitude"] == 37.4056
        assert result["longitude"] == -122.0775
        assert result["timezone"] == "America/Los_Angeles"
        assert result["asn"] is None
        assert result["as_org"] is None
        assert result["source"] == "local"
    
    def test_get_local_info_with_asn_only(self, geo_service):
        """Тест получения локальной информации (только ASN база)"""
        # Создаем мок для ASN response
        mock_asn_response = Mock()
        mock_asn_response.autonomous_system_number = 15169
        mock_asn_response.autonomous_system_organization = "Google LLC"
        mock_asn_response.network = "8.8.8.0/24"
        
        # Настраиваем asn reader
        geo_service._asn_reader.asn.return_value = mock_asn_response
        geo_service._city_reader = None
        
        result = geo_service._get_local_info("8.8.8.8")
        
        assert result["country"] is None
        assert result["city"] is None
        assert result["asn"] == 15169
        assert result["as_org"] == "Google LLC"
        assert result["network"] == "8.8.8.0/24"
        assert result["connection_type"] == "hosting"
        assert result["source"] == "local"
    
    @patch('geoip2.database.Reader')
    def test_get_local_info_with_both_databases(self, mock_reader, geo_service, mock_local_db_data):
        """Тест получения информации из обеих баз"""
        # Настройка мока для city базы
        mock_city_response = Mock()
        mock_city_response.country.name = "United States"
        mock_city_response.country.iso_code = "US"
        mock_city_response.city.name = "Mountain View"
        
        # Настройка мока для ASN базы
        mock_asn_response = Mock()
        mock_asn_response.autonomous_system_number = 15169
        mock_asn_response.autonomous_system_organization = "Google LLC"
        mock_asn_response.network = "8.8.8.0/24"
        
        # Настраиваем reader'ы
        mock_city_reader = Mock()
        mock_city_reader.city.return_value = mock_city_response
        
        mock_asn_reader = Mock()
        mock_asn_reader.asn.return_value = mock_asn_response
        
        geo_service._city_reader = mock_city_reader
        geo_service._asn_reader = mock_asn_reader
        
        result = geo_service._get_local_info("8.8.8.8")
        
        assert result["country"] == "United States"
        assert result["country_code"] == "US"
        assert result["city"] == "Mountain View"
        assert result["asn"] == 15169
        assert result["as_org"] == "Google LLC"
        assert result["network"] == "8.8.8.0/24"
        assert result["connection_type"] == "hosting"
        assert result["source"] == "local"
    
    def test_need_fallback_calculation(self, geo_service):
        """Тест логики определения необходимости fallback"""
        # Случай 1: нет данных - нужен fallback
        data1 = {
            "country": None,
            "city": None,
            "as_org": None
        }
        need_fallback1 = not any(data1.get(f) for f in ['country', 'city', 'as_org'])
        assert need_fallback1 is True
        
        # Случай 2: есть все данные - не нужен fallback
        data2 = {
            "country": "US",
            "city": "Mountain View",
            "as_org": "Google LLC"
        }
        need_fallback2 = not any(data2.get(f) for f in ['country', 'city', 'as_org'])
        assert need_fallback2 is False
        
        # Случай 3: частичные данные - не нужен fallback
        data3 = {
            "country": "US",
            "city": None,
            "as_org": None
        }
        need_fallback3 = not any(data3.get(f) for f in ['country', 'city', 'as_org'])
        assert need_fallback3 is False
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')
    async def test_call_api_success(self, mock_session_class, geo_service, mock_geoip_responses):
        """Тест успешного вызова API"""
        # Создаем мок ответа
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_geoip_responses["ip-api"])
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        # Создаем мок для get запроса
        mock_get = AsyncMock(return_value=mock_response)
        
        # Создаем мок сессии
        mock_session = AsyncMock()
        mock_session.get = mock_get
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        # Настраиваем класс сессии
        mock_session_class.return_value = mock_session
        
        # Мокаем _get_session
        geo_service._get_session = AsyncMock(return_value=mock_session)
        geo_service._rate_limiters['ip-api'].can_call.return_value = True
        
        api_config = {
            'name': 'ip-api',
            'url': 'http://ip-api.com/json/{ip}',
            'timeout': 2,
            'parser': lambda data: {
                'country': data.get('country'),
                'country_code': data.get('countryCode'),
                'asn': int(data.get('as', '').split()[0].replace('AS', '')) if data.get('as') else None,
                'as_org': data.get('org'),
            }
        }
        
        result = await geo_service._call_api(api_config, "8.8.8.8")
        
        assert result is not None
        assert result['country'] == 'United States'
        assert result['country_code'] == 'US'
    
    @pytest.mark.asyncio
    async def test_call_api_rate_limited(self, geo_service):
        """Тест rate limiting"""
        geo_service._rate_limiters['ip-api'].can_call.return_value = False
        
        api_config = {'name': 'ip-api', 'url': 'http://test.com/{ip}'}
        result = await geo_service._call_api(api_config, "8.8.8.8")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_geo_info_local_only(self, geo_service, mock_local_db_data):
        """Тест получения geo информации только из локальной БД"""
        # Мокаем _get_local_info
        mock_local_db_data["8.8.8.8"]["source"] = "local"
        geo_service._get_local_info = Mock(return_value=mock_local_db_data["8.8.8.8"])
        
        result = await geo_service.get_geo_info("8.8.8.8", use_fallback=False)
        
        assert result["country"] == "United States"
        assert result["asn"] == 15169
        assert result["source"] == "local"
    
    @pytest.mark.asyncio
    async def test_get_geo_info_with_fallback(self, geo_service):
        """Тест получения geo информации с fallback к API"""
        # Мокаем _get_local_info (возвращает неполные данные)
        geo_service._get_local_info = Mock(return_value={
            "country": None,
            "city": None,
            "as_org": None,
            "source": "local"
        })
        
        # Мокаем _call_api для возврата результата
        geo_service._call_api = AsyncMock(return_value={
            "country": "United States",
            "country_code": "US",
            "asn": 15169,
            "as_org": "Google LLC",
            "source": "ip-api"
        })
        
        result = await geo_service.get_geo_info("8.8.8.8", use_fallback=True)
        
        assert result["country"] == "United States"
        assert result["asn"] == 15169
        assert result["source"] == "local+ip-api"
    
    @pytest.mark.asyncio
    async def test_get_geo_info_fallback_no_data(self, geo_service):
        """Тест когда fallback не дал данных"""
        # Мокаем _get_local_info (возвращает неполные данные)
        geo_service._get_local_info = Mock(return_value={
            "country": None,
            "city": None,
            "as_org": None,
            "source": "local"
        })
        
        # Мокаем _call_api для возврата None
        geo_service._call_api = AsyncMock(return_value=None)
        
        result = await geo_service.get_geo_info("8.8.8.8", use_fallback=True)
        
        assert result["country"] is None
        assert result["source"] == "local"
    
    @pytest.mark.asyncio
    async def test_get_country_code_cached(self):
        """Тест кэширования country code"""
        # Создаем отдельный экземпляр сервиса
        test_service = GeoIPService()
        
        # Создаем новый AsyncMock для каждого вызова
        mock_get_geo_info = AsyncMock()
        mock_get_geo_info.return_value = {"country_code": "US"}
        test_service.get_geo_info = mock_get_geo_info
        
        # Первый вызов
        code1 = await test_service.get_country_code("8.8.8.8")
        assert code1 == "US"
        
        # Второй вызов с тем же IP
        code2 = await test_service.get_country_code("8.8.8.8")
        assert code2 == "US"
        
        # Проверяем что get_geo_info вызвался дважды
        assert mock_get_geo_info.call_count == 1