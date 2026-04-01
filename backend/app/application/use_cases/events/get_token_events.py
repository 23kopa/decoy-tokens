from __future__ import annotations

from uuid import UUID

from backend.app.application.errors import ValidationError
from backend.app.application.ports.event_repository import TokenEventRepositoryPort
from backend.app.application.ports.token_repository import TokenRepositoryPort
from backend.app.domain.entities.token_event import TokenEvent


class GetTokenEvents:
    def __init__(
        self,
        token_repo: TokenRepositoryPort,
        event_repo: TokenEventRepositoryPort,
    ):
        self.token_repo = token_repo
        self.event_repo = event_repo

    def execute(
        self,
        *,
        token_id: UUID,
        user_id: int,
        limit: int = 50,
    ) -> list[TokenEvent]:
        token = self.token_repo.get_by_id_and_user(token_id, user_id)
        if not token:
            raise ValidationError("Token not found")

        return self.event_repo.get_last_event_for_token(token_id, limit=limit)