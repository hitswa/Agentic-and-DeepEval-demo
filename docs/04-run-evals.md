# Run DeepEval

## 1) Run trace-based metrics

This executes the agent and evaluates:

- Task Completion
- Step Efficiency
- Plan Quality
- Plan Adherence

**macOS / Linux**
```bash
PYTHONPATH=src python -m evaluations.run_evals
```

**Windows (Command Prompt)**
```cmd
set PYTHONPATH=src && python -m evaluations.run_evals
```

**Windows (PowerShell)**
```powershell
$env:PYTHONPATH="src"; python -m evaluations.run_evals
```

## 2) Tool metrics output

After trace metrics, the script prints results for:

- Tool Correctness
- Argument Correctness

Example output:

```
Tool metrics for: Use the calculator tool with expression '12 * 7 + 3' ...
- ToolCorrectnessMetric: score=1.0 passed=True
- ArgumentCorrectnessMetric: score=1.0 passed=True
```

## Troubleshooting

- Ensure `OPENAI_API_KEY` is set in `.env`.
- If tool correctness fails, inspect `evaluations/outputs/*.json` to verify tool args.
