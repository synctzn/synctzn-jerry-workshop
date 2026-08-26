---
name: evidence-first-debugging
description: Find the failing boundary before changing a long-running agent system.
version: 1.0.0
status: tested
---

# Evidence-first debugging

Use this card when an agent, provider, tool, or downstream display behaves
unexpectedly. The goal is to find the boundary where the result changed, not
to collect a larger pile of logs.

## Method

1. **Name the symptom.** Write what a person saw and the exact error or missing
   result.
2. **Trace the path.** Check the layers in order: scheduler → model/provider →
   tool → external service → stored result → public display.
3. **Compare one working case.** Find the most recent successful run and list
   the smallest differences.
4. **Form one hypothesis.** State: “X is the failing boundary because Y.”
5. **Run one minimal test.** Prefer a read-only probe or a harmless invalid
   input that proves which component received the request.
6. **Fix the source.** Change the smallest configuration or module that owns
   the failure.
7. **Re-run the original check.** Confirm the old symptom is gone and record
   any remaining external blocker separately.

## Evidence labels

Use these labels in notes and handoffs:

- `observed` — returned by a live command or service;
- `configured` — present in a file but not yet exercised;
- `inferred` — a reasoned explanation that still needs a test;
- `blocked` — the next step requires a permission, provider, or external reply.

## Limits

This card does not grant shell, network, wallet, deploy, or write authority. It
also does not turn a successful local test into proof of adoption.

## Acceptance

The card is ready when a reader can point to the symptom, the failing boundary,
the minimal test, and a fresh verification result.
