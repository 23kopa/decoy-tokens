from typing import Generic, TypeVar, Type, Optional, Any
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: Any) -> Optional[T]:
        return self.session.get(self.model, id)

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.flush()
        return obj
