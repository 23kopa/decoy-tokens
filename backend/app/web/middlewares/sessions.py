from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.app.core.config import settings

def setup_session_middleware(app: FastAPI) -> None:
    is_production = settings.IS_PROD

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,

        session_cookie="session_id",
        same_site="lax",
        max_age=60 * 60 * 24 * 7, # 7 дней

        https_only=is_production,
    )
