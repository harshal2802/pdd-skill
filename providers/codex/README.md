# PDD for Codex

This provider adapter packages PDD as a Codex plugin with a `pdd` skill.

## Layout

- `plugin/.codex-plugin/plugin.json` contains the Codex plugin manifest.
- `plugin/skills/pdd/SKILL.md` is the Codex-facing adapter skill.
- `plugin/references/` and `plugin/workflows/` link to the canonical `core/` content.

## Notes

This first pass keeps the Codex adapter thin by leaning on `core/workflows/` and `core/references/` instead of duplicating the full workflow content again.
