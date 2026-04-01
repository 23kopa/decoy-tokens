from backend.app.domain.entities.token import Token as DomainToken
from backend.app.infrastructure.database.models.token import Token as TokenModel


def to_domain(model: TokenModel) -> DomainToken:
    return DomainToken(
        id=model.id,
        slug=model.slug,
        owner_user_id=model.owner_user_id,
        type=model.type,
        name=model.name,
        notify_email=model.notify_email,
        desc=model.desc,
        payload=model.payload or {},
        is_active=model.is_active,
        trigger_url=model.trigger_url,
        created_at=model.created_at,
        expires_at=model.expires_at,
    )


def to_model(entity: DomainToken) -> TokenModel:
    model = TokenModel(
        id=entity.id,
        slug=entity.slug,
        owner_user_id=entity.owner_user_id,
        type=entity.type,
        name=entity.name,
        notify_email=entity.notify_email,
        desc=entity.desc,
        payload=entity.payload,
        is_active=entity.is_active,
        trigger_url=entity.trigger_url,
    )

    if entity.created_at is not None:
        model.created_at = entity.created_at
    if entity.expires_at is not None:
        model.expires_at = entity.expires_at

    return model