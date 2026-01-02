"""
Pydantic schemas for medical history API
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# Medical Condition Schemas
class MedicalConditionCreate(BaseModel):
    """Schema for creating a medical condition"""

    condition_name: str = Field(..., min_length=1, max_length=200)
    diagnosed_date: Optional[date] = None
    status: str = Field(default="active", pattern="^(active|resolved|chronic|managed)$")
    severity: Optional[str] = Field(None, pattern="^(mild|moderate|severe)$")
    notes: Optional[str] = None


class MedicalConditionResponse(BaseModel):
    """Schema for medical condition response"""

    id: int
    user_id: int
    condition_name: str
    diagnosed_date: Optional[str]
    status: str
    severity: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Medication Schemas
class MedicationCreate(BaseModel):
    """Schema for creating a medication"""

    medication_name: str = Field(..., min_length=1, max_length=200)
    dosage: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)
    route: Optional[str] = Field(None, max_length=50)
    start_date: Optional[date] = None
    reason: Optional[str] = None
    prescribing_doctor: Optional[str] = Field(None, max_length=200)


class MedicationResponse(BaseModel):
    """Schema for medication response"""

    id: int
    user_id: int
    medication_name: str
    dosage: Optional[str]
    frequency: Optional[str]
    route: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    status: str
    reason: Optional[str]
    prescribing_doctor: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Allergy Schemas
class AllergyCreate(BaseModel):
    """Schema for creating an allergy"""

    allergen: str = Field(..., min_length=1, max_length=200)
    allergen_type: Optional[str] = Field(None, pattern="^(medication|food|environmental|other)$")
    reaction: str = Field(..., min_length=1)
    severity: str = Field(
        default="moderate",
        pattern="^(mild|moderate|severe|life-threatening)$",
    )
    verified_date: Optional[date] = None
    verified_by: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None


class AllergyResponse(BaseModel):
    """Schema for allergy response"""

    id: int
    user_id: int
    allergen: str
    allergen_type: Optional[str]
    reaction: str
    severity: str
    verified_date: Optional[str]
    verified_by: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Symptom Log Schemas
class SymptomLogCreate(BaseModel):
    """Schema for creating a symptom log"""

    symptom_description: str = Field(..., min_length=1)
    body_part: Optional[str] = Field(None, max_length=100)
    severity: Optional[int] = Field(None, ge=1, le=10)
    onset_date: Optional[datetime] = None
    duration: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)
    quality: Optional[str] = Field(None, max_length=200)
    associated_symptoms: Optional[str] = None
    triggers: Optional[str] = None
    relieving_factors: Optional[str] = None
    aggravating_factors: Optional[str] = None
    impact_on_life: Optional[str] = Field(None, pattern="^(none|mild|moderate|severe)$")
    notes: Optional[str] = None


class SymptomLogResponse(BaseModel):
    """Schema for symptom log response"""

    id: int
    user_id: int
    symptom_description: str
    body_part: Optional[str]
    severity: Optional[int]
    onset_date: Optional[str]
    duration: Optional[str]
    frequency: Optional[str]
    quality: Optional[str]
    associated_symptoms: Optional[str]
    triggers: Optional[str]
    relieving_factors: Optional[str]
    aggravating_factors: Optional[str]
    impact_on_life: Optional[str]
    notes: Optional[str]
    logged_at: str

    class Config:
        from_attributes = True


# Enhanced Chat Schemas
class ContextualMessageRequest(BaseModel):
    """Schema for contextual chat message"""

    message: str = Field(..., min_length=1, max_length=2000)


class ContextualMessageResponse(BaseModel):
    """Schema for contextual chat response"""

    message: str
    response: str
    safety_flags: list[str]
    has_emergency: bool
    context_used: bool
    severity: str


class SymptomAnalysisRequest(BaseModel):
    """Schema for symptom analysis request"""

    symptoms: str = Field(..., min_length=10, max_length=2000)


class SymptomAnalysisResponse(BaseModel):
    """Schema for symptom analysis response"""

    symptoms: str
    analysis: str
    safety_flags: list[str]
    has_emergency: bool


class TreatmentPlanRequest(BaseModel):
    """Schema for treatment plan request"""

    condition: str = Field(..., min_length=1, max_length=200)


class TreatmentPlanResponse(BaseModel):
    """Schema for treatment plan response"""

    condition: str
    treatment_plan: str
    safety_flags: list[str]
    personalized: bool
