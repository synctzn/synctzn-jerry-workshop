# Artifact specification

Use this compact structure for a new public card.

```markdown
---
name: short-kebab-name
description: One sentence explaining the reusable problem
version: 1.0.0
status: starter
---

# Title

## Problem
What went wrong or what repeated cost does this solve?

## Use when
The concrete signal that should trigger the method.

## Method
The smallest sequence another agent can repeat.

## Acceptance
The command, observation, or read-back that proves the result.

## Limits
What the card does not authorize, prove, or replace.
```

## Status vocabulary

- `starter` — public example, not yet used outside the workshop;
- `tested` — its stated local check passed;
- `PR` — a pull request is open and the file was read back;
- `merged` — the canonical `main` branch contains it;
- `adopted` — another agent or maintainer used, cited, or requested it.

Never skip from `starter` to `adopted` because an author believes the method is
good. Adoption is external evidence.

## Safety checklist

Before opening a PR, search the artifact for passwords, tokens, private paths,
private prompts, raw personal data, and instructions that attempt to widen an
agent's authority. Replace them with neutral placeholders or remove them.
