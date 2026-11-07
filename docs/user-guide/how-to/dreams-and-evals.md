---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: dream runs and evaluations

Configure bounded self-improvement (dreams), read its outputs, and decide
whether a candidate primitive change is safe.

**Model (specified, §9, §10, Appendix A):** a dream run is an admitted
workflow with **no administrative authority**: it runs under a **dream
grant** (time, cost share, cell cap, destinations, executor), scheduled by
HQ when the Soul is idle, funded by the **maintenance** sub-allocation
(§8). Accepting instruction changes needs a separate grant.

## Configure a dream run

```bash
hq dream grant <soul> --share 0.1 --wall-clock 2h --cells 8 --executor <adapter>
hq dream schedule <soul> --idle-after 30m
hq dream run <soul> --now        # manual trigger, still under the grant
hq dream show <run-id>
```

> [UNSPECIFIED — proposed] schedule format and verbs; the *grant shape* is
> Appendix A.

## Where outputs land

| What | Where |
|---|---|
| Inputs consumed | `dreams/inputs/` |
| Candidate change | `dreams/runs/<run-id>/candidate/` (full tree, own manifest + digest) |
| Eval results per cell | `dreams/runs/<run-id>/evals/<cell>/` |
| Run record, failures | run directory + candidate revision record |
| Logs | content-free diagnostics with correlation IDs (§12) |

## What a candidate must show before you accept

The candidate revision record carries (§10, Appendix A): a per-cell matrix
for **every assigned harness and understudy**, an in-run baseline,
held-out non-regression within your tolerance, train improvement, **zero
guardrail violations**, absolute counts, render success per adapter,
provenance warnings, and cost. A small replay set is **not** a statistical
guarantee (§9).

Suggested acceptance rule (proposed in
[Operator Questions](../../papers/operator-questions-2026-10-29.md#dreaming-evaluations-and-primitives)):
accept when held-out delta is non-negative on every assigned cell and
train delta is positive on the triggering cell.

## Team standards as evals

The product ships only the hello-world suite. Your team's standards enter
as (a) machine checks in task completion criteria (lint, unit tests,
review rules) and (b) owner-curated tasks marked held-out under `dreams/`
with a dataset digest (§9, §10). Declare any must-never-fail check a
**guardrail** — a guardrail violation disables a route (§9).

## If a candidate fails on one harness

The narrowed candidate is a **new candidate** scoped through per-adapter
overrides, re-evaluated, and shown with change list, matrix, provenance,
and cost. **Partial acceptance is disallowed** (§10, T28). The narrowed
record references the rejected parent and shows the scope diff.

## Harness upgraded? Nothing blocks (by default)

An already-accepted revision keeps running on an upgraded harness **with a
warning**; only a guardrail violation disables a route (§9, §10). What
*is* blocked is accepting a new candidate without coverage
(`eval_coverage_missing`, T27). Accepting an updated pin re-renders every
adapter and requires a passing evaluation cell for every role on that
harness version (§10, T27).

> [UNSPECIFIED — proposed] owner policy flag to *block* instead of warn.

## Rollback

See [rollback how-to](rollback.md) — acceptance of the parent digest,
never an in-place revert; and note the life changes rollback does **not**
undo (§10, §13).
