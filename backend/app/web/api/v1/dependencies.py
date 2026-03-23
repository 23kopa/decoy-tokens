from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.web.core.dependencies.db import get_db
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository

def get_token_repository(db: Session = Depends(get_db)) -> TokenRepository:
    """Фабрика репозитория токенов"""
    return TokenRepository(db)


def get_token_event_repository(db: Session = Depends(get_db)) -> TokenEventRepository:
    """Фабрика репозитория событий токенов"""
    return TokenEventRepository(db)