"""
Theo-AI API Server

This module implements the API endpoints for Theo-AI using FastAPI.
It handles chat message processing and scheduling requests.
"""
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uvicorn

from agents.theoAgent import create_agent
from utils.config import API_SECRET_KEY, DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL_ID
from utils.logging_utils import setup_logger

# Configure logging
logger = setup_logger("api", "api.log")

# Create FastAPI app
app = FastAPI(
    title="Theo-AI API",
    description="API for Theo-AI, a Telegram Helper for Enterprise Ops",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key security
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify the API key in the request header.
    """
    if api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key

# Define request/response models
class ChatMessage(BaseModel):
    party: str
    message: str

class ChatRequest(BaseModel):
    chatContext: List[ChatMessage]
    systemPrompt: str
    apiKeys: Optional[Dict[str, str]] = None
    modelProvider: Optional[str] = None
    modelId: Optional[str] = None
    chatId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    researchData: Optional[Dict[str, Any]] = None
    schedulingInfo: Optional[Dict[str, Any]] = None
    modelInfo: Optional[Dict[str, str]] = None

class ScheduleRequest(BaseModel):
    summary: str
    description: Optional[str] = ""
    attendees: List[str]
    startTime: str
    endTime: str
    timeZone: Optional[str] = "UTC"

class ScheduleResponse(BaseModel):
    eventId: Optional[str] = None
    eventLink: Optional[str] = None
    message: str
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[Dict[str, Any]] = None

# API endpoints
@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
async def process_chat(request: ChatRequest):
    """
    Process a chat message and return the agent's response.
    """
    try:
        # Convert Pydantic model to dict format expected by agent
        chat_context = [
            {"party": msg.party, "message": msg.message}
            for msg in request.chatContext
        ]
        
        # Log model selection
        model_provider = request.modelProvider or DEFAULT_MODEL_PROVIDER
        model_id = request.modelId or DEFAULT_MODEL_ID
        logger.info(f"Using model provider: {model_provider}, model: {model_id}")
        
        # Create an agent with the specified model
        agent = create_agent(
            model_provider=model_provider,
            model_id=model_id,
            chat_id=request.chatId
        )
        
        # Process the chat context
        response = agent.process_message(chat_context, request.systemPrompt)
        
        # Return the response
        return ChatResponse(
            response=response,
            researchData={},  # Placeholder for future research data
            schedulingInfo={},  # Placeholder for scheduling info
            modelInfo={
                "provider": model_provider,
                "model": model_id
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/models")
async def list_models():
    """
    List available model providers and recommended models.
    """
    return {
        "providers": [
            {
                "id": "formation",
                "name": "Formation Cloud",
                "description": "Formation's managed model hosting with intelligent routing",
                "default": DEFAULT_MODEL_PROVIDER == "formation",
                "models": [
                    {"id": "best-quality", "name": "Best Quality", "description": "Best model for high-quality outputs"},
                    {"id": "best-reasoning", "name": "Best Reasoning", "description": "Best model for complex reasoning tasks"},
                    {"id": "best-speed", "name": "Best Speed", "description": "Best model for fast responses"},
                    {"id": "best-rag", "name": "Best RAG", "description": "Best model for retrieval augmented generation"}
                ]
            },
            {
                "id": "openai",
                "name": "OpenAI",
                "description": "OpenAI's direct models",
                "default": DEFAULT_MODEL_PROVIDER == "openai",
                "models": [
                    {"id": "gpt-4o", "name": "GPT-4o", "description": "OpenAI's GPT-4o model"},
                    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "OpenAI's GPT-4 Turbo model"}
                ]
            }
        ],
        "defaultProvider": DEFAULT_MODEL_PROVIDER,
        "defaultModel": DEFAULT_MODEL_ID
    }

# Add a root endpoint for Formation Cloud
@app.get("/")
async def root():
    """
    Root endpoint that returns basic information about the API.
    """
    return {
        "name": "Theo-AI",
        "description": "A Telegram Helper for Enterprise Ops",
        "version": "1.0.0",
        "status": "online"
    }

# Run the server if executed directly
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True) 