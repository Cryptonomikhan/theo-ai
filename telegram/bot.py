"""
Theo-AI Telegram Bot

This module implements the Telegram bot for Theo-AI.
It listens to group chat messages and forwards them to the API endpoint.
"""
import logging
import os
import json
from typing import List, Dict, Any, Optional
import asyncio
import httpx

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from utils.config import (
    TELEGRAM_BOT_TOKEN, 
    API_SECRET_KEY, 
    DEFAULT_MODEL_PROVIDER,
    DEFAULT_MODEL_ID,
    FORMATION_API_KEY,  # Import Formation key
    OPENAI_API_KEY      # Import OpenAI key
)
from utils.logging_utils import setup_logger
from utils.system_prompts import DEFAULT_SYSTEM_PROMPT

# Configure logging
logger = setup_logger("telegram_bot", "telegram_bot.log")

# Define global variables
MAX_CONTEXT_LENGTH = 10  # Max number of messages to include in context

# Get API endpoint from environment or use default
# In production, this should be set to the Formation Cloud endpoint
API_ENDPOINT = os.environ.get(
    "API_ENDPOINT", 
    "http://localhost:8000/chat"
)

if "localhost" not in API_ENDPOINT and not API_ENDPOINT.endswith("/chat"):
    API_ENDPOINT = f"{API_ENDPOINT.rstrip('/')}/chat"

API_BASE_URL = API_ENDPOINT.replace("/chat", "")

logger.info(f"Using API endpoint: {API_ENDPOINT}")

# Store chat contexts
chat_contexts = {}

