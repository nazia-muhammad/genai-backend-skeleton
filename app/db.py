from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite with FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Model imports (needed so Alembic can discover tables) ---
# If you don't import models somewhere, alembic --autogenerate may create empty migrations.

# --- Model imports (needed so Alembic can discover tables) ---
from app.tenancy_models.organization import Organization
from app.tenancy_models.membership import Membership
from app.tenancy_models.workspace import Workspace
