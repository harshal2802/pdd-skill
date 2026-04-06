#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
CLAUDE_SKILL_PATH = ROOT / "core/metadata/claude-skill.json"
WORKFLOWS_PATH = ROOT / "core/metadata/workflows.json"
HELP_PATH = ROOT / "core/metadata/help.json"
PRINCIPLES_PATH = ROOT / "core/metadata/principles.json"
ROUTING_PATH = ROOT / "core/metadata/routing.json"
STATUS_PATH = ROOT / "core/metadata/status.json"
TARGET_SPECS = {
    "README.md": (
        "claude-command-table",
    ),
    "providers/copilot/README.md": (
        "copilot-command-table",
    ),
    "providers/codex/README.md": (
        "codex-command-table",
    ),
    "providers/claude/commands/pdd-help.md": (
        "claude-help-quick-start",
        "claude-help-command-groups",
        "claude-help-scenarios",
        "claude-help-command-detail",
    ),
    "providers/copilot/prompts/pdd-help.prompt.md": (
        "copilot-help-quick-start",
        "copilot-help-command-groups",
        "copilot-help-scenarios",
        "copilot-help-command-detail",
    ),
    "providers/claude/commands/pdd-status.md": (
        "claude-status-checks",
        "claude-status-output-format",
    ),
    "providers/copilot/prompts/pdd-status.prompt.md": (
        "copilot-status-checks",
        "copilot-status-output-format",
    ),
    "providers/claude/skills/pdd/SKILL.md": (
        "claude-workflow-overview",
        "claude-workflow-transitions",
        "claude-quick-path",
        "claude-principles",
        "claude-routing-table",
    ),
    "providers/copilot/copilot-instructions.md": (
        "copilot-principles",
        "copilot-routing-table",
    ),
    "providers/codex/plugin/skills/pdd/SKILL.md": (
        "codex-principles",
        "codex-simple-flow",
        "codex-complex-flow",
        "codex-routing-table",
    ),
}


def load_claude_skill():
    with CLAUDE_SKILL_PATH.open() as fh:
        return json.load(fh)


def load_workflows():
    with WORKFLOWS_PATH.open() as fh:
        return json.load(fh)["workflows"]


def load_help():
    with HELP_PATH.open() as fh:
        return json.load(fh)


def load_principles():
    with PRINCIPLES_PATH.open() as fh:
        return json.load(fh)


def load_routing():
    with ROUTING_PATH.open() as fh:
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


def render_help_document(workflows, help_meta, provider_id):
    if provider_id == "claude":
        frontmatter = ""
        user_input = "**User input**: $ARGUMENTS\n\n"
        specific_heading = "## If the user passed an argument"
        specific_text = (
            'If `$ARGUMENTS` names a specific command (e.g., "context", "pdd-context", "review"), '
            "show detailed help for that command only:"
        )
        fallback_heading = "## If no argument was provided"
        markers = {
            "quick_start": "claude-help-quick-start",
            "command_groups": "claude-help-command-groups",
            "scenarios": "claude-help-scenarios",
            "command_detail": "claude-help-command-detail",
        }
    elif provider_id == "copilot":
        frontmatter = (
            "---\n"
            "agent: agent\n"
            'description: "Quick reference for all PDD commands, workflow order, and usage guidance"\n'
            "---\n\n"
        )
        user_input = ""
        specific_heading = "## If the user asked about a specific command"
        specific_text = (
            'If the user mentioned a specific command (e.g., "context", "pdd-context", "review"), '
            "show detailed help for that command only:"
        )
        fallback_heading = "## If no specific command was mentioned"
        markers = {
            "quick_start": "copilot-help-quick-start",
            "command_groups": "copilot-help-command-groups",
            "scenarios": "copilot-help-scenarios",
            "command_detail": "copilot-help-command-detail",
        }
    else:
        raise ValueError(f"Unsupported help provider_id: {provider_id}")

    return (
        f"{frontmatter}"
        "# PDD Help\n\n"
        "Quick reference for all PDD commands, workflow order, and usage guidance.\n\n"
        f"{user_input}"
        f"{specific_heading}\n\n"
        f"{specific_text}\n\n"
        "- **What it does** — one-paragraph description\n"
        "- **When to use it** — the situation that calls for this workflow\n"
        "- **Inputs it expects** — what the user should provide or have ready\n"
        "- **What it produces** — the output artifact(s)\n"
        "- **Typical next step** — what command usually follows\n\n"
        "Use the command table and routing guide below to compose the answer. "
        "Give the user just what they asked about — don't dump the full help.\n\n"
        f"{fallback_heading}\n\n"
        "Show the full quick reference below.\n\n"
        "---\n\n"
        "### Quick start\n\n"
        f"<!-- GENERATED:{markers['quick_start']}:start -->\n"
        f"{render_quick_start(help_meta)}\n"
        f"<!-- GENERATED:{markers['quick_start']}:end -->\n\n"
        "### All commands\n\n"
        f"<!-- GENERATED:{markers['command_groups']}:start -->\n"
        f"{grouped_help_tables(workflows, provider_id)}\n"
        f"<!-- GENERATED:{markers['command_groups']}:end -->\n\n"
        "### \"What should I use?\"\n\n"
        f"<!-- GENERATED:{markers['scenarios']}:start -->\n"
        f"{render_scenarios(workflows, help_meta, provider_id)}\n"
        f"<!-- GENERATED:{markers['scenarios']}:end -->\n\n"
        "### Per-command detail\n\n"
        "Use this table when the user asks about a specific command.\n\n"
        f"<!-- GENERATED:{markers['command_detail']}:start -->\n"
        f"{render_command_detail(workflows, help_meta, provider_id)}\n"
        f"<!-- GENERATED:{markers['command_detail']}:end -->\n"
    )


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


