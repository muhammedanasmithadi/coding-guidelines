from __future__ import annotations

import argparse
import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_PATHS = ("scripts", "src")


def _is_bare_any(node: ast.expr | None) -> bool:
    return isinstance(node, ast.Name) and node.id == "Any"


def scan_file(path: pathlib.Path) -> list[tuple[int, str]]:
    problems: list[tuple[int, str]] = []
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return problems
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if _is_bare_any(node.returns):
            problems.append((node.lineno, f"{node.name}: returns Any"))
        for arg in (
            node.args.posonlyargs
            + node.args.args
            + node.args.kwonlyargs
            + ([node.args.vararg] if node.args.vararg else [])
            + ([node.args.kwarg] if node.args.kwarg else [])
        ):
            if _is_bare_any(arg.annotation):
                msg = f"{node.name}: param {arg.arg} is Any"
                problems.append((arg.lineno or node.lineno, msg))
    return problems


def main(root: pathlib.Path = ROOT, paths: list[str] | None = None) -> int:
    if paths is None:
        paths = [p for p in DEFAULT_PATHS if (root / p).exists()]
    problems: list[str] = []
    for name in paths:
        base = root / name
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            for line, msg in scan_file(path):
                rel = path.relative_to(root).as_posix()
                problems.append(f"{rel}:{line}: {msg}")
    if problems:
        for p in problems:
            print(p)
        return 1
    print("no bare Any at boundaries")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--paths", nargs="*", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    root = pathlib.Path(args.root)
    paths = args.paths if args.paths else None
    sys.exit(main(root, paths))
