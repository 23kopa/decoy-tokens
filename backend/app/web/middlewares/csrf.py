from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from urllib.parse import urlparse
import secrets
from fastapi.responses import JSONResponse

from backend.app.core.config import settings

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


class CSRFCookieInitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_production = settings.APP_ENV == "prod"

        csrf_token = request.cookies.get("csrf_token")
        should_set_cookie = False

        if not csrf_token:
            csrf_token = generate_csrf_token()
            should_set_cookie = True

        response = await call_next(request)

        if should_set_cookie:
            response.set_cookie(
                key="csrf_token",
                value=csrf_token,
                httponly=False,
                secure=is_production,
                samesite="lax",
                path="/",
            )

        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_paths: set[str] | None = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or set()

        parsed = urlparse(settings.PUBLIC_BASE_URL)
        self.expected_origin = f"{parsed.scheme}://{parsed.netloc}"

    async def dispatch(self, request: Request, call_next):
        if request.method in SAFE_METHODS:
            return await call_next(request)

        if request.url.path in self.exempt_paths:
            return await call_next(request)

        cookie_token = request.cookies.get("csrf_token")
        request_token = request.headers.get("X-CSRF-Token")

        if not request_token:
            content_type = request.headers.get("content-type", "")
            if (
                content_type.startswith("application/x-www-form-urlencoded")
                or content_type.startswith("multipart/form-data")
            ):
                form = await request.form()
                request_token = form.get("csrf_token")

        if not cookie_token or not request_token:
            return JSONResponse(status_code=403, content={"detail": "CSRF missing"})

        if not secrets.compare_digest(cookie_token, request_token):
            return JSONResponse(status_code=403, content={"detail": "CSRF invalid"})

        origin = request.headers.get("origin")
        if origin:
            parsed = urlparse(origin)
            if not parsed.scheme or not parsed.netloc:
                return JSONResponse(status_code=403, content={"detail": "Bad origin"})

            actual_origin = f"{parsed.scheme}://{parsed.netloc}"

            if actual_origin != self.expected_origin:
                return JSONResponse(status_code=403, content={"detail": "Bad origin"})

        return await call_next(request)