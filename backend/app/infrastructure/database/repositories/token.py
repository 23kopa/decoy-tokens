import uuid
from typing import Optional

from sqlalchemy import select, desc, asc
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.base import BaseRepository
from backend.app.infrastructure.database.models.token import Token

class TokenRepository(BaseRepository[Token]):
    def __init__(self, session: Session):
        super().__init__(session, Token)

    def get_by_id_and_user(self, token_id: uuid.UUID, user_id: int) -> Optional[Token]:
        stmt = select(Token).where(
            Token.id == token_id,
            Token.owner_user_id == user_id
        )
        return self.session.scalar(stmt)

    def get_by_slug(self, slug: str) -> Optional[Token]:
        stmt = select(Token).where(Token.slug == slug)
        return self.session.scalar(stmt)

    def get_all_by_user(
        self, 
        owner_user_id: int,
        
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100
        ) -> list[Token]:

        stmt = select(Token).where(Token.owner_user_id == owner_user_id)

        if sort_order == "desc":
            stmt = stmt.order_by(desc(getattr(Token, sort_by)))
        else:
            stmt = stmt.order_by(asc(getattr(Token, sort_by)))        

        stmt = stmt.offset(skip).limit(limit)

        return list(self.session.scalars(stmt).all())

    def get_active_by_user(
        self, 
        owner_user_id: int,
        only_active = True,
        
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100
        ) -> list[Token]:

        stmt = select(Token).where(Token.owner_user_id == owner_user_id, Token.is_active.is_(True))

        if sort_order == "desc":
            stmt = stmt.order_by(desc(getattr(Token, sort_by)))
        else:
            stmt = stmt.order_by(asc(getattr(Token, sort_by)))        

        stmt = stmt.offset(skip).limit(limit)

        return list(self.session.scalars(stmt).all())

    def get_inactive_by_user(
        self, 
        owner_user_id: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100
        ) -> list[Token]:

        stmt = select(Token).where(
            Token.owner_user_id == owner_user_id, 
            Token.is_active == False
        )

        # Применяем сортировку
        if sort_order == "desc":
            stmt = stmt.order_by(desc(getattr(Token, sort_by)))
        else:
            stmt = stmt.order_by(asc(getattr(Token, sort_by)))        

        # Применяем пагинацию
        stmt = stmt.offset(skip).limit(limit)

        return list(self.session.scalars(stmt).all())
    
    def set_active(self, token_id, user_id, is_active: bool):
        token = self.get_by_id_and_user(token_id, user_id)
        if not token:
            return None

        token.is_active = is_active
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token