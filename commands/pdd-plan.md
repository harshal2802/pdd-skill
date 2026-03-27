# Plan Before Prompting

You are helping the user create an implementation plan before writing any PDD prompts. **Plan first, prompt second.**

**User input**: $ARGUMENTS

## Why plan first

Jumping straight to prompts often leads to:
- Missing dependencies between features
- Wrong decomposition (prompts too large or too granular)
- Architectural decisions made implicitly instead of explicitly

A plan catches these issues before any code is generated.

## Step 1 — Load context

If `context/project.md` exists, read it along with `conventions.md` and `decisions.md`. Scan `prompts/features/` to see what's already been built. If no context files exist, proceed but flag this as a risk.

Detect the project type and load the matching reference file from `references/` for type-specific patterns.

## Step 2 — Understand the feature

Ask conversationally:
- What are you trying to build?
- What does "done" look like?
- What already exists that this connects to?
- Any unknowns or things you're unsure about?

## Step 3 — Decompose into phases

Break the feature into ordered phases. Each phase should produce one concrete, testable artifact and map to exactly one prompt.

```markdown
# Implementation Plan: <feature name>
**Created**: <date>
**Complexity**: Low | Medium | High
**Estimated prompts**: <count>

## Summary
<2-3 sentence overview of the approach>

## Phases

### Phase 1: <name>
**Produces**: <concrete artifact>
**Depends on**: nothing | Phase N | existing code
**Risk**: Low | Medium | High — <why>
**Prompt**: `prompts/features/<area>/<feature>-01-<phase>.md`

### Phase 2: <name>
...

## Risks & Unknowns
- <anything that needs investigation or a decision before proceeding>

## Decisions Needed
- <architectural choices the user must make — log in decisions.md once resolved>
```

## Step 4 — Review the plan with the user

Present the plan and ask:
- *"Does this decomposition feel right?"*
- *"Any phases that should be experiments first?"*
- *"Any decisions we should log before starting?"*

Don't proceed to prompts until the user confirms the plan.

## Step 5 — Save the plan

Save to `prompts/features/<area>/PLAN-<feature-name>.md`. This becomes the reference for the prompt chain.

## Edge cases

- **Trivial feature**: Skip the plan — suggest going directly to `/project:pdd-prompts`
- **Unknowns dominate**: Suggest an experiment prompt first (`prompts/experiments/`)
- **Plan changes mid-implementation**: Update the plan file and adjust remaining prompts
- **Multiple features**: Create separate plans — don't combine unrelated work

## Next step

After the plan is confirmed: *"Plan is set. Ready to write the first prompt? Run `/project:pdd-prompts` — start with Phase 1."*
