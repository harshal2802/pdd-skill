# Plan

## Purpose

Break a feature into phases and decide the prompt-chain strategy before generating implementation prompts.

## Use When

- The feature spans multiple files, layers, or phases.
- A single prompt would mix too many concerns.
- The team needs sequencing before coding.

## Inputs

- feature goal
- current context files
- research results if available

## Produces

- phased implementation outline
- prompt-chain order
- checkpoints for review and validation

## Default Next Step

Move to `prompts` and generate the first focused implementation prompt.
