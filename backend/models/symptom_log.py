"""
Symptom Log Models - Detailed symptom tracking over time
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.models.user import Base


class SymptomLog(Base):
    """Detailed symptom tracking for pattern analysis"""

    __tablename__ = "symptom_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symptom_description = Column(Text, nullable=False)
    body_part = Column(String(100), nullable=True)  # Location of symptom
    severity = Column(Integer, nullable=True)  # 1-10 scale
    onset_date = Column(DateTime, nullable=True)  # When symptom started
    duration = Column(String(100), nullable=True)  # How long it's lasted
    frequency = Column(String(100), nullable=True)  # constant, intermittent, occasional
    quality = Column(String(200), nullable=True)  # sharp, dull, throbbing, burning, etc.
    associated_symptoms = Column(Text, nullable=True)  # Other symptoms occurring
    triggers = Column(Text, nullable=True)  # What seems to cause it
    relieving_factors = Column(Text, nullable=True)  # What makes it better
    aggravating_factors = Column(Text, nullable=True)  # What makes it worse
    impact_on_life = Column(String(50), nullable=True)  # none, mild, moderate, severe
    notes = Column(Text, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="symptom_logs")

    def __repr__(self) -> str:
        return f"<SymptomLog(user_id={self.user_id}, symptom='{self.symptom_description[:50]}...', severity={self.severity})>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "symptom_description": self.symptom_description,
            "body_part": self.body_part,
            "severity": self.severity,
            "onset_date": self.onset_date.isoformat() if self.onset_date else None,
            "duration": self.duration,
            "frequency": self.frequency,
            "quality": self.quality,
            "associated_symptoms": self.associated_symptoms,
            "triggers": self.triggers,
            "relieving_factors": self.relieving_factors,
            "aggravating_factors": self.aggravating_factors,
            "impact_on_life": self.impact_on_life,
            "notes": self.notes,
            "logged_at": self.logged_at.isoformat() if self.logged_at else None,
        }
