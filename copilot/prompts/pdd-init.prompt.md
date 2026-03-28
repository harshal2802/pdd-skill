---
agent: agent
description: "Initialize PDD in an existing project — detect stack, create pdd/ structure"
---

# Initialize PDD in an Existing Project

You are adding Prompt Driven Development structure to an existing project that already has code and a git repository.

## Steps

1. **Verify this is an existing project.** Check for a git repo and existing source files. If the directory is empty or has no git history, suggest: *"This looks like a new project — use `/pdd-scaffold` instead."*

2. **Guard against overwrite.** If `pdd/` already exists, warn: *"This project already has a `pdd/` directory. Want me to continue and fill in anything missing, or stop?"* Do not overwrite existing files without confirmation.

3. **Auto-detect the project type** by scanning for:

| Files / directories | Inferred type |
|---|---|
| `package.json` with React/Vue/Angular/Svelte | Frontend |
| `package.json` with Express/Fastify/Hono, or `requirements.txt` with Flask/FastAPI/Django, or `go.mod`, `Cargo.toml` with server frameworks | Backend |
| `Podfile`, `build.gradle` with Android, `pubspec.yaml`, `app.json` (Expo) | Mobile |
| `requirements.txt` with pandas/torch/scikit-learn, `setup.py` with ML deps, Jupyter notebooks | Data / ML |
| `Dockerfile`, `terraform/`, `k8s/`, `.github/workflows/`, `Pulumi.yaml` | DevOps |
| `next.config.*`, `nuxt.config.*`, `svelte.config.*`, or frontend + backend signals together | Full-stack |

If multiple types match, mention all and ask the user to confirm.

4. **Auto-detect the tech stack.** Read dependency files (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `pubspec.yaml`, etc.) and identify language(s), framework(s), database, and deployment target.

5. **Identify the existing source directory.** Look for `src/`, `app/`, `lib/`, `cmd/`, `pkg/`, or code files at the project root.

6. **Detect existing conventions.** Scan for linter/formatter configs (`.eslintrc*`, `.prettierrc*`, `biome.json`, `.editorconfig`, `ruff.toml`, `.golangci.yml`, `rustfmt.toml`, `pyproject.toml`) and note key settings.

7. **Create the `pdd/` structure:**

```bash
mkdir -p pdd/{prompts/{features,templates,experiments},context,evals/{baselines,scripts}}
touch pdd/context/project.md pdd/context/conventions.md pdd/context/decisions.md
```

Only create the `pdd/` tree. Do not create a source directory, README, or run `git init`.

8. **Present a summary** of what was detected and ask the user to confirm accuracy.

9. **Suggest next step:** *"The `pdd/` structure is ready. Use `/pdd-context` to fill in your context files — I'll use what I detected as a starting point."*

## Important

- Never create a new project directory — work in the current directory
- Never run `git init` — the project already has a repo
- Never create or modify source directories — only create `pdd/`
- Do not overwrite any existing `pdd/` files without explicit confirmation
- If detection is uncertain, say so and ask — don't guess silently
- Adapt commands for the user's platform if not bash
