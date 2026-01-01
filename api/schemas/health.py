"""
Pydantic schemas for health metrics.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HealthMetricCreate(BaseModel):
    """Schema for creating a health metric"""

    metric_type: str = Field(..., min_length=1, max_length=50)
    value: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)


class HealthMetricResponse(BaseModel):
    """Schema for health metric response"""

    id: int
    metric_type: str
    value: float
    unit: str
    notes: Optional[str]
    recorded_at: datetime

    class Config:
        from_attributes = True


class HealthStatisticsResponse(BaseModel):
    """Schema for health statistics response"""

    metric_type: str
    count: int
    latest: float
    average: float
    minimum: float
    maximum: float
    unit: str
