# Prompt Driven Development: The Philosophy

There's a quiet shift happening in how software gets built. It's not just that developers are using AI tools — it's that the *act of prompting* is becoming a core part of the development workflow itself. Some are calling this Prompt Driven Development, or PDD. And if you're using AI tools daily without a clear structure around it, you're probably leaving a lot on the table.

---

## What is Prompt Driven Development?

PDD is a development approach where prompts — instructions given to AI models — are treated as first-class artifacts, not throwaway inputs. Andrew Miller, one of the earliest writers to formalize the term, describes it as a workflow where the developer is primarily prompting an LLM to generate all necessary code, with the developer reviewing changes rather than writing code themselves. Just as traditional development has source code, tests, and documentation, PDD has a structured set of prompts, context files, and outputs that together define how a project is built.

The key mental shift: **your prompts are the source of truth**, not just a means to an end.

Microsoft's developer content team puts it similarly: prompts should be saved, documented, and versioned to capture architectural intent — just like code or design documents.

This matters because without structure, AI-assisted development tends to drift. You end up re-explaining the same context in every session, regenerating code that contradicts earlier decisions, and losing the reasoning behind why things were built a certain way. PDD solves this by making context explicit and persistent.

---

## Why Structure Matters

A common trap with AI tools is treating them like a smarter autocomplete. You type a vague request, get something plausible-looking, copy it in, and move on. This works fine for one-off tasks — but it doesn't scale.

Here's what happens without structure:

```mermaid
graph LR
    subgraph "❌ Without Structure"
        A[New Session] --> B[Re-explain context]
        B --> C[Generate code]
        C --> D[Contradicts past decisions]
        D --> A
    end

    subgraph "✅ With PDD"
        E[New Session] --> F[Load context files]
        F --> G[Focused prompt]
        G --> H[Verify & review]
        H --> I[Commit & update context]
        I --> E
    end

    style A fill:#e74c3c,stroke:#c0392b,color:#fff
    style B fill:#e74c3c,stroke:#c0392b,color:#fff
    style C fill:#e74c3c,stroke:#c0392b,color:#fff
    style D fill:#e74c3c,stroke:#c0392b,color:#fff
    style E fill:#27ae60,stroke:#1e8449,color:#fff
    style F fill:#27ae60,stroke:#1e8449,color:#fff
    style G fill:#27ae60,stroke:#1e8449,color:#fff
    style H fill:#27ae60,stroke:#1e8449,color:#fff
    style I fill:#27ae60,stroke:#1e8449,color:#fff
```

**Context drift**: Every new session starts cold. The AI doesn't know your stack, your conventions, or what you built last week.

**Decision amnesia**: You make an architectural call in conversation, it never gets written down, and three weeks later the AI (or a teammate) proposes something that contradicts it.

**Opaque outputs**: Code generated without documented intent is hard to debug, harder to hand off, and hardest to extend.

Structure doesn't slow you down. It's what lets PDD compound over time instead of creating a sprawling mess.

---

## The Four Layers

```mermaid
graph TD
    C["Context Layer\nPermanent project briefing"]
    P["Prompt Layer\nModular, single-purpose instructions"]
    O["Output Layer\nReviewed & accepted artifacts"]
    E["Eval Layer\nValidation & checklists"]

    C -->|informs| P
    P -->|generates| O
    O -->|validated by| E
    E -->|refines| C

    style C fill:#4a90d9,stroke:#2c5f8a,color:#fff
    style P fill:#7b68ee,stroke:#5a4dba,color:#fff
    style O fill:#50c878,stroke:#3a9a5c,color:#fff
    style E fill:#f4a460,stroke:#c4824a,color:#fff
```

**Context layer** is what the AI always needs to know. Think of it as the permanent briefing you'd give a new contractor on day one. It gets prepended to every significant prompt session.

**Prompt layer** is the actual instructions — kept modular and single-purpose. A prompt that tries to do five things produces worse results than five focused prompts chained together.

**Output layer** is where reviewed, accepted AI-generated code or content lives. Nothing goes here without being read and understood.

