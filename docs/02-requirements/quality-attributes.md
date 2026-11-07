---
Status: Draft
Doc-Type: requirements
Owner: product-owner
Last-Reviewed: 2026-11-07
Sources: S6 §4, §6, §7, §10, §14; S1
---

# Quality attributes

The platform is judged on five goals: security, privacy, intelligence, accuracy and extensibility. It also has a fixed accessibility bar. This page maps each goal to the requirements and tests that already cover it and names where coverage is missing. Missing coverage becomes QA requirements once the owner accepts them. The first, QA-A11Y-01, was accepted with PDR-0001.

## Coverage by goal

| Goal | What it means here | Requirements | Tests | Coverage |
|---|---|---|---|---|
| Security | Authority is enforced outside the model; no silent downgrade; one Soul-level ceiling | R2, R3, R5, R6, R8, R12 | T01, T02, T03, T04, T10, T11, T12, T16, T19, T20, T21, T24, T26 | Strong |
| Privacy | Data reaches only owner-approved destinations; derived data keeps its source restrictions; retention is bounded | R4 (destinations only) | T19 (traced only through R6); T09 untraced | Weak: no requirement covers disclosure, derived data or retention |
| Intelligence | The Soul improves through evaluated, owner-accepted candidates and never authorizes its own change | R4, R6 | T10, T22; T27 to T30 untraced | Partial: evaluation rules live only in S6 section 10 |
| Accuracy | Receipts, not notes, are evidence; consequential effects happen once and are reconciled, never replayed | R1, R8 | T05, T06, T07, T17 untraced | Partial: exactly-once and reconciliation have tests but no requirement |
| Extensibility | Vendor-neutral contracts; versioned seams with N and N-1; adapters and plugins qualify independently | R7, R10 | T14 | Partial: plugin and adapter contracts are repo-local or plan only |
| Accessibility | Every user interface the platform ships meets WCAG 2.2 level AA | QA-A11Y-01 | None | Weak: no test or verification method yet |

Reliability (R9), operability (R11) and portability (R12) are tracked as secondary attributes in the [product requirements](product-requirements.md).

## Gaps to close

Each gap names the source text that a QA requirement would promote. The owner accepts or rejects them through a Decisions discussion; the [traceability matrix](traceability-matrix.md) shows the untraced tests.

- **Privacy.** S6 section 4 (data restrictions and approved destinations), T09 (destination change) and T19 (taint egress), and S1's rule that embeddings inherit the source restrictions of what they embed. The platform also has no retention requirement beyond [data flow and retention](../05-security-privacy/data-flow-and-retention.md).
- **Accuracy.** T05 to T07 and T17 prove deduplication, reconciliation and fencing, but no requirement says a consequential effect happens at most once. S6 section 10 says notes are memory, not evidence; no requirement says so.
- **Intelligence.** T27 to T30 (version coverage, partial cells, dream limits, source chains) verify S6 section 10, which has no requirement of its own beyond R4 and R6.
- **Extensibility.** The HQ plugin contract and the render-plugin API are seams without schemas; see [seams](../03-architecture/seams.md).
- **Accessibility.** QA-A11Y-01 does not yet say which interfaces are in scope or how each is checked. WP7 proposes the method. Owner products such as GeniusBar are outside the platform and set their own bar.

## Measures

S6 section 14 proposes pilot targets, all hypotheses until measured: first useful task within 30 minutes of account setup; at least 80 percent completion on 50 bounded tasks; zero unauthorized effects in the negative suite; complete receipts for every protected write; p95 under 50 ms for local authorization and durable enqueue on the declared reference machine.
