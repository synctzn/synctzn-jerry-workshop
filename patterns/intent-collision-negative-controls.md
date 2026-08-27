---
name: intent-collision-negative-controls
description: Preflight acceptance predicates with intent collisions and observer-owned negative controls.
version: 1.0.0
status: tested
---

# Intent-collision negative controls

## Problem

A field-only acceptance predicate can pass two different request intents when
both produce the same asserted fields. That is not merely a weak test: on the
fields it asserts, the predicate has no power to distinguish the cases it was
created to separate. A second failure is treating an unexecuted or
wrongly-triggered negative control as evidence of safety.

## Use when

Use this before trusting an acceptance condition for an API contract, a
registry record, a hash comparison, a liveness report, or another consequential
checker—especially when nullable, defaulted, sentinel, or truthy fields are
used as proxies for request intent.

## Method

1. **Enumerate intents.** List the positive and negative request modes the
   condition is supposed to distinguish: for example, bare, valid anchored,
   below-boundary, sentinel/zero, and malformed input.
2. **Build intent vectors.** For every intent, record the declared request
   parameters and provenance together with the response discriminator(s). Do
   not infer the request mode from a nullable result field.
3. **Run the collision preflight.** Compare the vectors before running the
   truth table. If two distinct intents collide on every asserted field, mark
   the condition `CONDITION_INVALID` and stop automatic judgement until the
   condition is repaired.
4. **Run a paired table.** Include the intended positive case, the exact
   near-miss the condition must reject, each sentinel/default boundary, and an
   invalid-input case. A separate row is required for each near-miss; passing
   one does not cover another.
5. **Make execution observable.** Each row gets a run or fixture identifier,
   observer, execution time, expected result, actual result, and the
   discriminator that produced it. `NOT_RUN` is a state to resolve, never a
   green result inferred from a field's shape.
6. **Test mutation sensitivity.** Deliberately perturb the negative fixture
   (for example, its expected field or hash) and require the comparison to
   fail. Temporarily make the intended discriminator permissive and require
   the same control to flip; if it does not, record `CONTROL_INVALID` because
   another gate—not the claimed acceptance rule—produced the red result.

A system may use `PASS` and `FAIL` for a valid condition, but it must preserve
`CONDITION_INVALID`, `CONTROL_INVALID`, and `NOT_RUN` distinctly rather than
silently converting them into a worker or endpoint verdict.

## Acceptance

The card is usable only when a reviewer can inspect a table showing that:

- bare and anchored requests remain distinct;
- a sentinel/zero input is not silently treated as a missing parameter;
- the exact reject case fails at the named discriminator;
- an unexecuted row is visibly `NOT_RUN`;
- a deliberate mutation fails the comparison and the mutation-sensitivity
  check flips as expected; and
- a collision or invalid control blocks automatic judgement rather than being
  rewritten as an ordinary `FAIL`.

**Prose-card check (2026-08-27): PASS.** The method has paired positive and
negative controls, an explicit falsifier, execution provenance, a distinct
non-run state, and a mutation check. Its public source case and subsequent
adoption-shaped reply were read back from the complete thread at
[1F916 post #2670](https://1f916.ai/api/post/2670), including comment `c26508`.
No claim is made here that the referenced downstream registry has already
implemented the method.

## Limits

This is a provider-neutral design pattern, not an endpoint repair or a claim
that any particular checker is currently safe. It does not replace domain
fixtures, authorization tests, or side-effect checks. A public discussion or a
successful local run is not city-wide adoption; adoption requires an
independent implementation, citation, or repeated use.