**Eval layer** is how you know your prompts are still working. Even simple checklists beat nothing.

---

## Search Before Building, Plan Before Prompting

Two of the most common failure modes in AI-assisted development:

1. **Building what already exists.** A developer prompts a custom validation layer when `zod` does the job. A team writes a custom auth flow when their framework has one built in. The AI is happy to build whatever you ask — it won't tell you not to.

2. **Prompting without a plan.** A developer writes a monolithic prompt for a feature that spans schema, API, and UI. The output is too large, too tangled, and too hard to review. Or they write prompts in the wrong order and discover halfway through that a dependency is missing.

The fix for both is the same: **slow down before you speed up.**

Before writing a prompt, check whether a library, MCP server, framework built-in, or existing codebase pattern already solves the problem. If the answer is "build it," decompose the feature into phases where each phase produces one testable artifact and maps to one prompt. The plan catches implicit decisions before they become embedded in generated code.

This doesn't apply to every feature. Simple, single-prompt tasks should skip straight to prompting. But for anything that spans multiple files or layers — search first, plan second, prompt third.

---

## Project Type Flavors

The core PDD structure is universal — it works for any kind of project. But where projects genuinely differ is in the *content* of those files and the *criteria* for good output.

```mermaid
graph TD
    PDD((PDD Core))

    PDD --> row1[ ] & row2[ ] & row3[ ] & row4[ ]

    row1 --> FE["Frontend / UI"]
    row1 --> BE["Backend / API"]
    row1 --> MO["Mobile"]

    row2 --> DA["Data / ML"]
    row2 --> DO["DevOps / Infra"]
    row2 --> FS["Full-stack"]

    row3 --> LB["Library / Package"]
    row3 --> CL["CLI / Dev Tools"]
    row3 --> EM["Embedded / IoT"]
    row3 --> GD["Game Dev"]

    row4 --> BC["Blockchain"]
    row4 --> SC["Security"]
    row4 --> AP["API Platform"]
    row4 --> DG["Desktop GUI"]
    row4 --> CO["Compiler"]

    style row1 fill:none,stroke:none
    style row2 fill:none,stroke:none
    style row3 fill:none,stroke:none
    style row4 fill:none,stroke:none
    style PDD fill:#2c3e50,stroke:#1a252f,color:#fff
    style FE fill:#3498db,stroke:#2471a3,color:#fff
    style BE fill:#9b59b6,stroke:#7d3c98,color:#fff
    style MO fill:#e67e22,stroke:#ca6f1e,color:#fff
    style DA fill:#27ae60,stroke:#1e8449,color:#fff
    style DO fill:#e74c3c,stroke:#c0392b,color:#fff
    style FS fill:#1abc9c,stroke:#17a589,color:#fff
    style LB fill:#f39c12,stroke:#d68910,color:#fff
    style CL fill:#8e44ad,stroke:#6c3483,color:#fff
    style EM fill:#d35400,stroke:#a04000,color:#fff
    style GD fill:#2ecc71,stroke:#27ae60,color:#fff
    style BC fill:#f1c40f,stroke:#d4ac0d,color:#333
    style SC fill:#c0392b,stroke:#96281b,color:#fff
    style AP fill:#2980b9,stroke:#1f6da0,color:#fff
    style DG fill:#16a085,stroke:#0e7a63,color:#fff
    style CO fill:#7f8c8d,stroke:#5d6d6e,color:#fff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
```

