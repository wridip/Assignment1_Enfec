import ast
import operator

# Supported operators for our safe calculator.
# We limit the operations to prevent potential security vulnerabilities.
OPERATORS = {
    ast.Add: operator.add,      # a + b
    ast.Sub: operator.sub,      # a - b
    ast.Mult: operator.mul,     # a * b
    ast.Div: operator.truediv,  # a / b
    ast.Mod: operator.mod,      # a % b
    ast.Pow: operator.pow,      # a ** b (exponentiation)
}

def safe_eval(node):
    """
    Recursively evaluate nodes of the Abstract Syntax Tree (AST).
    This method is safer than Python's eval() because it only allows 
    predefined math operations and literals.
    """
    # Base case: The node is a constant (a literal number like 5, 3.14, etc.)
    if isinstance(node, ast.Constant):
        return node.value

    # Recursive case: The node is a binary operation (e.g., left + right)
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)

        # Ensure the operator is in our allowlist.
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")

    else:
        # Prevent execution of any other types of Python code (e.g., function calls, imports).
        raise ValueError("Only basic arithmetic is allowed.")


def calculate(expression: str):
    """
    Main entry point for calculating math expressions.
    It parses the string into an AST and evaluates it safely.
    """
    try:
        # Parse the string into a syntax tree in 'eval' mode.
        tree = ast.parse(expression, mode='eval')
        
        # Start the recursive evaluation.
        result = safe_eval(tree.body)
        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        # Detailed error reporting back to the Research agent.
        return {
            "status": "error",
            "message": str(e)
        }