# Store chat settings
chat_settings = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    """
    await update.message.reply_text(
        "Hello! I'm Theo-AI, your Business Development Research Assistant. "
        "Add me to a group chat to help identify partnership opportunities and business synergies. "
        "I'll research companies, products, and people mentioned in conversations, and can also "
        "help schedule calls using Google Calendar."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.
    """
    await update.message.reply_text(
        "I'm Theo-AI, here to help with business development research!\n\n"
        "Here's what I can do:\n"
        "• Research companies and individuals mentioned in chat\n"
        "• Identify potential business synergies\n"
        "• Help schedule calls via Google Calendar\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/status - Check API connection status\n"
        "/model - View or change the AI model\n\n"
        "Just chat normally - I'll monitor the conversation and provide insights when relevant."
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /status command - reports the current API endpoint and bot status.
    """
    chat_id = str(update.effective_chat.id)
    
    # Get current model settings
    settings = chat_settings.get(chat_id, {})
    model_provider = settings.get("model_provider", DEFAULT_MODEL_PROVIDER)
    model_id = settings.get("model_id", DEFAULT_MODEL_ID)
    
    # Test API connection
    status_message = f"API Endpoint: {API_ENDPOINT}\n"
    status_message += f"Current Model: {model_provider}/{model_id}\n\n"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/health",
                headers={"X-API-Key": API_SECRET_KEY},
                timeout=5.0
            )
            
            if response.status_code == 200:
                status_message += "✅ API is online and responding"
            else:
                status_message += f"❌ API returned status code: {response.status_code}"
    except Exception as e:
        status_message += f"❌ Cannot connect to API: {str(e)}"
    
    await update.message.reply_text(status_message)

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /model command - allows selecting the AI model.
    """
    chat_id = str(update.effective_chat.id)
    
    # Get current model settings
    settings = chat_settings.get(chat_id, {})
    current_provider = settings.get("model_provider", DEFAULT_MODEL_PROVIDER)
    current_model = settings.get("model_id", DEFAULT_MODEL_ID)
    
    try:
        # Get available models
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/models",
                headers={"X-API-Key": API_SECRET_KEY},
                timeout=5.0
            )
            
            if response.status_code != 200:
                await update.message.reply_text(
                    f"❌ Error fetching available models. Status code: {response.status_code}"
                )
                return
                
            models_data = response.json()
            
        # Create model selection keyboard
        keyboard = []
        
        # First, add provider buttons
        provider_row = []
        for provider in models_data.get("providers", []):
            provider_id = provider.get("id")
            provider_name = provider.get("name")
            
            # Mark current provider
            if provider_id == current_provider:
                provider_name = f"✓ {provider_name}"
                
            provider_row.append(
                InlineKeyboardButton(
                    provider_name,
                    callback_data=f"provider:{provider_id}"
                )
            )
            
        keyboard.append(provider_row)
        
        # Add model buttons for current provider
        for provider in models_data.get("providers", []):
            if provider.get("id") == current_provider:
                for model in provider.get("models", []):
                    model_id = model.get("id")
                    model_name = model.get("name")
                    
                    # Mark current model
                    if model_id == current_model:
                        model_name = f"✓ {model_name}"
                        
                    keyboard.append([
                        InlineKeyboardButton(
                            model_name,
                            callback_data=f"model:{model_id}"
                        )
                    ])
        
        # Create inline keyboard markup
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Current model: {current_provider}/{current_model}\n\n"
            "Select a provider or model:",
            reply_markup=reply_markup
        )
            
    except Exception as e:
        logger.error(f"Error in model command: {str(e)}")
        await update.message.reply_text(
            f"❌ Error fetching available models: {str(e)}"
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle inline keyboard button callbacks.
    """
    query = update.callback_query
    await query.answer()
    
    chat_id = str(query.message.chat_id)
    
    # Initialize settings for this chat if not exists
    if chat_id not in chat_settings:
        chat_settings[chat_id] = {
            "model_provider": DEFAULT_MODEL_PROVIDER,
            "model_id": DEFAULT_MODEL_ID
        }
    
    callback_data = query.data
    
    if callback_data.startswith("provider:"):
        # Handle provider selection
        provider = callback_data.split(":", 1)[1]
        chat_settings[chat_id]["model_provider"] = provider
        
        # Update the message to show the new selection
        await model_command(update, context)
        await query.message.delete()
    
    elif callback_data.startswith("model:"):
        # Handle model selection
        model = callback_data.split(":", 1)[1]
        chat_settings[chat_id]["model_id"] = model
        
        # Send confirmation message
        provider = chat_settings[chat_id]["model_provider"]
        await query.message.edit_text(
            f"✅ Model updated to {provider}/{model}"
        )

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Process incoming chat messages, enrich with context, and forward to the AI backend.
    """
    # Ignore messages that are not from a group chat or private chat
    if update.effective_chat.type not in ['group', 'supergroup', 'private']:
        logger.debug(f"Ignoring message from chat type: {update.effective_chat.type}")
        return

    if not update.message or not update.message.text:
        logger.debug("Ignoring non-text message or message without text")
        return

    chat_id = str(update.effective_chat.id)
    user = update.effective_user
    message_text = update.message.text
    message_id = update.message.message_id

    logger.info(f"Processing message {message_id} from chat {chat_id} by user {user.username or user.id}")

    # Initialize context for this chat if not exists
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = []

    # Add current message to context
    chat_contexts[chat_id].append({
        "role": "user" if user else "assistant", # Simple role assignment
        "name": user.username or str(user.id) if user else "bot",
        "content": message_text
    })

    # Trim context if it exceeds max length
    if len(chat_contexts[chat_id]) > MAX_CONTEXT_LENGTH:
        chat_contexts[chat_id] = chat_contexts[chat_id][-MAX_CONTEXT_LENGTH:]

    # Get current model settings for the chat
    settings = chat_settings.get(chat_id, {})
    model_provider = settings.get("model_provider", DEFAULT_MODEL_PROVIDER)
    model_id = settings.get("model_id", DEFAULT_MODEL_ID)
    
    # --- Get User-Specific API Key ---
    user_api_key = None
    if model_provider == 'formation' and FORMATION_API_KEY:
        user_api_key = FORMATION_API_KEY
        logger.debug(f"Using Formation API Key for chat {chat_id}")
    elif model_provider == 'openai' and OPENAI_API_KEY:
        user_api_key = OPENAI_API_KEY
        logger.debug(f"Using OpenAI API Key for chat {chat_id}")
    else:
        logger.warning(f"No API key found for provider '{model_provider}' in chat {chat_id}. Request might fail.")
    # --- End Get User-Specific API Key ---

    # Prepare payload for the central API
    payload = {
        "chat_id": chat_id,
        "messages": chat_contexts[chat_id],
        "system_prompt": DEFAULT_SYSTEM_PROMPT, # TODO: Allow customizing this per chat?
        "model_config": {
            "provider": model_provider,
            "model_id": model_id
        }
        # Note: The central API needs to handle tool usage based on context
    }

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_SECRET_KEY # Secret for the central API itself
    }
    
    # --- Add User-Specific Key to Header ---
    if user_api_key:
        headers["X-User-API-Key"] = user_api_key
    # --- End Add User-Specific Key to Header ---

    # Send request to the central API endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=60.0  # Increased timeout for potentially long AI responses
            )
            response.raise_for_status() # Raise exception for 4xx/5xx errors
            
            response_data = response.json()
            ai_response_content = response_data.get("response")

            if ai_response_content:
                logger.info(f"Received AI response for chat {chat_id}: {ai_response_content[:100]}...")
                # Add AI response to context
                chat_contexts[chat_id].append({
                    "role": "assistant",
                    "name": "theo-ai",
                    "content": ai_response_content
                })
                # Send AI response back to Telegram chat
                await update.message.reply_text(ai_response_content)
            else:
                logger.warning(f"Received empty response from API for chat {chat_id}")
                # Optionally send a message like "I couldn't process that." to the user

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error calling API for chat {chat_id}: {e.response.status_code} - {e.response.text}")
        await update.message.reply_text("Sorry, I encountered an error processing your request.")
    except httpx.RequestError as e:
        logger.error(f"Request error calling API for chat {chat_id}: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't connect to the AI service.")
    except Exception as e:
        logger.exception(f"Unexpected error processing message for chat {chat_id}: {str(e)}")
        await update.message.reply_text("An unexpected error occurred.")

def main() -> None:
    """Start the bot."""
    # Validate required environment variables
    if not TELEGRAM_BOT_TOKEN:
        logger.critical("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        return
    if not API_SECRET_KEY:
        logger.critical("API_SECRET_KEY is not set. Exiting.")
        return
    if not FORMATION_API_KEY and not OPENAI_API_KEY:
        logger.warning("Neither FORMATION_API_KEY nor OPENAI_API_KEY is set. AI requests may fail.")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("model", model_command))
    
    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    
    # Register callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Starting Telegram bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main() 