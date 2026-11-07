---
Status: Draft
Doc-Type: index
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Sources: S6 §10; S1
---

# Intelligence

How a Soul remembers, learns and improves without ever authorizing its own change. This section is a stub on purpose: the rules exist only in whitepaper draft 0.4 (S6 section 10) and have not yet been promoted into requirements, so nothing here is normative beyond R4 and R6.

## What S6 proposes

- **Memory.** Knowledge records are the durable memory. Embeddings are derived indexes that can be rebuilt, and are never a record of permission. Typed notes (decision, finding, commitment, open question, handoff) are self-reported and kept apart from broker receipts.
- **Bounded improvement.** A dream run is an admitted member with its own grant, budget and host-enforced network limits. It may change knowledge under that grant, but a change to the definition (primitives, instructions, policy, routes, roles) is only a candidate.
- **Evaluation.** Each candidate is evaluated per cell, meaning one role on one harness version and provider, against the current revision replayed in the same run. It must pass held-out tasks within an owner-set tolerance. The owner approves the candidate digest; rollback accepts the parent digest.
- **External references.** Harness² (X6) for propose, probe and compose; ATIF (X7) for curated evaluation trajectories.

## Coverage

| ID | What it covers |
|---|---|
| R4 | The owner assigns roles and data destinations; evaluations advise and never grant permission. Verified by T22 (self-activation). |
| R6 | External material stays data, including through summarization, delegation and sleep. Verified by T04, T10 (memory laundering) and T19. |
| T27 to T30 | Version coverage, partial cell failure, dream limits, source chain. S6 maps no requirement to them; WP1 assigns one. |

## What is open

S6 records a conflict between its sources about how long ordinary notes last, and proposes a 30-second batched write. The evaluation tolerance, the held-out curation rule and delegated acceptance are unspecified. Each becomes a requirement through a Decisions discussion before any repository implements it; until then a repository cites S6 section 10 and says the behavior is proposed.
