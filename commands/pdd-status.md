# PDD Project Status

Check the health and completeness of the current PDD project setup.

**User input**: $ARGUMENTS

## What to check

Scan the current project directory and report on each layer:

### 1. Context layer

| Check | How |
|---|---|
| `context/project.md` exists and is non-empty | Read file, check for filled-in sections |
| `context/conventions.md` exists and is non-empty | Read file |
| `context/decisions.md` exists and has entries | Read file, count decisions |
| Context is fresh | Check for `**Last updated**` dates; flag if older than 30 days |

### 2. Prompts layer

| Check | How |
|---|---|
| `prompts/features/` has prompt files | Glob for `prompts/features/**/*.md` |
| Prompts follow the template structure | Spot-check for `## Task`, `## Context`, `## Constraints` sections |
| `prompts/experiments/` has stale entries | Flag any experiment files older than 7 days — suggest "Promote to `prompts/features/` or delete" |
| Prompt chains are complete | Check numbered sequences for gaps (e.g., `-01-` exists but `-02-` is missing) |
| Templates available | Check `prompts/templates/` for `.template.md` files. If empty but 3+ feature prompts exist with similar structure, suggest extracting a template. |

### 3. Evals layer

| Check | How |
|---|---|
| `evals/` has eval files | Glob for `evals/*.md` |
| Eval coverage | Compare prompts in `prompts/features/` vs evals — flag prompts without evals |

### 4. Output layer

| Check | How |
|---|---|
| `app/` has committed artifacts | Check if `app/` has files |
| Uncommitted AI output | Check git status for untracked files outside the PDD structure |

## Output format

```
## PDD Status: <project name>

### Context  [OK / NEEDS ATTENTION]
- project.md: <status>
- conventions.md: <status>
- decisions.md: <status>

### Prompts  [OK / NEEDS ATTENTION]
- Feature prompts: <count> across <areas count> areas
- Experiments: <count> (<stale count> stale)
- Chains: <complete/incomplete>

### Evals  [OK / NEEDS ATTENTION]
- Eval files: <count>
- Coverage: <prompts with evals> / <total prompts>

### Suggestions
- <actionable next step>
- <actionable next step>
```

Keep the output concise. Only flag problems and suggest the single most impactful next action.
