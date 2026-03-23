from sqlalchemy.orm import Session

from backend.app.infrastructure.database.base import BaseRepository
from backend.app.infrastructure.database.models.token_event import TokenEvent
from .crud import TokenEventCrudMixin
from .stats import TokenEventStatsMixin
from .update import TokenEventUpdateMixin


class TokenEventRepository(
    BaseRepository[TokenEvent],
    TokenEventCrudMixin,
    TokenEventStatsMixin,
    TokenEventUpdateMixin
):
    def __init__(self, session: Session):
        super().__init__(session, TokenEvent)