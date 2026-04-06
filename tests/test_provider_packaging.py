#!/usr/bin/env python3
import json
import pathlib
import shutil
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent.parent


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK:   {message}")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    ok(message)


def assert_file(path: pathlib.Path, message: str) -> None:
    assert_true(path.exists() and path.is_file(), message)


def load_json(path: pathlib.Path):
    with path.open() as fh:
        return json.load(fh)


def copy_repo(tmpdir: pathlib.Path) -> pathlib.Path:
    destination = tmpdir / "repo"
    shutil.copytree(
        ROOT,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    return destination


def test_claude_clone_surface(repo_copy: pathlib.Path) -> None:
    assert_true((repo_copy / "skills").is_symlink(), "cloned repo preserves skills compatibility symlink")
    assert_true((repo_copy / "commands").is_symlink(), "cloned repo preserves commands compatibility symlink")
    assert_true((repo_copy / ".claude-plugin").is_symlink(), "cloned repo preserves Claude plugin symlink")
    assert_file(repo_copy / "skills/pdd/SKILL.md", "Claude clone surface exposes skills/pdd/SKILL.md")
    assert_file(repo_copy / "commands/pdd-help.md", "Claude clone surface exposes commands/pdd-help.md")
    assert_file(repo_copy / ".claude-plugin/plugin.json", "Claude clone surface exposes plugin manifest")


def test_copilot_copy_surface(repo_copy: pathlib.Path) -> None:
    install_root = repo_copy / "_tmp-copilot-project" / ".github"
    install_root.mkdir(parents=True)

    shutil.copy2(repo_copy / "copilot/copilot-instructions.md", install_root / "copilot-instructions.md")
    shutil.copytree(repo_copy / "copilot/prompts", install_root / "prompts")
    shutil.copytree(repo_copy / "references", install_root / "references")

    assert_file(
        install_root / "copilot-instructions.md",
        "Copilot copy surface installs copilot-instructions.md",
    )
    assert_file(
        install_root / "prompts/pdd-context.prompt.md",
        "Copilot copy surface installs prompt files",
    )
    assert_file(
        install_root / "references/frontend.md",
        "Copilot copy surface installs shared references",
    )

    prompt_files = sorted((install_root / "prompts").glob("*.prompt.md"))
    reference_files = sorted((install_root / "references").glob("*.md"))
    assert_true(len(prompt_files) == 11, "Copilot install gets all 11 prompt files")
    assert_true(len(reference_files) == 16, "Copilot install gets all 16 reference files")


def test_codex_plugin_surface(repo_copy: pathlib.Path) -> None:
    plugin_root = repo_copy / "plugins/pdd-skill"
    assert_true(plugin_root.is_dir(), "Codex compatibility plugin path resolves to a directory")
    assert_file(plugin_root / ".codex-plugin/plugin.json", "Codex plugin path exposes plugin manifest")
    assert_file(plugin_root / "skills/pdd/SKILL.md", "Codex plugin path exposes skill entrypoint")
    assert_true((plugin_root / "workflows").is_symlink(), "Codex plugin keeps workflows as a shared symlink")
    assert_true((plugin_root / "references").is_symlink(), "Codex plugin keeps references as a shared symlink")
    assert_file(plugin_root / "assets/pdd-skill.svg", "Codex plugin path exposes brand assets")

    marketplace = load_json(repo_copy / ".agents/plugins/marketplace.json")
    plugin_entry = marketplace["plugins"][0]
    assert_true(plugin_entry["name"] == "pdd-skill", "Codex marketplace entry names the plugin correctly")
    assert_true(
        plugin_entry["source"]["path"] == "./plugins/pdd-skill",
        "Codex marketplace entry points at the compatibility plugin path",
    )


def test_manifest_alignment(repo_copy: pathlib.Path) -> None:
    claude_manifest = load_json(repo_copy / "providers/claude/plugin/plugin.json")
    codex_manifest = load_json(repo_copy / "providers/codex/plugin/.codex-plugin/plugin.json")
    assert_true(
        claude_manifest["name"] == codex_manifest["name"] == "pdd-skill",
        "Claude and Codex manifests share the plugin name",
    )
    assert_true(
        claude_manifest["version"] == codex_manifest["version"],
        "Claude and Codex manifests stay on the same version",
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_copy = copy_repo(pathlib.Path(tmpdir))
        test_claude_clone_surface(repo_copy)
        test_copilot_copy_surface(repo_copy)
        test_codex_plugin_surface(repo_copy)
        test_manifest_alignment(repo_copy)


if __name__ == "__main__":
    main()
