---
name: pdd-skill
description: >-
  Trigger when the user mentions PDD, wants to scaffold an AI-assisted project,
  write context or prompt files, improve prompts, or review AI-generated output.
  Also trigger for: "structure my AI project", "organize my prompts", or
  "review this AI code" -- even without the term PDD.
---

# Prompt Driven Development (PDD) Skill

This skill turns Claude into a PDD partner — helping users structure, operate, and improve AI-assisted development projects.

**Eight core workflows:**
1. **Scaffold** — set up the project folder structure
2. **Context** — write or update context files (`project.md`, `conventions.md`, `decisions.md`)
3. **Search** — research existing solutions before building custom features
4. **Plan** — decompose a feature into phases and a prompt chain strategy
5. **Prompts** — generate well-structured feature prompts
6. **Update** — improve or refactor an existing prompt
7. **Review** — verify and review AI-generated output before committing (includes automated quality checks)
8. **Eval** — run prompt evaluations and track quality over time

**Quick path**: For simple features, you only need **Context → Prompts → Review**. Search, Plan, and Eval add value for complex or critical features but are not required for every task.

---

## Project Type Detection

**Before starting any workflow**, detect the project type — this determines which reference file to load for enriched templates, conventions, and review criteria.

### How to detect

1. **Check `context/project.md`** if it exists — look at the tech stack section
2. **Infer from what the user says** — framework names, tools, or domain language
3. **If still unclear**, ask: *"What kind of project is this — web frontend, backend API, mobile app, data/ML pipeline, infrastructure, or full-stack?"*

### Project type → reference file

| Project type | Signals | Load |
|---|---|---|
| Frontend / UI | React, Vue, Angular, Svelte, CSS, Tailwind, design system | `references/frontend.md` |
| Backend / API | Node, FastAPI, Django, Rails, REST, GraphQL, gRPC, databases | `references/backend.md` |
| Mobile | iOS, Android, Swift, Kotlin, React Native, Flutter, Expo | `references/mobile.md` |
| Data / ML / AI | Python, Jupyter, pandas, PyTorch, scikit-learn, pipelines | `references/data-ml.md` |
| DevOps / Infra | Terraform, Docker, Kubernetes, CI/CD, AWS, GCP, Azure | `references/devops.md` |
| Full-stack | Frontend + backend together, Next.js, Nuxt, SvelteKit | `references/fullstack.md` + `references/frontend.md` + `references/backend.md` |
| Other / Unrecognized | Embedded, game dev, firmware, desktop, or anything not above | No reference file — use base workflows only |

Once the type is identified, read the corresponding reference file and use it to enrich: context file questions and templates, conventions starter content, prompt patterns, and the review checklist.

If the project spans multiple types, load all relevant reference files. When conventions conflict, ask the user which to follow and capture the decision in `context/decisions.md`.

**Full-stack merge priority**: When `fullstack.md`, `frontend.md`, and `backend.md` are loaded together, `fullstack.md` conventions take precedence where they overlap (e.g., naming, project structure, API design). Fall through to the frontend or backend reference only for concerns fullstack.md doesn't address.

---

## Step 0: Identify what the user needs

| If the user says... | Use workflow |
|---|---|
| "Start a new PDD project", "Set up folder structure", "How do I get started?" | → **Scaffold** |
| "Help me write my project.md", "What should my context file say?" | → **Context** |
| "Is there a library for this?", "Does something already do this?" | → **Search** |
| "Plan this feature", "How should I break this down?" | → **Plan** |
| "Write a prompt for this feature", "Help me prompt this" | → **Prompts** |
| "This prompt isn't working", "Can you improve this prompt?" | → **Update** |
| "Check this code", "Run the quality checks", "Is this ready to commit?", "Review this output", pastes code without instructions | → **Review** |
| "How is my prompt performing?", "Run the eval", "Track prompt quality" | → **Eval** |
| Vague or unclear | → Ask: *"Are you starting a new project, working on a feature prompt, or reviewing something the AI generated?"* |

**If context files don't exist yet:** Don't block the user. Proceed with the requested workflow and suggest context files afterward.

### Returning to an existing PDD project

