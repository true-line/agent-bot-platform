---
Status: Draft
Doc-Type: plan
Owner: product-owner
Last-Reviewed: 2026-11-13
Sources: S6 §13; S7 §2
---

# Roadmap

Delivery runs in evidence-gated stages, each ending in an observable vertical slice. Calendar ranges are S6's planning estimates, not commitments. A stage exits on its evidence, never on its date.

## Stages

| Stage | Planning range | Deliverable | Exit evidence | Recorded state |
|---|---|---|---|---|
| 0 Contract baseline | Weeks 1 to 2 | Glossary, schemas, fixtures, threat model, compatibility inventory, traceability | Shared fixtures validate in runtime and broker (T14) | In progress; reviewed 2026-11-13. Runtime and broker fixture component evidence has merged. The migration still needs reviewed production signing keys and notice alias parity; see [Stage 0 evidence and remaining work](#stage-0-evidence-and-remaining-work). No stage exit is declared. |
| 1 Local vertical slice | Weeks 3 to 5 | One Soul, two members, local admission, task ledger, fake adapters | One task completes with scoped proposals and one final commitment | Exit evidence produced on 2026-11-09; the owner confirms the exit. The agent-bot-souls entry point (agent-bot-hq plan §9 row 14, [agent-bot-souls#2](https://github.com/true-line/agent-bot-souls/pull/2)) runs a lead and a specialist on fake adapters against the real HQ, with agent-bot-comms's broker plugin serving the member socket (row 13b, [agent-bot-comms#307](https://github.com/true-line/agent-bot-comms/pull/307)). In its tests the owner offers a task on HQ's control socket ([agent-bot-hq#106](https://github.com/true-line/agent-bot-hq/pull/106)), the specialist's answer is recorded as a proposal, and the lead makes one final commitment. HQ admission and the task service are plan rows 12 and 13, with T04, T05 and T20 component tests. |
| 2a Member isolation | Weeks 6 to 7 | Caller binding on the Linux reference host, per-member principals, egress block | Hostile-member suite passes under the protected label | Not started |
| 2b Brokered adapters | Weeks 8 to 9 | Brokered inference and service adapter, budgets, recovery, reconciliation | Unknown effects reconcile without blind replay | Not started |
| 3 Operator pilot | Weeks 10 to 12 | Minimal owner console and HQ CLI, enrollment, approvals, export and restore | Pilot targets met on the declared host | Not started |
| 4 Portability and relay | After pilot gates | Coordinated moves, macOS protected profile, site then cloud routing | Fencing, transfer, partition and crypto conformance | Not started |

## Stage 0 evidence and remaining work

Reviewed against platform `main` at `2b14c0719051d5a23859656c07e75fb028502200`.
These are component results, not a `soul-conformance` result or an owner-confirmed
stage exit. [The reconciliation issue](https://github.com/true-line/agent-bot-platform/issues/58)
tracks the audit. Migration row numbers refer to the
[HQ migration plan](https://github.com/true-line/agent-bot-hq/blob/main/docs/daemon-plugin-split.md#stage-0-contract-baseline-and-in-place-preparation-wp1).
Component implementation details remain in their repositories.

| Boundary | Merged evidence | Remaining work |
|---|---|---|
| Runtime contracts | [agent-bot-souls#6](https://github.com/true-line/agent-bot-souls/pull/6) applies the production codec to HQ, task and note boundaries, exercises all 33 positive and 55 negative schema/parse verdicts, JCS vectors, and T14 version/capability refusals. Its final reviewed head `cb3aa2162296c55fa878435685c06b4a1cf30dad` passed 67 tests and CI. | Authority and time decisions remain with HQ and the broker; the runtime does not claim those semantic refusals. |
| Broker contracts | [agent-bot-comms#301](https://github.com/true-line/agent-bot-comms/pull/301) exercises every pinned `wire/v1` and `task/v1` fixture through its codecs (PDR-0024). HQ's admission and SDK wire tests exercise unsupported-version and required-capability refusal. | Keep this component evidence distinct from a T14 `soul-conformance` report. |
| Identity-service link, migration row 10 | [agent-bot-hq#124](https://github.com/true-line/agent-bot-hq/pull/124) and [agent-bot#197](https://github.com/true-line/agent-bot/pull/197) provide signer-backed transport, authenticated responses and configured key-metadata validation. | HQ's [release pin](https://github.com/true-line/agent-bot-hq/blob/main/governance/server-keys.json) is empty. The [rollout policy](https://github.com/true-line/agent-bot/blob/main/docs/server-response-signing-rollout.md) is Proposed; approved validity metadata, activation and real enrolled-client evidence remain outstanding ([agent-bot-hq#122](https://github.com/true-line/agent-bot-hq/issues/122)). |
| Durable notices, migration row 11 | [agent-bot-comms#314](https://github.com/true-line/agent-bot-comms/pull/314) and agent-bot-hq#124 provide configured custody-before-ack, crash recovery and notice-ID deduplication in HQ's store. | The legacy identity `take_inbox` path remains at-most-once. Alias parity is still open ([agent-bot-hq#13](https://github.com/true-line/agent-bot-hq/issues/13)); the durable consumer alone does not satisfy it. |

The runtime's schema-valid negative fixtures `approval-record.expired`,
`hello.stale-epoch`, `hello.unaccepted-definition`, `hello.unsupported-profile`
and `wire-frame.stale-expiry` require authority or time context. Accepting their
record shape in the runtime is not evidence of accepting their requested effect.
The runtime's explicit semantic tests cover `hello.unsupported-version` and
`wire-frame.unknown-required-capability`.

Both consumers use soul-contracts v0.4.1 at
`d9ca0731fbe7bbf7a29d066c8a23cd92717ee9bd`; the runtime and HQ verify the
same release digest. The [conformance catalog](../07-verification/conformance-catalog.md)
records component tests separately from the executable suite's implementation
status. On 2026-11-13 a production token refusal carried a valid signature, but
the hosted service published no key validity/status metadata; that observation does not
supply the missing reviewed release trust.

Merged work is counted only where its implementation survives. In particular,
[agent-bot-identity#1418](https://github.com/true-line/agent-bot-identity/pull/1418)
reverted eight unrelated changes; their original merge status is not completion
evidence for this migration. The detailed issue-status corrections belong to the
[reconciliation issue](https://github.com/true-line/agent-bot-platform/issues/58)
and the affected component issues.

## Work packages

| Package | Owner role | Depends on | Repositories |
|---|---|---|---|
| WP1 Contracts | protocol-maintainer | Source audit | soul-contracts, agent-bot-platform |
| WP2 HQ authority | security-implementer | WP1 | agent-bot-hq, agent-bot-machine, agent-bot |
| WP3 Soul runtime | runtime-implementer | WP1 | agent-bot-souls, soul-adapters, agent-bot-identity |
| WP4 Messaging and tasks | comms-implementer | WP1; integrates WP2 | agent-bot-comms, agent-bot-hq |
| WP5 Memory and packages | portability-implementer | WP1, WP3, WP4 | soul-package, agent-bot-souls |
| WP6 Owner interface | product-implementer | WP2, WP3, WP4 | geniusbar, agent-bot-hq (HQ CLI) |
| WP7 Verification | verification-lead | Begins with WP1 | soul-conformance |

Every work package returns an implementation reference, changed contract versions, test commands and results, migration implications, unresolved decisions and a bounded next task (S6 section 13).

## Migration path

Strangler-style. Nothing new is built before soul-contracts ships fixtures; the existing agent-bot daemon keeps working at every step; its HQ half is retired only when both implementations pass the same soul-conformance run (S7 section 2). The repository moves that PDR-0002 proposes happen between stages, never inside one.
