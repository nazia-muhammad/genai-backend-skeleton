from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import verify_password
from ..db import get_db
from ..errors import unauthorized
from ..jwt import create_access_token
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise unauthorized("Email and password required")

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise unauthorized("Invalid credentials")

    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}
