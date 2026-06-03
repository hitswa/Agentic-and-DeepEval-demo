from __future__ import annotations

# AutoGen agent definitions for the DeepEval demo.
# Each agent function represents one evaluation scenario (single-tool vs. multi-tool).
# The @observe decorator from DeepEval wraps each function so the framework can
# capture the input, output, and tool calls automatically for metric scoring.

import os
from pathlib import Path
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv

import autogen
from deepeval.tracing import observe, update_current_trace

from .tools import make_budget_estimator, make_calculator, make_city_info
from .trace import AgentRunTrace, ToolTrace, TraceRecorder


def _build_llm_config() -> dict:
    """Load environment variables and return the AutoGen LLM configuration dict.

    Reads the following variables from the .env file or the shell environment:
      OPENAI_API_TYPE        (optional) - defaults to azure.
      AZURE_OPENAI_API_KEY   (required) - Azure OpenAI resource key.
      AZURE_OPENAI_ENDPOINT  (required) - e.g. https://<resource>.openai.azure.com/
      AZURE_OPENAI_DEPLOYMENT (optional) - deployment name, defaults to gpt-4o-mini.
      AZURE_OPENAI_API_VERSION (optional) - API version, defaults to 2025-01-01-preview.

    Raises:
        RuntimeError: If AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT is not set.
    """
    # Load .env from repository root first, then fall back to dotenv's discovery.
    repo_root = Path(__file__).resolve().parents[2]
    env_file = repo_root / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
    else:
        load_dotenv(find_dotenv(), override=True)

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_type = os.getenv("OPENAI_API_TYPE", "azure")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    if not api_key:
        raise RuntimeError(
            "AZURE_OPENAI_API_KEY is required in the environment. "
            f"Expected .env at: {env_file}"
        )
    if not endpoint:
        raise RuntimeError(
            "AZURE_OPENAI_ENDPOINT is required in the environment. "
            f"Expected .env at: {env_file}"
        )
    return {
        "config_list": [
            {
                "model": deployment,
                "api_key": api_key,
                "base_url": endpoint.rstrip("/") + "/",
                "api_type": api_type,
                "api_version": api_version,
            }
        ]
    }


def _build_trace_output(plan: List[str], steps: List[str], final_answer: str) -> str:
    """Format the plan, execution steps, and final answer into a single trace string.

    This string is passed to DeepEval's update_current_trace() as the agent output
    so trace-level metrics (PlanQuality, PlanAdherence, etc.) have structured text to score.
    """
    plan_text = "\n".join(f"- {item}" for item in plan)
    steps_text = "\n".join(f"- {item}" for item in steps)
    return f"Plan:\n{plan_text}\nSteps:\n{steps_text}\nFinalAnswer:\n{final_answer}"


@observe(type="agent", available_tools=["calculator"])
def run_single_task(task: str, expected_output: Optional[str] = None) -> AgentRunTrace:
    """Run the single-tool demo task using an AutoGen assistant + user_proxy pair.

    The agent is expected to call the calculator tool exactly once with the
    arithmetic expression from the prompt and return only the numeric result.

    Args:
        task: The user prompt (e.g. "Use the calculator with '12 * 7 + 3'").
        expected_output: Ground-truth answer used by DeepEval metrics.

    Returns:
        AgentRunTrace containing the full execution record for evaluation.
    """
    # Define the intended plan upfront — used by PlanQuality / PlanAdherence metrics
    plan = ["Use calculator tool with the exact expression provided.", "Return numeric answer only."]
    recorder = TraceRecorder(
        task=task,
        plan=plan,
        expected_tools=[
            ToolTrace(
                name="calculator",
                input_parameters={"expression": "12 * 7 + 3"},
                output=None,
                description="Evaluate a basic arithmetic expression.",
            )
        ],
    )
    recorder.record_step("Start single-step task.")

    llm_config = _build_llm_config()

    # AssistantAgent: the LLM-backed agent that decides which tool to call
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message=(
            "You are a precise assistant. Always use the calculator tool with the exact "
            "expression given by the user. Respond with only the final number."
        ),
    )

    # UserProxyAgent: executes tool calls on behalf of the assistant (no human input)
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config={"use_docker": False},  # Disable Docker for simplicity in this demo
    )

    # Build the calculator tool bound to the current recorder, then register it
    calculator = make_calculator(recorder)
    user_proxy.register_for_execution()(calculator)                           # runs the tool
    assistant.register_for_llm(description="Evaluate arithmetic expressions.")(calculator)  # exposes to LLM

    # Kick off the AutoGen conversation; summary holds the final agent response
    chat_result = user_proxy.initiate_chat(
        assistant,
        message=task,
        summary_method="last_msg",
    )

    final_answer = chat_result.summary
    trace = recorder.finalize(final_answer, expected_output=expected_output)

    # Push structured trace data to DeepEval so trace-level metrics can score it
    trace_output = _build_trace_output(trace.plan, trace.steps, final_answer)
    update_current_trace(
        input=task,
        output=trace_output,
        expected_output=expected_output,
        tools_called=trace.tools_called_for_eval(),
        expected_tools=trace.expected_tools_for_eval(),
        metadata={"task_type": "single"},
    )
    return trace


