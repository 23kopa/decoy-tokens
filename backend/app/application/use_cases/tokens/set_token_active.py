from __future__ import annotations

from uuid import UUID

from backend.app.application.errors import ValidationError
from backend.app.application.ports.token_repository import TokenRepositoryPort
from backend.app.domain.entities.token import Token


class SetTokenActiveUseCase:
    def __init__(self, token_repo: TokenRepositoryPort):
        self.token_repo = token_repo

    def execute(self, *, token_id: UUID, user_id: int, is_active: bool) -> Token:
        token = self.token_repo.get_by_id_and_user(token_id, user_id)
        if not token:
            raise ValidationError("Token not found")

        if is_active:
            token.activate()
        else:
            token.deactivate()

        return self.token_repo.update(token)