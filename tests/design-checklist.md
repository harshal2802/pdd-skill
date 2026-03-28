# PDD Skill Design Checklist

**Last updated**: 2026-03-27
**Scope**: Design review checklist covering all workflows, cross-file consistency, and edge cases

---

## Summary

| Area | Test Cases | Notes |
|---|---|---|
| Trigger / Frontmatter | 8 | Skill activation signals |
| Project Type Detection | 12 | Type inference and reference loading |
| Step 0: Workflow Routing | 8 | Intent → workflow mapping |
| Workflow 1: Scaffold | 10 | Folder structure and platform support |
| Workflow 2: Context | 14 | Context file creation and updates |
| Workflow 3: Search | 6 | Existing solution research |
| Workflow 4: Plan | 7 | Feature decomposition |
| Workflow 5: Prompts | 11 | Prompt generation and chaining |
| Workflow 6: Update | 9 | Prompt diagnosis and improvement |
| Workflow 7: Review | 13 | Automated verification + subjective review |
| Workflow 8: Eval | 8 | Evaluation levels and pass rate tracking |
| Reference Files | 12 | Type-specific enrichment |
| Cross-file Consistency | 14 | Dependencies between SKILL.md, commands, Copilot, README |
| Cross-cutting / Edge Cases | 10 | Transitions, session re-entry, quick path |

---

## 1. Trigger / Frontmatter (8 tests)

| # | Test Case | Input | Expected | Result |
|---|---|---|---|---|
| 1.1 | Explicit PDD mention | "Help me with PDD" | Skill triggers | |
| 1.2 | Scaffold request | "Set up a new AI project" | Skill triggers | |
| 1.3 | Context file request | "Help me write my project.md" | Skill triggers | |
| 1.4 | Prompt writing request | "Write a prompt for this feature" | Skill triggers | |
| 1.5 | Review request | "Review this AI-generated code" | Skill triggers | |
| 1.6 | Indirect phrasing | "How do I structure my AI project?" | Skill triggers | |
| 1.7 | Vague AI workflow | "I want to start building with AI tools" | Skill triggers | |
| 1.8 | Unrelated request | "Help me debug this Python script" | Skill does NOT trigger | |

---

## 2. Project Type Detection (12 tests)

| # | Test Case | Signal | Expected | Result |
|---|---|---|---|---|
| 2.1 | Frontend from project.md | project.md contains "React 18, Tailwind" | Load `references/frontend.md` | |
| 2.2 | Backend from user speech | "I'm building an Express API" | Load `references/backend.md` | |
| 2.3 | Mobile from framework | "React Native with Expo" | Load `references/mobile.md` | |
| 2.4 | Data/ML from tools | "Using pandas and PyTorch" | Load `references/data-ml.md` | |
| 2.5 | DevOps from tools | "Terraform + Kubernetes" | Load `references/devops.md` | |
| 2.6 | Full-stack from framework | "Next.js app" | Load `fullstack.md` + `frontend.md` + `backend.md` | |
| 2.7 | Ambiguous signal | "Python project" | Ask for clarification | |
| 2.8 | No signal | User says nothing about stack | Ask: "What kind of project is this?" | |
| 2.9 | Multi-type project | "Terraform for infra + React dashboard" | Load DevOps + Frontend references | |
| 2.10 | Conflicting conventions | DevOps kebab-case vs Frontend PascalCase | Ask user which to follow | |
| 2.11 | Unknown type | "I'm building Arduino firmware" | Proceed with base workflows only, no reference file | |
| 2.12 | Type changes mid-session | Starts backend, later mentions frontend | Re-detect and load additional references | |

---

## 3. Step 0: Workflow Routing (8 tests)

| # | Test Case | User Input | Expected Workflow | Result |
|---|---|---|---|---|
| 3.1 | Explicit scaffold | "Start a new PDD project" | Workflow 1: Scaffold | |
| 3.2 | Context file help | "Help me write my project.md" | Workflow 2: Context | |
| 3.3 | Search for existing | "Is there a library for this?" | Workflow 3: Search | |
| 3.4 | Plan a feature | "How should I break this down?" | Workflow 4: Plan | |
| 3.5 | Feature prompt | "Write a prompt for user authentication" | Workflow 5: Prompts | |
| 3.6 | Prompt fix | "This prompt isn't working" | Workflow 6: Update | |
| 3.7 | Review/verify request | "Is this code ready to commit?" | Workflow 7: Review | |
| 3.8 | Vague input | "Help me with my project" | Ask clarifying question | |

---

