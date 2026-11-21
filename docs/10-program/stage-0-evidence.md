---
Status: Draft
Doc-Type: report
Owner: product-owner
Last-Reviewed: 2026-11-21
Sources: S6 §13; S7 §2
---

# Stage 0 evidence and remaining work

The 2026-11-13 baseline is platform `2b14c0719051d5a23859656c07e75fb028502200`.
[The reconciliation issue](https://github.com/true-line/agent-bot-platform/issues/58)
records the earlier audit. [Platform #66](https://github.com/true-line/agent-bot-platform/issues/66)
records the completed Stage 0 gate. Migration row numbers refer to the
[HQ migration plan](https://github.com/true-line/agent-bot-hq/blob/main/docs/daemon-plugin-split.md#stage-0-contract-baseline-and-in-place-preparation-wp1).

| Boundary | Recorded evidence | Remaining work |
|---|---|---|
| Runtime contracts | [agent-bot-souls#6](https://github.com/true-line/agent-bot-souls/pull/6) applies the production codec to HQ, task and note boundaries, exercises all 33 positive and 55 negative schema/parse verdicts, JCS vectors, and T14 version/capability refusals. Its final reviewed head `cb3aa2162296c55fa878435685c06b4a1cf30dad` passed 67 tests and CI. | Authority and time decisions remain with HQ and the broker; the runtime does not claim those semantic refusals. |
| Broker contracts | [agent-bot-comms#301](https://github.com/true-line/agent-bot-comms/pull/301) exercises every pinned `wire/v1` and `task/v1` fixture through its codecs (PDR-0024). HQ's admission and SDK wire tests exercise unsupported-version and required-capability refusal. | Keep this component evidence distinct from a T14 `soul-conformance` report. |
| Identity-service link, migration row 10 | [agent-bot-hq#124](https://github.com/true-line/agent-bot-hq/pull/124) and [agent-bot#197](https://github.com/true-line/agent-bot/pull/197) supplied the transport foundation. [HQ #122 closeout](https://github.com/true-line/agent-bot-hq/issues/122#issuecomment-6927276012) records the approved artifact and populated trust pin, deployed matching public metadata, actual enrolled-HQ signed token/API success and refusal, and a custody-preserving retained-artifact rollback followed by restored linked operation. | Acceptance is limited to the declared cloud workspace. Key-window maintenance and any wider client rollout follow the component rollout record; this does not qualify every client or declare Stage 0 exit. |
| Durable notices, migration row 11 | [agent-bot-comms#314](https://github.com/true-line/agent-bot-comms/pull/314) and agent-bot-hq#124 supplied durable ingestion. [HQ #13 closeout](https://github.com/true-line/agent-bot-hq/issues/13#issuecomment-6927251608) accepts the declared pilot: installed MCP handoff through the default HQ consumer and live mailbox, service custody excluding independent direct consumers, consume-reply loss without replay, and same-artifact restart persistence. Scope/refusal, no-query-uplink and upstream-redelivery evidence remain separately identified component tests. | The pilot uses a protocol fixture adapter and an explicitly development-loaded comms plugin. Native harnesses, other hosts, production plugin bundling and protected-profile qualification are outside this acceptance. The possible lost caller handoff after local consumption is the accepted [PDR-0062](../04-decisions/PDR-0062-hq-notice-scope-and-legacy-consume-one.md) boundary, not an unresolved parity defect. |

The runtime's schema-valid negative fixtures `approval-record.expired`,
`hello.stale-epoch`, `hello.unaccepted-definition`, `hello.unsupported-profile`
and `wire-frame.stale-expiry` require authority or time context. Accepting their
record shape in the runtime is not evidence of accepting their requested effect.
The runtime's explicit semantic tests cover `hello.unsupported-version` and
`wire-frame.unknown-required-capability`.

The earlier runtime and broker fixture results above used soul-contracts v0.4.1
at `d9ca0731fbe7bbf7a29d066c8a23cd92717ee9bd`. The accepted pilot uses approved
HQ source `e8c3da0f6856332c49c26b5f85708d7ade9b222e` and installed identity
0.15.20, with genuine offline v0.5.0 contracts at
`b96239cc47571237f7064ddbcbd0edec8e365c6b` for HQ/MCP; Souls retains v0.4.1.
The component closeouts own the exact artifact, plugin, inventory and receipt
records. The host reports the released value `managed-cooperative`; that
observation does not resolve [DRIFT-018](../00-governance/drift-register.md#drift-018-profile-values-say-managed-for-souls-hq-does-not-start)
or establish a managed Soul under PDR-0055. No protected-profile claim is made.

The 2026-11-13 signed production token refusal remains historical evidence: at
that time the service published no key validity/status metadata. HQ #122's
closeout supplies the later reviewed trust, activation and rollback evidence.

## Independent T14 report and exit proposal

The [immutable report](https://github.com/true-line/soul-conformance/blob/29847d194d0b227b52942e7d265c177a919930e2/reports/T14/2026-11-16-accepted-platform-main.json)
records `pass`: 16 checks, 119 fixtures; clean suite `585a57e`, publication
`29847d1`, fresh platform `1500663` (full pins and verified hashes linked). N-1 is
explicitly not applicable, with zero executions, under
[Accepted PDR-0075](../04-decisions/PDR-0075-t14-supported-major-inventory-and-profile-evidence.md).

Original v0.4.1 cohort (separate from HQ #13 pilot): real HQ admission
sockets with fixture enrollment/clock/definitions and production runtime/broker
codecs, without live wire transport. Observed `managed-cooperative` makes no
protected-enforcement claim.

[PR #1](https://github.com/true-line/soul-conformance/pull/1) merged at
`34a2375c106d734cb59c17cd6370020268672b62`. [Post-merge CI](https://github.com/true-line/soul-conformance/actions/runs/43959463020)
passed 15 self-tests, 16 checks and 119 fixture verdicts against fresh platform
main. The [catalog](../07-verification/conformance-catalog.md) records T14 passing.
The [DRIFT-021 correction](../00-governance/drift-register-resolved.md#drift-021-t14-previous-major-and-profile-evidence)
merged before the owner approved [closeout PR #79](https://github.com/true-line/agent-bot-platform/pull/79),
confirming Stage 0 exit for this cohort.

Merged work is counted only where its implementation survives. In particular,
[agent-bot-identity#1418](https://github.com/true-line/agent-bot-identity/pull/1418)
reverted eight unrelated changes; their original merge status is not completion
evidence for this migration. The detailed issue-status corrections belong to the
[reconciliation issue](https://github.com/true-line/agent-bot-platform/issues/58)
and the affected component issues.
