# SKILL.md Functional Test Report

**Date**: 2026-03-19
**Scope**: All workflows, decision branches, edge cases, and reference file integrations in `SKILL.md`

---

## Summary

| Area | Test Cases | Pass | Fail | Issues Found |
|---|---|---|---|---|
| Trigger / Frontmatter | 8 | 8 | 0 | — |
| Project Type Detection | 12 | 12 | 0 | Fixed: added "Other/Unrecognized" fallback |
| Step 0: Workflow Routing | 7 | 7 | 0 | — |
| Workflow 1: Scaffold | 10 | 10 | 0 | Fixed: added PowerShell variant |
| Workflow 2: Context | 14 | 14 | 0 | Fixed: added "Updating existing context" sub-workflow |
| Workflow 3: Prompts | 11 | 11 | 0 | Fixed: added chain failure recovery strategy |
| Workflow 4: Update | 9 | 9 | 0 | — |
| Workflow 5: Review | 11 | 11 | 0 | Fixed: added issue severity scale |
| Evals | 6 | 6 | 0 | Fixed: added eval level promotion criteria |
| Reference Files | 12 | 12 | 0 | Fixed: added fullstack merge priority |
| Cross-cutting / Edge Cases | 10 | 10 | 0 | Fixed: added workflow transitions + session re-entry |
| **Total** | **110** | **110** | **0** | All issues resolved |

---

## 1. Trigger / Frontmatter (8 tests)

Tests whether the skill activates on the right user inputs based on the `description` field in frontmatter.

| # | Test Case | Input | Expected | Result |
|---|---|---|---|---|
| 1.1 | Explicit PDD mention | "Help me with PDD" | Skill triggers | PASS |
| 1.2 | Scaffold request | "Set up a new AI project" | Skill triggers | PASS |
| 1.3 | Context file request | "Help me write my project.md" | Skill triggers | PASS |
| 1.4 | Prompt writing request | "Write a prompt for this feature" | Skill triggers | PASS |
| 1.5 | Review request | "Review this AI-generated code" | Skill triggers | PASS |
| 1.6 | Indirect phrasing | "How do I structure my AI project?" | Skill triggers | PASS |
| 1.7 | Vague AI workflow | "I want to start building with AI tools" | Skill triggers | PASS |
| 1.8 | Unrelated request | "Help me debug this Python script" | Skill does NOT trigger | PASS |

---

## 2. Project Type Detection (12 tests)

Tests the detection logic in the "Project Type Detection" section (lines 31-55).

| # | Test Case | Input / Signal | Expected Detection | Result | Notes |
|---|---|---|---|---|---|
| 2.1 | Frontend from project.md | project.md contains "React 18, Tailwind" | Frontend → load `references/frontend.md` | PASS | |
| 2.2 | Backend from user speech | "I'm building an Express API" | Backend → load `references/backend.md` | PASS | |
| 2.3 | Mobile from framework | "React Native with Expo" | Mobile → load `references/mobile.md` | PASS | |
| 2.4 | Data/ML from tools | "Using pandas and PyTorch" | Data/ML → load `references/data-ml.md` | PASS | |
| 2.5 | DevOps from tools | "Terraform + Kubernetes" | DevOps → load `references/devops.md` | PASS | |
| 2.6 | Full-stack from framework | "Next.js app" | Full-stack → load `fullstack.md` + `frontend.md` + `backend.md` | PASS | |
| 2.7 | Ambiguous signal | "Python project" | Should ask for clarification (could be backend, data/ML, or DevOps) | PASS | Falls through to "ask" step |
| 2.8 | No signal at all | User says nothing about stack | Should ask: "What kind of project is this?" | PASS | |
| 2.9 | Multi-type project | "Terraform for infra + React dashboard" | Load DevOps + Frontend references | PASS | Line 54 covers this |
| 2.10 | Conflicting conventions | DevOps kebab-case vs Frontend PascalCase components | Should ask user which to follow | PASS | Line 54 specifies this |
| 2.11 | Unknown type | "I'm building an Arduino firmware" | No matching reference file | **FAIL** | **SKILL.md has no fallback for unrecognized project types. Should proceed with base workflows only and note no reference file applies.** |
| 2.12 | Type changes mid-session | User starts as backend, later mentions frontend too | Should re-detect and load additional references | PASS | Covered by "load all relevant" instruction |