## 4. Workflow 1: Scaffold (10 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 4.1 | Mac/Linux scaffold | User on macOS | `mkdir -p` with correct structure | |
| 4.2 | Windows CMD scaffold | User on Windows CMD | `mkdir` with backslashes | |
| 4.3 | Non-technical user | "I don't use the terminal" | Folder diagram for manual creation | |
| 4.4 | Custom project name | User says "call it task-api" | `<project-name>` replaced correctly | |
| 4.5 | Post-scaffold prompt | After scaffold completes | Suggests writing `pdd/context/project.md` | |
| 4.6 | Git init included | Any scaffold | `git init` is part of commands | |
| 4.7 | All folders created | Any scaffold | pdd/{prompts/{features/,templates/,experiments/},context/,evals/{baselines,scripts}}, src/ | |
| 4.8 | Evals subdirectories | Any scaffold | `pdd/evals/baselines/` and `pdd/evals/scripts/` created | |
| 4.9 | PowerShell support | User on Windows PowerShell | PowerShell-compatible commands | |
| 4.10 | Team vs solo | User says "team project" | Notes team-specific considerations | |

---

## 5. Workflow 2: Context Files (14 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 5.1 | Base questions asked | New project | 5 base questions asked conversationally | |
| 5.2 | Type-specific questions | Frontend project detected | Frontend questions from reference file | |
| 5.3 | project.md template | User provides answers | Template filled with answers | |
| 5.4 | conventions.md from user | User has preferences | Draft from their answer | |
| 5.5 | conventions.md starter | User has no preferences | Type-specific starter from reference | |
| 5.6 | decisions.md format | Architectural decision made | Date, what, why, don't-suggest | |
| 5.7 | Monorepo edge case | User has monorepo | Root context + per-sub-project context | |
| 5.8 | Team project | "We're a team" | Prioritize conventions.md | |
| 5.9 | Context too long | project.md exceeds ~300 lines | Split into project.md + architecture.md | |
| 5.10 | Partial info | Doesn't know full stack | Draft with placeholders | |
| 5.11 | "Write what is true" | Aspirational description | Push back — write current reality | |
| 5.12 | Extended sections | Backend project | Backend-specific sections in template | |
| 5.13 | Questions not all at once | Any project | Asked conversationally | |
| 5.14 | Updating stale context | Project has evolved | Guide user to diff and update stale sections | |

---

## 6. Workflow 3: Search (6 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 6.1 | Search order followed | Any search | Codebase → packages → MCP servers → framework built-ins | |
| 6.2 | Adopt recommendation | Library does exactly what's needed | Recommend adopting, help install | |
| 6.3 | Build recommendation | Nothing fits | Log why in decisions.md, proceed to Plan or Prompts | |
| 6.4 | Compose recommendation | 2-3 pieces can be combined | Create prompt chain wiring them together | |
| 6.5 | User wants to build anyway | Overrides recommendation | Respect choice, log alternatives in decisions.md | |
| 6.6 | Decision matrix presented | Multiple options found | Comparison table with Adopt/Extend/Compose/Build | |

---

## 7. Workflow 4: Plan (7 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 7.1 | Phase decomposition | Multi-file feature | Ordered phases, each with one artifact | |
| 7.2 | Prompt chain mapping | 3-phase plan | Maps to `feature-01-`, `-02-`, `-03-` | |
| 7.3 | Risks identified | Unknown dependency | Flagged in Risks & Unknowns section | |
| 7.4 | Plan saved | Plan confirmed | Saved to `pdd/prompts/features/<area>/PLAN-<name>.md` | |
| 7.5 | Trivial feature skip | Single-prompt feature | Suggests skipping plan, go to Prompts | |
| 7.6 | User review before proceeding | Plan generated | User confirms before any prompts are written | |
| 7.7 | Unknowns dominate | Too many unknowns | Suggests experiment prompt first | |

---

## 8. Workflow 5: Prompts (11 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 8.1 | Single-job prompt | "Add user search" | One focused prompt generated | |
| 8.2 | Multi-concern detected | "Build auth AND user profiles" | Suggests splitting | |
| 8.3 | Prompt template used | Any feature prompt | Follows template structure | |
| 8.4 | File path convention | Feature prompt | Saved to `pdd/prompts/features/<area>/<feature-name>.md` | |
| 8.5 | Context referenced | Context files exist | Prompt references project.md | |
| 8.6 | No context files | Fresh project | Inline context + suggest creating files | |
| 8.7 | Prompt chaining | Multi-step feature | Numbered chain: -01-, -02- | |
| 8.8 | Chain independence | Each prompt in chain | Self-contained, independently runnable | |
| 8.9 | Vague goal | "Make the app better" | Break into feature list first | |
| 8.10 | Reusable template | Pattern emerging | Save to `pdd/prompts/templates/` | |
| 8.11 | Chain failure recovery | Step 2 of 3 fails | Fix failing step, re-run, verify downstream | |

---

