"""
Health metric model for tracking user health data.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .user import Base


class HealthMetric(Base):
    """Health metric model for tracking various health measurements"""

    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    notes = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="health_metrics")

    # Indexes for performance
    __table_args__ = (
        Index("idx_user_metric_type", "user_id", "metric_type"),
        Index("idx_user_recorded", "user_id", "recorded_at"),
    )

    def __repr__(self) -> str:
        return f"<HealthMetric(id={self.id}, type='{self.metric_type}', value={self.value} {self.unit})>"