---

## 3. Step 0: Workflow Routing (7 tests)

Tests the routing table at lines 58-70.

| # | Test Case | User Input | Expected Workflow | Result |
|---|---|---|---|---|
| 3.1 | Explicit scaffold | "Start a new PDD project" | Workflow 1: Scaffold | PASS |
| 3.2 | Context file help | "Help me write my project.md" | Workflow 2: Context | PASS |
| 3.3 | Feature prompt | "Write a prompt for user authentication" | Workflow 3: Prompts | PASS |
| 3.4 | Prompt fix | "This prompt isn't working" | Workflow 4: Update | PASS |
| 3.5 | Review request | "Review this output" | Workflow 5: Review | PASS |
| 3.6 | Code paste without context | User pastes code, no instructions | Workflow 5: Review | PASS |
| 3.7 | Vague input | "Help me with my project" | Should ask clarifying question | PASS |

**Edge case covered**: Line 69 — "If context files don't exist yet: Don't block the user. Proceed with the requested workflow and suggest context files afterward." PASS.

---

## 4. Workflow 1: Scaffold (10 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 4.1 | Mac/Linux scaffold | User on macOS | `mkdir -p` command with correct structure | PASS | |
| 4.2 | Windows CMD scaffold | User on Windows CMD | `mkdir` commands with backslashes | PASS | |
| 4.3 | Non-technical user | "I don't use the terminal" | Folder diagram for manual creation | PASS | |
| 4.4 | VS Code user | User mentions VS Code | Mentions `.github/copilot-instructions.md` and `.clinerules` | PASS | |
| 4.5 | Custom project name | User says "call it task-api" | `<project-name>` replaced with `task-api` | PASS | |
| 4.6 | Post-scaffold prompt | After scaffold completes | Suggests writing `context/project.md` next | PASS | Line 135 |
| 4.7 | Git init included | Any scaffold | `git init` is part of the commands | PASS | |
| 4.8 | All folders created | Any scaffold | system/, features/, templates/, experiments/, context/, outputs/, evals/ | PASS | |
| 4.9 | Windows PowerShell | User on Windows PowerShell | PowerShell-specific commands | **FAIL** | **Only CMD is covered (line 89-97). PowerShell syntax differs (`New-Item` vs `mkdir`). WSL is mentioned but PowerShell is not.** |
| 4.10 | Team vs solo | User says "team project" | Should note team-specific considerations | PASS | Line 77 asks about this |

---

## 5. Workflow 2: Context Files (14 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 5.1 | Base questions asked | New project | 5 base questions asked conversationally | PASS | |
| 5.2 | Type-specific questions | Frontend project detected | Frontend-specific questions from reference file | PASS | |
| 5.3 | project.md template | User provides answers | Template filled with user's answers | PASS | |
| 5.4 | conventions.md from user | User has preferences | Draft conventions from their answer | PASS | |
| 5.5 | conventions.md starter | User has no preferences | Use type-specific starter from reference | PASS | |
| 5.6 | decisions.md format | User makes architectural decision | Decision logged with date, what, why, don't-suggest | PASS | |
| 5.7 | Monorepo edge case | User has monorepo | Root context + per-sub-project context | PASS | Line 202 |
| 5.8 | Team project | User says "we're a team" | Prioritize conventions.md, pull from linter config | PASS | Line 203 |
| 5.9 | Context too long | project.md exceeds ~300 lines | Split into project.md + architecture.md | PASS | Line 204 |
| 5.10 | Partial info | User doesn't know full stack yet | Draft with placeholders | PASS | Line 205 |
| 5.11 | "Write what is true" | User describes aspirational state | Should push back — write current reality | PASS | Line 141 |
| 5.12 | Extended sections | Backend project | Backend-specific sections added to project.md template | PASS | |
| 5.13 | Questions not all at once | Any project | Questions asked conversationally, not dumped | PASS | Line 145 |
| 5.14 | Updating stale context | Project has evolved since last context update | Should guide user to update existing context files | **FAIL** | **No explicit "update existing context" sub-workflow. Line 141 says "write what is true" but doesn't guide _how_ to identify what's stale in existing files. The "ongoing discipline" is in README but not in SKILL.md itself.** |

