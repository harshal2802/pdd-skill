---
title: "Prompt Driven Development — A Practical Framework for Building with AI"
description: "PDD treats prompts as first-class artifacts. Structure your AI-assisted development with versioned prompts, persistent context, and automated review."
---

# Prompt Driven Development

**PDD is a development approach where prompts — instructions given to AI models — are treated as first-class artifacts, not throwaway inputs.**

Just as traditional development has source code, tests, and documentation, PDD has a structured set of prompts, context files, and outputs that together define how a project is built.

---

## The Problem

Without structure, AI-assisted development drifts. You re-explain the same context every session, generate code that contradicts earlier decisions, and lose the reasoning behind why things were built a certain way.

## The Solution

PDD gives you four layers:

| Layer | Purpose |
|-------|---------|
| **Context** | Permanent project briefing — stack, conventions, decisions |
| **Prompts** | Modular, single-purpose instructions for each feature |
| **Output** | Reviewed and accepted AI-generated artifacts |
| **Eval** | Validation checklists and automated checks |

## Quick Start

```bash
# Install the Claude Code skill
git clone <repository-url> .claude/skills/pdd-skill

# Add to your .claude/settings.json
echo '{ "skills": [".claude/skills/pdd-skill/SKILL.md"] }' > .claude/settings.json

# Start using PDD
# Claude auto-detects your intent, or use slash commands:
#   /project:pdd-scaffold  — new project
#   /project:pdd-init      — existing project
#   /project:pdd-help      — see all commands
```

Use this repository's clone URL, or your fork's clone URL if you are testing changes before opening a PR.

## Learn More

- **[The Philosophy Behind PDD](philosophy)** — Why structure matters, the four layers, project type flavors, and how to get started
- **[Efficiency Tips](efficiency-tips)** — Practical habits for reducing token usage and cost without changing the PDD workflow
- **[GitHub Repository](https://github.com/harshal2802/pdd-skill)** — Source code, installation instructions, and examples
- **[Copilot Version](https://github.com/harshal2802/pdd-skill/tree/main/copilot)** — Same workflows adapted for GitHub Copilot Chat

---

Built by [Harshal Chourasiya](https://www.linkedin.com/in/harshal-chourasiya-39bb0426) · [GitHub](https://github.com/harshal2802)
