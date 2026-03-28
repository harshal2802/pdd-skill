---
agent: agent
description: "Search for existing solutions before building custom features"
---

# Search Before Building

You are helping the user research existing solutions before writing a custom feature prompt. **Don't build what already exists.**

## Step 1 — Understand the need

Ask:
- What capability do you need?
- What's the integration point? (API, CLI, library, UI component)
- Any constraints? (license, size, dependencies, language)

## Step 2 — Search systematically

### Existing codebase
Search `src/`, `pdd/prompts/features/`, and source directories for similar functionality. Check `pdd/prompts/templates/` for matching patterns.

### Package ecosystem
Search the relevant package registry (npm, PyPI, crates.io, pkg.go.dev, etc.) for well-maintained options.

### MCP servers
Check if an MCP server already provides this capability (GitHub, Supabase, Vercel, Playwright, etc.).

### Framework built-ins
Check if the project's framework already includes this feature.

## Step 3 — Evaluate with decision matrix

| Option | When to use |
|---|---|
| **Adopt** | A library/tool does exactly what you need |
| **Extend** | Something close exists but needs minor customization |
| **Compose** | Combine 2-3 existing pieces to get the result |
| **Build** | Nothing exists, or existing options don't fit constraints |

Present findings:

```markdown
## Search Results: <capability>

### Option 1: <name> (Adopt / Extend / Compose / Build)
**What**: <description>
**Pros**: <benefits>
**Cons**: <drawbacks>
**Effort**: Low | Medium | High

### Recommendation
<which option and why>
```

## Step 4 — Proceed

- **Adopt**: Help install/configure
- **Extend**: Create a prompt adapting the existing solution
- **Compose**: Create a prompt chain wiring pieces together
- **Build**: Proceed to `/pdd-plan` or `/pdd-prompts`

If building, log why alternatives were rejected in `pdd/context/decisions.md`.

## Next step

*"Based on what I found, here's my recommendation. Want to proceed with <option>, or explore further?"*
