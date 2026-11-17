---
Status: Draft
Doc-Type: report
Owner: verification-lead
Last-Reviewed: 2026-11-17
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
| 2a | T01, T02, T03, T21 | macOS pilot host containment and key boundary, cooperative label honesty |
| 2b | T05–T11, T17–T19, T23, T25, T26 | brokered adapters, budgets, reconciliation without blind replay |
| 3 | T16, T22, T24, T27–T30 | package attack, pilot ops, approval digest binding, eval coverage |
| 4 | T12, T13, T15 | partition, crypto conformance, transfer |

Plus: the hostile-member suite (its own category under the protected
label), simulators, `hello.soul`, and the eval harness — all in
`true-line/soul-conformance`; current implementation status is recorded in the
[conformance catalog](../07-verification/conformance-catalog.md).

## Release report contents

Specified inputs: test results **name revision, policy digest, dependency
versions, and profile** (§14). Release prerequisites (§15) include
credential rotation/revocation hygiene and cost per accepted task.

A release report contains:

1. Stage-exit evidence table (above) with run dates and digests
2. Per-host results, including the T02 key boundary on the declared macOS pilot host and independently on each additional supported host
3. Adapter qualification manifests, signed, with eval dates (§9)
4. Compatibility matrix snapshot (§12)
5. Diagnostics bundle sample + redaction proof (§12)
6. Open `[UNSPECIFIED]` items promoted or retired this release
7. Known-limitation list (see [support](../09-operations/support.md#known-limitation-disclosures))
8. The platform commit SHA the evidence was checked against: the `main` commit each conformance run fetched ([PDR-0020](../04-decisions/PDR-0020-components-read-the-platform-at-main.md))

## Where the report lives

Per release, in `true-line/soul-conformance/release-reports/`, linked
from the release notes. Suite evidence can be published separately before a
release report is accepted.

The [T14 report published on 2026-11-16](https://github.com/true-line/soul-conformance/blob/29847d194d0b227b52942e7d265c177a919930e2/reports/T14/2026-11-16-accepted-platform-main.json)
passes for its declared v0.4.1 cooperative cohort against platform main
`15006630fbdc8c0dd7f951b66c2b033304810fd9`. The implementation and report merged in
[soul-conformance PR #1](https://github.com/true-line/soul-conformance/pull/1)
at `34a2375c106d734cb59c17cd6370020268672b62`; its
[post-merge qualification](https://github.com/true-line/soul-conformance/actions/runs/43959463020)
passed against fresh platform main. The [CI report artifact](https://github.com/true-line/soul-conformance/actions/runs/43959463020/artifacts/14272554749)
has ZIP SHA-256 `994ffb37d480e045a7169c9db619c4565f312ab58cb7c9e4c0f46bc718ce325f`.
These are bounded T14 acceptance evidence. The
[roadmap](../10-program/roadmap.md#independent-t14-report-and-exit-proposal)
records separate owner Stage 0 confirmation through approval of the closeout PR;
earlier merges did not grant that confirmation.

## Stage-exit docs gate

A stage is not exited until its docs land (see repository
[README conventions](https://github.com/true-line/soul-docs)):

| Stage | Docs that must exist |
|---|---|
| 0 | [error registry page](../03-architecture/interfaces/error-registry.md) regenerated; [wire](../03-architecture/interfaces/wire-v1.md)/[HQ](../03-architecture/interfaces/hq-v1.md) protocol pages current |
| 1 | quickstart runs green against hello.soul |
| 2a | trust-domains page matches enforced reality |
| 2b | adapter qualification + budgets pages current |
| 3 | **operator guide + CLI reference (real verbs) + this report** |
| 4 | transfer/portability guide; federation setup guide |
