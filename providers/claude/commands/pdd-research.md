# Research Before Building

You are helping the user explore a problem space, evaluate approaches, and decide what to build — before writing implementation prompts.

**User input**: $ARGUMENTS

## Why research first

Jumping straight from "I want feature X" to writing prompts skips the thinking that prevents wasted effort. Research clarifies what you're actually solving, what already exists, and which approach fits your constraints. Build only what's truly custom.

## Step 1 — Clarify the problem

Ask conversationally:
- What problem are you trying to solve? (not "what do you want to build" — the problem, not the solution)
- Who hits this problem and when?
- What happens today without this? (workaround, manual process, nothing?)
- What does success look like?

If the user already has a clear, specific need (e.g., "I need form validation"), skip ahead to Step 3 — they don't need problem clarification, just a solution scan.

## Step 2 — Surface requirements and constraints

Dig into what shapes the solution:
- Performance / scale requirements?
- Security or compliance constraints?
- Integration points with existing code?
- Timeline or effort budget?
- Things that are explicitly out of scope?

Capture anything non-obvious in notes — these feed into Plan and Prompts later.

## Step 3 — Scan for existing solutions

Check these sources in order:

### 3a. Existing codebase
- Does this project already have something similar?
- Search `src/`, `pdd/prompts/features/`, and `pdd/prompts/templates/`

### 3b. Package ecosystem
- Search the relevant registry (npm, PyPI, crates.io, pkg.go.dev, etc.)
- Look for well-maintained options (recent updates, active issues, good docs)

### 3c. MCP servers
- Check if an MCP server already provides this capability

### 3d. Framework built-ins
- Does the project's framework already include this?

## Step 4 — Evaluate approaches

| Approach | When to use | Example |
|---|---|---|
| **Adopt** | An existing tool does exactly what you need | Use zod for validation |
| **Extend** | Something close exists, needs minor customization | Fork a template, add constraints |
| **Compose** | Combine 2-3 existing pieces | Chain an MCP server with a wrapper |
| **Build** | Nothing fits, or constraints rule out existing options | Custom implementation |

Present findings:

```markdown
## Research: <problem being solved>

### Problem
<1-2 sentence problem statement refined from Step 1>

### Key constraints
- <from Step 2>

### Options evaluated
#### Option 1: <name> (Adopt / Extend / Compose / Build)
**What**: ...
**Pros**: ...
**Cons**: ...
**Effort**: Low | Medium | High

### Recommendation
<which approach and why, given the constraints>
```

## Step 5 — Decide and proceed

- **Adopt**: Help install/configure
- **Extend**: Create a prompt adapting the existing solution
- **Compose**: Create a prompt chain wiring existing pieces together
- **Build**: Proceed to `/project:pdd-plan` or `/project:pdd-prompts`

Log the decision and rejected alternatives in `pdd/context/decisions.md`.

Save the full research summary to `pdd/context/research/<topic>.md` if the findings will be useful for future prompts or decisions.

## Edge cases

- **User already knows what to build**: Skip Steps 1-2, go straight to solution scan
- **User wants to build anyway**: Respect their choice, log alternatives in `pdd/context/decisions.md`
- **Multiple good options**: Present comparison table, let user decide
- **No existing solutions**: Confirm search was thorough, proceed to Plan
- **Problem is too vague to research**: Help narrow it — suggest starting with one user story or use case

## Next step

After research: *"Based on what I found, here's my recommendation. Want to proceed with <option>, or explore further?"*
