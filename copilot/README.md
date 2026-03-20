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
    pdd-prompts.prompt.md
    pdd-update.prompt.md
    pdd-review.prompt.md
```

## Usage

In VS Code Copilot Chat, type `/` to see available prompt files, then select one:

| Command | What it does |
|---|---|
| `/pdd-scaffold` | Set up PDD folder structure for a new project |
| `/pdd-context` | Write or update context files (project.md, conventions.md, decisions.md) |
| `/pdd-prompts` | Generate a focused feature prompt |
| `/pdd-update` | Diagnose and fix a prompt that isn't working |
| `/pdd-review` | Review AI-generated code before committing |

The `copilot-instructions.md` file loads automatically in every Copilot Chat session, providing PDD-aware routing and core principles.

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
