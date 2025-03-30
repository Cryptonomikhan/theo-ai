# Project Requirements Document (PRD) for Theo-AI

## 1. Project Overview

Theo-AI is a stateless, serverless AI agent built using the open source agno framework. Its primary purpose is to act as a Telegram Helper for Enterprise Ops, designed to join Telegram group chats and assist in business development activities. Theo-AI listens to conversation threads, conducts on-demand research (such as checking company websites, Crunchbase funding rounds, LinkedIn profiles, etc.), and provides actionable insights on potential synergies and business opportunities. In essence, it is an efficient research partner for startups and business development professionals, particularly those active at conferences.

The objective of Theo-AI is to shorten sales and partnership cycles by ensuring that every opportunity is captured and evaluated. By automating basic research and scheduling tasks, Theo-AI helps identify key information like founding teams and market synergies for potential collaborations. The project is driven by the need for a focused, professional, and efficient research assistant that can seamlessly operate in the dynamic environment of a group chat, acting as a catalyst for timely and well-informed business decisions.

## 2. In-Scope vs. Out-of-Scope

**In-Scope:**

*   **API Endpoint for Interaction:** Theo-AI will be accessible via an API endpoint that receives complete chat context (in a "party: message" format) and a system prompt with defined rules and reasoning steps.
*   **Stateless, Serverless Design:** The core AI agent remains stateless, with external components (like the Telegram bot) managing context, state, and conversation history.
*   **Telegram Bot Integration:** Theo-AI will read Telegram group messages, construct responses, and display them in the group chat without requiring explicit commands.
*   **Research & Data Integration:** The agent can use integrated tools for web searching, web scraping, and interactions with external data sources (company websites, Crunchbase, and LinkedIn) to gather data.
*   **Scheduling Integration:** Initial support for scheduling calls using Google Calendar, with future capabilities to integrate additional platforms (e.g., cal.com, Calendly).
*   **Foundational AI Model Usage:** Start with a single AI model (selected by user) that is accessible via any OpenAI compatible API, with future support planned for switching between models.

**Out-of-Scope:**

*   **State Management Within the Agent:** Theo-AI itself remains stateless—the surrounding components are responsible for state and context management.
*   **Advanced Features (Day-1):** Detailed individual dossiers (e.g., hobbies, interests, personal profiles) and direct automated proposal generation are not part of the initial deployment.
*   **Multi-Model Switching:** While future-proof design is included, switching between multiple AI models is not an immediate requirement.
*   **Comprehensive Long-Term Memory:** Any long-term memory or extended context storage (e.g., databases or vector stores) for tracking historical conversations will be considered for later iterations.

## 3. User Flow

A typical interaction begins when a user adds Theo-AI to a Telegram group chat. As the conversation evolves, every message in the chat is captured and packaged into an API call. This call includes the full conversation context formatted in a “party: message” structure and appends a system prompt that reminds Theo-AI of its purpose, operational rules, and detailed reasoning requirements. With all the necessary context bundled in each API request, Theo-AI can perform its research and return actionable insights without holding any internal state.

After Theo-AI processes the API call using the agno framework, its research results (which may include information from public data sources, insights on synergies, and key personnel details) are sent back to the Telegram bot. The Telegram bot, which is responsible for managing the overall conversation state, then posts the AI-generated response directly into the group chat. This workflow ensures that the agent’s responses are timely, contextually aware, and in line with the professional tone required for business development.

## 4. Core Features

*   **API Endpoint Handling:**

    *   Receives full chat context in “party: message” format.
    *   Includes a dedicated system prompt outlining Theo-AI’s purpose, rules, and detailed reasoning steps.

*   **Stateless, Serverless Agent:**

    *   Theo-AI functions without retaining internal state—the surrounding Telegram bot handles conversation history.
    *   Designed to be scalable and easily integrated into serverless environments.

*   **Telegram Bot Integration:**

    *   Reads and processes incoming messages in group chats.
    *   Delivers contextually relevant responses while maintaining a professional and direct tone.
    *   Ensures full conversation context is passed to Theo-AI during each interaction.

*   **External Data Retrieval & Research:**

    *   Uses built-in tools from the agno framework for web search and web scraping.
    *   Gathers data from external sources (company websites, Crunchbase, LinkedIn).
    *   Identifies key business development information such as funding rounds, founding team profiles, and potential synergies.

