# Update an Existing Prompt

You are helping the user fix a PDD prompt that isn't producing good results. **Diagnose before rewriting.**

**User input**: $ARGUMENTS

## Step 1 — Identify the root cause

Ask the user to share the prompt and its output (if not already provided). Then diagnose:

| Symptom | Likely cause | Fix |
|---|---|---|
| Output is too generic | Missing context | Add project/tech context |
| Output ignores constraints | Constraints buried or vague | Move constraints higher, make explicit |
| Output does too many things | Task too broad | Split into multiple prompts |
| Output format is wrong | No format specified | Add explicit output format section |
| Output drifts across runs | Prompt is ambiguous | Add concrete examples |
| Output contradicts conventions | No conventions reference | Add or paste from `pdd/context/conventions.md` |

Run the prompt 2-3 times if possible:
- **Consistent errors** → the prompt is wrong
- **Inconsistent output** → the prompt is ambiguous
- **Correct but unusable** → the format spec is off

## Step 2 — Apply targeted fixes

Don't rewrite from scratch. Make the smallest effective change:
- Add missing context
- Elevate buried constraints above the task section
- Add a concrete input/output example
- Narrow the task by splitting

## Step 3 — Show what changed

Produce the improved version and explain what changed and why. Show a before/after diff of the key changes — not just a new prompt without reasoning.

## Step 4 — Verify and version

- Suggest running the updated prompt 2-3 times to confirm improvement
- Commit the new version with a message noting what was fixed
- Keep the old version commented out temporarily; delete once the new one proves better

## When to start fresh

If more than half the prompt needs rewriting, suggest starting from scratch with `/project:pdd-prompts` and moving the old prompt to `pdd/prompts/experiments/` with a date prefix: `YYYY-MM-DD-<descriptive-name>.md`.

## Next step

After updating: *"Try the updated prompt and I'll review the new output. Run `/project:pdd-review` when ready."*
