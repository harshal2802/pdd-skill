---
title: "Efficiency Tips — Getting More from PDD Without Burning Tokens"
description: "Practical tips for reducing token usage and cost when using PDD with Claude Code or other AI tools. Covers model selection, context hygiene, and prompt design."
---

# Efficiency Tips

PDD is a methodology — it works regardless of which AI tool you use. But the way you *operate* your tool directly affects how much value you get per dollar spent. This guide covers practical habits that reduce token usage and cost without changing the PDD workflow itself.

---

## Why This Matters for PDD

PDD's four layers (Context, Prompts, Output, Eval) all consume tokens. Context files get loaded every session. Prompts generate output. Evals re-read code. Without attention to efficiency, a well-structured PDD project can still burn through budget faster than necessary.

The good news: PDD's structure already sets you up well. Modular prompts, lean context files, and focused review sessions are inherently more efficient than unstructured conversations. These tips push that advantage further.

---

## Context Hygiene

Your `pdd/context/` files are loaded at the start of every significant session. Every extra line costs tokens on every interaction.

**Keep context files lean.** Write `project.md` like a briefing memo, not a novel. If a section hasn't influenced AI output in the last few sessions, it's probably not earning its token cost.

**Split rather than grow.** Instead of one sprawling `conventions.md`, keep it focused on what applies broadly. Move domain-specific conventions into prompts that need them.

**Audit periodically.** When you run `/project:pdd-status` or review your `pdd/` directory, ask: *is everything here still pulling its weight?*

---

## Prompt Design

**One prompt, one job.** This is already a PDD principle, but it's also an efficiency one. A focused prompt that produces 50 lines of reviewed code is cheaper than a sprawling prompt that produces 500 lines you end up discarding half of.

**Front-load constraints.** Put acceptance criteria and constraints early in the prompt. This steers the AI toward the right output sooner, reducing iterations and re-prompting.

**Reference, don't repeat.** If your context files already cover conventions, don't restate them in every prompt. A line like "Follow conventions from `pdd/context/conventions.md`" is cheaper than copying the full convention list.

---

## Session Management

**Start fresh between unrelated tasks.** Stale context from a previous task wastes tokens on every subsequent message. Clear your session when switching focus.

**Compact at logical breakpoints.** If your tool supports context compaction (Claude Code's `/compact`, for example), trigger it after completing a milestone — not mid-task where you'd lose important working context.

**Use the Search and Plan workflows to front-load thinking.** A 5-minute search that finds an existing library saves an entire implementation session. A plan that catches a wrong decomposition saves multiple re-prompting cycles.

---

## Model Selection

Most AI tools now offer model tiers. The general principle:

| Task complexity | Model tier | Examples |
|---|---|---|
| Exploration, file reading, mechanical changes | Lightweight / fast | Scanning code, running checks, simple edits |
| Daily development, refactors, feature implementation | Mid-tier | Most PDD prompt and review workflows |
| Complex architecture, ambiguous requirements, deep review | Top-tier | Initial project planning, critical design decisions |

**Default to the mid-tier.** Switch up only when the task genuinely requires deeper reasoning. Switch down for exploration and routine work.

If your tool supports different models for sub-tasks (e.g., subagents), use the cheapest model that gets the job done for those.

---

## Review Efficiency

The PDD Review workflow (`/project:pdd-review`) reads generated code and runs checks. To keep this efficient:

**Review incrementally.** Review each prompt's output before moving to the next, rather than batching a full feature's output into one massive review session.

**Be specific about what to review.** "Review the auth middleware I just generated" is cheaper than "review everything in `src/`."

**Trust your evals.** If your eval baselines catch regressions automatically, you don't need to manually re-review unchanged code. Focus review time (and tokens) on what's new or changed.

---

## Tool-Specific Settings

Different tools have different knobs. Here are patterns that apply broadly:

- **Thinking/reasoning budgets**: If your tool lets you cap how much the AI "thinks" before responding, reduce it for straightforward tasks. Full reasoning is valuable for complex problems, not for simple file edits.
- **Context window thresholds**: If your tool auto-manages context, configure it to compact earlier rather than later. Running near the limit degrades output quality.
- **Plugin/extension overhead**: Each active plugin, MCP server, or extension adds tool definitions to your context. Disable what you're not using for the current project.

For Claude Code specifically, see the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for settings like model selection, thinking token budgets, and compaction thresholds.

---

## Quick Checklist

- [ ] Context files are concise — no stale or redundant sections
- [ ] Prompts are single-purpose and front-load constraints
- [ ] Sessions are cleared between unrelated tasks
- [ ] Using an appropriate model tier for the task at hand
- [ ] Reviews target specific outputs, not the entire codebase
- [ ] Unused plugins/extensions are disabled for the current project
- [ ] Compaction happens at logical breakpoints, not mid-task

---

## The PDD Advantage

Structured PDD is already more efficient than unstructured AI usage. Context files eliminate re-explanation. Modular prompts reduce wasted output. The Plan workflow catches bad decomposition before you spend tokens on it. The Search workflow avoids building what already exists.

These tips are about pushing that natural efficiency further — not about changing how PDD works, but about being intentional with the resources each session consumes.
