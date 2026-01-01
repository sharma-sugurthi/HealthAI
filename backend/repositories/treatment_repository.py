"""
Treatment repository for treatment plan operations.
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.treatment import TreatmentPlan
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class TreatmentRepository(BaseRepository[TreatmentPlan]):
    """Repository for TreatmentPlan model operations"""

    def __init__(self, session: Session):
        super().__init__(TreatmentPlan, session)

    def create_plan(
        self, user_id: int, title: str, condition: str, plan_details: str
    ) -> TreatmentPlan:
        """
        Create a new treatment plan.

        Args:
            user_id: User ID
            title: Plan title
            condition: Medical condition
            plan_details: Detailed plan content

        Returns:
            Created TreatmentPlan instance
        """
        try:
            plan = TreatmentPlan(
                user_id=user_id, title=title, condition=condition, plan_details=plan_details
            )
            self.session.add(plan)
            self.session.commit()
            self.session.refresh(plan)

            logger.info(f"Created treatment plan for user_id={user_id}, condition={condition}")
            return plan

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating treatment plan: {str(e)}")
            raise

    def get_user_plans(self, user_id: int) -> List[TreatmentPlan]:
        """
        Get all treatment plans for a user.

        Args:
            user_id: User ID

        Returns:
            List of TreatmentPlan instances, ordered by created_at descending
        """
        return (
            self.session.query(TreatmentPlan)
            .filter(TreatmentPlan.user_id == user_id)
            .order_by(desc(TreatmentPlan.created_at))
            .all()
        )

    def get_plans_by_condition(self, user_id: int, condition: str) -> List[TreatmentPlan]:
        """
        Get treatment plans for a specific condition.

        Args:
            user_id: User ID
            condition: Medical condition

        Returns:
            List of TreatmentPlan instances
        """
        return (
            self.session.query(TreatmentPlan)
            .filter(
                TreatmentPlan.user_id == user_id, TreatmentPlan.condition.ilike(f"%{condition}%")
            )
            .order_by(desc(TreatmentPlan.created_at))
            .all()
        )

    def delete_plan(self, plan_id: int, user_id: int) -> bool:
        """
        Delete a treatment plan (with user ownership check).

        Args:
            plan_id: Plan ID
            user_id: User ID (for ownership verification)

        Returns:
            True if deleted, False if not found or not owned by user
        """
        try:
            plan = (
                self.session.query(TreatmentPlan)
                .filter(TreatmentPlan.id == plan_id, TreatmentPlan.user_id == user_id)
                .first()
            )

            if plan:
                self.session.delete(plan)
                self.session.commit()
                logger.info(f"Deleted treatment plan id={plan_id}")
                return True

            return False

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting treatment plan: {str(e)}")
            raise
