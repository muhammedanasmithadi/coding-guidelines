"""Fail when a module imports from a disallowed architectural layer."""

from __future__ import annotations

import argparse
import ast
import pathlib
import sys
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("pyyaml missing: pip install pyyaml")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_NAMES = ("layers.yml", "enforce/layers.yml")


def load_config(root: pathlib.Path) -> dict[str, Any] | None:
    for name in CONFIG_NAMES:
        path = root / name
        if path.exists():
            data = yaml.safe_load(path.read_text())
            if isinstance(data, dict):
                return data
    return None


def layer_of(
    path: pathlib.Path, root: pathlib.Path, config: dict[str, Any]
) -> str | None:
    rel = path.relative_to(root).as_posix()
    for layer in config.get("layers", []):
        prefix = str(layer.get("path", "")).rstrip("/") + "/"
        if rel.startswith(prefix):
            return str(layer.get("name"))
    return None


def imported_layers(path: pathlib.Path, config: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return found
    layers = config.get("layers", [])
    layer_names = {str(item.get("name")) for item in layers}
    layer_paths = {}
    for item in layers:
        name = str(item.get("name"))
        path_value = str(item.get("path", "")).rstrip("/")
        layer_paths[name] = path_value
    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
        for module in modules:
            for name, prefix in layer_paths.items():
                dotted = prefix.replace("/", ".")
                if module == dotted or module.startswith(dotted + "."):
                    found.add(name)
    return found & layer_names


def main(root: pathlib.Path = ROOT) -> int:
    config = load_config(root)
    if config is None:
        print("no layers config, ok")
        return 0
    rules = config.get("rules", {})
    problems: list[str] = []
    for layer in config.get("layers", []):
        base = root / str(layer.get("path", ""))
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            current = str(layer.get("name"))
            allowed = set(rules.get(current, []))
            for imported in imported_layers(path, config):
                if imported != current and imported not in allowed:
                    rel = path.relative_to(root).as_posix()
                    problems.append(f"{rel}: {current} imports {imported}")
    if problems:
        for p in problems:
            print(p)
        return 1
    print("layer boundaries ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
