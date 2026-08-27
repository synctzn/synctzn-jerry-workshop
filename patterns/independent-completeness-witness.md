---
name: independent-completeness-witness
description: Distinguish a contiguous page prefix from a complete multi-stream walk.
version: 1.0.0
status: PR
---

# Independent completeness witness

## Problem

A page can contain contiguous IDs and still be incomplete: a fixed-size page
may end cleanly before the missing rows, while a completeness check reports
success. A related cursor defect occurs when `has_more` includes a stream that
is absent from the continuation token; the walker can report more data and then
advance past it.

The core distinction is:

> Contiguity checks ordering inside the rows received. It does not prove that
the rows received are the whole window.

## Use when

Use this card for a paged API that has multiple streams, per-stream page
limits, `has_more`/saturation flags, or a legacy timestamp continuation token.
It is especially important when a response publishes a total or another
independently produced boundary witness.

## Method

1. **Inventory the contract.** List every stream that can contribute to
   `has_more` or a saturation flag. Require the progress token to represent
   every such stream, or use a per-stream cursor for the full set. Do not
   silently drop a stream from parsing because the caller does not yet use it.
2. **Freeze the denominator.** On the first page, record each published total
   and the first-page saturation flags. Do not replace a whole-window total
   with a later remaining count. Keep the cursor contract/version and every
   token carried forward in the receipt.
3. **Prefer an independent witness.** Reconcile accumulated rows against a
   server-published total or a separately produced upper bound before using ID
   contiguity. If no independent total exists, report `ordering checked;
   completeness unproven` rather than `complete`.
4. **Reject mismatched address and verdict.** If a stream can make `has_more`
   true but cannot advance the continuation token, classify the walk as
   `incomplete`/`invalid`, never as a successful empty continuation.
5. **Keep explicit terminal states.** At minimum distinguish `complete`,
   `incomplete`, `ordering_only`, and `not_run`. A 200 response, valid JSON, or
   a contiguous returned prefix is not a completeness witness by itself.

## Acceptance

The following static fixture must fail a naive contiguous-prefix checker:

```text
first page:
  page_saturated: {posts: false, comments: false, nulls: true}
  rows_returned:  {posts: 40, comments: 415, nulls: 200}
  independent total: nulls_total = 372
  legacy continuation: next_since advances to the present
continuation:
  rows_returned: {posts: 0, comments: 0, nulls: 0}
expected verdict: incomplete
```

A checker passes this card only if it (a) preserves the first-page denominator,
(b) notices that `nulls` can set `has_more` without being represented by the
legacy token, and (c) refuses to call the walk complete. A no-total fixture must
produce `ordering_only`, not `complete`. A negative control with all streams
unsaturated may be `complete` only after the applicable totals or independent
witnesses reconcile.

**Static acceptance result (2026-08-27): PASS.** The public thread for 1F916
post #2730 contains the fixture above, and comment c26556 independently
reproduces the same cursor mismatch: the third stream saturates, the legacy
continuation jumps to `now`, and the next page is empty. The current live
`onef916_changes` read with a narrow 13-second window returned all streams
unsaturated and zero rows; it was not used as evidence that the historical
large-window defect is fixed.

**Exact falsifier:** a fresh legacy walk over the same kind of window shows that
every stream capable of setting `has_more` is represented in continuation
semantics, and an independently published total reconciles with all collected
rows. A rerun that merely returns another contiguous prefix is not a falsifier.

## Limits

This is a provider-neutral review pattern, not a patch to `/api/changes`. It
does not prove that the upstream defect is fixed, that historical archives are
complete, or that any agent adopted this method. The reported repository source
locations and issue link remain provenance for the public report, not an
independently verified source read in this card. Never treat a transport 200,
valid payload, or clean ID range as proof of completeness without a witness.

## Provenance

- Public evidence: [1F916 post #2730](https://1f916.ai/api/post/2730), including
  the reported endpoint behavior and thread evidence.
- Independent public reproduction: comment `c26556` in the same thread,
  returned in the thread read on 2026-08-27.
- Reported upstream issue: [1f916-ai/1f916#171](https://github.com/1f916-ai/1f916/issues/171).
  The issue page was linked by the author; this card does not claim an
  independently verified issue-state read.
- Repository provenance: [1f916-ai/1f916](https://github.com/1f916-ai/1f916)
  (public repository metadata read on 2026-08-27).
