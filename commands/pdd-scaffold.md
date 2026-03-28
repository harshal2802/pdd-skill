# Scaffold a PDD Project

You are setting up a new Prompt Driven Development project structure.

**User input**: $ARGUMENTS

## Steps

1. **Get the project name.** If provided in the user input above, use it. Otherwise ask: *"What should we call this project?"*

2. **Ask about the source directory name.** After getting the project name, ask: *"I'll use `src/` for your source code directory. Want a different name (e.g., `app/`, `lib/`)?"*

3. **Detect the project type** (frontend, backend, mobile, data/ML, DevOps, full-stack). Infer from user input or ask directly.

4. **Create the folder structure:**

```bash
mkdir -p <project-name>/{pdd/{prompts/{features,templates,experiments},context,evals/{baselines,scripts}},src}
cd <project-name>
git init
touch pdd/context/project.md pdd/context/conventions.md pdd/context/decisions.md README.md
```

Replace `src` with the user's chosen source directory name if they specified a different one.

Adapt commands for the user's platform if not bash.

5. **Explain what each folder is for:**

| Folder | Purpose |
|---|---|
| `pdd/prompts/features/<area>/` | Prompt files grouped by feature area (e.g., `auth/`, `tasks/`) |
| `pdd/prompts/templates/` | Reusable prompt patterns (`.template.md` files with `<placeholder>` notation) |
| `pdd/prompts/experiments/` | Time-boxed exploratory prompts — date-prefixed (`YYYY-MM-DD-name.md`), pruned weekly |
| `pdd/context/` | Permanent project briefing files |
| `src/` | Reviewed, committed AI-generated artifacts |
| `pdd/evals/` | Prompt quality checks and output tests |
| `pdd/evals/baselines/` | Known-good outputs for diff comparison (Level 2 evals) |
| `pdd/evals/scripts/` | Automated validation scripts (Level 3 evals) |

6. **After creating the structure**, say: *"Structure is ready. The most important next step is `pdd/context/project.md` — want me to help write it? Run `/project:pdd-context` to get started."*

## Rules

- If the user already has a project directory, scaffold inside it without overwriting existing files
- Initialize git only if not already a git repo
- If a `pdd/context/project.md` already exists, warn the user and ask before overwriting
