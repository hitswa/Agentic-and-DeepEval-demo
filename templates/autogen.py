# Simple AutoGen template demonstrating a basic two-agent conversation.
# This file serves as a standalone reference example — it is NOT part of the
# evaluation pipeline and does not use DeepEval tracing or tools.

import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

# LLM configuration for Azure OpenAI — values are loaded from the .env file
llm_config = {
    "config_list": [
        {
            "model": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/") + "/",
            "api_type": "azure",
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        }
    ]
}

# AssistantAgent: the LLM-backed agent that generates responses
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful assistant."
)

# UserProxyAgent: simulates a human user and initiates the conversation
user = UserProxyAgent(
    name="user",
    human_input_mode="ALWAYS"  # Prompts for real human input at each turn
)

# Start the conversation — the user sends the first message
user.initiate_chat(
    assistant,
    message="Tell me about Agentic AI."
)