# Search Before Building

You are helping the user research existing solutions before writing a custom feature prompt. **Don't build what already exists.**

**User input**: $ARGUMENTS

## Why search first

Building custom code when a library, MCP server, or existing pattern already does the job wastes time and adds maintenance burden. Search first, build only what's truly custom.

## Step 1 — Understand the need

Ask:
- What capability do you need?
- What's the integration point? (API, CLI, library, UI component)
- Any constraints? (license, size, dependencies, language)

## Step 2 — Search systematically

Check these sources in order:

### 2a. Existing codebase
- Does this project already have something similar? Search `src/`, `pdd/prompts/features/`, and source directories
- Is there a pattern in `pdd/prompts/templates/` that covers this?

### 2b. Package ecosystem
- Search the relevant package registry:
  - npm (Node/JS/TS)
  - PyPI (Python)
  - crates.io (Rust)
  - pkg.go.dev (Go)
  - Maven/Gradle (Java/Kotlin)
  - RubyGems (Ruby)
- Look for well-maintained options (recent updates, active issues, good docs)

### 2c. MCP servers
- Check if an MCP server already provides this capability
- Common MCP servers: GitHub, Supabase, Vercel, Playwright, Firecrawl, Context7

### 2d. Framework built-ins
- Does the project's framework already include this feature?
- Check framework docs before building custom solutions

## Step 3 — Evaluate options

Use this decision matrix:

| Option | When to use | Example |
|---|---|---|
| **Adopt** | A library/tool does exactly what you need | Use `zod` for validation instead of writing custom validators |
| **Extend** | Something close exists but needs minor customization | Fork a template prompt, add project-specific constraints |
| **Compose** | Combine 2-3 existing pieces to get the result | Chain an MCP server with a thin wrapper |
| **Build** | Nothing exists, or existing options don't fit constraints | Write a custom prompt for truly novel features |

Present findings as:

```markdown
## Search Results: <capability needed>

### Option 1: <name> (Adopt / Extend / Compose / Build)
**What**: <description>
**Pros**: <benefits>
**Cons**: <drawbacks>
**Effort**: Low | Medium | High

### Option 2: <name>
...

### Recommendation
<which option and why>
```

## Step 4 — Proceed based on result

- **Adopt**: Help install/configure the existing solution
- **Extend**: Create a prompt that adapts the existing solution
- **Compose**: Create a prompt chain that wires existing pieces together
- **Build**: Proceed to `/project:pdd-plan` or `/project:pdd-prompts` for the custom implementation

If the decision is to build, log *why* existing options were rejected in `pdd/context/decisions.md`.

## Edge cases

- **User wants to build anyway**: Respect their choice, but log the alternatives in `pdd/context/decisions.md` for future reference
- **Multiple good options**: Present a comparison table and let the user decide
- **No results found**: Confirm the search was thorough, then proceed to build
- **Existing code is close but outdated**: Suggest updating existing code vs. building from scratch

## Next step

After search: *"Based on what I found, here's my recommendation. Want to proceed with <option>, or explore further?"*
