from fastapi import FastAPI

from .routes.notes import router as notes_router

app = FastAPI(title="GenAI Backend Skeleton")



app.include_router(notes_router)


@app.get("/health")
def health():
    return {"status": "ok"}
