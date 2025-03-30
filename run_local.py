#!/usr/bin/env python3
"""
Local development script for Theo-AI.

This script starts the API server for local testing and development.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

def check_env_file():
    """
    Check if .env file exists.
    """
    if not os.path.exists(".env"):
        print("Error: .env file not found. Please create one from .env.example")
        return False
    return True

def start_api_server():
    """
    Start the API server.
    """
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Start the API server
    try:
        print("Starting Theo-AI API server...")
        subprocess.run([sys.executable, "-m", "api.main"], check=True)
    except KeyboardInterrupt:
        print("\nAPI server stopped by user")
    except Exception as e:
        print(f"Error starting API server: {str(e)}")

def main():
    """
    Main entry point.
    """
    # Check if .env file exists
    if not check_env_file():
        return
    
    # Start API server
    start_api_server()

if __name__ == "__main__":
    main() 