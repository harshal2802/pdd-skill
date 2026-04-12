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
- workflow adapter document metadata

### `providers/`

Thin provider adapters:

- `providers/claude/`
- `providers/copilot/`
- `providers/codex/`

Each provider owns its packaging, activation model, and install-facing wrapper files.

At this point, the Claude and Copilot workflow wrappers are rendered from shared workflow sources plus provider metadata, so the provider layer is primarily packaging and surface-specific wording rather than a second source of workflow truth.

## Root-Level Paths

Most legacy compatibility symlinks have been removed. Only two root-level symlinks remain because they are functionally required by their respective plugin systems:

- `.claude-plugin/` — required by Claude Code plugin discovery
- `plugins/pdd-skill` — required by the Codex repo-local marketplace at `.agents/plugins/marketplace.json`

All other paths (`commands/`, `skills/`, `hooks/`, `copilot/`, `references/`, `examples/`) have been removed. Use the canonical `core/` and `providers/` locations directly.

## Current Status

This architecture is now in its intended steady state for the multi-provider rollout:

- source-of-truth boundaries are now explicit
- Codex support has a real plugin scaffold
- verification is aware of the new structure
- Claude and Copilot workflow wrappers are rendered from shared workflow sources
- legacy compatibility symlinks have been removed (only `.claude-plugin` and `plugins/pdd-skill` remain as functional requirements)

See [`final-architecture-review.md`](final-architecture-review.md) for the reviewer-facing checklist of what now counts as canonical, provider-owned, and intentionally transitional.
## Maintenance Loop

When shared behavior changes:

1. Update the relevant files under `core/`.
2. Run `python3 scripts/render_workflow_tables.py`.
3. Run `bash tests/consistency.sh`.
4. Run `bash tests/test-hooks.sh`.

See [`maintenance.md`](maintenance.md) for the maintainer-oriented workflow.
