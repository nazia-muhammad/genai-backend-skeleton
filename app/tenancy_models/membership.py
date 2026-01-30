from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False, default="MEMBER")  # OWNER | ADMIN | MEMBER

    __table_args__ = (
        UniqueConstraint("org_id", "user_id", name="uq_memberships_org_user"),
    )

    org = relationship("Organization", back_populates="memberships")
    user = relationship("User")
