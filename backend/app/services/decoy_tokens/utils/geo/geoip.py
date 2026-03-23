import geoip2.database
import geoip2.errors
import aiohttp
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from backend.app.core.config import settings
import logging
import time
from collections import OrderedDict

logger = logging.getLogger(__name__)


class RateLimiter:
    """Простой rate limiter для API запросов"""
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = OrderedDict()
    
    def can_call(self) -> bool:
        now = time.time()
        while self.calls and next(iter(self.calls.values())) < now - self.period:
            self.calls.popitem(last=False)
        
        if len(self.calls) < self.max_calls:
            self.calls[now] = now
            return True
        return False


class GeoIPService:
    _instance = None
    
    DATACENTER_KEYWORDS = (
        "amazon", "aws", "google", "microsoft", "azure", 
        "digitalocean", "linode", "ovh", "hetzner", "vultr",
        "oracle", "cloudflare", "alibaba",
    )
    
    FALLBACK_APIS = [
        {
            'name': 'ip-api',
            'url': 'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
            'enabled': True,
            'rate_limit': 45,
            'timeout': 2,
            'parser': lambda data: {
                'country': data.get('country'),
                'country_code': data.get('countryCode'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'postal_code': data.get('zip'),
                'latitude': data.get('lat'),
                'longitude': data.get('lon'),
                'timezone': data.get('timezone'),
                'asn': int(data.get('as', '').split()[0]) if data.get('as') else None,
                'as_org': data.get('org') or data.get('isp'),
                'connection_type': None,
            }
        },
        {
            'name': 'ipinfo',
            'url': 'https://ipinfo.io/{ip}/json',
            'enabled': bool(getattr(settings, 'IPINFO_TOKEN', False)),
            'token': getattr(settings, 'IPINFO_TOKEN', None),
            'rate_limit': 50000,
            'timeout': 2,
            'parser': lambda data: {
                'country': data.get('country'),
                'country_code': data.get('country'),
                'region': data.get('region'),
                'city': data.get('city'),
                'postal_code': data.get('postal'),
                'latitude': float(data.get('loc', '').split(',')[0]) if data.get('loc') else None,
                'longitude': float(data.get('loc', '').split(',')[1]) if data.get('loc') else None,
                'timezone': data.get('timezone'),
                'asn': int(data.get('asn', {}).get('asn', '').replace('AS', '')) if data.get('asn') else None,
                'as_org': data.get('org'),
                'connection_type': None,
            }
        }
    ]
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self._city_reader = None
        self._asn_reader = None
        self._rate_limiters = {}
        self._session = None
        self._country_code_cache = {}
        
        # Rate limiters
        for api in self.FALLBACK_APIS:
            if api.get('enabled'):
                self._rate_limiters[api['name']] = RateLimiter(api['rate_limit'], 60)
        
        # Загрузка баз
        self._load_databases()
    
    def _load_databases(self):
        try:
            if settings.GEOIP_CITY_PATH and Path(settings.GEOIP_CITY_PATH).exists():
                self._city_reader = geoip2.database.Reader(str(settings.GEOIP_CITY_PATH))
            
            if settings.GEOIP_ASN_PATH and Path(settings.GEOIP_ASN_PATH).exists():
                self._asn_reader = geoip2.database.Reader(str(settings.GEOIP_ASN_PATH))
        except Exception as e:
            logger.error(f"Error loading GeoIP databases: {e}")
    
    async def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    def _detect_connection_type(self, as_org: Optional[str]) -> Optional[str]:
        if not as_org:
            return None
        org = as_org.lower()
        return "hosting" if any(k in org for k in self.DATACENTER_KEYWORDS) else "residential"
    
    def _get_local_info(self, ip: str) -> Dict[str, Any]:
        result = {
            "country": None, "country_code": None, "region": None, "city": None,
            "postal_code": None, "latitude": None, "longitude": None, "timezone": None,
            "asn": None, "as_org": None, "network": None, "connection_type": None,
            "source": "local"
        }
        
        if self._city_reader:
            try:
                response = self._city_reader.city(ip)
                if response.country:
                    result["country"] = response.country.name
                    result["country_code"] = response.country.iso_code
                if response.city:
                    result["city"] = response.city.name
                if response.subdivisions:
                    result["region"] = response.subdivisions.most_specific.name
                if response.postal:
                    result["postal_code"] = response.postal.code
                if response.location:
                    result["latitude"] = response.location.latitude
                    result["longitude"] = response.location.longitude
                    result["timezone"] = response.location.time_zone
            except:
                pass
        
        if self._asn_reader:
            try:
                response = self._asn_reader.asn(ip)
                result["asn"] = response.autonomous_system_number
                result["as_org"] = response.autonomous_system_organization
                result["network"] = str(response.network) if response.network else None
                result["connection_type"] = self._detect_connection_type(result["as_org"])
            except:
                pass
        
        return result
    
    async def _call_api(self, api: Dict, ip: str) -> Optional[Dict]:
        rate_limiter = self._rate_limiters.get(api['name'])
        if rate_limiter and not rate_limiter.can_call():
            return None

        url = api['url'].format(ip=ip)
        if api.get('token'):
            url += f"?token={api['token']}"

        session = await self._get_session()

        try:
            response = await session.get(url, timeout=api['timeout'])
            async with response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'fail':
                        return None

                    parsed = api['parser'](data)
                    parsed['source'] = api['name']
                    parsed['connection_type'] = self._detect_connection_type(parsed.get('as_org'))
                    return parsed
        except Exception:
            return None

        return None
    
    async def get_geo_info(self, ip: str, use_fallback: bool = True) -> Dict[str, Any]:
        """Асинхронное получение гео-информации"""
        # Локальные данные
        result = self._get_local_info(ip)
        
        # Проверяем нужен ли fallback
        need_fallback = use_fallback and not any(result.get(f) for f in ['country', 'city', 'as_org'])
        
        if need_fallback:
            enabled_apis = [api for api in self.FALLBACK_APIS if api.get('enabled')]
            
            if enabled_apis:
                # Параллельные запросы ко всем API
                tasks = [self._call_api(api, ip) for api in enabled_apis]
                api_results = await asyncio.gather(*tasks)
                
                # Берем первый успешный
                for api_result in api_results:
                    if api_result:
                        for key, value in api_result.items():
                            if key != 'source' and result.get(key) is None and value is not None:
                                result[key] = value
                        result['source'] = f"local+{api_result['source']}"
                        break
        
        return result
    
    async def get_country_code(self, ip: str) -> Optional[str]:
        if ip in self._country_code_cache:
            return self._country_code_cache[ip]

        info = await self.get_geo_info(ip, use_fallback=False)
        country_code = info.get('country_code')
        self._country_code_cache[ip] = country_code
        return country_code


# Единственный экземпляр
geo_service = GeoIPService()