*   **Authentication and Security:**

    *   API access is secured with robust authentication measures.
    *   Optionally accepts provided API keys for third-party integrations; defaults to public data sources if none are provided.

*   **Scheduling and Calendar Integration:**

    *   Integrates with Google Calendar for scheduling calls.
    *   Built with future adaptability to support additional scheduling tools (e.g., cal.com, Calendly).

*   **Future Extension and Model Flexibility:**

    *   Initially uses a single AI model; designed for future capability to switch between multiple models (accessible via OpenAI compatible APIs).
    *   Lays the groundwork for collaboration with other agents (e.g., proposal generation agents).

## 5. Tech Stack & Tools

*   **Frontend & Messaging:**

    *   Telegram Bot: Manages chat interactions and delivery of messages.

*   **Backend:**

    *   agno Framework: Core framework to build the stateless AI agent.
    *   Serverless Architecture: Deploys as a stateless function accessible via API.
    *   API Authentication Libraries: To secure endpoint access.

*   **AI Models & Integration:**

    *   OpenAI Compatible API: Utilized for AI computations and responses.
    *   Web Search & Web Scraping Tools: To retrieve data from public websites and databases.

*   **Scheduling Integration:**

    *   Google Calendar API: For scheduling and managing calls.
    *   Future integrations for cal.com and Calendly are considered.

*   **Development Tools:**

    *   Cursor IDE: An advanced IDE for AI-powered coding with real-time suggestions which can help improve development efficiency.

## 6. Non-Functional Requirements

*   **Performance:**

    *   Fast response times with minimal latency per API call.
    *   Designed to scale using serverless architecture to handle bursts in message traffic.

*   **Security:**

    *   Robust authentication for API endpoints.
    *   Data privacy and secure handling of any API keys provided by the user.

*   **Usability:**

    *   The system should be intuitive with seamless integration within Telegram.
    *   The responses should maintain a professional, courteous, and focused tone suited for business development.

*   **Compliance:**

    *   Ensure all external integrations abide by data usage policies and third-party API terms.
    *   Maintain data security standards for handling enterprise communication data.

## 7. Constraints & Assumptions

*   **Constraints:**

    *   Theo-AI must remain stateless; all context management is handled externally.
    *   Built on open source agno framework, which necessitates compliance with its design patterns and limitations.
    *   Initial integrations (e.g., scheduling) are limited to Google Calendar, with other platforms slated for future development.
    *   Reliance on OpenAI compatible API; any changes or limitations in the API could affect agent performance.

*   **Assumptions:**

    *   The provided "party: message" formatted chat context is complete and accurate for each API call.
    *   Telegram bots and related middleware will reliably manage state and conversation history.
    *   The environment supports serverless deployments and external API integrations without significant restrictions.
    *   Future enhancements (like long term memory, multi-model support, and advanced research functionalities) are anticipated and can be added incrementally.

## 8. Known Issues & Potential Pitfalls

*   **State Management Reliance:** As Theo-AI is stateless, heavy reliance on external state management by the Telegram bot might introduce synchronization issues. Regular validation of context integrity is recommended.
*   **API Rate Limits:** External API integrations (web search, scraping, Google Calendar) may have rate limits or access restrictions. Implement rate limiting and caching strategies where possible.
*   **Data Accuracy and Availability:** Public data sources may vary in accuracy or be temporarily unavailable. Fallback mechanisms and error handling should be robust.
*   **Security Vulnerabilities:** API authentication must be strict to prevent unauthorized access; using standardized security protocols (e.g., OAuth) is advised.
*   **Integration Complexity:** Multiple tools (web scraping, external APIs) can lead to integration complexity. Modular design and clear error logging will help mitigate these issues.
*   **Scaling Challenges:** Although serverless architecture supports scalability, unexpected load spikes may still present issues. Continuous performance monitoring and auto-scaling configurations are necessary.

This PRD serves as the foundational document for Theo-AI, ensuring that all subsequent technical documents (Tech Stack, Frontend Guidelines, Backend Structure, App Flow, etc.) are generated with absolute clarity and precision. Every detail mentioned herein is designed to ensure that Theo-AI meets its objective of becoming a reliable, professional, and efficient tool for business development research and interaction in group chat environments.
