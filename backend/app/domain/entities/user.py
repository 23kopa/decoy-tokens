from dataclasses import dataclass
from typing import Optional

from backend.app.domain.value.email import Email


@dataclass
class User:
    id: Optional[int]
    email: Email
    username: str
    hashed_password: str
    is_active: bool = True

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