def render_status_document(status_meta, provider_id):
    if provider_id == "claude":
        frontmatter = ""
        user_input = "**User input**: $ARGUMENTS\n\n"
        markers = {
            "checks": "claude-status-checks",
            "output": "claude-status-output-format",
        }
    elif provider_id == "copilot":
        frontmatter = (
            "---\n"
            "agent: agent\n"
            'description: "Check the health and completeness of your PDD project setup"\n'
            "---\n\n"
        )
        user_input = ""
        markers = {
            "checks": "copilot-status-checks",
            "output": "copilot-status-output-format",
        }
    else:
        raise ValueError(f"Unsupported status provider_id: {provider_id}")

    return (
        f"{frontmatter}"
        "# PDD Project Status\n\n"
        "Check the health and completeness of the current PDD project setup.\n\n"
        f"{user_input}"
        "## What to check\n\n"
        "Scan the current project directory and report on each layer:\n\n"
        f"<!-- GENERATED:{markers['checks']}:start -->\n"
        f"{render_status_checks(status_meta, provider_id)}\n"
        f"<!-- GENERATED:{markers['checks']}:end -->\n\n"
        "## Output format\n\n"
        f"<!-- GENERATED:{markers['output']}:start -->\n"
        f"{render_status_output(status_meta)}\n"
        f"<!-- GENERATED:{markers['output']}:end -->\n"
    )


def render_routing_table(workflows, routing_meta, provider_id):
    workflow_map = {workflow["id"]: workflow for workflow in workflows}
    headers = {
        "claude": ("If the user says...", "Use workflow"),
        "copilot": ("User intent", "Suggest"),
        "codex": ("If the user wants to...", "Use"),
    }
    rows = []
    for route in routing_meta["routes"]:
        workflow = workflow_map[route["workflow_id"]]
        if provider_id == "claude":
            left = route["claude_signal"]
            right = f"-> **{workflow['label']}**: run `{workflow['providers']['claude']}`"
        elif provider_id == "copilot":
            left = route["copilot_intent"]
            right = f"Use `{workflow['providers']['copilot']}`"
        elif provider_id == "codex":
            left = route["codex_intent"]
            right = f"`{workflow['providers']['codex']}`"
        else:
            raise ValueError(f"Unsupported provider_id: {provider_id}")
        rows.append((left, right))
    return markdown_table_with_headers(headers[provider_id], rows)


def render_principles(principles_meta, provider_id):
    return "\n".join(f"- {entry[provider_id]}" for entry in principles_meta["principles"])


