from redis.asyncio import Redis

from backend.app.application.ports.services.rate_limiter import RateLimiterPort


class RedisRateLimiter(RateLimiterPort):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def hit(self, key: str, limit: int, window_seconds: int) -> bool:
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, window_seconds)
        return current <= limit