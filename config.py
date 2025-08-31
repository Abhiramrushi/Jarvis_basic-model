"""
Configuration file for Adaptive AI Agent
"""

import os
from typing import Dict

# API Configuration
API_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
    "google_credentials_path": os.getenv("GOOGLE_CREDENTIALS_PATH", "path/to/credentials.json"),
    "pinecone_api_key": os.getenv("PINECONE_API_KEY", "your_pinecone_api_key"),
    "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
    "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_sid"),
    "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_token")
}

# Database Configuration
DATABASE_CONFIG = {
    "postgres_url": os.getenv("POSTGRES_URL", "postgresql://localhost/ai_agent"),
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
    "vector_db_name": os.getenv("VECTOR_DB_NAME", "ai_agent_vectors")
}

# Model Configuration
MODEL_CONFIG = {
    "on_device_models": {
        "gemma2_small": {
            "model": "google/gemma-2-2b-it",
            "parameters": "2B",
            "use_case": "Quick responses, privacy-sensitive tasks"
        },
        "llama3_micro": {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "parameters": "8B",
            "use_case": "Balanced performance and privacy"
        },
        "mistral_small": {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "parameters": "7B",
            "use_case": "Good reasoning with moderate resource usage"
        }
    },
    "cloud_models": {
        "gpt4o": {
            "provider": "OpenAI",
            "use_case": "Complex reasoning, code generation, analysis"
        },
        "gpt5": {
            "provider": "OpenAI",
            "use_case": "Advanced reasoning, multimodal tasks"
        },
        "claude_opus": {
            "provider": "Anthropic",
            "use_case": "Long-form content, detailed analysis"
        }
    }
}

# Speech Configuration
SPEECH_CONFIG = {
    "whisper_model": "base",  # Options: tiny, base, small, medium, large
    "tts_voice": "en-US-Neural2-F",
    "language_code": "en-US",
    "audio_encoding": "MP3"
}

# Security Configuration
SECURITY_CONFIG = {
    "encryption_enabled": True,
    "local_storage_path": "./private_data",
    "session_timeout": 3600,  # 1 hour
    "max_request_size": 1048576  # 1MB
}

# Personalization Configuration
PERSONALIZATION_CONFIG = {
    "feedback_buffer_size": 1000,
    "learning_rate": 0.01,
    "preference_update_frequency": 10,  # interactions
    "relevance_threshold": 0.7
}

# System Prompt Template
SYSTEM_PROMPT_TEMPLATE = """You are an adaptive AI assistant designed to learn and adapt to user preferences over time.

CORE CAPABILITIES:
- Process user requests with context awareness
- Learn from user feedback and interactions
- Maintain user privacy and data security
- Provide personalized responses based on user history

USER CONTEXT:
- User ID: {user_id}
- Preferred communication style: {communication_style}
- Common topics: {common_topics}
- Response length preference: {response_length}

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

RESPONSE FORMAT:
- Be concise but helpful
- Match user's preferred communication style
- Include relevant context from user history
- Provide actionable suggestions when appropriate

Current conversation context: {conversation_context}
User's recent interactions: {recent_interactions}
"""

# Integration APIs
INTEGRATION_APIS = {
    "gmail": {
        "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
        "api_name": "gmail",
        "version": "v1"
    },
    "calendar": {
        "scopes": ["https://www.googleapis.com/auth/calendar"],
        "api_name": "calendar",
        "version": "v3"
    },
    "drive": {
        "scopes": ["https://www.googleapis.com/auth/drive.readonly"],
        "api_name": "drive",
        "version": "v3"
    }
}

# Development Configuration
DEV_CONFIG = {
    "debug_mode": os.getenv("DEBUG_MODE", "False").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "test_mode": os.getenv("TEST_MODE", "False").lower() == "true"
}
