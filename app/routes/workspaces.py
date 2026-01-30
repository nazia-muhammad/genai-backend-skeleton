from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..tenancy_models.deps import require_membership
from ..tenancy_models.rbac import require_min_role
from ..tenancy_models.workspace import Workspace

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("")
def list_workspaces(
    db: Session = Depends(get_db),
    membership=Depends(require_membership),  # requires X-Org-Id + membership
):
    rows = (
        db.query(Workspace)
        .filter(Workspace.org_id == membership.org_id)
        .order_by(Workspace.id.desc())
        .all()
    )
    return rows


@router.post("")
def create_workspace(
    name: str,
    db: Session = Depends(get_db),
    membership=Depends(require_min_role("ADMIN")),  # ADMIN+ only
):
    ws = Workspace(org_id=membership.org_id, name=name)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return ws
