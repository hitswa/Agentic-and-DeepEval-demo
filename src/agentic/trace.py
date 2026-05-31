from __future__ import annotations

# Tracing data structures used to record what the agent did during a run.
# These objects are later converted into DeepEval's ToolCall format for metric scoring.

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from deepeval.test_case import ToolCall


@dataclass
class ToolTrace:
    """Represents a single tool invocation captured during an agent run.

    Stores the tool name, the arguments passed to it, its output, and
    optional metadata (description and reasoning) needed by DeepEval metrics.
    """

    name: str                            # Name of the tool that was called
    input_parameters: Dict[str, Any]     # Arguments passed to the tool
    output: Any                          # Value returned by the tool
    description: Optional[str] = None   # Human-readable description of the tool
    reasoning: Optional[str] = None     # Why the agent decided to call this tool

    def to_tool_call(self) -> ToolCall:
        """Convert this internal trace record into a DeepEval ToolCall object."""
        return ToolCall(
            name=self.name,
            description=self.description,
            reasoning=self.reasoning,
            input_parameters=self.input_parameters,
            output=self.output,
        )


@dataclass
class AgentRunTrace:
    """Complete record of a single agent run, including its plan, steps, and tool usage.

    This is the final snapshot produced by TraceRecorder.finalize() and is passed
    to DeepEval metrics for scoring.
    """

    task: str                                                      # The original user prompt
    plan: List[str]                                                # Ordered list of planned steps
    steps: List[str]                                               # Steps actually executed at runtime
    tools_called: List[ToolTrace] = field(default_factory=list)    # Tools the agent actually called
    expected_tools: List[ToolTrace] = field(default_factory=list)  # Tools the agent should have called
    output: Optional[str] = None                                   # Final answer produced by the agent
    expected_output: Optional[str] = None                          # Ground-truth expected answer

    def tools_called_for_eval(self) -> List[ToolCall]:
        """Return actually-called tools as DeepEval ToolCall objects for metric scoring."""
        return [tool.to_tool_call() for tool in self.tools_called]

    def expected_tools_for_eval(self) -> List[ToolCall]:
        """Return expected tools as DeepEval ToolCall objects for metric scoring."""
        return [tool.to_tool_call() for tool in self.expected_tools]


class TraceRecorder:
    """Collects tool calls and execution steps during an agent run.

    An instance is created at the start of each agent task. Tools call
    record_tool() when they execute, and the agent calls finalize() at the
    end to produce an immutable AgentRunTrace snapshot.
    """

    def __init__(self, task: str, plan: List[str], expected_tools: List[ToolTrace]) -> None:
        """
        Args:
            task: The user prompt / task description.
            plan: Ordered list of intended steps defined before the agent runs.
            expected_tools: Tools that should be called (used for evaluation).
        """
        self.task = task
        self.plan = plan
        self.expected_tools = expected_tools
        self.tools_called: List[ToolTrace] = []  # Populated as the agent runs
        self.steps: List[str] = []               # Populated as the agent runs

    def record_step(self, step: str) -> None:
        """Append a free-text execution step to the step log."""
        self.steps.append(step)

    def record_tool(
        self,
        name: str,
        input_parameters: Dict[str, Any],
        output: Any,
        description: Optional[str] = None,
        reasoning: Optional[str] = None,
    ) -> None:
        """Record that a tool was called and log a corresponding step entry.

        Args:
            name: Tool name.
            input_parameters: Arguments the tool received.
            output: Value the tool returned.
            description: Optional tool description for DeepEval.
            reasoning: Optional explanation of why the tool was chosen.
        """
        self.tools_called.append(
            ToolTrace(
                name=name,
                input_parameters=input_parameters,
                output=output,
                description=description,
                reasoning=reasoning,
            )
        )
        # Also log the tool call as a step so the full execution trace is in one place
        self.record_step(f"Tool:{name} input={input_parameters}")

    def finalize(self, output: str, expected_output: Optional[str] = None) -> AgentRunTrace:
        """Close the recorder and return the complete AgentRunTrace.

        Args:
            output: The final answer produced by the agent.
            expected_output: Ground-truth answer (optional, used by metrics).

        Returns:
            An immutable AgentRunTrace containing the full run history.
        """
        self.record_step("Responded with final answer.")
        return AgentRunTrace(
            task=self.task,
            plan=self.plan,
            steps=self.steps,
            tools_called=self.tools_called,
            expected_tools=self.expected_tools,
            output=output,
            expected_output=expected_output,
        )
