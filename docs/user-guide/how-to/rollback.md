---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: roll back a Soul revision

Undo a bad definition/primitive change. Specified (§5, §10).

## Procedure

```bash
hq revision list <soul>
hq revision rollback <soul> <parent-digest>
# verify the Hello at the old digest in the admission result
```

**Rollback is `rollback-revision`: acceptance of the parent digest — never
an in-place revert.** The previous revision stays pinned. The Soul drains,
then re-admits at the old digest (§5, §10).

## What rollback does *not* undo

The candidate record lists these explicitly:

- **Life changes committed by the same run** — knowledge consolidation,
  index rebuilds, consumed dream inputs (§10)
- **External effects already submitted** (§13) — resolved by
  reconciliation, not rollback
- **Receipts** — history is history

Read the candidate record before rolling back so you know which life
changes will persist.

## After rollback

1. Confirm the admission result names the parent digest.
2. Confirm the console shows the expected profile (§8).
3. If the bad candidate came from a dream run, tighten the dream grant
   (cell cap / guardrails) before the next schedule
   ([dreams and evals](dreams-and-evals.md)).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `revision conflict` on rollback | a newer revision was accepted meanwhile | re-list, choose current parent |
| Soul still reports old behavior post-rollback | render cache / lease not renewed | check lease renewal; re-admission repeats at digest |
| "unknown outcome" during rollback window | task mid-commit when drain started | [reconcile runbook](../../09-operations/runbooks/reconcile-unknown-outcome.md) |
