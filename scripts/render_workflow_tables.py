#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS_PATH = ROOT / "core/metadata/workflows.json"
HELP_PATH = ROOT / "core/metadata/help.json"
STATUS_PATH = ROOT / "core/metadata/status.json"


def load_workflows():
    with WORKFLOWS_PATH.open() as fh:
        return json.load(fh)["workflows"]


def load_help():
    with HELP_PATH.open() as fh:
        return json.load(fh)


def load_status():
    with STATUS_PATH.open() as fh:
        return json.load(fh)


def markdown_table(rows):
    lines = [
        "| Command | What it does |",
        "|---|---|",
    ]
    for command, summary in rows:
        lines.append(f"| `{command}` | {summary} |")
    return "\n".join(lines)


def markdown_table_with_headers(headers, rows):
    lines = [
        f"| {headers[0]} | {headers[1]} |",
        "|---|---|",
    ]
    for left, right in rows:
        lines.append(f"| {left} | {right} |")
    return "\n".join(lines)


def command_name(workflow, provider_id, style):
    full = workflow["providers"][provider_id]
    if style == "full":
        return full
    if style == "bare":
        if provider_id == "claude":
            return full.replace("/project:", "")
        return full.lstrip("/")
    raise ValueError(f"Unknown style: {style}")


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


def grouped_help_tables(workflows, provider_id):
    ordered_groups = [
        ("Getting started", ["help", "scaffold", "init", "status"]),
        ("Building features", ["context", "research", "plan", "prompts", "update"]),
        ("Quality", ["review", "eval"]),
    ]
    workflow_map = {workflow["id"]: workflow for workflow in workflows}
    blocks = []
    for title, workflow_ids in ordered_groups:
        rows = []
        for workflow_id in workflow_ids:
            workflow = workflow_map[workflow_id]
            rows.append((command_name(workflow, provider_id, "full"), workflow["summary"]))
        blocks.append(f"**{title}**\n\n{markdown_table(rows)}")
    return "\n\n".join(blocks)


def render_quick_start(help_meta):
    return f"> **Quick start**: {help_meta['quick_start']}"


def render_scenarios(workflows, help_meta, provider_id):
    workflow_map = {workflow["id"]: workflow for workflow in workflows}
    rows = []
    for scenario in help_meta["scenario_routes"]:
        command_chain = " -> ".join(
            f"`{command_name(workflow_map[workflow_id], provider_id, 'bare' if provider_id == 'claude' else 'full')}`"
            for workflow_id in scenario["workflow_ids"]
        )
        rows.append((scenario["goal"], command_chain))
    return markdown_table_with_headers(("I want to...", "Use"), rows)


def render_command_detail(workflows, help_meta, provider_id):
    workflow_map = {workflow["id"]: workflow for workflow in workflows}
    lines = [
        "| Command | When to use | Inputs | Produces | Next step |",
        "|---|---|---|---|---|",
    ]
    for workflow in workflows:
        detail = help_meta["command_details"][workflow["id"]]
        next_step = detail["next_step_template"]
        for candidate_id, candidate in workflow_map.items():
            next_step = next_step.replace(
                f"{{{candidate_id}}}",
                f"`{command_name(candidate, provider_id, 'bare' if provider_id == 'claude' else 'full')}`",
            )
        lines.append(
            "| {} | {} | {} | {} | {} |".format(
                f"`{command_name(workflow, provider_id, 'bare')}`",
                detail["when_to_use"],
                detail["inputs"],
                detail["produces"],
                next_step,
            )
        )
    return "\n".join(lines)


def render_status_checks(status_meta, provider_id):
    how_key = f"{provider_id}_how"
    blocks = []
    for layer in status_meta["layers"]:
        rows = [(item["check"], item[how_key]) for item in layer["checks"]]
        blocks.append(f"### {layer['title']}\n\n{markdown_table_with_headers(('Check', 'How'), rows)}")
    return "\n\n".join(blocks)


def render_status_output(status_meta):
    code = "\n".join(status_meta["output_format"])
    return f"```text\n{code}\n```\n\n{status_meta['closing_note']}"


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
    help_meta = load_help()
    status_meta = load_status()
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
        ROOT / "providers/claude/commands/pdd-help.md": {
            "claude-help-quick-start": render_quick_start(help_meta),
            "claude-help-command-groups": grouped_help_tables(workflows, "claude"),
            "claude-help-scenarios": render_scenarios(workflows, help_meta, "claude"),
            "claude-help-command-detail": render_command_detail(workflows, help_meta, "claude"),
        },
        ROOT / "providers/copilot/prompts/pdd-help.prompt.md": {
            "copilot-help-quick-start": render_quick_start(help_meta),
            "copilot-help-command-groups": grouped_help_tables(workflows, "copilot"),
            "copilot-help-scenarios": render_scenarios(workflows, help_meta, "copilot"),
            "copilot-help-command-detail": render_command_detail(workflows, help_meta, "copilot"),
        },
        ROOT / "providers/claude/commands/pdd-status.md": {
            "claude-status-checks": render_status_checks(status_meta, "claude"),
            "claude-status-output-format": render_status_output(status_meta),
        },
        ROOT / "providers/copilot/prompts/pdd-status.prompt.md": {
            "copilot-status-checks": render_status_checks(status_meta, "copilot"),
            "copilot-status-output-format": render_status_output(status_meta),
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
