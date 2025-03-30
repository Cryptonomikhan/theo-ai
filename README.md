# Theo-AI: Telegram Helper for Enterprise Ops

Theo-AI is a stateless, serverless AI agent built using the agno framework. It's designed to assist with business development research and partnership opportunities in Telegram group chats by gathering information about companies and individuals, identifying synergies, scheduling calls, and collaborating with other agents.

## Features

- **Stateless & Serverless Design**: Theo-AI operates as a stateless agent, with all context managed externally.
- **Telegram Bot Integration**: Seamlessly joins group chats to provide research assistance.
- **Research Capabilities**: Uses web search, web scraping, and API integrations to gather data from company websites, Crunchbase, LinkedIn, etc.
- **Scheduling Integration**: Connects with Google Calendar to schedule calls and meetings.
- **Enterprise-focused**: Specifically designed for business development professionals and startups.
- **Model Flexibility**: Uses Formation Cloud by default for intelligent model routing with "best-x" selection, but also supports OpenAI models.

## Tech Stack

- **agno Framework**: Powers the core AI agent with multi-agent capabilities.
- **Python**: Backend implementation language.
- **Formation Cloud**: Primary AI model provider with intelligent routing.
- **Telegram Bot API**: For chat integration.
- **Google Calendar API**: For scheduling functionality.
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

## Setup and Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys:
   - For Formation Cloud, add your `FORMATION_API_KEY`
   - Alternatively, you can use OpenAI by setting `DEFAULT_MODEL_PROVIDER=openai` and adding your `OPENAI_API_KEY`
6. Set up Google Calendar (optional):
   - Follow the instructions at [https://docs.agno.com/tools/toolkits/googlecalendar](https://docs.agno.com/tools/toolkits/googlecalendar) to set up Google Calendar API access
   - Download the credentials.json file to the project root
7. Set up your Telegram bot:
   - Create a new bot with BotFather on Telegram
   - Get the token and add it to your `.env` file
   - To get your chat ID, send a message to your bot and visit: `https://api.telegram.org/bot<your-token>/getUpdates`
8. Run the API server: `python run_local.py`
9. Start the Telegram bot: `python run_telegram_bot.py`

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

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the [agno framework](https://docs.agno.com/) for building AI agents
- Built for streamlining business development and research tasks 