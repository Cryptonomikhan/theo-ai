# Theo-AI: Telegram Helper for Enterprise Ops

Theo-AI is a stateless, serverless AI agent built using the agno framework. It's designed to assist with business development research and partnership opportunities in Telegram group chats by gathering information about companies and individuals, identifying synergies, scheduling calls, and collaborating with other agents.

## Features

- **Stateless & Serverless Design**: Theo-AI operates as a stateless agent, with all context managed externally.
- **Telegram Bot Integration**: Seamlessly joins group chats to provide research assistance.
- **Research Capabilities**: Uses web search, web scraping, and API integrations to gather data from company websites, Crunchbase, LinkedIn, etc.
- **Scheduling Integration**: Connects with Google Calendar to schedule calls and meetings.
- **Enterprise-focused**: Specifically designed for business development professionals and startups.
- **Model Flexibility**: Uses Formation Cloud by default for intelligent model routing with "best-x" selection, but also supports OpenAI models.
- **Agno Framework Integration**: Leverages agno's TelegramTools and GoogleCalendarTools for efficient and scalable functionality.

## Tech Stack

- **agno Framework**: Powers the core AI agent with multi-agent capabilities.
- **Python**: Backend implementation language.
- **Formation Cloud**: Primary AI model provider with intelligent routing.
- **Telegram Bot API**: For chat integration via agno's TelegramTools.
- **Google Calendar API**: For scheduling functionality via agno's GoogleCalendarTools.
- **OpenAI Compatible API**: For alternative AI model access.

## Project Structure

```
theo-ai/
├── api/              # API endpoints
├── agents/           # agno agent implementations
├── models/           # Custom model implementations
├── services/         # External service integrations
├── telegram/         # Telegram bot implementation
├── integrations/     # Third-party integrations (Calendar, etc.)
├── utils/            # Helper utilities
└── logs/             # Log files
```

## Deployment Options

Theo-AI supports multiple deployment options to fit different user needs:

### 1. Local/Self-Hosted Deployment (Available Now)

Run your own instance of Theo-AI with full control over configuration:

- **Direct Installation**: Install and run locally on your own machine
- **Docker Deployment**: Use our Docker configurations for containerized deployment
- **Cloud Self-Hosting**: Deploy to your own cloud instances (AWS, GCP, etc.)

