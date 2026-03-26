from fastapi import HTTPException
from starlette.requests import Request

from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.infrastructure.database.repositories.token_event import TokenEventRepository
from backend.app.services.decoy_tokens.engines.email import EmailEngine
from backend.app.services.decoy_tokens.engines.link import LinkEngine
from backend.app.services.decoy_tokens.token_event_logger import TokenEventLoggerService


class TokenActivatorService:
    def __init__(
        self,
        token_repo: TokenRepository,
        event_repo: TokenEventRepository,
    ):
        self.token_repo = token_repo
        self.event_repo = event_repo

    async def activate(self, slug: str, request: Request):
        token = self.token_repo.get_by_slug(slug)
        if not token or not token.is_active:
            raise HTTPException(status_code=404, detail="Не найдено")

        trusted_proxies = {
            "127.0.0.1",
            "localhost",
            "::1",
            "172.16.0.0/12",
            "10.0.0.0/8",
            "192.168.0.0/16",
        }

        event_logger = TokenEventLoggerService(
            self.event_repo,
            trusted_proxies=trusted_proxies,
        )
        await event_logger.log_hit(token.id, request)

        engine = self._pick_engine(token.type)
        return engine.render(token, request)

    def _pick_engine(self, token_type: str):
        if token_type == "link":
            return LinkEngine()
        if token_type == "email":
            return EmailEngine()

        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тип токена: {token_type}",
        )