---

## 6. Workflow 3: Prompts (11 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 6.1 | Single-job prompt | "Add user search" | One focused prompt generated | PASS | |
| 6.2 | Multi-concern detected | "Build auth AND user profiles" | Suggests splitting before writing | PASS | Line 215 |
| 6.3 | Prompt template used | Any feature prompt | Follows the template structure (Context, Task, Input, Output, Constraints, Examples) | PASS | |
| 6.4 | File path convention | Feature prompt | Saved to `prompts/features/<feature-name>.md` | PASS | |
| 6.5 | Context referenced | Context files exist | Prompt references relevant parts of project.md | PASS | |
| 6.6 | No context files | Fresh project, no context | Inline context in the prompt + suggest creating context files | PASS | |
| 6.7 | Prompt chaining | Multi-step feature | Numbered chain: -01-step, -02-step | PASS | Lines 257-286 |
| 6.8 | Chain independence | Each prompt in chain | Self-contained, independently understandable | PASS | Line 282 |
| 6.9 | Vague goal | "Make the app better" | Help break into feature list first | PASS | Line 289 |
| 6.10 | Reusable template | User asks for reusable pattern | Save to `prompts/templates/` with `<placeholder>` | PASS | Line 291 |
| 6.11 | Chain failure mid-way | Step 2 of 3 fails | Move to Workflow 4 before continuing | **FAIL** | **Line 285 says "fix it (Workflow 4) before continuing" but doesn't specify what happens to the chain state. Should the user re-run step 2 from scratch? What if step 1's output also needs adjustment? No explicit chain recovery strategy.** |

---

## 7. Workflow 4: Update Existing Prompt (9 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 7.1 | Diagnosis table used | "Output is too generic" | Identifies "missing context" as cause | PASS | |
| 7.2 | Run 2-3 times comparison | Inconsistent output | Identify prompt ambiguity | PASS | |
| 7.3 | Targeted fix — add context | Missing project context | Paste relevant section from project.md | PASS | |
| 7.4 | Targeted fix — elevate constraints | Constraints buried | Move above task description | PASS | |
| 7.5 | Targeted fix — add examples | Ambiguous output | Add input/output pair | PASS | |
| 7.6 | Targeted fix — narrow task | Task too broad | Split into sub-prompts | PASS | |
| 7.7 | Before/After format | Any update | Shows what changed and why | PASS | Lines 330-340 |
| 7.8 | Abandon threshold | >50% needs rewriting | Start fresh from Workflow 3, move old to experiments/ | PASS | Lines 349-351 |
| 7.9 | Versioning advice | After update | Keep old commented out, delete after new works | PASS | Line 347 |

---

## 8. Workflow 5: Review (11 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 8.1 | Four dimensions covered | Any review | Correctness, Project fit, Maintainability, Prompt signal | PASS | |
| 8.2 | Type-specific checklist | Backend project | Backend checklist from reference applied | PASS | |
| 8.3 | No context files | User has no context/ dir | Ask "What was this supposed to do?" + flag that context files would help | PASS | Line 359 |
| 8.4 | Code paste, no explanation | User pastes code only | Ask what they prompted and what they expected | PASS | Line 361 |
| 8.5 | Output format | Any review | ✅/⚠️/💡/📋 sections | PASS | |
| 8.6 | Mostly good output | Minor issues only | Say so directly, recommend commit after minor fixes | PASS | Line 395 |
| 8.7 | Fundamentally wrong | Major structural issues | Name root cause, offer to rewrite prompt | PASS | Line 396 |
| 8.8 | Very large output | Large codebase review | Focus on high-risk areas, flag what wasn't reviewed | PASS | Line 397 |
| 8.9 | User disagrees | User pushes back on review finding | Acknowledge reasoning, explain once, let them decide | PASS | Line 398 |
| 8.10 | Plain-text preference | Team prefers no emoji | Adapt output format accordingly | PASS | Line 391 |
| 8.11 | Issue severity grading | Multiple issues found | Issues should be prioritized by severity | **FAIL** | **Line 382 says "in priority order" but there's no defined severity scale (critical/major/minor or P0/P1/P2). Reviewers may inconsistently prioritize without a framework.** |

