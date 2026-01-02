"""
Symptom Repository - Manages symptom log data
"""

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.models.symptom_log import SymptomLog
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class SymptomRepository(BaseRepository[SymptomLog]):
    """Repository for symptom log management"""

    def __init__(self, db: Session):
        super().__init__(SymptomLog, db)
        self.session = db

    def get_by_user(self, user_id: int, limit: Optional[int] = None) -> List[SymptomLog]:
        """Get symptom logs for a user"""
        try:
            query = (
                self.db.query(SymptomLog)
                .filter(SymptomLog.user_id == user_id)
                .order_by(desc(SymptomLog.logged_at))
            )

            if limit:
                query = query.limit(limit)

            symptoms = query.all()
            logger.info(f"Retrieved {len(symptoms)} symptom logs for user {user_id}")
            return symptoms

        except Exception as e:
            logger.error(f"Error retrieving symptom logs for user {user_id}: {e}")
            return []

    def get_recent_symptoms(self, user_id: int, days: int = 30) -> List[SymptomLog]:
        """Get symptoms from last N days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            symptoms = (
                self.db.query(SymptomLog)
                .filter(SymptomLog.user_id == user_id, SymptomLog.logged_at >= cutoff_date)
                .order_by(desc(SymptomLog.logged_at))
                .all()
            )
            return symptoms
        except Exception as e:
            logger.error(f"Error retrieving recent symptoms for user {user_id}: {e}")
            return []

    def log_symptom(
        self,
        user_id: int,
        symptom_description: str,
        severity: Optional[int] = None,
        body_part: Optional[str] = None,
        onset_date: Optional[datetime] = None,
        duration: Optional[str] = None,
        frequency: Optional[str] = None,
        quality: Optional[str] = None,
        associated_symptoms: Optional[str] = None,
        triggers: Optional[str] = None,
        relieving_factors: Optional[str] = None,
        aggravating_factors: Optional[str] = None,
        impact_on_life: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[SymptomLog]:
        """Log a new symptom"""
        try:
            symptom = SymptomLog(
                user_id=user_id,
                symptom_description=symptom_description,
                body_part=body_part,
                severity=severity,
                onset_date=onset_date,
                duration=duration,
                frequency=frequency,
                quality=quality,
                associated_symptoms=associated_symptoms,
                triggers=triggers,
                relieving_factors=relieving_factors,
                aggravating_factors=aggravating_factors,
                impact_on_life=impact_on_life,
                notes=notes,
            )
            return self.create(symptom)
        except Exception as e:
            logger.error(f"Error logging symptom: {e}")
            return None

    def get_symptom_patterns(
        self, user_id: int, body_part: Optional[str] = None
    ) -> List[SymptomLog]:
        """Get symptom patterns for analysis"""
        try:
            query = self.db.query(SymptomLog).filter(SymptomLog.user_id == user_id)

            if body_part:
                query = query.filter(SymptomLog.body_part.ilike(f"%{body_part}%"))

            symptoms = query.order_by(desc(SymptomLog.logged_at)).limit(50).all()
            return symptoms
        except Exception as e:
            logger.error(f"Error retrieving symptom patterns: {e}")
            return []
