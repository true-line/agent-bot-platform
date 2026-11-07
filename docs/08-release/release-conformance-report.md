---
Status: Draft
Doc-Type: report
Owner: verification-lead
Last-Reviewed: 2026-11-05
Scope: T01–T30 conformance suite + release reports
---

# Release and conformance report

What every release must prove, and the shape of the report enterprises
can demand. T01–T30 are **product conformance tests** — not Soul
evaluations (which are per-Soul, ATIF-based, §9–§10).

## Conformance suite (T01-T30)

| Stage | Tests | What they prove |
|---|---|---|
| 0 | T14 | version mismatch refusal (contract baseline gate) |
| 1 | T04, T05, T20 | scoped proposals → one final commitment; dedup |
| 2a | T01, T02, T03, T21 | hostile-member containment, key boundary, protected label honesty |
| 2b | T05–T11, T17–T19, T23, T25, T26 | brokered adapters, budgets, reconciliation without blind replay |
| 3 | T16, T22, T24, T27–T30 | package attack, pilot ops, approval digest binding, eval coverage |
| 4 | T12, T13, T15 | partition, crypto conformance, transfer |

Plus: the hostile-member suite (its own category under the protected
label), simulators, `hello.soul`, and the eval harness — all in
`true-line/soul-conformance` (30 suite stubs scaffolded today;
[repository plan](../papers/repository-plan-2026-10-24.md#1-repository-map)).

## Release report contents

Specified inputs: test results **name revision, policy digest, dependency
versions, and profile** (§14). Release prerequisites (§15) include
credential rotation/revocation hygiene and cost per accepted task.

A release report contains:

1. Stage-exit evidence table (above) with run dates and digests
2. Per-host results: T02 key boundary on each supported host
3. Adapter qualification manifests, signed, with eval dates (§9)
4. Compatibility matrix snapshot (§12)
5. Diagnostics bundle sample + redaction proof (§12)
6. Open `[UNSPECIFIED]` items promoted or retired this release
7. Known-limitation list (see [support](../09-operations/support.md#known-limitation-disclosures))

## Where the report lives

Per release, in `true-line/soul-conformance/release-reports/`, linked
from the release notes. This governance page links the latest.

## Stage-exit docs gate

A stage is not exited until its docs land (see repository
[README conventions](https://github.com/true-line/soul-docs)):

| Stage | Docs that must exist |
|---|---|
| 0 | error registry page regenerated; wire/hq protocol pages current |
| 1 | quickstart runs green against hello.soul |
| 2a | trust-domains page matches enforced reality |
| 2b | adapter qualification + budgets pages current |
| 3 | **operator guide + CLI reference (real verbs) + this report** |
| 4 | transfer/portability guide; federation setup guide |
