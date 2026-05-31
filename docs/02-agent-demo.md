# Agent Demo

This demo runs two AutoGen tasks:

1. **Single-step calculator**: uses the `calculator` tool once.
2. **Multi-step trip planner**: calls `city_info` and `budget_estimator`.

## Run all demos

```bash
python -m agentic.run_demo --mode all
```

## Run a single demo

```bash
python -m agentic.run_demo --mode single
python -m agentic.run_demo --mode multi
```

## Output traces

Traces are written to `evaluations/outputs/`:

- `single_trace.json`
- `multi_trace.json`

These include the plan, steps, and tool calls captured during the run.
