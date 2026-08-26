---
name: verified-handoff
description: Package a finished agent result so another person can inspect it without asking for hidden text.
version: 1.0.0
status: tested
---

# Verified handoff

Use this when a result is ready to leave the notebook and become a durable
public artifact.

## Method

1. State the problem and the intended consumer.
2. Keep only the smallest sanitized file, example, or pattern that solves it.
3. Add provenance: source type, date, test command, and known limits.
4. Run the focused check and save the result.
5. Publish on a non-main `jerry/*` branch.
6. Open or reuse one pull request.
7. Read the exact file and pull request back from the remote repository.
8. Share the link together with the status: `tested`, `PR`, `merged`, or
   `adopted`.

## Handoff sentence

Use this shape:

> I checked **[problem]**, packaged **[artifact]**, and verified it with
> **[check]**. The current status is **[status]**; the remaining question is
> **[next adoption or review gate]**. Link: **[URL]**.

## Failure rule

If the branch, file, pull request, or read-back fails, say `prepared locally`
or `publication unknown`. Do not say `published` and do not paste a secret or
private working context as a substitute for the link.

## Limits

This card prepares a reviewable handoff. It does not merge a pull request,
deploy city software, or authorize changes to another agent's identity or
permissions.

## Acceptance

The handoff is complete when a fresh reader can open the link, reproduce the
stated check, and see exactly what remains undecided.
