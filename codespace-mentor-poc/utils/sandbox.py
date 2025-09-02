import ast

class UnsafeCodeError(Exception):
    pass

def reject_unsafe_nodes(tree: ast.AST):
    forbidden = (ast.Import, ast.ImportFrom)
    for node in ast.walk(tree):
        if isinstance(node, forbidden):
            raise UnsafeCodeError("Imports are blocked in PoC sandbox.")

def run_in_sandbox(user_code: str) -> dict:
    tree = ast.parse(user_code, mode="exec")
    reject_unsafe_nodes(tree)
    compiled = compile(tree, filename="<user>", mode="exec")
    g = {"__builtins__": {}}
    l = {}
    exec(compiled, g, l)
    return l

def check_exercise(ex, user_code: str) -> tuple[bool, str]:
    try:
        local_vars = run_in_sandbox(user_code)
    except Exception as e:
        return False, f"Error: {e}"

    kind, name = ex["checker"].split(":", 1)

    if kind == "variables":
        if name not in local_vars:
            return False, f"Expected a variable `{name}`."
        return True, "Looks good!"

    if kind == "function":
        if name not in local_vars or not callable(local_vars[name]):
            return False, f"Expected a function `{name}`."
        return True, "Function looks good!"

    return False, "Unknown checker"
