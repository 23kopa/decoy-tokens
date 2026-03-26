from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any


class EventIpHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ip: Optional[str]
    timestamp: str

    geo: Dict[str, Any] = {}
    asn: Optional[str] = None
    org: Optional[str] = None
    connection_type: Optional[str] = None

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    token_id: uuid.UUID
    fingerprint: str

    seen_count: int
    is_first: bool
    is_repeat: bool = False

    first_seen: datetime
    last_seen: datetime

    first_ip: Optional[str] = None
    last_ip: Optional[str] = None
    ip_history: List[EventIpHistoryItem] = []
    unique_ip_count: int = 0
    has_ip_changes: bool = False

    current_ip: Optional[str] = None
    current_ip_data: Dict[str, Any] = {}
    current_port: Optional[int] = None

    current_user_agent: Optional[str] = None
    current_headers: Dict[str, Any] = {}

    current_browser: str | None = None
    current_device: str | None = None
    current_os: str | None = None
    current_language: str | None = None

    geo: Dict[str, Any] = {}
    asn: Optional[str] = None
    org: Optional[str] = None

    location_label: str | None = None
    provider_label: str | None = None
    connection_type_label: str | None = None
    coordinates_label: str | None = None
    ip_version_label: str | None = None

    visit_kind_label: str | None = None
    event_status_label: str | None = None

    accept_header: str | None = None
    accept_language_header: str | None = None
    accept_encoding_header: str | None = None
    referer_header: str | None = None
    origin_header: str | None = None
    fetch_site_header: str | None = None
    fetch_mode_header: str | None = None
    fetch_dest_header: str | None = None

    additional_data: Dict[str, Any] = {}