"""
Pydantic schemas for chat-related requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""

    message: str = Field(..., min_length=1, max_length=5000)


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""

    id: int
    message: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True


class SymptomAnalysisRequest(BaseModel):
    """Schema for symptom analysis request"""

    symptoms: str = Field(..., min_length=10, max_length=5000)


class SymptomAnalysisResponse(BaseModel):
    """Schema for symptom analysis response"""

    id: int
    symptoms: str
    analysis: str
    timestamp: datetime


class TreatmentPlanRequest(BaseModel):
    """Schema for treatment plan generation request"""

    condition: str = Field(..., min_length=3, max_length=200)


class TreatmentPlanGenerationResponse(BaseModel):
    """Schema for treatment plan generation response"""

    condition: str
    plan: str
