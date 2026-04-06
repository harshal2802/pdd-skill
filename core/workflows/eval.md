# Eval

## Purpose

Track prompt quality over time with explicit criteria instead of relying on memory or one successful run.

## Use When

- A prompt matters enough to measure repeatedly.
- The team wants a baseline or regression signal.
- A once-good prompt has started to drift.

## Inputs

- prompt under test
- expected outputs or acceptance criteria
- baseline artifacts when available

## Produces

- evaluation notes or files under `pdd/evals/`
- pass/fail signals
- follow-up recommendations when quality drops

## Default Next Step

If the eval fails, move to `update`. If it passes consistently, keep the prompt in active use.
