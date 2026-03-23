---
mode: "agent"
description: "Scaffold a new PDD project with folders, context files, and git init"
---

# Scaffold a PDD Project

You are setting up a new Prompt Driven Development project structure.

## Steps

1. Ask the user for a **project name** if not provided: *"What should we call this project?"*

2. Detect or ask the **project type** (frontend, backend, mobile, data/ML, DevOps, full-stack).

3. Create the following structure:

```bash
mkdir -p {{project-name}}/{prompts/{system,features,templates,experiments},context,app,evals}
cd {{project-name}}
git init
touch context/project.md context/conventions.md context/decisions.md README.md
```

4. Explain the folder structure:

| Folder | Purpose |
|---|---|
| `prompts/system/` | Persistent AI personas and global constraints |
| `prompts/features/<area>/` | Prompt files grouped by feature area, app, or tool (e.g., `features/auth/`, `features/tasks/`) |
| `prompts/templates/` | Reusable prompt patterns |
| `prompts/experiments/` | Time-boxed exploratory prompts — dated, pruned weekly |
| `context/` | Permanent project briefing files |
| `app/` | Reviewed, committed AI-generated artifacts |
| `evals/` | Prompt quality checks and output tests |

5. After creating the structure, say:
*"Structure is ready. The most important next step is `context/project.md` — want me to help write it? Use `/pdd-context` to get started."*

## Important

- Adapt commands for the user's platform if not bash (e.g., PowerShell on Windows)
- If the user already has a project directory, scaffold inside it without overwriting existing files
- Initialize git only if not already a git repo
