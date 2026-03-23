# Prompt Driven Development (PDD) Skill

A Claude Code skill for structuring AI-assisted development with versioned prompts, persistent context, and structured review.

PDD treats prompts as first-class artifacts — not throwaway inputs. This skill gives Claude five workflows: **scaffold** a project structure, write **context** files, generate feature **prompts**, **update** failing prompts, and **review** AI-generated output before committing it.

## Installation

### Option 1 — Clone into your project (recommended)

```bash
# From your project root
git clone https://github.com/harshal2802/pdd-skill.git .claude/skills/pdd-skill
```

Then reference the skill in your `.claude/settings.json`:

```json
{
  "skills": [".claude/skills/pdd-skill/SKILL.md"]
}
```

### Option 2 — Clone standalone and reference globally

```bash
git clone https://github.com/harshal2802/pdd-skill.git ~/pdd-skill
```

Add to your global settings (`~/.claude/settings.json`):

```json
{
  "skills": ["~/pdd-skill/SKILL.md"]
}
```

## Project Structure

A PDD project looks like this:

```
my-project/
├── prompts/
│   ├── system/          # Persistent system prompts and constraints
│   ├── features/        # Prompt files grouped by area (e.g., features/auth/, features/tasks/)
│   │   ├── auth/        #   One subfolder per feature domain, app module, or tool
│   │   └── tasks/
│   ├── templates/       # Reusable prompt patterns
│   └── experiments/     # Exploratory, time-boxed prompts
├── context/
│   ├── project.md       # What you're building, why, and with what stack
│   ├── conventions.md   # Code style, naming, patterns the AI should follow
│   └── decisions.md     # Architecture decisions and the reasoning behind them
├── app/                 # Reviewed, committed AI-generated artifacts
└── evals/               # Tests for prompt quality and output correctness
```

## What's Included

| Path | Purpose |
|---|---|
| `SKILL.md` | Core skill definition — five workflows, project type detection, prompt templates |
| `references/frontend.md` | Context questions, conventions, and review checklists for frontend/UI projects |
| `references/backend.md` | Same for backend/API projects |
| `references/mobile.md` | Same for mobile (iOS, Android, cross-platform) |
| `references/data-ml.md` | Same for data science and ML projects |
| `references/devops.md` | Same for DevOps and infrastructure |
| `references/fullstack.md` | Same for full-stack projects (also loads frontend + backend refs) |
| `examples/` | Complete PDD example for a Task Management API |

The skill auto-detects your project type and loads the right reference file to enrich context questions, conventions, and review checklists.

## Example

See [`examples/task-management-api/`](examples/task-management-api/) for a complete PDD setup with filled-in context files, standalone and chained feature prompts, and an eval checklist.

## GitHub Copilot Version

This skill is also available for GitHub Copilot Chat. See [`copilot/`](copilot/) for setup instructions and prompt files that map to the same five workflows.

## Learn More

For the philosophy behind PDD, integration guides, and further reading, see [`docs/philosophy.md`](docs/philosophy.md).

## License

MIT
