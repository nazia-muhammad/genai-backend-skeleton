from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Backend Skeleton")


# ---------- Models (what a Note looks like) ----------
class NoteCreate(BaseModel):
    text: str


class Note(BaseModel):
    id: str
    text: str


# ---------- Temporary storage (in-memory) ----------
NOTES: List[Note] = []


# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notes", response_model=Note)
def create_note(payload: NoteCreate):
    note = Note(id=str(uuid4()), text=payload.text)
    NOTES.append(note)
    return note


@app.get("/notes", response_model=List[Note])
def list_notes():
    return NOTES


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    for note in NOTES:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    for i, note in enumerate(NOTES):
        if note.id == note_id:
            NOTES.pop(i)
            return {"deleted": True, "id": note_id}
    raise HTTPException(status_code=404, detail="Note not found")
