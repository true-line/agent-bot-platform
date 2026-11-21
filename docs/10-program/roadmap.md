---
Status: Draft
Doc-Type: plan
Owner: product-owner
Last-Reviewed: 2026-11-21
Sources: S6 §13; S7 §2
---

# Roadmap

Stages exit on evidence. S6 estimates the dates. [PDR-0085](../04-decisions/PDR-0085-macos-first-protected-pilot.md) sets the host order.

## Stages

| Stage | Planning range | Deliverable | Exit evidence | Recorded state |
|---|---|---|---|---|
| 0 Contract baseline | Weeks 1 to 2 | Glossary, schemas, fixtures, threat model, compatibility inventory, traceability | Shared fixtures validate in runtime and broker (T14) | The owner confirmed exit by approving [closeout PR #79](https://github.com/true-line/agent-bot-platform/pull/79), which closed [#66](https://github.com/true-line/agent-bot-platform/issues/66). See [evidence](#stage-0-evidence-and-remaining-work). |
| 1 Local vertical slice | Weeks 3 to 5 | One Soul, two members, local admission, task ledger, fake adapters | One task completes with scoped proposals and one final commitment | Exit evidence complete 2026-11-17; approval of [#67](https://github.com/true-line/agent-bot-platform/issues/67) confirms exit. T04/T05/T20 passed under `managed-cooperative` ([soul-conformance PR #7](https://github.com/true-line/soul-conformance/pull/7)). [PR #10](https://github.com/true-line/soul-conformance/pull/10) [post-merge CI](https://github.com/true-line/soul-conformance/actions/runs/44104254218) passed 31 tests and `hello.soul` against the pinned runtime and real HQ. Clean reports: [artifact 14336598815](https://github.com/true-line/soul-conformance/actions/runs/44104254218/artifacts/14336598815), ZIP SHA-256 `3449cc028f36a3653de16d1fd23346df65138d31bfe0fb1fb2bc0a1fa0baeeed`. Cooperative only; Stage 2a retains the protected-host gate. |
| 2a Member isolation | Weeks 6 to 7 | HQ starts the Soul through the Soul runner; HQ-hosted comms binds its local agents; macOS caller binding, isolation, key custody and egress control | On the declared Mac, an HQ-started Soul passes T01–T03 protected and T21 cooperative through the HQ-hosted comms path | In progress ([#68](https://github.com/true-line/agent-bot-platform/issues/68)); HQ Soul-start and macOS qualification pending. |
| 2b Brokered adapters | Weeks 8 to 9 | HQ-hosted comms routes live `wire/v1` and mirrors HQ's `task/v1`; brokered inference and service adapter, budgets, recovery, reconciliation | Unknown effects reconcile without blind replay through the live HQ broker | Not started |
| 3 Operator pilot | Weeks 10 to 12 | Minimal owner console and HQ CLI, enrollment, approvals, export and restore | Pilot targets met on qualified protected macOS | Not started |
| 4 Portability and relay | After pilot gates | HQ routes cross-machine agent traffic through Agent-Bot Harbor and the site/cloud relay path; coordinated moves | Fencing, transfer, partition and crypto conformance on the routed path | Not started |

## Communications delivery dependencies

`true-line/agent-bot-comms` is the renamed `qwts/agent-comms` repository
([PDR-0040](../04-decisions/PDR-0040-repository-renames-and-transfers-to-true-line.md)).
Its pre-platform standalone broker and peer-task flow do not establish the
platform's HQ communications center. The target is the HQ-hosted broker plugin
([PDR-0037](../04-decisions/PDR-0037-agent-bot-executables-are-daemon-plugins-behind-a-shim.md));
HQ owns admission and authority, and comms routes messages to local agents or,
when federation is qualified, through Agent-Bot Harbor. An agent using Harbor's
MCP tools may receive Harbor-enforced policy without becoming a managed Soul;
an IDE or CLI agent may have local hooks and guardrails without becoming one.
Only a Soul that HQ starts is managed
([PDR-0055](../04-decisions/PDR-0055-a-soul-is-managed-when-hq-starts-it.md)).

| Stage | Comms work that must land | Evidence before exit |
|---|---|---|
| 2a | Release and install matching HQ and comms plugin builds; start the Soul from HQ and bind each local agent to its own broker connection under the declared Machine-provisioned account layout. | Physical T01 refuses a copied handle before the operation and after HQ restart. The same HQ-started run supplies T02–T03 and the cooperative T21 replay; direct vendor or IDE trials are supporting evidence only. |
| 2b | Connect live broker delivery to `wire/v1` and mirror authoritative HQ task records through `task/v1`, then broker inference and service effects. | End-to-end routed frame, task receipt and recovery evidence on the exact released cohort. Codec fixtures alone do not satisfy this row. |
| 4 | Route cross-machine messages from HQ through Harbor and qualified relays; preserve the separate `control-v1` authority boundary. | Federation, partition and transfer tests on that route, including refusal of remote control over relay traffic. |

The published comms [v0.5.6 release](https://github.com/true-line/agent-bot-comms/releases/tag/v0.5.6) includes the HQ plugin packaging
([PR #323](https://github.com/true-line/agent-bot-comms/pull/323)). A matching
HQ release, installation, and physical run remain Stage 2a evidence gates. Live `wire/v1` delivery
remains tracked in [comms #300](https://github.com/true-line/agent-bot-comms/issues/300).
Neither a green plugin fixture nor an older standalone-broker release is a
Stage 2a physical result. [DRIFT-018](../00-governance/drift-register.md#drift-018-profile-values-say-managed-for-souls-hq-does-not-start)
tracks released profile values that still say `managed` for externally started
Souls; do not infer managed status from that label alone.

## Stage 0 evidence and remaining work

The detailed contract, pilot and independent T14 evidence is in the
[Stage 0 evidence record](stage-0-evidence.md).

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
