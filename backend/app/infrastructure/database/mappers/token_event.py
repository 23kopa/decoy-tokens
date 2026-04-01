from backend.app.domain.entities.token_event import TokenEvent as DomainTokenEvent
from backend.app.infrastructure.database.models.token_event import TokenEvent as TokenEventModel


def to_domain(model: TokenEventModel) -> DomainTokenEvent:
    return DomainTokenEvent(
        id=model.id,
        token_id=model.token_id,
        fingerprint=model.fingerprint,
        seen_count=model.seen_count,
        first_ip=model.first_ip,
        last_ip=model.last_ip,
        ip_history=model.ip_history or [],
        unique_ip_count=model.unique_ip_count,
        first_seen=model.first_seen,
        last_seen=model.last_seen,
        current_ip=model.current_ip,
        current_ip_data=model.current_ip_data or {},
        current_user_agent=model.current_user_agent,
        current_headers=model.current_headers or {},
        current_port=model.current_port,
        geo=model.geo or {},
        asn=model.asn,
        org=model.org,
        is_first=model.is_first,
        additional_data=model.additional_data or {},
    )


def to_model(entity: DomainTokenEvent) -> TokenEventModel:
    model = TokenEventModel(
        token_id=entity.token_id,
        fingerprint=entity.fingerprint,
        seen_count=entity.seen_count,
        first_ip=entity.first_ip,
        last_ip=entity.last_ip,
        ip_history=entity.ip_history,
        unique_ip_count=entity.unique_ip_count,
        current_ip=entity.current_ip,
        current_ip_data=entity.current_ip_data,
        current_user_agent=entity.current_user_agent,
        current_headers=entity.current_headers,
        current_port=entity.current_port,
        geo=entity.geo,
        asn=entity.asn,
        org=entity.org,
        is_first=entity.is_first,
        additional_data=entity.additional_data,
    )

    if entity.id is not None:
        model.id = entity.id
    if entity.first_seen is not None:
        model.first_seen = entity.first_seen
    if entity.last_seen is not None:
        model.last_seen = entity.last_seen

    return model