def render_claude_workflow_overview(workflows, claude_skill_meta):
    workflow_map = {workflow["id"]: workflow for workflow in workflows}
    lines = []
    for index, item in enumerate(claude_skill_meta["workflow_overview"], start=1):
        workflow = workflow_map[item["workflow_id"]]
        lines.append(f"{index}. **{workflow['label']}** — {item['description']}")
    return "\n".join(lines)


def render_claude_transitions(claude_skill_meta):
    lines = [
        "| Just finished | Suggest next |",
        "|---|---|",
    ]
    for item in claude_skill_meta["transitions"]:
        lines.append(f"| {item['just_finished']} | {item['suggest_next']} |")
    return "\n".join(lines)


def replace_block(text, marker, body):
    start = f"<!-- GENERATED:{marker}:start -->"
    end = f"<!-- GENERATED:{marker}:end -->"
    if start not in text or end not in text:
        raise ValueError(f"Missing generated markers for {marker}")

    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    new_block = f"{start}\n{body}\n{end}"
    return before + new_block + after


def target_paths():
    return {ROOT / relative_path: markers for relative_path, markers in TARGET_SPECS.items()}


def render_files():
    claude_skill_meta = load_claude_skill()
    workflows = load_workflows()
    help_meta = load_help()
    principles_meta = load_principles()
    routing_meta = load_routing()
    status_meta = load_status()
    rendered_blocks = {
        ROOT / "README.md": {
            "claude-command-table": markdown_table(provider_rows(workflows, "claude")),
        },
        ROOT / "providers/copilot/README.md": {
            "copilot-command-table": markdown_table(provider_rows(workflows, "copilot")),
        },
        ROOT / "providers/codex/README.md": {
            "codex-command-table": markdown_table(codex_rows(workflows)),
        },
        ROOT / "providers/claude/skills/pdd/SKILL.md": {
            "claude-workflow-overview": render_claude_workflow_overview(workflows, claude_skill_meta),
            "claude-workflow-transitions": render_claude_transitions(claude_skill_meta),
            "claude-quick-path": f"**Quick path**: {principles_meta['claude_quick_path']}",
            "claude-principles": render_principles(principles_meta, "claude"),
            "claude-routing-table": render_routing_table(workflows, routing_meta, "claude"),
        },
        ROOT / "providers/copilot/copilot-instructions.md": {
            "copilot-principles": render_principles(principles_meta, "copilot"),
            "copilot-routing-table": render_routing_table(workflows, routing_meta, "copilot"),
        },
        ROOT / "providers/codex/plugin/skills/pdd/SKILL.md": {
            "codex-principles": render_principles(principles_meta, "codex"),
            "codex-simple-flow": principles_meta["codex_default_flow"]["simple"],
            "codex-complex-flow": principles_meta["codex_default_flow"]["complex"],
            "codex-routing-table": render_routing_table(workflows, routing_meta, "codex"),
        },
    }
    fully_rendered_targets = {
        ROOT / "providers/claude/commands/pdd-help.md": render_help_document(workflows, help_meta, "claude"),
        ROOT / "providers/copilot/prompts/pdd-help.prompt.md": render_help_document(workflows, help_meta, "copilot"),
        ROOT / "providers/claude/commands/pdd-status.md": render_status_document(status_meta, "claude"),
        ROOT / "providers/copilot/prompts/pdd-status.prompt.md": render_status_document(status_meta, "copilot"),
    }

    expected_paths = set(target_paths())
    actual_paths = set(rendered_blocks) | set(fully_rendered_targets)
    if actual_paths != expected_paths:
        raise ValueError("Rendered targets do not match TARGET_SPECS")
    for path, expected_markers in target_paths().items():
        if path in rendered_blocks:
            actual_markers = tuple(rendered_blocks[path])
        else:
            text = fully_rendered_targets[path]
            actual_markers = tuple(
                marker
                for marker in expected_markers
                if f"<!-- GENERATED:{marker}:start -->" in text
            )
        if actual_markers != expected_markers:
            raise ValueError(
                f"Marker list mismatch for {path.relative_to(ROOT)}: "
                f"{actual_markers!r} != {expected_markers!r}"
            )

    rendered = {}
    for path, text in fully_rendered_targets.items():
        rendered[path] = text
    for path, blocks in rendered_blocks.items():
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
