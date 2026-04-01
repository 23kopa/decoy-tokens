from __future__ import annotations

from datetime import datetime
from typing import Any, Awaitable, Callable
from uuid import UUID

from backend.app.application.ports.repositories.event_repository import TokenEventRepositoryPort
from backend.app.domain.entities.token_event import TokenEvent


class LogTokenEvent:
    def __init__(
        self,
        repo: TokenEventRepositoryPort,
        request_info_collector: Callable[..., Awaitable[dict[str, Any]]],
        fingerprint_generator: Callable[[dict[str, Any]], str],
        is_bot_checker: Callable[[str | None], bool],
        bot_type_getter: Callable[[str | None], str | None],
        deduplicator_factory: Callable[[TokenEventRepositoryPort], Any],
        trusted_proxies: set[str] | None = None,
    ):
        self.repo = repo
        self.request_info_collector = request_info_collector
        self.fingerprint_generator = fingerprint_generator
        self.is_bot_checker = is_bot_checker
        self.bot_type_getter = bot_type_getter
        self.deduplicator = deduplicator_factory(repo)
        self.trusted_proxies = trusted_proxies or set()

    async def execute(self, token_id: UUID, request) -> None:
        request_data = await self.request_info_collector(request, self.trusted_proxies)
        fingerprint = self.fingerprint_generator(request_data)

        if self.deduplicator.process(token_id, fingerprint, request_data):
            return

        headers = request_data.get("headers", {}) or {}
        user_agent = headers.get("user-agent")

        is_bot_flag = self.is_bot_checker(user_agent)
        bot_type = self.bot_type_getter(user_agent) if is_bot_flag else None

        ip_data = request_data.get("ip_data", {}) or {}
        geo_data = request_data.get("geo", {}) or {}
        detected_ip = ip_data.get("detected_ip")

        now = datetime.utcnow()

        event = TokenEvent(
            id=None,
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