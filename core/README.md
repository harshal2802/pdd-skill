# PDD Core

This directory is the canonical home for provider-agnostic PDD content.

## Ownership

- `workflows/` defines the shared workflow intent, expected inputs, outputs, and next-step guidance.
- `references/` contains project-type reference files shared across providers.
- `examples/` contains example PDD project layouts and prompt artifacts.
- `metadata/` contains structured workflow/provider metadata used by verification and future generation tooling.

## Provider Boundary

Provider-specific packaging lives under `providers/`:

- `providers/claude/`
- `providers/copilot/`
- `providers/codex/`

Top-level paths like `commands/`, `skills/`, `copilot/`, `references/`, and `examples/` are compatibility links so existing install paths and docs keep working during the transition.

## Current Approach

This first pass establishes the source-of-truth boundary and Codex-ready structure without fully generating every provider file yet. Claude and Copilot still keep hand-authored wrappers, while Codex consumes the shared workflow and reference layer more directly.
