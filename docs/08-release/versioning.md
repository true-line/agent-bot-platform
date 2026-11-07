---
Status: Draft
Doc-Type: reference
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Scope: platform, protocol, schema, adapter versioning policy
---

# Versioning and compatibility policy

How versions move: schemas, protocols, packages, adapters, harnesses.

## Layered version model

| Layer | Versioned by | Compatibility rule | Enforced by |
|---|---|---|---|
| Schemas (Appendix A) | soul-contracts | add-only via registry; fixtures updated in same PR | CI fixture validation |
| Protocols (hq/v1, wire/v1) | frame version field | version mismatch refused | T14 |
| `.soul` format | format 1/2 | import validation refuses unknown | import gate (§11) |
| Definition revisions | per-Soul | new revision ≠ new Soul ID; parent stays pinned | revision records (§10) |
| Adapters | qualification manifest per version | profile + primitive classes declared | compatibility matrix (§12) |
| Harnesses | external | upgrade marks cells **unevaluated** | §9, §10 |

## Adapter/harness upgrade behavior

Specified: an upgraded harness **warns and keeps running** an accepted
revision; only a guardrail violation disables a route. Accepting a new
candidate without eval coverage is blocked (`eval_coverage_missing`,
T27). Accepting an updated pin re-renders every adapter and requires a
passing evaluation cell for every role on that harness version.

> [UNSPECIFIED — proposed] owner policy flag to *block* instead of warn
> for Souls that need the stricter trade.

## Deprecation policy

- A deprecated schema field or error code stays in the registry marked
  deprecated for **two minor versions** before removal; removal changes
  the protocol version (T14 is the tripwire)
- A deprecated adapter qualification stays in the matrix marked
  deprecated; new qualifications refuse to claim profiles the harness
  no longer supports
- Paper versions: papers are immutable records; superseded drafts move to
  [archive](../archive/soul-platform-draft-0.3.md) with a pointer from the
  [current paper](../papers/soul-platform-draft-0.4.md)

## Platform release cadence

Tied to stages, not dates: Stage 0 contract baseline → Stage 1 local
vertical slice → 2a member isolation → 2b brokered adapters → 3 operator
pilot → 4 portability/relay. Exit evidence per stage:
[repository plan](../papers/repository-plan-2026-10-24.md#2-cross-repository-sequence).

## What enterprises can pin

- A Soul definition digest (per installation)
- Adapter version + qualification manifest digest
- The compatibility matrix row for their harness set (§12)
- Protocol version accepted at Hello (hq/v1, wire/v1)