@observe(type="agent", available_tools=["city_info", "budget_estimator"])
def run_multi_task(task: str, expected_output: Optional[str] = None) -> AgentRunTrace:
    """Run the multi-tool demo task using an AutoGen assistant + user_proxy pair.

    The agent must call city_info (to get city facts) and budget_estimator
    (to compute total cost) in sequence, then summarise both results.

    Args:
        task: The user prompt describing the city and budget parameters.
        expected_output: Ground-truth answer used by DeepEval metrics.

    Returns:
        AgentRunTrace containing the full execution record for evaluation.
    """
    # Three-step plan: city lookup → budget calculation → summary
    plan = [
        "Call city_info with the provided city.",
        "Call budget_estimator with the provided days and daily budget.",
        "Summarize results in one response.",
    ]
    recorder = TraceRecorder(
        task=task,
        plan=plan,
        expected_tools=[
            ToolTrace(
                name="city_info",
                input_parameters={"city": "Paris"},
                output=None,
                description="Return basic facts about a city.",
            ),
            ToolTrace(
                name="budget_estimator",
                input_parameters={"days": 3, "daily_budget": 200},
                output=None,
                description="Estimate a simple trip budget.",
            ),
        ],
    )
    recorder.record_step("Start multi-step task.")

    llm_config = _build_llm_config()

    # AssistantAgent: LLM-backed planner that decides the tool call sequence
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message=(
            "You are a structured trip planner. Follow the exact tool calls required. "
            "Respond with a short summary including city highlight and total budget."
        ),
    )

    # UserProxyAgent: executes tool calls returned by the assistant
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=4,
        code_execution_config={"use_docker": False},  # Disable Docker for simplicity in this demo
    )

    # Build both tools bound to the current recorder, then register them
    city_info = make_city_info(recorder)
    budget_estimator = make_budget_estimator(recorder)
    user_proxy.register_for_execution()(city_info)
    user_proxy.register_for_execution()(budget_estimator)
    assistant.register_for_llm(description="Return basic facts about a city.")(city_info)
    assistant.register_for_llm(description="Estimate a simple trip budget.")(budget_estimator)

    # Kick off the AutoGen conversation; summary holds the final agent response
    chat_result = user_proxy.initiate_chat(
        assistant,
        message=task,
        summary_method="last_msg",
    )

    final_answer = chat_result.summary
    trace = recorder.finalize(final_answer, expected_output=expected_output)

    # Push structured trace data to DeepEval so trace-level metrics can score it
    trace_output = _build_trace_output(trace.plan, trace.steps, final_answer)
    update_current_trace(
        input=task,
        output=trace_output,
        expected_output=expected_output,
        tools_called=trace.tools_called_for_eval(),
        expected_tools=trace.expected_tools_for_eval(),
        metadata={"task_type": "multi"},
    )
    return trace
