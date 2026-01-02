"""
Allergy Models - Track patient allergies and reactions
"""

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.models.user import Base


class Allergy(Base):
    """Patient allergies and adverse reactions"""

    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    allergen = Column(String(200), nullable=False)  # What they're allergic to
    allergen_type = Column(String(50), nullable=True)  # medication, food, environmental, other
    reaction = Column(Text, nullable=False)  # Description of reaction
    severity = Column(
        String(50), nullable=False, default="moderate"
    )  # mild, moderate, severe, life-threatening
    verified_date = Column(Date, nullable=True)  # When allergy was confirmed
    verified_by = Column(String(200), nullable=True)  # Doctor who verified
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="allergies")

    def __repr__(self) -> str:
        return f"<Allergy(user_id={self.user_id}, allergen='{self.allergen}', severity='{self.severity}')>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "allergen": self.allergen,
            "allergen_type": self.allergen_type,
            "reaction": self.reaction,
            "severity": self.severity,
            "verified_date": (self.verified_date.isoformat() if self.verified_date else None),
            "verified_by": self.verified_by,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
