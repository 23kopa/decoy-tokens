import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.domain.entities.token_event import TokenEvent as DomainTokenEvent
from backend.app.infrastructure.database.mappers.token_event import to_domain, to_model
from backend.app.infrastructure.database.models.token_event import TokenEvent as TokenEventModel


class TokenEventCrudMixin:
    session: Session

    def add(self, event: DomainTokenEvent) -> DomainTokenEvent:
        model = to_model(event)
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return to_domain(model)

    def get_event_by_id(self, event_id: uuid.UUID) -> Optional[DomainTokenEvent]:
        stmt = select(TokenEventModel).where(TokenEventModel.id == event_id)
        model = self.session.scalar(stmt)
        return to_domain(model) if model else None

    def get_event_by_fingerprint_id(
        self,
        token_id: uuid.UUID,
        fingerprint: str,
    ) -> Optional[DomainTokenEvent]:
        stmt = (
            select(TokenEventModel)
            .where(
                TokenEventModel.token_id == token_id,
                TokenEventModel.fingerprint == fingerprint,
            )
        )
        model = self.session.scalar(stmt)
        return to_domain(model) if model else None

    def get_last_event_for_token(
        self,
        token_id: uuid.UUID,
        limit: int = 50,
    ) -> list[DomainTokenEvent]:
        stmt = (
            select(TokenEventModel)
            .where(TokenEventModel.token_id == token_id)
            .order_by(TokenEventModel.last_seen.desc())
            .limit(limit)
        )
        return [to_domain(model) for model in self.session.scalars(stmt).all()]

    def count_events_by_token_id(
        self,
        token_id: uuid.UUID,
        since: Optional[datetime] = None,
    ) -> int:
        stmt = select(func.count()).where(TokenEventModel.token_id == token_id)
        if since:
            stmt = stmt.where(TokenEventModel.last_seen >= since)
        return self.session.execute(stmt).scalar() or 0