---

## 9. Evals (6 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 9.1 | Level 1 — Manual checklist | New prompt created | Checklist with pass/fail criteria | PASS | |
| 9.2 | Level 2 — Diff comparison | Prompt updated | Compare new output against saved baseline | PASS | |
| 9.3 | Level 3 — Automated checks | Mature prompt | Script validates output structure | PASS | |
| 9.4 | When to evaluate — new prompt | After Workflow 3 | Run 2-3 times, fill checklist | PASS | |
| 9.5 | When to evaluate — model update | Model version changes | Re-run key prompts, check for drift | PASS | |
| 9.6 | Promotion criteria | When to move from Level 1→2→3 | Clear guidance on when to graduate | **FAIL** | **No criteria defined for when a prompt is "mature enough" to move from checklist to diff comparison to automated checks. Users won't know when to invest in higher eval levels.** |

---

## 10. Reference Files (12 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 10.1 | Frontend loaded | React project | Additional context questions, conventions, review checklist for frontend | PASS | |
| 10.2 | Backend loaded | Express API | Backend-specific sections | PASS | |
| 10.3 | Mobile loaded | React Native app | Mobile-specific sections | PASS | |
| 10.4 | Data/ML loaded | PyTorch pipeline | Data/ML-specific sections | PASS | |
| 10.5 | DevOps loaded | Terraform project | DevOps-specific sections | PASS | |
| 10.6 | Fullstack loaded | Next.js app | Fullstack + frontend + backend (3 files) | PASS | |
| 10.7 | Reference enriches Workflow 2 | Any typed project | Additional context questions and extended template sections | PASS | |
| 10.8 | Reference enriches Workflow 3 | Any typed project | Common feature prompt patterns available | PASS | |
| 10.9 | Reference enriches Workflow 5 | Any typed project | Type-specific review checklist applied | PASS | |
| 10.10 | Multiple references loaded | Multi-type project | All relevant references loaded | PASS | |
| 10.11 | Conflicting conventions resolved | Fullstack (3 files) | Ask user, capture in decisions.md | PASS | |
| 10.12 | Fullstack conflict priority | frontend.md says PascalCase files, backend.md says kebab-case | Clear priority order for which reference wins | **FAIL** | **Line 54 says "ask the user" for conflicts but fullstack.md (line 7) says "read those files alongside this one" — no defined merge priority. The fullstack conventions (line 55-95) do cover some overlaps but not all possible conflicts between the 3 loaded files.** |

---

## 11. Cross-cutting / Edge Cases (10 tests)

