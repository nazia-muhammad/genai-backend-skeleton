from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Quota(Base):
    __tablename__ = "quotas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    limit: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "day", name="uq_user_day_quota"),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    # creator (not tenant boundary)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # tenant boundary (IMPORTANT)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)

    # optional grouping within org
    workspace_id: Mapped[int | None] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=True,
        index=True,
    )

    user = relationship("User")
    org = relationship("Organization")
    workspace = relationship("Workspace")