When context files already exist, check freshness first: *"Has anything changed since your context files were last updated?"* If yes → Workflow 2 before proceeding.

### Workflow transitions

After completing any workflow, suggest the natural next step:

| Just finished | Suggest next |
|---|---|
| **Scaffold** | → Context: *"Structure is ready. Want to write `context/project.md`?"* |
| **Context** | → Search or Plan: *"Context is set. Before writing prompts — want to search for existing solutions or plan the implementation?"* |
| **Search** — adopt/extend/compose | → Help install/configure, or create a prompt adapting the solution |
| **Search** — build | → Plan: *"Nothing existing fits. Let's plan the implementation."* |
| **Plan** | → Prompts: *"Plan is set. Ready to write the first prompt? Start with Phase 1."* |
| **Prompts** | → Run the prompt 2–3 times, then → Review: *"Run this prompt, then `/project:pdd-review` to verify and review the output."* For critical prompts, create a Level 1 eval first. |
| **Update** | → Re-run the prompt, then → Review: *"Try the updated prompt and run `/project:pdd-review` on the output."* |
| **Review** — issues found | → Fix code, or → Update if the prompt needs work |
| **Review** — looks good | → Commit both prompt and output. → Eval: *"Consider running `/project:pdd-eval` to track this prompt's quality over time."* |
| **Eval** — passes | → Level up the eval if 5+ runs, or continue to next feature |
| **Eval** — fails | → Update: *"These criteria failed. Fix the prompt first."* |

---

## Workflow 1: Scaffold Project Structure

Ask or infer the **project name**, then scaffold:

```bash
mkdir -p <project-name>/{prompts/{features,templates,experiments},context,app,evals/{baselines,scripts}}
cd <project-name>
git init
touch context/project.md context/conventions.md context/decisions.md README.md
```

Adapt the commands for your platform if not using bash.

### Folder reference

| Folder | What goes here |
|---|---|
| `prompts/features/<area>/` | Prompt files grouped by feature area, app, or tool (e.g., `features/auth/`, `features/billing/`) |
| `prompts/templates/` | Reusable prompt patterns (`.template.md` files with `<placeholder>` notation) |
| `prompts/experiments/` | Time-boxed exploratory prompts — date-prefixed (`YYYY-MM-DD-name.md`), pruned weekly |
| `context/` | Permanent project briefing files |
| `app/` | Reviewed, committed AI-generated artifacts |
| `evals/` | Prompt quality checks and output tests |
| `evals/baselines/` | Known-good outputs for diff comparison (Level 2 evals) |
| `evals/scripts/` | Automated validation scripts (Level 3 evals) |

After scaffold say: *"Structure is ready. The most important next step is `context/project.md`. Want me to help write it?"*

---

## Workflow 2: Write Context Files

**Write what is true, not what you hope will be true.**

Load the project type reference file first — it contains additional type-specific questions and template extensions.

### Base questions (ask conversationally, not all at once)

1. What are you building, and who is it for?
2. What's the tech stack?
3. What does good output look like?
4. What should the AI never do or suggest?
5. What's already been built?

Then ask the type-specific questions from the reference file.

### Base `context/project.md` template

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

*Extend with type-specific sections from the reference file.*

### `context/conventions.md`

Ask: *"Do you have code style preferences or patterns the AI should always follow?"*
Draft from their answer, or use the type-specific starter from the reference file. This is also the right place for persistent AI instructions — persona definitions, global constraints, or "always/never" rules that apply across all prompts.

### `context/decisions.md`

```markdown
## Decision: <short title>
**Date**: <approximate>
**What was decided**: <the decision>
**Why**: <rationale>
**Don't suggest**: <alternatives to avoid>
```

### Updating existing context files

Read the existing files, ask what's changed (stack, decisions, constraints), and update the specific stale sections. If you can see the codebase, diff what the context claims vs. what actually exists. Add a `**Last updated**: <date>` line. Surgical updates, not rewrites — stale context actively misleads.

### Edge cases

- **Monorepo**: Root `context/project.md` for the system + `context/` inside each sub-project
- **Team project**: Prioritize `conventions.md` — pull from existing style guide or linter config
- **Context too long**: Split `project.md` (overview) + `architecture.md` (technical depth) at ~300 lines
- **Partial info**: Draft with placeholders — partial is better than none

