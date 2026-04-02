from fastapi import FastAPI

from backend.app.core.config import settings

from .sessions import setup_session_middleware
from .csrf import CSRFCookieInitMiddleware, CSRFMiddleware
from .rate_limit import RateLimitMiddleware
from .test_headers import TestHeadersMiddleware


def setup_middlewares(app: FastAPI) -> None:
    setup_session_middleware(app)

    app.add_middleware(RateLimitMiddleware)

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