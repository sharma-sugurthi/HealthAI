"""
Allergy Repository - Manages allergy data
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.models.allergy import Allergy
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class AllergyRepository(BaseRepository[Allergy]):
    """Repository for allergy management"""

    def __init__(self, db: Session):
        super().__init__(Allergy, db)

    def get_by_user(self, user_id: int) -> List[Allergy]:
        """Get all allergies for a user"""
        try:
            allergies = (
                self.db.query(Allergy)
                .filter(Allergy.user_id == user_id)
                .order_by(desc(Allergy.severity), desc(Allergy.created_at))
                .all()
            )
            logger.info(f"Retrieved {len(allergies)} allergies for user {user_id}")
            return allergies

        except Exception as e:
            logger.error(f"Error retrieving allergies for user {user_id}: {e}")
            return []

    def get_severe_allergies(self, user_id: int) -> List[Allergy]:
        """Get severe/life-threatening allergies"""
        try:
            allergies = (
                self.db.query(Allergy)
                .filter(
                    Allergy.user_id == user_id,
                    Allergy.severity.in_(["severe", "life-threatening"]),
                )
                .all()
            )
            return allergies
        except Exception as e:
            logger.error(f"Error retrieving severe allergies for user {user_id}: {e}")
            return []

    def add_allergy(
        self,
        user_id: int,
        allergen: str,
        reaction: str,
        severity: str = "moderate",
        allergen_type: Optional[str] = None,
        verified_date: Optional[datetime] = None,
        verified_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[Allergy]:
        """Add a new allergy"""
        try:
            allergy = Allergy(
                user_id=user_id,
                allergen=allergen,
                allergen_type=allergen_type,
                reaction=reaction,
                severity=severity,
                verified_date=verified_date,
                verified_by=verified_by,
                notes=notes,
            )
            return self.create(allergy)
        except Exception as e:
            logger.error(f"Error adding allergy: {e}")
            return None

    def check_allergen(self, user_id: int, allergen_name: str) -> Optional[Allergy]:
        """Check if user has specific allergy"""
        try:
            allergy = (
                self.db.query(Allergy)
                .filter(
                    Allergy.user_id == user_id,
                    Allergy.allergen.ilike(f"%{allergen_name}%"),
                )
                .first()
            )
            return allergy
        except Exception as e:
            logger.error(f"Error checking allergen: {e}")
            return None
