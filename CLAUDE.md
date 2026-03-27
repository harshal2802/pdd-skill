# PDD Skill — Development Notes

## What this repo is

A Claude Code skill (and Copilot adaptation) for Prompt Driven Development. The skill definition is in `SKILL.md`. Commands live in `commands/`, Copilot prompt files in `copilot/prompts/`, and project type reference files in `references/`.

## Pre-PR checklist

Run these checks before opening a PR. The goal is to catch cross-file consistency gaps — the most common source of bugs in this repo.

### Workflow parity

- [ ] Every workflow in SKILL.md has a matching file in `commands/`
- [ ] Every file in `commands/` has a matching file in `copilot/prompts/`
- [ ] Workflow count in SKILL.md matches README.md, copilot/README.md, and actual file count
- [ ] Workflow numbers in SKILL.md cross-references are correct

### File references resolve

- [ ] Every `references/*.md` path in SKILL.md and commands exists in the repo
- [ ] Every `#file:references/*.md` in Copilot prompts has a copy instruction in `copilot/README.md` setup
- [ ] Every `/project:pdd-*` in commands points to an existing command file
- [ ] Every `/pdd-*` in Copilot prompts points to an existing prompt file

### README consistency

- [ ] Every command file appears in the README command table
- [ ] Every Copilot prompt file appears in the Copilot README command table
- [ ] `copilot/README.md` setup instructions cover all files that Copilot prompts depend on

### Quick verify

```bash
# Commands ↔ Copilot prompts match
diff <(ls commands/ | sed 's/.md//' | sort) <(ls copilot/prompts/ | sed 's/.prompt.md//' | sort)

# All referenced reference files exist
for f in frontend backend mobile data-ml devops fullstack; do
  [ -f "references/$f.md" ] && echo "OK: $f" || echo "MISSING: $f"
done

# Copilot setup covers references
grep -q 'cp.*references/' copilot/README.md && echo "OK: references/ copy instruction" || echo "MISSING: references/ copy"
for f in frontend backend mobile data-ml devops fullstack; do
  grep -q "$f.md" copilot/README.md && echo "OK: $f.md listed" || echo "MISSING: $f.md"
done
```

## Conventions

- When adding a new workflow: update SKILL.md, create a command file, create a Copilot prompt file, update both READMEs, update copilot-instructions.md routing table
- When a command references `references/`: the Copilot version must have a `#file:` equivalent and the setup instructions must include copying that file
- Copilot prompt frontmatter uses `agent: agent` (not `mode: "agent"`)
- Commit messages: imperative mood, describe the why not just the what
- Never add Co-Authored-By trailer to commits
- PDD project structure: all PDD artifacts live under `pdd/` (prompts, context, evals). Source code goes in `src/` (or user-chosen name). See `docs/migration.md` for migration from the old layout.
