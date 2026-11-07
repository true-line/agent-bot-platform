---
Status: Accepted
Doc-Type: governance
Owner: product-owner
Last-Reviewed: 2026-11-07
Decided-By: PDR-0001
---

# Authority and ownership

Every fact about the platform has exactly one home, and every home has a fixed rank. When two sources disagree an agent stops and records the conflict; it never chooses silently. This page is the map agents consult before writing anything.

## What belongs in this repository

Only what is true across repositories: product intent, the quality bar, the shape of the system, the contracts between parts, and decisions that bind more than one part. The test for any new page or decision is the same:

> If exactly one repository would have to change, it does not belong here.

A component's design, build, internal modules, local ADRs and changelog stay in that component. The platform links to them when a seam needs it and never copies them. This keeps the platform small enough to read whole and stops it from becoming a monolith of everyone's documentation.

## Where each fact lives

| Fact | Home | Form |
|---|---|---|
| Vision, scope, users | platform `docs/01-concept/` | Prose |
| Product requirements (R) and quality attributes (QA) | platform `registry/requirements.yaml` | Registry, generated pages |
| What each conformance test must prove (T) | platform `registry/tests.yaml` | Registry, generated pages |
| Glossary of platform terms | platform [glossary](../glossary.md) | Prose |
| Architecture, trust domains, enforcement profiles | platform `docs/03-architecture/` | Prose and diagrams |
| Repository charters and dispositions | platform `registry/repos.yaml` | Registry |
| Seams between repositories | platform `registry/seams.yaml` | Registry |
| Decisions binding two or more repositories | platform `docs/04-decisions/PDR-*.md` | Decision record |
| Security, privacy, intelligence and verification strategy | platform sections 05 to 07 ([security](../05-security-privacy/README.md), [intelligence](../06-intelligence/README.md), [verification](../07-verification/README.md)) | Prose |
| Release criteria and stage gates | platform `docs/08-release/`, `registry/tests.yaml` | Prose and registry |
| Exact bytes on the wire: schemas, fixtures, error codes | `soul-contracts` | JSON Schema, JSON |
| Executable tests and conformance results | `soul-conformance` | Code, reports |
| Component design, build, internals, local decisions | the component repository | Its own docs and ADRs |
| Engineering process: issues, branches, PRs, review, release | `qwts/qwts-agent-sop` | SOPs (linked through the governed block) |
| Source papers | platform `docs/papers/` and `docs/archive/`, pinned in `registry/sources.yaml` | Frozen conversions; originals held by the owner |

## Order of authority

When sources disagree, rank tells you which is the current description. It does not make the conflict acceptable: every conflict becomes a DRIFT entry.

1. **The owner's explicit instruction** in the current task.
2. **Accepted PDRs**, newest first.
3. **Approved requirements** in `registry/requirements.yaml`.
4. **Contracts in soul-contracts** for the shape of a record. A schema that contradicts a requirement is a defect in one of them, not a waiver.
5. **Accepted platform pages** (architecture, strategy, catalog).
6. **Component ADRs and specs**, within the limits set by items 1 to 5.
7. **Draft and Proposed platform pages.** They describe intent and may change.
8. **Papers and archive.** They are the reasoning behind a decision, not the decision.

Code shows what a component currently does. It never defines what the platform intends; a mismatch is a defect or a DRIFT entry.

## Moving a fact

A fact that lives in the wrong place moves in two steps. First the platform gains the controlled record, citing its source. Then the old location is replaced by a link at a pinned platform commit, in a PR to that repository. Until the second step lands, the drift register records both copies.
