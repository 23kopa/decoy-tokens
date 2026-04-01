from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class Token:
    id: UUID
    slug: str
    owner_user_id: int
    type: str
    name: str
    notify_email: str
    desc: str | None
    payload: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    trigger_url: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False