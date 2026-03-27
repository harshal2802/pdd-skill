---
agent: agent
description: "Create an implementation plan before writing PDD prompts"
---

# Plan Before Prompting

You are helping the user create an implementation plan before writing any PDD prompts. **Plan first, prompt second.**

## Why plan first

Jumping straight to prompts leads to missing dependencies, wrong decomposition, and implicit architectural decisions. A plan catches these before any code is generated.

## Step 1 — Load context

If `pdd/context/project.md` exists, read it along with `conventions.md` and `decisions.md`. Scan `pdd/prompts/features/` to see what already exists.

## Step 2 — Understand the feature

Ask conversationally:
- What are you trying to build?
- What does "done" look like?
- What already exists that this connects to?
- Any unknowns or things you're unsure about?

## Step 3 — Decompose into phases

Break the feature into ordered phases. Each phase produces one concrete, testable artifact and maps to exactly one prompt.

```markdown
# Implementation Plan: <feature name>
**Created**: <date>
**Complexity**: Low | Medium | High
**Estimated prompts**: <count>

## Summary
<2-3 sentence overview>

## Phases

### Phase 1: <name>
**Produces**: <artifact>
**Depends on**: nothing | Phase N | existing code
**Risk**: Low | Medium | High — <why>
**Prompt**: `pdd/prompts/features/<area>/<feature>-01-<phase>.md`

### Phase 2: <name>
...

## Risks & Unknowns
- <anything needing investigation>

## Decisions Needed
- <choices to log in decisions.md>
```

## Step 4 — Review with the user

Present the plan and ask:
- *"Does this decomposition feel right?"*
- *"Any phases that should be experiments first?"*
- *"Any decisions we should log before starting?"*

## Step 5 — Save the plan

Save to `pdd/prompts/features/<area>/PLAN-<feature-name>.md`.

## Edge cases

- **Trivial feature**: Skip the plan — go directly to `/pdd-prompts`
- **Unknowns dominate**: Suggest an experiment prompt first
- **Plan changes mid-implementation**: Update the plan file and adjust remaining prompts

## Next step

After plan is confirmed: *"Plan is set. Ready to write the first prompt? Use `/pdd-prompts` — start with Phase 1."*
