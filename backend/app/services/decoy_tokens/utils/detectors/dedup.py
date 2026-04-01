from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from backend.app.application.ports.repositories.event_repository import TokenEventRepositoryPort


class Deduplicator:
    def __init__(self, repo: TokenEventRepositoryPort, window_seconds: int = 60):
        self.repo = repo
        self.window_seconds = window_seconds

    def process(self, token_id: UUID, fingerprint: str, request_data: dict[str, Any]) -> bool:
        existing = self.repo.get_event_by_fingerprint_id(token_id, fingerprint)
        if existing:
            self.repo.update_event_with_new_ip(
                event=existing,
                current_ip_data=request_data.get("ip_data", {}),
                request_data=request_data,
            )
            return True

        return False


class AdvancedDeduplicator(Deduplicator):
    def __init__(
        self,
        repo: TokenEventRepositoryPort,
        window_seconds: int = 60,
        max_visits_per_day: int = 10,
    ):
        super().__init__(repo, window_seconds)
        self.max_visits_per_day = max_visits_per_day

    def check_rate_limit(self, token_id: UUID, fingerprint: str) -> bool:
        day_ago = datetime.utcnow() - timedelta(days=1)
        visits_today = self.repo.count_by_fingerprint_since(
            token_id=token_id,
            fingerprint=fingerprint,
            since=day_ago,
        )
        return visits_today >= self.max_visits_per_day


def create_deduplicator(
    repo: TokenEventRepositoryPort,
    window_seconds: int = 60,
) -> Deduplicator:
    return Deduplicator(repo, window_seconds)