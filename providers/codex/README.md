# PDD for Codex

This provider adapter packages PDD as a Codex plugin with a `pdd` skill.

The canonical Codex provider lives under `providers/codex/`. The root `plugins/pdd-skill` path is a deprecated compatibility shim that remains in place so existing local marketplace setups do not break.

## Repo Packaging

This repo already includes the pieces needed for a repo-local Codex plugin setup:

- canonical plugin files under `providers/codex/plugin/`
- compatibility plugin path at `plugins/pdd-skill`
- repo-local marketplace metadata at `.agents/plugins/marketplace.json`

That means the repo can be treated as a local plugin source without inventing a second Codex-only project layout, while still steering new docs and tooling toward the canonical `providers/codex/` layout.

## Layout

- `plugin/.codex-plugin/plugin.json` contains the Codex plugin manifest.
- `plugin/skills/pdd/SKILL.md` is the Codex-facing adapter skill.
- `plugin/references/` and `plugin/workflows/` link to the canonical `core/` content.

## Available Workflows

Use the `pdd` skill and route into the matching workflow:

<!-- GENERATED:codex-command-table:start -->
| Command | What it does |
|---|---|
| `pdd:scaffold` | Set up a new PDD project with folders, context stubs, and starter guidance. |
| `pdd:init` | Add PDD structure to an existing repository and infer a starting context. |
| `pdd:context` | Write or update the persistent project context files that future prompts depend on. |
| `pdd:research` | Explore the problem space, evaluate options, and decide what to build. |
| `pdd:plan` | Break a feature into phases and decide the prompt chain strategy before coding. |
| `pdd:prompts` | Generate focused feature prompts and place them in the right PDD folder. |
| `pdd:update` | Diagnose and improve a prompt that is producing weak or incorrect output. |
| `pdd:review` | Verify and review AI-generated output before it is committed. |
| `pdd:eval` | Track prompt quality over time with repeatable evaluation criteria. |
| `pdd:status` | Check what PDD artifacts exist, what is stale, and what to do next. |
| `pdd:help` | Show the available workflows, when to use them, and the typical sequence. |
<!-- GENERATED:codex-command-table:end -->

## Notes

This first pass keeps the Codex adapter thin by leaning on `core/workflows/` and `core/references/` instead of duplicating the full workflow content again.

Generated sections in the wider repo are rendered from shared metadata under `core/metadata/`, then verified by `bash tests/consistency.sh`.
