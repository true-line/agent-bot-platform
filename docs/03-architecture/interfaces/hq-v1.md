---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-16
Normative-Source: true-line/soul-contracts (Appendix A schemas + fixtures)
---

# Protocol reference: hq/v1

The local HQ control and admission records connect owner clients and the Soul
entry point to HQ's authority. This reference distinguishes released record
shapes from the broader planned operation surface.

> **Normative source for record bytes:** the released [hq/v1 schemas](https://github.com/true-line/soul-contracts/tree/b96239cc47571237f7064ddbcbd0edec8e365c6b/schemas/hq/v1)
> and [fixtures](https://github.com/true-line/soul-contracts/tree/b96239cc47571237f7064ddbcbd0edec8e365c6b/fixtures).
> Platform authority follows [authority and ownership](../../00-governance/authority-and-ownership.md);
> a schema does not override an approved requirement. The bounded T14 report
> tests the v0.4.1 cohort; the notice pilot uses v0.5.0 on HQ/MCP. Their
> distinct evidence is recorded in the [roadmap](../../10-program/stage-0-evidence.md#stage-0-evidence-and-remaining-work).

## Operations

This is the specified surface, not a claim that every operation is implemented
or qualified by T14. Released schemas and component documentation determine
which records and commands are available.

| Operation | Direction | Purpose | Specified |
|---|---|---|---|
| Hello | client → HQ | handshake; carries Soul/definition/installation identity, offered versions/capabilities and requested role assignments | §5, Stage 0 |
| Admission result | HQ → client | successful admission names negotiated versions, profile and runtime; refusals use the separate typed-error record | §5, §8 |
| Admit / Equip / Brief / Ready / Lease | HQ ↔ entry point | the admission sequence; Equip returns credential **references**, never secrets | §5 |
| Grant add/revoke/list | owner → HQ | standing authority records | §8, Appendix A |
| Directive (task offer) | owner → HQ | assign work outside a chat | §7 |
| Approval record | HQ → owner → HQ | digest-bound single-action or bounded-class approval | §8, T24 |
| Lifecycle: start / pause / resume / stop / move | owner → HQ | supervision operations | §5 |
| Revision: accept / rollback | owner → HQ | definition and primitive revisions | §10 |
| Credential add / rotate / revoke | owner → HQ | key store management (verbs proposed) | §5, §11 |
| Diag bundle / doctor | owner → HQ | diagnostics + crash-recovery report (proposed verbs) | §12 |

Every approval, grant, and lifecycle request **records the owner session**
that issued it (§4). The socket is access-controlled to the installing
host account (§4).

## Identity model in the protocol

Five identifiers, attributed separately (§1): **Soul**, **member**,
**installation**, **runtime**, **session**. Census records all five; the
Soul ID is stable across revisions, hosts, and harness swaps; a new Soul
ID comes only from a template or a fork
([glossary](../../glossary.md), [sessions](../lifecycle.md#souls-agents-installations-runtimes-sessions)).

## Versioning

Hello identifies its record with `contract: "hq/v1"` and offers positive major
versions in `supported_versions`; HQ returns `negotiated_versions`. No common
required version produces `unsupported_version`. Unknown required capabilities
produce `required_capability_missing` at the relevant receiving boundary; these
are distinct [registered refusals](error-registry.md).

[Accepted PDR-0075](../../04-decisions/PDR-0075-t14-supported-major-inventory-and-profile-evidence.md)
and its inventory govern current/previous-major T14 coverage. A package release
number is not a protocol major, and a passing version check does not establish
protected enforcement.

## What this protocol deliberately does not do

- Carry secrets (references only)
- Enforce task semantics (the task state machine library decides nothing
  about authority; HQ calls its checks —
  [state machine](task-state-machine.md))
- Serve remote peers (federation runs over wire/v1 relays —
  [federation](../federation.md))
