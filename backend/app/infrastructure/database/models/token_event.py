import uuid
from datetime import datetime
from typing import Any, Optional, List, Dict

from sqlalchemy import DateTime, ForeignKey, String, Integer, Index, Boolean, Float 
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import UUID, JSONB

from backend.app.infrastructure.database.engine import Base


class TokenEvent(Base):
    __tablename__ = "token_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tokens.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # --- ОСНОВНЫЕ ПОЛЯ ---
    fingerprint: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    seen_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # --- IP ИСТОРИЯ (новые поля) ---
    first_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    ip_history: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    unique_ip_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # --- ВРЕМЕННЫЕ МЕТКИ ---
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # --- ТЕКУЩИЕ ДАННЫЕ ---
    current_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    current_ip_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    current_user_agent: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    current_headers: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    current_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # --- ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ ---
    geo: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    asn: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    org: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # --- Дополнительные данные ---
    is_first: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    additional_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    __table_args__ = (
        Index("ix_token_events_token_fingerprint", "token_id", "fingerprint"),
        Index("ix_token_events_token_last_seen", "token_id", "last_seen"),
        Index("ix_token_events_fingerprint", "fingerprint"),
        Index("ix_token_events_current_ip", "current_ip"),
    )