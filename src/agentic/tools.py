from __future__ import annotations

# Tool factory functions for the demo agent.
# Each factory accepts a TraceRecorder so the tool can log its own invocation,
# then returns the actual callable wrapped with DeepEval's @observe decorator.

import ast
import operator
from typing import Callable, Dict

from deepeval.tracing import observe

from .trace import TraceRecorder


# Mapping from AST binary-operator node types to Python operator functions.
# Used by _safe_eval to evaluate arithmetic without calling eval() directly.
_OPS: Dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def _safe_eval(node: ast.AST) -> float:
    """Recursively evaluate a parsed arithmetic AST node.

    Only supports +, -, *, /, ** on numeric constants and unary +/-.
    Raises ValueError for any unsupported construct, preventing code injection.
    """
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        # Recursively evaluate left and right operands, then apply the operator
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        # Handle unary plus/minus (e.g. -5)
        operand = _safe_eval(node.operand)
        return operand if isinstance(node.op, ast.UAdd) else -operand
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        # Base case: a plain numeric literal
        return float(node.value)
    raise ValueError("Unsupported expression.")


def make_calculator(recorder: TraceRecorder):
    """Create a calculator tool bound to the given TraceRecorder.

    The tool parses and safely evaluates a basic arithmetic expression,
    records the call in the recorder, and returns the result as a string.
    """

    @observe(type="tool", description="Evaluate a basic arithmetic expression.")
    def calculator(expression: str) -> str:
        # Parse into an AST to avoid using eval() directly (security)
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed.body)
        # Log the tool invocation so it appears in the DeepEval trace
        recorder.record_tool(
            name="calculator",
            input_parameters={"expression": expression},
            output=result,
            description="Evaluate a basic arithmetic expression.",
        )
        return str(result)

    return calculator


def make_city_info(recorder: TraceRecorder):
    """Create a city_info tool bound to the given TraceRecorder.

    Returns basic facts (country and highlight) for a known city.
    Falls back to "Unknown" values for cities not in the local database.
    """

    # Static in-memory city database (extend this dict to support more cities)
    city_db = {
        "Paris": {"country": "France", "highlight": "Louvre Museum"},
        "Tokyo": {"country": "Japan", "highlight": "Shibuya Crossing"},
    }

    @observe(type="tool", description="Return basic facts about a city.")
    def city_info(city: str) -> str:
        # Look up city; default to Unknown fields if not in the database
        info = city_db.get(city, {"country": "Unknown", "highlight": "Unknown"})
        # Log the tool invocation for tracing / evaluation
        recorder.record_tool(
            name="city_info",
            input_parameters={"city": city},
            output=info,
            description="Return basic facts about a city.",
        )
        return str(info)

    return city_info


def make_budget_estimator(recorder: TraceRecorder):
    """Create a budget_estimator tool bound to the given TraceRecorder.

    Calculates total trip cost as days * daily_budget and logs the call.
    """

    @observe(type="tool", description="Estimate a simple trip budget.")
    def budget_estimator(days: int, daily_budget: int) -> str:
        # Simple multiplication: total cost = number of days × daily spend
        total = days * daily_budget
        # Log the tool invocation for tracing / evaluation
        recorder.record_tool(
            name="budget_estimator",
            input_parameters={"days": days, "daily_budget": daily_budget},
            output={"total_budget": total},
            description="Estimate a simple trip budget.",
        )
        return str({"total_budget": total})

    return budget_estimator
