# DeepEval Metrics Mapping

The demo covers the agentic metrics as mentioned below.

## 1) Task Completion

- **Metric**: `TaskCompletionMetric`
- **Inputs**: user query, expected outcome, actual response
- **Where set**: `update_current_trace(input, output, expected_output)` in `agentic/agents.py`

## 2) Tool Correctness

- **Metric**: `ToolCorrectnessMetric`
- **Inputs**: `tools_called`, `expected_tools`
- **Where set**: `AgentRunTrace.tools_called` and `expected_tools` populated by tool wrappers

## 3) Plan Adherence

- **Metric**: `PlanAdherenceMetric`
- **Inputs**: inferred plan + execution steps
- **Where set**: Plan and steps are embedded in the trace output string for extraction

## 4) Plan Quality

- **Metric**: `PlanQualityMetric`
- **Inputs**: inferred plan + task goal
- **Where set**: Plan text in trace output

## 5) Step Efficiency

- **Metric**: `StepEfficiencyMetric`
- **Inputs**: execution steps vs task goal
- **Where set**: Step list in trace output

## 6) Argument Correctness

- **Metric**: `ArgumentCorrectnessMetric`
- **Inputs**: tool call arguments vs expected arguments
- **Where set**: tool wrappers record args and expected args live in fixtures

## Where the data comes from

- `agentic/tools.py` logs tool usage into a `TraceRecorder`.
- `agentic/agents.py` updates the DeepEval trace with plan/steps/output.
- `evaluations/fixtures.py` defines expected tools and outputs.
