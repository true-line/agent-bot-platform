---
Status: Draft
Doc-Type: runbook
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Verified-Against: S6 §5, §9
---

# Runbook: harness hang or crash loop

Contain a member runtime that hangs or keeps restarting, keep the rest of the Soul working, and find out whether the harness, its adapter or its route is at fault.

**Symptom:** a member is unresponsive, or restarts repeatedly; console
shows the member's runtime flapping; lease age growing.

## Immediate actions

The entry point's **recovery ladder** is specified (§5, §9) — let it work
before intervening:

1. Restart with backoff: automatic
2. **Quarantine after five crashes in one hour**: automatic
3. Re-equip on auth failure: automatic
4. Fail over to the alternate provider on provider outage: automatic

Check the ladder state before doing anything manual — most interventions
below are only needed when the ladder has already run out.

```bash
hq soul status <soul>       # ladder state, lease age per member
```

## Diagnosis

- **Lease stale vs stopped:** a missed lease is *stale*, not stopped (§9)
  — the member's work is not presumed dead until the ladder says so
- **Quarantined:** five crashes in an hour triggered quarantine; find the
  crash cause in the member's runtime logs before releasing
- **Auth failures flapping:** rotated credential not picked up → re-equip
  should resolve; if not, [credentials](../../user-guide/how-to/credentials.md)

## Resolution

- **Hang, ladder exhausted:** stop the member, restart the harness at the
  pinned digest, re-admit. If the crash repeats, render the package fresh
  (`soul build`) — the pin may be corrupt
- **Quarantine:** fix the cause (bad revision? failing provider?), then
  release from quarantine and re-admit
- **Bad revision is the trigger:** [roll back](../../user-guide/how-to/rollback.md)
  rather than patching the live tree

## Verification

- Member rejoins with a fresh lease; census records new runtime for the
  member (identity stays the Soul's)
- Receipts continue under the same task IDs
- No `outcome unknown` left behind by the crashed member — if there are,
  [reconcile](reconcile-unknown-outcome.md)

## Escalation

Crash loop with hostile-member signals (state outside the member home,
direct provider egress) is a containment concern, not an availability
one: capture `hq diag bundle`, revoke that member's grants, and escalate
to security review ([threat model](../../05-security-privacy/threat-model.md)).
