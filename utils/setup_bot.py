#!/usr/bin/env python3
"""
Utility script to set up and configure a Telegram bot for Theo-AI.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from theo.utils.telegram import BotManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default bot description
DEFAULT_DESCRIPTION = """
Theo-AI is your intelligent business development assistant. I help research companies, 
identify synergies, and schedule meetings right here in your Telegram chat.

I can:
• Research companies and individuals
• Identify potential business synergies
• Schedule calls via Google Calendar
• Assist with partnership opportunities

Just chat naturally in the group, and I'll help when relevant!
""".strip()

DEFAULT_SHORT_DESCRIPTION = "AI-powered business development assistant for enterprise teams"

def setup_bot(token: str, webhook_url: str = None, env_file: str = ".env") -> None:
    """Set up and configure a Telegram bot for Theo-AI.
    
    Args:
        token: Telegram bot token
        webhook_url: Optional webhook URL for production deployment
        env_file: Path to environment file to update
    """
    try:
        bot = BotManager(token)
        
        # 1. Set up commands
        logger.info("Setting up bot commands...")
        bot.setup_commands()
        
        # 2. Set descriptions
        logger.info("Setting bot description...")
        bot.set_description(DEFAULT_DESCRIPTION)
        bot.set_short_description(DEFAULT_SHORT_DESCRIPTION)
        
        # 3. Configure webhook if URL provided, otherwise use polling
        if webhook_url:
            logger.info(f"Setting up webhook at {webhook_url}...")
            bot.setup_webhook(webhook_url)
        else:
            logger.info("No webhook URL provided, bot will use polling mode")
            bot.remove_webhook()
            
        # 4. Update environment file
        if env_file:
            update_env_file(env_file, token, webhook_url)
            
        logger.info("Bot setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error setting up bot: {e}")
        sys.exit(1)

def update_env_file(env_file: str, token: str, webhook_url: str = None) -> None:
    """Update or create environment file with bot configuration.
    
    Args:
        env_file: Path to environment file
        token: Telegram bot token
        webhook_url: Optional webhook URL
    """
    env_path = Path(env_file)
    
    # Read existing env file if it exists
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    # Update with new values
    env_vars['TELEGRAM_BOT_TOKEN'] = token
    if webhook_url:
        env_vars['WEBHOOK_URL'] = webhook_url
    
    # Write updated env file
    with open(env_path, 'w') as f:
        for key, value in sorted(env_vars.items()):
            f.write(f'{key}={value}\n')
    
    logger.info(f"Updated environment file: {env_file}")

def main():
    parser = argparse.ArgumentParser(description="Set up a Telegram bot for Theo-AI")
    parser.add_argument('--token', required=True, help="Telegram bot token from BotFather")
    parser.add_argument('--webhook-url', help="Webhook URL for production deployment")
    parser.add_argument('--env-file', default=".env", help="Path to environment file")
    
    args = parser.parse_args()
    setup_bot(args.token, args.webhook_url, args.env_file)

if __name__ == '__main__':
    main() 