---
Status: Draft
Doc-Type: strategy
Owner: verification-lead
Last-Reviewed: 2026-11-17
Sources: S6 §13, §14; S7 §4
---

# Test strategy

How the platform proves it meets its requirements, from contract fixtures to the operator pilot. The strategy is platform-wide; each component repository keeps its own unit and integration tests and maps them to T-series IDs where they implement one.

## Test levels

| Level | Proves | Owned by | Runs in |
|---|---|---|---|
| Contract | Records validate against schemas; canonicalization is stable; N and N-1 both parse | soul-contracts | soul-contracts CI |
| Component | A repository's behavior, including its share of a T-series test | each component | its own CI |
| Conformance | The T-series tests, end to end across components | soul-conformance | soul-conformance CI and the reference hosts |
| Adversarial | A hostile member cannot obtain authority (T01 to T03 and the hostile-member suite) | soul-conformance | the declared macOS pilot host under the protected profile |
| Evaluation | A candidate revision beats its baseline on held-out tasks per eval cell | soul-conformance eval harness | dream runs and release candidates |
| Pilot | Functional and operational targets with real adapters | verification-lead with the pilot cohort | the declared pilot hosts |

## Entry and exit by stage

A stage exits when its required evidence and that of preceding stages pass on the exact supported host and adapter versions (S6 section 14). The first pilot and any protected claim require full protected qualification. Blocked or unenforced observations can support development profiles only.

| Stage | Exit evidence (S6 section 13) | Tests |
|---|---|---|
| 0 Contract baseline | Shared fixtures validate in both runtime and broker | T14 |
| 1 Local vertical slice | One task completes with scoped proposals and one final commitment | T04, T05, T20 |
| 2a Member isolation | Caller binding, Machine signing custody and host egress denial under protected enforcement, plus cooperative profile honesty | T01, T02, T03, T21 |
| 2b Brokered adapters | Unknown effects reconcile without blind replay | T06 to T11, T17 to T19, T23, T25, T26 |
| 3 Operator pilot | Pilot tasks meet functional and operational targets on qualified hosts | T16, T22, T24, T27 to T30 |
| 4 Portability and relay | Fencing, transfer, partition and cryptographic conformance | T12, T13, T15 |

Stage 1 acceptance requires T04, T05 and T20 to demonstrate their required semantic observations under `managed-cooperative`; a blocked, skipped or reported-as-unenforced observation is not a pass. That evidence qualifies task-source authority, deduplication and proposal/finalization semantics only and makes no protected-host containment claim. Protected qualification requires T01 to T03 under the protected profile on the designated Mac. T21 uses the cooperative profile and passes when every receipt names cooperative and protected claims are refused with `profile_insufficient`. A protected release claim requires the exact-cohort cumulative result. This clarification does not resolve the `managed-*` naming conflict recorded in [DRIFT-018](../00-governance/drift-register.md#drift-018-profile-values-say-managed-for-souls-hq-does-not-start).

**Delayed — Agent Comms verification.** The installed broker bind, caller
binding through Agent Comms, brokered turn, and cooperative broker receipts are
tracked in the [delayed stage](../10-program/roadmap.md#delayed-stage). Roadmap
placement is pending. Stage 2a retains T01–T03 and T21.

The full specification of each test is in the [conformance catalog](conformance-catalog.md); its requirement coverage is in the [traceability matrix](../02-requirements/traceability-matrix.md).

## Independence

The verification-lead (WP7) is independent of the implementers. Implementers propose changes to tests; the verification-lead merges them in soul-conformance (S7 section 3.9). A failing security requirement is recorded as a release blocker, never rewritten as success under the same profile name (S6 section 13).

## Evidence

Every result names the definition revision, policy digest, dependency versions, enforcement profile, host and adapter versions (S6 section 14). Results are published as a [release conformance report](../08-release/release-conformance-report.md). A defect links to the requirement or test it violates, and its fix re-runs the failing test.

## Environments

Protected macOS qualifies first. Linux and Windows qualify separately. Each result applies to its declared host and configuration. [Host priority](../04-decisions/PDR-0085-macos-first-protected-pilot.md) Stages 1 and 2 may use deterministic simulators for providers and services (S6 section 2); the pilot must use approved real adapters.
