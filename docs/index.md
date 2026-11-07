---
Status: Draft
Doc-Type: index
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
---

# Soul Agent Platform

The single source of truth for the Soul Agent Platform: its requirements, architecture, cross-repository decisions and verification plan. Component repositories implement what is recorded here and link to it rather than keeping their own copies.

## Start where you are

| I am | Start with | Then |
|---|---|---|
| An agent changing any repository | [Authority and ownership](00-governance/authority-and-ownership.md) | [Repository catalog](03-architecture/repository-catalog.md), [seams](03-architecture/seams.md), [drift register](00-governance/drift-register.md) |
| The owner deciding something | [Decisions](04-decisions/README.md) | [Decision log](04-decisions/decision-log.md), [change control](00-governance/change-control.md) |
| A platform engineer | [Architecture](03-architecture/README.md) | [Requirements](02-requirements/product-requirements.md), [traceability](02-requirements/traceability-matrix.md) |
| A security reviewer | [Threat model](05-security-privacy/threat-model.md) | [Key boundaries](05-security-privacy/key-boundaries.md), [data flow and retention](05-security-privacy/data-flow-and-retention.md) |
| A test author | [Test strategy](07-verification/test-strategy.md) | [Conformance catalog](07-verification/conformance-catalog.md) |
| An operator | [Quickstart](user-guide/tutorials/quickstart.md) | [User guide](user-guide/README.md) |
| An adapter developer | [Adapter qualification](user-guide/adapters/adapter-qualification.md) | [Render plugins](user-guide/adapters/render-plugins.md), [hq/v1](03-architecture/interfaces/hq-v1.md) |

## Lifecycle map

| Section | Answers |
|---|---|
| [00 Governance](00-governance/README.md) | Which source wins, how records change, how components stay aligned |
| [01 Concept](01-concept/README.md) | Why the product exists, for whom, and what the MVP includes |
| [02 Requirements](02-requirements/README.md) | What must be true, and how each requirement is verified |
| [03 Architecture](03-architecture/README.md) | Trust domains, repositories, seams and interfaces |
| [04 Decisions](04-decisions/README.md) | Platform decisions that bind more than one repository |
| [05 Security and privacy](05-security-privacy/README.md) | Threats, keys, data flow and retention |
| [06 Intelligence](06-intelligence/README.md) | Memory, bounded improvement, evaluation |
| [07 Verification](07-verification/README.md) | Test levels, stage gates, conformance tests |
| [08 Release](08-release/README.md) | Versioning and release evidence |
| [09 Operations](09-operations/README.md) | Support and cross-repository runbooks |
| [10 Program](10-program/README.md) | Stages, work packages, risks |

## Five things worth knowing first

1. **The Soul is the unit.** One stable Soul ID; members, installations, runtimes, sessions and revisions are attributed separately ([glossary](glossary.md)).
2. **HQ is the enforcement point.** A trusted supervisor admits runtimes, and a broker mediates protected operations outside the agent shell's trust domain ([trust domains](03-architecture/trust-domains-and-profiles.md)).
3. **Credentials never enter the package.** HQ holds keys; `Equip` returns references, never secrets ([credentials](user-guide/how-to/credentials.md)).
4. **The two profiles are not equivalent.** Linux runs *protected*; macOS runs *cooperative*, where hostile-member containment is not assured, and receipts say which is in force ([profiles](03-architecture/trust-domains-and-profiles.md#protected-vs-cooperative)).
5. **Everything is receipted.** A protected action produces a receipt with task, caller, destination and settled cost; an effect whose outcome is lost is reconciled, never blindly replayed ([lifecycle](03-architecture/lifecycle.md)).

## Status of this site

Every page is Draft or Proposed until the owner accepts it; the status is in each page's front matter. The [papers](papers/soul-platform-draft-0.4.md) are frozen sources, cited by ID (S1 to S10), and propose rather than decide. A section mark such as "S6 §4" means section 4 of whitepaper draft 0.4.
