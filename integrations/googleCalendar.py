"""
Google Calendar Integration for Theo-AI.

This module provides functions to interact with the Google Calendar API,
allowing the creation of calendar events for scheduled calls.
"""
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from utils.config import (
    GOOGLE_CALENDAR_CLIENT_ID,
    GOOGLE_CALENDAR_CLIENT_SECRET,
    GOOGLE_CALENDAR_REDIRECT_URI
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/google_calendar.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def create_credentials_file():
    """
    Create a credentials.json file from environment variables.
    This is needed for the OAuth2 flow.
    """
    if not all([GOOGLE_CALENDAR_CLIENT_ID, GOOGLE_CALENDAR_CLIENT_SECRET, GOOGLE_CALENDAR_REDIRECT_URI]):
        logger.error("Missing Google Calendar credentials in environment variables")
        return False
    
    credentials_data = {
        "installed": {
            "client_id": GOOGLE_CALENDAR_CLIENT_ID,
            "project_id": "theo-ai",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": GOOGLE_CALENDAR_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_CALENDAR_REDIRECT_URI]
        }
    }
    
    try:
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials_data, f)
        logger.info("Created credentials.json file")
        return True
    except Exception as e:
        logger.error(f"Error creating credentials.json: {str(e)}")
        return False

def get_calendar_service():
    """
    Get an authenticated Google Calendar service.
    
    Returns:
        A Google Calendar API service object or None if authentication fails.
    """
    creds = None
    
    # Check if token.json exists
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_info(
                json.load(open(TOKEN_FILE))
            )
        except Exception as e:
            logger.error(f"Error loading credentials from token.json: {str(e)}")
    
    # If no valid credentials available, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Error refreshing credentials: {str(e)}")
                return None
        else:
            # Check if credentials.json exists, if not, create it
            if not os.path.exists(CREDENTIALS_FILE):
                if not create_credentials_file():
                    return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logger.error(f"Error during authentication flow: {str(e)}")
                return None
            
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Error building calendar service: {str(e)}")
        return None

def create_calendar_event(
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    attendees: List[str],
    time_zone: str = 'UTC'
) -> Dict[str, Any]:
    """
    Create a Google Calendar event.
    
    Args:
        summary: Title of the event
        description: Description of the event
        start_time: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
        end_time: End time in ISO format (YYYY-MM-DDTHH:MM:SS)
        attendees: List of attendee email addresses
        time_zone: Time zone for the event
    
    Returns:
        A dictionary containing event details or an error message
    """
    try:
        service = get_calendar_service()
        if not service:
            return {"error": "Failed to authenticate with Google Calendar"}
        
        # Format attendees
        attendee_list = [{'email': email} for email in attendees]
        
        # Create event
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': time_zone,
            },
            'attendees': attendee_list,
            'reminders': {
                'useDefault': True
            },
        }
        
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        # Return success response
        return {
            "eventId": created_event['id'],
            "eventLink": created_event.get('htmlLink', ''),
            "message": "Calendar event created successfully"
        }
    
    except Exception as e:
        error_msg = f"Error creating calendar event: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg} 