See the [Setup and Installation](#setup-and-installation) section below for step-by-step instructions.

### 2. Managed Deployment (Coming Soon)

We're developing a hosted platform that will offer one-click Telegram bot deployments:

- **No Technical Setup**: Simply create an account and configure your bot through our web UI
- **Automatic Updates**: Always get the latest features without manual updates
- **Managed Infrastructure**: We handle hosting, scaling, and monitoring for you
- **Secure Credential Management**: Your API keys and tokens are securely stored and isolated
- **Simple Dashboard**: Monitor and control your bot through an intuitive web interface

Join our [waitlist](#) to get notified when the managed deployment option is available.

## Architecture Overview

Theo-AI follows a frontend/backend architecture:

- **Frontend (Telegram Bot)**: Handles chat interaction, context management, and communication with the backend
- **Backend (Theo-AI Agent)**: Stateless serverless agent that performs the actual processing

This design allows multiple bot instances (frontends) to share a single scalable backend service. When using self-hosted deployment, you need to run both components. Our future managed service will handle this automatically.

## Setup and Installation

### Quick Start (Local Development)

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys (see [Environment Variables](#environment-variables))
6. Set up your Telegram bot (see [Detailed Setup Guide](#detailed-setup-guide))
7. Run the API server: `python run_local.py`
8. Start the Telegram bot: `python run_telegram_bot.py`

### Quick Start (Docker)

1. Clone this repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

For detailed setup instructions, including Telegram bot creation and configuration, see the [Detailed Setup Guide](#detailed-setup-guide) below.

## Detailed Setup Guide

### Setting Up Your Telegram Bot

1. **Create a New Bot with BotFather** (Required One-time Setup)
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` to BotFather
   - Follow the prompts to:
     1. Choose a display name for your bot
     2. Choose a username for your bot (must end in 'bot')
   - BotFather will provide a token - save this as your `TELEGRAM_BOT_TOKEN`

2. **Automated Bot Configuration**
   You can use our utility script to automatically configure the bot:
   ```bash
   python utils/setup_bot.py --token YOUR_BOT_TOKEN
   ```
   This script will:
   - Set up command menu
   - Configure bot description and about text
   - Set up webhook (if using webhook mode)
   - Generate necessary environment variables
   
   Or configure programmatically in your code:
   ```python
   from theo.utils.telegram import BotManager
   
   bot_manager = BotManager(token="YOUR_BOT_TOKEN")
   bot_manager.setup_commands()
   bot_manager.setup_webhook()  # if using webhook mode
   ```

3. **Chat ID Management**
   Our bot automatically handles chat ID management:
   - For direct messages: Automatically captured when a user starts the bot
   - For group chats: Automatically captured when the bot is added
   - Access via the API:
     ```python
     from theo.utils.telegram import get_chat_info
     
     # Get all chats where bot is present
     chats = get_chat_info(token="YOUR_BOT_TOKEN")
     
     # Get specific chat info
     chat_info = get_chat_info(token="YOUR_BOT_TOKEN", chat_id="CHAT_ID")
     ```

4. **Webhook vs Polling**
   Theo supports both webhook and polling modes:
   - **Webhook Mode** (Recommended for Production):
     ```python
     from theo.utils.telegram import setup_webhook
     
     # Setup webhook
     setup_webhook(
         token="YOUR_BOT_TOKEN",
         webhook_url="https://your-domain.com/webhook"
     )
     ```
   - **Polling Mode** (Good for Development):
     ```python
     from theo.utils.telegram import start_polling
     
     # Start polling
     start_polling(token="YOUR_BOT_TOKEN")
     ```

### Running the Bot

Each instance of the Telegram bot needs access to the user's specific AI provider API key (Formation or OpenAI) to authenticate requests sent to the central Theo-AI API.

1.  **Configure User API Key**: Ensure that *your* `FORMATION_API_KEY` or `OPENAI_API_KEY` is correctly set in the `.env` file for the bot instance you are running.
2.  **Start Services**:
    *   **Local**: Run `python run_local.py` (for the central API) in one terminal and `python run_telegram_bot.py` in another.
    *   **Docker**: Run `docker-compose up --build`. Docker Compose will manage both the API and bot services.

**How it Works:**

*   The `run_telegram_bot.py` script reads your API key from the `.env` file.
*   When a message needs processing, the bot sends the chat context *and* your API key (in the `X-User-API-Key` header) to the central Theo-AI API endpoint.
*   The central Theo-AI API uses the key provided in the header to make authenticated calls to the AI model provider (Formation/OpenAI) on your behalf.
*   This ensures the central API remains stateless and doesn't store user keys, while allowing multiple users to securely utilize the shared Theo-AI agent with their own credentials.

### Running with Docker

1. **Prerequisites**
   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. **Configuration**
   Create a `docker-compose.yml` file in your project root:
   ```yaml
   version: '3.8'
   
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       env_file:
         - .env
       command: python run_local.py
       volumes:
         - ./logs:/app/logs
   
     telegram-bot:
       build: .
       env_file:
         - .env
       command: python run_telegram_bot.py
       depends_on:
         - api
       volumes:
         - ./logs:/app/logs
   ```

3. **Build and Run**
   ```bash
   # Build and start services
   docker-compose up --build

   # Run in detached mode
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop services
   docker-compose down
   ```

4. **Environment Variables**
   Create a `.env` file with required variables:
   ```
   # Required
   API_SECRET_KEY=your_secret_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   FORMATION_API_KEY=your_formation_api_key

   # Optional
   DEFAULT_MODEL_PROVIDER=formation
   DEFAULT_MODEL_ID=best-quality
   API_ENDPOINT=http://api:8000  # Use this for Docker
   ```

### Optional: Google Calendar Setup

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Click "Select a project" at the top of the page, then "New Project"
   - Enter a project name (e.g., "Theo AI Calendar") and click "Create"
   - Once created, select your new project from the project selector

2. **Enable the Google Calendar API**
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Google Calendar API" and select it
   - Click "Enable" to activate the API for your project

3. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Select "External" user type (unless you're in a Google Workspace organization)
   - Fill in the required information:
     - App name: "Theo AI"
     - User support email: Your email
     - Developer contact information: Your email
   - Click "Save and Continue"
   - Under "Scopes", add the following scopes:
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/calendar.events`
   - Click "Save and Continue"
   - Add test users (your Google email) if in external mode
   - Click "Save and Continue" to complete the setup

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" and select "OAuth client ID"
   - Application type: "Web application"
   - Name: "Theo AI Calendar Integration"
   - Authorized redirect URIs:
     - For local testing: `http://localhost:8000/google/oauth2callback`
     - For production: Add your production callback URL
   - Click "Create"
   - A popup will display your Client ID and Client Secret - click "Download JSON"
   - Rename the downloaded file to `credentials.json`

5. **Configure Theo-AI Calendar Integration**
   - Place the `credentials.json` file in your project root directory
   - Add the following to your `.env` file:
     ```
     GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
     GOOGLE_CALENDAR_CLIENT_ID=your_client_id_from_credentials
     GOOGLE_CALENDAR_CLIENT_SECRET=your_client_secret_from_credentials
     GOOGLE_CALENDAR_REDIRECT_URI=http://localhost:8000/google/oauth2callback
     ```

6. **First-time Authorization**
   - When running Theo-AI for the first time with Calendar integration enabled, you will be prompted to authorize access
   - A URL will be displayed in the console - open it in your browser
   - Sign in with the Google account whose calendar you want to use
   - Grant the requested permissions
   - You will be redirected to the callback URL and a token will be saved for future use

7. **For Organizations (Google Workspace)**
   - If deploying for an organization, your Google Workspace administrator may need to approve the OAuth consent
   - For internal use, you can select "Internal" user type in the OAuth consent screen which simplifies the approval process
   - For organization-wide deployment, consult your IT department about domain-wide delegation for service accounts

### Troubleshooting Google Calendar

- **Authorization Errors**:
  - Ensure your OAuth consent screen is configured correctly
  - Verify the redirect URI matches exactly what's in your credentials
  - Check if you've authorized the correct Google account
  
- **Quota Errors**:
  - New Google Cloud projects have usage limits
  - If needed, you can request quota increases in the Google Cloud Console

- **"Invalid Client" Errors**:
  - Make sure `credentials.json` is correctly formatted and contains valid credentials
  - Confirm the Client ID and Secret in your `.env` file match what's in Google Cloud Console

- **Token Expiration**:
  - Tokens are refreshed automatically, but if you encounter issues, delete `token.json` and reauthorize

### Verifying the Setup

1. **Check API Server**
   ```bash
   curl http://localhost:8000/status
   ```

2. **Test Telegram Bot**
   - Send `/start` to your bot
   - Bot should respond with welcome message
   - Send `/status` to check API connection

3. **Test Calendar Integration (if configured)**
   - Send a message about scheduling a call
   - Bot should be able to create calendar events

### Troubleshooting

Common issues and solutions:

1. **Bot Not Responding**
   - Check if both API and bot services are running
   - Verify `TELEGRAM_BOT_TOKEN` is correct
   - Ensure bot has proper permissions in group

2. **API Connection Errors**
   - Check if API server is running
   - Verify `API_ENDPOINT` is correct
   - Check network connectivity

3. **Calendar Integration Issues**
   - Verify OAuth credentials
   - Check if `credentials.json` is properly formatted
   - Ensure required scopes are enabled

For more troubleshooting help, check the logs in the `logs/` directory.

## Usage

1. Add your Theo-AI Telegram bot to a group chat.
2. Engage in conversation as normal - Theo-AI listens and processes messages in context.
3. Mention the bot or reply to its messages to get responses.
4. Use the following commands to interact with the bot:
   - `/start` - Start the bot
   - `/help` - Show help information
   - `/status` - Check the API connection status
   - `/model` - View or change the AI model
5. When business development opportunities arise, Theo-AI will:
   - Research companies and individuals mentioned
   - Identify potential synergies
   - Assist with scheduling calls via Google Calendar

## Model Selection

Theo-AI supports different model providers and models:

### Formation Cloud (Default)

Formation Cloud provides intelligent model routing with "best-x" capabilities:

- `best-quality` - Optimal for high-quality, detailed responses
- `best-reasoning` - Excels at complex reasoning tasks
- `best-speed` - Optimized for fast responses
- `best-rag` - Best for retrieval augmented generation tasks

### OpenAI

Theo-AI also supports direct OpenAI models:

- `gpt-4o` - OpenAI's GPT-4o model
- `gpt-4-turbo` - OpenAI's GPT-4 Turbo model

You can change the model provider and model using the `/model` command in the Telegram chat or by setting the `DEFAULT_MODEL_PROVIDER` and `DEFAULT_MODEL_ID` environment variables.

## Environment Variables

Required environment variables:
- `API_SECRET_KEY`: Secret key for API authentication
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- Either `FORMATION_API_KEY` or `OPENAI_API_KEY` depending on your chosen model provider

Optional environment variables:
- `DEFAULT_MODEL_PROVIDER`: Default model provider ('formation' or 'openai')
- `DEFAULT_MODEL_ID`: Default model ID to use
- `FORMATION_API_BASE_URL`: Base URL for Formation API
- `GOOGLE_CALENDAR_CLIENT_ID`: Google Calendar OAuth client ID
- `GOOGLE_CALENDAR_CLIENT_SECRET`: Google Calendar OAuth client secret
- `GOOGLE_CALENDAR_REDIRECT_URI`: Redirect URI for Google Calendar OAuth
- `GOOGLE_CALENDAR_CREDENTIALS_PATH`: Path to Google Calendar credentials JSON file (default: "credentials.json")

## Agno Framework Integration

Theo-AI leverages the agno framework's tools and functionality for optimal performance:

### TelegramTools

The agent uses agno's TelegramTools for direct integration with Telegram, allowing it to:
- Send messages directly to Telegram chats
- Interact seamlessly with the chat context
- Maintain a professional and responsive presence in group conversations

```python
# Example of TelegramTools integration in the agent
tools.append(TelegramTools(
    token=TELEGRAM_BOT_TOKEN,
    chat_id=chat_id
))
```

### GoogleCalendarTools

The agent uses agno's GoogleCalendarTools for efficient calendar operations:
- Create and manage calendar events
- Schedule calls and meetings
- Handle OAuth authentication automatically

```python
# Example of GoogleCalendarTools integration in the agent
tools.append(GoogleCalendarTools(
    credentials_path=GOOGLE_CALENDAR_CREDENTIALS_PATH,
    token_path="./token.json"
))
```

## Deployment

Theo-AI is deployed on [Formation Cloud](https://formation.cloud), a vertically integrated agent and model marketplace.

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t theo-ai .
   ```

2. Test the Docker image locally:
   ```
   docker run -p 8000:8000 --env-file .env theo-ai
   ```

3. For Formation Cloud deployment:
   - Push the Docker image to the Formation Cloud registry
   - Configure the deployment settings in the Formation Cloud dashboard
   - Access your deployed agent at: `agents.formation.cloud/<agent-id>/<version>/<command>`

### Running in Production

In production, the Telegram bot component should be run as a separate process that communicates with the API endpoint. Update the `API_ENDPOINT` variable in `telegram/bot.py` to point to your Formation Cloud endpoint before deploying the bot.

## Future Improvements

Future plans for Theo-AI include:
1. Implementing specialized agents for different tasks (research, scheduling, synthesis)
2. Using agno's Team functionality for better coordination between specialized agents
3. Adding more tools for enhanced business development capabilities

Check the `.cursor/implementation_plan.md` file for detailed future improvement plans.

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the [agno framework](https://docs.agno.com/) for building AI agents
- Built for streamlining business development and research tasks

## Roadmap

In addition to the core features currently available, we're working on:

1. **Hosted Bot Platform** - One-click deployment for non-technical users
2. **Multi-Model Support** - Enhanced model selection and configuration
3. **Long-Term Memory** - Optional storage for extended conversation context
4. **Collaborative Agents** - Teams of specialized agents for different tasks
5. **Advanced Scheduling** - Integration with additional calendar services beyond Google Calendar 