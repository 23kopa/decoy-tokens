from typing import Protocol


class RateLimiterPort(Protocol):
    async def hit(self, key: str, limit: int, window_seconds: int) -> bool:
        ...