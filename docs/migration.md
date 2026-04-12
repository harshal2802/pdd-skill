# Migration Guide: PDD Project Structure

This guide covers migrating from the original PDD project layout to the new consolidated structure.

## What changed

PDD artifacts (`prompts/`, `context/`, `evals/`) now live under a single `pdd/` directory. The default source directory changed from `app/` to `src/`.

### Before (v1)

```
my-project/
├── prompts/
│   ├── features/
│   ├── templates/
│   └── experiments/
├── context/
│   ├── project.md
│   ├── conventions.md
│   └── decisions.md
├── app/
└── evals/
    ├── baselines/
    └── scripts/
```

### After (v2)

```
my-project/
├── pdd/
│   ├── prompts/
│   │   ├── features/
│   │   ├── templates/
│   │   └── experiments/
│   ├── context/
│   │   ├── project.md
│   │   ├── conventions.md
│   │   └── decisions.md
│   └── evals/
│       ├── baselines/
│       └── scripts/
├── src/
└── ...
```

## Why

- **Less clutter** — PDD files no longer compete with your application code at the project root
- **Follows conventions** — similar to `.github/`, `.vscode/`, and other tooling directories
- **Easier to manage** — one directory to `.gitignore`, share, or exclude from builds
- **`src/` default** — matches the dominant convention across most ecosystems

## Migration steps

### 1. Create the `pdd/` directory and move files

```bash
mkdir -p pdd

# Move the three PDD directories under pdd/
mv prompts pdd/prompts
mv context pdd/context
mv evals pdd/evals
```

If using git, use `git mv` instead of `mv` to preserve history:

```bash
mkdir -p pdd
git mv prompts pdd/prompts
git mv context pdd/context
git mv evals pdd/evals
```

### 2. Rename `app/` to `src/` (optional)

If you're using the default `app/` directory for AI-generated artifacts:

```bash
git mv app src
```

If you already use `src/` or another name, skip this step.

### 3. Update internal path references

Search your PDD files for old paths and update them:

```bash
# Find files with old path references
grep -r "prompts/features\|context/project\|context/conventions\|context/decisions\|evals/" pdd/

# Common replacements:
# prompts/features/  → pdd/prompts/features/
# prompts/templates/ → pdd/prompts/templates/
# prompts/experiments/ → pdd/prompts/experiments/
# context/project.md → pdd/context/project.md
# context/conventions.md → pdd/context/conventions.md
# context/decisions.md → pdd/context/decisions.md
# evals/ → pdd/evals/
# app/ → src/ (if you renamed it)
```

Files that commonly contain path references:
- `**File**:` headers in prompt files
- `**Prompt**:` headers in eval files
- Cross-references between prompts (e.g., `**Depends on**:`)
- Plan files referencing prompt paths

### 4. Update external references

If other tools or config files reference PDD paths, update those too:

- **CLAUDE.md** — any paths to context or prompt files
- **.github/copilot-instructions.md** — if using the Copilot adaptation
- **CI/CD scripts** — any scripts that read from `context/` or `prompts/`
- **IDE settings** — workspace search scopes, file watchers

### 5. Verify

```bash
# Check that all three directories moved successfully
ls pdd/prompts pdd/context pdd/evals

# Ensure no stale references remain
grep -rn "\"context/" pdd/ --include="*.md" | grep -v "pdd/context"
grep -rn "\"prompts/" pdd/ --include="*.md" | grep -v "pdd/prompts"
grep -rn "\"evals/" pdd/ --include="*.md" | grep -v "pdd/evals"
```

### 6. Commit

```bash
git add pdd/
git add -u  # stages the deletions of old paths
git commit -m "Restructure PDD layout: consolidate under pdd/, rename app/ to src/"
```

## Notes

- **No functional changes** — this is purely a directory reorganization. All workflows, commands, and prompt formats remain the same.
- **Gradual migration** — if you have a large project, you can migrate one directory at a time. The skill will work with either layout during the transition.
- **Team communication** — if others on your team use PDD, coordinate the move so everyone updates their working copies.

---

## Repo Structure Migration: Removing Compatibility Symlinks

If you previously referenced the old top-level convenience paths in scripts, docs, or config, update them to the canonical locations.

### What changed

The following root-level symlinks have been removed:

| Old path | Canonical replacement |
|---|---|
| `commands/` | `providers/claude/commands/` |
| `skills/` | `providers/claude/skills/` |
| `hooks/` | `providers/claude/hooks/` |
| `copilot/` | `providers/copilot/` |
| `references/` | `core/references/` |
| `examples/` | `core/examples/` |

Two root-level symlinks remain because they are required by their respective plugin systems:

- `.claude-plugin/` — Claude Code plugin discovery
- `plugins/pdd-skill` — Codex repo-local marketplace

### What to update

**Claude Code manual skill install** — if your `settings.json` references the old path:

```diff
- "skills": [".claude/skills/pdd-skill/skills/pdd/SKILL.md"]
+ "skills": [".claude/skills/pdd-skill/providers/claude/skills/pdd/SKILL.md"]
```

**Claude Code manual command copy:**

```diff
- cp -r .claude/skills/pdd-skill/commands/* .claude/commands/
+ cp -r .claude/skills/pdd-skill/providers/claude/commands/* .claude/commands/
```

**Copilot setup** — if you followed the old copy instructions:

```diff
- cp copilot/copilot-instructions.md <project>/.github/copilot-instructions.md
- cp -r copilot/prompts/ <project>/.github/prompts/
- cp -r references/ <project>/.github/references/
+ cp providers/copilot/copilot-instructions.md <project>/.github/copilot-instructions.md
+ cp -r providers/copilot/prompts/ <project>/.github/prompts/
+ cp -r core/references/ <project>/.github/references/
```

**Plugin installs are unaffected** — if you installed via `/plugin marketplace add`, no changes are needed.
