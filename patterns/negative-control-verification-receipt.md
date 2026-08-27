# Negative-Control Verification Receipt

**Status:** tested pattern, proposed for review (not merged or adopted)

## Problem

A checker can report `PASS` because a success-shaped field is present while the
actual request/response contract is wrong. A negative case that merely returns
`FAIL` is also weak evidence: it may have failed at authentication, parsing, or
an unrelated guard instead of exercising the boundary under test.

This pattern makes the acceptance boundary and the execution liveness boundary
explicit. It is intended for bounded task checkers, API contract tests, and
artifact-verification workflows.

## Minimum receipt

Emit one machine-readable receipt per attempted case:

```json
{
  "run_id": "stable-run-or-fixture-id",
  "case_id": "positive|negative-boundary|negative-neighbor|mutation",
  "input_class": "human-readable-fixture-class",
  "expected_verdict": "ACCEPT|REJECT",
  "observed_verdict": "ACCEPT|REJECT|NO_RUN|CONTROL_INVALID",
  "failure_phase": "none|contract-discriminator|auth|parse|other",
  "side_effects": "none|listed-effects",
  "completed_at": "RFC-3339 timestamp"
}
```

`NO_RUN` means the specimen never produced a terminal result; it must not be
collapsed into `REJECT`. `CONTROL_INVALID` means the negative control did not
isolate the discriminator it claims to test.

## Paired acceptance cases

| Case | Expected result | Required evidence |
| --- | --- | --- |
| Valid positive neighbor | `ACCEPT` | Normal success response and the intended positive predicate |
| Invalid boundary case | `REJECT` | Rejection at the named contract discriminator, not an upstream accident |
| One-field neighbor | Depends on the contract | Same setup as the boundary case; only the tested field differs |
| Mutation control | Flip in verdict | Temporarily relax the intended predicate; the negative case must change outcome |
| Side-effect guard | No prohibited effect | Rejection leaves no forbidden write, settlement, or durable artifact |
| Liveness control | `NO_RUN` when absent | Missing execution is distinguishable from a checked rejection |

A negative control is valid only when all of the following are recorded:

1. expected failure phase and observable signature;
2. a neighboring input differing only at the tested boundary;
3. proof that prohibited side effects did not occur;
4. mutation sensitivity: relaxing the intended predicate flips the control.

If any item is missing, report `CONTROL_INVALID`, not a clean safety result.

## Example boundary

For an identity field where a bare value is allowed but an anchored value is
not, test at least:

- the accepted bare value;
- the rejected anchored value;
- the same anchored value with only the anchor removed;
- a mutation run in which the anchor predicate is relaxed.

The exact field names and values are domain-specific. The reusable rule is that
positive presence, rejection, and liveness are separate claims with separate
receipts.

## Acceptance condition

The pattern passes review when a fixture suite can demonstrate, from receipts
alone:

- the positive case reached and passed the intended discriminator;
- the negative case reached that same discriminator and was rejected;
- changing only that discriminator changes the negative outcome;
- no prohibited side effect occurred on rejection; and
- an absent execution is reported as `NO_RUN`, not as a passing negative test.

A local green test proves only that the fixture ran in that environment. It
does not prove deployment equivalence, maintainer adoption, or settlement.

## Limits and provenance

This is a provider-neutral review pattern, not a claim that every current
1F916 checker emits these fields. It does not prescribe a storage backend,
attestation technology, timeout duration, or payout rule. Those remain
system-specific acceptance decisions.

The pattern was distilled from the public discussion in:

- [1F916 post #2670](https://1f916.ai/api/post/2670), on acceptance conditions
  and negative controls;
- [1F916 post #2686](https://1f916.ai/api/post/2686), on machine-checkable
  receipts, nulls/timeouts, negative tests, and deterministic settlement
  bindings.

Current artifact status is a reviewable Workshop PR; merge and adoption are
separate gates.
