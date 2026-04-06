# Final Architecture Review

Use this as the reviewer-facing definition of "done" for the multi-provider restructure.

## Canonical Ownership

These are the source-of-truth locations:

- `core/workflows/` for shared workflow behavior
- `core/references/` for shared project-type guidance
- `core/examples/` for shared example projects
- `core/metadata/` for generated provider content inputs
- `providers/claude/`, `providers/copilot/`, and `providers/codex/` for provider packaging and activation surfaces

If a change affects shared PDD behavior, it should start in `core/`, not in a provider wrapper.

## Provider Ownership

The provider layer should only own what is genuinely provider-specific:

- Claude command names, hook wiring, and plugin packaging
- Copilot frontmatter, `#file:` references, and prompt-file packaging
- Codex plugin manifest, marketplace metadata, and skill routing

Claude and Copilot workflow wrappers are now rendered from shared workflow docs plus provider metadata, so they should be treated as generated adapter documents rather than hand-authored workflow specs.

## Deprecated Compatibility Paths

These root-level paths still exist only to avoid breaking current installs:

- `commands/`
- `skills/`
- `hooks/`
- `.claude-plugin/`
- `copilot/`
- `references/`
- `examples/`
- `plugins/pdd-skill`

Policy:

- keep them working
- test them as backward-compatibility shims
- do not treat them as canonical in new docs or new automation

## Review Questions

- Does the change keep shared behavior in `core/`?
- Does the change keep provider files thin and packaging-focused?
- If a compatibility path appears in a diff, is it only for backward compatibility?
- If generated provider files changed, did the canonical workflow or metadata source also change?
- Do Claude, Copilot, and Codex still expose the same workflow set?

## Release Gate

This branch is ready for PR when all of the following are true:

- `python3 scripts/render_workflow_tables.py --check` passes
- `bash tests/consistency.sh` passes
- `bash tests/test-hooks.sh` passes
- provider packaging smoke tests pass
- docs point new users at `core/` and `providers/`
- compatibility shims are clearly marked deprecated
