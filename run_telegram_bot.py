#!/usr/bin/env python3
"""
Run the Theo-AI Telegram bot.

This script starts the Telegram bot for local testing and development.
"""
import os
import subprocess
import sys
from pathlib import Path

def check_env_file():
    """
    Check if .env file exists and contains required variables.
    """
    if not os.path.exists(".env"):
        print("Error: .env file not found. Please create one from .env.example")
        return False
    
    # Check for TELEGRAM_BOT_TOKEN
    with open(".env", "r") as f:
        content = f.read()
        if "TELEGRAM_BOT_TOKEN=" not in content or "your_telegram_bot_token_here" in content:
            print("Error: TELEGRAM_BOT_TOKEN not properly configured in .env file")
            return False
    
    return True

def start_telegram_bot():
    """
    Start the Telegram bot.
    """
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Start the Telegram bot
    try:
        print("Starting Theo-AI Telegram bot...")
        subprocess.run([sys.executable, "-m", "telegram.bot"], check=True)
    except KeyboardInterrupt:
        print("\nTelegram bot stopped by user")
    except Exception as e:
        print(f"Error starting Telegram bot: {str(e)}")

def main():
    """
    Main entry point.
    """
    # Check if .env file exists and is properly configured
    if not check_env_file():
        return
    
    # Start Telegram bot
    start_telegram_bot()

if __name__ == "__main__":
    main() 