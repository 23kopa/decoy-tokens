import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.models.token_event import TokenEvent


class TokenEventUpdateMixin:
    session: Session

    def update_event_with_new_ip(
        self,
        event: TokenEvent,
        current_ip_data: dict,
        request_data: dict,
    ) -> None:
        now = datetime.utcnow()

        old_ip = event.current_ip
        new_ip = current_ip_data.get("detected_ip")
        old_last_seen = event.last_seen

        event.seen_count += 1
        event.is_first = False

        if event.ip_history is None:
            event.ip_history = []

        history = list(event.ip_history or [])

        # На каждом повторном срабатывании сохраняем предыдущее состояние
        if old_ip:
            old_entry = {
                "ip": old_ip,
                "timestamp": old_last_seen.isoformat() if old_last_seen else now.isoformat(),
                "geo": event.geo or {},
                "asn": event.asn,
                "org": event.org,
                "connection_type": (event.geo or {}).get("connection_type"),
                "ip_version": (event.current_ip_data or {}).get("ip_version"),
            }

            # защита только от полного дубля подряд
            last_entry = history[-1] if history else None
            is_exact_duplicate = (
                last_entry
                and last_entry.get("ip") == old_entry["ip"]
                and last_entry.get("timestamp") == old_entry["timestamp"]
            )

            if not is_exact_duplicate:
                history.append(old_entry)

        event.ip_history = history

        if new_ip:
            event.current_ip = new_ip
            event.last_ip = new_ip

        event.current_ip_data = current_ip_data
        event.current_user_agent = request_data.get("headers", {}).get("user-agent")
        event.current_headers = request_data.get("headers", {})
        event.current_port = request_data.get("client_port")

        geo_data = request_data.get("geo", {}) or {}
        event.geo = geo_data
        event.asn = str(geo_data.get("asn")) if geo_data.get("asn") is not None else None
        event.org = geo_data.get("as_org") or geo_data.get("organization")

        unique_ips = {entry["ip"] for entry in event.ip_history if entry.get("ip")}
        if event.current_ip:
            unique_ips.add(event.current_ip)
        event.unique_ip_count = len(unique_ips)

        event.last_seen = now

        self.session.add(event)

    def count_by_fingerprint_since(
        self,
        token_id: uuid.UUID,
        fingerprint: str,
        since: datetime
    ) -> int:
        stmt = (
            select(TokenEvent.seen_count)
            .where(
                TokenEvent.token_id == token_id,
                TokenEvent.fingerprint == fingerprint,
                TokenEvent.last_seen >= since
            )
        )
        result = self.session.execute(stmt).scalar()
        return result or 0