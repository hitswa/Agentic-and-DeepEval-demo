# Agentic DeepEval Demo Plan

## Scope
Build a small Python project that runs one or more AutoGen-based agentic tasks and evaluates them with DeepEval metrics (task completion, tool correctness, plan adherence, plan quality, step efficiency, argument correctness). Provide step-by-step documentation and runnable scripts under a venv.

## Project Structure
- Create a lightweight layout:
  - `src/` for agent implementation and task runners
  - `evaluations/` for DeepEval evaluation scripts
  - `templates/` for standalone reference examples:
    - `autogen.py` — minimal two-agent AutoGen conversation
    - `tracing.py` — simple DeepEval `@observe` tracing example
    - `deepeval.py` — simple `LLMTestCase` + metric evaluation example
  - `docs/` for step-by-step guides and metric explanations
  - `requirements.txt` (or `pyproject.toml`) for dependencies
  - `README.md` for quickstart

## Agentic Task Design
- Use AutoGen agents and tools to keep the agentic flow explicit.
- Implement two demos to cover single and multi-step behavior:
  - **Single-step tool use**: e.g., a simple calculator or file summarizer tool.
  - **Multi-step planner**: a small workflow that plans, executes tools, and returns a final answer.
- Include a structured trace format (plan, steps, tool calls, args, outputs) to feed DeepEval.

## DeepEval Integration
- Add DeepEval dependency and create evaluation wrappers in `evaluations/`.
- Map each metric to the required inputs:
  - Task completion: user query, expected outcome, actual response.
  - Tool correctness: expected tool vs actual tool call; tool response logs.
  - Plan adherence: expected plan/steps vs actual execution steps.
  - Plan quality: generated plan vs task goal.
  - Step efficiency: execution steps vs task goal; time/resource metadata.
  - Argument correctness: expected vs actual tool arguments; tool schema/rules.
- Implement a small fixture dataset for expected vs actual outputs.

## Documentation
- Create multiple markdown files:
  - `docs/01-setup.md` for venv + install steps
  - `docs/02-agent-demo.md` for running single/multi-step tasks
  - `docs/03-deepeval-metrics.md` describing each metric and inputs
  - `docs/04-run-evals.md` for executing evaluations and interpreting results
- Keep docs aligned with code paths and scripts.

## Validation
- Provide a simple `python -m` runner for tasks and for evaluations.
- Ensure commands listed in docs are minimal and consistent.

## Deliverables
- Working Python agent demo
- DeepEval evaluation scripts and sample data
- Multiple markdown docs detailing every step
