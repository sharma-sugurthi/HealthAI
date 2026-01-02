"""
Medical History Repository - Manages medical conditions data
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from backend.models.medical_condition import MedicalCondition
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MedicalHistoryRepository(BaseRepository[MedicalCondition]):
    """Repository for medical conditions management"""

    def __init__(self, db: Session):
        super().__init__(MedicalCondition, db)

    def get_by_user(self, user_id: int, status: Optional[str] = None) -> List[MedicalCondition]:
        """
        Get all medical conditions for a user

        Args:
            user_id: User ID
            status: Optional status filter (active, resolved, chronic)

        Returns:
            List of medical conditions
        """
        try:
            query = self.db.query(MedicalCondition).filter(MedicalCondition.user_id == user_id)

            if status:
                query = query.filter(MedicalCondition.status == status)

            conditions = query.order_by(desc(MedicalCondition.created_at)).all()
            logger.info(f"Retrieved {len(conditions)} medical conditions for user {user_id}")
            return conditions

        except Exception as e:
            logger.error(f"Error retrieving medical conditions for user {user_id}: {e}")
            return []

    def get_active_conditions(self, user_id: int) -> List[MedicalCondition]:
        """Get only active/chronic conditions"""
        try:
            conditions = (
                self.db.query(MedicalCondition)
                .filter(
                    and_(
                        MedicalCondition.user_id == user_id,
                        MedicalCondition.status.in_(["active", "chronic", "managed"]),
                    )
                )
                .order_by(desc(MedicalCondition.created_at))
                .all()
            )
            return conditions
        except Exception as e:
            logger.error(f"Error retrieving active conditions for user {user_id}: {e}")
            return []

    def add_condition(
        self,
        user_id: int,
        condition_name: str,
        status: str = "active",
        severity: Optional[str] = None,
        diagnosed_date: Optional[datetime] = None,
        notes: Optional[str] = None,
    ) -> Optional[MedicalCondition]:
        """Add a new medical condition"""
        try:
            condition = MedicalCondition(
                user_id=user_id,
                condition_name=condition_name,
                status=status,
                severity=severity,
                diagnosed_date=diagnosed_date,
                notes=notes,
            )
            return self.create(condition)
        except Exception as e:
            logger.error(f"Error adding medical condition: {e}")
            return None

    def update_status(self, condition_id: int, status: str) -> Optional[MedicalCondition]:
        """Update condition status"""
        try:
            condition = self.get_by_id(condition_id)
            if condition:
                condition.status = status
                condition.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Updated condition {condition_id} status to {status}")
                return condition
            return None
        except Exception as e:
            logger.error(f"Error updating condition status: {e}")
            self.db.rollback()
            return None
