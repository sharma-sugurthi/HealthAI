import os
import time
import logging
from typing import Optional
import google.generativeai as genai

# IMPORTANT: Integration with blueprint:python_gemini
# Using Google Gemini API for AI-powered healthcare assistance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiAPI:
    """Handles all Gemini API interactions with error handling and retry logic"""
    
    def __init__(self, max_retries=3, retry_delay=2):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_key = os.environ.get('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Use gemini-pro for text generation
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Configure safety settings to be more permissive for medical content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
    
    def _make_request(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Make a request to Gemini API with retry logic"""
        
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n{prompt}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(
                    full_prompt,
                    safety_settings=self.safety_settings
                )
                
                # Check if response was blocked
                if not response.text:
                    if hasattr(response, 'prompt_feedback'):
                        logger.warning(f"Response blocked: {response.prompt_feedback}")
                        return "I apologize, but I cannot provide a response to this query due to safety filters. Please rephrase your question or consult a healthcare professional directly."
                    else:
                        return "I apologize, but I couldn't generate a response. Please try again or rephrase your question."
                
                return response.text
                
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
        
        patient_context = f"Patient: {patient_info.get('age')} years old, {patient_info.get('gender')}"
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


def get_gemini_client() -> Optional[GeminiAPI]:
    """Factory function to get Gemini API client with error handling"""
    try:
        return GeminiAPI()
    except Exception as e:
        logger.error(f"Failed to initialize Gemini API: {str(e)}")
        return None
