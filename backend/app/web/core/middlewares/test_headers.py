# backend/app/web/middlewares/test_headers.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.datastructures import MutableHeaders
import random

class TestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/t/"):
            # Модифицируем заголовки
            headers = MutableHeaders(scope=request.scope)
            
            # Реальные внешние IP для тестирования
            test_ips = [
                # Публичные IP из разных стран
                "8.8.8.8",           # Google DNS (США)
                "1.1.1.1",           # Cloudflare DNS (Австралия/США)
                "9.9.9.9",            # Quad9 DNS (Швейцария/США)
                "185.220.101.1",      # Tor exit node (Германия)
                "104.16.0.1",         # Cloudflare CDN (США)
                "151.101.1.1",        # Fastly CDN (США)
                "140.82.112.3",       # GitHub (США)
                "34.120.0.1",         # Google Cloud (США)
                "52.4.0.1",           # AWS (США)
                "20.0.0.1",           # Microsoft Azure (США)
                # Европейские IP
                "80.80.80.80",        # Freenet (Германия)
                "77.88.55.77",        # Yandex DNS (Россия)
                "208.67.222.222",     # OpenDNS (США/Европа)
            ]
            
            # Выбираем случайный внешний IP
            real_ip = random.choice(test_ips)
            
            # Добавляем X-Forwarded-For с цепочкой
            # Формат: реальный IP, потом IP прокси (если есть)
            headers["x-forwarded-for"] = f"{real_ip}, 10.0.0.1"
            
            # Добавляем X-Real-IP (часто используется nginx)
            headers["x-real-ip"] = real_ip
            
            # Добавляем Cloudflare заголовки для теста
            headers["cf-connecting-ip"] = real_ip
            headers["cf-ray"] = f"test-{random.randint(10000, 99999)}"
            
            # Оставляем оригинальный user-agent или меняем на тестовый
            if "user-agent" not in headers:
                headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            
            print(f"\n🔧 TestHeadersMiddleware: Добавлен внешний IP {real_ip}")
            
        response = await call_next(request)
        return response