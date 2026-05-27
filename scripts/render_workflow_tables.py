#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent

_VERSION_OVERRIDE = None


def get_version():
    if _VERSION_OVERRIDE:
        return _VERSION_OVERRIDE
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always"],
            capture_output=True, text=True, cwd=ROOT,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return "unknown"
ADAPTER_DOCS_PATH = ROOT / "core/metadata/adapter-docs.json"
CLAUDE_SKILL_PATH = ROOT / "core/metadata/claude-skill.json"
WORKFLOWS_PATH = ROOT / "core/metadata/workflows.json"
HELP_PATH = ROOT / "core/metadata/help.json"
PRINCIPLES_PATH = ROOT / "core/metadata/principles.json"
ROUTING_PATH = ROOT / "core/metadata/routing.json"
STATUS_PATH = ROOT / "core/metadata/status.json"
WORKFLOW_RENDER_IDS = (
    "scaffold",
    "init",
    "context",
    "research",
    "plan",
    "prompts",
    "update",
    "review",
    "eval",
)
TARGET_SPECS = {
    "README.md": (
        "claude-command-table",
        "antigravity-command-table",
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
    "providers/claude/commands/pdd-scaffold.md": (),
    "providers/claude/commands/pdd-init.md": (),
    "providers/claude/commands/pdd-context.md": (),
    "providers/claude/commands/pdd-research.md": (),
    "providers/claude/commands/pdd-plan.md": (),
    "providers/claude/commands/pdd-prompts.md": (),
    "providers/claude/commands/pdd-update.md": (),
    "providers/claude/commands/pdd-review.md": (),
    "providers/claude/commands/pdd-eval.md": (),
    "providers/copilot/prompts/pdd-scaffold.prompt.md": (),
    "providers/copilot/prompts/pdd-init.prompt.md": (),
    "providers/copilot/prompts/pdd-context.prompt.md": (),
    "providers/copilot/prompts/pdd-research.prompt.md": (),
    "providers/copilot/prompts/pdd-plan.prompt.md": (),
    "providers/copilot/prompts/pdd-prompts.prompt.md": (),
    "providers/copilot/prompts/pdd-update.prompt.md": (),
    "providers/copilot/prompts/pdd-review.prompt.md": (),
    "providers/copilot/prompts/pdd-eval.prompt.md": (),
    "providers/antigravity/README.md": (
        "antigravity-command-table",
    ),
    "providers/antigravity/GEMINI.md": (
        "antigravity-principles",
        "antigravity-routing-table",
    ),
    "providers/antigravity/skills/pdd/SKILL.md": (
        "antigravity-workflow-overview",
        "antigravity-workflow-transitions",
        "antigravity-quick-path",
        "antigravity-principles",
        "antigravity-routing-table",
    ),
    "providers/antigravity/workflows/pdd-help.md": (
        "antigravity-help-quick-start",
        "antigravity-help-command-groups",
        "antigravity-help-scenarios",
        "antigravity-help-command-detail",
    ),
    "providers/antigravity/workflows/pdd-status.md": (
        "antigravity-status-checks",
        "antigravity-status-output-format",
    ),
    "providers/antigravity/workflows/pdd-scaffold.md": (),
    "providers/antigravity/workflows/pdd-init.md": (),
    "providers/antigravity/workflows/pdd-context.md": (),
    "providers/antigravity/workflows/pdd-research.md": (),
    "providers/antigravity/workflows/pdd-plan.md": (),
    "providers/antigravity/workflows/pdd-prompts.md": (),
    "providers/antigravity/workflows/pdd-update.md": (),
    "providers/antigravity/workflows/pdd-review.md": (),
    "providers/antigravity/workflows/pdd-eval.md": (),
}
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


def load_adapter_docs():
    with ADAPTER_DOCS_PATH.open() as fh:
        return json.load(fh)


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


def workflow_by_id(workflows):
    return {workflow["id"]: workflow for workflow in workflows}


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
    elif provider_id == "antigravity":
        frontmatter = ""
        user_input = ""
        specific_heading = "## If the user asked about a specific command"
        specific_text = (
            'If the user mentioned a specific command (e.g., "context", "pdd-context", "review"), '
            "show detailed help for that command only:"
        )
        fallback_heading = "## If no specific command was mentioned"
        markers = {
            "quick_start": "antigravity-help-quick-start",
            "command_groups": "antigravity-help-command-groups",
            "scenarios": "antigravity-help-scenarios",
            "command_detail": "antigravity-help-command-detail",
        }
    else:
        raise ValueError(f"Unsupported help provider_id: {provider_id}")

    version = get_version()

    return (
        f"{frontmatter}"
        "# PDD Help\n\n"
        f"> **Version**: {version}\n\n"
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
    elif provider_id == "antigravity":
        frontmatter = ""
        user_input = ""
        markers = {
            "checks": "antigravity-status-checks",
            "output": "antigravity-status-output-format",
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
        "antigravity": ("User intent", "Use"),
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
        elif provider_id == "antigravity":
            left = route["antigravity_intent"]
            right = f"Use `{workflow['providers']['antigravity']}`"
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


def strip_h1(text):
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).strip()


def transform_inline_code(text, workflows, provider_id):
    workflow_map = workflow_by_id(workflows)

    def replace(match):
        code = match.group(1)
        if code in workflow_map:
            return f"`{workflow_map[code]['providers'][provider_id]}`"
        if provider_id == "copilot" and code.startswith("references/"):
            return f"`#file:{code}`"
        return match.group(0)

    return INLINE_CODE_RE.sub(replace, text)


def render_shared_workflow_body(workflow_id, workflows, provider_id):
    text = (ROOT / f"core/workflows/{workflow_id}.md").read_text()
    body = strip_h1(text)
    return transform_inline_code(body, workflows, provider_id)


def render_workflow_adapter_document(workflow, adapter_meta, workflows, provider_id):
    body = render_shared_workflow_body(workflow["id"], workflows, provider_id)
    title = adapter_meta["title"]

    if provider_id == "claude":
        adapter_note = (
            f"This is the Claude adapter for the shared `{workflow['label']}` workflow in "
            f"`core/workflows/{workflow['id']}.md`. Keep shared workflow behavior aligned there; "
            "this file exists to preserve Claude-specific command wording and `$ARGUMENTS` handling."
        )
        return (
            f"# {title}\n\n"
            f"{adapter_note}\n\n"
            "**User input**: $ARGUMENTS\n\n"
            f"{body}\n"
        )

    if provider_id == "copilot":
        adapter_note = (
            f"This is the Copilot adapter for the shared `{workflow['label']}` workflow in "
            f"`core/workflows/{workflow['id']}.md`. Keep shared workflow behavior aligned there; "
            "this file exists to preserve Copilot-specific frontmatter, `#file:` references, "
            "and `/pdd-*` command wording."
        )
        return (
            "---\n"
            "agent: agent\n"
            f'description: "{adapter_meta["copilot_description"]}"\n'
            "---\n\n"
            f"# {title}\n\n"
            f"{adapter_note}\n\n"
            f"{body}\n"
        )

    if provider_id == "antigravity":
        adapter_note = (
            f"This is the Antigravity adapter for the shared `{workflow['label']}` workflow in "
            f"`core/workflows/{workflow['id']}.md`. Keep shared workflow behavior aligned there; "
            "this file exists to preserve Antigravity-specific `/pdd-*` command wording."
        )
        return (
            f"# {title}\n\n"
            f"{adapter_note}\n\n"
            f"{body}\n"
        )

    raise ValueError(f"Unsupported workflow adapter provider_id: {provider_id}")


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
    adapter_docs = load_adapter_docs()
    claude_skill_meta = load_claude_skill()
    workflows = load_workflows()
    help_meta = load_help()
    principles_meta = load_principles()
    routing_meta = load_routing()
    status_meta = load_status()
    workflow_map = workflow_by_id(workflows)
    rendered_blocks = {
        ROOT / "README.md": {
            "claude-command-table": markdown_table(provider_rows(workflows, "claude")),
            "antigravity-command-table": markdown_table(provider_rows(workflows, "antigravity")),
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
        ROOT / "providers/antigravity/README.md": {
            "antigravity-command-table": markdown_table(provider_rows(workflows, "antigravity")),
        },
        ROOT / "providers/antigravity/GEMINI.md": {
            "antigravity-principles": render_principles(principles_meta, "antigravity"),
            "antigravity-routing-table": render_routing_table(workflows, routing_meta, "antigravity"),
        },
        ROOT / "providers/antigravity/skills/pdd/SKILL.md": {
            "antigravity-workflow-overview": render_claude_workflow_overview(workflows, claude_skill_meta),
            "antigravity-workflow-transitions": render_claude_transitions(claude_skill_meta),
            "antigravity-quick-path": f"**Quick path**: {principles_meta['claude_quick_path']}",
            "antigravity-principles": render_principles(principles_meta, "antigravity"),
            "antigravity-routing-table": render_routing_table(workflows, routing_meta, "antigravity"),
        },
    }
    fully_rendered_targets = {
        ROOT / "providers/claude/commands/pdd-help.md": render_help_document(workflows, help_meta, "claude"),
        ROOT / "providers/copilot/prompts/pdd-help.prompt.md": render_help_document(workflows, help_meta, "copilot"),
        ROOT / "providers/antigravity/workflows/pdd-help.md": render_help_document(workflows, help_meta, "antigravity"),
        ROOT / "providers/claude/commands/pdd-status.md": render_status_document(status_meta, "claude"),
        ROOT / "providers/copilot/prompts/pdd-status.prompt.md": render_status_document(status_meta, "copilot"),
        ROOT / "providers/antigravity/workflows/pdd-status.md": render_status_document(status_meta, "antigravity"),
    }
    for workflow_id in WORKFLOW_RENDER_IDS:
        workflow = workflow_map[workflow_id]
        adapter_meta = adapter_docs["workflows"][workflow_id]
        fully_rendered_targets[
            ROOT / f"providers/claude/commands/pdd-{workflow_id}.md"
        ] = render_workflow_adapter_document(workflow, adapter_meta, workflows, "claude")
        fully_rendered_targets[
            ROOT / f"providers/copilot/prompts/pdd-{workflow_id}.prompt.md"
        ] = render_workflow_adapter_document(workflow, adapter_meta, workflows, "copilot")
        fully_rendered_targets[
            ROOT / f"providers/antigravity/workflows/pdd-{workflow_id}.md"
        ] = render_workflow_adapter_document(workflow, adapter_meta, workflows, "antigravity")

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
    parser.add_argument("--version", default=None, help="version string to stamp into help output (defaults to git describe)")
    args = parser.parse_args()

    global _VERSION_OVERRIDE
    _VERSION_OVERRIDE = args.version

    rendered = render_files()
    stale = []
    version_re = re.compile(r"^> \*\*Version\*\*: .+$", re.MULTILINE)
    for path, new_text in rendered.items():
        old_text = path.read_text()
        if args.check:
            if version_re.sub("", old_text) != version_re.sub("", new_text):
                stale.append(path)
        else:
            if old_text != new_text:
                stale.append(path)
                path.write_text(new_text)

    if args.check and stale:
        for path in stale:
            print(f"STALE: {path.relative_to(ROOT)}")
        print("Run `python3 scripts/render_workflow_tables.py` to update generated workflow tables.")
        sys.exit(1)


if __name__ == "__main__":
    main()
