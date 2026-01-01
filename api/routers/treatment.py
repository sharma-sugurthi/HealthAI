"""
Treatment plans router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.schemas.treatment import TreatmentPlanCreate, TreatmentPlanResponse
from api.dependencies import get_db, get_current_user
from backend.services.treatment_service import TreatmentService
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/plans", response_model=TreatmentPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan_data: TreatmentPlanCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a treatment plan."""
    try:
        treatment_service = TreatmentService(db)
        plan = treatment_service.create_plan(
            user_id=current_user["id"],
            title=plan_data.title,
            condition=plan_data.condition,
            plan_details=plan_data.plan_details,
        )
        return TreatmentPlanResponse(**plan)
    except Exception as e:
        logger.error(f"Error creating treatment plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create treatment plan",
        )


@router.get("/plans", response_model=List[TreatmentPlanResponse])
async def get_plans(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all treatment plans for current user."""
    try:
        treatment_service = TreatmentService(db)
        plans = treatment_service.get_user_plans(current_user["id"])
        return [TreatmentPlanResponse(**p) for p in plans]
    except Exception as e:
        logger.error(f"Error fetching treatment plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch treatment plans",
        )


@router.get("/plans/{plan_id}", response_model=TreatmentPlanResponse)
async def get_plan(
    plan_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get a specific treatment plan."""
    try:
        treatment_service = TreatmentService(db)
        plan = treatment_service.get_plan_by_id(current_user["id"], plan_id)

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Treatment plan not found"
            )

        return TreatmentPlanResponse(**plan)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching treatment plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch treatment plan",
        )


@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    plan_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete a treatment plan."""
    try:
        treatment_service = TreatmentService(db)
        deleted = treatment_service.delete_plan(current_user["id"], plan_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Treatment plan not found"
            )

        logger.info(f"Treatment plan {plan_id} deleted by user {current_user['id']}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting treatment plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete treatment plan",
        )
