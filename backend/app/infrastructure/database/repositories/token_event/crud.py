# backend/app/infrastructure/database/repositories/token_event/crud.py

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.models.token_event import TokenEvent

class TokenEventCrudMixin:
    
    session: Session

    def get_event_by_id(self, event_id: uuid.UUID) -> Optional[TokenEvent]:
        stmt = select(TokenEvent).where(TokenEvent.id == event_id)
        return self.session.scalar(stmt)

    def get_event_by_fingerprint_id(
        self,
        token_id: uuid.UUID,
        fingerprint: str,
    ) -> Optional[TokenEvent]:
        
        stmt = (
            select(TokenEvent)
            .where(
                TokenEvent.token_id == token_id,
                TokenEvent.fingerprint == fingerprint,
            )
        )
        return self.session.scalars(stmt).first()

    def get_last_event_for_token(
            self,
            token_id: uuid.UUID,
            limit: int = 50
    ) -> List[TokenEvent]:
        
        stmt = (
            select(TokenEvent)
            .where(TokenEvent.token_id == token_id)
            .order_by(TokenEvent.last_seen.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def count_events_by_token_id(
        self,
        token_id: uuid.UUID,
        since: Optional[datetime] = None
    ) -> int:
        
        stmt = select(func.count()).where(TokenEvent.token_id == token_id)
        if since:
            stmt = stmt.where(TokenEvent.last_seen >= since)
        return self.session.execute(stmt).scalar() or 0