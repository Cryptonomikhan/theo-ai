#!/usr/bin/env python3
"""
Test script for Formation model integration with agno.

This script tests the Formation model by sending a simple message and printing the response.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path to find the models module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.formation import Formation
from agno.models.message import Message

def main():
    """Main test function."""
    # Check for API key
    api_key = os.environ.get("FORMATION_API_KEY")
    if not api_key:
        print("Error: FORMATION_API_KEY not found in environment variables")
        print("Please set the FORMATION_API_KEY in your .env file")
        return
    
    print("Testing Formation model integration with agno...")
    
    # Initialize the model
    formation_model = Formation(
        id="best-quality",  # Using Formation's intelligent model routing
        api_key=api_key,
        temperature=0.7
    )
    
    # Define a simple message
    messages = [
        Message(role="system", content="You are a helpful assistant for business development professionals."),
        Message(role="user", content="What are the key factors to look for when identifying potential business partnerships?")
    ]
    
    print("\nSending request to Formation model...")
    
    try:
        # Get a response
        response = formation_model.invoke(messages)
        
        # Parse the response
        model_response = formation_model.parse_provider_response(response)
        
        # Print the response
        print("\nResponse from Formation model:")
        print("-" * 50)
        print(model_response.content)
        print("-" * 50)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError testing Formation model: {str(e)}")

if __name__ == "__main__":
    main() 