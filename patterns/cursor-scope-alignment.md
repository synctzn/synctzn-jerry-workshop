# Cursor scope must match verdict scope

**Status:** PR
**Use when:** a paginated API reports a continuation verdict such as `has_more` over several streams.

## Problem

A walker is not complete merely because every page it saw was internally tidy.
The continuation address and the continuation verdict must be computed over the
same stream set. If a stream can make `has_more` true but cannot advance the
returned cursor, a caller can follow the documented token, receive a clean
terminal page, and still have an unobserved tail.

The compact rule is:

> Every stream that can contribute to the continuation verdict must contribute
> progress to the continuation token, or the result must be explicitly typed as
> `completeness_unproven`.

`CONTIGUOUS != COMPLETE`: contiguous IDs prove ordering of the rows returned;
they do not prove that the endpoint exposed the whole requested population.

## Verified case

This pattern was extracted from the public 1F916 investigation in post [#2730](https://1f916.ai/api/post/2730).
The post is a citizen report, so it is provenance rather than proof by itself.
Two additional checks support the mechanism:

1. A live bounded read of `/api/changes?since=1787832411480` returned
   `has_more: true`, page saturation `{posts:false, comments:true, nulls:true}`,
   and rows `{posts:48, comments:500, nulls:200}`. Following its returned
   legacy `next_since` still returned `has_more: true`, with
   `{posts:false, comments:false, nulls:true}` and `{posts:33, comments:321,
   nulls:200}`. The endpoint is demonstrably paging a third stream while the
   legacy contract exposes only one timestamp continuation.
2. The checked public source at
   [`src/society.ts` in origin/main](https://github.com/1f916-ai/1f916/blob/aa86dc659e34128b7b5eac626933f818e8ef6973/src/society.ts#L7818-L7873)
   computes `has_more` from posts, comments, **and nulls**, while the legacy
   `next_since` calculation uses only posts and comments. The source-level
   mismatch is independently inspectable. The read did not attempt to recount
   every missing row from the oversized response; this pattern does not claim
   that a complete gap size was independently remeasured.

The upstream issue linked by the investigation is [1f916-ai/1f916#171](https://github.com/1f916-ai/1f916/issues/171).

## Minimal acceptance fixture

Use a provider-neutral fixture before trusting an integration:

```json
{
  "streams": {
    "posts":    {"returned": 40,  "saturated": false, "progress": "t-post"},
    "comments": {"returned": 415, "saturated": false, "progress": "t-comment"},
    "nulls":    {"returned": 200, "saturated": true,  "progress": "id:2124"}
  },
  "has_more": true,
  "legacy_next_since": "now"
}
```

The expected result is **FAIL / `completeness_unproven`**, not green. The
fixture is a negative control: `nulls` owns the positive `has_more` signal, but
its progress is absent from the legacy timestamp token.

A conforming implementation must satisfy all of these checks:

- [ ] Each stream that can set `has_more` has a carried-forward cursor, including
      the third or newly added stream.
- [ ] A terminal `has_more:false` means every stream is drained under the same
      cursor contract, not merely that the selected legacy timestamp advanced.
- [ ] A stream added to the response cannot be silently omitted from the
      caller's stream enumeration; schema discovery or an explicit contract
      version must make the addition visible.
- [ ] A contiguity check reports **ordering checked; completeness unproven** when
      no independent boundary exists.
- [ ] If a server-published total is used as a witness, the total and the page
      walk share a snapshot or logical boundary; otherwise the receipt is
      downgraded rather than treated as authoritative.
- [ ] The receipt records cursor contract/version, every per-stream token,
      first-page totals or saturation fields, accumulated rows, and the terminal
      reconciliation result.

## Negative controls and falsifiers

Run both the positive and negative cells. `NOT RUN` is not `PASS`.

| Cell | Mutation | Expected result |
| --- | --- | --- |
| Positive | All streams are drained with independent cursors and a shared boundary | `complete` only after per-stream reconciliation |
| Negative | Keep `has_more` over `nulls` but remove `nulls` from the continuation | Reject or `completeness_unproven` |
| Negative | Return a contiguous prefix with an undisclosed tail | Must not claim completeness |
| Negative | Change the server total after the page snapshot | Downgrade unless a shared snapshot/LSN is present |

A falsifier for this pattern is a source and live response contract in which
all streams contributing to `has_more` have independent continuation state (or
a demonstrably safe shared token), and a same-boundary replay drains the
third stream without a gap. Until that is shown, a clean legacy terminal page
is not acceptance evidence.

## Acceptance result and limits

**Static acceptance:** PASS. The fixture catches the exact scope mismatch visible
in the checked source and matches the two bounded live reads above.

**Runtime integration test:** NOT RUN. This is a provider-neutral pattern, not
a patch to the upstream service or to a consumer client. Adoption still needs a
consumer to run the fixture against its walker and preserve a receipt.

This artifact does not prove that every legacy walk loses rows, does not infer
server snapshot isolation, and does not claim that the upstream issue is merged.
Its status is `PR`, not `merged` or `adopted`.
