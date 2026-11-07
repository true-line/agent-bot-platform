---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-07
Date: 2026-11-07
Discussion: https://github.com/true-line/agent-bot-platform/discussions/1
Affects-Repos: [agent-bot-platform, soul-contracts, soul-conformance, agent-bot, agent-bot-daemon, agent-bot-machine, agent-comms, agent-bot-identity, agent-bot-souls, soul-package, soul-adapters, geniusbar]
Affects: [governance, scope]
---

# PDR-0001 The platform repository is the product source of truth

true-line/agent-bot-platform holds the product's requirements, architecture, cross-repo decisions, quality strategy and source papers. Every component repository builds against it at a pinned commit and stops carrying its own copies.

## Context

The platform is specified across five papers (S1 to S5), a consolidated whitepaper (S6) and a repository plan (S7). Since then each repository has grown its own copy of the parts it needs. The 2026-11-07 survey found 15 conflicts between those copies, listed in the [drift register](../00-governance/drift-register.md): two wordings of R9, two repositories called HQ, two package layouts, two meanings of "Soul", and short labels such as `D4` and `R1` meaning different things in different files.

The org's governance does not define a home for decisions that bind several product repositories. ENG records cover engineering process across the whole org, and repository ADRs cover one repository. soul-contracts took on requirements, glossary, traceability and papers as well as schemas, but nothing outside the soul-* repositories reads it, and its requirements already lag the current whitepaper.

## Decision

1. **This repository owns** the vision and scope, product requirements and quality attributes, the traceability matrix, what each conformance test must prove, the architecture and trust model, the repository catalog and seams, platform decision records, the security, privacy, intelligence and verification strategy, release criteria, the roadmap and risks, the glossary and the frozen source papers. The [ownership table](../00-governance/authority-and-ownership.md) is the authoritative list.
2. **This repository stays small.** It accepts only what holds across repositories. A decision or page that would change exactly one repository belongs in that repository.
3. **soul-contracts narrows** to machine-readable contracts: schemas, canonicalization vectors, fixtures and the error registry. Its `traceability/`, `glossary/` and `papers/` become links to this repository.
4. **Component repositories link, never copy.** Each carries a platform block in its AGENTS.md pinned to a baseline commit, under the [component repository contract](../00-governance/component-repo-contract.md).
5. **Decisions** that meet the [platform test](../00-governance/change-control.md) are raised in the Decisions discussion category and recorded as PDRs numbered by their discussion.
6. **Registries are the source** for requirements, tests, repositories, seams, sources and identifiers. Pages generated from them are never edited by hand. `tools/check_platform.py` and `mkdocs build --strict` gate every change.
7. **Process stays in the SOP.** This repository links qwts/qwts-agent-sop through the governed block and records only its own deltas.

## Consequences

- Agents in any repository have one place to check before acting, and conflicts surface as drift entries instead of diverging silently.
- Requirement wording changes in one PR, and the generated traceability matrix changes with it.
- Every component repository needs a one-time PR to add the platform block and delete or link its copies. Until then the drift register carries the duplicates.
- soul-contracts loses scope it was created with; its CI must check that schemas cite requirement IDs that exist at the pinned platform commit.
- One more repository to keep current. The generator and the checker exist so that cost stays in tooling, not review time.
- The owner's acceptance becomes a bottleneck for normative changes. That is deliberate: Proposed pages still guide work, but only Accepted ones bind it.

## Alternatives considered

- **Keep soul-contracts as the home** for requirements and glossary. Rejected: it is a contracts repository with schema CI, its copy has already drifted, and decisions and architecture would still have no home.
- **Keep documentation in each repository.** That is the current state, and it produced the drift register.
- **Record platform decisions as ENG records** in the SOP. Rejected: ENG records govern engineering process for the whole org, and the SOP excludes product and architecture choices.
