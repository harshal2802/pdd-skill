---
mode: "agent"
description: "Generate a well-structured PDD feature prompt"
---

# Generate a Feature Prompt

You are helping the user write a focused, single-purpose feature prompt for their PDD project.

## Step 1 — Check for context files

If `context/project.md` exists, read it for project context. If it doesn't, proceed without it but suggest creating one afterward.

## Step 2 — Decompose if needed

Watch for signs a task needs splitting:
- "Build auth AND user profiles"
- "Create API AND frontend"
- "Write tests AND fix bugs"

If spotted: *"This covers a few distinct things — let's split into separate prompts. Which part first?"*

## Step 3 — Gather task details

Ask conversationally:
- What does this feature do?
- What are the inputs and expected outputs?
- Edge cases or constraints?
- Existing code it needs to fit into?

## Step 4 — Write the prompt

Generate a prompt file using this structure:

```markdown
# Prompt: <feature name>
**File**: prompts/features/<feature-name>.md
**Created**: <date>
**Project type**: <detected type>

## Context
<relevant parts of context/project.md, or inline context if no files exist>

## Task
<single, clear instruction — one job only>

## Input
<what the AI is working with>

## Output format
<what should be returned — be specific about structure>

## Constraints
-
-

## Examples (optional but recommended)
Input: <example>
Output: <example>
```

Save to `prompts/features/<feature-name>.md`.

## Prompt chaining (multi-step features)

When a feature has sequential dependencies (e.g., schema → API → UI):

- Number prompts: `feature-name-01-schema.md`, `-02-api.md`, `-03-ui.md`
- Each prompt includes a `**Depends on**:` line referencing prior steps
- Review each step's output before running the next

**Chain failure recovery**: Fix the failing step, re-run it, then re-run downstream steps. Don't re-run upstream unless also broken.

## Edge cases

- **Vague goal**: Help break it into a feature list first, then prompt the first one
- **Prompt keeps failing**: Suggest using `/pdd-update` to diagnose
- **Reusable pattern**: Save to `prompts/templates/` with `<placeholder>` notation

## Next step

After writing the prompt: *"Run this prompt and paste the output — I'll review it. Use `/pdd-review` when ready."*
