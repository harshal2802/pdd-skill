# Write PDD Context Files

You are helping the user create or update their PDD context layer. **Write what is true, not what you hope will be true.**

**User input**: $ARGUMENTS

## Detect project type first

Check `pdd/context/project.md` (if it exists) or infer from user input. Load the matching reference file from this skill's `references/` folder to get type-specific questions and templates:

| Type | Signals | Reference |
|---|---|---|
| Frontend / UI | React, Vue, Angular, Svelte, CSS, Tailwind | `references/frontend.md` |
| Backend / API | Node, FastAPI, Django, Rails, REST, GraphQL | `references/backend.md` |
| Mobile | iOS, Android, Swift, Kotlin, React Native, Flutter | `references/mobile.md` |
| Data / ML / AI | Python, Jupyter, pandas, PyTorch, pipelines | `references/data-ml.md` |
| DevOps / Infra | Terraform, Docker, Kubernetes, CI/CD, AWS | `references/devops.md` |
| Full-stack | Frontend + backend, Next.js, Nuxt, SvelteKit | `references/fullstack.md` |

## If creating new context files

Ask these questions conversationally (not all at once):

1. What are you building, and who is it for?
2. What's the tech stack?
3. What does good output look like?
4. What should the AI never do or suggest?
5. What's already been built?

Then ask type-specific questions from the reference file.

### Generate `pdd/context/project.md`

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

## Current state
<what's already built, or "Starting from scratch">
```

Extend with type-specific sections from the reference file.

### Generate `pdd/context/conventions.md`

Ask: *"Do you have code style preferences or patterns the AI should always follow?"*

Draft from their answer, or use the type-specific starter from the reference file. Even 10 lines covering naming, file structure, and error handling is valuable. This is also the right place for persistent AI instructions — persona definitions, global constraints, or "always/never" rules that apply across all prompts.

### Generate `pdd/context/decisions.md`

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

- **Monorepo**: Root `pdd/context/project.md` for the system + `pdd/context/` inside each sub-project
- **Team project**: Prioritize `conventions.md` — pull from existing linter config or style guide
- **Context too long**: Split at ~300 lines into `project.md` (overview) + `architecture.md` (depth)
- **Partial info**: Draft with placeholders — partial context is better than none

## Next step

After writing context: *"Context is set. Ready to write your first feature prompt? Run `/project:pdd-prompts`."*
