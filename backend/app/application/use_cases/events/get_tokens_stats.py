from __future__ import annotations

from uuid import UUID

from backend.app.application.ports.repositories.event_repository import TokenEventRepositoryPort
from backend.app.application.ports.repositories.token_repository import TokenRepositoryPort
from backend.app.application.errors import ValidationError


class GetTokenStats:
    def __init__(
        self,
        token_repo: TokenRepositoryPort,
        event_repo: TokenEventRepositoryPort,
    ):
        self.token_repo = token_repo
        self.event_repo = event_repo

    def execute(self, token_id: UUID, user_id: int) -> dict:
        token = self.token_repo.get_by_id_and_user(token_id, user_id)
        if not token:
            raise ValidationError("Token not found")

        stats = self.event_repo.get_token_stats(token_id)
        total_events = self.event_repo.count_events_by_token_id(token_id)

        return {
            "total_events": total_events,
            "unique_fingerprints": stats["unique_fingerprints"],
            "unique_ips": stats["unique_ips"],
            "first_seen": stats["first_seen"],
            "last_seen": stats["last_seen"],
        }