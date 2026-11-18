
import ast
import operator
from langchain_community.tools import DuckDuckGoSearchRun


# WEB SEARCH TOOL
def web_search(query):
    try:
        search_tool = DuckDuckGoSearchRun()
        result = search_tool.invoke(query)
        return result

    except Exception as error:
        return f"Web search failed: {str(error)}"


# SAFE CALCULATOR TOOL
def calculate(expression):

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def evaluate(node):

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large")

            result = operation(left, right)

            if abs(result) > 10**15:
                raise ValueError("Result is too large")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operator")

            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression")

    try:
        parsed = ast.parse(expression, mode="eval")
        return str(evaluate(parsed.body))

    except Exception as error:
        return f"Calculation error: {str(error)}"


# TOOL ROUTER
def execute_tool(user_input):

    text = user_input.lower().strip()

    if text.startswith("calculate:"):
        expression = user_input.split(":", 1)[1].strip()
        return "Calculator", calculate(expression)

    if text.startswith("search:"):
        query = user_input.split(":", 1)[1].strip()
        return "Web Search", web_search(query)

    return None, None
