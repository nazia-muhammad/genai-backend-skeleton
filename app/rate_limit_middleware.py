import asyncio
import time
import os
from collections import defaultdict, deque
from typing import Deque, DefaultDict, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse


class RateLimiter:
    """
    Simple in-memory fixed-window-ish limiter using timestamps.
    Limit: max_requests per window_seconds per client (IP).
    """

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: DefaultDict[str, Deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    def _get_client_ip(self, request: Request) -> str:
        # Render/Proxies often set X-Forwarded-For: "client, proxy1, proxy2"
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def allow(self, request: Request) -> Tuple[bool, str, int]:
        now = time.time()
        cutoff = now - self.window_seconds
        ip = self._get_client_ip(request)

        async with self._lock:
            q = self._hits[ip]
            # drop old timestamps
            while q and q[0] < cutoff:
                q.popleft()

            remaining = self.max_requests - len(q)
            if remaining <= 0:
                retry_after = int(q[0] + self.window_seconds - now) if q else self.window_seconds
                return False, ip, max(retry_after, 1)

            q.append(now)
            return True, ip, 0


limiter = RateLimiter(max_requests=30, window_seconds=60)


async def rate_limit_middleware(request: Request, call_next):
    # Disable rate limiting during tests (CI)
    if os.getenv("PYTEST_CURRENT_TEST"):
        return await call_next(request)

    ok, _ip, retry_after = await limiter.allow(request)
    if not ok:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(retry_after)},
        )

    return await call_next(request)
