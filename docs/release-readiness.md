# Release Readiness

Use this checklist before opening the multi-provider restructure PR or cutting the next release.

## Scope Of This Rollout

This branch introduces:

- a `core/` source-of-truth layer
- provider adapters under `providers/`
- Codex plugin support
- generated provider sections driven by `core/metadata/`
- generated Claude and Copilot workflow wrappers driven by shared workflow docs

## Pre-PR Checklist

- [ ] `python3 scripts/render_workflow_tables.py --check`
- [ ] `bash tests/consistency.sh`
- [ ] `bash tests/test-hooks.sh`
- [ ] Confirm `python3 tests/test_provider_packaging.py` passes directly if packaging changed
- [ ] Review generated-section changes separately from canonical metadata changes

## Pre-Release Checklist

- [ ] Confirm the target release version
- [ ] Update version fields in provider manifests if releasing a new version
- [ ] Re-check install instructions in:
  - `README.md`
  - `providers/copilot/README.md`
  - `providers/codex/README.md`
- [ ] Confirm `plugins/pdd-skill` and `.agents/plugins/marketplace.json` still line up
- [ ] Confirm `.claude-plugin/` and `plugins/pdd-skill` symlinks still resolve
- [ ] Confirm no other legacy compatibility symlinks exist at the repo root

## Reviewer Focus Areas

- Did shared behavior move into `core/` instead of being copied into another provider file?
- Do generated blocks still reflect the intended provider-specific wording?
- Do Claude, Copilot, and Codex all still expose the same workflow set?
- Did any provider-specific install path or packaging expectation change?
- Are new docs and tests targeting canonical `core/` and `providers/` locations?

## Suggested Release Notes

### User-facing

- PDD now has a cleaner multi-provider architecture with shared core content and provider adapters.
- Codex plugin support is scaffolded in-repo.
- Legacy compatibility symlinks have been removed. All docs point at canonical provider locations.

### Maintainer-facing

- High-duplication provider sections are now generated from `core/metadata/`.
- Provider packaging smoke tests now cover Claude, Copilot, and Codex install surfaces.
- The expected render-and-verify loop is documented in `docs/maintenance.md`.
- Structural verification now checks shared metadata and confirms legacy symlinks are removed.

## Suggested PR Summary

```md
This PR restructures the repo into a shared `core/` layer plus `providers/claude`, `providers/copilot`, and `providers/codex`.

It centralizes repeated provider content into `core/metadata/` and renders the highest-duplication sections back into provider wrappers, reducing manual sync work as we add Codex support. Legacy compatibility symlinks have been removed — only `.claude-plugin` and `plugins/pdd-skill` remain as functional requirements.
```
