---
Status: Draft
Doc-Type: runbook
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Verified-Against: S6 §7; T06
---

# Runbook: reconcile an unknown outcome

Settle an external effect whose result was lost, by asking the remote service what happened rather than sending the request again.

**Symptom:** a task is in `reconciling`; the console shows an action as
**outcome unknown** — the effect may or may not have landed on the remote
service (§7, T06).

## Immediate actions

**Do not re-run the action.** Blind replay is the failure mode this
runbook exists to prevent.

1. Leave the task in `reconciling`.
2. List the unknown effects:

```bash
hq receipts <soul> --outcome unknown
```

3. If the returning worker is alive, it looks up the remote outcome
   **through the broker** (§7) — let it finish.

## Diagnosis

| Signal | Meaning | Action |
|---|---|---|
| Worker returns, broker lookup succeeds | outcome resolved automatically | verify receipt settled state |
| Broker lookup fails / destination unreachable | still ambiguous | keep in reconciling; check destination status page |
| Worker dead (crash loop) | nobody to look up | [harness crash loop](harness-crash-loop.md) first, then return here |
| Outcome genuinely undecidable remotely | ambiguous | wait for owner decision |

## Resolution

- **Resolved:** receipt settles; task leaves `reconciling`.
- **Ambiguous:** the task **waits for your decision** (§7, T06). The
  console presents the action digest and everything known. Decide:
  treat-as-applied (skip re-submission) or treat-as-failed (allow a fresh
  action under a new operation ID).
- After resolution, `hq receipts <soul> --task <task-id>` must show no
  `unknown` rows for that task.

## Verification

- No `outcome unknown` entries remain for the task
- Late-arriving duplicate results are kept as evidence only — the task
  does not reopen (§7)
- If you chose treat-as-failed, the retry runs under a **new operation
  ID** (dedup must not swallow it, §6)

## Escalation

If the destination cannot report state at all (no idempotent lookup), that
is a service-adapter gap, not an operator problem — escalate with
`hq diag bundle` and the receipt digests
([diagnostics](../../user-guide/how-to/diagnostics.md)).

## Why this design

Reconciliation over replay is specified in §7 and proven by T06: an
unknown outcome must be *looked up*, never assumed. Pausing a Soul does
not pause effects already submitted — see
[pause/revoke](../../user-guide/how-to/pause-revoke-cancel.md).
