---
agent: agent
description: "Write or update PDD context files (project.md, conventions.md, decisions.md)"
---

# Write PDD Context Files

You are helping the user create or update their PDD context layer. **Write what is true, not what you hope will be true.**

## Detect project type first

Check `context/project.md` (if it exists) or infer from the user's language. Use `#file:` to load the matching reference file for type-specific questions and templates:

| Type | Signals | Reference |
|---|---|---|
| Frontend / UI | React, Vue, Angular, Svelte, CSS, Tailwind | `#file:references/frontend.md` |
| Backend / API | Node, FastAPI, Django, Rails, REST, GraphQL | `#file:references/backend.md` |
| Mobile | iOS, Android, Swift, Kotlin, React Native, Flutter | `#file:references/mobile.md` |
| Data / ML / AI | Python, Jupyter, pandas, PyTorch, pipelines | `#file:references/data-ml.md` |
| DevOps / Infra | Terraform, Docker, Kubernetes, CI/CD, AWS | `#file:references/devops.md` |
| Full-stack | Frontend + backend, Next.js, Nuxt, SvelteKit | `#file:references/fullstack.md` |

## If creating new context files

Ask these questions conversationally (not all at once):

1. What are you building, and who is it for?
2. What's the tech stack?
3. What does good output look like?
4. What should the AI never do or suggest?
5. What's already been built?

Then ask type-specific questions from the reference file.

Generate `context/project.md` using this template:

```markdown
# Project: <name>

## What we're building
<1-2 sentence description>

## Who it's for
<target users or stakeholders>

## Tech stack
- Language:
- Framework:
- Database:
- Deployment:

## What good output looks like
<quality bar, style expectations, standards>

## Constraints (what the AI should never do or suggest)
-
-

## Current state
<what's already built, or "Starting from scratch">
```

Extend with type-specific sections from the reference file.

## conventions.md

Ask: *"Do you have code style preferences or patterns the AI should always follow?"*

Draft from their answer. Even 10 lines covering naming, file structure, and error handling is valuable. This is also the right place for persistent AI instructions — persona definitions, global constraints, or "always/never" rules that apply across all prompts. The user will grow it over time.

## decisions.md

For each architectural decision, use this format:

```markdown
## Decision: <short title>
**Date**: <approximate>
**What was decided**: <the decision>
**Why**: <rationale>
**Don't suggest**: <alternatives to avoid>
```

## If updating existing context files

1. Read the existing files first
2. Ask what has changed (stack, decisions, constraints)
3. Update only the stale sections — surgical updates, not rewrites
4. Add `**Last updated**: <date>` to modified files
5. If you can see the codebase, diff what context claims vs. what actually exists

## Edge cases

- **Monorepo**: Root `context/project.md` for the system + `context/` inside each sub-project
- **Team project**: Prioritize `conventions.md` — pull from existing linter config or style guide
- **Context too long**: Split at ~300 lines into `project.md` (overview) + `architecture.md` (depth)
- **Partial info**: Draft with placeholders — partial context is better than none

## Next step

After writing context, suggest: *"Context is set. Ready to write your first feature prompt? Use `/pdd-prompts`."*
