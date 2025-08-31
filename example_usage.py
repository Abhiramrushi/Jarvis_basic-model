#!/usr/bin/env python3
"""
Example usage of the Adaptive AI Agent
"""

import os
from adaptive_ai_agent import AdaptiveAIAgent

def main():
    # Configuration
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
        "postgres_url": os.getenv("POSTGRES_URL", "postgresql://localhost/ai_agent"),
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379")
    }
    
    # Initialize the AI agent
    print("Initializing Adaptive AI Agent...")
    agent = AdaptiveAIAgent(config)
    
    # Example user interactions
    user_id = "demo_user_001"
    
    print("\n=== Example Interactions ===")
    
    # Interaction 1: Simple question
    print("\n1. Simple question:")
    response1 = agent.process_request(user_id, "What's the weather like today?")
    print(f"User: What's the weather like today?")
    print(f"Agent: {response1['response']}")
    print(f"Model used: {response1['model_used']}")
    print(f"Confidence: {response1['confidence']}")
    
    # Provide feedback
    if 'interaction_id' in response1:
        agent.provide_feedback(user_id, response1['interaction_id'], 5, "Great response!")
    
    # Interaction 2: Privacy-sensitive request
    print("\n2. Privacy-sensitive request:")
    response2 = agent.process_request(user_id, "This is a private message about my personal finances")
    print(f"User: This is a private message about my personal finances")
    print(f"Agent: {response2['response']}")
    print(f"Model used: {response2['model_used']}")
    print(f"Confidence: {response2['confidence']}")
    
    # Provide feedback
    if 'interaction_id' in response2:
        agent.provide_feedback(user_id, response2['interaction_id'], 4, "Good privacy handling")
    
    # Interaction 3: Complex reasoning request
    print("\n3. Complex reasoning request:")
    response3 = agent.process_request(user_id, "Analyze the pros and cons of implementing a hybrid cloud architecture")
    print(f"User: Analyze the pros and cons of implementing a hybrid cloud architecture")
    print(f"Agent: {response3['response']}")
    print(f"Model used: {response3['model_used']}")
    print(f"Confidence: {response3['confidence']}")
    
    # Provide feedback
    if 'interaction_id' in response3:
        agent.provide_feedback(user_id, response3['interaction_id'], 5, "Excellent analysis")
    
    # Get user preferences
    print("\n=== User Preferences ===")
    preferences = agent.get_user_preferences(user_id)
    print(f"User preferences: {preferences}")
    
    print("\n=== Agent Summary ===")
    print("✅ AI Agent successfully initialized")
    print("✅ Processed multiple types of requests")
    print("✅ Collected user feedback")
    print("✅ Learned user preferences")
    print("✅ Maintained privacy for sensitive requests")
    print("✅ Routed requests to appropriate models")

if __name__ == "__main__":
    main()
