from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..tenancy_models.membership import Membership
from ..tenancy_models.deps import require_membership, get_current_org_id
from ..tenancy_models.rbac import require_min_role

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("")
def list_memberships(
    db: Session = Depends(get_db),
    membership=Depends(require_membership),  # MEMBER+ (any member can list)
):
    rows = (
        db.query(Membership)
        .filter(Membership.org_id == membership.org_id)
        .order_by(Membership.id.desc())
        .all()
    )
    return rows


@router.post("")
def add_member(
    user_id: int,
    role: str = "MEMBER",
    db: Session = Depends(get_db),
    membership=Depends(require_min_role("ADMIN")),  # ADMIN+
):
    # prevent duplicates
    exists = (
        db.query(Membership)
        .filter(Membership.org_id == membership.org_id, Membership.user_id == user_id)
        .first()
    )
    if exists:
        raise HTTPException(status_code=409, detail="User already a member")

    m = Membership(org_id=membership.org_id, user_id=user_id, role=role)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.put("/{membership_id}")
def change_role(
    membership_id: int,
    role: str,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id),
    _actor=Depends(require_min_role("OWNER")),  # OWNER only
):
    m = (
        db.query(Membership)
        .filter(Membership.id == membership_id, Membership.org_id == org_id)
        .first()
    )
    if not m:
        raise HTTPException(status_code=404, detail="Membership not found")

    m.role = role
    db.commit()
    db.refresh(m)
    return m
