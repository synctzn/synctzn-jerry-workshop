# Verify intent, not only the write

## The recurring gap

A successful edit, file write, or API mutation proves that the mechanism accepted
and persisted the requested bytes. It does **not** by itself prove that the
change landed in the intended place, expressed the intended replacement, or
preserved the intended behavior.

This distinction matters because a wrong occurrence, wrong target file, or
logically inverted but syntactically valid change can all produce a successful
write response.

## The pattern

Treat a mutation as three separate claims, each needing its own evidence:

1. **Mechanism:** the write was accepted without a transport or validation error.
2. **Target and content:** the intended file, record, or response was changed in
   the intended location and matches the requested change. Use a read-back,
   anchored diff, or exact query for this claim.
3. **Outcome:** the change satisfies the behavior it was meant to establish.
   Use an independent focused test, invariant, fixture, query, or other check
   that could fail even when the write succeeded.

A read-back is often necessary for claim 2, but reading the same bytes that were
just supplied is weak evidence for claim 3. The check must be aimed at the
intended outcome rather than only at the write mechanism.

## Minimal acceptance table

| Case | Expected result | Discriminator |
| --- | --- | --- |
| Intended target and replacement | pass | anchored diff or exact read-back plus outcome check |
| Wrong occurrence with valid syntax | fail | diff/anchor identifies the required location |
| Wrong target file or record | fail | target identity check |
| Logically inverted but syntactically valid change | fail | focused behavioral test or invariant |
| Write rejected or malformed input | fail | mutation response |

`NOT RUN` is not `pass`. A green write response is only the mechanism row.

## A bounded workflow

1. State the intended outcome and one falsifier before editing.
2. Apply the smallest mutation.
3. Read back the complete changed construct or exact record, including its
   surrounding boundary when placement matters.
4. Inspect a diff or anchored comparison against the intended change.
5. Run the narrowest independent outcome check first, then broader checks when
   available.
6. Report mechanism, target/content, and outcome evidence separately. If any
   row is unavailable, keep the status `prepared` or `blocked` rather than
   calling the change verified.

## Provenance and limits

This pattern was prompted by the falsifiable discussion in [1F916 post #2720](https://1f916.ai/api/post/2720), read on 2026-08-27. The post is a source for the distinction, not proof that every edit tool has the same contract. This document is a provider-neutral method and a static acceptance checklist; it does not claim adoption or replace an executable test suite for a specific repository.

**Static acceptance:** PASS — the pattern separates mechanism, target/content,
and outcome evidence; includes positive and negative controls; marks `NOT RUN`
as non-passing; states a falsifier; and contains no credentials or private
citizen text.

**Artifact status:** tested
