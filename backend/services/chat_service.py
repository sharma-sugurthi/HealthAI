"""
Chat service for managing AI conversations.
"""

from typing import Dict, List

from sqlalchemy.orm import Session

from ai_client import get_ai_client
from backend.repositories.chat_repository import ChatRepository
from backend.utils.logger import get_logger
from validation import InputValidator

logger = get_logger(__name__)


class ChatService:
    """Service for chat operations"""

    def __init__(self, session: Session):
        """
        Initialize chat service.

        Args:
            session: Database session
        """
        self.session = session
        self.chat_repo = ChatRepository(session)
        self.ai_client = get_ai_client()

    def send_message(self, user_id: int, message: str) -> Dict:
        """
        Send a message and get AI response.

        Args:
            user_id: User ID
            message: User's message

        Returns:
            Dictionary with message and response

        Raises:
            ValidationError: If message validation fails
            Exception: If AI service fails
        """
        try:
            # Validate message
            message = InputValidator.validate_message(message)

            # Get AI response
            if self.ai_client:
                response = self.ai_client.chat_with_patient(message)
            else:
                response = "I'm currently unavailable. Please try again later."
                logger.warning("AI client not available")

            # Save to database
            chat = self.chat_repo.add_message(user_id, message, response)

            logger.info(f"Message processed for user_id={user_id}")

            return {
                "id": chat.id,
                "message": chat.message,
                "response": chat.response,
                "timestamp": chat.timestamp,
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def get_chat_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        Get chat history for a user.

        Args:
            user_id: User ID
            limit: Maximum number of messages

        Returns:
            List of chat messages
        """
        history = self.chat_repo.get_user_history(user_id, limit)

        return [
            {
                "id": chat.id,
                "message": chat.message,
                "response": chat.response,
                "timestamp": chat.timestamp,
            }
            for chat in reversed(history)  # Reverse to show oldest first
        ]

    def analyze_symptoms(self, user_id: int, symptoms: str) -> Dict:
        """
        Analyze symptoms using AI.

        Args:
            user_id: User ID
            symptoms: Symptom description

        Returns:
            Dictionary with analysis
        """
        try:
            # Validate symptoms
            symptoms = InputValidator.validate_symptoms(symptoms)

            # Get AI analysis
            if self.ai_client:
                analysis = self.ai_client.analyze_symptoms(symptoms)
            else:
                analysis = "AI service is currently unavailable."
                logger.warning("AI client not available for symptom analysis")

            # Save to chat history
            chat = self.chat_repo.add_message(user_id, f"Symptom Check: {symptoms}", analysis)

            logger.info(f"Symptoms analyzed for user_id={user_id}")

            return {
                "id": chat.id,
                "symptoms": symptoms,
                "analysis": analysis,
                "timestamp": chat.timestamp,
            }

        except Exception as e:
            logger.error(f"Error analyzing symptoms: {str(e)}")
            raise

    def generate_treatment_plan(self, user_id: int, condition: str, patient_info: Dict) -> str:
        """
        Generate treatment plan using AI.

        Args:
            user_id: User ID
            condition: Medical condition
            patient_info: Patient information (age, gender)

        Returns:
            Treatment plan text
        """
        try:
            # Validate condition
            condition = InputValidator.validate_condition(condition)

            # Get AI treatment plan
            if self.ai_client:
                plan = self.ai_client.generate_treatment_plan(condition, patient_info)
            else:
                plan = "AI service is currently unavailable."
                logger.warning("AI client not available for treatment plan")

            logger.info(f"Treatment plan generated for user_id={user_id}, condition={condition}")

            return plan

        except Exception as e:
            logger.error(f"Error generating treatment plan: {str(e)}")
            raise

    def clear_history(self, user_id: int) -> int:
        """
        Clear chat history for a user.

        Args:
            user_id: User ID

        Returns:
            Number of deleted messages
        """
        count = self.chat_repo.delete_user_history(user_id)
        logger.info(f"Cleared {count} messages for user_id={user_id}")
        return count
