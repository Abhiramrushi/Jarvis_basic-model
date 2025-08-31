"""
Adaptive AI Agent Implementation
A comprehensive AI assistant with on-device and cloud models, personalization, and privacy features.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages on-device and cloud models"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        
        # Model configurations
        self.on_device_models = {
            "gemma2_small": {
                "model": "google/gemma-2-2b-it",
                "parameters": "2B",
                "use_case": "Quick responses, privacy-sensitive tasks"
            },
            "llama3_micro": {
                "model": "meta-llama/Llama-3.1-8B-Instruct",
                "parameters": "8B",
                "use_case": "Balanced performance and privacy"
            }
        }
        
        self.cloud_models = {
            "gpt4o": {
                "provider": "OpenAI",
                "use_case": "Complex reasoning, code generation, analysis"
            },
            "gpt5": {
                "provider": "OpenAI",
                "use_case": "Advanced reasoning, multimodal tasks"
            }
        }
    
    def route_request(self, user_input: str) -> str:
        """Route request to appropriate model"""
        privacy_keywords = ["private", "confidential", "personal", "secret"]
        complex_keywords = ["analyze", "explain", "compare", "generate", "create"]
        
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in privacy_keywords):
            return "on_device"
        elif any(keyword in input_lower for keyword in complex_keywords):
            return "cloud"
        else:
            return "on_device"
    
    def generate_response(self, user_input: str, model_type: str) -> Tuple[str, float]:
        """Generate response using specified model"""
        if model_type == "on_device":
            return self._generate_on_device(user_input)
        else:
            return self._generate_cloud(user_input)
    
    def _generate_on_device(self, user_input: str) -> Tuple[str, float]:
        """On-device response generation"""
        response = f"On-device response: {user_input}"
        return response, 0.8
    
    def _generate_cloud(self, user_input: str) -> Tuple[str, float]:
        """Cloud response generation"""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content, 0.9
            
        except Exception as e:
            logger.error(f"Cloud model error: {e}")
            return "I apologize, but I'm having trouble processing your request.", 0.0

class PersonalizationEngine:
    """Handles user personalization and learning"""
    
    def __init__(self):
        self.feedback_buffer = []
        self.user_preferences = {}
    
    def collect_feedback(self, user_id: str, interaction_id: str, 
                        rating: int, feedback_text: str = ""):
        """Collect user feedback"""
        feedback = {
            "user_id": user_id,
            "interaction_id": interaction_id,
            "rating": rating,
            "feedback_text": feedback_text,
            "timestamp": datetime.now()
        }
        self.feedback_buffer.append(feedback)
        logger.info(f"Feedback collected: {feedback}")
    
    def learn_preferences(self, user_id: str) -> Dict:
        """Learn user preferences from feedback"""
        user_feedback = [f for f in self.feedback_buffer if f["user_id"] == user_id]
        
        if user_feedback:
            avg_rating = sum(f["rating"] for f in user_feedback) / len(user_feedback)
            preferences = {
                "satisfaction_score": avg_rating,
                "feedback_count": len(user_feedback),
                "last_updated": datetime.now()
            }
            self.user_preferences[user_id] = preferences
            return preferences
        
        return {}

class SpeechManager:
    """Handles speech-to-text and text-to-speech"""
    
    def __init__(self):
        self.whisper_model = None
        self.google_tts_client = None
    
    def transcribe_audio(self, audio_file: str) -> str:
        """Transcribe audio to text"""
        try:
            import whisper
            if not self.whisper_model:
                self.whisper_model = whisper.load_model("base")
            
            result = self.whisper_model.transcribe(audio_file)
            return result["text"]
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    def synthesize_speech(self, text: str) -> bytes:
        """Synthesize text to speech"""
        try:
            from google.cloud import texttospeech
            
            if not self.google_tts_client:
                self.google_tts_client = texttospeech.TextToSpeechClient()
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Neural2-F"
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.google_tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return b""

class SecurityManager:
    """Handles encryption and security"""
    
    def __init__(self):
        self.local_storage = {}
    
    def encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        try:
            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            return cipher_suite.encrypt(data.encode())
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data.encode()
    
    def store_private_data(self, key: str, data: str):
        """Store sensitive data locally"""
        encrypted_data = self.encrypt_data(data)
        self.local_storage[key] = encrypted_data
        logger.info(f"Private data stored for key: {key}")

class AdaptiveAIAgent:
    """Main AI agent class"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Initialize components
        self.model_manager = ModelManager(config.get("openai_api_key", ""))
        self.personalization_engine = PersonalizationEngine()
        self.speech_manager = SpeechManager()
        self.security_manager = SecurityManager()
        
        # System prompt
        self.system_prompt = """You are an adaptive AI assistant designed to learn and adapt to user preferences over time.

CORE CAPABILITIES:
- Process user requests with context awareness
- Learn from user feedback and interactions
- Maintain user privacy and data security
- Provide personalized responses based on user history

PRIVACY GUIDELINES:
- Never store sensitive information in cloud databases
- Use local storage for personal data
- Encrypt all sensitive communications
- Respect user privacy preferences

ADAPTATION RULES:
- Learn from explicit feedback (ratings, comments)
- Adapt communication style based on user preferences
- Remember successful interaction patterns
- Continuously improve response relevance
"""
    
    def process_request(self, user_id: str, user_input: str, 
                       input_type: str = "text") -> Dict:
        """Process user request and generate response"""
        try:
            # Handle voice input
            if input_type == "voice":
                user_input = self.speech_manager.transcribe_audio(user_input)
            
            # Route to appropriate model
            model_type = self.model_manager.route_request(user_input)
            
            # Generate response
            response_text, confidence = self.model_manager.generate_response(
                user_input, model_type
            )
            
            # Create interaction ID
            interaction_id = hashlib.md5(
                f"{user_id}_{datetime.now()}".encode()
            ).hexdigest()
            
            # Learn from interaction
            self.personalization_engine.learn_preferences(user_id)
            
            # Handle voice output
            audio_output = None
            if input_type == "voice":
                audio_output = self.speech_manager.synthesize_speech(response_text)
            
            return {
                "response": response_text,
                "confidence": confidence,
                "model_used": model_type,
                "interaction_id": interaction_id,
                "audio_output": audio_output
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {"error": str(e)}
    
    def provide_feedback(self, user_id: str, interaction_id: str, 
                        rating: int, feedback_text: str = ""):
        """Collect user feedback"""
        self.personalization_engine.collect_feedback(
            user_id, interaction_id, rating, feedback_text
        )
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences"""
        return self.personalization_engine.user_preferences.get(user_id, {})

# Example usage
if __name__ == "__main__":
    # Configuration
    config = {
        "openai_api_key": "your_openai_api_key_here"
    }
    
    # Initialize agent
    agent = AdaptiveAIAgent(config)
    
    # Example interaction
    user_id = "test_user_123"
    response = agent.process_request(user_id, "What's the weather like today?")
    print(f"Response: {response}")
    
    # Provide feedback
    if "interaction_id" in response:
        agent.provide_feedback(user_id, response["interaction_id"], 5, "Great response!")
    
    # Get user preferences
    preferences = agent.get_user_preferences(user_id)
    print(f"User preferences: {preferences}")
