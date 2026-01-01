"""
Treatment service for managing treatment plans.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.repositories.treatment_repository import TreatmentRepository
from backend.utils.logger import get_logger
from validation import InputValidator

logger = get_logger(__name__)


class TreatmentService:
    """Service for treatment plan operations"""

    def __init__(self, session: Session):
        """
        Initialize treatment service.

        Args:
            session: Database session
        """
        self.session = session
        self.treatment_repo = TreatmentRepository(session)

    def create_plan(self, user_id: int, title: str, condition: str, plan_details: str) -> Dict:
        """
        Create a treatment plan.

        Args:
            user_id: User ID
            title: Plan title
            condition: Medical condition
            plan_details: Detailed plan content

        Returns:
            Dictionary with plan information

        Raises:
            ValidationError: If validation fails
        """
        try:
            # Validate inputs
            condition = InputValidator.validate_condition(condition)

            # Create plan
            plan = self.treatment_repo.create_plan(
                user_id=user_id, title=title, condition=condition, plan_details=plan_details
            )

            logger.info(f"Created treatment plan for user_id={user_id}")

            return {
                "id": plan.id,
                "title": plan.title,
                "condition": plan.condition,
                "plan_details": plan.plan_details,
                "created_at": plan.created_at,
            }

        except Exception as e:
            logger.error(f"Error creating treatment plan: {str(e)}")
            raise

    def get_user_plans(self, user_id: int) -> List[Dict]:
        """
        Get all treatment plans for a user.

        Args:
            user_id: User ID

        Returns:
            List of treatment plans
        """
        plans = self.treatment_repo.get_user_plans(user_id)

        return [
            {
                "id": p.id,
                "title": p.title,
                "condition": p.condition,
                "plan_details": p.plan_details,
                "created_at": p.created_at,
            }
            for p in plans
        ]

    def get_plan_by_id(self, user_id: int, plan_id: int) -> Optional[Dict]:
        """
        Get a specific treatment plan.

        Args:
            user_id: User ID
            plan_id: Plan ID

        Returns:
            Dictionary with plan or None
        """
        plan = self.treatment_repo.get_by_id(plan_id)

        # Verify ownership
        if not plan or plan.user_id != user_id:
            return None

        return {
            "id": plan.id,
            "title": plan.title,
            "condition": plan.condition,
            "plan_details": plan.plan_details,
            "created_at": plan.created_at,
        }

    def get_plans_by_condition(self, user_id: int, condition: str) -> List[Dict]:
        """
        Get treatment plans for a specific condition.

        Args:
            user_id: User ID
            condition: Medical condition

        Returns:
            List of treatment plans
        """
        plans = self.treatment_repo.get_plans_by_condition(user_id, condition)

        return [
            {
                "id": p.id,
                "title": p.title,
                "condition": p.condition,
                "plan_details": p.plan_details,
                "created_at": p.created_at,
            }
            for p in plans
        ]

    def delete_plan(self, user_id: int, plan_id: int) -> bool:
        """
        Delete a treatment plan.

        Args:
            user_id: User ID
            plan_id: Plan ID

        Returns:
            True if deleted, False otherwise
        """
        deleted = self.treatment_repo.delete_plan(plan_id, user_id)

        if deleted:
            logger.info(f"Deleted treatment plan id={plan_id} for user_id={user_id}")

        return deleted
