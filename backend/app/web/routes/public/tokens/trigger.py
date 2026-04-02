from fastapi import APIRouter, Depends, HTTPException, Request

from backend.app.application.errors import ValidationError
from backend.app.application.use_cases.tokens.activate_token import ActivateToken
from backend.app.services.decoy_tokens.engines.email import EmailEngine
from backend.app.services.decoy_tokens.engines.link import LinkEngine
from backend.app.web.dependencies.use_cases import get_activate_token

router = APIRouter(prefix="/t", tags=["public"])


def pick_engine(token_type: str):
    if token_type == "link":
        return LinkEngine()
    if token_type == "email":
        return EmailEngine()
    raise HTTPException(status_code=400, detail=f"Неподдерживаемый тип токена: {token_type}")


@router.get("/{slug}", include_in_schema=False)
async def activate_token(
    slug: str,
    request: Request,
    uc: ActivateToken = Depends(get_activate_token),
):
    try:
        token = await uc.execute(slug, request)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

    engine = pick_engine(token.type)
    return engine.render(token, request)