from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteOut(NoteCreate):
    id: int


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
