import time
from typing import Callable, Tuple, TypeVar

T = TypeVar("T")

DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_BASE_S = 0.3


def retry_with_backoff(
    fn: Callable[[], T],
    retries: int = DEFAULT_MAX_RETRIES,
    backoff_base_s: float = DEFAULT_BACKOFF_BASE_S,
    retry_on: Tuple[type[Exception], ...] = (Exception,),
) -> T:
    """
    Generic retry helper (prep for external calls later: LLM, HTTP, etc.)
    Exponential backoff: base * 2^attempt
    """
    last_err: Exception | None = None

    for attempt in range(retries + 1):
        try:
            return fn()
        except retry_on as e:
            last_err = e
            if attempt == retries:
                raise
            time.sleep(backoff_base_s * (2**attempt))

    raise last_err if last_err else RuntimeError("retry_with_backoff failed")
