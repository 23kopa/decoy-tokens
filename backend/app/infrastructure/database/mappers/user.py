from backend.app.domain.entities.user import User as DomainUser
from backend.app.infrastructure.database.models.user import User as ORMUser

class UserMapper:
    @staticmethod
    def to_domain(orm: ORMUser) -> DomainUser:
        return DomainUser(
            id=orm.id,
            email=orm.email,
            username=orm.username,
            hashed_password=orm.hashed_password,
            is_active=orm.is_active,
        )

    @staticmethod
    def to_orm_new(domain: DomainUser) -> ORMUser:
        return ORMUser(
            email=domain.email,
            username=domain.username,
            hashed_password=domain.hashed_password,
            is_active=domain.is_active,
        )
    
    @staticmethod
    def apply_to_orm(orm: ORMUser, domain: DomainUser) -> ORMUser:
        orm.email = domain.email
        orm.username = domain.username
        orm.hashed_password = domain.hashed_password
        orm.is_active = domain.is_active
        return orm