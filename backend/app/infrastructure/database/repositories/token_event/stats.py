import uuid
from datetime import datetime
from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.models.token_event import TokenEvent


class TokenEventStatsMixin:

    session: Session

    def count_unique_fingerprints(self, token_id: uuid.UUID) -> int:
        stmt = select(func.count(func.distinct(TokenEvent.fingerprint))).where(
            TokenEvent.token_id == token_id
        )
        return self.session.execute(stmt).scalar() or 0

    def count_max_unique_ips(self, token_id: uuid.UUID) -> int:
        stmt = select(func.max(TokenEvent.unique_ip_count)).where(
            TokenEvent.token_id == token_id
        )
        return self.session.execute(stmt).scalar() or 0

    def get_user_stats(
        self, token_ids: List[uuid.UUID], hours_24: datetime) -> dict:
        if not token_ids:
            return {"events_24h": 0, "unique_sources": 0, "hits_7d": 0}

        # События за 24 часа
        stmt_24h = select(func.count()).where(
            TokenEvent.token_id.in_(token_ids), TokenEvent.last_seen >= hours_24
        )
        events_24h = self.session.execute(stmt_24h).scalar() or 0

        # Уникальные fingerprint
        stmt_fp = select(func.count(func.distinct(TokenEvent.fingerprint))).where(
            TokenEvent.token_id.in_(token_ids)
        )
        unique_fingerprints = self.session.execute(stmt_fp).scalar() or 0

        # Уникальные IP
        stmt_ip = select(func.count(func.distinct(TokenEvent.current_ip))).where(
            TokenEvent.token_id.in_(token_ids),
            TokenEvent.current_ip.is_not(None),
        )
        unique_ips = self.session.execute(stmt_ip).scalar() or 0

        return {
          "events_24h": events_24h,
          "unique_fingerprints": unique_fingerprints,
          "unique_ips": unique_ips,
        }

    def get_token_stats(self, token_id: uuid.UUID) -> dict:
        # Первое и последнее событие
        stmt_first = select(func.min(TokenEvent.first_seen)).where(
            TokenEvent.token_id == token_id
        )
        first_seen = self.session.execute(stmt_first).scalar()

        stmt_last = select(func.max(TokenEvent.last_seen)).where(
            TokenEvent.token_id == token_id
        )
        last_seen = self.session.execute(stmt_last).scalar()

        # Уникальные IP из истории
        unique_ips = self.count_max_unique_ips(token_id)

        # Сумма seen_count
        stmt_total = select(func.sum(TokenEvent.seen_count)).where(
            TokenEvent.token_id == token_id
        )
        total_events = self.session.execute(stmt_total).scalar() or 0

        return {
            "first_seen": first_seen,
            "last_seen": last_seen,
            "total_events": total_events,
            "unique_ips": unique_ips,
            "unique_fingerprints": self.count_unique_fingerprints(token_id),
        }


