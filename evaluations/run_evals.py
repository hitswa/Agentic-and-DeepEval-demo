from __future__ import annotations

# Evaluation runner for the DeepEval demo.
#
# Two evaluation passes are performed:
#   1. run_trace_metrics() — scores the full agent trace (plan, steps) using
#      TaskCompletion, StepEfficiency, PlanQuality, and PlanAdherence metrics.
#   2. run_tool_metrics()  — scores individual tool calls using
#      ToolCorrectness and ArgumentCorrectness metrics.

import os

from dotenv import load_dotenv

# Route DeepEval's internal OpenAI calls (LLM-as-judge metrics) through the
# Azure OpenAI endpoint.  Must be done before importing deepeval metrics.
load_dotenv()
os.environ.setdefault("OPENAI_API_KEY", os.getenv("AZURE_OPENAI_API_KEY", ""))
_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
if _endpoint:
    os.environ.setdefault("OPENAI_BASE_URL", f"{_endpoint}/openai/v1/")

from typing import List

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import (
    ArgumentCorrectnessMetric,
    PlanAdherenceMetric,
    PlanQualityMetric,
    StepEfficiencyMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.test_case import LLMTestCase, ToolCall

from agentic.agents import run_multi_task, run_single_task
from agentic.trace import AgentRunTrace

from .fixtures import ALL_TASKS, MULTI_TASK, SINGLE_TASK


def _tool_calls(tool_calls: List[ToolCall]) -> List[ToolCall]:
    """Re-build a list of ToolCall objects to ensure all fields are explicitly set.

    DeepEval metrics expect ToolCall objects with all attributes present.
    This helper normalises any partially-populated ToolCall coming from a trace.
    """
    return [
        ToolCall(
            name=tool.name,
            description=tool.description,
            reasoning=tool.reasoning,
            input_parameters=tool.input_parameters,
            output=tool.output,
        )
        for tool in tool_calls
    ]


def _build_test_case(trace: AgentRunTrace) -> LLMTestCase:
    """Convert an AgentRunTrace into a DeepEval LLMTestCase for tool-level metrics.

    LLMTestCase is the standard input format for DeepEval metrics that evaluate
    individual tool calls (ToolCorrectness, ArgumentCorrectness).
    """
    return LLMTestCase(
        input=trace.task,
        actual_output=trace.output or "",
        expected_output=trace.expected_output,
        tools_called=_tool_calls(trace.tools_called_for_eval()),
        expected_tools=_tool_calls(trace.expected_tools_for_eval()),
    )


def run_trace_metrics() -> List[AgentRunTrace]:
    """Run both agent tasks and evaluate them with trace-level DeepEval metrics.

    Builds an EvaluationDataset from the Golden fixtures, iterates over each
    dataset entry (which triggers DeepEval's tracing context), runs the matching
    agent function, and returns the collected traces for further evaluation.

    Returns:
        List of AgentRunTrace objects (one per Golden) with trace data populated.
    """
    # Build the evaluation dataset from the predefined Golden fixtures
    dataset = EvaluationDataset(
        goldens=[
            Golden(
                input=SINGLE_TASK.prompt,
                expected_output=SINGLE_TASK.expected_output,
                expected_tools=SINGLE_TASK.expected_tools,
            ),
            Golden(
                input=MULTI_TASK.prompt,
                expected_output=MULTI_TASK.expected_output,
                expected_tools=MULTI_TASK.expected_tools,
            ),
        ]
    )

    # Trace-level metrics that score the overall agent behaviour
    metrics = [
        TaskCompletionMetric(),   # Did the agent successfully complete the task?
        StepEfficiencyMetric(),   # Did the agent avoid unnecessary steps?
        PlanQualityMetric(),      # Was the stated plan coherent and sensible?
        PlanAdherenceMetric(),    # Did execution match the plan?
    ]

    traces: List[AgentRunTrace] = []
    # evals_iterator sets up the DeepEval tracing context for each Golden
    for golden in dataset.evals_iterator(metrics=metrics):
        # Route each Golden to the correct agent function based on its prompt
        if golden.input == SINGLE_TASK.prompt:
            trace = run_single_task(golden.input, expected_output=golden.expected_output)
        else:
            trace = run_multi_task(golden.input, expected_output=golden.expected_output)
        traces.append(trace)
    return traces


def run_tool_metrics(traces: List[AgentRunTrace]) -> None:
    """Score each trace's tool calls using ToolCorrectness and ArgumentCorrectness.

    Converts each AgentRunTrace to an LLMTestCase, then runs tool-level metrics
    and prints scores and reasons to stdout.

    Args:
        traces: List of traces produced by run_trace_metrics().
    """
    # Tool-level metrics that check which tools were called and with what arguments
    tool_metrics = [
        ToolCorrectnessMetric(),      # Were the correct tools invoked?
        ArgumentCorrectnessMetric(),  # Were the correct arguments passed?
    ]

    for trace in traces:
        test_case = _build_test_case(trace)
        print(f"\nTool metrics for: {trace.task}")
        for metric in tool_metrics:
            metric.measure(test_case)
            print(
                f"- {metric.__class__.__name__}: score={metric.score} "
                f"passed={metric.is_successful()}"
            )
            if metric.reason:
                print(f"  reason: {metric.reason}")


def main() -> None:
    """Entry point: run trace metrics first, then tool metrics on the collected traces."""
    print("Running trace metrics...")
    traces = run_trace_metrics()
    print("Trace metrics complete.")
    run_tool_metrics(traces)


if __name__ == "__main__":
    main()
