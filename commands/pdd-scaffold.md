# Scaffold a PDD Project

You are setting up a new Prompt Driven Development project structure.

**User input**: $ARGUMENTS

## Steps

1. **Get the project name.** If provided in the user input above, use it. Otherwise ask: *"What should we call this project?"*

2. **Detect the project type** (frontend, backend, mobile, data/ML, DevOps, full-stack). Infer from user input or ask directly.

3. **Create the folder structure:**

```bash
mkdir -p <project-name>/{prompts/{features,templates,experiments},context,app,evals/{baselines,scripts}}
cd <project-name>
git init
touch context/project.md context/conventions.md context/decisions.md README.md
```

Adapt commands for the user's platform if not bash.

4. **Explain what each folder is for:**

| Folder | Purpose |
|---|---|
| `prompts/features/<area>/` | Prompt files grouped by feature area (e.g., `auth/`, `tasks/`) |
| `prompts/templates/` | Reusable prompt patterns (`.template.md` files with `<placeholder>` notation) |
| `prompts/experiments/` | Time-boxed exploratory prompts — date-prefixed (`YYYY-MM-DD-name.md`), pruned weekly |
| `context/` | Permanent project briefing files |
| `app/` | Reviewed, committed AI-generated artifacts |
| `evals/` | Prompt quality checks and output tests |
| `evals/baselines/` | Known-good outputs for diff comparison (Level 2 evals) |
| `evals/scripts/` | Automated validation scripts (Level 3 evals) |

5. **After creating the structure**, say: *"Structure is ready. The most important next step is `context/project.md` — want me to help write it? Run `/project:pdd-context` to get started."*

## Rules

- If the user already has a project directory, scaffold inside it without overwriting existing files
- Initialize git only if not already a git repo
- If a `context/project.md` already exists, warn the user and ask before overwriting
