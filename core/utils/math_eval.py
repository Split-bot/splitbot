import ast
import operator as op

_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

_MAX_LENGTH = 100


def eval_expr(expr):
    if not expr or len(expr) > _MAX_LENGTH:
        return None
    try:
        return eval_(ast.parse(expr, mode="eval").body)
    except (SyntaxError, TypeError):
        return None


def eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return _OPERATORS[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return _OPERATORS[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)
