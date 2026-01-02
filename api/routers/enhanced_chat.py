"""
Enhanced Chat Router - Context-aware AI chat with medical intelligence
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.schemas.medical_history import (
    ContextualMessageRequest,
    ContextualMessageResponse,
    SymptomAnalysisRequest,
    SymptomAnalysisResponse,
    TreatmentPlanRequest,
    TreatmentPlanResponse,
)
from backend.services.enhanced_chat_service import EnhancedChatService
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/enhanced-chat", tags=["Enhanced Chat (Tier 3)"])


@router.post("/message", response_model=ContextualMessageResponse)
async def send_contextual_message(
    message_data: ContextualMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Send message with full patient context for intelligent AI response.

    **Features:**
    - Complete medical history integration
    - Emergency symptom detection
    - Allergy and medication awareness
    - Safety checks and warnings
    - Comprehensive responses (300-500 words)
    """
    try:
        service = EnhancedChatService(db)
        result = service.send_contextual_message(current_user["id"], message_data.message)

        return ContextualMessageResponse(**result)

    except Exception as e:
        logger.error(f"Enhanced chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message",
        )


@router.post("/analyze-symptoms", response_model=SymptomAnalysisResponse)
async def analyze_symptoms_contextual(
    symptom_data: SymptomAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Comprehensive symptom analysis with patient context.

    **Features:**
    - Emergency detection
    - Medical history consideration
    - Clarifying questions
    - Detailed assessment (500-700 words)
    - Safety warnings
    """
    try:
        service = EnhancedChatService(db)
        result = service.analyze_symptoms_with_context(current_user["id"], symptom_data.symptoms)

        return SymptomAnalysisResponse(**result)

    except Exception as e:
        logger.error(f"Symptom analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze symptoms",
        )


@router.post("/treatment-plan", response_model=TreatmentPlanResponse)
async def generate_personalized_treatment_plan(
    plan_request: TreatmentPlanRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate personalized treatment plan with full patient context.

    **Features:**
    - Medical history integration
    - Medication interaction awareness
    - Allergy-safe recommendations
    - Age and gender-specific guidance
    - Comprehensive plans (700-1000 words)
    """
    try:
        service = EnhancedChatService(db)
        result = service.generate_treatment_plan_with_context(
            current_user["id"], plan_request.condition
        )

        return TreatmentPlanResponse(**result)

    except Exception as e:
        logger.error(f"Treatment plan error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate treatment plan",
        )