| Flavor | Key concerns |
|--------|-------------|
| **Frontend / UI** | Design systems, component naming, accessibility, state management |
| **Backend / API** | Schema design, auth patterns, error handling, parameterized queries |
| **Mobile** | Platform constraints, offline-first, permissions, app store readiness |
| **Data / ML** | Dataset provenance, model selection, eval metrics, pipeline idempotency |
| **DevOps / Infra** | IaC conventions, blast radius, secret management, change safety |
| **Full-stack** | Client/server boundary, shared types, API contracts |
| **Library / Package** | Public API design, semver, dependency policy, tree-shaking, multi-environment support |
| **CLI / Developer Tools** | Argument parsing, exit codes, signal handling, piped output, cross-platform behavior, shell completions |
| **Embedded / IoT** | Memory constraints, interrupt safety, power budgets, cross-compilation, OTA updates, real-time behavior |
| **Game Development** | Frame budgets, ECS architecture, asset pipelines, physics/rendering integration, platform certification |
| **Blockchain / Smart Contracts** | Security patterns (reentrancy, access control), gas optimization, upgradeability, audit readiness, on-chain math |
| **Security / Pentesting Tools** | Detection quality, false positive management, safe defaults, responsible disclosure, SIEM integration, adversarial input handling |
| **API Platform / SDK** | Backward compatibility, SDK generation, error design, rate limiting, pagination, webhooks, developer experience |
| **Desktop / Native GUI** | Window management, OS integration, code signing, auto-updates, cross-platform behavior, memory budgets, accessibility |
| **Compiler / Language Tooling** | Parsing, AST design, type systems, error recovery, source span tracking, incremental compilation, LSP integration |

A React app and a Python data pipeline both need a `project.md` and versioned prompts. What changes is what goes inside them. The Library flavor is **composable** — a React component library would combine it with the Frontend flavor, a Python ML toolkit with the Data / ML flavor.

---

## Starting a Fresh Project

**Before writing a single prompt**, set up the skeleton:

```bash
mkdir my-project && cd my-project
git init
mkdir -p pdd/{prompts/{features,templates,experiments},context,evals/{baselines,scripts}} src
touch pdd/context/project.md pdd/context/conventions.md pdd/context/decisions.md README.md
```

```mermaid
flowchart LR
    A["1. Scaffold\nDirectories & files"] --> B["2. Write context\nproject.md\nconventions.md"]
    B --> S{"Complex\nfeature?"}
    S -- Yes --> R["3. Search\nExisting solutions?"]
    R --> P["4. Plan\nDecompose into phases"]
    P --> C
    S -- No --> C["5. Write prompt\nprompts/features/area/"]
    C --> D["6. Review\nVerify + review"]
    D --> E["7. Commit both\nPrompt + output"]
    E --> F{"Decision\nmade?"}
    F -- Yes --> G["Log in\ndecisions.md"]
    F -- No --> C
    G --> C

    style A fill:#3498db,stroke:#2471a3,color:#fff
    style B fill:#3498db,stroke:#2471a3,color:#fff
    style S fill:#f1c40f,stroke:#d4ac0d,color:#333
    style R fill:#1abc9c,stroke:#17a589,color:#fff
    style P fill:#1abc9c,stroke:#17a589,color:#fff
    style C fill:#9b59b6,stroke:#7d3c98,color:#fff
    style D fill:#e67e22,stroke:#ca6f1e,color:#fff
    style E fill:#27ae60,stroke:#1e8449,color:#fff
    style F fill:#f1c40f,stroke:#d4ac0d,color:#333
    style G fill:#1abc9c,stroke:#17a589,color:#fff
```

The **quick path** for simple features is Context → Prompt → Review → Commit. For complex features, add Search and Plan before prompting — they catch missing dependencies, wrong decomposition, and "don't build what already exists" moments.

Then invest 30 minutes writing `pdd/context/project.md`. Answer these questions:
- What are we building and why?
- What's the tech stack and why those choices?
- What does good output look like here?
- What should the AI never do or suggest?

Follow that with a lean `pdd/context/conventions.md` — even 10 lines covering naming, file structure, and error handling. You'll grow it over time.

For each new feature: write a prompt in `pdd/prompts/features/<area>/`, run it, review the output, and commit both. If you made any architectural decision in the process, capture it in `pdd/context/decisions.md`.

**The ongoing discipline**: every session starts by asking — *is my context still current?*

---

## Integrating Into an Existing Project

Retrofitting PDD is trickier, but very doable if you resist doing it all at once. The **Init** workflow (`/project:pdd-init` in Claude Code, `/pdd-init` in Copilot) automates the first step — it scans your existing project, detects the tech stack, conventions, and source layout, then creates the `pdd/` structure without touching your code.

