#!/usr/bin/env python3
"""
Test script to verify Agno Agent API functionality.
"""
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main():
    """Test Agno Agent functionality."""
    # Create a basic agent
    agent = Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=OPENAI_API_KEY
        ),
        system_message="You are a helpful assistant that provides concise answers.",
    )
    
    # Test different ways to get responses
    user_message = "Tell me the capital of France."
    
    print("\nTesting agent.response():")
    try:
        response = agent.response(user_message)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error with agent.response(): {str(e)}")
    
    print("\nTesting agent.__call__():")
    try:
        response = agent(user_message)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error with agent.__call__(): {str(e)}")
    
    print("\nTesting print_response (which prints directly):")
    try:
        agent.print_response(user_message)
    except Exception as e:
        print(f"Error with print_response(): {str(e)}")

if __name__ == "__main__":
    main() 