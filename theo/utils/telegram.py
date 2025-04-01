"""
Telegram bot management utilities for Theo-AI.
Provides automated configuration and management features for Telegram bots.
"""

import json
import logging
import requests
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class BotManager:
    """Manages Telegram bot configuration and setup.
    
    Handles interactions with the Telegram Bot API.
    """
    
    def __init__(self, token: str):
        """Initialize the bot manager.
        
        Args:
            token: Telegram bot token from BotFather
        """
        if not token:
            raise ValueError("Telegram bot token cannot be empty.")
        self.token = token
        self.api_base = f"https://api.telegram.org/bot{token}/"
        
    def _make_request(self, method: str, data: Optional[Dict] = None) -> Dict:
        """Make a request to the Telegram Bot API.
        
        Args:
            method: API method name (e.g., 'getMe', 'setMyCommands')
            data: Request payload (dictionary)
            
        Returns:
            API response as a dictionary.
            
        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the API response indicates an error.
        """
        url = urljoin(self.api_base, method)
        try:
            response = requests.post(url, json=data) if data else requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            result = response.json()
            if not result.get('ok'):
                error_description = result.get('description', 'Unknown error')
                logger.error(f"Telegram API error for method '{method}': {error_description}")
                raise ValueError(f"Telegram API error: {error_description}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed for method '{method}': {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response for method '{method}': {e}")
            raise ValueError("Invalid JSON response from Telegram API")
    
    def get_me(self) -> Dict:
        """Get basic information about the bot.
        
        Returns:
            Bot information dictionary.
        """
        return self._make_request("getMe")

    def setup_commands(self, commands: Optional[List[Dict[str, str]]] = None) -> Dict:
        """Set up bot commands displayed in the Telegram interface.
        
        Args:
            commands: List of command dictionaries, each with 'command' 
                      (string, lowercase, 1-32 chars, a-z, 0-9, underscores) 
                      and 'description' (string, 3-256 chars).
                      If None, uses default Theo commands.
        
        Returns:
            API response dictionary.
        """
        if commands is None:
            commands = [
                {"command": "start", "description": "Start the bot"},
                {"command": "help", "description": "Show help information"},
                {"command": "status", "description": "Check API connection status"},
                {"command": "model", "description": "View or change AI model"}
            ]
            
        return self._make_request("setMyCommands", {"commands": commands})
    
    def setup_webhook(self, url: str, allowed_updates: Optional[List[str]] = None) -> Dict:
        """Set up a webhook for the bot to receive updates.
        
        Args:
            url: HTTPS URL to send updates to.
            allowed_updates: List of update types to receive (e.g., ["message", "callback_query"]).
                             If None, receives all update types except chat_member.
            
        Returns:
            API response dictionary.
        """
        payload = {"url": url}
        if allowed_updates is not None:
            payload["allowed_updates"] = allowed_updates
            
        return self._make_request("setWebhook", payload)
    
    def remove_webhook(self, drop_pending_updates: bool = False) -> Dict:
        """Remove webhook integration.

        Args:
            drop_pending_updates: Pass True to drop all pending updates.
        
        Returns:
            API response dictionary.
        """
        return self._make_request("deleteWebhook", {"drop_pending_updates": drop_pending_updates})
    
    def get_webhook_info(self) -> Dict:
        """Get current webhook status.
        
        Returns:
            Webhook information dictionary.
        """
        return self._make_request("getWebhookInfo")
    
    def set_description(self, description: str) -> Dict:
        """Set the bot's description (visible in the chat profile).
        
        Args:
            description: New bot description, 0-512 characters.
            
        Returns:
            API response dictionary.
        """
        return self._make_request("setMyDescription", {"description": description})
    
    def set_short_description(self, short_description: str) -> Dict:
        """Set the bot's short description (shown on profile pages).
        
        Args:
            short_description: New short description, 0-120 characters.
            
        Returns:
            API response dictionary.
        """
        return self._make_request("setMyShortDescription", {"short_description": short_description})

def get_chat_info(token: str, chat_id: Union[str, int]) -> Dict:
    """Get information about a specific chat.
    
    Note: Telegram Bot API does not provide a method to list all chats 
    a bot is a member of. You must know the chat_id.
    
    Args:
        token: Telegram bot token.
        chat_id: Unique identifier for the target chat (integer or string).
        
    Returns:
        Chat information dictionary.
        
    Raises:
        ValueError: If chat_id is not provided.
    """
    if not chat_id:
        raise ValueError("chat_id must be provided to get chat information.")
    
    bot = BotManager(token)
    try:
        # The 'result' key contains the chat object
        response = bot._make_request("getChat", {"chat_id": str(chat_id)})
        return response.get('result', {})
    except ValueError as e:
        # Handle cases where the chat might not be found or bot lacks permission
        logger.warning(f"Could not get info for chat_id {chat_id}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error getting info for chat_id {chat_id}: {e}")
        return {}

def setup_webhook_convenience(token: str, webhook_url: str) -> Dict:
    """Convenience function to set up a webhook.
    
    Args:
        token: Telegram bot token.
        webhook_url: HTTPS URL for the webhook.
        
    Returns:
        API response dictionary.
    """
    bot = BotManager(token)
    return bot.setup_webhook(webhook_url)

# Removed start_polling function as it belongs in the main bot execution logic,
# not in a utility module. 