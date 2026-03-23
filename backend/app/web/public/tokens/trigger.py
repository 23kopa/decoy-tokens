"""
Публичные эндпоинты для активации токенов.
Не требуют аутентификации.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.app.web.core.dependencies.db import get_db
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.services.decoy_tokens.security import verify_secret
from backend.app.services.decoy_tokens.events import TokenEventService
from backend.app.services.decoy_tokens.engines.link import LinkEngine
from backend.app.services.decoy_tokens.engines.email import EmailEngine

router = APIRouter(prefix="/t", tags=["public"])


def pick_engine(token_type: str):
    if token_type == "link":
        return LinkEngine()
    if token_type == "email":
        return EmailEngine()
    raise HTTPException(status_code=400, detail=f"Неподдерживаемый тип токена: {token_type}")


@router.get("/{token_id}/{secret}", include_in_schema=False)
async def activate_token(
    token_id: uuid.UUID,
    secret: str,
    request: Request,
    db: Session = Depends(get_db)
):
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)

    token = token_repo.get_by_id(token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    if not token.is_active:
        raise HTTPException(status_code=404, detail="Не найдено")

    if not verify_secret(secret, token.secret_hash):
        raise HTTPException(status_code=404, detail="Не найдено")

    trusted_proxies={
        "127.0.0.1", 
        "localhost", 
        "::1",
        "172.16.0.0/12",  # Docker network (все IP от 172.16.0.0 до 172.31.255.255)
        "10.0.0.0/8",      # Приватные сети
        "192.168.0.0/16"   # Приватные сети
    }

    # Логируем визит
    ev_service = TokenEventService(event_repo, trusted_proxies=trusted_proxies)
    await ev_service.log_hit(token.id, request)
    db.commit()

    engine = pick_engine(token.type)
    return engine.render(token, request)