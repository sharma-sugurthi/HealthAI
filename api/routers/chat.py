"""
Chat router for AI conversations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    SymptomAnalysisRequest,
    SymptomAnalysisResponse,
    TreatmentPlanGenerationResponse,
    TreatmentPlanRequest,
)
from backend.services.chat_service import ChatService
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    message_data: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Send a chat message and get AI response.

    Args:
        message_data: Chat message
        current_user: Current authenticated user
        db: Database session

    Returns:
        Chat message with AI response
    """
    try:
        chat_service = ChatService(db)
        result = chat_service.send_message(current_user["id"], message_data.message)
        return ChatMessageResponse(**result)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process message"
        )


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    limit: int = 50, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get chat history for current user.

    Args:
        limit: Maximum number of messages
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of chat messages
    """
    try:
        chat_service = ChatService(db)
        history = chat_service.get_chat_history(current_user["id"], limit)
        return [ChatMessageResponse(**msg) for msg in history]

    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch chat history"
        )


@router.post("/symptoms", response_model=SymptomAnalysisResponse)
async def analyze_symptoms(
    symptom_data: SymptomAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Analyze symptoms using AI.

    Args:
        symptom_data: Symptom description
        current_user: Current authenticated user
        db: Database session

    Returns:
        Symptom analysis
    """
    try:
        chat_service = ChatService(db)
        result = chat_service.analyze_symptoms(current_user["id"], symptom_data.symptoms)
        return SymptomAnalysisResponse(**result)

    except Exception as e:
        logger.error(f"Symptom analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to analyze symptoms"
        )


@router.post("/treatment-plan", response_model=TreatmentPlanGenerationResponse)
async def generate_treatment_plan(
    plan_request: TreatmentPlanRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate treatment plan using AI.

    Args:
        plan_request: Treatment plan request
        current_user: Current authenticated user
        db: Database session

    Returns:
        Generated treatment plan
    """
    try:
        chat_service = ChatService(db)

        # Get user info for personalization
        from backend.services.auth_service import AuthService

        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(current_user["id"])

        patient_info = {"age": user["age"], "gender": user["gender"]}

        plan = chat_service.generate_treatment_plan(
            current_user["id"], plan_request.condition, patient_info
        )

        return TreatmentPlanGenerationResponse(condition=plan_request.condition, plan=plan)

    except Exception as e:
        logger.error(f"Treatment plan generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate treatment plan",
        )


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Clear chat history for current user.

    Args:
        current_user: Current authenticated user
        db: Database session
    """
    try:
        chat_service = ChatService(db)
        chat_service.clear_history(current_user["id"])
        logger.info(f"Chat history cleared for user {current_user['id']}")

    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to clear chat history"
        )
