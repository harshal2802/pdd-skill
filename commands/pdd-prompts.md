# Generate a Feature Prompt

You are helping the user write a focused, single-purpose feature prompt for their PDD project.

**User input**: $ARGUMENTS

## Step 1 — Load context

If `pdd/context/project.md` exists, read it for project context. If not, proceed without it but suggest creating one afterward via `/project:pdd-context`.

Detect the project type and load the matching reference file from `references/` for type-specific prompt patterns.

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

Before writing from scratch, check `pdd/prompts/templates/` for an existing template that fits this feature type.

```markdown
# Prompt: <feature name>
**File**: pdd/prompts/features/<area>/<feature-name>.md
**Created**: <date>
**Project type**: <detected type>

## Context
<relevant parts of pdd/context/project.md, or inline context if no files exist>

## Task
<single, clear instruction — one job only>

## Input
<what the AI is working with>

## Output format
<what should be returned — be specific about structure>

## Constraints
-

## Examples (optional but recommended)
Input: <example>
Output: <example>
```

Save to `pdd/prompts/features/<area>/<feature-name>.md`. The `<area>` is a broad grouping — feature domain, app module, or tool (e.g., `auth/`, `tasks/`). Create the subfolder if needed.

## Prompt chaining (multi-step features)

When a feature has sequential dependencies (e.g., schema → API → UI):

- Number prompts: `feature-name-01-schema.md`, `-02-api.md`, `-03-ui.md`
- Each prompt includes a `**Depends on**:` line referencing prior steps
- Review each step's output before running the next

**Chain failure recovery**: Fix the failing step, re-run it, then re-run downstream steps. Don't re-run upstream unless also broken.

## Edge cases

- **Vague goal**: Help break it into a feature list first, then prompt the first one
- **Prompt keeps failing**: Suggest `/project:pdd-update` to diagnose
- **Exploratory / uncertain approach**: Save to `pdd/prompts/experiments/YYYY-MM-DD-<name>.md` instead of `features/`. Signals "temporary — evaluate within a week."
- **Reusable pattern emerging**: If you've written 2+ prompts with the same structure, extract a template to `pdd/prompts/templates/<pattern-name>.template.md` with `<placeholder>` notation for the parts that change

## Next step

After writing the prompt: *"Run this prompt and paste the output — I'll review it. Run `/project:pdd-review` when ready."* For critical prompts, also suggest creating a Level 1 eval checklist in `pdd/evals/`.
