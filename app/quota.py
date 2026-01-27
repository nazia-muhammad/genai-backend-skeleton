from datetime import date

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .db import get_db
from .deps import get_current_user
from .models import Quota, User

DEFAULT_DAILY_LIMIT = 50  # or read from env later


def charge_quota(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    q = (
        db.query(Quota)
        .filter(Quota.user_id == current_user.id, Quota.day == today)
        .first()
    )

    if q is None:
        q = Quota(user_id=current_user.id, day=today, used=0, limit=DEFAULT_DAILY_LIMIT)
        db.add(q)
        db.commit()
        db.refresh(q)

    if q.used >= q.limit:
        raise HTTPException(
            status_code=429,
            detail=f"Quota exceeded ({q.used}/{q.limit}) for today.",
            headers={
                "X-Quota-Limit": str(q.limit),
                "X-Quota-Used": str(q.used),
            },
        )

    q.used += 1
    db.commit()

    return {"used": q.used, "limit": q.limit}
