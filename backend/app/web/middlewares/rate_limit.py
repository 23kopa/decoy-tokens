from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from backend.app.infrastructure.redis.client import redis_client
from backend.app.infrastructure.redis.rate_limiter import RedisRateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.limiter = RedisRateLimiter(redis_client)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method
        ip = request.client.host if request.client else "unknown"
        user_id = request.session.get("user_id") if "session" in request.scope else None

        if path.startswith("/static/") or path.startswith("/media/"):
            return await call_next(request)
        elif path == "/health":
            return await call_next(request)

        subject = f"user:{user_id}" if user_id else f"ip:{ip}"

        limit = None
        window = None
        rate_path = path

        if path == "/auth/login" and method == "POST":
            limit, window = 5, 60
            rate_path = "/auth/login"
        elif path == "/auth/register" and method == "POST":
            limit, window = 3, 60
            rate_path = "/auth/register"
        elif path == "/api/v1/tokens" and method == "POST":
            limit, window = 10, 60
            rate_path = "/api/v1/tokens"
        elif path.startswith("/api/v1/tokens/") and path.endswith("/status") and method == "PATCH":
            limit, window = 30, 60
            rate_path = "/api/v1/tokens/:id/status"
        elif path.startswith("/t/") and method == "GET":
            limit, window = 60, 60
            rate_path = "/t/:slug"

        if limit is not None and window is not None:
            key = f"rate_limit:{method}:{rate_path}:{subject}"
            allowed = await self.limiter.hit(key, limit, window)
            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"},
                )

        return await call_next(request)