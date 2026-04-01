import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.domain.entities.token_event import TokenEvent as DomainTokenEvent
from backend.app.infrastructure.database.models.token_event import TokenEvent as TokenEventModel


class TokenEventUpdateMixin:
    session: Session

    def update_event_with_new_ip(
        self,
        event: DomainTokenEvent,
        current_ip_data: dict,
        request_data: dict,
    ) -> None:
        if event.id is None:
            return

        stmt = select(TokenEventModel).where(TokenEventModel.id == event.id)
        model = self.session.scalar(stmt)
        if not model:
            return

        now = datetime.utcnow()

        old_ip = model.current_ip
        new_ip = current_ip_data.get("detected_ip")
        old_last_seen = model.last_seen

        model.seen_count += 1
        model.is_first = False

        if model.ip_history is None:
            model.ip_history = []

        history = list(model.ip_history or [])

        if old_ip:
            old_entry = {
                "ip": old_ip,
                "timestamp": old_last_seen.isoformat() if old_last_seen else now.isoformat(),
                "geo": model.geo or {},
                "asn": model.asn,
                "org": model.org,
                "connection_type": (model.geo or {}).get("connection_type"),
                "ip_version": (model.current_ip_data or {}).get("ip_version"),
            }

            last_entry = history[-1] if history else None
            is_exact_duplicate = (
                last_entry
                and last_entry.get("ip") == old_entry["ip"]
                and last_entry.get("timestamp") == old_entry["timestamp"]
            )

            if not is_exact_duplicate:
                history.append(old_entry)

        model.ip_history = history

        if new_ip:
            model.current_ip = new_ip
            model.last_ip = new_ip

        model.current_ip_data = current_ip_data
        model.current_user_agent = request_data.get("headers", {}).get("user-agent")
        model.current_headers = request_data.get("headers", {})
        model.current_port = request_data.get("client_port")

        geo_data = request_data.get("geo", {}) or {}
        model.geo = geo_data
        model.asn = str(geo_data.get("asn")) if geo_data.get("asn") is not None else None
        model.org = geo_data.get("as_org") or geo_data.get("organization")

        unique_ips = {entry["ip"] for entry in model.ip_history if entry.get("ip")}
        if model.current_ip:
            unique_ips.add(model.current_ip)
        model.unique_ip_count = len(unique_ips)

        model.last_seen = now

        self.session.add(model)

    def count_by_fingerprint_since(
        self,
        token_id: uuid.UUID,
        fingerprint: str,
        since: datetime,
    ) -> int:
        stmt = (
            select(TokenEventModel.seen_count)
            .where(
                TokenEventModel.token_id == token_id,
                TokenEventModel.fingerprint == fingerprint,
                TokenEventModel.last_seen >= since,
            )
        )
        result = self.session.execute(stmt).scalar()
        return result or 0