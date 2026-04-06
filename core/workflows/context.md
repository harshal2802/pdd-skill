# Context

## Purpose

Write or update the persistent project context layer so future prompts are grounded in real project constraints.

## Use When

- Context files do not exist yet.
- The stack, constraints, or architectural decisions have changed.
- The user wants better prompt quality and consistency.

## Inputs

- What the project is
- who it is for
- the tech stack
- quality expectations
- hard constraints and anti-patterns
- current implementation state

## Produces

- `pdd/context/project.md`
- `pdd/context/conventions.md`
- `pdd/context/decisions.md`

## Default Next Step

For simple work, move to `prompts`. For higher-risk or ambiguous work, move to `research` or `plan`.
