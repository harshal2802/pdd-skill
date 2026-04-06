# Review

## Purpose

Treat AI-generated output like a PR by verifying correctness, identifying regressions, and calling out missing tests or checks.

## Use When

- The AI generated code, docs, config, or another artifact that may be committed.
- The user asks if something is ready to commit.

## Inputs

- generated output
- relevant files or diffs
- expected behavior

## Produces

- review findings
- verification results
- fix guidance or a commit-ready recommendation

## Default Next Step

If issues are found, iterate on code or prompts. If the output is solid, commit it and consider `eval`.
