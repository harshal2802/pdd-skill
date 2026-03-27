# PDD Skill for GitHub Copilot

The same Prompt Driven Development workflows, adapted for GitHub Copilot Chat in VS Code.

## Setup

Copy these files into your project:

```bash
# Copy the always-on instructions
cp copilot-instructions.md <your-project>/.github/copilot-instructions.md

# Copy the prompt files
cp -r prompts/ <your-project>/.github/prompts/
```

Your project should end up with:

```
.github/
  copilot-instructions.md
  prompts/
    pdd-scaffold.prompt.md
    pdd-context.prompt.md
    pdd-search.prompt.md
    pdd-plan.prompt.md
    pdd-prompts.prompt.md
    pdd-update.prompt.md
    pdd-review.prompt.md
    pdd-eval.prompt.md
    pdd-status.prompt.md
```

## Usage

In VS Code Copilot Chat, type `/` to see available prompt files, then select one:

| Command | What it does |
|---|---|
| `/pdd-scaffold` | Set up PDD folder structure for a new project |
| `/pdd-context` | Write or update context files (project.md, conventions.md, decisions.md) |
| `/pdd-search` | Search for existing solutions before building custom features |
| `/pdd-plan` | Create an implementation plan before writing prompts |
| `/pdd-prompts` | Generate a focused feature prompt |
| `/pdd-update` | Diagnose and fix a prompt that isn't working |
| `/pdd-review` | Verify and review AI-generated code before committing |
| `/pdd-eval` | Run prompt evaluations and track pass rates |
| `/pdd-status` | Health check — what's set up, what's missing, what's stale |

The `copilot-instructions.md` file loads automatically in every Copilot Chat session, providing PDD-aware routing and core principles.

## Workflow

```mermaid
flowchart LR
    A["/pdd-scaffold"] --> B["/pdd-context"]
    B --> S{Complex?}
    S -- Yes --> C["/pdd-search"] --> D["/pdd-plan"] --> E
    S -- No --> E["/pdd-prompts"]
    E --> F["Run prompt"]
    F --> G["/pdd-review"]
    G --> H["Commit"]
    H -.-> I["/pdd-eval"]

    style S fill:#f1c40f,stroke:#d4ac0d,color:#333
    style C fill:#1abc9c,stroke:#17a589,color:#fff
    style D fill:#1abc9c,stroke:#17a589,color:#fff
    style I fill:#f4a460,stroke:#c4824a,color:#fff
```

**Quick path**: `/pdd-context` → `/pdd-prompts` → `/pdd-review` → commit. Add `/pdd-search` and `/pdd-plan` for complex features. Use `/pdd-eval` to track prompt reliability over time.

Each prompt file suggests the next step at the end, so you don't need to memorize the flow.

## Differences from the Claude Code version

| Aspect | Claude Code (SKILL.md) | Copilot (prompt files) |
|---|---|---|
| Activation | Auto-triggers on keywords | User invokes manually via `/` |
| Reference files | Loaded dynamically by type | Use `#file:` references in prompts |
| Workflow chaining | Built-in suggestions | Each file suggests the next step |
| Always-on context | Only when triggered | `copilot-instructions.md` is always loaded |

## Requirements

- VS Code with GitHub Copilot Chat extension
- Copilot Chat must have prompt file support enabled (VS Code 1.93+)
