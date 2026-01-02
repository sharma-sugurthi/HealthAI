"""
Medical Context Service - Gathers complete patient context for AI
"""

from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from backend.models.user import User
from backend.repositories.allergy_repository import AllergyRepository
from backend.repositories.chat_repository import ChatRepository
from backend.repositories.medical_history_repository import MedicalHistoryRepository
from backend.repositories.medication_repository import MedicationRepository
from backend.repositories.symptom_repository import SymptomRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MedicalContextService:
    """
    Gathers and formats complete patient medical context for AI
    """

    def __init__(self, db: Session):
        self.db = db
        self.medical_history_repo = MedicalHistoryRepository(db)
        self.medication_repo = MedicationRepository(db)
        self.allergy_repo = AllergyRepository(db)
        self.symptom_repo = SymptomRepository(db)
        self.chat_repo = ChatRepository(db)

    def get_patient_context(self, user_id: int) -> Dict:
        """
        Compile complete patient context for AI

        Args:
            user_id: User ID

        Returns:
            Dictionary with complete patient context:
            {
                'age': int,
                'gender': str,
                'medical_history': [list of conditions],
                'current_medications': [list of medications],
                'allergies': [list of allergies],
                'recent_symptoms': [list of symptoms],
                'conversation_context': [recent conversations]
            }
        """
        try:
            # Get user basic info
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"User {user_id} not found")
                return self._empty_context()

            # Gather all medical data
            context = {
                "user_id": user_id,
                "age": user.age,
                "gender": user.gender,
                "full_name": user.full_name,
                "medical_history": self._get_medical_history_list(user_id),
                "current_medications": self._get_current_medications_list(user_id),
                "allergies": self._get_allergies_list(user_id),
                "recent_symptoms": self._get_recent_symptoms_list(user_id),
                "conversation_context": self._get_conversation_context_list(user_id),
            }

            logger.info(f"Compiled complete context for user {user_id}")
            return context

        except Exception as e:
            logger.error(f"Error compiling patient context: {e}")
            return self._empty_context()

    def get_medical_history_summary(self, user_id: int) -> str:
        """
        Get formatted medical history summary

        Returns:
            Formatted string of medical conditions
        """
        conditions = self.medical_history_repo.get_active_conditions(user_id)

        if not conditions:
            return "No significant active medical conditions reported"

        summary_lines = []
        for condition in conditions:
            status = condition.status
            severity = f" ({condition.severity})" if condition.severity else ""
            summary_lines.append(f"- {condition.condition_name} ({status}){severity}")

        return "\n".join(summary_lines)

    def get_current_medications_summary(self, user_id: int) -> str:
        """
        Get formatted current medications summary

        Returns:
            Formatted string of active medications
        """
        medications = self.medication_repo.get_active_medications(user_id)

        if not medications:
            return "No current medications reported"

        summary_lines = []
        for med in medications:
            dosage = med.dosage or ""
            frequency = med.frequency or ""
            summary_lines.append(f"- {med.medication_name} {dosage} {frequency}".strip())

        return "\n".join(summary_lines)

    def get_allergies_summary(self, user_id: int) -> str:
        """
        Get formatted allergies summary

        Returns:
            Formatted string of allergies
        """
        allergies = self.allergy_repo.get_by_user(user_id)

        if not allergies:
            return "No known allergies"

        summary_lines = []
        for allergy in allergies:
            severity = allergy.severity
            reaction = allergy.reaction[:50] if allergy.reaction else ""
            summary_lines.append(f"- {allergy.allergen} ({severity}): {reaction}")

        return "\n".join(summary_lines)

    def get_recent_symptoms_summary(self, user_id: int, days: int = 30) -> str:
        """
        Get formatted recent symptoms summary

        Args:
            user_id: User ID
            days: Number of days to look back

        Returns:
            Formatted string of recent symptoms
        """
        symptoms = self.symptom_repo.get_recent_symptoms(user_id, days)

        if not symptoms:
            return "No recent symptoms logged"

        summary_lines = []
        for symptom in symptoms[:5]:  # Last 5 symptoms
            date = symptom.logged_at.strftime("%Y-%m-%d") if symptom.logged_at else ""
            desc = symptom.symptom_description[:100]
            severity = f" (severity: {symptom.severity}/10)" if symptom.severity else ""
            summary_lines.append(f"- {date}: {desc}{severity}")

        return "\n".join(summary_lines)

    def get_conversation_context(self, user_id: int, limit: int = 5) -> str:
        """
        Get recent conversation summary

        Args:
            user_id: User ID
            limit: Number of recent conversations

        Returns:
            Formatted conversation history
        """
        conversations = self.chat_repo.get_user_history(user_id, limit=limit)

        if not conversations:
            return "First conversation with patient"

        summary_lines = []
        for conv in conversations:
            msg = conv.message[:100] if conv.message else ""
            resp = conv.response[:150] if conv.response else ""
            summary_lines.append(f"Patient: {msg}...\nDr. HealthAI: {resp}...\n")

        return "\n".join(summary_lines)

    def has_critical_allergies(self, user_id: int) -> bool:
        """Check if patient has severe/life-threatening allergies"""
        severe_allergies = self.allergy_repo.get_severe_allergies(user_id)
        return len(severe_allergies) > 0

    def get_allergy_warnings(self, user_id: int) -> List[str]:
        """Get list of critical allergy warnings"""
        severe_allergies = self.allergy_repo.get_severe_allergies(user_id)
        warnings = []
        for allergy in severe_allergies:
            warnings.append(f"⚠️ SEVERE ALLERGY: {allergy.allergen} - {allergy.reaction}")
        return warnings

    def _get_medical_history_list(self, user_id: int) -> List[Dict]:
        """Get medical history as list of dicts"""
        conditions = self.medical_history_repo.get_active_conditions(user_id)
        return [
            {
                "condition_name": c.condition_name,
                "status": c.status,
                "severity": c.severity,
                "diagnosed_date": (c.diagnosed_date.isoformat() if c.diagnosed_date else None),
            }
            for c in conditions
        ]

    def _get_current_medications_list(self, user_id: int) -> List[Dict]:
        """Get current medications as list of dicts"""
        medications = self.medication_repo.get_active_medications(user_id)
        return [
            {
                "medication_name": m.medication_name,
                "dosage": m.dosage,
                "frequency": m.frequency,
                "route": m.route,
            }
            for m in medications
        ]

    def _get_allergies_list(self, user_id: int) -> List[Dict]:
        """Get allergies as list of dicts"""
        allergies = self.allergy_repo.get_by_user(user_id)
        return [
            {
                "allergen": a.allergen,
                "allergen_type": a.allergen_type,
                "reaction": a.reaction,
                "severity": a.severity,
            }
            for a in allergies
        ]

    def _get_recent_symptoms_list(self, user_id: int) -> List[Dict]:
        """Get recent symptoms as list of dicts"""
        symptoms = self.symptom_repo.get_recent_symptoms(user_id, days=30)
        return [
            {
                "symptom_description": s.symptom_description,
                "severity": s.severity,
                "logged_at": s.logged_at.isoformat() if s.logged_at else None,
                "body_part": s.body_part,
            }
            for s in symptoms[:10]  # Last 10 symptoms
        ]

    def _get_conversation_context_list(self, user_id: int) -> List[Dict]:
        """Get conversation context as list of dicts"""
        conversations = self.chat_repo.get_user_history(user_id, limit=5)
        return [
            {
                "message": c.message,
                "response": c.response[:200],  # Truncate long responses
                "timestamp": c.timestamp.isoformat() if c.timestamp else None,
            }
            for c in conversations
        ]

    def _empty_context(self) -> Dict:
        """Return empty context structure"""
        return {
            "user_id": None,
            "age": None,
            "gender": None,
            "full_name": None,
            "medical_history": [],
            "current_medications": [],
            "allergies": [],
            "recent_symptoms": [],
            "conversation_context": [],
        }
