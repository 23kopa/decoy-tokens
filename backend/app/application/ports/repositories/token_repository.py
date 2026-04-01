from __future__ import annotations

from typing import Protocol
from uuid import UUID

from backend.app.domain.entities.token import Token


class TokenRepositoryPort(Protocol):
    def add(self, token: Token) -> Token: ...
    def get_by_slug(self, slug: str) -> Token | None: ...
    def get_by_id(self, token_id: UUID) -> Token | None: ...
    def get_by_id_and_user(self, token_id: UUID, user_id: int) -> Token | None: ...
    def update(self, token: Token) -> Token: ...
    def get_all_by_user(
        self,
        owner_user_id: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100,
    ) -> list[Token]: ...