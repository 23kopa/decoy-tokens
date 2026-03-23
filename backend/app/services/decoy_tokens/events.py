from datetime import datetime
from starlette.requests import Request

from backend.app.infrastructure.database.models.token_event import TokenEvent
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository

from backend.app.services.decoy_tokens.collector import collect_request_info

from backend.app.services.decoy_tokens.utils.fingerprint.generate import generate_fingerprint
from backend.app.services.decoy_tokens.utils.detectors.bot import is_bot, get_bot_type
from backend.app.services.decoy_tokens.utils.detectors.dedup import create_deduplicator

class TokenEventService:
    def __init__(self, repo: TokenEventRepository, trusted_proxies: set[str] | None = None):
        self.repo = repo
        self.trusted_proxies = trusted_proxies or set()
        self.deduplicator = create_deduplicator(repo, window_seconds=60)

    async def log_hit(self, token_id, request: Request) -> None:

        # Собираем данные и генерируем fingerprint
        request_data = await collect_request_info(request, self.trusted_proxies)
        fingerprint = generate_fingerprint(request_data)
 
        # Пороверяем дубликаты
        if self.deduplicator.process(token_id, fingerprint, request_data):
            return

        # Детекция ботов
        ua = request.headers.get("user-agent")
        is_bot_flag = is_bot(ua)
        bot_type = get_bot_type(ua) if is_bot_flag else None

        # Получаем детальную IP информацию
        ip_data = request_data.get("ip_data", {})
        geo_data = request_data.get("geo", {})
        detected_ip = ip_data.get("detected_ip")

        now = datetime.utcnow()

        # Создаем событие с новой структурой
        ev = TokenEvent(
            token_id=token_id,
            
            # Основные поля
            fingerprint=fingerprint,
            seen_count=1,
            
            # IP история
            first_ip=detected_ip,
            last_ip=detected_ip,
            ip_history=[],
            unique_ip_count=1,
            
            # Временные метки
            first_seen=now,
            last_seen=now,
            
            # Текущие данные
            current_ip=detected_ip,
            current_ip_data=ip_data,
            current_user_agent=ua,
            current_headers=request_data.get("headers", {}),
            current_port=request_data.get("client_port"),
            
            # Гео данные
            geo=geo_data,
            asn = str(geo_data["asn"]) if geo_data and geo_data.get("asn") else None,
            org=geo_data.get("as_org") or geo_data.get("organization"),
            
            # Флаги
            is_first=True,
            
            # Дополнительные данные
            additional_data={
                "bot_info": {
                    "is_bot": is_bot_flag,
                    "bot_type": bot_type,
                }
            }
        )
        
        self.repo.add(ev)