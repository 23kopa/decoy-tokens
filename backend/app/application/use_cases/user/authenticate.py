from typing import Optional
from backend.app.application.domain.entities.user import User
from backend.app.application.ports.user_repository import UserRepositoryPort


class AuthenticateUser:
    def __init__(self, repo: UserRepositoryPort, verifier):
        self.repo = repo
        self.verifier = verifier

    def execute(self, *, email: str, password: str) -> Optional[User]:
        user = self.repo.get_by_email(email)

        if not user:
            return None

        if not user.verify_password(password, self.verifier):
            return None

        if not user.is_active:
            return None

        return user
