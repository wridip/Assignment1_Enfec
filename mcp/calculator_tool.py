import ast
import operator

# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def safe_eval(node):
    if isinstance(node, ast.Constant):  # numbers
        return node.value

    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)

        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        else:
            raise ValueError("Unsupported operator")

    else:
        raise ValueError("Invalid expression")


def calculate(expression: str):
    try:
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree.body)
        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
