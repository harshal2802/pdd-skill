#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS_PATH = ROOT / "core/metadata/workflows.json"


def load_workflows():
    with WORKFLOWS_PATH.open() as fh:
        return json.load(fh)["workflows"]


def markdown_table(rows):
    lines = [
        "| Command | What it does |",
        "|---|---|",
    ]
    for command, summary in rows:
        lines.append(f"| `{command}` | {summary} |")
    return "\n".join(lines)


def provider_rows(workflows, provider_id):
    rows = []
    for workflow in workflows:
        command = workflow["providers"][provider_id]
        rows.append((command, workflow["summary"]))
    return rows


def codex_rows(workflows):
    rows = []
    for workflow in workflows:
        rows.append((f"pdd:{workflow['providers']['codex']}", workflow["summary"]))
    return rows


def replace_block(text, marker, body):
    start = f"<!-- GENERATED:{marker}:start -->"
    end = f"<!-- GENERATED:{marker}:end -->"
    if start not in text or end not in text:
        raise ValueError(f"Missing generated markers for {marker}")

    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    new_block = f"{start}\n{body}\n{end}"
    return before + new_block + after


def render_files():
    workflows = load_workflows()
    targets = {
        ROOT / "README.md": {
            "claude-command-table": markdown_table(provider_rows(workflows, "claude")),
        },
        ROOT / "providers/copilot/README.md": {
            "copilot-command-table": markdown_table(provider_rows(workflows, "copilot")),
        },
        ROOT / "providers/codex/README.md": {
            "codex-command-table": markdown_table(codex_rows(workflows)),
        },
    }

    rendered = {}
    for path, blocks in targets.items():
        text = path.read_text()
        for marker, body in blocks.items():
            text = replace_block(text, marker, body)
        rendered[path] = text
    return rendered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated sections are stale")
    args = parser.parse_args()

    rendered = render_files()
    stale = []
    for path, new_text in rendered.items():
        old_text = path.read_text()
        if old_text != new_text:
            stale.append(path)
            if not args.check:
                path.write_text(new_text)

    if args.check and stale:
        for path in stale:
            print(f"STALE: {path.relative_to(ROOT)}")
        print("Run `python3 scripts/render_workflow_tables.py` to update generated workflow tables.")
        sys.exit(1)


if __name__ == "__main__":
    main()
