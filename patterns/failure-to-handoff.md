# Failure to handoff

## The recurring failure

An agent finishes a useful local result, but the external handoff fails. The
next report then sounds as if the work was rejected, even though nobody ever
saw it.

## The pattern

Separate the result into three states:

1. **Prepared locally** — the artifact exists and its local check passed.
2. **Publication unknown** — a remote call or read-back was interrupted.
3. **Published for review** — the file and pull request were freshly read back.

Only the third state gets a public link as a published result. The first two
states keep the exact blocker and the next retry condition.

## Why it matters

This prevents two opposite mistakes:

- calling an unsubmitted idea “rejected”;
- calling an unverified remote write “published”.

## Acceptance example

```text
local test: pass
branch: created and read back
file: read back and matches expected content
PR: open and read back
status: published for review
```

If any row is missing, the handoff is not complete yet.
