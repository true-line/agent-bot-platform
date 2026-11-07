---
Status: Draft
Doc-Type: tutorial
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# Tutorial: your first pilot task on real work

Move from `hello.soul` to a real task on a real repository with real
credentials — scoped, receipted, and reversible. This is the Stage 3 pilot
flow (§13); functional and operational targets come from §14, proven by
T16, T22, T24, T27–T30.

## Before you start

- Completed the [quickstart](quickstart.md)
- A repository you can afford to have an agent write to
- Provider key + a GitHub App (private key goes to **HQ**, never the
  package — §11)
- Decide the profile honestly: on **macOS cooperative**, give the Soul only
  credentials you would give its least-trusted harness
  ([why](../../03-architecture/trust-domains-and-profiles.md#protected-vs-cooperative))

## 1. Import or create the production Soul

```bash
hq soul create pilot-soul --template team-standard.soul
# or
hq soul import pilot.soul
```

## 2. Assign lead and specialist

Pick the lead as the harness with the best evaluation **on your own task
set** with a qualified ACP adapter; the specialist is the narrower role
([choosing harnesses](../../papers/operator-questions-2026-10-29.md#getting-started)).

```bash
hq soul roles pilot-soul --lead claude-code --specialist codex
hq adapters list   # qualified profile, primitive classes, last evaluation date
```

> [UNSPECIFIED — proposed] `hq adapters list` output shape; each release
> ships a signed qualification manifest per adapter version.

## 3. Grant exactly what the task needs

```bash
hq grant add pilot-soul --resource "repo/acme/widget" --action write \
  --destination github.com/acme/widget --expiry 2026-12-01 --ceiling 50
```

Grants carry action and resource selectors, destinations, and data
restrictions (Appendix A). Narrow now; widen later with evidence.

## 4. Add credentials to HQ

```bash
hq credential add github-acme
hq credential add anthropic
```

References only reach harnesses at `Equip` (§5); verify the boundary with
`hq audit secrets` ([credentials how-to](../how-to/credentials.md)).

## 5. Set the budget

One ceiling with **working** and **maintenance** sub-allocations (§8).
There is deliberately no per-member limit — four members never get four
allowances ([budgets how-to](../how-to/budgets-and-costs.md)).

## 6. Offer the task

```bash
hq task offer pilot-soul --objective "<the real objective>" \
  --scope "repo/acme/widget" --write-scope "src/**"
```

Tasks carry a resource scope and an exclusive write scope (§7).

## 7. Supervise, approve, and let it finish

- The Soul works; when it hits a permission edge it stops in
  `waiting for owner input` and the **approval request** names the exact
  action, resource, destination, why existing authority is insufficient,
  expected cost, and expiry (§8). Approve the single action or a bounded
  class — a single-action approval grants nothing beyond that record's
  digest (T24).
- Interrupt any time: your interactive turn preempts background work at
  the next safe point (§5,
  [pause/revoke how-to](../how-to/pause-revoke-cancel.md)).

## 8. Review the evidence

```bash
hq receipts pilot-soul --task <task-id>
```

Interleave **receipts** (authoritative) with **notes** (self-reported
memory — not evidence) (§10). Cost attribution per task and per member
comes from settled receipts (§15).

## What you just did

A real task ran under scoped grants with brokered inference, one ceiling,
digest-bound approvals, and full receipts. Next steps: set up
[dream runs and evaluations](../how-to/dreams-and-evals.md), learn
[rollback](../how-to/rollback.md), and rehearse
[backup/restore](../how-to/backup-restore-transfer.md) before
you need it.
