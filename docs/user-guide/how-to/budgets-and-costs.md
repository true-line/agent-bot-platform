---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: budgets and cost attribution

Set spend limits for model calls, evaluation runs, network use, and dream
runs; attribute settled cost to tasks and members.

**Model (specified, §8, §10, §15, Appendix A):** one ceiling per Soul with
**working** and **maintenance** sub-allocations. Grants carry a budget and
cost ceiling; the dream grant carries time, cost share, and cell cap.
Network is an allowlist plus the broker's narrow API (§4). There is
deliberately **no per-member limit** — participation is a Soul-level
policy, so four members never get four allowances.

## Set the ceiling and sub-allocations

```bash
hq budget set <soul> --ceiling <amount> \
  --working <share> --maintenance <share>
```

Maintenance funds sleep/dream upkeep; working funds assigned tasks.
Set on grant records via CLI or GeniusBar.

## Where limits bite

| Limit | Enforced | When |
|---|---|---|
| Soul ceiling | broker | any protected spend |
| Grant ceiling | broker | per grant, per destination |
| Dream share/cells | scheduler | when scheduling dream runs (§10) |
| Network allowlist | broker egress | every destination check (§4) |

Refusals are typed codes (`budget_exhausted`, Appendix A) and the task
waits for you — it does not silently degrade.

## Read cost attribution

```bash
hq receipts <soul> --task <task-id>     # per-task, per-member settled cost
hq receipts <soul> --destination provider/anthropic
```

Every receipt records task, caller (member and runtime), destination,
adapter route, and **settled cost** (§7); cost per accepted task is a
release criterion (§15). Sensitive payload is stored separately under its
own access policy; receipts carry a request digest instead (§7).

## What leaves the machine (and how to restrict it)

Specified (§4, §6, §10): remote model — task context the broker sends,
after checking destination against task data restrictions; relay — **outer
frame only** (destination, epoch hint, message ID, expiry, size, wake
class), content sealed, timing/size observable; eval exports apply the
same disclosure restrictions as the original task. To restrict further:
tighten destinations per grant, use disclosure labels, or point at a
**local model** destination.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `budget_exhausted` early in the month | maintenance share consumed by dreams | re-balance sub-allocations, or shrink dream share |
| Cost attributed to "unknown" member | caller died mid-action | reconcile; receipts keep the runtime id |
| Spend without receipts | cooperative egress on macOS | expected on cooperative; see profile warning |
