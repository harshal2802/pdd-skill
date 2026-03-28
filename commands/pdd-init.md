# Initialize PDD in an Existing Project

You are adding Prompt Driven Development structure to an existing project that already has code and a git repository.

**User input**: $ARGUMENTS

## Steps

1. **Verify this is an existing project.** Check for a git repo and existing source files. If the directory is empty or has no git history, suggest: *"This looks like a new project — want to use `/project:pdd-scaffold` instead?"*

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

If multiple types match, mention all and ask the user to confirm the primary type.

4. **Auto-detect the tech stack.** Read dependency files (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `pubspec.yaml`, etc.) and identify:
   - Language(s)
   - Framework(s)
   - Database (if detectable from deps or config files)
   - Deployment (if detectable from CI/CD configs, `Dockerfile`, cloud config)

5. **Identify the existing source directory.** Look for common patterns: `src/`, `app/`, `lib/`, `cmd/`, `pkg/`, or code files at the project root. Note what you find — this is informational, not something to create.

6. **Detect existing conventions.** Scan for linter/formatter configs (`.eslintrc*`, `.prettierrc*`, `biome.json`, `.editorconfig`, `ruff.toml`, `.golangci.yml`, `rustfmt.toml`, `pyproject.toml [tool.*]`) and note key settings (indentation, quote style, naming patterns).

7. **Create the `pdd/` structure:**

```bash
mkdir -p pdd/{prompts/{features,templates,experiments},context,evals/{baselines,scripts}}
touch pdd/context/project.md pdd/context/conventions.md pdd/context/decisions.md
```

Only create the `pdd/` tree. Do not create a source directory, `README.md`, or run `git init`.

8. **Present a summary** of what was detected:

```
Project type:    <detected type>
Tech stack:      <language, framework, database, deployment>
Source dir:      <detected path(s)>
Conventions:     <key settings from linter/formatter configs>
Created:         pdd/ directory structure with empty context files
```

Ask the user to confirm the detection is accurate and note anything that's wrong or missing.

9. **Suggest next step:** *"The `pdd/` structure is ready with empty context files. Run `/project:pdd-context` to fill them in — I'll use what I detected about your project as a starting point."*

## Rules

- Never create a new project directory — work in the current directory
- Never run `git init` — the project already has a repo
- Never create or modify source directories — only create `pdd/`
- Do not overwrite any existing `pdd/` files without explicit confirmation
- If detection is uncertain, say so and ask — don't guess silently
- Adapt commands for the user's platform if not bash
