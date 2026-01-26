API_PREFIX = "/api/v1"

def api(path: str) -> str:
    return f"{API_PREFIX}{path}"
