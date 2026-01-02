"""
Medication Models - Track current and past medications
"""

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.models.user import Base


class Medication(Base):
    """Patient's current and past medications"""

    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    medication_name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=True)  # e.g., "500mg", "10ml"
    frequency = Column(String(100), nullable=True)  # e.g., "twice daily", "as needed"
    route = Column(String(50), nullable=True)  # oral, topical, injection, etc.
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="active")  # active, discontinued, completed
    reason = Column(Text, nullable=True)  # Reason for medication
    prescribing_doctor = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="medications")

    def __repr__(self) -> str:
        return f"<Medication(user_id={self.user_id}, medication='{self.medication_name}', status='{self.status}')>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "route": self.route,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "reason": self.reason,
            "prescribing_doctor": self.prescribing_doctor,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
