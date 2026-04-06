# Multi-Provider Architecture

This repo now separates provider-agnostic PDD content from provider-specific packaging.

## Canonical Layers

### `core/`

Shared source of truth:

- `core/workflows/` for provider-neutral workflow definitions
- `core/references/` for project-type reference docs
- `core/examples/` for sample PDD projects
- `core/metadata/` for workflow and provider metadata

The `core/metadata/` layer now drives a growing share of provider-facing content:

- workflow command tables
- help tables and per-command detail
- status checklists
- routing tables
- shared principles
- Claude skill workflow overview and transitions

### `providers/`

Thin provider adapters:

- `providers/claude/`
- `providers/copilot/`
- `providers/codex/`

Each provider owns its packaging, activation model, and install-facing wrapper files.

## Compatibility Paths

Top-level paths are still present as compatibility links so existing installs and docs keep working:

- `commands/`
- `skills/`
- `hooks/`
- `.claude-plugin/`
- `copilot/`
- `references/`
- `examples/`

The new Codex plugin distribution path is `plugins/pdd-skill`, with repo-local marketplace metadata at `.agents/plugins/marketplace.json`.

## Current Status

This is the first restructuring pass:

- source-of-truth boundaries are now explicit
- Codex support has a real plugin scaffold
- verification is aware of the new structure
- several high-duplication provider sections are generated from shared metadata

## Maintenance Loop

When shared behavior changes:

1. Update the relevant files under `core/`.
2. Run `python3 scripts/render_workflow_tables.py`.
3. Run `bash tests/consistency.sh`.
4. Run `bash tests/test-hooks.sh`.

See [`maintenance.md`](maintenance.md) for the maintainer-oriented workflow.

Future work can build on this by generating more provider wrappers directly from `core/metadata/` and `core/workflows/`.
