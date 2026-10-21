import ast
import pathlib
import sys

import hypothesis.strategies as st
from hypothesis import given

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_changelog import needs_changelog  # noqa: E402
from check_import_cycles import module_name  # noqa: E402
from check_no_any import _is_bare_any  # noqa: E402


@given(st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=5))
def test_needs_changelog_consistent(paths: list[str]) -> None:
    watched = ["docs/" + p for p in paths]
    assert needs_changelog(watched) is True
    assert needs_changelog(["scripts/" + p for p in paths]) is False


@given(st.text(alphabet="abc", min_size=1, max_size=10))
def test_module_name_nonempty(name: str) -> None:
    path = pathlib.Path(name + ".py")
    root = pathlib.Path()
    full = root / path
    result = module_name(full, root)
    assert isinstance(result, str)


@given(st.booleans())
def test_is_bare_any_bool(flag: bool) -> None:
    node = ast.Name(id="Any" if flag else "int", ctx=ast.Load())
    assert _is_bare_any(node) is flag