## 9. Workflow 6: Update (9 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 9.1 | Diagnosis table used | "Output is too generic" | Identifies "missing context" | |
| 9.2 | Run 2-3 times | Inconsistent output | Identifies ambiguity | |
| 9.3 | Fix — add context | Missing project context | Paste from project.md | |
| 9.4 | Fix — elevate constraints | Constraints buried | Move above task | |
| 9.5 | Fix — add examples | Ambiguous output | Add input/output pair | |
| 9.6 | Fix — narrow task | Task too broad | Split into sub-prompts | |
| 9.7 | Before/After shown | Any update | Shows what changed and why | |
| 9.8 | Abandon threshold | >50% needs rewriting | Start fresh, move old to experiments/ | |
| 9.9 | Versioning advice | After update | Keep old commented out | |

---

## 10. Workflow 7: Review (13 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 10.1 | Phase 1 runs first | Any review | Automated checks before subjective review | |
| 10.2 | Build check | Code has build errors | FAIL, stops before Phase 2 | |
| 10.3 | Type check | TypeScript errors | FAIL at type check phase | |
| 10.4 | Lint check | Lint warnings | FAIL or auto-fix | |
| 10.5 | Test check | Tests fail | FAIL, shows which tests | |
| 10.6 | Security check | Hardcoded API key | FAIL, flags the secret | |
| 10.7 | Checks skipped when N/A | No build system | Build and type check skipped | |
| 10.8 | Correctness dimension | Phase 2 | Does it do what was asked? | |
| 10.9 | Project fit dimension | Context files exist | Matches stack, follows conventions | |
| 10.10 | Severity tagging | Issues found | Every issue tagged: Blocking/Should fix/Consider | |
| 10.11 | No context files | Fresh project | Ask "What was this supposed to do?" | |
| 10.12 | Code paste, no explanation | User pastes code only | Ask what they prompted and expected | |
| 10.13 | Type-specific checklist | Backend project | Backend checklist from reference applied | |

---

## 11. Workflow 8: Eval (8 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 11.1 | Level 1 — checklist | New prompt | Pass/fail criteria checklist created | |
| 11.2 | Level 2 — baseline | 5+ runs | Known-good output saved to `pdd/evals/baselines/` | |
| 11.3 | Level 3 — automated | Stable prompt | Validation script in `pdd/evals/scripts/` | |
| 11.4 | Run log tracked | Each eval run | Logged in run log table | |
| 11.5 | Pass rate calculated | 3+ runs | pass@1 and pass@3 percentages | |
| 11.6 | Eval after new prompt | Workflow 5 completed | Suggest creating Level 1 eval | |
| 11.7 | Eval after model update | Model changes | Re-run key prompts, check for drift | |
| 11.8 | Level promotion criteria | Enough runs accumulated | Clear guidance: 5+ → Level 2, stable → Level 3 | |

---

## 12. Reference Files (12 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 12.1 | Frontend loaded | React project | Frontend questions, conventions, review checklist | |
| 12.2 | Backend loaded | Express API | Backend-specific sections | |
| 12.3 | Mobile loaded | React Native app | Mobile-specific sections | |
| 12.4 | Data/ML loaded | PyTorch pipeline | Data/ML-specific sections | |
| 12.5 | DevOps loaded | Terraform project | DevOps-specific sections | |
| 12.6 | Fullstack loaded | Next.js app | Fullstack + frontend + backend (3 files) | |
| 12.7 | Reference enriches Context | Any typed project | Additional questions and template sections | |
| 12.8 | Reference enriches Prompts | Any typed project | Common prompt patterns available | |
| 12.9 | Reference enriches Review | Any typed project | Type-specific review checklist applied | |
| 12.10 | Multiple references loaded | Multi-type project | All relevant references loaded | |
| 12.11 | Conflicting conventions | Fullstack (3 files) | Fullstack.md takes precedence on overlaps | |
| 12.12 | Reference enriches Plan | Any typed project | Type-specific patterns inform decomposition | |

---

## 13. Cross-file Consistency (14 tests)

Every dependency between files must be valid. If file A references file B, file B must exist and be accessible.

### 13a. Workflow parity

Every workflow in SKILL.md must have a corresponding command and Copilot prompt.

| # | Test Case | How to verify | Result |
|---|---|---|---|
| 13.1 | Command for every workflow | Each workflow in SKILL.md has a matching `commands/pdd-*.md` | |
| 13.2 | Copilot prompt for every command | Each `commands/pdd-*.md` has a matching `copilot/prompts/pdd-*.prompt.md` | |
| 13.3 | Workflow count matches | SKILL.md count, README count, and actual file count are consistent | |
| 13.4 | Workflow numbering consistent | Internal cross-references use correct workflow numbers | |

### 13b. File references resolve

