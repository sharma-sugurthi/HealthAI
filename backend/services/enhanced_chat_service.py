"""
Enhanced Chat Service - Intelligent, context-aware medical AI chat
"""

from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ai_client import get_ai_client
from backend.ai.prompt_builder import MedicalPromptBuilder
from backend.ai.safety_checker import MedicalSafetyChecker, SafetyWarningGenerator
from backend.repositories.chat_repository import ChatRepository
from backend.services.medical_context_service import MedicalContextService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class EnhancedChatService:
    """
    Context-aware chat service with advanced medical AI
    """

    def __init__(self, db: Session):
        self.db = db
        self.context_service = MedicalContextService(db)
        self.prompt_builder = MedicalPromptBuilder()
        self.safety_checker = MedicalSafetyChecker()
        self.warning_generator = SafetyWarningGenerator()
        self.chat_repo = ChatRepository(db)
        self.ai_client = get_ai_client()

    def send_contextual_message(self, user_id: int, message: str) -> Dict[str, any]:
        """
        Send message with full patient context for intelligent response

        Args:
            user_id: User ID
            message: User's message

        Returns:
            {
                'message': original message,
                'response': AI response with safety checks,
                'safety_flags': list of safety concerns,
                'has_emergency': bool,
                'context_used': bool
            }
        """
        try:
            # 1. Check for emergency symptoms in user message
            has_emergency = self.safety_checker.detect_emergency_symptoms(message)
            if has_emergency:
                return self._handle_emergency_response(user_id, message)

            # 2. Get complete patient context
            patient_context = self.context_service.get_patient_context(user_id)
            logger.info(f"Retrieved context for user {user_id}")

            # 3. Build context-aware system prompt
            system_prompt = self.prompt_builder.build_system_prompt(patient_context)

            # 4. Get AI response with context
            ai_response = self.ai_client.chat_completion(
                system_prompt=system_prompt,
                user_message=message,
                max_tokens=1500,  # Allow comprehensive responses
                temperature=0.7,
            )

            # 5. Safety check the response
            safety_result = self.safety_checker.check_response(ai_response, patient_context)

            # 6. Add safety warnings if needed
            final_response = self._add_safety_warnings(ai_response, safety_result, patient_context)

            # 7. Add general disclaimer
            final_response = self.warning_generator.add_general_disclaimer(final_response)

            # 8. Save conversation with context
            self.chat_repo.add_message(user_id=user_id, message=message, response=final_response)

            logger.info(f"Sent contextual message for user {user_id}")

            return {
                "message": message,
                "response": final_response,
                "safety_flags": safety_result.get("flags", []),
                "has_emergency": False,
                "context_used": True,
                "severity": safety_result.get("severity", "low"),
            }

        except Exception as e:
            logger.error(f"Error in contextual message: {e}")
            return {
                "message": message,
                "response": "I apologize, but I encountered an error. Please try again or consult a healthcare provider.",
                "safety_flags": ["Error occurred"],
                "has_emergency": False,
                "context_used": False,
            }

    def analyze_symptoms_with_context(self, user_id: int, symptoms: str) -> Dict[str, any]:
        """
        Comprehensive symptom analysis with patient history

        Args:
            user_id: User ID
            symptoms: Symptom description

        Returns:
            Detailed symptom analysis with recommendations
        """
        try:
            # Check for emergency symptoms
            if self.safety_checker.detect_emergency_symptoms(symptoms):
                return self._handle_emergency_response(user_id, symptoms)

            # Get patient context
            patient_context = self.context_service.get_patient_context(user_id)

            # Build symptom analysis prompt
            analysis_prompt = self.prompt_builder.build_symptom_analysis_prompt(
                symptoms, patient_context
            )

            # Get comprehensive analysis
            system_prompt = self.prompt_builder.build_system_prompt(patient_context)
            ai_analysis = self.ai_client.chat_completion(
                system_prompt=system_prompt,
                user_message=analysis_prompt,
                max_tokens=2000,  # Longer for detailed analysis
                temperature=0.7,
            )

            # Safety check
            safety_result = self.safety_checker.check_response(ai_analysis, patient_context)

            # Add warnings
            final_analysis = self._add_safety_warnings(ai_analysis, safety_result, patient_context)
            final_analysis = self.warning_generator.add_general_disclaimer(final_analysis)

            # Save to chat history
            self.chat_repo.add_message(
                user_id=user_id,
                message=f"Symptom Analysis: {symptoms}",
                response=final_analysis,
            )

            return {
                "symptoms": symptoms,
                "analysis": final_analysis,
                "safety_flags": safety_result.get("flags", []),
                "has_emergency": False,
            }

        except Exception as e:
            logger.error(f"Error in symptom analysis: {e}")
            return {
                "symptoms": symptoms,
                "analysis": "Unable to analyze symptoms. Please consult a healthcare provider.",
                "safety_flags": ["Error occurred"],
                "has_emergency": False,
            }

    def generate_treatment_plan_with_context(self, user_id: int, condition: str) -> Dict[str, any]:
        """
        Generate personalized treatment plan with patient context

        Args:
            user_id: User ID
            condition: Medical condition

        Returns:
            Comprehensive treatment plan
        """
        try:
            # Get patient context
            patient_context = self.context_service.get_patient_context(user_id)

            # Build treatment plan prompt
            plan_prompt = self.prompt_builder.build_treatment_plan_prompt(
                condition, patient_context
            )

            # Get comprehensive plan
            system_prompt = self.prompt_builder.build_system_prompt(patient_context)
            ai_plan = self.ai_client.chat_completion(
                system_prompt=system_prompt,
                user_message=plan_prompt,
                max_tokens=2500,  # Very comprehensive
                temperature=0.7,
            )

            # Safety check
            safety_result = self.safety_checker.check_response(ai_plan, patient_context)

            # Add warnings
            final_plan = self._add_safety_warnings(ai_plan, safety_result, patient_context)

            # Add medication disclaimer
            final_plan = self.warning_generator.add_medication_disclaimer(final_plan)
            final_plan = self.warning_generator.add_general_disclaimer(final_plan)

            # Save to chat history
            self.chat_repo.add_message(
                user_id=user_id,
                message=f"Treatment Plan Request: {condition}",
                response=final_plan,
            )

            return {
                "condition": condition,
                "treatment_plan": final_plan,
                "safety_flags": safety_result.get("flags", []),
                "personalized": True,
            }

        except Exception as e:
            logger.error(f"Error generating treatment plan: {e}")
            return {
                "condition": condition,
                "treatment_plan": "Unable to generate plan. Please consult a healthcare provider.",
                "safety_flags": ["Error occurred"],
                "personalized": False,
            }

    def _handle_emergency_response(self, user_id: int, message: str) -> Dict:
        """Handle emergency symptom detection"""
        emergency_response = """
🚨 **EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION** 🚨

Your symptoms may indicate a medical emergency. Please:

1. **Call emergency services (911) immediately** or go to the nearest emergency room
2. Do NOT wait or try to treat this at home
3. If alone, call someone to be with you or unlock your door for emergency responders

**While waiting for help:**
- Stay calm
- Sit or lie down in a comfortable position
- Do not eat or drink anything
- Have your medication list ready if possible

**This is NOT the time for online medical advice. Get professional help NOW.**

---
*If this is not an emergency, please rephrase your question and I'll be happy to help.*
        """

        # Save emergency detection
        self.chat_repo.add_message(user_id=user_id, message=message, response=emergency_response)

        return {
            "message": message,
            "response": emergency_response,
            "safety_flags": ["EMERGENCY_DETECTED"],
            "has_emergency": True,
            "context_used": False,
        }

    def _add_safety_warnings(
        self, response: str, safety_result: Dict, patient_context: Dict
    ) -> str:
        """Add appropriate safety warnings to response"""
        warnings_added = response

        # Add allergy alerts
        for flag in safety_result.get("flags", []):
            if "ALLERGY ALERT" in flag:
                # Extract allergen from flag
                parts = flag.split(":")
                if len(parts) > 1:
                    allergen_info = parts[1].strip()
                    warnings_added = f"\n\n⚠️ {flag}\n\n" + warnings_added

        # Add emergency warning if needed
        if safety_result.get("severity") == "high":
            warnings_added = self.warning_generator.add_emergency_warning(warnings_added)

        return warnings_added
