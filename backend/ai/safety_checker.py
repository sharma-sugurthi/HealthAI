"""
Safety Checker - Validates AI responses for medical safety
"""

import re
from typing import Dict, List

from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MedicalSafetyChecker:
    """
    Validates AI responses for safety concerns
    """

    # Emergency symptoms that require immediate medical attention
    EMERGENCY_KEYWORDS = [
        "chest pain",
        "difficulty breathing",
        "severe bleeding",
        "loss of consciousness",
        "severe headache",
        "stroke symptoms",
        "heart attack",
        "suicidal",
        "severe allergic reaction",
        "anaphylaxis",
        "seizure",
        "severe abdominal pain",
        "coughing blood",
        "sudden vision loss",
        "severe burns",
        "poisoning",
        "overdose",
    ]

    # Patterns that suggest medication prescriptions (should be avoided)
    MEDICATION_PRESCRIPTION_PATTERNS = [
        r"take \d+\s*mg",
        r"prescribe \w+",
        r"dosage of \d+",
        r"start taking \w+",
        r"\d+\s*mg\s+of\s+\w+",
        r"you should take \w+",
    ]

    def __init__(self):
        self.logger = get_logger(__name__)

    def check_response(self, response: str, patient_context: Dict) -> Dict:
        """
        Comprehensive safety check of AI response

        Args:
            response: AI generated response
            patient_context: Patient medical context

        Returns:
            {
                'has_concerns': bool,
                'flags': [list of concern descriptions],
                'severity': 'low'|'medium'|'high',
                'recommendations': [safety recommendations]
            }
        """
        flags = []
        severity = "low"

        # Check for medication prescription attempts
        if self._check_medication_prescription(response):
            flags.append("Response contains medication prescription language")
            severity = "high"

        # Check for allergy conflicts
        allergy_conflicts = self._check_allergy_conflicts(response, patient_context)
        if allergy_conflicts:
            flags.extend(allergy_conflicts)
            severity = "high"

        # Check for medication interaction warnings needed
        interaction_warnings = self._check_medication_interactions(response, patient_context)
        if interaction_warnings:
            flags.extend(interaction_warnings)
            severity = "medium" if severity == "low" else severity

        # Check if emergency disclaimer is needed
        if self._needs_emergency_disclaimer(response):
            flags.append("Response should include emergency care disclaimer")
            severity = "medium" if severity == "low" else severity

        has_concerns = len(flags) > 0

        return {
            "has_concerns": has_concerns,
            "flags": flags,
            "severity": severity,
            "recommendations": self._generate_recommendations(flags),
        }

    def detect_emergency_symptoms(self, text: str) -> bool:
        """
        Detect if text mentions emergency symptoms

        Args:
            text: Text to check

        Returns:
            True if emergency symptoms detected
        """
        text_lower = text.lower()
        for keyword in self.EMERGENCY_KEYWORDS:
            if keyword in text_lower:
                logger.warning(f"Emergency keyword detected: {keyword}")
                return True
        return False

    def _check_medication_prescription(self, response: str) -> bool:
        """Check if response contains medication prescription language"""
        for pattern in self.MEDICATION_PRESCRIPTION_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                logger.warning(f"Medication prescription pattern detected: {pattern}")
                return True
        return False

    def _check_allergy_conflicts(self, response: str, patient_context: Dict) -> List[str]:
        """Check for potential allergy conflicts"""
        conflicts = []
        allergies = patient_context.get("allergies", [])

        for allergy in allergies:
            allergen = allergy.get("allergen", "").lower()
            if allergen and allergen in response.lower():
                severity = allergy.get("severity", "unknown")
                conflicts.append(f"⚠️ ALLERGY ALERT: Patient allergic to {allergen} ({severity})")
                logger.warning(f"Allergy conflict detected: {allergen}")

        return conflicts

    def _check_medication_interactions(self, response: str, patient_context: Dict) -> List[str]:
        """Check if response should mention medication interactions"""
        warnings = []
        current_meds = patient_context.get("current_medications", [])

        # If patient is on medications and response mentions treatments
        if current_meds and any(
            word in response.lower() for word in ["treatment", "medication", "drug", "medicine"]
        ):
            warnings.append(
                "Response should remind patient to discuss with doctor about current medications"
            )

        return warnings

    def _needs_emergency_disclaimer(self, response: str) -> bool:
        """Check if response needs emergency care disclaimer"""
        serious_keywords = [
            "severe",
            "serious",
            "emergency",
            "urgent",
            "immediate",
            "critical",
        ]
        return any(keyword in response.lower() for keyword in serious_keywords)

    def _generate_recommendations(self, flags: List[str]) -> List[str]:
        """Generate safety recommendations based on flags"""
        recommendations = []

        if any("prescription" in flag.lower() for flag in flags):
            recommendations.append(
                "Remove specific medication names and dosages. Use general medication classes instead."
            )

        if any("allergy" in flag.lower() for flag in flags):
            recommendations.append("Add prominent allergy warning at the beginning of response.")

        if any("interaction" in flag.lower() for flag in flags):
            recommendations.append(
                "Add reminder to discuss with healthcare provider about current medications."
            )

        if any("emergency" in flag.lower() for flag in flags):
            recommendations.append("Add clear guidance on when to seek emergency medical care.")

        return recommendations


class SafetyWarningGenerator:
    """
    Generates appropriate safety warnings and disclaimers
    """

    @staticmethod
    def add_emergency_warning(response: str) -> str:
        """Add emergency care warning to response"""
        warning = (
            "\n\n🚨 **IMPORTANT**: If you experience severe or worsening symptoms, "
            "seek immediate medical attention by calling emergency services or "
            "going to the nearest emergency room.\n"
        )
        return warning + response

    @staticmethod
    def add_medication_disclaimer(response: str) -> str:
        """Add medication safety disclaimer"""
        disclaimer = (
            "\n\n⚕️ **MEDICATION REMINDER**: Never start, stop, or change medications "
            "without consulting your healthcare provider. This information is for "
            "educational purposes only.\n"
        )
        return response + disclaimer

    @staticmethod
    def add_allergy_alert(response: str, allergen: str, severity: str) -> str:
        """Add allergy-specific alert"""
        alert = (
            f"\n\n⚠️ **ALLERGY ALERT**: Your medical records show you have a "
            f"{severity} allergy to {allergen}. Please inform all healthcare "
            f"providers about this allergy.\n"
        )
        return alert + response

    @staticmethod
    def add_general_disclaimer(response: str) -> str:
        """Add general medical disclaimer"""
        disclaimer = (
            "\n\n---\n"
            "*This information is for educational purposes only and is not a "
            "substitute for professional medical advice, diagnosis, or treatment. "
            "Always consult your healthcare provider with any questions about your health.*"
        )
        return response + disclaimer
