# Simple AutoGen template demonstrating a basic two-agent conversation.
# This file serves as a standalone reference example — it is NOT part of the
# evaluation pipeline and does not use DeepEval tracing or tools.

from autogen import AssistantAgent, UserProxyAgent

# LLM configuration — replace api_key with a real key or load from environment
llm_config = {
    "model": "gpt-4o",
    "api_key": "YOUR_API_KEY"
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