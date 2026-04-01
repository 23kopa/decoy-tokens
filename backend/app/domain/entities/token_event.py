from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class TokenEvent:
    id: UUID | None
    token_id: UUID
    fingerprint: str
    seen_count: int
    first_ip: str | None
    last_ip: str | None
    ip_history: list[dict[str, Any]] = field(default_factory=list)
    unique_ip_count: int = 1

    first_seen: datetime | None = None
    last_seen: datetime | None = None

    current_ip: str | None = None
    current_ip_data: dict[str, Any] = field(default_factory=dict)
    current_user_agent: str | None = None
    current_headers: dict[str, Any] = field(default_factory=dict)
    current_port: int | None = None

    geo: dict[str, Any] = field(default_factory=dict)
    asn: str | None = None
    org: str | None = None

    is_first: bool = True
    additional_data: dict[str, Any] = field(default_factory=dict)