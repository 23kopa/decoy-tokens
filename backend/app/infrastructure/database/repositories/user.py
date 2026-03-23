from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.application.ports.user_repository import UserRepositoryPort
from backend.app.application.domain.entities.user import User as DomainUser
from backend.app.infrastructure.database.models.user import User as ORMUser
from backend.app.infrastructure.database.base import BaseRepository
from backend.app.infrastructure.database.mappers.user import UserMapper

class SQLAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session
        self.base = BaseRepository(session, ORMUser)

    def get_by_id(self, user_id: int) -> DomainUser | None:
        orm = self.base.get_by_id(user_id)
        return UserMapper.to_domain(orm) if orm else None

    def get_by_email(self, email: str) -> DomainUser | None:
        orm = self.session.query(ORMUser).filter(ORMUser.email == email).first()
        return UserMapper.to_domain(orm) if orm else None

    def add(self, user: DomainUser) -> DomainUser:
        orm = UserMapper.to_orm_new(user)
        try:
            orm = self.base.add(orm)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Пользователь с таким Email уже зарегистрирован")    
        return UserMapper.to_domain(orm)

    def update(self, user: DomainUser) -> DomainUser:
        if user.id is None:
            raise ValueError("Нельзя обновить пользователя без id")

        orm = self.session.get(ORMUser, user.id)
        if orm is None:
            raise ValueError("Пользователь не найден")

        UserMapper.apply_to_orm(orm, user)

        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Пользователь с таким Email уже зарегистрирован")

        return UserMapper.to_domain(orm)