"""
Configuration utilities for Theo-AI.
"""
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration manager for Theo-AI.
    Handles loading and accessing environment variables.
    """
    
    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        """
        Get an environment variable.
        
        Args:
            key: The name of the environment variable.
            default: Default value if the variable is not found.
            
        Returns:
            The value of the environment variable, or the default if not found.
        """
        return os.environ.get(key, default)
    
    @staticmethod
    def get_required(key: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            key: The name of the environment variable.
            
        Returns:
            The value of the environment variable.
            
        Raises:
            ValueError: If the environment variable is not found.
        """
        value = os.environ.get(key)
        if value is None:
            raise ValueError(f"Required environment variable '{key}' not found")
        return value
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """
        Get an environment variable as a boolean.
        
        Args:
            key: The name of the environment variable.
            default: Default value if the variable is not found.
            
        Returns:
            The value of the environment variable as a boolean.
        """
        value = os.environ.get(key)
        if value is None:
            return default
        return value.lower() in ('true', 'yes', '1', 'y')
    
    @staticmethod
    def get_api_keys() -> Dict[str, str]:
        """
        Get all API keys defined in environment variables.
        
        Returns:
            A dictionary of API keys.
        """
        api_keys = {}
        
        # OpenAI API key
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if openai_api_key:
            api_keys['openai'] = openai_api_key
        
        # Formation API key
        formation_api_key = os.environ.get('FORMATION_API_KEY')
        if formation_api_key:
            api_keys['formation'] = formation_api_key
        
        # Optional third-party API keys
        crunchbase_api_key = os.environ.get('CRUNCHBASE_API_KEY')
        if crunchbase_api_key:
            api_keys['crunchbase'] = crunchbase_api_key
        
        return api_keys

# Constants
API_SECRET_KEY = Config.get_required('API_SECRET_KEY')
OPENAI_API_KEY = Config.get('OPENAI_API_KEY')
FORMATION_API_KEY = Config.get('FORMATION_API_KEY')
TELEGRAM_BOT_TOKEN = Config.get_required('TELEGRAM_BOT_TOKEN')
ENVIRONMENT = Config.get('ENVIRONMENT', 'development')

# Model settings
DEFAULT_MODEL_PROVIDER = Config.get('DEFAULT_MODEL_PROVIDER', 'formation')
DEFAULT_MODEL_ID = Config.get('DEFAULT_MODEL_ID', 'best-quality')

# API Endpoint for Formation Cloud
API_ENDPOINT = Config.get('API_ENDPOINT', 'http://localhost:8000')
if not API_ENDPOINT.endswith('/'):
    API_ENDPOINT += '/'

# Formation API settings
FORMATION_API_BASE_URL = Config.get('FORMATION_API_BASE_URL', 'https://agents.formation.cloud/v1')

# Google Calendar credentials
GOOGLE_CALENDAR_CLIENT_ID = Config.get('GOOGLE_CALENDAR_CLIENT_ID')
GOOGLE_CALENDAR_CLIENT_SECRET = Config.get('GOOGLE_CALENDAR_CLIENT_SECRET')
GOOGLE_CALENDAR_REDIRECT_URI = Config.get('GOOGLE_CALENDAR_REDIRECT_URI') 