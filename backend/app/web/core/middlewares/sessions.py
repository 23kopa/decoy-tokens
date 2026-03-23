from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.app.core.config import settings

def setup_session_middleware(app: FastAPI) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,
        https_only=settings.APP_ENV == "prod",
        same_site="lax",
        max_age=60 * 60 * 24 * 7, # 7 дней
    )
