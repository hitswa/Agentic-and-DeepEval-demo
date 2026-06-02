# Agent Demo

This demo runs two AutoGen tasks:

1. **Single-step calculator**: uses the `calculator` tool once.
2. **Multi-step trip planner**: calls `city_info` and `budget_estimator`.

## Run all demos

**macOS / Linux**

```bash
PYTHONPATH=src python -m agentic.run_demo --mode all
```

**Windows (Command Prompt)**

```cmd
set PYTHONPATH=src && python -m agentic.run_demo --mode all
```

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH="src"; python -m agentic.run_demo --mode all
```

## Run a single demo

**macOS / Linux**
```bash
PYTHONPATH=src python -m agentic.run_demo --mode single
PYTHONPATH=src python -m agentic.run_demo --mode multi
```

**Windows (Command Prompt)**
```cmd
set PYTHONPATH=src && python -m agentic.run_demo --mode single
set PYTHONPATH=src && python -m agentic.run_demo --mode multi
```

**Windows (PowerShell)**
```powershell
$env:PYTHONPATH="src"; python -m agentic.run_demo --mode single
$env:PYTHONPATH="src"; python -m agentic.run_demo --mode multi
```

## Output traces

Traces are written to `evaluations/outputs/`:

- `single_trace.json`
- `multi_trace.json`

These include the plan, steps, and tool calls captured during the run.
