from fastapi import Depends, HTTPException

from app.tenancy_models.deps import require_membership

ROLE_ORDER = {"MEMBER": 1, "ADMIN": 2, "OWNER": 3}

def require_min_role(min_role: str):
    def _dep(membership=Depends(require_membership)):
        role = membership.role or "MEMBER"
        if ROLE_ORDER.get(role, 0) < ROLE_ORDER[min_role]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return membership
    return _dep
