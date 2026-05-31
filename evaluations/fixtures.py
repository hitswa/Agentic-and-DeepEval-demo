from __future__ import annotations

# Predefined test cases (fixtures) for the DeepEval evaluation suite.
# Each DemoTask bundles a prompt, the expected answer, and the expected tool calls
# so the evaluation harness can compare actual agent behaviour against these targets.

from dataclasses import dataclass
from typing import List

from deepeval.test_case import ToolCall


@dataclass
class DemoTask:
    """Holds all the data needed to run and evaluate a single agent scenario.

    Attributes:
        name: Short identifier for the task (used in logs and output file names).
        prompt: The user message sent to the agent.
        expected_output: The correct final answer the agent should produce.
        expected_tools: The tool calls the agent should make (name + arguments).
    """

    name: str
    prompt: str
    expected_output: str
    expected_tools: List[ToolCall]


# --- Single-tool task ---
# The agent must call the calculator tool exactly once with the given expression.
SINGLE_TASK = DemoTask(
    name="single_calculator",
    prompt="Use the calculator tool with expression '12 * 7 + 3' and reply with only the number.",
    expected_output="87",
    expected_tools=[
        ToolCall(
            name="calculator",
            description="Evaluate a basic arithmetic expression.",
            input_parameters={"expression": "12 * 7 + 3"},
        )
    ],
)

# --- Multi-tool task ---
# The agent must call city_info then budget_estimator and summarise both results.
MULTI_TASK = DemoTask(
    name="multi_trip",
    prompt=(
        "Call city_info with city Paris, then call budget_estimator with days=3 and "
        "daily_budget=200. Reply with a short summary that mentions the city highlight "
        "and the total budget."
    ),
    expected_output="Highlight: Louvre Museum. Total budget: 600.",
    expected_tools=[
        ToolCall(
            name="city_info",
            description="Return basic facts about a city.",
            input_parameters={"city": "Paris"},
        ),
        ToolCall(
            name="budget_estimator",
            description="Estimate a simple trip budget.",
            input_parameters={"days": 3, "daily_budget": 200},
        ),
    ],
)

# Convenience list containing all tasks — used by run_demo.py for batch runs
ALL_TASKS = [SINGLE_TASK, MULTI_TASK]
