from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..errors import not_found
from ..models import Note
from ..schemas import NoteCreate, NoteOut
from ..quota import charge_quota
from ..deps import get_current_user
from ..models import User
from ..tenancy_models.deps import require_membership

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteOut)
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_membership),   # ✅ requires X-Org-Id + checks user is member
    _quota=Depends(charge_quota),
):
    note = Note(
        title=payload.title,
        content=payload.content,
        user_id=current_user.id,              # creator
        org_id=membership.org_id,             # ✅ tenant boundary
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=list[NoteOut])
def list_notes(
    membership=Depends(require_membership),   # ✅ requires X-Org-Id + checks membership
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return (
        db.query(Note)
        .filter(Note.org_id == membership.org_id)   # ✅ org-scoped
        .order_by(Note.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    responses={
        404: {
            "description": "Note not found",
            "content": {"application/json": {"example": {"detail": "Note not found"}}},
        }
    },
)
def get_note(
    note_id: int,
    membership=Depends(require_membership),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.org_id == membership.org_id)
        .first()
    )
    if note is None:
        raise not_found("Note not found")
    return note


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    responses={
        404: {
            "description": "Note not found",
            "content": {"application/json": {"example": {"detail": "Note not found"}}},
        }
    },
)
def update_note(
    note_id: int,
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership=Depends(require_membership),
    _quota=Depends(charge_quota),
):
    note = (
        db.query(Note)
       .filter(Note.id == note_id, Note.org_id == membership.org_id)
        .first()
    )
    if note is None:
        raise not_found("Note not found")

    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note


@router.delete(
    "/{note_id}",
    responses={
        404: {
            "description": "Note not found",
            "content": {"application/json": {"example": {"detail": "Note not found"}}},
        }
    },
)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership=Depends(require_membership),
    _quota=Depends(charge_quota),
):
    note = (
        db.query(Note)
       .filter(Note.id == note_id, Note.org_id == membership.org_id)
        .first()
    )
    if note is None:
        raise not_found("Note not found")

    db.delete(note)
    db.commit()
    return {"deleted": True, "id": note_id}

