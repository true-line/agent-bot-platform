---
Status: Draft
Doc-Type: plan
Owner: product-owner
Last-Reviewed: 2026-11-08
Sources: S6 §13; S7 §2
---

# Roadmap

Delivery runs in evidence-gated stages, each ending in an observable vertical slice. Calendar ranges are S6's planning estimates, not commitments. A stage exits on its evidence, never on its date.

## Stages

| Stage | Planning range | Deliverable | Exit evidence | State on 2026-11-08 |
|---|---|---|---|---|
| 0 Contract baseline | Weeks 1 to 2 | Glossary, schemas, fixtures, threat model, compatibility inventory, traceability | Shared fixtures validate in runtime and broker (T14) | In progress. Broker side met: agent-comms runs every wire/v1 and task/v1 fixture through its codecs ([agent-comms#301](https://github.com/qwts/agent-comms/pull/301), PDR-0024), and agent-bot-hq builds against the pinned soul-contracts v0.4.1 and refuses an unsupported version and an unknown required capability (T14, in its HQ admission and SDK wire tests). Runtime side not met: agent-bot-souls has no code yet. |
| 1 Local vertical slice | Weeks 3 to 5 | One Soul, two members, local admission, task ledger, fake adapters | One task completes with scoped proposals and one final commitment | In progress: HQ admission and the task service are in agent-bot-hq (its plan §9 rows 12 and 13, with T04, T05 and T20 component tests); the entry point in agent-bot-souls (row 14) remains |
| 2a Member isolation | Weeks 6 to 7 | Caller binding on the Linux reference host, per-member principals, egress block | Hostile-member suite passes under the protected label | Not started |
| 2b Brokered adapters | Weeks 8 to 9 | Brokered inference and service adapter, budgets, recovery, reconciliation | Unknown effects reconcile without blind replay | Not started |
| 3 Operator pilot | Weeks 10 to 12 | Minimal owner console and HQ CLI, enrollment, approvals, export and restore | Pilot targets met on the declared host | Not started |
| 4 Portability and relay | After pilot gates | Coordinated moves, macOS protected profile, site then cloud routing | Fencing, transfer, partition and crypto conformance | Not started |

## Work packages

| Package | Owner role | Depends on | Repositories |
|---|---|---|---|
| WP1 Contracts | protocol-maintainer | Source audit | soul-contracts, agent-bot-platform |
| WP2 HQ authority | security-implementer | WP1 | agent-bot-hq, agent-bot-machine, agent-bot |
| WP3 Soul runtime | runtime-implementer | WP1 | agent-bot-souls, soul-adapters, agent-bot-identity |
| WP4 Messaging and tasks | comms-implementer | WP1; integrates WP2 | agent-comms, agent-bot-hq |
| WP5 Memory and packages | portability-implementer | WP1, WP3, WP4 | soul-package, agent-bot-souls |
| WP6 Owner interface | product-implementer | WP2, WP3, WP4 | geniusbar, agent-bot-hq (HQ CLI) |
| WP7 Verification | verification-lead | Begins with WP1 | soul-conformance |

Every work package returns an implementation reference, changed contract versions, test commands and results, migration implications, unresolved decisions and a bounded next task (S6 section 13).

## Migration path

Strangler-style. Nothing new is built before soul-contracts ships fixtures; the existing agent-bot daemon keeps working at every step; its HQ half is retired only when both implementations pass the same soul-conformance run (S7 section 2). The repository moves that PDR-0002 proposes happen between stages, never inside one.