Every path mentioned in a file must be accessible from where that file runs.

| # | Test Case | How to verify | Result |
|---|---|---|---|
| 13.5 | SKILL.md → references/ | Every `references/*.md` path in SKILL.md exists in the repo | |
| 13.6 | Commands → references/ | Every `references/` path in commands exists relative to the skill dir | |
| 13.7 | Copilot prompts → `#file:` | Every `#file:references/*.md` in Copilot prompts has a setup instruction to copy it | |
| 13.8 | Copilot setup → files exist | Every file listed in `copilot/README.md` setup exists in the repo | |

### 13c. Slash command references

Every `/project:pdd-*` or `/pdd-*` reference points to an existing command.

| # | Test Case | How to verify | Result |
|---|---|---|---|
| 13.9 | Commands reference valid commands | Every `/project:pdd-*` in command files maps to an existing `commands/pdd-*.md` | |
| 13.10 | Copilot prompts reference valid prompts | Every `/pdd-*` in Copilot prompts maps to an existing `copilot/prompts/pdd-*.prompt.md` | |
| 13.11 | SKILL.md references valid commands | Every `/project:pdd-*` in SKILL.md maps to an existing command file | |

### 13d. README consistency

| # | Test Case | How to verify | Result |
|---|---|---|---|
| 13.12 | README command table complete | Every file in `commands/` appears in the README command table | |
| 13.13 | Copilot README command table complete | Every file in `copilot/prompts/` appears in the Copilot README table | |
| 13.14 | Copilot README setup covers all deps | Every external file referenced by Copilot prompts has a copy instruction in setup | |

---

## 14. Cross-cutting / Edge Cases (10 tests)

| # | Test Case | Scenario | Expected | Result |
|---|---|---|---|---|
| 14.1 | Context files missing | Any workflow without pdd/context/ | Don't block — proceed and suggest afterward | |
| 14.2 | Quick path works | Simple feature | Context → Prompts → Review is sufficient | |
| 14.3 | Complex path works | Multi-layer feature | Search → Plan → Prompts → Review | |
| 14.4 | Workflow transitions | Finish any workflow | Suggests the natural next step | |
| 14.5 | Session re-entry | User returns next day | Context freshness check | |
| 14.6 | "I don't know where to start" | New user | Ask → Scaffold + Context | |
| 14.7 | "This is too complicated" | Overwhelmed user | Start with just project.md | |
| 14.8 | "Can you just do it?" | Hands-off user | Yes, but explain each step | |
| 14.9 | One prompt, one job | Any prompt request | Enforced throughout | |
| 14.10 | Timebox experiments | Experiment older than a week | Graduate or delete | |

---

## How to Run This Checklist

1. Read through SKILL.md, commands/, copilot/prompts/, and both READMEs
2. For each test case, verify the expected behavior is defined in the relevant file(s)
3. Mark PASS or FAIL
4. For cross-file consistency (section 13), use the verification commands below

### Quick verification commands

```bash
# 13.1 — Command for every workflow (should be 9: 8 workflows + status)
ls commands/pdd-*.md | wc -l

# 13.2 — Copilot prompt for every command
diff <(ls commands/ | sed 's/.md//' | sort) <(ls copilot/prompts/ | sed 's/.prompt.md//' | sort)

# 13.5/13.6 — All referenced reference files exist
for f in frontend backend mobile data-ml devops fullstack; do
  [ -f "references/$f.md" ] && echo "OK: references/$f.md" || echo "MISSING: references/$f.md"
done

# 13.7 — Copilot #file: references have setup instructions
# Check that a references/ copy instruction exists and individual files are listed
grep -q 'cp.*references/' copilot/README.md && echo "OK: references/ copy instruction" || echo "MISSING: references/ copy instruction"
for f in frontend backend mobile data-ml devops fullstack; do
  grep -q "$f.md" copilot/README.md && echo "OK: $f.md listed" || echo "MISSING from setup: $f.md"
done

# 13.9/13.10 — Slash command references point to existing files
grep -oh '/project:pdd-[a-z]*' commands/*.md | sort -u | while read cmd; do
  f="commands/$(echo $cmd | sed 's|/project:||').md"
  [ -f "$f" ] && echo "OK: $cmd" || echo "BROKEN: $cmd → $f"
done

# 13.12/13.13 — README tables match actual files
echo "=== Main README ==="
for f in $(ls commands/ | sed 's/.md//'); do
  grep -q "$f" README.md && echo "OK: $f" || echo "MISSING from README: $f"
done
echo "=== Copilot README ==="
for f in $(ls copilot/prompts/ | sed 's/.prompt.md//'); do
  grep -q "$f" copilot/README.md && echo "OK: $f" || echo "MISSING from Copilot README: $f"
done
```