---

## Workflow 3: Search Before Building

**Don't build what already exists.** Before writing a custom feature prompt, check whether a library, MCP server, framework built-in, or existing codebase pattern already solves the problem.

### Search order

1. **Existing codebase** — search `app/`, `prompts/features/`, and `prompts/templates/` for similar work
2. **Package ecosystem** — npm, PyPI, crates.io, pkg.go.dev, etc.
3. **MCP servers** — GitHub, Supabase, Vercel, Playwright, Context7, etc.
4. **Framework built-ins** — check if the project's framework already includes the feature

### Decision matrix

| Option | When to use | Example |
|---|---|---|
| **Adopt** | A library/tool does exactly what you need | Use `zod` for validation instead of writing custom validators |
| **Extend** | Something close exists but needs customization | Fork a template prompt, add project-specific constraints |
| **Compose** | Combine 2-3 existing pieces | Chain an MCP server with a thin wrapper |
| **Build** | Nothing exists or doesn't fit constraints | Write a custom prompt for truly novel features |

If the decision is to build, log why existing options were rejected in `context/decisions.md`.

---

## Workflow 4: Plan Before Prompting

**Plan first, prompt second.** For non-trivial features, create an implementation plan before writing any prompts. This catches missing dependencies, wrong decomposition, and implicit architectural decisions.

### When to plan

- Feature spans multiple files or layers (schema → API → UI)
- Feature has unknowns or requires architectural decisions
- Feature will need a prompt chain (3+ sequential prompts)

Skip the plan for single-prompt features — go directly to Workflow 5 (Prompts). See the **Quick path** above.

### How to plan

1. Read context files and scan existing prompts
2. Decompose into ordered phases — each phase produces one testable artifact and maps to one prompt
3. Identify risks, unknowns, and decisions needed
4. Map phases to a prompt chain: `feature-01-<phase>.md` through `feature-NN-<phase>.md`

### Plan template

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
**Depends on**: nothing | Phase N
**Risk**: Low | Medium | High — <why>
**Prompt**: `prompts/features/<area>/<feature>-01-<phase>.md`

## Risks & Unknowns
- <risk>

## Decisions Needed
- <choice to log in decisions.md>
```

Save to `prompts/features/<area>/PLAN-<feature-name>.md`. Review with the user before proceeding to prompts.

---

## Workflow 5: Generate Feature Prompts

Load the project type reference file — it contains type-specific prompt patterns and common feature templates.

### Step 1 — Decompose if needed

Signs a task needs splitting: "Build auth AND user profiles", "Create API AND frontend", "Write tests AND fix bugs."

If spotted: *"This covers a few distinct things — let's split. Which first?"*

### Step 2 — Gather task details

- What does this feature do?
- Inputs and expected outputs?
- Edge cases or constraints?
- Existing code it needs to fit into?

### Step 3 — Write the prompt

Before writing from scratch, check `prompts/templates/` for an existing template that fits this feature type.

```markdown
# Prompt: <feature name>
**File**: prompts/features/<area>/<feature-name>.md
**Created**: <date>
**Project type**: <type>

## Context
<relevant parts of context/project.md, or inline if no context files exist>

## Task
<single, clear instruction — one job only>

## Input
<what the AI is working with>

## Output format
<what should be returned>

## Constraints
-
-

