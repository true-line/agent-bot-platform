---
Status: Draft
Doc-Type: reference
Owner: product-implementer
Last-Reviewed: 2026-11-05
---

# HQ CLI reference

> **Status: illustrative.** Draft 0.4 requires an HQ CLI (§3, §8) but
> names no verbs. WP6 delivers the real surface at Stage 3
> ([repository plan](../../papers/repository-plan-2026-10-24.md#2-cross-repository-sequence)).
> The verbs below are the **proposed** set from
> [Operator Questions](../../papers/operator-questions-2026-10-29.md); when WP6 lands, this page becomes
> the generated, authoritative reference.

## Souls

| Command | Purpose | Status |
|---|---|---|
| `hq soul create <name> --template <path>` | new Soul from template (new Soul ID) | proposed |
| `hq soul import <path>.soul` | import + validate before activation | proposed |
| `hq soul roles <name> --lead <a> --specialist <a>` | assign roles → new definition revision | proposed |
| `hq soul start / pause / resume / stop <name>` | lifecycle | proposed (ops are hq/v1, §5) |
| `hq soul export <name> --life --offline-artifacts` | package export | proposed |
| `hq soul chat <name>` | terminal chat entry (`agent-bot` side) | proposed |

## Grants, credentials, budgets

| Command | Purpose | Status |
|---|---|---|
| `hq grant add / revoke / list` | standing authority | proposed (record is Appendix A) |
| `hq credential add / rotate / revoke / audit secrets` | key store + boundary scan | proposed |
| `hq budget set <soul> --ceiling --working --maintenance` | spend ceilings | proposed (§8 model) |

## Tasks, receipts, revisions

| Command | Purpose | Status |
|---|---|---|
| `hq task offer / cancel` | directives and cancellation | proposed |
| `hq receipts <soul> [--task --destination --outcome unknown]` | receipt queries | proposed |
| `hq revision list / rollback <name> <digest>` | revision acceptance state | proposed |

## Dreams and evaluations

| Command | Purpose | Status |
|---|---|---|
| `hq dream grant / schedule / run / show` | dream grants + runs | proposed (grant shape is Appendix A) |

## Adapters and diagnostics

| Command | Purpose | Status |
|---|---|---|
| `hq adapters list` | version, qualified profile, primitive classes, last eval date | proposed |
| `hq doctor` | post-crash reconciliation report | proposed |
| `hq diag bundle <soul>` | diagnostics collection | proposed |

## Conventions

- Every mutating command produces an **owner-session-stamped record** (§4)
- Refusals are typed codes from the [error registry](../../03-architecture/interfaces/error-registry.md)
- Commands that change authority or definition require/produce an
  **approval record** bound to the digest (§8, T24)
