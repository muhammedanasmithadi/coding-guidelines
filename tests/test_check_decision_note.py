import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_decision_note import (  # noqa: E402
    has_rationale,
    main,
    watched,
)


def commit(root: pathlib.Path, message: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", message],
        cwd=root,
        check=True,
    )


def repo_with_change(tmp_path: pathlib.Path, path: str) -> pathlib.Path:
    root = tmp_path
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / "seed.txt").write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    commit(root, "seed")
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("y\n")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    commit(root, "change")
    return root


def test_watched_paths() -> None:
    assert watched(["docs/a.md", "README.md"]) == ["docs/a.md"]
    assert watched(["README.md"]) == []
    assert watched(["enforce/python/pyproject.toml"]) == [
        "enforce/python/pyproject.toml"
    ]


def test_rationale_markers() -> None:
    assert has_rationale("Decision: keep /livez")
    assert has_rationale("Rationale: the preset is broken")
    assert has_rationale("see ADR-0008 for the reasoning")
    assert not has_rationale("just a typo fix")


def test_no_rule_paths_passes(tmp_path: pathlib.Path) -> None:
    root = repo_with_change(tmp_path, "README.md")
    assert main("HEAD~1", "HEAD", None, root) == 0


def test_rule_path_without_rationale_fails(tmp_path: pathlib.Path) -> None:
    root = repo_with_change(tmp_path, "docs/a.md")
    body = root / "body.md"
    body.write_text("no rationale here\n")
    assert main("HEAD~1", "HEAD", str(body), root) == 1
    body.write_text("Decision: keep it\n")
    assert main("HEAD~1", "HEAD", str(body), root) == 0
