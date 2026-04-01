from fastapi import FastAPI

from backend.app.core.config import settings
from backend.app.web.middlewares.sessions import setup_session_middleware
from backend.app.web.middlewares.csrf import (
    CSRFCookieInitMiddleware,
    CSRFMiddleware,
)
from backend.app.web.middlewares.test_headers import TestHeadersMiddleware


def setup_middlewares(app: FastAPI) -> None:
    setup_session_middleware(app)

    app.add_middleware(CSRFCookieInitMiddleware)

    app.add_middleware(
        CSRFMiddleware,
        exempt_paths={
            "/auth/login",
            "/auth/register",
        },
    )

    if settings.IS_DEV:
        app.add_middleware(TestHeadersMiddleware)