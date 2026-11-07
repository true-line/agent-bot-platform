---
Status: Draft
Doc-Type: strategy
Owner: verification-lead
Last-Reviewed: 2026-11-07
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
| Adversarial | A hostile member cannot obtain authority (T01 to T03 and the hostile-member suite) | soul-conformance | the Linux reference host under the protected profile |
| Evaluation | A candidate revision beats its baseline on held-out tasks per eval cell | soul-conformance eval harness | dream runs and release candidates |
| Pilot | Functional and operational targets with real adapters | verification-lead with the pilot cohort | the declared pilot hosts |

## Entry and exit by stage

A stage exits only when every test gated at or before it passes on the exact supported host and adapter versions (S6 section 14). "Blocked or reported as unenforced" passes a weaker development profile, never the protected one.

| Stage | Exit evidence (S6 section 13) | Tests |
|---|---|---|
| 0 Contract baseline | Shared fixtures validate in both runtime and broker | T14 |
| 1 Local vertical slice | One task completes with scoped proposals and one final commitment | T04, T05, T20 |
| 2a Member isolation | Hostile-member suite passes under the protected label | T01, T02, T03, T21 |
| 2b Brokered adapters | Unknown effects reconcile without blind replay | T06 to T11, T17 to T19, T23, T25, T26 |
| 3 Operator pilot | Pilot tasks meet functional and operational targets | T16, T22, T24, T27 to T30 |
| 4 Portability and relay | Fencing, transfer, partition and cryptographic conformance | T12, T13, T15 |

The full specification of each test is in the [conformance catalog](conformance-catalog.md); its requirement coverage is in the [traceability matrix](../02-requirements/traceability-matrix.md).

## Independence

The verification-lead (WP7) is independent of the implementers. Implementers propose changes to tests; the verification-lead merges them in soul-conformance (S7 section 3.9). A failing security requirement is recorded as a release blocker, never rewritten as success under the same profile name (S6 section 13).

## Evidence

Every result names the definition revision, policy digest, dependency versions, enforcement profile, host and adapter versions (S6 section 14). Results are published as a [release conformance report](../08-release/release-conformance-report.md). A defect links to the requirement or test it violates, and its fix re-runs the failing test.

## Environments

The Linux reference host is the protected-profile environment from Stage 2a. macOS runs the cooperative profile until its protected profile qualifies in Stage 4. Stages 1 and 2 may use deterministic simulators for providers and services (S6 section 2); the pilot must use approved real adapters.
