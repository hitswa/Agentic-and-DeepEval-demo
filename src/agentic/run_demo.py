from __future__ import annotations

# CLI entry point for running the AutoGen demo tasks outside of the evaluation suite.
# Runs the agent(s), captures the AgentRunTrace, and writes a JSON file per task
# to the specified output directory for manual inspection.

import argparse
import json
from pathlib import Path

from evaluations.fixtures import ALL_TASKS, MULTI_TASK, SINGLE_TASK

from .agents import run_multi_task, run_single_task


def _trace_to_dict(trace) -> dict:
    """Serialise an AgentRunTrace to a plain dict suitable for JSON output."""
    return {
        "task": trace.task,
        "plan": trace.plan,
        "steps": trace.steps,
        "output": trace.output,
        "expected_output": trace.expected_output,
        "tools_called": [
            {
                "name": tool.name,
                "input_parameters": tool.input_parameters,
                "output": tool.output,
                "description": tool.description,
            }
            for tool in trace.tools_called
        ],
        "expected_tools": [
            {
                "name": tool.name,
                "input_parameters": tool.input_parameters,
                "output": tool.output,
                "description": tool.description,
            }
            for tool in trace.expected_tools
        ],
    }


def main() -> None:
    """Parse CLI arguments, run the selected task(s), and write trace JSON files."""
    parser = argparse.ArgumentParser(description="Run AutoGen demo tasks.")
    parser.add_argument(
        "--mode",
        choices=["single", "multi", "all"],
        default="all",
        help="Which demo to run.",
    )
    parser.add_argument(
        "--output-dir",
        default="evaluations/outputs",
        help="Directory to store trace output JSON.",
    )
    args = parser.parse_args()

    # Create the output directory if it doesn't already exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    runs = []
    # Run the selected task(s) and collect (mode_name, trace) pairs
    if args.mode in ("single", "all"):
        trace = run_single_task(SINGLE_TASK.prompt, SINGLE_TASK.expected_output)
        runs.append(("single", trace))
    if args.mode in ("multi", "all"):
        trace = run_multi_task(MULTI_TASK.prompt, MULTI_TASK.expected_output)
        runs.append(("multi", trace))

    # Write one JSON file per task run
    for mode, trace in runs:
        output_path = output_dir / f"{mode}_trace.json"
        output_path.write_text(json.dumps(_trace_to_dict(trace), indent=2))
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
