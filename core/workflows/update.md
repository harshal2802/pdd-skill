# Update

## Purpose

Improve a prompt that is underperforming instead of immediately rewriting it from scratch.

## Use When

- The prompt produces wrong output.
- The results are inconsistent, incomplete, or too broad.
- The user can describe what went wrong.

## Inputs

- the existing prompt
- observed failure mode
- desired behavior

## Produces

- a revised prompt
- clearer scope or constraints
- a recommendation for how to re-run and verify it

## Default Next Step

Re-run the prompt, then move to `review` on the resulting output.
