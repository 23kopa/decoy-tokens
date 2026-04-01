# backend/app/web/api/v1/tokens/events_routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from backend.app.web.dependencies.current_user import get_current_user
from backend.app.web.dependencies.db import get_db

from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository

from backend.app.application.errors import ValidationError

from backend.app.application.use_cases.events.get_tokens_stats import GetTokenStats
from backend.app.application.use_cases.events.get_token_events import GetTokenEvents

from backend.app.web.routes.api.v1.events.presenter import build_event_responses
from backend.app.web.routes.api.v1.events.schemas import EventResponse

router = APIRouter(prefix="/tokens/{token_id}/events", tags=["token-events"])


@router.get("", response_model=List[EventResponse])
async def get_token_events(
    token_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100),
):
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)

    uc = GetTokenEvents(
        token_repo=token_repo,
        event_repo=event_repo,
    )

    try:
        events = uc.execute(
            token_id=token_id,
            user_id=current_user.id,
            limit=limit,
        )
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return build_event_responses(events)

@router.get("/stats", response_model=dict)
async def get_token_events_stats(
    token_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)
    uc = GetTokenStats(token_repo=token_repo, event_repo=event_repo)

    try:
        return uc.execute(token_id=token_id, user_id=current_user.id)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))