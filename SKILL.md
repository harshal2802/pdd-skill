---
name: prompt-driven-development
description: >-
  Use this skill whenever the user wants to set up, manage, or work within a
  Prompt Driven Development (PDD) project. Trigger this skill when the user
  mentions PDD, wants to scaffold a new AI-assisted project, needs help writing
  a project context file, wants to create or improve prompts for features, or
  wants feedback on AI-generated output. Also trigger when the user asks how to
  organize their prompts, context files, or AI workflow -- even if they do not
  use the term PDD explicitly. Trigger for phrases like: help me structure my AI
  project, how do I work with AI on a codebase, review this AI-generated code,
  write a prompt for this feature, or I want to start building with AI tools.
  This skill covers five core workflows: scaffold project structure, write
  context files, generate feature prompts, update existing prompts, and review
  AI-generated output.
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

Once the type is identified, read the corresponding reference file and use it to enrich: context file questions and templates, conventions starter content, prompt patterns, and the review checklist.

If the project spans multiple types, load all relevant reference files. When conventions from different references conflict (e.g., file naming patterns), ask the user which convention to follow and capture the decision in `context/decisions.md`.

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

---

## Workflow 1: Scaffold Project Structure

### Detect environment first

Before outputting commands, ask or infer: **project name** (used in folder and commands), OS (affects commands), git comfort level, solo vs team, and IDE.

### Mac / Linux / WSL

```bash
mkdir -p <project-name>/{prompts/{system,features,templates,experiments},context,outputs,evals}
cd <project-name>
git init
touch context/project.md context/conventions.md context/decisions.md README.md
```

### Windows (Command Prompt)

```cmd
mkdir <project-name>\prompts\system && mkdir <project-name>\prompts\features
mkdir <project-name>\prompts\templates && mkdir <project-name>\prompts\experiments
mkdir <project-name>\context && mkdir <project-name>\outputs && mkdir <project-name>\evals
cd <project-name> && git init
type nul > context\project.md && type nul > context\conventions.md
type nul > context\decisions.md && type nul > README.md
```

### No CLI / non-technical user

Provide as a folder diagram and tell them to create manually in Finder or File Explorer:

```
my-project/
├── prompts/
│   ├── system/
│   ├── features/
│   ├── templates/
│   └── experiments/
├── context/
│   ├── project.md
│   ├── conventions.md
│   └── decisions.md
├── outputs/
├── evals/
└── README.md
```

### VS Code / Cursor users

Mention `.github/copilot-instructions.md` (Copilot) and `.clinerules` (Cline/Cursor) as native equivalents of `context/project.md` — auto-loaded by those tools.

### Folder reference

| Folder | What goes here |
|---|---|
| `prompts/system/` | Persistent AI personas and global constraints |
| `prompts/features/` | One prompt file per feature or task |
| `prompts/templates/` | Reusable prompt patterns |
| `prompts/experiments/` | Time-boxed exploratory prompts — dated, pruned weekly |
| `context/` | Permanent project briefing files |
| `outputs/` | Reviewed, committed AI-generated artifacts |
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
**File**: prompts/features/<feature-name>.md
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

Save to `prompts/features/<feature-name>.md` and commit alongside the output.

### Prompt chaining (multi-step features)

When a feature requires multiple sequential steps, create a **chain** — a numbered set of prompts where each builds on the output of the previous one.

**When to chain**: the feature has a natural order of dependencies (e.g., schema → API → UI), or the full task would exceed what a single prompt can do well.

**How to structure a chain**:

```markdown
# Chain: <feature name>
**Files**: prompts/features/<feature-name>-01-<step>.md, -02-<step>.md, ...

## Prompt 01: <first step>
<full prompt — self-contained, no dependency on later steps>

## Prompt 02: <second step>
**Depends on**: output from Prompt 01
<full prompt — reference what Prompt 01 produced as input>

## Prompt 03: <third step>
**Depends on**: output from Prompt 01 + 02
<full prompt>
```

**Rules for chains**:
- Each prompt in the chain must be independently understandable — don't rely on conversational context
- Number prompts sequentially: `feature-name-01-schema.md`, `feature-name-02-api.md`, `feature-name-03-ui.md`
- Review each step's output before running the next prompt
- If a step fails, fix it (Workflow 4) before continuing the chain

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

Run the prompt 2–3 times and compare outputs. Look for:
- **Consistent errors**: the prompt is wrong (missing context, bad constraints)
- **Inconsistent output**: the prompt is ambiguous (add examples, tighten wording)
- **Correct but unusable**: the output format doesn't match what you need

### Step 2 — Apply targeted fixes

Don't rewrite from scratch. Make the smallest change that addresses the diagnosed cause:

1. **Add missing context** — paste the relevant section from `project.md` or `conventions.md` directly into the prompt
2. **Elevate buried constraints** — move critical constraints above the task description, not below
3. **Add concrete examples** — show one input/output pair to anchor the AI's interpretation
4. **Narrow the task** — if splitting is needed, extract sub-tasks into separate prompts

### Step 3 — Rewrite and explain

Produce the improved version and explain what changed and why — not just a new prompt without reasoning.

Use this format when presenting the update:

```
## What changed
- <specific change 1>: <why>
- <specific change 2>: <why>

## Before (key section)
<the problematic part of the old prompt>

## After (key section)
<the improved version>
```

### Step 4 — Verify and version

- Run the updated prompt 2–3 times to confirm improvement
- Commit the new version with a message noting what was fixed

Versioning: *"Keep the old version commented out. If the new one works better across a few runs, delete the old."*

### When to abandon and start fresh

If more than half the prompt needs rewriting, or the fundamental approach is wrong (e.g., one prompt trying to do three jobs), start a new prompt from Workflow 3 instead of iterating. Move the old prompt to `prompts/experiments/` with a note on why it was retired.

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

### Output format

```
✅ What's good
<concrete strengths — don't skip even if problems exist>

⚠️ Issues to fix before committing
<specific problems + fixes, in priority order>

💡 Prompt improvement
<how to revise the prompt for better output next time>

📋 Next step
<one clear action>
```

*This is the default format. If the user or team prefers plain-text output without emoji, adapt accordingly.*

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
**Prompt**: prompts/features/<prompt-file>.md
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

**Level 2 — Diff comparison**

Save representative outputs from good prompt runs to `evals/baselines/`. When you update a prompt, diff the new output against the baseline to catch regressions.

```
evals/
├── baselines/
│   └── <prompt-name>-baseline.txt
└── <prompt-name>-eval.md
```

**Level 3 — Automated checks**

For mature prompts, write lightweight scripts that validate output structure:
- Does the output parse as valid code / JSON / markdown?
- Are required sections present?
- Do imports reference real packages?

Save scripts to `evals/scripts/` and run them after each generation.

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