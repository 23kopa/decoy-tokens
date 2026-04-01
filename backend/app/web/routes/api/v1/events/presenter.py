from __future__ import annotations

from typing import Iterable

from backend.app.domain.entities.token_event import TokenEvent

from backend.app.web.routes.api.v1.events.schemas import EventResponse

from backend.app.web.presenters.events.behavior_presenter import build_behavior_summary
from backend.app.web.presenters.events.client_presenter import build_client_summary
from backend.app.web.presenters.events.headers_presenter import build_headers_summary
from backend.app.web.presenters.events.network_presenter import build_network_summary
from backend.app.web.presenters.events.timeline_presenter import build_timeline_summary
from backend.app.web.presenters.events.history_presenter import (build_history_summary, build_ip_history)


def build_event_response(event: TokenEvent) -> EventResponse:
    headers = event.current_headers or {}
    ip_data = event.current_ip_data or {}
    geo = event.geo or {}
    additional_data = event.additional_data or {}

    ip_history = build_ip_history(event.ip_history)

    payload = {
        "id": event.id,
        "token_id": event.token_id,
        "fingerprint": event.fingerprint,
        **build_client_summary(headers),
        **build_headers_summary(
            current_user_agent=event.current_user_agent,
            current_headers=headers,
        ),
        **build_network_summary(
            current_ip=event.current_ip,
            current_ip_data=ip_data,
            current_port=event.current_port,
            geo=geo,
            org=event.org,
            asn=event.asn,
        ),
        **build_timeline_summary(
            first_seen=event.first_seen,
            last_seen=event.last_seen,
            seen_count=event.seen_count,
            is_first=event.is_first,
        ),
        **build_behavior_summary(
            headers=headers,
            is_first=event.is_first,
            additional_data=additional_data,
            seen_count=event.seen_count,
        ),
        **build_history_summary(
            first_ip=event.first_ip,
            last_ip=event.last_ip,
            unique_ip_count=event.unique_ip_count,
            ip_history=ip_history,
        ),
        "additional_data": additional_data,
    }

    return EventResponse(**payload)


def build_event_responses(events: Iterable[TokenEvent]) -> list[EventResponse]:
    return [build_event_response(event) for event in events]