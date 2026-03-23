---
name: prompt-driven-development
description: >-
  Trigger when the user mentions PDD, wants to scaffold an AI-assisted project,
  write context or prompt files, improve prompts, or review AI-generated output.
  Also trigger for: "structure my AI project", "organize my prompts", or
  "review this AI code" -- even without the term PDD.
---

# Prompt Driven Development (PDD) Skill

This skill turns Claude into a PDD partner — helping users structure, operate, and improve AI-assisted development projects.

**Five core workflows:**
1. **Scaffold** — set up the project folder structure
2. **Context** — write or update context files (`project.md`, `conventions.md`, `decisions.md`)
3. **Prompts** — generate well-structured feature prompts
4. **Update** — improve or refactor an existing prompt
5. **Review** — critique AI-generated output before it gets committed

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
| "Write a prompt for this feature", "Help me prompt this" | → **Prompts** |
| "This prompt isn't working", "Can you improve this prompt?" | → **Update** |
| "Review this output", pastes code without instructions | → **Review** |
| Vague or unclear | → Ask: *"Are you starting a new project, working on a feature prompt, or reviewing something the AI generated?"* |

**If context files don't exist yet:** Don't block the user. Proceed with the requested workflow and suggest context files afterward.

### Returning to an existing PDD project

When context files already exist, check freshness first: *"Has anything changed since your context files were last updated?"* If yes → Workflow 2 before proceeding.

### Workflow transitions

After completing any workflow, suggest the natural next step:

| Just finished | Suggest next |
|---|---|
| **Scaffold** | → Workflow 2 (Context): *"Structure is ready. Want to write `context/project.md`?"* |
| **Context** | → Workflow 3 (Prompts): *"Context is set. Ready to write your first feature prompt?"* |
| **Prompts** | → Run the prompt, then → Workflow 5 (Review): *"Run this prompt and paste the output — I'll review it."* |
| **Update** | → Re-run the prompt, then → Workflow 5 (Review): *"Try the updated prompt and I'll review the new output."* |
| **Review** — issues found | → Fix code, or → Workflow 4 (Update) if the prompt needs work |
| **Review** — looks good | → Commit both prompt and output |

---

## Workflow 1: Scaffold Project Structure

Ask or infer the **project name**, then scaffold:

```bash
mkdir -p <project-name>/{prompts/{system,features,templates,experiments},context,app,evals}
cd <project-name>
git init
touch context/project.md context/conventions.md context/decisions.md README.md
```

Adapt the commands for your platform if not using bash.

### Folder reference

| Folder | What goes here |
|---|---|
| `prompts/system/` | Persistent AI personas and global constraints |
| `prompts/features/<area>/` | Prompt files grouped by feature area, app, or tool (e.g., `features/auth/`, `features/billing/`) |
| `prompts/templates/` | Reusable prompt patterns |
| `prompts/experiments/` | Time-boxed exploratory prompts — dated, pruned weekly |
| `context/` | Permanent project briefing files |
| `app/` | Reviewed, committed AI-generated artifacts |
| `evals/` | Prompt quality checks and output tests |

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
Draft from their answer, or use the type-specific starter from the reference file.

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

## Workflow 3: Generate Feature Prompts

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

**Chain failure recovery**: Fix the failing step (Workflow 4), re-run it, then re-run any downstream steps that depend on it. Don't re-run upstream steps unless they're also broken. If the failure reveals the chain's decomposition was wrong, restructure before continuing.

### Edge cases

- **Vague goal**: Help break into feature list first, then prompt the first one
- **Prompt keeps failing**: Move to Workflow 4 (Update)
- **Reusable template needed**: Save to `prompts/templates/` with `<placeholder>` notation

---

## Workflow 4: Update an Existing Prompt

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

If more than half the prompt needs rewriting, start fresh from Workflow 3 instead. Move the old prompt to `prompts/experiments/`.

---

## Workflow 5: Review AI-Generated Output

Act as a critical reviewer. Load the project type reference file for the type-specific checklist.

**If no context files exist:** Ask *"What was this supposed to do?"* then proceed. Flag that context files would make future reviews more thorough.

**If user pastes code without explanation:** Ask *"What did you prompt to get this, and what were you expecting?"*

### Universal review dimensions

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

Structure your review as: what's good (concrete strengths), issues to fix (tagged with severity, highest first), suggestions, how to improve the prompt, and one clear next step.

### Edge cases

- **Mostly good**: Say so directly — recommend committing after minor fixes
- **Fundamentally wrong**: Name the root cause, offer to rewrite the prompt
- **Very large output**: Focus on highest-risk areas (business logic, data, security) — flag what wasn't reviewed
- **User disagrees**: Acknowledge their reasoning; update if they have valid context, otherwise explain once and let them decide

---

## Evaluating Prompts (`evals/`)

The `evals/` folder tracks whether your prompts are producing consistent, quality output over time. Start simple — even a manual checklist counts.

### Three levels of evaluation

**Level 1 — Manual checklist** (start here)

Create a markdown file per prompt or feature with pass/fail criteria:

```markdown
# Eval: <prompt name>
**Prompt**: prompts/features/<area>/<prompt-file>.md
**Last run**: <date>

## Criteria
- [ ] Output compiles / runs without errors
- [ ] Matches the specified output format
- [ ] Handles the listed edge cases
- [ ] Follows project conventions
- [ ] No hallucinated imports, APIs, or functions

## Notes
<anything surprising about this run>
```

Save to `evals/<prompt-name>-eval.md`. Review after each significant prompt change.

**Level 2 — Diff comparison**: Save good outputs to `evals/baselines/`. When you update a prompt, diff new output against the baseline to catch regressions.

**Level 3 — Automated checks**: For mature prompts, write scripts that validate output structure (valid code, required sections, real imports). Save to `evals/scripts/`.

### When to evaluate

- After creating a new prompt (Workflow 3) — run it 2–3 times and fill out the checklist
- After updating a prompt (Workflow 4) — compare against baseline
- After a model update — re-run key prompts and check for drift

---

## General Principles

- **One prompt, one job.** Split if multiple concerns.
- **Commit prompts alongside outputs.** The prompt is part of the codebase.
- **Update context after every significant decision.** Stale context degrades future prompts.
- **Timebox experiments.** Older than one week: graduate or delete.
- **Never commit unreviewed output.** Treat it like a PR.
- **Context must reflect reality.** Aspirational `project.md` actively misleads.

---

## Common Situations

**"I don't know where to start"** → Ask if they have a project in mind, then Scaffold + Context or define the project first.

**"This is too complicated"** → Start with just `context/project.md`. Everything else can come later.

**"I'm mid-project and things are messy"** → Write context files for what exists now. Apply full workflow to new work only.

**"My team doesn't know about PDD"** → Start with `context/` layer — reads as plain docs, no workflow change required.

**"The prompt didn't work at all"** → Workflow 4. Diagnose before rewriting.

**"Can you just do it for me?"** → Yes — but explain each step so the user learns the pattern.