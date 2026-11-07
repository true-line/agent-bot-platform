---
Status: Proposed
Doc-Type: index
Owner: product-owner
Last-Reviewed: 2026-11-07
---

# Decisions

Platform decision records (PDRs) are the decisions that bind more than one repository: requirements and scope, trust model, seams and repository topology. Everything else is decided, and recorded, in the one repository it affects.

## Platform decision records

| PDR | Title | Status |
|---|---|---|
| [PDR-0001](PDR-0001-platform-repository-is-the-product-source-of-truth.md) | The platform repository is the product source of truth | Accepted 2026-11-07 |
| [PDR-0002](PDR-0002-repository-topology-and-admission.md) | Repository topology and admission | Accepted 2026-11-07 |
| [PDR-0020](PDR-0020-components-read-the-platform-at-main.md) | Components read the platform at main | Accepted 2026-11-07; amends PDR-0001 |

## How a decision is made

1. Check the [platform test](../00-governance/change-control.md#is-it-a-platform-decision). If exactly one repository would change, stop and record it there.
2. Open a discussion in [Decisions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions). Its number is the PDR number.
3. Deliberate in the discussion; the owner marks the chosen answer.
4. Record it as `PDR-NNNN-slug.md` from the PDR template, Proposed, then Accepted when the owner approves the PR.

## Related pages

- [Decision log](decision-log.md): decisions made before this repository existed, and the open decisions the whitepaper already names.
- [Repository ADRs that constrain a seam](cross-repo-adr-index.md).
