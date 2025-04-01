"""
Theo-AI Agent Module

This module defines the main agno-based agent for Theo-AI.
The agent integrates web search, web scraping, and scheduling capabilities
to assist with business development tasks.
"""
from typing import List, Dict, Any, Optional
import os
import logging

from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.website import WebsiteTools
from agno.tools.googlecalendar import GoogleCalendarTools
from agno.tools.telegram import TelegramTools

from models.formation import Formation
from utils.config import (
    OPENAI_API_KEY, 
    FORMATION_API_KEY,
    TELEGRAM_BOT_TOKEN, 
    DEFAULT_MODEL_PROVIDER,
    DEFAULT_MODEL_ID,
    FORMATION_API_BASE_URL,
    GOOGLE_CALENDAR_CREDENTIALS_PATH
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
                WebsiteTools(),     # Website content extraction and analysis
            ]
            
            # Add Google Calendar Tools using Agno's native implementation
            # Only if credentials path is configured or exists in the default location
            credentials_path = GOOGLE_CALENDAR_CREDENTIALS_PATH
            if credentials_path and os.path.exists(credentials_path):
                try:
                    tools.append(GoogleCalendarTools(
                        credentials_path=credentials_path,
                        # Store token in a specific location for better tracking
                        token_path="./token.json"
                    ))
                    logger.info("Google Calendar Tools added to agent")
                except Exception as e:
                    logger.error(f"Failed to initialize Google Calendar Tools: {str(e)}")
            
            # Add Telegram Tools if chat_id is provided
            if chat_id and TELEGRAM_BOT_TOKEN:
                try:
                    tools.append(TelegramTools(
                        token=TELEGRAM_BOT_TOKEN,
                        chat_id=chat_id
                    ))
                    logger.info(f"Telegram Tools added for chat ID: {chat_id}")
                except Exception as e:
                    logger.error(f"Failed to initialize Telegram Tools: {str(e)}")
            
            # Create agent with the specified model
            self.agent = Agent(
                model=model,
                tools=tools,
                markdown=True,
                show_tool_calls=True,
                description="""
                You are Theo-AI, a professional business development research assistant.
                You help identify partnership opportunities and business synergies by researching 
                companies and individuals mentioned in conversations.
                
                Always maintain a professional, courteous, and focused tone suitable for business development.
                """,
                instructions=[
                    "When you need information, use your research tools to gather data about company backgrounds, products, and funding rounds",
                    "Research key personnel and their professional backgrounds",
                    "Identify potential synergies and partnership opportunities",
                    "First use DuckDuckGo to search for relevant information, then use the Website tools to extract detailed information",
                    "If calendar scheduling is mentioned, help schedule calls using the Google Calendar integration",
                    "When sending messages to the Telegram chat, use the Telegram tools directly"
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
            
            # Create a new agent with custom system message if needed
            if system_prompt:
                # Temporarily override the system message if needed
                self.agent.system_message = system_prompt
            
            # Get agent's response using the run method
            # This is the standard way to use Agno agents as shown in the documentation and examples
            run_response: RunResponse = self.agent.run(formatted_context)
            
            # Extract the content from the RunResponse
            response = run_response.content if hasattr(run_response, 'content') else str(run_response)
            
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