from __future__ import annotations

from backend.app.application.ports.token_repository import TokenRepositoryPort


class ListUserTokens:
    def __init__(self, token_repo: TokenRepositoryPort):
        self.token_repo = token_repo

    def execute(
        self,
        user_id: int,
        *,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100,
    ):
        return self.token_repo.get_all_by_user(
            owner_user_id=user_id,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
        )