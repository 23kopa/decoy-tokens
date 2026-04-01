import uuid

from fastapi import APIRouter, Depends, HTTPException

from backend.app.application.errors import (
    SlugGenerationError,
    UnsupportedTokenTypeError,
    ValidationError,
)
from backend.app.application.use_cases.tokens.create_token import CreateTokenUseCase
from backend.app.application.use_cases.tokens.set_token_active import SetTokenActiveUseCase

from backend.app.web.routes.api.v1.tokens import schemas
from backend.app.web.dependencies.current_user import get_current_user
from backend.app.web.dependencies.use_cases import get_create_token, get_set_token_active

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("", response_model=schemas.TokenCreateOut)
def create_token(
    data: schemas.TokenCreateIn,
    user=Depends(get_current_user),
    uc: CreateTokenUseCase = Depends(get_create_token),
):
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")

    try:
        token = uc.execute(
            user_id=user.id,
            token_type=data.type,
            name=data.name,
            notify_email=data.notify_email,
            desc=data.desc,
            payload=dict(data.payload or {}),
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UnsupportedTokenTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SlugGenerationError as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    user=Depends(get_current_user),
    uc: SetTokenActiveUseCase = Depends(get_set_token_active),
):
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")

    try:
        token = uc.execute(
            token_id=token_id,
            user_id=user.id,
            is_active=payload.is_active,
        )
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "id": str(token.id),
        "is_active": token.is_active,
    }