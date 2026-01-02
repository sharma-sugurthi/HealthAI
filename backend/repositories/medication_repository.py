"""
Medication Repository - Manages medication data
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from backend.models.medication import Medication
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MedicationRepository(BaseRepository[Medication]):
    """Repository for medication management"""

    def __init__(self, db: Session):
        super().__init__(Medication, db)

    def get_by_user(self, user_id: int, status: Optional[str] = None) -> List[Medication]:
        """Get all medications for a user"""
        try:
            query = self.db.query(Medication).filter(Medication.user_id == user_id)

            if status:
                query = query.filter(Medication.status == status)

            medications = query.order_by(desc(Medication.created_at)).all()
            logger.info(f"Retrieved {len(medications)} medications for user {user_id}")
            return medications

        except Exception as e:
            logger.error(f"Error retrieving medications for user {user_id}: {e}")
            return []

    def get_active_medications(self, user_id: int) -> List[Medication]:
        """Get only active medications"""
        try:
            medications = (
                self.db.query(Medication)
                .filter(and_(Medication.user_id == user_id, Medication.status == "active"))
                .order_by(desc(Medication.start_date))
                .all()
            )
            return medications
        except Exception as e:
            logger.error(f"Error retrieving active medications for user {user_id}: {e}")
            return []

    def add_medication(
        self,
        user_id: int,
        medication_name: str,
        dosage: Optional[str] = None,
        frequency: Optional[str] = None,
        route: Optional[str] = None,
        start_date: Optional[datetime] = None,
        reason: Optional[str] = None,
        prescribing_doctor: Optional[str] = None,
    ) -> Optional[Medication]:
        """Add a new medication"""
        try:
            medication = Medication(
                user_id=user_id,
                medication_name=medication_name,
                dosage=dosage,
                frequency=frequency,
                route=route,
                start_date=start_date,
                status="active",
                reason=reason,
                prescribing_doctor=prescribing_doctor,
            )
            return self.create(medication)
        except Exception as e:
            logger.error(f"Error adding medication: {e}")
            return None

    def discontinue_medication(
        self, medication_id: int, end_date: Optional[datetime] = None
    ) -> Optional[Medication]:
        """Mark medication as discontinued"""
        try:
            medication = self.get_by_id(medication_id)
            if medication:
                medication.status = "discontinued"
                medication.end_date = end_date or datetime.utcnow()
                medication.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Discontinued medication {medication_id}")
                return medication
            return None
        except Exception as e:
            logger.error(f"Error discontinuing medication: {e}")
            self.db.rollback()
            return None
