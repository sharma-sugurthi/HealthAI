"""
Treatment plan model for storing user treatment plans.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from .user import Base


class TreatmentPlan(Base):
    """Treatment plan model for storing personalized health plans"""

    __tablename__ = "treatment_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    condition = Column(String(200), nullable=False, index=True)
    plan_details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="treatment_plans")

    # Indexes for performance
    __table_args__ = (Index("idx_user_created", "user_id", "created_at"),)

    def __repr__(self) -> str:
        return f"<TreatmentPlan(id={self.id}, title='{self.title}', condition='{self.condition}')>"
