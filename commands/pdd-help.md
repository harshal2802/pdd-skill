# PDD Help

Quick reference for all PDD commands, workflow order, and usage guidance.

**User input**: $ARGUMENTS

## If the user passed an argument

If `$ARGUMENTS` names a specific command (e.g., "context", "pdd-context", "review"), show detailed help for that command only:

- **What it does** — one-paragraph description
- **When to use it** — the situation that calls for this workflow
- **Inputs it expects** — what the user should provide or have ready
- **What it produces** — the output artifact(s)
- **Typical next step** — what command usually follows

Use the command table and routing guide below to compose the answer. Give the user just what they asked about — don't dump the full help.

## If no argument was provided

Show the full quick reference below.

---

### Quick start

> **Quick start**: For most features, you only need three commands: **Context → Prompts → Review**. Add Research, Plan, and Eval for complex or critical features.

### All commands

**Getting started**

| Command | What it does |
|---|---|
| `/project:pdd-help` | Show this quick reference |
| `/project:pdd-scaffold` | Set up a new PDD project with folders, context stubs, and git init |
| `/project:pdd-init` | Add PDD to an existing project — auto-detects stack and conventions |
| `/project:pdd-status` | Health check — shows what's set up, what's missing, and what's stale |

**Building features**

| Command | What it does |
|---|---|
| `/project:pdd-context` | Write or update context files (project.md, conventions.md, decisions.md) |
| `/project:pdd-research` | Explore problem space, evaluate approaches, decide what to build |
| `/project:pdd-plan` | Decompose a feature into phases and prompt chain strategy |
| `/project:pdd-prompts` | Generate well-structured feature prompts |
| `/project:pdd-update` | Improve or refactor an existing prompt |

**Quality**

| Command | What it does |
|---|---|
| `/project:pdd-review` | Verify AI-generated output before committing |
| `/project:pdd-eval` | Run prompt evaluations and track quality over time |

### "What should I use?"

| I want to... | Use |
|---|---|
| Start a brand new project | `pdd-scaffold` → `pdd-context` |
| Add PDD to an existing codebase | `pdd-init` → `pdd-context` |
| Build a new feature (complex) | `pdd-context` → `pdd-research` → `pdd-plan` → `pdd-prompts` → `pdd-review` |
| Build a new feature (simple) | `pdd-context` → `pdd-prompts` → `pdd-review` |
| Fix a prompt that isn't working | `pdd-update` |
| Check if my project setup is complete | `pdd-status` |
| Track prompt quality over time | `pdd-eval` |

### Per-command detail

Use this table when the user asks about a specific command.

| Command | When to use | Inputs | Produces | Next step |
|---|---|---|---|---|
| `pdd-scaffold` | Starting a brand new project from scratch | Project name (optional) | Folder structure with context stubs | `pdd-context` |
| `pdd-init` | Adding PDD to a project that already has code | Existing project directory | PDD folders + auto-detected context | `pdd-context` |
| `pdd-context` | Before writing prompts, or when the project changes | Answers to context questions | `pdd/context/project.md`, `conventions.md`, `decisions.md` | `pdd-research` or `pdd-prompts` |
| `pdd-research` | Before building — clarify the problem, evaluate approaches | Problem description or feature idea | Research summary + approach recommendation | `pdd-plan` or `pdd-prompts` |
| `pdd-plan` | Feature spans multiple files, modules, or phases | Feature description + context files | Phased implementation plan with prompt chain strategy | `pdd-prompts` |
| `pdd-prompts` | Ready to write the actual feature prompt | Feature description + context files | Prompt file(s) in `pdd/prompts/features/` | Run the prompt, then `pdd-review` |
| `pdd-update` | A prompt isn't producing good results | The failing prompt + what went wrong | Updated prompt file | Run the prompt again, then `pdd-review` |
| `pdd-review` | AI generated code and you want to verify it | Generated code (pasted or in files) | Quality report + fix suggestions | Commit or iterate |
| `pdd-eval` | After committing, to track prompt reliability | Prompt file + expected outcomes | Eval results in `pdd/evals/` | Update prompt if quality drops |
| `pdd-status` | Want to check project health | None | Status report with suggestions | Whatever the report recommends |
| `pdd-help` | Want to see available commands | Command name (optional) | This reference | Whatever workflow fits |
