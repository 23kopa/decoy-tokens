from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from backend.app.core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
