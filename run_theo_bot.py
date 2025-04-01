#!/usr/bin/env python3
"""
Run the Theo-AI Telegram bot.

This script starts the Telegram bot using the theo_telegram module.
"""
import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("run_theo_bot")

def check_env_file():
    """
    Check if .env file exists and contains required variables.
    """
    if not os.path.exists(".env"):
        logger.error("Error: .env file not found. Please create one from .env.example")
        return False
    
    # Check for TELEGRAM_BOT_TOKEN
    with open(".env", "r") as f:
        content = f.read()
        if "TELEGRAM_BOT_TOKEN=" not in content or "your_telegram_bot_token_here" in content:
            logger.error("Error: TELEGRAM_BOT_TOKEN not properly configured in .env file")
            return False
    
    return True

def check_dependencies():
    """
    Check if required dependencies are installed.
    """
    try:
        import telegram
        import telegram.ext
        logger.info("Successfully imported python-telegram-bot")
        return True
    except ImportError:
        logger.error("python-telegram-bot package not found. Install with: pip install python-telegram-bot[ext]>=22.0")
        return False

def main():
    """
    Main entry point.
    """
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Check if .env file exists and is properly configured
    if not check_env_file():
        return

    # Load environment variables
    load_dotenv()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Now import the theo_telegram bot module and run it
    try:
        logger.info("Starting Theo-AI Telegram bot...")
        
        # Import the bot module from our renamed theo_telegram package
        from theo_telegram.bot import main as run_bot
        
        # Run the bot
        run_bot()
        
    except Exception as e:
        logger.error(f"Error running Telegram bot: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 