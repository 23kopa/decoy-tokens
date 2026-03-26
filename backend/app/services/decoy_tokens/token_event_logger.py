from __future__ import annotations

from datetime import datetime
from uuid import UUID

from starlette.requests import Request

from backend.app.infrastructure.database.models.token_event import TokenEvent
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.services.decoy_tokens.request_collector import collect_request_info
from backend.app.services.decoy_tokens.utils.detectors.bot import get_bot_type, is_bot
from backend.app.services.decoy_tokens.utils.detectors.dedup import create_deduplicator
from backend.app.services.decoy_tokens.utils.fingerprint.generate import generate_fingerprint


class TokenEventLoggerService:
    def __init__(
        self,
        repo: TokenEventRepository,
        trusted_proxies: set[str] | None = None,
    ):
        self.repo = repo
        self.trusted_proxies = trusted_proxies or set()
        self.deduplicator = create_deduplicator(repo, window_seconds=60)

    async def log_hit(self, token_id: UUID, request: Request) -> None:
        request_data = await collect_request_info(request, self.trusted_proxies)
        fingerprint = generate_fingerprint(request_data)

        if self.deduplicator.process(token_id, fingerprint, request_data):
            return

        headers = request_data.get("headers", {}) or {}
        user_agent = headers.get("user-agent")

        is_bot_flag = is_bot(user_agent)
        bot_type = get_bot_type(user_agent) if is_bot_flag else None

        ip_data = request_data.get("ip_data", {}) or {}
        geo_data = request_data.get("geo", {}) or {}
        detected_ip = ip_data.get("detected_ip")

        now = datetime.utcnow()

        event = TokenEvent(
            token_id=token_id,
            fingerprint=fingerprint,
            seen_count=1,
            first_ip=detected_ip,
            last_ip=detected_ip,
            ip_history=[],
            unique_ip_count=1,
            first_seen=now,
            last_seen=now,
            current_ip=detected_ip,
            current_ip_data=ip_data,
            current_user_agent=user_agent,
            current_headers=headers,
            current_port=request_data.get("client_port"),
            geo=geo_data,
            asn=str(geo_data["asn"]) if geo_data.get("asn") else None,
            org=geo_data.get("as_org") or geo_data.get("organization"),
            is_first=True,
            additional_data={
                "bot_info": {
                    "is_bot": is_bot_flag,
                    "bot_type": bot_type,
                }
            },
        )

        self.repo.add(event)