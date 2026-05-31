# Simple DeepEval evaluation template demonstrating how to score an LLM response.
# This file is a standalone reference example — run it directly to see how
# DeepEval metrics evaluate an agent's actual output against the expected output.

from deepeval.metrics import TaskCompletionMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall


# --- Step 1: Define the actual vs. expected data ---
# In a real project this would come from running your agent.

actual_output = "The answer is 10."       # What the agent actually said
expected_output = "The answer is 10."     # Ground-truth correct answer

# Tools the agent actually called during its run
tools_called = [
    ToolCall(
        name="add",
        description="Add two numbers together.",
        input_parameters={"a": 3, "b": 7},
        output=10,
    )
]

# Tools the agent was supposed to call
expected_tools = [
    ToolCall(
        name="add",
        description="Add two numbers together.",
        input_parameters={"a": 3, "b": 7},
    )
]


# --- Step 2: Wrap everything in an LLMTestCase ---
# LLMTestCase is the standard input format for all DeepEval metrics.

test_case = LLMTestCase(
    input="Add 3 and 7, then tell me the result.",
    actual_output=actual_output,
    expected_output=expected_output,
    tools_called=tools_called,
    expected_tools=expected_tools,
)


# --- Step 3: Choose metrics and measure ---
# Each metric scores the test case and exposes .score and .reason.

if __name__ == "__main__":
    metrics = [
        TaskCompletionMetric(),    # Did the agent complete the task correctly?
        ToolCorrectnessMetric(),   # Did the agent call the right tools?
    ]

    for metric in metrics:
        metric.measure(test_case)
        status = "PASSED" if metric.is_successful() else "FAILED"
        print(f"[{status}] {metric.__class__.__name__}: score={metric.score}")
        if metric.reason:
            print(f"        reason: {metric.reason}")
