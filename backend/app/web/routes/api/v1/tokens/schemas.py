import uuid
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr


class TokenCreateIn(BaseModel):
    """Схема запроса на создание токена"""
    type: str = Field(..., description="link|email|file|dns|image|word|...")
    name: str = Field(..., min_length=1, max_length=255, description="Название токена")
    notify_email: EmailStr
    desc: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)


class TokenCreateOut(BaseModel):
    """Схема ответа после создания токена"""
    id: uuid.UUID
    type: str
    name: str
    desc: Optional[str]
    trigger_url: str


class TokenResponse(BaseModel):
    """Схема для получения токена"""
    id: uuid.UUID
    type: str
    name: str
    desc: Optional[str]
    created_at: str
    is_active: bool
    trigger_url: str


class TokenStatsOut(BaseModel):
    """Схема статистики токена"""
    total_hits: int
    unique_ips: int
    first_seen: Optional[str]
    last_seen: Optional[str]
    bot_count: int


class TokenEventOut(BaseModel):
    """Схема события токена"""
    id: int
    timestamp: str
    ip: str
    user_agent: str
    is_bot: bool
    bot_type: Optional[str]

class TokenStatusUpdateRequest(BaseModel):
    is_active: bool