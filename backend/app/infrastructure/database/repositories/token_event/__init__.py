from sqlalchemy.orm import Session

from .crud import TokenEventCrudMixin
from .stats import TokenEventStatsMixin
from .update import TokenEventUpdateMixin


class TokenEventRepository(
    TokenEventCrudMixin,
    TokenEventStatsMixin,
    TokenEventUpdateMixin,
):
    def __init__(self, session: Session):
        self.session = session