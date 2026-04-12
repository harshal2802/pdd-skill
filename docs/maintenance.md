# Maintenance Workflow

This repo now has two kinds of files:

- canonical source files under `core/`
- provider wrappers under `providers/`, some of which contain generated sections or are rendered from shared metadata

## Source Of Truth

Use `core/` as the starting point when changing shared PDD behavior:

- `core/workflows/` for provider-neutral workflow intent
- `core/references/` for project-type guidance
- `core/examples/` for example projects
- `core/metadata/` for generated provider sections

Current metadata files:

- `adapter-docs.json`
- `workflows.json`
- `help.json`
- `status.json`
- `routing.json`
- `principles.json`
- `claude-skill.json`
- `providers.json`

## Generated Content

There are two rendering patterns in the repo:

- hand-authored provider files with generated blocks wrapped in markers like:

```md
<!-- GENERATED:marker:start -->
...
<!-- GENERATED:marker:end -->
```

- fully rendered provider documents generated from shared metadata and provider-specific templates

Both are rendered by:

```bash
python3 scripts/render_workflow_tables.py
```

Today, all Claude and Copilot workflow wrappers are rendered as complete documents from shared workflow sources, while files like the skill entrypoints and provider READMEs still use generated blocks inside hand-authored files.

To verify that generated sections are current:

```bash
python3 scripts/render_workflow_tables.py --check
bash tests/consistency.sh
bash tests/test-hooks.sh
```

## Typical Change Flow

1. Update the relevant file in `core/`.
2. Run `python3 scripts/render_workflow_tables.py`.
3. Run `bash tests/consistency.sh`.
4. Run `bash tests/test-hooks.sh`.
5. Commit the metadata change and the regenerated provider wrappers together.

For PR and release prep, see [`release-readiness.md`](release-readiness.md).

## Root-Level Paths

Legacy compatibility symlinks have been removed. Only two root-level symlinks remain because they are required by their respective plugin systems:

- `.claude-plugin/` — Claude Code plugin discovery
- `plugins/pdd-skill` — Codex repo-local marketplace

All docs, tests, and automation should use `core/` and `providers/` paths directly.
