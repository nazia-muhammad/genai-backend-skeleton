from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import hash_password
from ..db import get_db
from ..errors import conflict
from ..models import User
from ..schemas import UserCreate, UserOut
from ..tenancy_models.organization import Organization
from ..tenancy_models.membership import Membership

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise conflict("Email already registered")

    # 1) Create user
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()  # ensures user.id exists

    # 2) Create default org
    org = Organization(name=f"{user.email}'s Org")
    db.add(org)
    db.flush()  # ensures org.id exists

    # 3) Make user OWNER of that org
    membership = Membership(user_id=user.id, org_id=org.id, role="OWNER")
    db.add(membership)

    # 4) Commit everything together
    db.commit()
    db.refresh(user)

    return UserOut(id=user.id, email=user.email)
