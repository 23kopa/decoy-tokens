from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.services.decoy_tokens.token_activator import TokenActivatorService
from backend.app.web.core.dependencies.db import get_db

router = APIRouter(prefix="/t", tags=["public"])


@router.get("/{slug}", include_in_schema=False)
async def activate_token(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)

    activator = TokenActivatorService(
        token_repo=token_repo,
        event_repo=event_repo,
    )
    response = await activator.activate(slug, request)

    db.commit()
    return response