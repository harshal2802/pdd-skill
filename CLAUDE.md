# PDD Skill — Development Notes

## What this repo is

A multi-provider PDD repo with a shared `core/` layer and provider adapters under `providers/`. The compatibility paths `skills/`, `commands/`, `copilot/`, `references/`, and `examples/` still exist, but the canonical homes are:

- `core/workflows/`
- `core/references/`
- `core/examples/`
- `core/metadata/`
- `providers/claude/`
- `providers/copilot/`
- `providers/codex/`

## Pre-PR checklist

Run these checks before opening a PR. The goal is to catch cross-file consistency gaps — the most common source of bugs in this repo.

### Workflow parity

- [ ] Every workflow in `core/metadata/workflows.json` has a matching file in `core/workflows/`
- [ ] Every workflow id maps to a Claude command and Copilot prompt
- [ ] Codex plugin manifest and `skills/pdd/SKILL.md` both exist
- [ ] Compatibility links still point at the intended canonical directories

### File references resolve

- [ ] Every file in `core/references/` exists and is reachable from compatibility paths
- [ ] Copilot setup still covers `references/`
- [ ] Claude command references resolve
- [ ] Copilot prompt references resolve

### README consistency

- [ ] Root `README.md` mentions Claude, Copilot, and Codex
- [ ] Root `README.md` describes the `core/` + `providers/` split
- [ ] `copilot/README.md` setup instructions still match the compatibility paths

### Quick verify

```bash
bash tests/consistency.sh
bash tests/test-hooks.sh
```

## Conventions

- When adding a new workflow: update `core/metadata/workflows.json`, add the canonical file in `core/workflows/`, then add or update the provider wrappers that expose it
- Keep provider-specific files thin whenever possible; shared behavior belongs in `core/`
- Run `python3 scripts/render_workflow_tables.py` after changing workflow metadata, Claude skill metadata, help metadata, principles metadata, routing metadata, status metadata, or provider command names. `help` and `status` wrappers are rendered as full provider documents, not just partial generated blocks.
- When a command or prompt references `references/`: the Copilot version must have a `#file:` equivalent and the setup instructions must include copying that file
- Copilot prompt frontmatter uses `agent: agent` (not `mode: "agent"`)
- Commit messages: imperative mood, describe the why not just the what
- Never add Co-Authored-By trailer to commits
- PDD project structure: all PDD artifacts live under `pdd/` (prompts, context, evals). Source code goes in `src/` (or user-chosen name). See `docs/migration.md` for migration from the old layout.
