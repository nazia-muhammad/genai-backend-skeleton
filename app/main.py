import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routes.notes import router as notes_router

app = FastAPI(title="GenAI Backend Skeleton")

app.include_router(notes_router)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", extra={"path": str(request.url.path)})
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
