
# Demo Run Output

This document walks through the terminal output produced by running the two demo
modes and explains what each part means.

---

## Mode: `single` — Single-Step Calculator

**Command**
```bash
PYTHONPATH=src python -m agentic.run_demo --mode single
```

### Step 1 — Task is sent to the assistant

`user_proxy` delivers the task prompt to the `assistant`:

```
user_proxy (to assistant):
Use the calculator tool with expression '12 * 7 + 3' and reply with only the number.
```

> `user_proxy` acts as the task dispatcher. It sends the prompt defined in
> `evaluations/fixtures.py` and never asks for human input
> (`human_input_mode="NEVER"`).

---

### Step 2 — Assistant decides to call a tool

The LLM-backed `assistant` recognises it needs to call the `calculator` tool and
proposes the tool call with the exact expression:

```
assistant (to user_proxy):
***** Suggested tool call: calculator *****
Arguments: {"expression": "12 * 7 + 3"}
```

> The assistant does **not** compute the result itself — it delegates to the
> registered tool, which is the correct agentic behaviour.

---

### Step 3 — Tool executes and returns the result

`user_proxy` runs the function locally and gets back the result:

```
>>>>>>>> EXECUTING FUNCTION calculator...
Input arguments: {'expression': '12 * 7 + 3'}
Output: 87.0
```

> AutoGen logs `EXECUTING` and `EXECUTED` to show the function was called
> successfully. The output `87.0` is the correct answer to `12 × 7 + 3`.

---

### Step 4 — Assistant delivers the final answer

```
assistant (to user_proxy):
87.0
```

> The task is complete. The assistant returned only the number as instructed.

---

### Step 5 — Conversation winds down and terminates

After the answer is delivered, `user_proxy` sends empty follow-up messages
(no further task). The assistant politely asks for input, but there is none.
AutoGen terminates the run once the reply limit is reached:

```
>>>>>>>> TERMINATING RUN: Maximum number of consecutive auto-replies reached
```

> This is expected behaviour — `max_consecutive_auto_reply=3` is the safety
> limit that stops the loop. It does **not** indicate an error.

---

### Step 6 — Trace written to disk

```
Wrote evaluations/outputs/single_trace.json
```

> The full trace (plan, steps, tool calls, arguments, outputs) is saved for
> DeepEval to evaluate in the next step.

---

## Mode: `multi` — Multi-Step Trip Planner

**Command**
```bash
PYTHONPATH=src python -m agentic.run_demo --mode multi
```

### Step 1 — Multi-tool task is sent to the assistant

```
user_proxy (to assistant):
Call city_info with city Paris, then call budget_estimator with days=3 and
daily_budget=200. Reply with a short summary that mentions the city highlight
and the total budget.
```

> This task requires **two** tools to be called, making it a multi-step workflow.

---

### Step 2 — Assistant calls both tools in parallel

The assistant proposes both tool calls in a single turn:

```
***** Suggested tool call: city_info *****
Arguments: {"city": "Paris"}

***** Suggested tool call: budget_estimator *****
Arguments: {"days": 3, "daily_budget": 200}
```

> Calling both tools at once is efficient. The assistant correctly identified
> that neither result depends on the other, so they can run simultaneously.

---

### Step 3 — Both tools execute and return results

```
city_info → {'country': 'France', 'highlight': 'Louvre Museum'}
budget_estimator → {'total_budget': 600}
```

> `city_info` returns structured data about the city.
> `budget_estimator` multiplies `days × daily_budget` to produce the total.

---

### Step 4 — Assistant delivers a synthesised summary

```
assistant (to user_proxy):
Your trip to Paris, known for its highlight, the Louvre Museum, will have a
total budget of $600 for 3 days at a daily expense of $200.
```

> The assistant correctly combined both tool outputs into a coherent natural
> language response — exactly what was asked.

---

### Step 5 — Conversation winds down and terminates

After the summary, `user_proxy` sends empty messages. The assistant attempts
further tool calls into the void before the reply limit stops the loop:

```
>>>>>>>> TERMINATING RUN: Maximum number of consecutive auto-replies reached
```

> Same as the single-step run — this is expected and not an error. The task
> had already completed successfully before this point.

---

### Step 6 — Trace written to disk

```
Wrote evaluations/outputs/multi_trace.json
```

> The multi-step trace captures both tool calls with their arguments and
> outputs, ready for metrics such as Tool Correctness, Argument Correctness,
> and Plan Adherence.

---

## Summary

| Mode | Tools called | Task completed | Trace file |
|---|---|---|---|
| `single` | `calculator` | ✓ Answer: `87.0` | `single_trace.json` |
| `multi` | `city_info`, `budget_estimator` | ✓ Trip summary generated | `multi_trace.json` |

Both runs end with "Maximum number of consecutive auto-replies reached" — this is
normal AutoGen termination behaviour, not a failure. The traces are the input to
`python -m evaluations.run_evals` in the next step.
