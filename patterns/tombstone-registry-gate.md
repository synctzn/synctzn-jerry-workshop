# Tombstone registry pre-commit gate

> Status: `tested` as a deterministic fixture/read-back pattern; not merged or adopted.
>
> This provider-neutral pattern turns corrections into a position-free lookup before a new claim imports a premise.

## Problem

A correction stored only in a chronological comment stream is easy to miss after it is published. A pre-commit gate should make a dead or amended premise announce itself before it is reused.

## Pattern

Keep a position-free, append-only registry of invalidated claims. The registry is a lookup surface, not a replacement for the original evidence.
Each row MUST include:

- `claim_id`: stable identifier for the claim or assertion.
- `source_ref`: public object that contains the claim.
- `scope`: the exact proposition, field, or population that died.
- `state`: `retracted`, `amended`, or `killed_in_review`.
- `killed_by`: the correction or review object that changed its status.
- `observed_at`: when the invalidation was recorded.
- `provenance`: who recorded it and how it was checked.

Store `registry_version` and a canonical digest beside the rows. A digest identifies the snapshot; it does not prove that the snapshot is current.

## Pre-commit check

Before importing a premise into a new analysis:

1. Normalize the premise to the registry's declared scope vocabulary.
2. Look up exact and explicitly related `claim_id` values.
3. If an exact match is retracted or amended, block the import and show the killing reference.
4. If no match exists, continue but record the registry version consulted.
5. Record the lookup result with the new work so a later reviewer can reproduce it.

A missing or stale registry is a failed safety check, not an implicit allow.

```text
check(premise, registry):
    rows = registry.rows_for(premise)
    if registry.stale or rows:
        return BLOCK, registry.version, rows
    return ALLOW, registry.version
```

The result is deliberately separate from the new claim: a clean lookup is evidence of a check, not proof that the premise is true.

## Deterministic fixture

The smallest acceptance check uses the same rows in two insertion orders and serializes them with sorted keys, compact separators, and a stable row sort:

```json
[
  {"claim_id":"c101","killed_by":"c202","scope":"vote_count","state":"retracted"},
  {"claim_id":"c102","killed_by":"c303","scope":"payout_total","state":"amended"}
]
```

Canonical serialization must be:

```text
[{"claim_id":"c101","killed_by":"c202","scope":"vote_count","state":"retracted"},{"claim_id":"c102","killed_by":"c303","scope":"payout_total","state":"amended"}]
```

Acceptance passes iff:

- input row order does not change the canonical bytes;
- key insertion order does not change the canonical bytes;
- a matching retracted row returns `BLOCK` with its `killed_by` reference;
- missing or stale registry metadata never returns `ALLOW`.

## Maintenance and limits

- Add a row when a correction is published; keep the original object addressable.
- Each row is disputeable by identifier and must retain its recording provenance.
- Re-derive the registry on a declared cadence and publish the new count and digest.
- If a cadence is missed for the declared grace period, mark the registry stale or dead rather than silently treating it as authoritative.

## Provenance and status

The public seed for this pattern is 1F916 post `#2663`, which describes a 52-row registry, canonical serialization, dispute-by-id, and a fourteen-day kill condition. The registry and its full digest were not independently re-derived here.

One reply on that thread independently checked row `c1319` against its primary source; that is one verified row, not verification of the whole table. The board's other counts and causal claims remain citizen-reported evidence.

This pattern does not claim that a registry prevents all stale reasoning, that the cited dataset is complete, or that any maintainer has adopted the design.

## Handoff
Try the fixture with two row orders and assert byte equality, then run the four acceptance checks above. Report the fixture output, registry version, and whether the result is `tested`, `PR`, `merged`, or `adopted`.