## Examples (optional but recommended)
Input: <example>
Output: <example>
```

Save to `prompts/features/<area>/<feature-name>.md` and commit alongside the output. The `<area>` is a broad grouping — feature domain, app module, or tool (e.g., `auth/`, `tasks/`, `billing/`, `infra/`). Create the subfolder if it doesn't exist.

### Prompt chaining (multi-step features)

When a feature requires multiple sequential steps, create a **chain** — a numbered set of prompts where each builds on the output of the previous one.

**When to chain**: the feature has a natural order of dependencies (e.g., schema → API → UI), or the full task would exceed what a single prompt can do well.

**How to structure**: Number prompts sequentially within the same area subfolder (`<area>/feature-name-01-schema.md`, `-02-api.md`, `-03-ui.md`). Each prompt must be self-contained with a `**Depends on**:` line referencing prior steps' output. Review each step's output before running the next.

**Chain failure recovery**: Fix the failing step (Workflow 6), re-run it, then re-run any downstream steps that depend on it. Don't re-run upstream steps unless they're also broken. If the failure reveals the chain's decomposition was wrong, restructure before continuing.

### Edge cases

- **Vague goal**: Help break into feature list first, then prompt the first one
- **Prompt keeps failing**: Move to Workflow 6 (Update)
- **Exploratory / uncertain approach**: Save to `prompts/experiments/YYYY-MM-DD-<name>.md` instead of `features/`. This signals "temporary — evaluate within a week."
- **Reusable pattern emerging**: If you've written 2+ prompts with the same structure, extract a template to `prompts/templates/<pattern-name>.template.md` with `<placeholder>` notation for the parts that change

---

## Workflow 6: Update an Existing Prompt

### Diagnose first

| Symptom | Likely cause | Fix |
|---|---|---|
| Output is too generic | Missing context | Add project/tech context |
| Output ignores constraints | Constraints buried or vague | Move higher, make explicit |
| Output does too many things | Task too broad | Split into multiple prompts |
| Output format is wrong | No format specified | Add explicit output format section |
| Output drifts across runs | Prompt is ambiguous | Add examples |
| Output contradicts conventions | No conventions reference | Add link or paste from `conventions.md` |

### Step 1 — Identify the root cause

Run the prompt 2–3 times and compare outputs. Consistent errors mean the prompt is wrong; inconsistent output means it's ambiguous; correct but unusable means the format is off.

### Step 2 — Apply targeted fixes

Don't rewrite from scratch. Make the smallest change: add missing context, elevate buried constraints above the task, add a concrete example, or narrow the task by splitting.

### Step 3 — Rewrite and explain

Produce the improved version and show what changed and why — not just a new prompt without reasoning.

### Step 4 — Verify and version

- Run the updated prompt 2–3 times to confirm improvement
- Commit the new version with a message noting what was fixed

Versioning: *"Keep the old version commented out. If the new one works better across a few runs, delete the old."*

If more than half the prompt needs rewriting, start fresh from Workflow 5 instead. Move the old prompt to `prompts/experiments/` with a date prefix: `YYYY-MM-DD-<descriptive-name>.md`.

---

## Workflow 7: Review AI-Generated Output

Review combines automated quality checks with subjective code review in a single pass. Run verification first, then review what the checks can't catch.

**If no context files exist:** Ask *"What was this supposed to do?"* then proceed. Flag that context files would make future reviews more thorough.

**If user pastes code without explanation:** Ask *"What did you prompt to get this, and what were you expecting?"*

Load the project type reference file for the type-specific checklist.

### Phase 1: Automated verification

Run these checks in order. Stop at the first failure — fix before continuing.

| Check | What it checks | Tools |
|---|---|---|
| **Build** | Code compiles/builds without errors | `npm run build`, `tsc`, `go build`, `cargo build`, etc. |
| **Type check** | Passes static type checking (if applicable) | `tsc --noEmit`, `mypy`, `pyright` |
| **Lint** | No new lint warnings | ESLint, Biome, Ruff, golangci-lint, clippy |
| **Test** | Existing tests pass, new code has tests | `npm test`, `pytest`, `go test`, `cargo test` |
| **Security** | No hardcoded secrets, injection vulnerabilities, or dependency issues | Pattern scan, `npm audit`, `pip audit` |

Skip checks that don't apply (e.g., no build system, no static types). If all checks pass, proceed to Phase 2. If any fail, fix first.

### Phase 2: Subjective review

**1. Correctness** — Does it do what was asked? Unhandled edge cases? Obvious bugs?

**2. Project fit** *(if context files exist)* — Matches stack, follows conventions, no contradictions with decisions?

**3. Maintainability** — Readable? Anti-patterns? Teammate-understandable?

**4. Prompt signal** — What does this output reveal about the prompt? Fixable with better prompting?

*Then apply the type-specific checklist from the reference file.*

### Issue severity

When listing issues, tag each with a severity level so the user knows what to fix now vs. later:

| Severity | Meaning | Action |
|---|---|---|
| **Blocking** | Broken, insecure, or violates a hard constraint — will cause problems in production | Must fix before committing |
| **Should fix** | Wrong pattern, missing edge case, or convention violation — will cause problems later | Fix before or soon after committing |
| **Consider** | Style nit, minor improvement, or optional enhancement — won't cause problems | Fix if time allows, otherwise skip |

### Output format

Structure your review as: verification results (pass/fail per check), what's good (concrete strengths), issues to fix (tagged with severity, highest first), suggestions, how to improve the prompt, and one clear next step.

### Edge cases

- **Mostly good**: Say so directly — recommend committing after minor fixes
- **Fundamentally wrong**: Name the root cause, offer to rewrite the prompt
- **Very large output**: Focus on highest-risk areas (business logic, data, security) — flag what wasn't reviewed
- **User disagrees**: Acknowledge their reasoning; update if they have valid context, otherwise explain once and let them decide

---

## Workflow 8: Evaluate Prompts (`evals/`)

The `evals/` folder tracks whether your prompts produce consistent, quality output over time. Treat evals as the unit tests of AI development — define expected behavior, run continuously, track regressions.

### Three levels of evaluation

**Level 1 — Manual checklist** (start here)

```markdown
# Eval: <prompt name>
**Prompt**: prompts/features/<area>/<prompt-file>.md
**Created**: <date>
**Level**: 1 — Manual checklist

