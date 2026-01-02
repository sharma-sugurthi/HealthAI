"""
Medical History Models - Track patient medical conditions over time
"""

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.models.user import Base


class MedicalCondition(Base):
    """Patient's medical conditions and diagnoses"""

    __tablename__ = "medical_conditions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    condition_name = Column(String(200), nullable=False)
    diagnosed_date = Column(Date, nullable=True)
    status = Column(
        String(50), nullable=False, default="active"
    )  # active, resolved, chronic, managed
    severity = Column(String(50), nullable=True)  # mild, moderate, severe
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="medical_conditions")

    def __repr__(self) -> str:
        return f"<MedicalCondition(user_id={self.user_id}, condition='{self.condition_name}', status='{self.status}')>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "condition_name": self.condition_name,
            "diagnosed_date": (self.diagnosed_date.isoformat() if self.diagnosed_date else None),
            "status": self.status,
            "severity": self.severity,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
