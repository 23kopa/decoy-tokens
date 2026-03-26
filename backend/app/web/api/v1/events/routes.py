# backend/app/web/api/v1/tokens/events_routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional
from datetime import datetime, timedelta

from backend.app.web.core.dependencies.current_user import get_current_user
from backend.app.web.core.dependencies.db import get_db

from backend.app.infrastructure.database.models.user import User
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.services.decoy_tokens.event_presenter import build_event_responses
from backend.app.web.api.v1.events.schemas import EventResponse

router = APIRouter(prefix="/tokens/{token_id}/events", tags=["token-events"])

@router.get("", response_model=List[EventResponse])
async def get_token_events(
    token_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100),
):
    token_repo = TokenRepository(db)
    token = token_repo.get_by_id_and_user(token_id, current_user.id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    event_repo = TokenEventRepository(db)
    events = event_repo.get_last_event_for_token(token_id, limit=limit)

    return build_event_responses(events)

@router.get("/stats", response_model=dict)
async def get_token_events_stats(
    token_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
      
    # Проверяем доступ к токену
    token_repo = TokenRepository(db)
    token = token_repo.get_by_id_and_user(token_id, current_user.id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    # Получаем статистику через существующие методы
    event_repo = TokenEventRepository(db)
    
    # Используем get_token_stats
    stats = event_repo.get_token_stats(token_id)
    
    # Добавляем общее количество событий
    total_events = event_repo.count_events_by_token_id(token_id)
    
    return {
        "total_events": total_events,
        "unique_fingerprints": stats["unique_fingerprints"],
        "unique_ips": stats["unique_ips"],
        "first_seen": stats["first_seen"],
        "last_seen": stats["last_seen"],
    }