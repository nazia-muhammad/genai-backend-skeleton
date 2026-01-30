from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("org_id", "name", name="uq_workspaces_org_name"),)

    org = relationship("Organization", back_populates="workspaces")
