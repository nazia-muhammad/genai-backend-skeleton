from uuid import uuid4
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    memberships = relationship("Membership", back_populates="org", cascade="all, delete-orphan")
    workspaces = relationship("Workspace", back_populates="org", cascade="all, delete-orphan")
