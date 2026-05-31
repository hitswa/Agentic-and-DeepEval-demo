# Agentic DeepEval Demo (AutoGen)

This project demonstrates a small AutoGen-based agentic workflow and evaluates it
using DeepEval agentic metrics (task completion, tool correctness, plan adherence,
plan quality, step efficiency, and argument correctness).

## Quickstart

1. Create and activate a Python venv.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.

Run the demo tasks:

```bash
python -m agentic.run_demo --mode all
```

Run DeepEval metrics:

```bash
python -m evaluations.run_evals
```

## Project Layout

- `src/agentic/` AutoGen agents, tools, and trace helpers.
- `evaluations/` DeepEval evaluation scripts and fixtures.
- `templates/` Standalone reference examples (AutoGen, tracing, DeepEval).
- `docs/` Step-by-step documentation.

## Notes

- AutoGen is installed from the `ag2` package but imported as `autogen`.
- DeepEval metrics require LLM access. Make sure your API key is set.
