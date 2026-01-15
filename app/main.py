from fastapi import FastAPI

from .db import engine
from .models import Base
from .routes.notes import router as notes_router

app = FastAPI(title="GenAI Backend Skeleton")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(notes_router)


@app.get("/health")
def health():
    return {"status": "ok"}
