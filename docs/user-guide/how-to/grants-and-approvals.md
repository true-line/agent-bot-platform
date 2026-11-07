---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: grants and approvals

Give a Soul standing authority for a *class* of work, and handle the
single-action approvals when it reaches the edge.

**Model (specified, §4, §8, Appendix A):** grants carry action and resource
selectors, destinations, data restrictions, expiry, and a budget/ceiling.
Standing grants are "standing policies": authorize a class once; the broker
enforces per operation.

## Add a standing grant

```bash
hq grant add <soul> --resource <selector> --action <read|write|…> \
  --destination <id> --expiry <date> --ceiling <amount>
```

Selectors: resource paths (path globs under the protected profile's
mediated workspace views — proposed), destinations, data restrictions.
Narrow first, widen with evidence.

## What happens at the edge

When a task exceeds its authority the broker **refuses with a typed code**
(`destination_denied`, `grant_revoked`, `budget_exhausted`, Appendix A)
and the task moves to `waiting for owner input` (§7). The Soul does not
retry around the refusal.

## Approve one action

The approval request names: the exact action or policy change, the
resource and destination, why existing authority is insufficient, expected
cost, and expiry (§8).

Approve the single action — it grants nothing beyond **that record's
digest**; editing the action invalidates the approval (T24).

## Approve a bounded class

To avoid prompt fatigue, approve a bounded class instead (same §8
mechanism). Prefer expiry + ceiling to make the class self-limiting.

## Revoke

```bash
hq grant revoke <soul> <grant-id>
```

Revocation takes effect at the **next protected operation** (§4).
Already-submitted external effects are *not* undone — they are reconciled
([pause/revoke](pause-revoke-cancel.md)).

## Audit what authority exists

```bash
hq grant list <soul>        # standing grants, expiry, ceilings
```

> [UNSPECIFIED — proposed] `hq grant list` output; the grant *record* is
> Appendix A, the verb is not yet fixed.

## Related

- Receipts always record which profile enforced (or merely reported) each
  action (§4, R8) — see [trust domains](../../03-architecture/trust-domains-and-profiles.md#protected-vs-cooperative)
- Workspace path-scope details: [Operator Questions → Repository and tool setup](../../papers/operator-questions-2026-10-29.md#repository-and-tool-setup)
