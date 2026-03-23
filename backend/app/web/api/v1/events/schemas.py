# backend/app/web/api/v1/events/schemas.py

from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

class EventIpHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ip: Optional[str]
    timestamp: str

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    token_id: uuid.UUID
    
    fingerprint: str
    seen_count: int

    first_seen: datetime
    last_seen: datetime

    first_ip: Optional[str] = None
    last_ip: Optional[str] = None

    ip_history: List[EventIpHistoryItem] = []
    unique_ip_count: int = 0

    current_ip: Optional[str] = None
    current_ip_data: Dict[str, Any] = {}
    current_user_agent: Optional[str] = None
    current_headers: Dict[str, Any] = {} 
    current_port: Optional[int] = None

    geo: Dict[str, Any]
    asn: Optional[str]
    org: Optional[str]

    is_first: bool
    additional_data: Dict[str, Any] = {}
    