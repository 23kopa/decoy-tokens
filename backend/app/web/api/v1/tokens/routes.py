import uuid
from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.web.core.dependencies.current_user import get_current_user
from backend.app.web.core.dependencies.db import get_db
from backend.app.web.api.v1.tokens import schemas
from backend.app.web.api.v1.dependencies import get_token_repository

from backend.app.infrastructure.database.models.token import Token
from backend.app.services.decoy_tokens.security import generate_secret, hash_secret
from backend.app.core.config import settings

router = APIRouter(prefix="/tokens", tags=["tokens"])

@router.post("", response_model=schemas.TokenCreateOut)
def create_token(
    data: schemas.TokenCreateIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")
    
    if not data.name or not data.name.strip():
      raise HTTPException(
          status_code=400, 
          detail="Название токена обязательно"
      )

    token_type = data.type

    # MVP: только link/email
    payload: dict[str, Any] = dict(data.payload or {})
    if token_type == "link":
        if not payload.get("redirect_url"):
            payload["show_gif"] = True
        else:
            payload["show_gif"] = False
    elif token_type == "email":
        payload = {}
    else:
        raise HTTPException(
            status_code=400, detail=f"Неподдерживаемый тип токена: {token_type}"
        )

    secret = generate_secret()
    token_id = uuid.uuid4()
    trigger_url = f"{settings.PUBLIC_BASE_URL}/t/{token_id}/{secret}"

    token = Token(
        id=token_id,
        owner_user_id=user.id,
        type=token_type,
        name=data.name.strip(),
        notify_email=data.notify_email,
        desc=data.desc,
        payload=payload,
        secret_hash=hash_secret(secret),
        is_active=True,
        trigger_url=trigger_url, 
    )
    token_repo = get_token_repository(db)
    token_repo.add(token)
    db.commit()

    #if notify_email:
    #    send_notification(notify_email, trigger_url, token.name)

    return schemas.TokenCreateOut(
        id=token.id,
        type=token.type,
        name=token.name,
        desc=token.desc,
        trigger_url=trigger_url,
    )

@router.patch("/{token_id}/status")
async def update_token_status(
    token_id: uuid.UUID,
    payload: schemas.TokenStatusUpdateRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    token_repo = get_token_repository(db)
    token = token_repo.set_active(
        token_id=token_id,
        user_id=user.id,
        is_active=payload.is_active,
    )

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    return {
        "id": str(token.id),
        "is_active": token.is_active,
    }