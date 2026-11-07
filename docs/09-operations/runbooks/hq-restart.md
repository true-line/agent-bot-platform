---
Status: Draft
Doc-Type: runbook
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Verified-Against: S6 §5, §7, §12 (partly specified)
---

# Runbook: HQ crash and restart

Recover after the HQ process (agent-bot-daemon) stops, without losing task, lease or intent state and without replaying any external effect.

**Symptom:** HQ daemon down; Souls still running local read-only work;
protected operations stalled.

## What is safe by design

Specified:

- Leases expire → **protected commits stop** while local read-only work
  continues (§5)
- Action intents and the outbox are **durable** (§7, §12) — submitted
  effects survive the crash as *unknown outcomes* to reconcile, not to
  replay
- On restart, **admission repeats** (§5)

## Immediate actions

1. Restart HQ under the OS supervisor.

```bash
# the OS supervisor restarts HQ (agent-bot-daemon); unit name unspecified
hq doctor     # report leases, intents, unknown actions needing reconciliation
```

> [UNSPECIFIED — proposed] HQ runs under the OS supervisor with ledger
> crash persistence stated in the §12 storage baseline; `hq doctor`
> reporting is the proposed surface. Track both.

2. Let admission repeat for each Soul; check the admission results.
3. Work the `hq doctor` list: expired leases re-acquire; **unknown actions
   reconcile** — see [reconcile runbook](reconcile-unknown-outcome.md).
   Never blind-replay.

## Diagnosis

| After restart you see | Meaning | Action |
|---|---|---|
| Souls re-admit, leases renew | healthy | verify receipts flowing |
| Souls refuse admission | key store / authority DB damaged | restore from backup, then [backup/restore](../../user-guide/how-to/backup-restore-transfer.md) |
| Duplicate external effects reported | dedup records lost | ledger reconstruction needed — escalate, this should be impossible if §12 persistence holds |
| Outbox entries stuck | broker host not up | check broker binding; re-deliver per wake class |

## Verification

- `hq doctor` reports clean: no intents pending, no unknown actions
- Receipt timeline resumes; send reservations settle (§8)
- Console shows the correct profile on every re-admitted Soul (§8)

## Escalation

Authority database loss is the one unrecoverable-without-backup case:
restore per [backup/restore](../../user-guide/how-to/backup-restore-transfer.md) —
secrets and reusable grants excluded from export, so they are re-added
manually. Attach `hq diag bundle` to the incident
([diagnostics](../../user-guide/how-to/diagnostics.md)).
