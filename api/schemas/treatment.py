"""
Pydantic schemas for treatment plans.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TreatmentPlanCreate(BaseModel):
    """Schema for creating a treatment plan"""

    title: str = Field(..., min_length=1, max_length=200)
    condition: str = Field(..., min_length=1, max_length=200)
    plan_details: str = Field(..., min_length=10)


class TreatmentPlanResponse(BaseModel):
    """Schema for treatment plan response"""

    id: int
    title: str
    condition: str
    plan_details: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
