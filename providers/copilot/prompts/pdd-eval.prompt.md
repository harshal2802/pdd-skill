---
agent: agent
description: "Run prompt evaluations, track pass/fail results, and level up eval maturity"
---

# Run Prompt Evaluations

You are helping the user evaluate their PDD prompts by running evals and tracking results over time.

## Step 1 — Identify what to evaluate

If the user specifies a prompt, evaluate that one. Otherwise, scan for prompts without evals and suggest the most critical one.

## Step 2 — Check for existing eval

Look in `pdd/evals/` for a matching eval file (`<prompt-name>-eval.md`). If none exists, create one:

```markdown
# Eval: <prompt name>
**Prompt**: pdd/prompts/features/<area>/<prompt-file>.md
**Created**: <date>
**Level**: 1 — Manual checklist

## Criteria
- [ ] Output compiles / runs without errors
- [ ] Matches the specified output format
- [ ] Handles the listed edge cases
- [ ] Follows project conventions
- [ ] No hallucinated imports, APIs, or functions
- [ ] Integrates with existing code without conflicts

## Run log

| Run | Date | Result | Notes |
|---|---|---|---|
| 1 | | | |
```

## Step 3 — Run the evaluation

Ask the user to provide output from a recent prompt run. Check each criterion, mark pass/fail, and log the run.

### Pass rate tracking
After 3+ runs, calculate:
- **pass@1**: Passes on first try
- **pass@3**: Passes at least once in 3 tries

## Step 4 — Level up if ready

| Level | Trigger | Action |
|---|---|---|
| 1 → 2 | 5+ runs | Save good output to `pdd/evals/baselines/` — diff future runs against it |
| 2 → 3 | Prompt is stable | Write a validation script in `pdd/evals/scripts/` |

## Step 5 — Report

```markdown
## Eval Report: <prompt name>

**Level**: 1 | 2 | 3
**Result**: PASS | FAIL

### Criteria results
- [x] <passing>
- [ ] <failing> — <why>

### Pass rate
- pass@1: <X/Y>
- pass@3: <X/Y>

### Recommendation
<keep | update prompt | promote eval level>
```

## Next step

- Passes: *"Prompt is healthy. Consider leveling up the eval if you have 5+ runs."*
- Fails: *"These criteria failed. Use `/pdd-update` to fix the prompt, then re-evaluate."*
