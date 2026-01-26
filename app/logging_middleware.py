import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger("app.request")


async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Request-ID"] = request_id

    logger.info(
    f'{request.method} {request.url.path} -> {response.status_code} '
    f'duration_ms={duration_ms:.2f} request_id={request_id}'
)
    return response
