import uuid
from typing import Optional

from sqlalchemy import select, desc, asc
from sqlalchemy.orm import Session

from backend.app.domain.entities.token import Token as DomainToken
from backend.app.infrastructure.database.models.token import Token as TokenModel
from backend.app.infrastructure.database.mappers.token import to_domain, to_model


class TokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, token: DomainToken) -> DomainToken:
        model = to_model(token)
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return to_domain(model)

    def get_by_id(self, token_id: uuid.UUID) -> Optional[DomainToken]:
        stmt = select(TokenModel).where(TokenModel.id == token_id)
        model = self.session.scalar(stmt)
        return to_domain(model) if model else None

    def get_by_slug(self, slug: str) -> Optional[DomainToken]:
        stmt = select(TokenModel).where(TokenModel.slug == slug)
        model = self.session.scalar(stmt)
        return to_domain(model) if model else None

    def get_by_id_and_user(self, token_id: uuid.UUID, user_id: int) -> Optional[DomainToken]:
        stmt = select(TokenModel).where(
            TokenModel.id == token_id,
            TokenModel.owner_user_id == user_id,
        )
        model = self.session.scalar(stmt)
        return to_domain(model) if model else None

    def get_all_by_user(
        self,
        owner_user_id: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100,
    ) -> list[DomainToken]:
        stmt = select(TokenModel).where(TokenModel.owner_user_id == owner_user_id)

        column = getattr(TokenModel, sort_by)
        stmt = stmt.order_by(desc(column) if sort_order == "desc" else asc(column))
        stmt = stmt.offset(skip).limit(limit)

        return [to_domain(model) for model in self.session.scalars(stmt).all()]

    def get_active_by_user(
        self,
        owner_user_id: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100,
    ) -> list[DomainToken]:
        stmt = select(TokenModel).where(
            TokenModel.owner_user_id == owner_user_id,
            TokenModel.is_active.is_(True),
        )

        column = getattr(TokenModel, sort_by)
        stmt = stmt.order_by(desc(column) if sort_order == "desc" else asc(column))
        stmt = stmt.offset(skip).limit(limit)

        return [to_domain(model) for model in self.session.scalars(stmt).all()]

    def get_inactive_by_user(
        self,
        owner_user_id: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100,
    ) -> list[DomainToken]:
        stmt = select(TokenModel).where(
            TokenModel.owner_user_id == owner_user_id,
            TokenModel.is_active.is_(False),
        )

        column = getattr(TokenModel, sort_by)
        stmt = stmt.order_by(desc(column) if sort_order == "desc" else asc(column))
        stmt = stmt.offset(skip).limit(limit)

        return [to_domain(model) for model in self.session.scalars(stmt).all()]

    def update(self, token: DomainToken) -> DomainToken:
        stmt = select(TokenModel).where(TokenModel.id == token.id)
        model = self.session.scalar(stmt)
        if not model:
            raise ValueError("Token not found")

        model.slug = token.slug
        model.owner_user_id = token.owner_user_id
        model.type = token.type
        model.name = token.name
        model.notify_email = token.notify_email
        model.desc = token.desc
        model.payload = token.payload
        model.is_active = token.is_active
        model.trigger_url = token.trigger_url
        model.expires_at = token.expires_at

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_domain(model)