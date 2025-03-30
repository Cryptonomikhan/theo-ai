"""
Theo-AI Agent Module

This module defines the main agno-based agent for Theo-AI.
The agent integrates web search, web scraping, and scheduling capabilities
to assist with business development tasks.
"""
from typing import List, Dict, Any, Optional
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.langchain import WebBrowserTools
from agno.tools.googlecalendar import GoogleCalendarTools
from agno.tools.telegram import TelegramTools

from models.formation import Formation, FormationChat
from utils.config import (
    OPENAI_API_KEY, 
    FORMATION_API_KEY,
    TELEGRAM_BOT_TOKEN, 
    DEFAULT_MODEL_PROVIDER,
    DEFAULT_MODEL_ID,
    FORMATION_API_BASE_URL
)
from utils.logging_utils import setup_logger

# Configure logging
logger = setup_logger("theo_agent", "theo_agent.log")

class TheoAgent:
    """
    Theo-AI agent built on the agno framework.
    Provides business development research and assistance in Telegram group chats.
    """
    
    def __init__(
        self, 
        model_provider: Optional[str] = None, 
        model_id: Optional[str] = None, 
        chat_id: Optional[str] = None
    ):
        """
        Initialize the Theo-AI agent.
        
        Args:
            model_provider: AI model provider ('formation', 'openai', etc.)
            model_id: ID of the AI model to use
            chat_id: Telegram chat ID to send messages to
        """
        self.model_provider = model_provider or DEFAULT_MODEL_PROVIDER
        self.model_id = model_id or DEFAULT_MODEL_ID
        self.chat_id = chat_id
        
        # Initialize the agent
        try:
            # Set up model based on provider
            if self.model_provider == 'formation':
                if not FORMATION_API_KEY:
                    raise ValueError("Formation API key is required for Formation models")
                
                model = Formation(
                    id=self.model_id,
                    api_key=FORMATION_API_KEY,
                    base_url=FORMATION_API_BASE_URL
                )
                logger.info(f"Using Formation model: {self.model_id}")
            elif self.model_provider == 'openai':
                if not OPENAI_API_KEY:
                    raise ValueError("OpenAI API key is required for OpenAI models")
                
                model = OpenAIChat(
                    id=self.model_id,
                    api_key=OPENAI_API_KEY
                )
                logger.info(f"Using OpenAI model: {self.model_id}")
            else:
                raise ValueError(f"Unsupported model provider: {self.model_provider}")
            
            # Set up tools
            tools = [
                DuckDuckGoTools(),  # Web search
                WebBrowserTools(),   # Web browser/scraping
            ]
            
            # Add Google Calendar Tools if credentials file exists
            if os.path.exists('credentials.json'):
                tools.append(GoogleCalendarTools(credentials_path="credentials.json"))
            
            # Add Telegram Tools if chat_id is provided
            if chat_id and TELEGRAM_BOT_TOKEN:
                tools.append(TelegramTools(token=TELEGRAM_BOT_TOKEN, chat_id=chat_id))
            
            # Create agent with the specified model
            self.agent = Agent(
                model=model,
                tools=tools,
                markdown=True,
                show_tool_calls=True,
                instructions=[
                    """
                    You are Theo-AI, a professional business development research assistant.
                    You help identify partnership opportunities and business synergies by researching 
                    companies and individuals mentioned in conversations.
                    
                    Always maintain a professional, courteous, and focused tone suitable for business development.
                    
                    When you need information, use your web search and web browser tools to gather data about:
                    - Company backgrounds, products, and funding rounds
                    - Key personnel and their professional backgrounds
                    - Potential synergies and partnership opportunities
                    
                    If calendar scheduling is mentioned, help schedule calls using the Google Calendar integration.
                    """
                ]
            )
            
            logger.info(f"Theo-AI agent initialized with {self.model_provider} model {self.model_id}")
        except Exception as e:
            logger.error(f"Error initializing Theo-AI agent: {str(e)}")
            raise
    
    def process_message(self, chat_context: List[Dict[str, str]], system_prompt: str) -> str:
        """
        Process a message from the Telegram chat.
        
        Args:
            chat_context: List of messages in the chat, formatted as [{"party": "...", "message": "..."}]
            system_prompt: System prompt containing rules and reasoning steps
            
        Returns:
            The agent's response
        """
        try:
            # Format the chat context for the agent
            formatted_context = self._format_chat_context(chat_context)
            
            # Get agent's response
            response = self.agent.get_response(
                formatted_context,
                system_prompt=system_prompt
            )
            
            logger.info(f"Agent response generated successfully")
            return response
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(error_msg)
            return f"I encountered an error while processing your request. Please try again later."
    
    def _format_chat_context(self, chat_context: List[Dict[str, str]]) -> str:
        """
        Format the chat context for the agent.
        
        Args:
            chat_context: List of messages in the chat
            
        Returns:
            Formatted context string
        """
        formatted_messages = []
        for message in chat_context:
            party = message.get("party", "Unknown")
            content = message.get("message", "")
            formatted_messages.append(f"{party}: {content}")
        
        return "\n".join(formatted_messages)

def create_agent(
    model_provider: Optional[str] = None,
    model_id: Optional[str] = None, 
    chat_id: Optional[str] = None
) -> TheoAgent:
    """
    Factory function to create a Theo-AI agent.
    
    Args:
        model_provider: Optional model provider ('formation', 'openai', etc.)
        model_id: Optional model ID to use
        chat_id: Optional Telegram chat ID to send messages to
        
    Returns:
        An initialized TheoAgent instance
    """
    return TheoAgent(
        model_provider=model_provider,
        model_id=model_id,
        chat_id=chat_id
    ) 