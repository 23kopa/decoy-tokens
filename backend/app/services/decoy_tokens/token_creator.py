import string
import uuid
from typing import Any

from fastapi import HTTPException

from backend.app.core.config import settings
from backend.app.infrastructure.database.models.token import Token
from backend.app.infrastructure.database.repositories.token import TokenRepository
from backend.app.services.decoy_tokens.shared.slug import generate_slug


class TokenCreateService:
    def __init__(self, token_repo: TokenRepository):
        self.token_repo = token_repo

    def create(
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
            raise HTTPException(status_code=400, detail="Название токена обязательно")

        prepared_payload = self._build_payload(token_type, payload or {})
        slug = self._build_unique_slug()
        trigger_url = f"{settings.PUBLIC_BASE_URL}/t/{slug}"

        token = Token(
            id=uuid.uuid4(),
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

        self.token_repo.add(token)
        return token

    def _build_payload(self, token_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        prepared_payload = dict(payload)

        if token_type == "link":
            if not prepared_payload.get("redirect_url"):
                prepared_payload["show_gif"] = True
            else:
                prepared_payload["show_gif"] = False
            return prepared_payload

        if token_type == "email":
            return {}

        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тип токена: {token_type}",
        )

    def _build_unique_slug(self, length: int = 10) -> str:
        for _ in range(20):
            slug = generate_slug(length)
            if not self.token_repo.get_by_slug(slug):
                return slug

        raise RuntimeError("Не удалось сгенерировать уникальный slug")