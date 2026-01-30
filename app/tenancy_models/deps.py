from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.tenancy_models.membership import Membership


def get_current_org_id(x_org_id: str | None = Header(None, alias="X-Org-Id")) -> str | None:
    return x_org_id


def require_membership(
    org_id: str | None = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> Membership:
    # If org header provided, enforce that org membership
    if org_id is not None:
        membership = (
            db.query(Membership)
            .filter(Membership.org_id == org_id, Membership.user_id == current_user.id)
            .first()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Not a member of this organization")
        return membership

    # If header missing, auto-pick ONLY if user has exactly one org
    memberships = (
        db.query(Membership)
        .filter(Membership.user_id == current_user.id)
        .all()
    )
    if not memberships:
        raise HTTPException(status_code=403, detail="No organization membership found")

    if len(memberships) > 1:
        raise HTTPException(status_code=400, detail="X-Org-Id header required (multiple orgs)")

    return memberships[0]
