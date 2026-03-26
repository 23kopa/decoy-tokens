import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.web.api.v1.dependencies import get_token_repository
from backend.app.web.api.v1.tokens import schemas
from backend.app.web.core.dependencies.current_user import get_current_user
from backend.app.web.core.dependencies.db import get_db
from backend.app.services.decoy_tokens.token_creator import TokenCreateService

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("", response_model=schemas.TokenCreateOut)
def create_token(
    data: schemas.TokenCreateIn,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")

    token_repo = get_token_repository(db)
    token_creator = TokenCreateService(token_repo)

    token = token_creator.create(
        user_id=user.id,
        token_type=data.type,
        name=data.name,
        notify_email=data.notify_email,
        desc=data.desc,
        payload=dict(data.payload or {}),
    )
    db.commit()

    return schemas.TokenCreateOut(
        id=token.id,
        type=token.type,
        name=token.name,
        desc=token.desc,
        trigger_url=token.trigger_url,
    )


@router.patch("/{token_id}/status")
async def update_token_status(
    token_id: uuid.UUID,
    payload: schemas.TokenStatusUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
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