"""
Prompt Builder - Constructs context-aware prompts for medical AI
"""

from backend.ai.prompt_templates import MedicalPromptTemplates, PromptFormatter


class MedicalPromptBuilder:
    """
    Builds sophisticated, context-aware prompts with patient history
    """

    def __init__(self):
        self.templates = MedicalPromptTemplates()
        self.formatter = PromptFormatter()

    def build_system_prompt(self, patient_context: dict) -> str:
        """
        Build system prompt with complete patient context

        Args:
            patient_context: Dict with age, gender, medical_history, medications, allergies, etc.

        Returns:
            Formatted system prompt with patient context
        """
        return self.templates.SYSTEM_PROMPT.format(
            age=patient_context.get("age", "Unknown"),
            gender=patient_context.get("gender", "Unknown"),
            medical_history=self.formatter.format_medical_history(
                patient_context.get("medical_history", [])
            ),
            current_medications=self.formatter.format_medications(
                patient_context.get("current_medications", [])
            ),
            allergies=self.formatter.format_allergies(patient_context.get("allergies", [])),
            recent_symptoms=self.formatter.format_recent_symptoms(
                patient_context.get("recent_symptoms", [])
            ),
        )

    def build_symptom_analysis_prompt(self, symptoms: str, patient_context: dict) -> str:
        """
        Build comprehensive symptom analysis prompt

        Args:
            symptoms: Patient's symptom description
            patient_context: Patient medical context

        Returns:
            Formatted symptom analysis prompt
        """
        return self.templates.SYMPTOM_ANALYSIS_PROMPT.format(
            symptoms=symptoms,
            age=patient_context.get("age", "Unknown"),
            gender=patient_context.get("gender", "Unknown"),
            medical_history=self.formatter.format_medical_history(
                patient_context.get("medical_history", [])
            ),
            current_medications=self.formatter.format_medications(
                patient_context.get("current_medications", [])
            ),
        )

    def build_treatment_plan_prompt(self, condition: str, patient_context: dict) -> str:
        """
        Build personalized treatment plan prompt

        Args:
            condition: Medical condition for treatment plan
            patient_context: Patient medical context

        Returns:
            Formatted treatment plan prompt
        """
        return self.templates.TREATMENT_PLAN_PROMPT.format(
            condition=condition,
            age=patient_context.get("age", "Unknown"),
            gender=patient_context.get("gender", "Unknown"),
            medical_history=self.formatter.format_medical_history(
                patient_context.get("medical_history", [])
            ),
            current_medications=self.formatter.format_medications(
                patient_context.get("current_medications", [])
            ),
            allergies=self.formatter.format_allergies(patient_context.get("allergies", [])),
        )

    def build_follow_up_prompt(self, current_message: str, conversation_history: list) -> str:
        """
        Build follow-up conversation prompt with history

        Args:
            current_message: Patient's current message
            conversation_history: List of previous conversations

        Returns:
            Formatted follow-up prompt
        """
        # Summarize previous conversations
        summary = self._summarize_conversations(conversation_history)

        return self.templates.FOLLOW_UP_PROMPT.format(
            previous_conversation_summary=summary, current_message=current_message
        )

    def build_emergency_response(self, emergency_symptoms: str, urgency_explanation: str) -> str:
        """
        Build emergency response prompt

        Args:
            emergency_symptoms: Detected emergency symptoms
            urgency_explanation: Why this is urgent

        Returns:
            Formatted emergency response
        """
        immediate_actions = self._get_immediate_actions(emergency_symptoms)

        return self.templates.EMERGENCY_RESPONSE.format(
            emergency_symptoms=emergency_symptoms,
            urgency_explanation=urgency_explanation,
            immediate_actions=immediate_actions,
        )

    def _summarize_conversations(self, conversations: list) -> str:
        """Summarize recent conversations for context"""
        if not conversations:
            return "First conversation with patient"

        summaries = []
        for conv in conversations[-3:]:  # Last 3 conversations
            msg = conv.get("message", "")[:100]
            resp = conv.get("response", "")[:150]
            summaries.append(f"Patient: {msg}...\nDr. HealthAI: {resp}...")

        return "\n\n".join(summaries)

    def _get_immediate_actions(self, symptoms: str) -> str:
        """Get immediate actions for emergency symptoms"""
        # Basic emergency actions
        actions = [
            "Stay calm and call emergency services immediately",
            "Do not drive yourself - call ambulance or have someone drive you",
            "If alone, unlock door for emergency responders",
            "Have list of current medications ready",
            "Note time symptoms started",
        ]

        # Add symptom-specific actions
        if "chest pain" in symptoms.lower():
            actions.append("Sit down and rest, chew aspirin if not allergic")
        elif "difficulty breathing" in symptoms.lower():
            actions.append("Sit upright, loosen tight clothing")
        elif "bleeding" in symptoms.lower():
            actions.append("Apply direct pressure to wound")

        return "\n".join([f"- {action}" for action in actions])
