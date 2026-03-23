from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_active: bool = True

    def verify_password(self, plain: str, verifier) -> bool:
        return verifier(plain, self.hashed_password)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
