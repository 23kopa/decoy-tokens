from backend.app.application.errors import ValidationError
from backend.app.application.ports.repositories.token_repository import TokenRepositoryPort
from backend.app.domain.entities.token import Token


class ActivateToken:
    def __init__(self, token_repo: TokenRepositoryPort, log_token_event):
        self.token_repo = token_repo
        self.log_token_event = log_token_event

    async def execute(self, slug: str, request) -> Token:
        token = self.token_repo.get_by_slug(slug)
        if not token or not token.is_active:
            raise ValidationError("Не найдено")

        await self.log_token_event.execute(token.id, request)
        return token