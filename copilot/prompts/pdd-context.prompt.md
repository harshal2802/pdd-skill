---
mode: "agent"
description: "Write or update PDD context files (project.md, conventions.md, decisions.md)"
---

# Write PDD Context Files

You are helping the user create or update their PDD context layer. **Write what is true, not what you hope will be true.**

## If creating new context files

Ask these questions conversationally (not all at once):

1. What are you building, and who is it for?
2. What's the tech stack?
3. What does good output look like?
4. What should the AI never do or suggest?
5. What's already been built?

Then generate `context/project.md` using this template:

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

## conventions.md

Ask: *"Do you have code style preferences or patterns the AI should always follow?"*

Draft from their answer. Even 10 lines covering naming, file structure, and error handling is valuable. The user will grow it over time.

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
