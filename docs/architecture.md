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

These compatibility paths are now deprecated. New docs, tests, and integrations should point at the canonical `core/` and `providers/` locations. The shims remain in place to avoid breaking existing installs.

## Current Status

## Current Status

This architecture is now in its intended steady state for the multi-provider rollout:

- source-of-truth boundaries are now explicit
- Codex support has a real plugin scaffold
- verification is aware of the new structure
- Claude and Copilot workflow wrappers are rendered from shared workflow sources
- compatibility links remain only as deprecated shims

See [`final-architecture-review.md`](final-architecture-review.md) for the reviewer-facing checklist of what now counts as canonical, provider-owned, and intentionally transitional.
## Maintenance Loop

When shared behavior changes:

1. Update the relevant files under `core/`.
2. Run `python3 scripts/render_workflow_tables.py`.
3. Run `bash tests/consistency.sh`.
4. Run `bash tests/test-hooks.sh`.

See [`maintenance.md`](maintenance.md) for the maintainer-oriented workflow.
