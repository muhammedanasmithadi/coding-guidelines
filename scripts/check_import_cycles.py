"""Fail when Python modules import each other in a cycle."""

from __future__ import annotations

import argparse
import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_PATHS = ("scripts", "src")


def module_name(path: pathlib.Path, root: pathlib.Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def collect_modules(root: pathlib.Path, paths: list[str]) -> dict[str, pathlib.Path]:
    modules: dict[str, pathlib.Path] = {}
    for name in paths:
        base = root / name
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            modules[module_name(path, root)] = path
    return modules


def resolve_relative(current: str, level: int, module: str | None) -> str:
    package = current.rsplit(".", 1)[0] if "." in current else ""
    base = package
    for _ in range(level - 1):
        base = base.rsplit(".", 1)[0] if "." in base else ""
    if module:
        return base + "." + module if base else module
    return base


def imports_of(path: pathlib.Path, current: str) -> set[str]:
    found: set[str] = set()
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return found
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                if node.module:
                    found.add(resolve_relative(current, node.level, node.module))
                else:
                    for alias in node.names:
                        found.add(resolve_relative(current, node.level, alias.name))
            elif node.module:
                found.add(node.module)
    return found


def build_graph(root: pathlib.Path, paths: list[str]) -> dict[str, set[str]]:
    modules = collect_modules(root, paths)
    graph: dict[str, set[str]] = {m: set() for m in modules}
    for module, path in modules.items():
        for imported in imports_of(path, module):
            if imported in modules:
                graph[module].add(imported)
    return graph


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    color = {node: 0 for node in graph}
    parent: dict[str, str | None] = {node: None for node in graph}
    cycles: list[list[str]] = []

    def visit(node: str, stack: list[str]) -> None:
        color[node] = 1
        stack.append(node)
        for neighbor in sorted(graph[node]):
            if color.get(neighbor, 0) == 0:
                parent[neighbor] = node
                visit(neighbor, stack)
            elif color.get(neighbor, 0) == 1:
                idx = stack.index(neighbor)
                cycle = stack[idx:] + [neighbor]
                cycles.append(cycle)
        stack.pop()
        color[node] = 2

    for node in sorted(graph):
        if color[node] == 0:
            visit(node, [])
    unique: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for cycle in cycles:
        key = tuple(sorted(cycle))
        if key in seen:
            continue
        seen.add(key)
        unique.append(cycle)
    return unique


def main(root: pathlib.Path = ROOT, paths: list[str] | None = None) -> int:
    if paths is None:
        paths = [p for p in DEFAULT_PATHS if (root / p).exists()]
    graph = build_graph(root, paths)
    cycles = find_cycles(graph)
    if cycles:
        for cycle in cycles:
            print("import cycle: " + " -> ".join(cycle))
        return 1
    print("import cycles ok")
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
