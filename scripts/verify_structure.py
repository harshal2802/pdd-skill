#!/usr/bin/env python3
import json
import os
import pathlib


ROOT = pathlib.Path(__file__).resolve().parent.parent


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK:   {message}")


def load_json(path: pathlib.Path):
    with path.open() as fh:
        return json.load(fh)


def assert_file(path: pathlib.Path, message: str) -> None:
    if not path.exists():
        fail(message)
    ok(message)


def assert_symlink(path: pathlib.Path, target: str) -> None:
    if not path.is_symlink():
        fail(f"{path.relative_to(ROOT)} is not a symlink")
    actual = os.readlink(path)
    if actual != target:
        fail(f"{path.relative_to(ROOT)} points to {actual}, expected {target}")
    ok(f"{path.relative_to(ROOT)} -> {target}")


def main() -> None:
    workflow_meta = load_json(ROOT / "core/metadata/workflows.json")["workflows"]
    provider_meta = load_json(ROOT / "core/metadata/providers.json")["providers"]

    assert_file(ROOT / "core/README.md", "core/README.md exists")
    assert_file(ROOT / "docs/architecture.md", "docs/architecture.md exists")
    assert_file(ROOT / "core/metadata/help.json", "core/metadata/help.json exists")
    assert_file(ROOT / "core/metadata/status.json", "core/metadata/status.json exists")

    workflow_ids = [entry["id"] for entry in workflow_meta]
    for workflow_id in workflow_ids:
        assert_file(
            ROOT / f"core/workflows/{workflow_id}.md",
            f"core/workflows/{workflow_id}.md exists",
        )
        assert_file(
            ROOT / f"providers/claude/commands/pdd-{workflow_id}.md",
            f"providers/claude/commands/pdd-{workflow_id}.md exists",
        )
        assert_file(
            ROOT / f"providers/copilot/prompts/pdd-{workflow_id}.prompt.md",
            f"providers/copilot/prompts/pdd-{workflow_id}.prompt.md exists",
        )

    for ref in sorted((ROOT / "core/references").glob("*.md")):
        ok(f"{ref.relative_to(ROOT)} exists")

    assert_file(
        ROOT / "providers/claude/skills/pdd/SKILL.md",
        "providers/claude/skills/pdd/SKILL.md exists",
    )
    assert_file(
        ROOT / "providers/claude/plugin/plugin.json",
        "providers/claude/plugin/plugin.json exists",
    )
    assert_file(
        ROOT / "providers/copilot/copilot-instructions.md",
        "providers/copilot/copilot-instructions.md exists",
    )
    assert_file(
        ROOT / "providers/codex/plugin/.codex-plugin/plugin.json",
        "providers/codex/plugin/.codex-plugin/plugin.json exists",
    )
    assert_file(
        ROOT / "providers/codex/plugin/skills/pdd/SKILL.md",
        "providers/codex/plugin/skills/pdd/SKILL.md exists",
    )
    assert_file(
        ROOT / ".agents/plugins/marketplace.json",
        ".agents/plugins/marketplace.json exists",
    )

    assert_symlink(ROOT / "commands", "providers/claude/commands")
    assert_symlink(ROOT / "skills", "providers/claude/skills")
    assert_symlink(ROOT / "hooks", "providers/claude/hooks")
    assert_symlink(ROOT / ".claude-plugin", "providers/claude/plugin")
    assert_symlink(ROOT / "copilot", "providers/copilot")
    assert_symlink(ROOT / "references", "core/references")
    assert_symlink(ROOT / "examples", "core/examples")
    assert_symlink(ROOT / "plugins/pdd-skill", "../providers/codex/plugin")

    provider_ids = {provider["id"] for provider in provider_meta}
    if provider_ids != {"claude", "copilot", "codex"}:
        fail(f"provider ids mismatch: {sorted(provider_ids)}")
    ok("provider metadata covers claude, copilot, and codex")

    readme = (ROOT / "README.md").read_text()
    for expected in ("Claude Code", "GitHub Copilot", "Codex", "core/", "providers/"):
        if expected not in readme:
            fail(f"README.md missing {expected!r}")
    ok("README.md covers the multi-provider structure")

    copilot_readme = (ROOT / "providers/copilot/README.md").read_text()
    if "cp -r references/" not in copilot_readme:
        fail("providers/copilot/README.md missing references copy instruction")
    ok("providers/copilot/README.md still covers reference copying")


if __name__ == "__main__":
    main()
