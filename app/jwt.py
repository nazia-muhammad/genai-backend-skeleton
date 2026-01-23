from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from .settings import settings


def create_access_token(
    subject: str,
    expires_minutes: int | None = None,
) -> str:
    expire_minutes = expires_minutes or settings.JWT_EXPIRES_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> str:
    """
    Returns subject (sub) if valid. Raises ValueError if invalid/expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        sub = payload.get("sub")
        if not sub:
            raise ValueError("Token missing subject")
        return sub
    except JWTError as e:
        raise ValueError("Invalid token") from e