```mermaid
gantt
    title PDD Adoption Timeline
    dateFormat X
    axisFormat Week %s

    section Observe
        Log prompts & pain points           :active, w1, 1, 2

    section Initialize
        Run pdd-init & write context files  :w2, 2, 3

    section Apply
        PDD on new features only            :w3, 3, 5
```

**Week 1 — observe before changing**: Run your normal workflow, but log what you ask the AI, which prompts work well, and what context you re-explain repeatedly.

**Week 2 — initialize and build context**: Run `pdd-init` to create the `pdd/` structure and detect your project's stack. Then fill in `pdd/context/project.md` describing the project *as it currently is* and `pdd/context/decisions.md` retroactively — capturing the big decisions already made.

**Week 3 onward — apply the full workflow to new work only**: Don't PDD-ify your entire existing codebase. Apply the full workflow only to new features and significant changes.

---

## Rules of Thumb

**Don't build what already exists.** Search before prompting — a library, framework built-in, or existing pattern may already solve the problem.

**One prompt, one job.** Decompose aggressively before prompting. For complex features, write a plan first.

**Version your prompts.** A prompt that worked last week may not work after a model update.

**Document intent, not just output.** Note *why* you prompted it that way.

**Timebox experiments.** Exploratory prompts go in `/experiments` with a date. If they don't graduate within a week, delete them.

**Never treat raw output as done.** Verify it builds, passes tests, and has no security issues. Then review it like you'd review a PR.

---

## The Biggest Mistake to Avoid

Building a long, tangled single conversation and treating it as your project. Context windows end. Models get updated. Teammates can't see your chat history.

Anything important that emerges in a session — a decision, a pattern that worked, a constraint you discovered — needs to be extracted into your `pdd/context/` or `pdd/prompts/` directories before the session ends. Otherwise it's gone.

---

## Closing Thought

PDD isn't magic, and it won't replace engineering judgment. What it does is give that judgment a structured interface to work through. The developers who get the most out of it are the ones who use it to move faster on things they already understand — not to skip understanding entirely.

The analogy that keeps coming to mind: calculators didn't make math literacy less important. They raised the stakes for knowing *when* and *what* to calculate.

The same applies here. The better your prompts, context, and review discipline — the better the AI works for you.

---

## Further Reading

**Foundational PDD**
- [Andrew Miller — "Prompt Driven Development"](https://andrewships.substack.com/p/prompt-driven-development) — The original formalization of the term and workflow *(Jan 2025)*
- [VS Code / DEV Community — "Introduction to Prompt Driven Development"](https://dev.to/azure/introduction-to-prompt-driven-development-36b0) — Microsoft's formal series on PDD as an engineering practice *(Jan 2026)*
- [Capgemini Engineering — "Prompt Driven Development"](https://capgemini.github.io/ai/prompt-driven-development/) — A practitioner's account building real projects with Cline and V0 *(May 2025)*
- [Chris Perrin — "Prompt Driven Development: What We Were Really Doing All Along"](https://medium.com/@CommonDialog/prompt-driven-development-what-we-were-really-doing-all-along-accidentally-790528287705) — A reflective piece on why prompting must become a first-class citizen *(Jan 2026)*

**Related Thinking**
- [Simon Willison — "Vibe Engineering"](https://simonwillison.net/2025/Oct/7/vibe-engineering/) — The case for responsible AI-assisted development with real engineering discipline *(Oct 2025)*
- [Simon Willison — "Agentic Engineering Patterns"](https://simonw.substack.com/p/agentic-engineering-patterns) — How PDD evolves when the AI can also execute and iterate autonomously *(Feb 2026)*
- [Hexaware — "PromptOps"](https://hexaware.com/blogs/prompt-driven-development-coding-in-conversation/) — Scaling PDD across teams with prompt registries and versioning infrastructure *(2025)*

**Academic**
- [MDPI Electronics — Empirical Study on PDD](https://www.mdpi.com/2079-9292/15/4/903) — Peer-reviewed research building a full framework using only prompts, no manually written code *(March 2026)*
