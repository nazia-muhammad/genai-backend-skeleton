from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

# NOTE: for now these are simple defaults.
# We'll move them to env vars (Settings) later.
SECRET_KEY = "change-me-in-env"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """
    Returns subject (sub) if valid. Raises ValueError if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise ValueError("Token missing subject")
        return sub
    except JWTError as e:
        raise ValueError("Invalid token") from e

