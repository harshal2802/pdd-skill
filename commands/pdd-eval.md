# Run Prompt Evaluations

You are helping the user evaluate their PDD prompts by running evals and tracking results over time.

**User input**: $ARGUMENTS

## Step 1 — Identify what to evaluate

If the user specifies a prompt, evaluate that one. Otherwise, scan for prompts without evals:

```
# Find prompts in features/ that don't have a matching eval
# pdd/prompts/features/auth/login.md → pdd/evals/login-eval.md
```

Suggest starting with the prompt that has the most runs or is most critical.

## Step 2 — Check for existing eval

Look in `pdd/evals/` for a matching eval file (`<prompt-name>-eval.md`).

- **Eval exists**: Load it, run the checklist against the latest output
- **No eval exists**: Create one using the template below

### Eval template (Level 1 — Manual checklist)

```markdown
# Eval: <prompt name>
**Prompt**: pdd/prompts/features/<area>/<prompt-file>.md
**Created**: <date>
**Level**: 1 — Manual checklist

## Criteria
- [ ] Output compiles / runs without errors
- [ ] Matches the specified output format
- [ ] Handles the listed edge cases
- [ ] Follows project conventions (from conventions.md)
- [ ] No hallucinated imports, APIs, or functions
- [ ] Integrates with existing code without conflicts

## Type-specific criteria
<add checks from the project type reference file>

## Run log

| Run | Date | Result | Notes |
|---|---|---|---|
| 1 | <date> | <pass/fail> | <what happened> |
| 2 | | | |
| 3 | | | |
```

Save to `pdd/evals/<prompt-name>-eval.md`.

## Step 3 — Run the evaluation

Ask the user to run the prompt (or provide output from a recent run). Then:

1. Check each criterion in the eval checklist
2. Mark pass/fail for each
3. Log the run in the run log table
4. Calculate overall result

### Pass/fail rules

- **All criteria pass** → PASS
- **Any criterion fails** → FAIL (list which ones)
- **Track pass rate**: After 3+ runs, calculate pass@1 (passes on first try) and pass@3 (passes at least once in 3 tries)

## Step 4 — Level up if ready

| Current level | Trigger to level up | Action |
|---|---|---|
| **Level 1** (checklist) | 5+ runs of the same prompt | Save a known-good output to `pdd/evals/baselines/<prompt-name>-baseline.md` → Level 2 |
| **Level 2** (baseline diff) | Prompt is stable and used regularly | Write a validation script in `pdd/evals/scripts/` → Level 3 |

### Level 2 — Baseline comparison

When a good output is saved as a baseline, future evals diff against it:
- What sections changed?
- Are the changes improvements or regressions?
- Does the new output still pass all Level 1 criteria?

### Level 3 — Automated validation

For mature, frequently-used prompts:

```markdown
# Eval script: <prompt name>
**Script**: pdd/evals/scripts/<prompt-name>-eval.sh
**Checks**:
- Output is valid <language> (syntax check)
- Required imports/sections present
- No forbidden patterns (hardcoded values, TODO placeholders)
- Output structure matches expected format
```

## Step 5 — Report

```markdown
## Eval Report: <prompt name>

**Level**: 1 | 2 | 3
**Run**: #<N>
**Date**: <date>
**Result**: PASS | FAIL

### Criteria results
- [x] <passing criterion>
- [ ] <failing criterion> — <why it failed>

### Pass rate
- pass@1: <X/Y> (<percentage>)
- pass@3: <X/Y> (<percentage>)

### Recommendation
<keep prompt as-is | update prompt via /project:pdd-update | promote eval to next level>
```

## Edge cases

- **No prompt output available**: Ask the user to run the prompt first, or run it if possible
- **Prompt has never been evaluated**: Create a Level 1 eval and run the first evaluation
- **All prompts already have evals**: Report coverage summary and suggest running the least-recently-evaluated prompt
- **Eval criteria feel wrong**: Update the eval — criteria should evolve as the prompt matures

## Next step

- If eval passes: *"Prompt is healthy. Consider leveling up the eval if you have 5+ runs."*
- If eval fails: *"These criteria failed. Run `/project:pdd-update` to fix the prompt, then re-evaluate."*
