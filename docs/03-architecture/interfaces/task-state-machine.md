---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-05
Normative-Source: true-line/soul-contracts (task/v1 schema + transition table fixture)
---

# Protocol reference: task state machine

The task/v1 lifecycle: nine states, one transition table, compare-and-swap
on revision.

> **Normative source:** the task/v1 commitment request and task record
> schemas (§7, Appendix A) carry the full state machine as an enum plus a
> transition table fixture. This page is a map, not the law.

## States (§7, §8)

| State | Meaning |
|---|---|
| queued | offered, not yet delivered |
| delivered | at a member, not accepted |
| accepted | a member took it |
| running | work in progress |
| paused | owner pause; reason recorded |
| waiting | blocked — reason is one of: owner input, owner pause, dependency, provider availability, reconciliation decision (§7) |
| reconciling | an external effect's outcome is unknown; broker lookup in progress |
| completed | finished; receipts and outcome recorded |
| outcome unknown | terminal ambiguity — evidence kept, owner decides |

## Rules the machine enforces

- **Compare-and-swap on revision**: concurrent writers conflict instead of
  racing (revision conflict vectors in fixtures)
- **Repeated operation ID** refused (dedup vector)
- **Write-scope exclusion**: one exclusive write scope per task (§7)
- Only the **current admitted lead** may finalise task decisions; a
  changed lead gets a new lease generation (§7)
- **Reconciliation, never replay**: an unknown outcome is looked up
  through the broker (§7, T06 —
  [runbook](../../09-operations/runbooks/reconcile-unknown-outcome.md))
- Cancel: stops future actions, reconciles submitted effects; late
  specialist results are evidence only (§7)

## Who runs the machine

The state machine ships as a **library** in `qwts/agent-comms`; it exposes
checks, and **HQ calls them** — the library decides nothing about
authority. The old "comms enforces orchestration" path is removed; client
checks become advisory with the broker repeating them (Appendix B).
