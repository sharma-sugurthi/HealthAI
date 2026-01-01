import logging
import os
import time
from typing import Optional

from openai import OpenAI

from config import config

# Using OpenRouter API for AI-powered healthcare assistance
# OpenRouter provides access to multiple AI models including xAI's Grok

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthAIClient:
    """Handles all AI API interactions with error handling and retry logic via OpenRouter"""

    def __init__(self, max_retries=None, retry_delay=None):
        self.max_retries = max_retries or config.AI_MAX_RETRIES
        self.retry_delay = retry_delay or config.AI_RETRY_DELAY
        self.api_key = config.OPENROUTER_API_KEY

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        # Initialize OpenAI client with OpenRouter endpoint
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={"HTTP-Referer": "https://healthai.app", "X-Title": config.APP_NAME},
        )

        # Use configured AI model
        self.model_name = config.AI_MODEL

    def _make_request(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Make a request to OpenRouter API with retry logic"""

        # Build messages array for OpenAI-compatible format
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=config.AI_TEMPERATURE,
                    max_tokens=config.AI_MAX_TOKENS,
                )

                # Extract response content
                if response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        return content
                    else:
                        return "I apologize, but I couldn't generate a response. Please try again or rephrase your question."
                else:
                    return "I apologize, but I couldn't generate a response. Please try again."

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"All retry attempts failed: {str(e)}")
                    return f"I'm experiencing technical difficulties. Please try again in a moment. Error: {str(e)}"

        return "Unable to process your request at this time. Please try again later."

    def chat_with_patient(self, message: str) -> str:
        """Handle patient chat queries"""

        system_instruction = """You are HealthAI, an intelligent healthcare assistant. Your role is to:
1. Provide accurate, evidence-based health information
2. Be empathetic and supportive
3. Always remind users that you are an AI assistant and not a substitute for professional medical advice
4. Encourage users to consult healthcare professionals for serious concerns
5. Be clear and concise in your responses
6. Ask clarifying questions when needed

Important: Always include a disclaimer that you are not a doctor and users should seek professional medical advice for diagnosis and treatment."""

        return self._make_request(message, system_instruction)

    def analyze_symptoms(self, symptoms: str) -> str:
        """Analyze symptoms and suggest possible conditions"""

        system_instruction = """You are a medical symptom analyzer. Based on the symptoms provided:
1. List possible conditions that could cause these symptoms (from most to least likely)
2. Explain why each condition might be relevant
3. Suggest when to seek immediate medical attention
4. Recommend appropriate next steps

IMPORTANT: Always emphasize that this is not a diagnosis and users must consult a healthcare professional for proper evaluation.

Format your response clearly with:
- Possible Conditions (with likelihood)
- When to Seek Immediate Care
- Recommended Next Steps
- Disclaimer"""

        prompt = f"Please analyze these symptoms and provide possible conditions:\n\n{symptoms}"
        return self._make_request(prompt, system_instruction)

    def generate_treatment_plan(self, condition: str, patient_info: dict) -> str:
        """Generate a treatment plan recommendation"""

        system_instruction = """You are a healthcare planning assistant. Generate a comprehensive treatment plan that includes:
1. Overview of the condition
2. Recommended lifestyle modifications
3. Dietary recommendations
4. Exercise suggestions
5. When to follow up with healthcare providers
6. Warning signs to watch for

IMPORTANT: This is a general wellness plan, not a medical prescription. Always remind users to consult their healthcare provider before starting any treatment."""

        patient_context = (
            f"Patient: {patient_info.get('age')} years old, {patient_info.get('gender')}"
        )
        prompt = f"{patient_context}\n\nCondition: {condition}\n\nPlease generate a comprehensive treatment and wellness plan."

        return self._make_request(prompt, system_instruction)

    def get_health_advice(self, topic: str) -> str:
        """Get general health advice on a topic"""

        system_instruction = """You are a health educator. Provide clear, evidence-based information about health topics.
Include:
1. Key facts about the topic
2. Best practices
3. Common misconceptions
4. When to consult a healthcare provider

Keep responses informative but accessible to general audiences."""

        prompt = f"Please provide information and advice about: {topic}"
        return self._make_request(prompt, system_instruction)


def get_ai_client() -> Optional[HealthAIClient]:
    """Factory function to get AI client with error handling"""
    try:
        return HealthAIClient()
    except Exception as e:
        logger.error(f"Failed to initialize AI client: {str(e)}")
        return None
