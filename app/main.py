import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routes.notes import router as notes_router
from .routes.users import router as users_router
from .routes.auth import router as auth_router

from .logging_middleware import add_request_id

from .error_schemas import ErrorResponse
from fastapi.middleware.cors import CORSMiddleware
from .rate_limit_middleware import rate_limit_middleware
API_PREFIX = "/api/v1"


app = FastAPI(title="GenAI Backend Skeleton")
app.middleware("http")(add_request_id)
app.middleware("http")(rate_limit_middleware)

app.include_router(notes_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev-friendly for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "GenAI Backend Skeleton is running",
        "health": "/health",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)

    logger.exception(
        "Unhandled exception",
        extra={
            "path": str(request.url.path),
            "request_id": request_id,
        },
    )

    body = ErrorResponse(
        detail="Internal server error", request_id=request_id
    ).model_dump()
    return JSONResponse(status_code=500, content=body)
