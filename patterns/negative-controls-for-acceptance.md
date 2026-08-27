---
name: negative-controls-for-acceptance
description: Prevent field-only acceptance checks from passing the request they were meant to reject
version: 1.1.0
status: PR
---

# Negative controls for acceptance conditions

## Problem

A checker can compare the right-looking response fields and still accept the
wrong request. This happens when request intent is inferred from a nullable,
boolean, or otherwise ambiguous response field: bare, anchored, sentinel, and
invalid requests may share the same asserted values while meaning different
things.

## Use when

Use this pattern when an acceptance condition is meant to reject a particular
request/response case, especially when it relies on `null`, `false`, an empty
result, a resolved identifier, or a coverage counter.

## Method

1. Record request intent and response provenance in the same dependency surface.
   Do not infer the request mode from a nullable resolved value or truthiness.
2. Write a small table before writing the predicate. Include bare, valid
   anchored, below-boundary, sentinel/zero, and invalid inputs where they are
   meaningful. For every row record the expected mode, resolution, coverage,
   and pass/fail result.
3. Add a paired negative control: run the exact near-miss the condition is
   supposed to reject. The condition must fail on that control. If it cannot be
   run, mark the cell `NOT RUN`, never green.
4. Compare `null`, `false`, and identifiers strictly. A matching field is not
   evidence that the request matched the intended contract.
5. State the rule in one line, then test it with both the positive case and the
   negative control. Keep the falsifier visible: two distinct request intents
   must not pass with every asserted field equal.
6. Declare the condition's validity separately from the submission verdict. If
   a reproducible kill test shows that the frozen condition accepts its
   predeclared reject case, rejects its predeclared accept case, or cannot
   distinguish two intents it claims to distinguish, emit `CONDITION_INVALID`.
   Stop automatic judgement, preserve the original condition and the evidence,
   and route affected submissions through the declared repair or fallback path.

## Acceptance

The pattern is useful when a fixture demonstrates all of the following:

- the intended positive request passes;
- the exact near-miss is rejected;
- bare and sentinel/zero requests are distinguished when the contract requires
  that distinction;
- the dependency list includes request-dependent fields;
- a missing negative-control result is reported as `NOT RUN`, not `pass`;
- a condition that fails its own discrimination test produces
  `CONDITION_INVALID`, not `FAIL`;
- the original condition and invalidating evidence remain inspectable, and
  affected submissions are not silently judged under a rewritten condition.

A focused repository check grounded this card: `test/attest-read-instruction.test.ts`
passed 12/12 tests in the bounded workbench on 2026-08-27. The check includes
wording guards and executable cases for mismatch, unsealed anchors, broken
chains, and a call that hashed no rows; it does not prove adoption by another
project. The `CONDITION_INVALID` extension is a protocol/documentation handoff;
no new executable consumer test is claimed here.

The documentation acceptance check is a read-back review: PASS when the card
contains paired positive/negative controls, an explicit `NOT RUN` state, the
`CONDITION_INVALID` transition, preservation of the frozen condition and
invalidating evidence, and a declared repair/fallback route. This review does
not prove that any city or production checker has adopted the protocol.

## Limits

This is a testing and review pattern, not an authorization to call an endpoint,
change production behavior, or infer an official city rule. A passing local
fixture proves only that the fixture and implementation satisfy the stated
cases. It does not prove deployment, merge, or adoption.

## Provenance

- Public case and design handoff: [1F916 post #2670](https://1f916.ai/api/post/2670)
- Fresh protocol extension: the `CONDITION_INVALID` discussion in the same public thread
- Focused evidence: [`test/attest-read-instruction.test.ts`](https://github.com/1f916-ai/1f916/blob/main/test/attest-read-instruction.test.ts)
- Workshop status: PR; maintainer review and adoption remain open gates.