## Criteria
- [ ] Output compiles / runs without errors
- [ ] Matches the specified output format
- [ ] Handles the listed edge cases
- [ ] Follows project conventions
- [ ] No hallucinated imports, APIs, or functions
- [ ] Integrates with existing code without conflicts

## Run log
| Run | Date | Result | Notes |
|---|---|---|---|
| 1 | | | |
```

Save to `evals/<prompt-name>-eval.md`.

**Level 2 — Baseline comparison**: Save known-good outputs to `evals/baselines/`. Diff new output against the baseline to catch regressions.

**Level 3 — Automated validation**: Write scripts that check output structure, valid syntax, required sections, and forbidden patterns. Save to `evals/scripts/`.

### Pass rate tracking

After 3+ runs, track reliability metrics:
- **pass@1** — passes on first try (percentage)
- **pass@3** — passes at least once in 3 tries (percentage)

These metrics tell you whether the prompt is reliable or needs work.

### When to evaluate

- After creating a new prompt (Workflow 5) — run 2–3 times and fill out the checklist
- After updating a prompt (Workflow 6) — compare against baseline
- After a model update — re-run key prompts and check for drift

### When to level up

- **Level 1 → Level 2**: After 5+ runs, save a known-good output to `evals/baselines/`
- **Level 2 → Level 3**: When the prompt is stable and used regularly — write a validation script in `evals/scripts/`

---

## General Principles

- **One prompt, one job.** Split if multiple concerns.
- **Commit prompts alongside outputs.** The prompt is part of the codebase.
- **Update context after every significant decision.** Stale context degrades future prompts.
- **Timebox experiments.** Name with a date prefix (`YYYY-MM-DD-`). After one week: promote to `prompts/features/` if it worked, delete if it didn't.
- **Never commit unreviewed output.** Treat it like a PR.
- **Context must reflect reality.** Aspirational `project.md` actively misleads.

---

## Common Situations

**"I don't know where to start"** → Ask if they have a project in mind, then Scaffold + Context or define the project first.

**"This is too complicated"** → Start with just `context/project.md`. Everything else can come later.

**"I'm mid-project and things are messy"** → Write context files for what exists now. Apply full workflow to new work only.

**"My team doesn't know about PDD"** → Start with `context/` layer — reads as plain docs, no workflow change required.

**"The prompt didn't work at all"** → Workflow 6 (Update). Diagnose before rewriting.

**"Is this code ready to commit?"** → Workflow 7 (Review). Runs automated checks first, then detailed review.

**"How reliable is this prompt?"** → Workflow 8 (Eval). Track pass rates across runs.

**"Can you just do it for me?"** → Yes — but explain each step so the user learns the pattern.