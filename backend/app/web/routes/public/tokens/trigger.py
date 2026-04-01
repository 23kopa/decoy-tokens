from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.app.application.errors import ValidationError
from backend.app.application.use_cases.tokens.activate_token import ActivateToken
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.infrastructure.http.token_request_collector import collect_request_info
from backend.app.services.decoy_tokens.engines.email import EmailEngine
from backend.app.services.decoy_tokens.engines.link import LinkEngine
from backend.app.services.decoy_tokens.utils.detectors.bot import get_bot_type, is_bot
from backend.app.services.decoy_tokens.utils.detectors.dedup import create_deduplicator
from backend.app.services.decoy_tokens.utils.fingerprint.generate import generate_fingerprint
from backend.app.application.use_cases.events.log_token_event import LogTokenEvent
from backend.app.web.dependencies.db import get_db

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
    db: Session = Depends(get_db),
):
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)

    trusted_proxies = {
        "127.0.0.1",
        "localhost",
        "::1",
        "172.16.0.0/12",
        "10.0.0.0/8",
        "192.168.0.0/16",
    }

    log_event_uc = LogTokenEvent(
        repo=event_repo,
        request_info_collector=collect_request_info,
        fingerprint_generator=generate_fingerprint,
        is_bot_checker=is_bot,
        bot_type_getter=get_bot_type,
        deduplicator_factory=lambda repo: create_deduplicator(repo, window_seconds=60),
        trusted_proxies=trusted_proxies,
    )

    activate_uc = ActivateToken(
        token_repo=token_repo,
        log_token_event=log_event_uc,
    )

    try:
        token = await activate_uc.execute(slug, request)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

    db.commit()

    engine = pick_engine(token.type)
    return engine.render(token, request)