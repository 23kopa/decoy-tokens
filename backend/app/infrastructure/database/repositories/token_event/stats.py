import uuid
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.models.token_event import TokenEvent as TokenEventModel


class TokenEventStatsMixin:
    session: Session

    def count_unique_fingerprints(self, token_id: uuid.UUID) -> int:
        stmt = select(func.count(func.distinct(TokenEventModel.fingerprint))).where(
            TokenEventModel.token_id == token_id
        )
        return self.session.execute(stmt).scalar() or 0

    def count_max_unique_ips(self, token_id: uuid.UUID) -> int:
        stmt = select(func.max(TokenEventModel.unique_ip_count)).where(
            TokenEventModel.token_id == token_id
        )
        return self.session.execute(stmt).scalar() or 0

    def get_user_stats(self, token_ids: list[uuid.UUID], hours_24: datetime) -> dict:
        if not token_ids:
            return {"events_24h": 0, "unique_fingerprints": 0, "unique_ips": 0}

        stmt_24h = select(func.count()).where(
            TokenEventModel.token_id.in_(token_ids),
            TokenEventModel.last_seen >= hours_24,
        )
        events_24h = self.session.execute(stmt_24h).scalar() or 0

        stmt_fp = select(func.count(func.distinct(TokenEventModel.fingerprint))).where(
            TokenEventModel.token_id.in_(token_ids)
        )
        unique_fingerprints = self.session.execute(stmt_fp).scalar() or 0

        stmt_ip = select(func.count(func.distinct(TokenEventModel.current_ip))).where(
            TokenEventModel.token_id.in_(token_ids),
            TokenEventModel.current_ip.is_not(None),
        )
        unique_ips = self.session.execute(stmt_ip).scalar() or 0

        return {
            "events_24h": events_24h,
            "unique_fingerprints": unique_fingerprints,
            "unique_ips": unique_ips,
        }

    def get_token_stats(self, token_id: uuid.UUID) -> dict:
        stmt_first = select(func.min(TokenEventModel.first_seen)).where(
            TokenEventModel.token_id == token_id
        )
        first_seen = self.session.execute(stmt_first).scalar()

        stmt_last = select(func.max(TokenEventModel.last_seen)).where(
            TokenEventModel.token_id == token_id
        )
        last_seen = self.session.execute(stmt_last).scalar()

        stmt_total = select(func.sum(TokenEventModel.seen_count)).where(
            TokenEventModel.token_id == token_id
        )
        total_events = self.session.execute(stmt_total).scalar() or 0

        return {
            "first_seen": first_seen,
            "last_seen": last_seen,
            "total_events": total_events,
            "unique_ips": self.count_max_unique_ips(token_id),
            "unique_fingerprints": self.count_unique_fingerprints(token_id),
        }