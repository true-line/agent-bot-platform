---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-05
Normative-Source: true-line/soul-contracts (Appendix A schemas + fixtures)
---

# Protocol reference: hq/v1

The HQ control socket protocol: the owner-side control plane between HQ
clients (CLI, GeniusBar, agent-watcher) and the local authority.

> **Normative source:** schemas, fixtures, and the canonicalization vector
> live in `true-line/soul-contracts`. This page summarizes; the repo wins
> on conflict. Stage 0 shipped `hq/v1` Hello and the admission result with
> fixtures and CI ([repository plan](../../papers/repository-plan-2026-10-24.md#1-repository-map)).

## Operations

| Operation | Direction | Purpose | Specified |
|---|---|---|---|
| Hello | client → HQ | handshake; carries Soul + member + installation + runtime + session identity | §5, Stage 0 |
| Admission result | HQ → client | accept/refuse with typed code; names profile and definition digest | §5, §8 |
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

`hq/v1` is versioned in the frame; a version mismatch is refused with the
typed code proven by **T14** (version mismatch) — the soul-contracts
Stage 0 gate ([error registry](error-registry.md)).

## What this protocol deliberately does not do

- Carry secrets (references only)
- Enforce task semantics (the task state machine library decides nothing
  about authority; HQ calls its checks —
  [state machine](task-state-machine.md))
- Serve remote peers (federation runs over wire/v1 relays —
  [federation](../federation.md))
