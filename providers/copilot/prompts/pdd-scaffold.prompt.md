---
agent: agent
description: "Scaffold a new PDD project with folders, context files, and git init"
---

# Scaffold a PDD Project

You are setting up a new Prompt Driven Development project structure.

## Steps

1. Ask the user for a **project name** if not provided: *"What should we call this project?"*

2. Detect or ask the **project type** (frontend, backend, mobile, data/ML, DevOps, full-stack).

3. Ask the user what they want to call their **source directory** (default: `src`): *"What should the source/output directory be called? (default: `src`)"*

4. Create the following structure:

```bash
mkdir -p {{project-name}}/{pdd/{prompts/{features,templates,experiments},context,evals/{baselines,scripts}},src}
cd {{project-name}}
git init
touch pdd/context/project.md pdd/context/conventions.md pdd/context/decisions.md README.md
```

5. Explain the folder structure:

| Folder | Purpose |
|---|---|
| `pdd/prompts/features/<area>/` | Prompt files grouped by feature area, app, or tool (e.g., `features/auth/`, `features/tasks/`) |
| `pdd/prompts/templates/` | Reusable prompt patterns (`.template.md` files with `<placeholder>` notation) |
| `pdd/prompts/experiments/` | Time-boxed exploratory prompts — date-prefixed (`YYYY-MM-DD-name.md`), pruned weekly |
| `pdd/context/` | Permanent project briefing files |
| `src/` | Reviewed, committed AI-generated artifacts |
| `pdd/evals/` | Prompt quality checks and output tests |
| `pdd/evals/baselines/` | Known-good outputs for diff comparison (Level 2 evals) |
| `pdd/evals/scripts/` | Automated validation scripts (Level 3 evals) |

6. After creating the structure, say:
*"Structure is ready. The most important next step is `pdd/context/project.md` — want me to help write it? Use `/pdd-context` to get started."*

## Important

- Adapt commands for the user's platform if not bash (e.g., PowerShell on Windows)
- If the user already has a project directory, scaffold inside it without overwriting existing files
- Initialize git only if not already a git repo
