import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_changelog import main, needs_changelog  # noqa: E402


def _git(root: pathlib.Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def make_repo(tmp: pathlib.Path) -> pathlib.Path:
    _git(tmp, "init", "-q")
    _git(tmp, "config", "user.email", "t@t.com")
    _git(tmp, "config", "user.name", "t")
    (tmp / "docs").mkdir()
    (tmp / "docs" / "a.md").write_text("# A\n")
    (tmp / "CHANGELOG.md").write_text("# changelog\n")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-q", "-m", "base")
    return tmp


def test_no_watched_change_ok(tmp_path: pathlib.Path) -> None:
    root = make_repo(tmp_path)
    (root / "README.md").write_text("hi\n")
    _git(root, "add", "README.md")
    _git(root, "commit", "-q", "-m", "readme")
    assert main("HEAD~1", "HEAD", root) == 0


def test_watched_change_without_changelog_fails(tmp_path: pathlib.Path) -> None:
    root = make_repo(tmp_path)
    (root / "docs" / "a.md").write_text("# A2\n")
    _git(root, "add", "docs/a.md")
    _git(root, "commit", "-q", "-m", "doc")
    assert main("HEAD~1", "HEAD", root) == 1


def test_watched_change_with_changelog_ok(tmp_path: pathlib.Path) -> None:
    root = make_repo(tmp_path)
    (root / "docs" / "a.md").write_text("# A2\n")
    (root / "CHANGELOG.md").write_text("# changelog 2\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "doc+cl")
    assert main("HEAD~1", "HEAD", root) == 0


def test_needs_changelog() -> None:
    assert needs_changelog(["docs/a.md"]) is True
    assert needs_changelog(["scripts/x.py"]) is False


def test_bad_git_ref_raises(tmp_path: pathlib.Path) -> None:
    import subprocess

    root = tmp_path
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    try:
        main("nonexistent-base", "HEAD", root)
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected RuntimeError")  # noqa: TRY003


def test_cli_entrypoint(tmp_path: pathlib.Path) -> None:
    import subprocess
    import sys

    root = tmp_path
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
    (root / "README.md").write_text("hi\n")
    subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=root, check=True)
    (root / "README.md").write_text("hi2\n")
    subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "second"], cwd=root, check=True)
    result = subprocess.run(
        [
            sys.executable,
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "scripts"
                / "check_changelog.py"
            ),
            "--root",
            str(root),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
