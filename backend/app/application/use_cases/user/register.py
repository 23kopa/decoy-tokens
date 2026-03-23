from backend.app.application.domain.entities.user import User
from backend.app.application.ports.user_repository import UserRepositoryPort


class RegisterUser:
    def __init__(self, repo: UserRepositoryPort, hasher):
        self.repo = repo
        self.hasher = hasher

    def execute(self, *, email: str, username: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise ValueError("Пользователь с таким Email уже зарегистрирован")

        user = User(
            id=None,
            email=email,
            username=username,
            hashed_password=self.hasher(password),
            is_active=True,
        )

        return self.repo.add(user)
