from fastapi import Depends
from sqlalchemy.orm import Session

from .db import get_db
from .errors import unauthorized, not_found
from .jwt import decode_access_token
from .models import User
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer(auto_error=False)


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not credentials.credentials
    ):
        raise unauthorized("Missing bearer token")
    return credentials.credentials


def get_current_user(
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db),
) -> User:
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise unauthorized("Invalid or expired token")

    user = db.get(User, int(user_id))
    if user is None:
        raise not_found("User not found")

    return user
