# tools/lint_checkpoints.py
import ast, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
bad: list[str] = []

def check_file(path: pathlib.Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return

    for node in ast.walk(tree):
        # 1) run_scene_with_options(..., checkpoint=foo())  <-- wrong (call)
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "run_scene_with_options":
            for kw in node.keywords:
                if kw.arg == "checkpoint" and isinstance(kw.value, ast.Call):
                    bad.append(f"{path}:{node.lineno}: checkpoint should be a function reference (use checkpoint=foo)")

        # 2) {"handler": foo()} inside option dicts          <-- wrong (call)
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == "handler" and isinstance(v, ast.Call):
                    lineno = getattr(node, "lineno", getattr(v, "lineno", 1))
                    bad.append(f"{path}:{lineno}: option.handler should be a function reference (use handler=foo)")

if __name__ == "__main__":
    for py in ROOT.rglob("*.py"):
        p = str(py)
        if "/.venv/" in p or "/.git/" in p:
            continue
        check_file(py)
    if bad:
        print("\n".join(bad))
        sys.exit(1)
