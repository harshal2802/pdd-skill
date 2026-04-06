---
name: pdd
description: Use when the user wants Prompt Driven Development help, needs to structure AI-assisted work, create or improve prompt artifacts, or review AI-generated output before committing.
---

# Prompt Driven Development (PDD)

Use this as the Codex entrypoint for PDD workflows. This skill keeps provider-specific guidance light and leans on the shared workflow docs in `../../workflows/` plus the project-type references in `../../references/`.

## Core Workflows

The canonical workflow descriptions live here:

- `../../workflows/scaffold.md`
- `../../workflows/init.md`
- `../../workflows/context.md`
- `../../workflows/research.md`
- `../../workflows/plan.md`
- `../../workflows/prompts.md`
- `../../workflows/update.md`
- `../../workflows/review.md`
- `../../workflows/eval.md`
- `../../workflows/status.md`
- `../../workflows/help.md`

## How To Route

Map user intent to the matching workflow:

<!-- GENERATED:codex-routing-table:start -->
| If the user wants to... | Use |
|---|---|
| Start a brand new PDD project | `scaffold` |
| Add PDD to an existing repo | `init` |
| Write or refresh context files | `context` |
| Explore the problem space first | `research` |
| Break work into phases before prompting | `plan` |
| Write a feature prompt | `prompts` |
| Fix a weak prompt | `update` |
| Check generated output before commit | `review` |
| Measure prompt quality over time | `eval` |
| See what is set up or what is missing | `status` |
| Get workflow guidance | `help` |
<!-- GENERATED:codex-routing-table:end -->

## Project Type References

Load the matching reference files from `../../references/` to shape context questions, conventions, and review checklists:

- `frontend.md`
- `backend.md`
- `mobile.md`
- `data-ml.md`
- `devops.md`
- `fullstack.md`
- `library.md`
- `cli-devtools.md`
- `embedded-iot.md`
- `game-dev.md`
- `blockchain.md`
- `security.md`
- `api-platform.md`
- `desktop-gui.md`
- `compiler-lang.md`
- `robotics.md`

When a project spans multiple types, load the relevant references together and surface any convention conflicts instead of hiding them.

## General Principles

- One prompt, one job.
- Commit prompts alongside outputs.
- Update context after meaningful decisions.
- Never commit unreviewed AI output.
- Keep context truthful and current.
- Timebox exploratory prompts.

## Default Flow

For simple work:

`context -> prompts -> review`

For more complex work:

`context -> research -> plan -> prompts -> review -> eval`

## Output Expectations

- Be explicit about which PDD workflow you are using.
- Produce durable artifacts in the repo when the task calls for it.
- Suggest the next workflow after finishing the current one.
- Keep the user moving instead of leaving them with a generic explanation only.