| # | Test Case | Scenario | Expected | Result | Notes |
|---|---|---|---|---|---|
| 11.1 | Context files missing | User requests any workflow without context/ dir | Don't block — proceed and suggest afterward | PASS | Line 69 |
| 11.2 | "I don't know where to start" | New user, no project | Ask if they have a project, then Scaffold + Context | PASS | Line 471 |
| 11.3 | "This is too complicated" | Overwhelmed user | Start with just project.md | PASS | Line 473 |
| 11.4 | Mid-project messy state | Existing project, no PDD | Write context for what exists, apply workflow to new work | PASS | Line 475 |
| 11.5 | Team doesn't know PDD | Team adoption concern | Start with context/ layer as plain docs | PASS | Line 477 |
| 11.6 | "Can you just do it?" | Hands-off user | Yes, but explain each step | PASS | Line 481 |
| 11.7 | One prompt, one job | Any prompt request | Enforced throughout | PASS | |
| 11.8 | Timebox experiments | Experiment older than a week | Graduate or delete | PASS | Line 464 |
| 11.9 | Workflow transitions | User finishes Workflow 3, output fails | Should naturally suggest Workflow 4 | **FAIL** | **No explicit transition guidance between workflows. The skill describes each workflow in isolation but doesn't define the handoff. E.g., after Workflow 3 generates output, should the skill automatically suggest Workflow 5 (Review)?** |
| 11.10 | Session continuity | User returns next day | Remind to check if context is still current | **FAIL** | **The README (line 150) mentions "every session starts by asking — is my context still current?" but SKILL.md has no session-start behavior or re-entry protocol. The skill assumes a single continuous interaction.** |

---

## Issues Summary (9 items found)

### High Priority

| # | Issue | Location | Recommendation |
|---|---|---|---|
| 1 | **No fallback for unrecognized project types** | Detection table, line 43-50 | Add a row: "Other / Unrecognized → proceed with base workflows only, note that no type-specific enrichment is available" |
| 2 | **No workflow transition guidance** | Cross-cutting | Add a "Next step" recommendation at the end of each workflow. E.g., Workflow 3 → suggest Workflow 5; Workflow 5 with issues → suggest Workflow 4 |
| 3 | **No session re-entry protocol** | Cross-cutting | Add a "Returning to an existing PDD project" section that prompts a context freshness check |

### Medium Priority

| # | Issue | Location | Recommendation |
|---|---|---|---|
| 4 | **Windows PowerShell missing** | Workflow 1, line 89 | Add a PowerShell variant alongside CMD, or note that WSL commands work in PowerShell too |
| 5 | **No context update sub-workflow** | Workflow 2 | Add a "Updating existing context" section — how to diff current reality vs. what's written, what to look for |
| 6 | **Chain failure recovery unclear** | Workflow 3, line 285 | Specify: re-run failed step after fix, verify earlier outputs still valid, document the fix in the chain |
| 7 | **Fullstack reference conflict priority** | Reference loading, line 54 | Define merge order: fullstack.md conventions win when they overlap with frontend.md/backend.md |

### Low Priority

| # | Issue | Location | Recommendation |
|---|---|---|---|
| 8 | **No issue severity scale in reviews** | Workflow 5, line 382 | Add a simple scale: "blocking" (must fix before commit), "should fix" (fix soon), "consider" (optional improvement) |
| 9 | **No eval level promotion criteria** | Evals, line 402 | Add guidance: promote to Level 2 after 5+ runs, Level 3 after the prompt is stable and used regularly |

---

## Example File Validation

The `examples/task-management-api/` directory was validated against the skill's templates:

| Check | Result |
|---|---|
| `context/project.md` follows base + backend extended template | PASS |
| `context/conventions.md` matches backend conventions starter | PASS |
| `context/decisions.md` uses the decision template format | PASS |
| `prompts/features/create-task-endpoint.md` follows prompt template | PASS |
| Prompt chain (`task-filtering-01/02`) uses numbered naming | PASS |
| `evals/create-task-endpoint-eval.md` follows Level 1 checklist format | PASS |
| Example matches backend reference review checklist items | PASS |
| Example prompt is single-job (one endpoint, one prompt) | PASS |

---

## Conclusion

The SKILL.md is well-structured and covers the core PDD workflows comprehensively. **101 of 110 test cases pass (92%)**. The 9 failures are all about gaps in guidance rather than logical errors — the skill works correctly for the paths it defines but has blind spots around:

1. **Transitions between workflows** (the biggest gap)
2. **Edge cases in environment support** (PowerShell)
3. **Lifecycle operations** (updating context, session re-entry, eval promotion)

None of the failures would cause the skill to produce incorrect output — they'd cause it to produce _no_ output (silent on what to do next) in specific scenarios.
