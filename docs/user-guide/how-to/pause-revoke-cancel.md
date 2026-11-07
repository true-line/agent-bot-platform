---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: pause, revoke, cancel — and what each leaves undone

Interrupt a Soul safely. Specified (§4, §5, §7, §8).

## Pause

```bash
hq soul pause <soul>
```

`pause`/`resume` are hq/v1 operations (§5). Your interactive turn
**preempts background work at its next safe point** (§5, §8). Paused tasks
sit in `waiting` with reason `owner pause` (§7).

**What is *not* paused:** an external effect already submitted cannot be
unstopped. The console shows it as **underway** or **outcome unknown**
until reconciled — never as "paused" (§5, §7, §8).

## Revoke access

```bash
hq grant revoke <soul> <grant-id>     # or rotate/revoke a credential
```

Effective at the **next protected operation** (§4). In-flight cooperative
work on macOS is *reported*, not stopped — that is what cooperative means
([profiles](../../03-architecture/trust-domains-and-profiles.md#protected-vs-cooperative)).

## Cancel a task

```bash
hq task cancel <soul> <task-id>
```

Cancel **stops future actions and reconciles submitted effects**. A late
specialist result arriving after cancel is kept as evidence; it does not
reopen the task (§7). Send reservations settle on retry or cancel (§8).

## Emergency: stop everything

Revoke the credentials *and* revoke the grants *and* pause the Soul. That
stops all protected operations at their next check. For anything already
on the wire to an external service, reconciliation — not revocation — is
the tool:

1. `hq receipts <soul> --outcome unknown` — list effects in flight
2. For each: the returning worker looks up the remote outcome **through
   the broker** and never replays blindly (§7, T06)
3. Ambiguous outcomes wait for your decision — the console asks

> [UNSPECIFIED — proposed] `hq receipts --outcome unknown` filter; the
> *reconciling* state is §7, the filter verb is not yet fixed.

## Checklist: what each control does and doesn't undo

| Control | Stops future | Undoes past effects | Notes |
|---|---|---|---|
| Pause | yes (at safe point) | no | external effects stay underway/unknown |
| Revoke grant/credential | yes (next protected op) | no | typed refusal codes |
| Cancel task | yes | no — reconciles | late results kept as evidence |
| Reconciliation | n/a | resolves unknowns | broker lookup, never blind replay (T06) |

## Related runbooks

- [Reconcile an unknown outcome](../../09-operations/runbooks/reconcile-unknown-outcome.md)
- [HQ restart](../../09-operations/runbooks/hq-restart.md)
