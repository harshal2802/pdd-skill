# PDD Examples: Task Management API

These files demonstrate a Prompt Driven Development project for a **Task Management REST API** built with Node.js, Express, and PostgreSQL.

Browse these examples to see how PDD artifacts look in practice, then adapt them for your own project.

## Table of Contents

### Context files

| File | Purpose |
|---|---|
| [context/project.md](context/project.md) | Project overview, tech stack, and quality bar |
| [context/conventions.md](context/conventions.md) | Coding standards the AI must follow |
| [context/decisions.md](context/decisions.md) | Architecture decisions with rationale |

### Feature prompts

| File | Purpose |
|---|---|
| [prompts/features/tasks/create-task-endpoint.md](prompts/features/tasks/create-task-endpoint.md) | Standalone prompt for the POST /tasks endpoint |
| [prompts/features/tasks/task-filtering-01-schema.md](prompts/features/tasks/task-filtering-01-schema.md) | Chained prompt 1/2: database query layer for filtering |
| [prompts/features/tasks/task-filtering-02-api.md](prompts/features/tasks/task-filtering-02-api.md) | Chained prompt 2/2: API endpoint that uses the query layer |

### Evals

| File | Purpose |
|---|---|
| [evals/create-task-endpoint-eval.md](evals/create-task-endpoint-eval.md) | Manual checklist to verify the create-task prompt output |

## How to use these examples

1. Read `context/project.md` first to understand the fictional project.
2. Look at the feature prompts to see how tasks are scoped and structured.
3. Notice how the chained prompts (`task-filtering-01` and `task-filtering-02`) build on each other.
4. Review the eval checklist to see how prompt output is verified before committing.

Copy any file as a starting point and replace the details with your own project.
