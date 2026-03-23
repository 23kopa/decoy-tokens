from fastapi import Request, Depends
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.repositories.user import SQLAlchemyUserRepository
from .db import get_db

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None

    repo = SQLAlchemyUserRepository(db)
    return repo.get_by_id(user_id)