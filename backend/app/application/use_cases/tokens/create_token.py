from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from backend.app.application.errors import (
    SlugGenerationError,
    UnsupportedTokenTypeError,
    ValidationError,
)
from backend.app.application.ports.token_repository import TokenRepositoryPort
from backend.app.domain.entities.token import Token


class CreateTokenUseCase:
    def __init__(
        self,
        token_repo: TokenRepositoryPort,
        slug_generator: Callable[[int], str],
        public_base_url: str,
    ):
        self.token_repo = token_repo
        self.slug_generator = slug_generator
        self.public_base_url = public_base_url.rstrip("/")

    def execute(
        self,
        *,
        user_id: int,
        token_type: str,
        name: str,
        notify_email: str,
        desc: str | None,
        payload: dict[str, Any] | None = None,
    ) -> Token:
        normalized_name = (name or "").strip()
        if not normalized_name:
            raise ValidationError("Название токена обязательно")

        prepared_payload = self._build_payload(token_type, payload or {})
        slug = self._build_unique_slug()
        trigger_url = f"{self.public_base_url}/t/{slug}"

        token = Token(
            id=uuid4(),
            slug=slug,
            owner_user_id=user_id,
            type=token_type,
            name=normalized_name,
            notify_email=notify_email,
            desc=desc,
            payload=prepared_payload,
            is_active=True,
            trigger_url=trigger_url,
        )

        return self.token_repo.add(token)

    def _build_payload(self, token_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        prepared_payload = dict(payload)

        if token_type == "link":
            prepared_payload["show_gif"] = not bool(prepared_payload.get("redirect_url"))
            return prepared_payload

        if token_type == "email":
            return {}

        raise UnsupportedTokenTypeError(f"Неподдерживаемый тип токена: {token_type}")

    def _build_unique_slug(self, length: int = 10, max_attempts: int = 20) -> str:
        for _ in range(max_attempts):
            slug = self.slug_generator(length)
            if not self.token_repo.get_by_slug(slug):
                return slug

        raise SlugGenerationError("Не удалось сгенерировать уникальный slug")