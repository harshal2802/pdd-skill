# Maintenance Workflow

This repo now has two kinds of files:

- canonical source files under `core/`
- provider wrappers under `providers/`, some of which contain generated sections

## Source Of Truth

Use `core/` as the starting point when changing shared PDD behavior:

- `core/workflows/` for provider-neutral workflow intent
- `core/references/` for project-type guidance
- `core/examples/` for example projects
- `core/metadata/` for generated provider sections

Current metadata files:

- `workflows.json`
- `help.json`
- `status.json`
- `routing.json`
- `principles.json`
- `claude-skill.json`
- `providers.json`

## Generated Sections

Some provider-facing files are still hand-authored overall, but include generated blocks wrapped in markers like:

```md
<!-- GENERATED:marker:start -->
...
<!-- GENERATED:marker:end -->
```

Those blocks are rendered by:

```bash
python3 scripts/render_workflow_tables.py
```

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

## Compatibility Paths

The top-level paths below are compatibility links for existing installs and docs:

- `commands/`
- `skills/`
- `hooks/`
- `.claude-plugin/`
- `copilot/`
- `references/`
- `examples/`

Their canonical homes live under `providers/` or `core/`.
