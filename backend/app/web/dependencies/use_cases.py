from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings

from backend.app.application.use_cases.user.register import RegisterUserUseCase
from backend.app.application.use_cases.user.authenticate import AuthenticateUserUseCase

from backend.app.application.use_cases.tokens.create_token import CreateTokenUseCase
from backend.app.application.use_cases.tokens.set_token_active import SetTokenActiveUseCase
from backend.app.application.use_cases.tokens.activate_token import ActivateToken
from backend.app.application.use_cases.tokens.list_user_tokens import ListUserTokens

from backend.app.application.use_cases.events.log_token_event import LogTokenEvent
from backend.app.application.use_cases.events.get_tokens_stats import GetTokenStats
from backend.app.application.use_cases.events.get_token_events import GetTokenEvents

from backend.app.infrastructure.database.repositories.user import UserRepository
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository

from backend.app.infrastructure.security.password import hash_password, verify_password
from backend.app.infrastructure.utils.slug import generate_slug
from backend.app.infrastructure.http.token_request_collector import collect_request_info

from backend.app.services.decoy_tokens.utils.detectors.bot import get_bot_type, is_bot
from backend.app.services.decoy_tokens.utils.detectors.dedup import create_deduplicator
from backend.app.services.decoy_tokens.utils.fingerprint.generate import generate_fingerprint

from .db import get_db


def get_register_user(db: Session = Depends(get_db)) -> RegisterUserUseCase:
    repo = UserRepository(db)
    return RegisterUserUseCase(repo, hash_password)


def get_authenticate_user(db: Session = Depends(get_db)) -> AuthenticateUserUseCase:
    repo = UserRepository(db)
    return AuthenticateUserUseCase(repo, verify_password)


def get_create_token(db: Session = Depends(get_db)) -> CreateTokenUseCase:
    repo = TokenRepository(db)
    return CreateTokenUseCase(
        token_repo=repo,
        slug_generator=generate_slug,
        public_base_url=settings.PUBLIC_BASE_URL,
    )


def get_set_token_active(db: Session = Depends(get_db)) -> SetTokenActiveUseCase:
    repo = TokenRepository(db)
    return SetTokenActiveUseCase(token_repo=repo)


def get_log_token_event(db: Session = Depends(get_db)) -> LogTokenEvent:
    repo = TokenEventRepository(db)

    return LogTokenEvent(
        repo=repo,
        request_info_collector=collect_request_info,
        fingerprint_generator=generate_fingerprint,
        is_bot_checker=is_bot,
        bot_type_getter=get_bot_type,
        deduplicator_factory=create_deduplicator,
        trusted_proxies=settings.TRUSTED_PROXIES_SET,
    )


def get_activate_token(
    db: Session = Depends(get_db),
    log_token_event: LogTokenEvent = Depends(get_log_token_event),
) -> ActivateToken:
    token_repo = TokenRepository(db)
    return ActivateToken(
        token_repo=token_repo,
        log_token_event=log_token_event,
    )


def get_token_stats(db: Session = Depends(get_db)) -> GetTokenStats:
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)
    return GetTokenStats(
        token_repo=token_repo,
        event_repo=event_repo,
    )


def get_list_user_tokens(db: Session = Depends(get_db)) -> ListUserTokens:
    token_repo = TokenRepository(db)
    return ListUserTokens(token_repo=token_repo)


def get_token_events(db: Session = Depends(get_db)) -> GetTokenEvents:
    token_repo = TokenRepository(db)
    event_repo = TokenEventRepository(db)
    return GetTokenEvents(
        token_repo=token_repo,
        event_repo=event_repo,
    )