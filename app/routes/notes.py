from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..errors import not_found
from ..models import Note
from ..schemas import NoteCreate, NoteOut
from ..deps import get_current_user
from ..models import User

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=NoteOut)
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=list[NoteOut])
def list_notes(
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return (
        db.query(Note)
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
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
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
def update_note(note_id: int, payload: NoteCreate, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
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
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if note is None:
        raise not_found("Note not found")

    db.delete(note)
    db.commit()
    return {"deleted": True, "id": note_id}

