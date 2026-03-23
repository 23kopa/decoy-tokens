from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
import uuid
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.app.web.core.dependencies.current_user import get_current_user
from backend.app.web.core.dependencies.db import get_db
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository

from backend.app.core.config import settings

router = APIRouter()

def format_dt(value: datetime | None) -> str:
    if not value:
        return "—"
    return value.strftime("%d.%m.%Y %H:%M")

@router.get("/dashboard")
async def dashboard(
    request: Request, 
    user=Depends(get_current_user), 
    db: Session = Depends(get_db)
    ):
    
    if not user:
        return RedirectResponse("/", status_code=303)

    templates = request.app.state.templates

    # Репозитории
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)

    # Получаем все токены пользователя
    user_tokens = token_repo.get_all_by_user(owner_user_id=user.id)

    # Формируем карточки
    token_card = [
        {
            "id": token.id,
            "type": token.type,
            "name": token.name,
            "desc": token.desc,
            "created_at": format_dt(token.created_at),
            "is_active": token.is_active,
            "trigger_url": token.trigger_url
        }
        for token in user_tokens
    ]

    token_ids = [token.id for token in user_tokens]

    # Временные метки для статистики
    now = datetime.utcnow()
    hours_24 = now - timedelta(hours=24)

    # Собираем статистику по всем токенам пользователя
    if token_ids:
        stats = event_repo.get_user_stats(
            token_ids=token_ids, hours_24=hours_24
        )
        events_24h = stats.get("events_24h", 0)
        unique_fingerprints = stats.get("unique_fingerprints", 0)
        unique_ips = stats.get("unique_ips", 0)
    else:
        # Для нового пользователя без токенов
        events_24h = 0
        unique_fingerprints = 0
        unique_ips = 0

    context = {
        "request": request,
        "user": user,
        "tokens": user_tokens,
        "token_card": token_card,

        "total_tokens": len(user_tokens),
        "events_24h": events_24h,
        "unique_fingerprints": unique_fingerprints,
        "unique_ips": unique_ips,
    }

    return templates.TemplateResponse("pages/dashboard.html", context)
