# Simple DeepEval tracing template demonstrating how to trace an agent and its tools.
# This file is a standalone reference example — run it directly to see how
# @observe captures inputs, outputs, and tool calls into a DeepEval trace.

from deepeval.tracing import observe, update_current_trace


# --- Step 1: Decorate a tool with @observe(type="tool") ---
# DeepEval will automatically record the tool's name, input, and output.

@observe(type="tool", description="Add two numbers together.")
def add(a: int, b: int) -> int:
    return a + b


# --- Step 2: Decorate the agent function with @observe(type="agent") ---
# This creates a parent trace that groups all tool calls made inside it.

@observe(type="agent", available_tools=["add"])
def my_agent(task: str) -> str:
    # Simulate the agent deciding to call the tool
    result = add(3, 7)
    answer = f"The answer is {result}."

    # Step 3: Enrich the trace with structured data for DeepEval metrics
    update_current_trace(
        input=task,
        output=answer,
        expected_output="The answer is 10.",   # Ground-truth for scoring
        metadata={"model": "demo"},
    )

    return answer


# --- Run the agent ---
# DeepEval captures the full trace (agent → tool → output) automatically.
if __name__ == "__main__":
    output = my_agent("Add 3 and 7, then tell me the result.")
    print(output)
    # Expected output: The answer is 10.
    # Check your DeepEval dashboard or logs to see the captured trace.
